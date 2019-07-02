import os
import numpy as np
from time import sleep

import yaml
from model.real_daq import RealDaq
from model.dummy_daq import DummyDaq
try:
    from model.imaginary_daq import ImaginaryDaq
except ModuleNotFoundError:
    print('ImaginaryDaq does not exist')

from model import ur


class Experiment:
    def __init__(self):
        self.config = None
        self.daq = None
        self.volts = []
        self.currents = []
        self.is_running = False
        self.i = 0

    def load_daq(self):
        if self.config['DAQ']['name'] == 'Real':

            self.daq = RealDaq(self.config['DAQ']['port'])
        elif self.config['DAQ']['name'] == 'Dummy':

            self.daq = DummyDaq(self.config['DAQ']['port'])
        else:
            raise Exception(f"DAQ {self.config['DAQ']['name']} not recognized")

    def load_config(self, filename):
        with open(filename) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def monitor_signal(self):
        if self.is_running:
            raise Exception('Device already running')

        self.monitor_currents = np.zeros(self.config['monitor']['samples']) * ur('mA')

        resistance = ur(self.config['experiment']['resistance'])
        self.keep_running = True
        self.is_running = True
        while self.keep_running:
            new_current = self.daq.read_analog(self.config['monitor']['channel_in'])/resistance
            self.monitor_currents = np.roll(self.monitor_currents, -1)
            self.monitor_currents[-1] = new_current.m_as('mA')
        self.is_running = False


    def do_scan(self):
        if self.is_running:
            raise Exception('Scan already running')

        start = ur(self.config['scan']['start'])
        stop = ur(self.config['scan']['stop'])
        num_steps = int(self.config['scan']['num_steps'])

        self.volts = np.linspace(start.m_as('V'), stop.m_as('V'), num_steps) * ur('V')

        self.currents = np.zeros(num_steps) * ur('A')
        resistance = ur(self.config['experiment']['resistance'])
        delay = ur(self.config['scan']['delay']).m_as('s')

        self.keep_running = True
        self.i = 0
        self.is_running = True
        for volt in self.volts:
            self.daq.set_analog(self.config['scan']['channel_out'], volt)
            current = self.daq.read_analog(self.config['scan']['channel_in'])/resistance
            # self.currents.append(current.to('mA'))
            self.currents[self.i] = current.to('A')
            self.i += 1
            sleep(delay)
            if not self.keep_running:
                print('Scan stopped')
                break
        self.is_running = False

    def save_data(self):
        directory = self.config['experiment']['save_directory']
        try:
            os.makedirs(directory)
        except FileExistsError:
            print('Not creating new directory')

        i = 1
        filename = self.config['experiment']['save_file']
        full_filename = os.path.join(directory, filename+ '.dat')
        while os.path.isfile(full_filename):
            full_filename = os.path.join(directory, filename + '_' + str(i) + '.dat')
            i += 1

        with open(full_filename, 'w') as f:
            for i in range(len(self.currents)):
                volt = self.volts[i]
                current = self.currents[i]
                f.write(f'{volt}, {current}\n')

    def save_metadata(self):
        directory = self.config['experiment']['save_directory']
        if not os.path.exists(directory):
            os.makedirs(directory)

        i = 1
        filename = self.config['experiment']['save_meta']
        full_filename = os.path.join(directory, filename + '.dat')
        while os.path.isfile(full_filename):
            full_filename = os.path.join(directory, filename + '_' + str(i) + '.dat')
            i += 1

        with open(full_filename, 'w') as f:
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
