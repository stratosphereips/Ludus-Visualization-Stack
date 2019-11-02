import os
import time
import pexpect
import json
import check_all_running
import my_decrypt

fin = "/home/kalin/str/.stuff/"
fcreds = ['.elastic', '.db_pass']
decrypted = my_decrypt.decrypt(fin, fcreds)
counter = 0

while True:
    docker_up = check_all_running.check_all()

    data_command = """curl -XGET "http://localhost:9200/tst_breakup_02/_search" -H 'Content-Type: application/json' -d'
    {
       "size": 1,
       "sort": { "@timestamp": "desc"},
       "query": {
          "match_all": {}
       }
    }' -u elastic -p"""

    try:
        elk_data = pexpect.spawn(data_command)
        elk_data.expect("Enter host password for user 'elastic':")
        time.sleep(0.1)
        elk_data.sendline(decrypted[0])
        elk_data.expect(pexpect.EOF)
        dat = elk_data.before.decode("utf-8")
        idx = dat.find('@timestamp')
        dat = dat[idx+13:idx+36]
        last_time = dat.replace('T', ' ')
        data_message = "Last time data transfered to elasticsearch (UTC): {}".format(last_time)
    except:
        data_message = "Last time data transfered to elasticsearch: {}".format("Elasticsearch could not be reached")

    ssh_command = """psql --host=localhost --port=5432 --username=ludus --dbname=sentinel"""
    for i in range(20):
        try:
            ssh_check = pexpect.spawn(ssh_command)
            ssh_check.expect("Password for user ludus:")
            time.sleep(0.1)
            ssh_check.sendline(decrypted[1])
            time.sleep(1)
            ssh_check.sendline("\q")
            ssh_check.expect(pexpect.EOF)
            dat = ssh_check.before.decode("utf-8")
            idx = dat.find('sentinel')
            if idx == -1:
                ssh_up = 0
            else:
                ssh_up = 1
        except Exception as e:
            print(e)
            ssh_up = 0
        if ssh_up == 1:
            break
        else:
            time.sleep(10)

    if ssh_up == True:
        ssh_message = "SSH tunnel: OK"
    else: 
        ssh_message = "SSH tunnel: Broken"

    if docker_up == True:
        docker_message = "Dockers: {}".format("UP")
    else:
        docker_message = "Dockers: {}".format("DOWN")



    command = '''curl -X POST --data-urlencode 'payload={{\"channel\": \"@UGQA894V9\", \"username\": \"Ludus Notifier\", \"text\": \"{}\n{}\n{}\", \"icon_emoji\": \":ludus:\"}}' https://hooks.slack.com/services/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'''.format(ssh_message, docker_message, data_message)

    # command = '''curl -X POST --data-urlencode 'payload={\"channel\": \"@UGQA894V9\", \"username\": \"Ludus Notifier\", \"text\": \"One of the docker containers is down.\", \"icon_emoji\": \":ludus:\"}' https://hooks.slack.com/services/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'''
    print(command)
    if ssh_up != True or docker_up != True:
        os.system(command)
        counter = 0
    if counter%(12*24) == 0:
        os.system(command)
    time.sleep(5*60)
    counter+=1
