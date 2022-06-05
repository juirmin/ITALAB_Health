import subprocess


class FDK400:
    def __init__(self):
        self.cmd = '''
        { printf 'scan on\n\n'
          printf 'connect 07:B3:EC:03:99:BE\n\n'
          printf 'menu gatt\n\n'
          printf 'select-attribute /org/bluez/hci0/dev_07_B3_EC_03_99_BE/service0021/char0022\n\n'
          printf 'read\n\n'
          printf '\n\n'
          sleep 1 
         
        } | bluetoothctl
        
        '''

    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        result = {'pressure_S': 0, 'pressure_D': 0, 'pulse': 0}
        for i in range(50):
            res = proc.stdout.readline()
            data = res.decode('utf-8').strip()
            if data.find('ff fe 0a') != -1:
                data = data.split(" ")[3:14]
                result['pressure_S'] = int(data[7], 16)
                result['pressure_D'] = int(data[9], 16)
                result['pulse'] = int(data[10], 16)
                return result

        return result


if __name__ == '__main__':
    fdk400 = FDK400()
    while 1:
        data = fdk400.get_sensor_data()
        print(data)
