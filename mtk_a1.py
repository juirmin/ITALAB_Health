import subprocess
import os


class MTKA1:
    def __init__(self):
        os.system('sudo systemctl restart bluetooth')
        self.find_data = False
        self.cmd = '''
        { printf 'scan on\n\n'
          printf '\n\n'
          sleep 1
          printf 'quit'
         
        } | bluetoothctl
        
        '''

    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        for i in range(100):
            res = proc.stdout.readline()
            data = res.decode('utf-8').strip()
            data_index = data.find(
                'Device 6D:97:40:33:34:D0 ManufacturerData Value:')

            if self.find_data == True:
                raw_data = data.split(' ')
                raw_weight = ''.join(raw_data[-10:-8])
                weight = 0
                try:
                    weight = int(raw_weight, 16) / 10
                except:
                    pass
                if (weight <= 0) or (weight > 300):
                    continue
                self.find_data = False
                return {'weight': weight}

            if data_index != -1:
                self.find_data = True
        return {'weight': 0}


if __name__ == '__main__':
    scale = MTKA1()
    while 1:
        data = scale.get_sensor_data()
        print(data)
