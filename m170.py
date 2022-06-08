import subprocess
import os

class M170:
    def __init__(self):
        os.system('sudo systemctl restart bluetooth')
        self.cmd = '''
        { printf 'scan on\n\n'
          printf 'connect C8:DF:84:37:B4:D8\n\n'
          printf 'menu gatt\n\n'
          printf 'select-attribute /org/bluez/hci0/dev_C8_DF_84_37_B4_D8/service001f/char0020\n\n'
          printf 'notify on\n\n'
          printf '\n\n'
          sleep 1
          
          
        } | bluetoothctl
        
        '''

    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        pulse_list = []
        oxygen_list = []
        pi_list = []
        result = {'pulse': 0, 'oxygen': 0, 'pi': 0}
        for i in range(50):
            #print('ttt')
            res = proc.stdout.readline()
            #print(res)
            data = res.decode('utf-8').strip()
            if data.find('fe 6a 76 52 04 81') != -1:
                data=(data.split(' ')[25:35])
                #data = data.split(" ")[3:12]
                if len(data[6]) > 0:
                    result = {'pulse': int(data[6], 16),
                              'oxygen': int(data[7], 16),
                              'pi': int(data[8], 16)/10}
                    return result
            
        
        return result


if __name__ == '__main__':
    m170 = M170()
    while 1:
        data = m170.get_sensor_data()
        print(data)


