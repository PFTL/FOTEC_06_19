from time import sleep

from model import ur
from model.IV_measurement import Experiment
from threading import Thread

exp = Experiment()
exp.load_config('examples/config.yml')
exp.load_daq()

t = Thread(target=exp.do_scan)
t.start()
print('Scan started')
while t.is_alive():
    print('Still running')
    sleep(1)
    exp.keep_running = False

print('Scan is done')

exp.save_data()
exp.save_metadata()
exp.finalize()
print('After finalize')
