import unittest
import mock
from datetime import datetime, timedelta

from temp_serve.sensor import (Sensor,
                               SensorException,
                               )

class TestInit(unittest.TestCase):
    def setUp(self):
        self._setup_patcher = mock.patch('temp_serve.sensor.Sensor._setup')
        self.mock_setup = self._setup_patcher.start()

    def tearDown(self):
        self._setup_patcher.stop()

    def test_init(self):
        Sensor()
        self.mock_setup.assert_called_once_with()

    def test_setup_raises(self):
        self.mock_setup.side_effect = SensorException('FAIL')

        Sensor()

class TestIsInitialized(unittest.TestCase):
    def setUp(self):
        self._setup_patcher = mock.patch('temp_serve.sensor.Sensor._setup')
        self.mock_setup = self._setup_patcher.start()

        self.sensor = Sensor()

    def tearDown(self):
        self._setup_patcher.stop()

    def test_initialized(self):
        self.sensor._bus = 'valid'

        self.assertTrue(self.sensor.is_initialized())

    def test_not_initialized(self):
        self.sensor._bus = None

        self.assertFalse(self.sensor.is_initialized())

class TestSetup(unittest.TestCase):
    def setUp(self):
        self.listdir_patcher = mock.patch('temp_serve.sensor.os.listdir')
        self.mock_listdir = self.listdir_patcher.start()

        self.mock_listdir.return_value = []

    def tearDown(self):
        self.listdir_patcher.stop()

    def test_already_initialized(self):
        sensor = Sensor()
        sensor._bus = 'valid'

        self.assertRaises(SensorException,
                          sensor._setup)
        self.assertEqual(sensor._bus, 'valid')

    def test_bus_set(self):
        self.mock_listdir.return_value = ['w1_bus_master1',
                                          'test_foo']

        sensor = Sensor()
        self.assertEqual(sensor._bus, 'test_foo')

    def test_sensor_not_found(self):
        sensor = Sensor()
        self.assertRaises(SensorException,
                          sensor._setup)

class TestRead(unittest.TestCase):
    def setUp(self):
        self.MINIMUM_UPDATE_TIME_patcher = mock.patch('temp_serve.sensor.MINIMUM_UPDATE_TIME', 30)
        self.MINIMUM_UPDATE_TIME_patcher.start()

        self.open_patcher = mock.patch('__builtin__.open')
        self.mock_open = self.open_patcher.start()
        self.mock_open.return_value.__enter__.return_value.read.return_value = (
                'asdfasdasdf\n0 1 2 3 4 5 6 7 8 t=50000')

        self.listdir_patcher = mock.patch('temp_serve.sensor.os.listdir')
        self.mock_listdir = self.listdir_patcher.start()

        self.mock_listdir.return_value = ['test_bus']

        self.sensor = Sensor()
        self.sensor._last_update = datetime.now()
        self.sensor._cached_temp = 'test_cached_temp'

    def tearDown(self):
        self.MINIMUM_UPDATE_TIME_patcher.stop()
        self.open_patcher.stop()

    def test_no_bus(self):
        self.sensor._bus = None

        self.assertRaises(SensorException,
                          self.sensor._read)

    def test_use_cache(self):
        expected = 'test_cached_temp'
        actual = self.sensor._read()

        self.assertEqual(expected, actual)

    def test_invalid_cache(self):
        self.sensor._last_update = datetime.now() - timedelta(seconds=31)
        expected = 50
        actual = self.sensor._read()

        self.assertEqual(expected, actual)

class TestGetCelsius(unittest.TestCase):
    def setUp(self):
        self._read_patcher = mock.patch('temp_serve.sensor.Sensor._read')
        self.mock_read = self._read_patcher.start()

        self._setup_patcher = mock.patch('temp_serve.sensor.Sensor._setup')
        self.mock_setup = self._setup_patcher.start()

        self.sensor = Sensor()

    def tearDown(self):
        self._read_patcher.stop()
        self._setup_patcher.stop()

    def test_celsius(self):
        expected = self.mock_read.return_value
        actual = self.sensor.get_celsius()

        self.assertEqual(expected, actual)

class TestFahrenheit(unittest.TestCase):
    def setUp(self):
        self._read_patcher = mock.patch('temp_serve.sensor.Sensor._read')
        self.mock_read = self._read_patcher.start()

        self._setup_patcher = mock.patch('temp_serve.sensor.Sensor._setup')
        self.mock_setup = self._setup_patcher.start()

        self.sensor = Sensor()

    def tearDown(self):
        self._read_patcher.stop()
        self._setup_patcher.stop()

    def test_0_celsius(self):
        self.mock_read.return_value = 0

        expected = 32
        actual = self.sensor.get_fahrenheit()

        self.assertEqual(expected, actual)

    def test_100_celsius(self):
        self.mock_read.return_value = 100

        expected = 212
        actual = self.sensor.get_fahrenheit()

        self.assertEqual(expected, actual)

