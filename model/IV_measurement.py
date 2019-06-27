import os
from time import sleep

import yaml
from model.real_daq import RealDaq
from model import ur


class Experiment:
    def __init__(self):
        self.config = None
        self.daq = None
        self.volts = []
        self.currents = []

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
        self.volts = []
        while volt < stop.to('V'):
            self.volts.append(volt)
            volt += step.to('V')

        self.currents = []
        resistance = ur(self.config['experiment']['resistance'])
        delay = ur(self.config['scan']['delay']).m_as('s')
        for volt in self.volts:
            self.daq.set_analog(self.config['scan']['channel_out'], volt)
            current = self.daq.read_analog(self.config['scan']['channel_in'])/resistance
            self.currents.append(current.to('mA'))
            sleep(delay)

    def save_data(self):
        i = 1
        filename = self.config['experiment']['save_file'] + '.dat'
        while os.path.isfile(filename):
            filename = self.config['experiment']['save_file'] + '_' + str(i) + '.dat'
            i += 1

        with open(filename, 'w') as f:
            for i in range(len(self.currents)):
                volt = self.volts[i]
                current = self.currents[i]
                f.write(f'{volt:}, {current}\n')

    def save_metadata(self):
        i = 1
        filename = self.config['experiment']['save_meta'] + '.dat'
        while os.path.isfile(filename):
            filename = self.config['experiment']['save_meta'] + '_' + str(i) + '.dat'
            i += 1
        with open(filename, 'w') as f:
            f.write(yaml.dump(self.config))

    def save(self):
        self.save_metadata()
        self.save_data()

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
