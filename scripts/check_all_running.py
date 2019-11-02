import subprocess

def check_all():
    s = subprocess.check_output('docker ps', shell=True)
    s = s.decode('utf-8').split('=')[0]
    run_bool = 0
    if s.find('dockerelk_elasticsearch_1') != -1:
        run_bool += 1
    if s.find('dockerelk_logstash_1') != -1:
        run_bool += 1
    if s.find('dockerelk_kibana_1') != -1:
        run_bool += 1
    if s.find('dockerelk_reverseproxy_1') != -1:
        run_bool += 1
    if run_bool == 4:
        return 1
    else:
        return 0

if __name__ == '__main__':
    res = check_all()
    print(res)
