import os
import pyqtgraph as pg

from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from view.monitor_window import MonitorWindow


class StartWindow(QMainWindow):
    def __init__(self, experiment, parent=None):
        super().__init__(parent=parent)
        self.experiment = experiment
        this_folder = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(this_folder, 'GUI', 'scan_window.ui')
        uic.loadUi(ui_file, self)

        self.startButton.clicked.connect(self.start_pressed)
        self.stopButton.clicked.connect(self.stop_pressed)

        self.outChannelLine.setText(str(self.experiment.config['scan']['channel_out']))
        self.outStartLine.setText(self.experiment.config['scan']['start'])
        self.outStopLine.setText(self.experiment.config['scan']['stop'])
        self.outNumStepsLine.setText(str(self.experiment.config['scan']['num_steps']))
        self.inChannelLine.setText(str(self.experiment.config['scan']['channel_in']))
        self.inDelayLine.setText(self.experiment.config['scan']['delay'])

        self.plotWidget = pg.PlotWidget()
        self.plot = self.plotWidget.plot([0], [0])
        self.plotWidget.setLabel('left', "Current", units='A')
        self.plotWidget.setLabel('bottom', "Voltage", units='V')

        self.layout = self.centralwidget.layout()
        self.layout.addWidget(self.plotWidget)

        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.timeout.connect(self.update_progress_bar)
        self.action_Save.triggered.connect(self.save_data)

        self.scan_progress_bar.setValue(0)

        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitor)
        self.monitor_window = MonitorWindow(self)
        self.actionShow_Monitor.triggered.connect(self.monitor_window.show)
        self.actionStart_Monitor.triggered.connect(self.start_monitor)
        self.actionStop_Monitor.triggered.connect(self.stop_monitor)
        self.monitor_window.monitor_closed.connect(self.stop_monitor)

    def update_monitor(self):
        self.monitor_window.update_plot(self.experiment.monitor_currents)

    def start_monitor(self):
        self.monitor_thread = Thread(target=self.experiment.monitor_signal)
        self.monitor_thread.start()
        self.monitor_timer.start(30)

    def stop_monitor(self):
        self.experiment.keep_running = False
        self.monitor_timer.stop()

    def update_plot(self):
        self.plot.setData(self.experiment.volts, self.experiment.currents)
        if self.experiment.is_running:
            self.startButton.setEnabled(False)
        else:
            self.startButton.setEnabled(True)

    def update_progress_bar(self):
        progress = self.experiment.i/self.experiment.config['scan']['num_steps']*100
        self.scan_progress_bar.setValue(progress)

    def start_pressed(self):
        self.experiment.config['scan'].update({
            'start': self.outStartLine.text(),
            'stop': self.outStopLine.text(),
            'num_steps': int(self.outNumStepsLine.text()),
            'channel_out': int(self.outChannelLine.text()),
            'channel_in': int(self.inChannelLine.text()),
            'delay': self.inDelayLine.text(),
        })

        self.working_thread = Thread(target=self.experiment.do_scan)
        self.working_thread.start()

    def stop_pressed(self):
        self.experiment.keep_running = False

    def save_data(self):

        self.experiment.save_data()
        self.experiment.save_metadata()

    def closeEvent(self, evnt):
        self.experiment.keep_running = False
        super().closeEvent(evnt)


if __name__ == '__main__':
    app = QApplication([])
    win = StartWindow(None)
    win.show()
    app.exec()