'''
breakup.py
Parsing program to flatten the nested data from the ludus_jsons in a meaningful way for Elastic stack
'''
import json
import time
import datetime, pytz

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def brk(fin, fout, length):
    '''
    Breaks up nested jsons from fin in the format (output of txt2json.py):
    {
      "port_info": 
      [
        {
          "pkts_to_server": int,
          "port": int,
          "protocol": str,
          "pkts_to_client": int,
          "status": str,
          "bytes_to_server": int,
          "bytes_to_client": int
        },...
      ],
      "tw_start": str,
      "tw_end": str,
      "GameStrategyFileName": str,
      "id": str,
      "ts": int,
      "instance_hash": str,
      "flows": [
        {
          "pkts_toclient": int,
          "protcol": str,
          "bytes_toclient": int,
          "alert": False,
          "dport": int,
          "pkts_toserver": int,
          "sport": int,
          "src_ip": str,
          "bytes_toserver": int
        },
        {
          "pkts_toclient": int,
          "protcol": str,
          "bytes_toclient": int,
          "alert": [{
            "severity": int,
            "category": str,
            "signature": str
          }, {
            "severity": int, 
            "category": str,
            "signature": str
          }],
          "dport": int,
          "pkts_toserver": int,
          "sport": int,
          "src_ip": str,
          "bytes_toserver": int,
          "flow_timestamp": str
        }, ...
      ]
    }
    Prints broken up jsons into fout in the format:
    {
      "instance_hash": str,
      "GameStrategyFileName": str,

      "alert": bool,
      "flow_timestamp":str,
      "severity": int,          # only if alert = True
      "category": str,          # only if alert = True
      "signature": str,         # only if alert = True
      "protcol": str,
      "dport": int,
      "pkts_toclient": int, 
      "bytes_toclient": int,
      "status": str,
      "sport": int,
      "src_ip": str,
      "pkts_toserver": int,
      "bytes_toserver": int,
      "tw_start": str,
      "tw_end": str,
      "@timestamp": str
    }

    :param fin:     input file path (json result of txt2json.py)
    :param fout:    output file path (json)
    '''
    output_file=open(fout, 'w')
    step = 0
    wae = 0
    with open(fin) as f:
        for line in f:
            json_decode = json.loads(line) 
            # flows
            try:
                local_timezone = pytz.timezone(json_decode['timezone'])
            except:
                local_timezone = pytz.timezone('CET') # default timezone is Prague, Czechia
                
            for flow in json_decode['flows']: 
                tmp_flow = flow.copy()
                
                #### alert
                proc = tmp_flow['alert']
                if proc == False or proc == []:
                    tmp_flow['alert'] = 0
                else:
                    alerts = proc.copy()
                    if type(alerts) != list():
                        alerts = [alerts]
                    tmp_flow['alert'] = 1
                    tmp_flow['number_alerts'] = len(alerts)
                    tmp_flow['severity'] = []
                    tmp_flow['category'] = []
                    tmp_flow['signature'] = []
                    
                    if tmp_flow['number_alerts'] > 1:
                        print(tmp_flow['number_alerts'])
                    try:
                        for i in range(len(alerts)):
                            tmp_flow['severity'].append(alerts[i]['severity'])
                            tmp_flow['category'].append(alerts[i]['category'])
                            tmp_flow['signature'].append(alerts[i]['signature'])
                    except:
                        alerts = alerts[0]
                        for i in range(len(alerts)):
                            tmp_flow['severity'].append(alerts[i]['severity'])
                            tmp_flow['category'].append(alerts[i]['category'])
                            tmp_flow['signature'].append(alerts[i]['signature'])
                    tmp_flow['severity'] = tmp_flow['severity']
                    tmp_flow['category'] = tmp_flow['category']
                    tmp_flow['signature'] = tmp_flow['signature']
                    try: 
                        tmp_flow['flow_timestamp'] = tw2date(tw2utc(json_decode["flow_timestamp"], local_timezone))
                    except:
                        pass

                ### DUCT TAPE START - solution: REORGANIZE jsons sent out from routers ####    
                
                #### port_info 
                for field in json_decode['port_info']:
                    try:
                        if  field['port'] == tmp_flow['dport']:
                            tmp_flow['status'] = field['status']
                    except Exception as e:
                        print(e)
                        
                #### router and flow metadata  
                try:
                    tmp_flow["instance_hash"] = json_decode["instance_hash"]
                except:
                    print("no instance hash - it's not fatal")
                tmp_flow["id"] = json_decode["id"]
                tmp_flow["GameStrategyFileName"] = json_decode["GameStrategyFileName"]
                tmp_flow["json_id"] = json_decode["json_id"]
                                
                # convert tw_start, tw_end and ts to Elastic-recognizable format              
                tmp_flow['tw_end'] = tw2date(tw2utc(json_decode['tw_end'], local_timezone))
                tmp_flow['tw_start'] = tw2date(tw2utc(json_decode['tw_start'], local_timezone))
                     
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(json_decode['ts']))
                naive = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                
                
                try:    #Daylight savings time problem (some times don't exist!)
                        # Yup, not a typo (some times like 2:35 on October 27th, 2019 in the Central European Time zone just don't exist - the clock went from 1:59 to 3:00 am)
                        # Who doesn't love time zones and daylight savings?!
                        # What is the solution?
                        # Lobby your local government to remove all timezones and DST to have one time everywhere on Earth!
                    local_dt = local_timezone.localize(naive, is_dst=None)
                except:
                    naive = naive + datetime.timedelta(hours=1)       
                    local_dt = local_timezone.localize(naive, is_dst=None)
                
                utc_dt = local_dt.astimezone(pytz.utc)
                utc_dt = str(utc_dt)
                plus = utc_dt.find('+')
                utc_dt = utc_dt[0:plus-0]
                tmp_flow['@timestamp'] = tw2date(utc_dt)
                tmp_flow['@timestamp'] = tmp_flow['tw_start']
                tmp_flow = json.dumps(tmp_flow)
                ### DUCT TAPE END ####    
                
                # print(tmp_flow)
                print(tmp_flow, file=output_file)
            step +=1
            percent_complete = step/length*100
            if percent_complete % 2 == 0:
                print('Line: ', step, ' Percent complete: ', percent_complete, '%')
    print('WAE: {}'.format(wae))
    
def tw2utc(proc, local_timezone):
    try:
        naive = datetime.datetime.strptime(proc, "%Y-%m-%d %H:%M:%S.%f")
    except:
        print(naive) 
        print(type(naive))

    try: #Daylight savings time problem (some times don't exist!)
        # Yup, not a typo (some times like 2:35 on October 27th, 2019 in the Central European Time zone just don't exist - the clock went from 1:59 to 3:00 am)
        # Who doesn't love time zones and daylight savings?!
        local_dt = local_timezone.localize(naive, is_dst=None)
    except:
        naive = naive + datetime.timedelta(hours=1)       
        local_dt = local_timezone.localize(naive, is_dst=None)

    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt = str(utc_dt)
    plus = utc_dt.find('+')
    return utc_dt[0:plus-0]

def make_aware(value, timezone):
    """
    Makes a naive datetime.datetime in a given time zone aware.
    """
    if hasattr(timezone, 'localize'):
        # This method is available for pytz time zones.
        return timezone.localize(value, is_dst=None)
    else:
        # Check that we won't overwrite the timezone of an aware datetime.
        if is_aware(value):
            raise ValueError(
                "make_aware expects a naive datetime, got %s" % value)
        # This may be wrong around DST changes!
        return value.replace(tzinfo=timezone)    

def tw2date(proc):
    '''
    Helper function to convert '%Y-%m-%d %H:%M:%S' datetime format into '%Y-%m-%dT%H:%M:%SZ' Elastic-stack datetime format
    :param proc:    datetime in '%Y-%m-%d %H:%M:%S' format
    '''
    proc = proc.replace(' ', 'T')
    proc = proc + 'Z'
    return proc
    
if __name__ == '__main__':
    start = time.time()
    fin = '/home/kalin/third.json'
    fout = '/home/kalin/tmp-brk.json'
#    fin = '/home/alex/Documents/dep/str_not/first_10000.json'
#    fout = '/home/alex/Documents/dep/str_not/first_10000-brk.json'
    length = file_len(fin)
    brk(fin, fout, length)
    end = time.time()
    print('Breakup took: ', (end-start)/60, 'minutes')



