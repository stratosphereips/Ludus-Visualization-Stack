
# Ludus Visualization Stack

The Ludus Visualization Stack uses the [Elastic stack](https://www.elastic.co/) to visualize data from gathered from [Ludus](https://github.com/stratosphereips/Ludus). Data from the Ludus database is backed up in the process. 

## Structure

ludus_viz.py :
1. gets user and database information from command line
2. starts filebeat
3. calls `get_data.py` to transfer data from psql database and copy it to mysql
4. calls `txt2json.py` to get last updated row in table
5. calls `break_up.py` to break up big json into multiple small jsons usable in Elastic stack

![alt text](https://github.com/xvanov/str/blob/master/ludus.png)

## Starting and Stopping

Run for first time (if dockers aren't set up - check with ```docker ps```)
(-bt option specifies the number of minutes for which the data should be backed up - e.g. every 10 minutes)
```
python3 ludus_viz.py -bt 10
```

Run (if dockers are already setup)
```
python3 keep_it_running.py -bt 10
```

Stop

find process id (PID) of ```ludus_viz.py``` or ```keep_it_running.py```:
```
ps ax | grep ludus_viz.py
```
end process:
```
kill PID
```
repeat finding the PID and killing the process for ```grep filebeat```

## Configuration

In `/filbeat`
  * filebeat: filebeat.yml
  
 In `/docker-elk`
   * `docker-compose.yml`
   * logstash: `config/logstash.yml`, `pipeline/logstash.conf`, `Dockerfile`
   * elasticsearch: `config/elasticsearch.yml`, `Dockerfile`
   * kibana: `config/kibana.yml`, `Dockerfile`
   
### Manually starting dockers
```ludus_viz.py``` build and/or starts dockers automatically. However, to manually start them:
1. in ```/docker-elk/``` run ```docker-compose up``` or ```docker-compose up -d``` for running in the background.
2. to stop: in ```/docker-elk/``` run ```docker-compose down```

#### Updating the stack
1. Change ELK_VERSION=7.0.1 in all configuration files to next version of ELK.
2. Run `docker-compose -f /docker-elk build` in terminal

## Ludus data format 
Postgres data table:

	   CREATE TABLE ludus_jsons (
	   json_id serial PRIMARY KEY,
	   record_id varchar NOT NULL,
	   router_id varchar NOT NULL,
	   complete_json json NOT NULL,
	   date_stored date
	   );
	   
Mysql data table:

	    CREATE TABLE ludus_jsons (
	    json_id SERIAL,
	    record_id VARCHAR(40) NOT NULL,
	    router_id VARCHAR(40) NOT NULL,
	    complete_json VARCHAR(10000) NOT NULL,
	    date_stored DATE,
	    PRIMARY KEY ( json_id )
	    );

Example of `complete_json` structure after breakup:
 
    {
	    "pkts_toclient": 1, 
	    "protcol": "udp", 
	    "bytes_toclient": 110, 
	    "alert": 1, 
	    "dport": 32792, 
	    "pkts_toserver": 1, 
	    "sport": 55847, 
	    "src_ip": "125.64.94.210", 
	    "bytes_toserver": 82, 
	    "severity": 2, 
	    "category": "Misc Attack", 
	    "signature": "ET DROP Dshield Block Listed Source group 1", 
	    "status": "closed", 
	    "id": "0000000B0001188B", 
	    "@timestamp": "2019-04-25T04:10:35.899835Z",
	    "tw_end": "2019-04-25 04:20:35.899835", 
	    "ts": 1556158836
    }
	
If `"alert": 0`, then `"severity"`, `"category"`, and `"signature"` are nor present.


<!--stackedit_data:
eyJoaXN0b3J5IjpbNjkzMjk5MjkzXX0=
-->
