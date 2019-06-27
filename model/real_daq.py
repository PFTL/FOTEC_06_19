import pint
from controller.simple_daq import Device

ur = pint.UnitRegistry()


class RealDaq:
    def __init__(self, port):
        self.driver = Device(port)

    def set_analog(self, channel, output):
        new_output = int(output.m_as('V')*4095/3.3)
        self.driver.set_output(channel, new_output)

    def read_analog(self, channel):
        ans = self.driver.read_input(channel)
        return ans/1024*ur('3.3V')

if __name__ == '__main__':
    daq = RealDaq('COM7')
    daq.set_analog(0, ur('3.3V'))
    print(daq.read_analog(0))
