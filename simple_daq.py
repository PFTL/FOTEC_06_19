from time import sleep
import serial


class Device:
    def __init__(self, port):
        self.rsc = serial.Serial(port)
        sleep(0.5)
        self.write_termination = '\n'

    def write(self, command):
        command = command + self.write_termination
        command = command.encode('ascii')
        self.rsc.write(command)
        sleep(0.05)

    def read(self):
        ans = self.rsc.readline()
        ans = ans.decode()
        ans = ans.strip()
        return ans

    def query(self, command):
        self.write(command)
        return self.read()

    def idn(self):
        return self.query('IDN')

    def set_output(self, channel, value):
        new_value = int(value*4095/3.3)
        command = f'OUT:CH{channel}:{new_value}'
        self.write(command)

    def read_input(self, channel):
        command = f'IN:CH{channel}'
        ans = int(self.query(command))
        volts = ans/1024*3.3
        return volts


if __name__ == '__main__':
    dev = Device('COM7')
    print(dev.idn())
    dev.set_output(0, '3.3V')
    print(dev.read_input(0))

