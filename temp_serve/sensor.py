import os
from datetime import datetime, timedelta

MINIMUM_UPDATE_TIME = 30

class SensorException(Exception):
    pass

class Sensor(object):
    def __init__(self):
        self._bus = None
        self._cached_temp = None
        self._last_update = None

        try:
            self._setup()
        except SensorException as e:
            print(e)

    def is_initialized(self):
        return bool(self._bus)

    def _setup(self):
        if self._bus:
            raise SensorException('Sensor is already initialized')

        for x in os.listdir('/sys/bus/w1/devices'):
            if x != 'w1_bus_master1':
                self._bus = x
                break

        if not self._bus:
            raise SensorException('Failed to find temperature sensor')

    def _read(self):
        if not self._bus:
            raise SensorException('Sensor is not initialized')

        if (not self._cached_temp or
                not self._last_update or
                (self._last_update + timedelta(seconds=MINIMUM_UPDATE_TIME) < datetime.now())):
            location = '/sys/bus/w1/devices/{}/w1_slave'.format(self._bus)

            with open(location) as tfile:
                text = tfile.read()

            secondline = text.split("\n")[1]
            temperaturedata = secondline.split(" ")[9]
            temperature = float(temperaturedata[2:])
            temperature = temperature / 1000.0
            self._cached_temp = temperature
            self._last_update = datetime.now()

        return self._cached_temp

    def get_celsius(self):
        return self._read()

    def get_fahrenheit(self):
        return self.get_celsius() * (9.0 / 5.0) + 32
