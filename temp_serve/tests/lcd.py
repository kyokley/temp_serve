import LCD1602
import time
from threading import Thread
from sensor import Sensor

class LCD(object):
    def __init__(self):
        LCD1602.init(0x27, 1)

    def write(self, x, y, text):
        LCD1602.write(x, y, text)

    def clear(self):
        LCD1602.clear()

def run_it():
    lcd = LCD()
    sensor = Sensor()

    while True:
        lcd.write(0, 0, 'Temp: {}C'.format(sensor.get_celsius()))
        lcd.write(6, 1, '{}F'.format(sensor.get_fahrenheit()))

        time.sleep(30)
