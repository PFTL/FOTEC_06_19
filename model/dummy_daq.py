import numpy as np
from model import ur


class DummyDaq:
    def __init__(self, port):
        self.port = port

    def idn(self):
        return f'Dummy Daq at port {self.port}'

    def read_analog(self, channel):
        return np.random.random()*ur('V')

    def set_analog(self, channel, value):
        value = int(value.m_as('V') / 3.3 * 4095)
