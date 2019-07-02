from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
import pyqtgraph as pg


class MonitorWindow(QMainWindow):
    monitor_closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.plotWidget = pg.PlotWidget()
        self.setCentralWidget(self.plotWidget)
        self.plot = self.plotWidget.plot([0], [0])
        self.plotWidget.setLabel('left', "Current", units='A')

    def update_plot(self, data):
        self.plot.setData(data)

    def closeEvent(self, evnt):
        self.monitor_closed.emit()

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    win = MonitorWindow()
    win.show()
    app.exec()

