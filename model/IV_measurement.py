from time import sleep

import yaml
from model.real_daq import RealDaq
from model import ur


class Experiment:
    def __init__(self):
        self.config = None
        self.daq = None

    def load_daq(self):
        self.daq = RealDaq(self.config['DAQ']['port'])

    def load_config(self, filename):
        with open(filename) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def do_scan(self):
        start = ur(self.config['scan']['start'])
        stop = ur(self.config['scan']['stop'])
        step = ur(self.config['scan']['step'])

        volt = start.to('V')
        volts = []
        while volt < stop.to('V'):
            volts.append(volt)
            volt += step.to('V')

        currents = []
        resistance = ur(self.config['experiment']['resistance'])
        delay = ur(self.config['scan']['delay']).m_as('s')
        for volt in volts:
            self.daq.set_analog(self.config['scan']['channel_out'], volt)
            current = self.daq.read_analog(self.config['scan']['channel_in'])/resistance
            currents.append(current.to('mA'))
            sleep(delay)

    def save_data(self):
        pass

    def save_metadata(self):
        pass

    def finalize(self):
        pass


if __name__ == '__main__':
    exp = Experiment()
    exp.load_config('../examples/config.yml')
    exp.load_daq()
    exp.do_scan()
    exp.save_data()
    exp.save_metadata()
    exp.finalize()
