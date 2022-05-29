import time
import RPi.GPIO as GPIO
def readmode():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31, GPIO.IN)
    GPIO.setup(33, GPIO.IN)
    GPIO.setup(35, GPIO.IN)
    GPIO.setup(37, GPIO.IN)
    mode_list=['temperature','oxygen','pressure','weight']
    gpio_list = [1,1,1,1]
    for i in range(10000):
        if i < 1000:
            continue
        if(GPIO.input(31)!=True):
            gpio_list[3] = 0
        if(GPIO.input(33)!=True):
            gpio_list[2] = 0
        if(GPIO.input(35)!=True):
            gpio_list[1] = 0
        if(GPIO.input(37)!=True):
            gpio_list[0] = 0
    mode = mode_list[0]
    for i,e in enumerate(gpio_list):
        if e:
            mode = mode_list[i]
            break
    return (mode)
if __name__ == "__main__":
    print(readmode())
