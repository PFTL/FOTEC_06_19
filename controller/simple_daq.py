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
        """ Value from 0 to 4095 """
        command = f'OUT:CH{channel}:{value}'
        self.write(command)

    def read_input(self, channel):
        command = f'IN:CH{channel}'
        return int(self.query(command))


if __name__ == '__main__':
    dev = Device('COM7')
    print(dev.idn())
    dev.set_output(0, 4000)
    print(dev.read_input(0))
    sleep(1)
    dev.set_output(0, 2000)
    print(dev.read_input(0))

