import subprocess


class M170:
    def __init__(self):
        self.cmd = '''
        { printf 'scan on\n\n'
          printf 'connect C8:DF:84:37:B4:D8\n\n'
          printf 'menu gatt\n\n'
          printf 'select-attribute /org/bluez/hci0/dev_C8_DF_84_37_B4_D8/service001f/char0020\n\n'
          printf 'notify on\n\n'
          printf '\n\n'
          sleep 1
          printf 'disconnect\n\n'
         
        } | bluetoothctl
        
        '''

    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        pulse_list = []
        oxygen_list = []
        pi_list = []
        result = {'pulse': 0, 'oxygen': 0, 'pi': 0}
        for i in range(150):
            res = proc.stdout.readline()
            data = res.decode('ascii').strip()
            if data.find('fe 6a 76 52 04 81') != -1:
                data = data.split(" ")[3:12]
                if len(data[6]) > 0:
                    pulse_list.append(int(data[6], 16))
                    oxygen_list.append(int(data[7], 16))
                    pi_list.append(int(data[8], 16)/10)
            if len(pulse_list) > 2:
                pulse_mean = sum(pulse_list)//len(pulse_list)
                oxygen_mean = sum(oxygen_list)//len(oxygen_list)
                pi_mean = sum(pi_list)//len(pi_list)
                result = {'pulse': pulse_mean,
                          'oxygen': oxygen_mean, 'pi': pi_mean}
                return result
        return result


if __name__ == '__main__':
    m170 = M170()
    while 1:
        data = m170.get_sensor_data()
        print(data)
