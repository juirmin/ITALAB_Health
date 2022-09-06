import os
import subprocess


class FDK300:
    def __init__(self):
        os.system('sudo systemctl restart bluetooth')
        self.cmd = '''
        { printf 'scan on\n\n'
          printf 'connect C6:05:04:07:4D:54\n\n'
          printf 'menu gatt\n\n'
          printf 'select-attribute /org/bluez/hci0/dev_C6_05_04_07_4D_54/service0020/char0023\n\n'
          printf 'read\n\n'
          printf '\n\n'
          sleep 1
         
        } | bluetoothctl
        
        '''

    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        result = {'temperature': 0}
        temperateure = 0
        for i in range(50):
            res = proc.stdout.readline()
            data = res.decode('utf-8').strip()
            if data.find('fe 6a 72 5a') != -1:
                data = data.split(' ')
                idx = data.index('fe')
                temp = str("").join(data[idx + 4:idx + 6])
                temperateure = int(temp, 16) / 100
                if temperateure < 50:
                    result['temperature'] = float(temperateure)
                    return result

        return result


if __name__ == '__main__':
    fdk300 = FDK300()
    while 1:
        data = fdk300.get_sensor_data()
        print(data)
