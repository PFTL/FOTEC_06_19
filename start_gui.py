from PyQt5.QtWidgets import QApplication

from model.IV_measurement import Experiment
from view.start_window import StartWindow

exp = Experiment()
exp.load_config('examples/config.yml')
exp.load_daq()

app = QApplication([])
win = StartWindow(exp)
win.show()
app.exec()

exp.finalize()
