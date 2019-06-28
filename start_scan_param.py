from model.IV_measurement import Experiment

exp = Experiment()
exp.load_config('examples/config.yml')
exp.load_daq()

for i in range(100):
    exp.config['scan']['num_steps'] = i
    print('Scan started')
    exp.do_scan()
    print('Scan is done')
    exp.save_data()
    exp.save_metadata()
    exp.finalize()

print('After finalize')
