from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from artificial_data import spectrum
import sys
import ipdb
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
    
    def __init__(self, *args, **kwargs):
        super(Main_thread, self).__init__()
        #self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
        self.fig = self.win.addPlot(title='Spects')
        self.fig.setRange(yRange=[0,10], xRange=[0,8191])
        self.fig.showGrid(x=True, y=True)
        
        self.threadpool = QtCore.QThreadPool(parent=self.win)
        self.curve0 = self.fig.plot(pen='y')
        self.curve1 = self.fig.plot(pen='r')
        self.curve0.setData(np.arange(8192), np.zeros(8192))
        self.curve1.setData(np.arange(8192), np.zeros(8192))
        self.counter = 0
        self.exit_flag = 0
        self.Update() 
    
    
    def Update(self):
        self.counter = self.counter+20
        if(self.counter>4190):
            self.counter=0
        QtGui.QApplication.processEvents()
        worker1 = Worker(self.ex_function, 3000)
        worker2 = Worker(self.ex_function, 4000+int(self.counter))
        worker1.signals.result.connect(self.plot1)
        worker2.signals.result.connect(self.plot2)
        #ipdb.set_trace()
        self.threadpool.start(worker1) 
        self.threadpool.start(worker2)
        if(self.exit_flag):
            return
        
        #QtCore.QTimer.singleShot(1, self.Update)
        timer = QtCore.QTimer(parent=self.win)
        timer.timeout.connect(self.Update)
        timer.setSingleShot(True)
        timer.start(1)
        
    
    def exit_handle(self):
        self.exit_flag = 1
    
    def ex_function(self,chann):
        print('asdqwe')
        data = spectrum(peak_loc=chann)
        return (np.arange(len(data)), data)
        
    def plot1(self, *args):
        #ipdb.set_trace()
        self.curve0.setData(args[0][0], args[0][1])
        #QtGui.QApplication.processEvents()


    def plot2(self, *args):
        self.curve1.setData(args[0][0],args[0][1])
        #QtGui.QApplication.processEvents()
 

if __name__=='__main__':
    app = QtGui.QApplication([])
    window = Main_thread()
    app.aboutToQuit.connect(window.exit_handle)
    sys.exit(app.exec_())
    
    #to run it again in ipython is enough define a 
    #new window and run app.exec_()..ie just run
    ##window = Main_thread([]); app.exec_()
