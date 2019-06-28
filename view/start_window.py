import os
from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class StartWindow(QMainWindow):
    def __init__(self, experiment, parent=None):
        super().__init__(parent=parent)
        self.experiment = experiment
        this_folder = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(this_folder, 'GUI', 'scan_window.ui')
        uic.loadUi(ui_file, self)

        self.start_button.clicked.connect(self.start_pressed)
        self.stop_button.clicked.connect(self.stop_pressed)

    def start_pressed(self):
        print('Button pressed')
        start_voltage = self.start_line.text()
        self.experiment.config['scan']['start'] = start_voltage

        self.working_thread = Thread(target=self.experiment.do_scan)
        self.working_thread.start()

    def stop_pressed(self):
        print('Stop pressed')
        self.experiment.keep_running = False

    def closeEvent(self, evnt):
        print('Window Closing')


if __name__ == '__main__':
    app = QApplication([])
    win = StartWindow()
    win.show()
    app.exec()