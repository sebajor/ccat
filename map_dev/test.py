import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import sys


class Workersignal(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(tuple)
    #prorgress = QtCore.pyqtSignal(tuple)

class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Workersignal()
        #self.kwargs['progress_callback'] = [0,0]

    @QtCore.pyqtSlot()   
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signal.error.emit((0, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)


class Main_thread(QtGui.QMainWindow):
    
    def __init__(self, x_size, y_size):
        self.win = pg.GraphicsLayoutWidget()
        self.win.show()
        self.view1 = self.win.addViewBox()
        self.view1.setAspectLocked(True)        
        self.power_map = pg.ImageItem(border='w')
        self.view1.addItem(self.img)
        self.view1.setRange(QtCore.QRectF(0, 0, x_size, y_size))
        
        self.power_phase = pg.ImageItem(border='r')
        
             















