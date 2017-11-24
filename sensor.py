import os

class Sensor(object):
    def __init__(self):
        self._bus = None
        self._setup()

    def _setup(self):
        for x in os.listdir('/sys/bus/w1/devices'):
            if x != 'w1_bus_master1':
                self._bus = x
                break

        if not self._bus:
            raise Exception('Failed to find temperature sensor')

    def read(self):
        location = '/sys/bus/w1/devices/{}/w1_slave'.format(self._bus)

        with open(location) as tfile:
            text = tfile.read()

        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000.0
        return temperature
