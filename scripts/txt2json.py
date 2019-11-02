import subprocess
import json

class parse_raw_dat():
    def __init__(self, fin, fout):
        self.fin = fin
        self.fout = fout

    def read_dat(self):
        data = []
        with open(self.fin) as f:
            for line in f:
                id_end = line.find('|')
                json_id = line[0:id_end]
                begin = line.find('{')
                end = line.rfind('}')
                line = line[begin:end+1]
                try:
                    new = json.loads(line)
                    new['json_id'] = json_id
                    new['ts']
                    data.append(new)
                except Exception as e:
                    print(e)
#                       print(line)

        return data

    def write_dat(self, data):
        with open(self.fout, 'w') as f:
            counter = 1
            for line in data:
                counter +=1
                f.write(json.dumps(line))
                f.write('\n')

    def read_one_fout_row(self):
        with open(self.fout) as f:
            print(f.readline())

    def find_last_row(self):
        line = str(subprocess.check_output(['tail', '-1', self.fin]).rstrip())
        begin = line.find("'")
        end = line.find('|')
        last = line[begin+1:end]
        return int(last)

if __name__ == '__main__':

    fin = '/home/kalin/tmp.txt'
    fout = '/home/kalin/tmp.json'
    parser = parse_raw_dat(fin,fout)
    data = parser.read_dat()
    parser.write_dat(data)
