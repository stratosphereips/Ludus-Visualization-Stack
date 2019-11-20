
# Ludus Visualization Stack

The Ludus Visualization Stack uses the [Elastic stack](https://www.elastic.co/) to visualize data from gathered from [Ludus](https://github.com/stratosphereips/Ludus). Data from the Ludus database is backed up in the process. 

## Structure

`ludus_viz.py`:
1. gets user and database information from command line
2. starts filebeat
3. calls `get_data.py` to transfer data from psql database and copy it to mysql
4. calls `txt2json.py` to get last updated row in table
5. calls `break_up.py` to break up big json into multiple small jsons usable in Elastic stack

![alt text](https://github.com/xvanov/str/blob/master/ludus.png)

## Credentials

1. cznic user password
2. ssh key to establish tunnel
3. remote psql database username and password
4. kibana and elastic passwords (same for both)
5. local mysql database username and password
6. ludus key (generated by `generate_key.py`) encrypts credentials 1-5 and stores them in local directory `/.stuff`

`generate_key.py`: generates a key that encrypts all the credentials
`my_encrypt.py`: encypts credentials input by user into `/.stuff` folder 
`my_decrypt.py`: decrypts credentials for use by `ludus_viz.py`

## Setup ssh tunnel
Before starting `ludus_viz.py` which copies the data from the remote database, an ssh tunnel has to be established. 
This is done by `keep_tunnel_open3.py` running by the `cznic` user as such:
```
nohup python3 keep_tunnel_open3.py
```
input ludus key and exit process wth ctrl-z 
```
ctrl-z
```
note job ID
```
jobs
```
disown process
```
disown -h %jobid
```
put process in background
```
bg %jobid
```

## Starting and Stopping

#### 1a. Run for first time (only run if dockers aren't set up - check with ```docker ps``` before)

-bt option specifies the number of minutes for which the data should be backed up - e.g. every 10 minutes
```
python3 ludus_viz.py -bt 10
```
input ludus key

#### 1b. Run (if dockers are already setup)
```
python3 keep_it_running.py -bt 10
```
input ludus key

#### 2. Run indefinitely
```
nohup python3 keep_it_running.py [or ludus_viz.py] -bt 10 
```
input ludus key and exit process wth ctrl-z 
```
ctrl-z
```
note job ID
```
jobs
```
disown process
```
disown -h %jobid
```
put process in background
```
bg %jobid
```

#### 3. Stop

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
   
#### Manually starting dockers
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
