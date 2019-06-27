from controller.simple_daq import Device
from model import ur


class RealDaq:
    def __init__(self, port):
        self.driver = Device(port)

    def idn(self):
        return self.driver.query('IDN')

    def get_analog_value(self, channel):
        query_string = 'IN:CH{}'.format(channel)
        value_bits = int(self.driver.query(query_string))
        value_volts = value_bits/1024*ur('3.3V')
        return value_volts

    def set_analog_value(self, channel, value):
        value = int(value.m_as('V')/3.3*4095)
        query_string = 'OUT:CH{}:{}'.format(channel, value)
        self.driver.write(query_string)


if __name__ == '__main__':
    daq = RealDaq('COM9')
    daq.set_analog_value(0, ur('3.3V'))
    print(daq.get_analog_value(0))
