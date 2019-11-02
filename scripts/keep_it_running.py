#!/usr/bin/env python3
'''
ludus_viz.py
Calls scripts: get_data.py, txt2json.py, breakup.py
Executes following steps in inifinite loop:
(1) run filebeat: Sends data to Elastic Stack when it is available
(2) call get_data.py: Copies data from new rows of postgres database to mysql every --backup_time minutes
(3) call txt2json.py: Converts data into a json format
(4) call breakup.py: Breaks up the data into Elastic Stack manegeable jsons (filebeat sends these jsons to the stack)

___START___:

MAKE FILE EXECUTABLE:
chmod +x ludus_viz.py
RUN IN BACKGROUND:
nohup /path/to/ludus_viz2.py &

RUN PROGRAM:
python3 ludus_viz.py -bt TIME_IN_MINUTES 

RUN PROGRAM INFINITELY:
python3 ludus_viz.py -bt TIME_IN_MINUTES 
CTRL+Z
jobs # note jobs id
disown -h %jobid
bg %jobid


___STOP___:

TO SEE PROCESS ID (PID):
ps ax | grep ludus_viz.py
TO END PROCESS:
kill PID
'''

import argparse
import time
import sys
import os

import get_data             # psql -> *.txt
import txt2json             # *.txt -> *.json
import breakup              # *.json -> *-brk.json
import check_all_running    # checks if dockers (E,L,K,nginx) are running
import my_decrypt

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i+1

def get_arguments():
    '''
    Gets arguments from user when running the script in terminal
    :return: all arguments argparse.ArgumentParser() object
    :backup_time: copy entries from postgres database every (backup_time) minutes
    '''
    parser = argparse.ArgumentParser()
#    parser.add_argument("-l", "--log_file", action="store", type=str) # program log file name
    parser.add_argument("-bt", "--backup_time", action="store", type=int) # in minutes
    return parser.parse_args(sys.argv[1:])

if __name__ == "__main__":
    print(time.asctime(), end=' ')
    print("Starting Ludus Visualizer Program (manages Elastic stack for Ludus data)")
    fin = "/home/kalin/str/.stuff/"
    fcreds = ['.db_user', '.db_pass', '.us_user', '.us_pass', '.ssh_pass', '.bdb_user', '.bdb_pass', '.kibana', '.elastic']
    decrypted = my_decrypt.decrypt(fin, fcreds)
    args = get_arguments()
    table_psql = 'ludus_jsons'
    table_mysql = 'ludus_jsons' # name of table in postgres and mysql databases
    local_dir = "/home/kalin/str/"
    filebeat_path = "{}filebeat-7.0.1-linux-x86_64/".format(local_dir)
    backup_path = "{}backup/".format(local_dir)
    docker_path = "{}docker-elk/".format(local_dir)
    script_path = "{}scripts/".format(local_dir)

#    os.system('export ELK_VERSION=7.0.1')

    with open(backup_path+'.last') as f: # remember last updated rows
        last = int(f.readline())

#    os.system('docker-compose -f {}docker-compose.yml up -d'.format(docker_path))
    print("Setting up Elastic Stack...")

#    time.sleep(60) # buffer
    #delete_cmd = """curl -X DELETE localhost:9200/_all -u 'elastic:{}' -p""".format("password")
     
    #k_cmd = """curl -H 'Content-Type: application/json' -XPUT -u 'elastic:password' -p 'localhost:9200/_xpack/security/user/kibana/_password' -d '{{"password" : "{}"}}'""".format(decrypted[7])
    #e_cmd = """curl -H 'Content-Type: application/json' -XPUT -u 'elastic:password' -p 'localhost:9200/_xpack/security/user/elastic/_password' -d '{{"password" : "{}"}}'""".format(decrypted[8])

#    with open(script_path+'data_mapping.txt') as maps:
#        print("\nDelete old index mapping")
#        os.system(delete_cmd)
#        print("\nSet up new kibana password")
#        os.system(k_cmd)
#        print("\nSet up new elasticsearch password")
#        os.system(e_cmd)
#        map_raw = maps.read()
#        print("\nPut new index mapping")
#        map_cmd ="""curl -H \'Content-Type: application/json\' -X PUT -d\'{}\' http://localhost:9200/tst_breakup_02/ -u 'elastic:{}' -p""".format(map_raw, decrypted[8])
#        os.system(map_cmd)

#    print("\nStarting filebeat")
#    time.sleep(25)
    os.system('nohup {}filebeat -e -c {}filebeat.yml -d "publish" &'.format(filebeat_path,filebeat_path))
    loop_i = 0
    while True:
        try:
            loop_i += 1
            ### (1) Get newly updated entries from postgres and copy them to mysql,
            ###     and create json file with the new data
            print('\n')
            print(time.asctime(), end=' ')
            print(' Looping #{}'.format(loop_i))
            print('     Starting: Step 1/4 backup database')
            running_bool = check_all_running.check_all()
            print(running_bool)
            if running_bool == 0:
                raise ValueError('Docker container(s) not running.')
                print('Docker container(s) not running.')
            file_path, new_last = get_data.backup(backup_path, decrypted, table_psql, table_mysql, last)
            if last == new_last:
                print('No new data')
            else:
                last = new_last
                print('Saved new data from postgres to {}'.format(file_path+'.txt'))
                print('Last json_id: {}'.format(new_last))
                print('     Finished: Step 1/4')
                print('     Starting: Step 2/4 parsing of new data')

                ### (2) Extract json from (1)
                parser = txt2json.parse_raw_dat(file_path+'.txt',file_path+'.json')
                data = parser.read_dat()
                parser.write_dat(data)

                ### (3) Break up (2) into Elastic-manegeable jsons
                print('New data in complete_json saved to {}'.format(file_path+'.json'))
                print('     Finished: Step 2/4')
                print('     Starting: Step 3/4 breakup of complete_jsons into smaller by-port jsons')
                leng = file_len(file_path+'.json')
                breakup.brk(file_path+'.json', file_path+'-brk.json', leng)
                print('     Finished: Step 3/4')
                print('     Starting: Step 4/4 deleting temporary files and sleep')

                ### (4) During pause feed (3) into logstash running at localhost:5000 via filebeat
                print('Sleeping for {} minutes (1st half of sleep time)'.format(args.backup_time/2))
                time.sleep(args.backup_time*60/2) # sleep for 1st half of the sleep time
                # delete temporary files
                print('Deleting temporary files')
                os.system('rm {}'.format(backup_path+'*'))
                print('Sleeping for {} minutes (2nd half of sleep time)'.format(args.backup_time/2))
                time.sleep(args.backup_time*60/2) # sleep for 2nd half of the sleep time
                print('     Finished: Step 4/4')
        except KeyboardInterrupt:
            with open(backup_path+'.last', 'w') as f:  # update last rows
                print(last, file=f)
            # os.system('docker-compose -f {}docker-compose.yml down'.format(docker_path))
            try:
                os.system('rm {}*'.format(backup_path))
            except:
                pass
            break
        except Exception as e:
            print('Error: {}'.format(e))
            with open(backup_path+'.last', 'w') as f: # update last rows
                print(last, file=f)
            # os.system('docker-compose -f {}docker-compose.yml down'.format(docker_path))
            try:
                os.system('rm {}*'.format(backup_path))
            except:
                pass
            break
