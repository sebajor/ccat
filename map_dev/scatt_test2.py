from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import sys
import ipdb


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
            #ipdb.set_trace()
            self.signals.result.emit(result)



class map_sim(QtGui.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(map_sim, self).__init__()
        self.counter = 0
        self.x_pos = np.loadtxt('x_val')
        self.y_pos = np.loadtxt('y_val')
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('scatt anim')
        self.win.show()
        p = self.win.addPlot()
        p.setRange(xRange=[-10, 10], yRange=[-10, 10])
        self.scatter = pg.ScatterPlotItem()
        p.addItem(self.scatter)
        self.colormap = self.mapping_init(0,100)
        
        self.threadpool = QtCore.QThreadPool(parent=self.win)
        self.threadpool.setMaxThreadCount(1)
        self.update()



    def  mapping_init(self,min_val,max_val,cmap='viridis'):
        a = min_val
        b = max_val
        colormap = plt.get_cmap(cmap)
        positions = np.linspace(a,b,len(colormap.colors), endpoint=True)
        brush = pg.ColorMap(pos=positions, color=colormap.colors)
        return brush


    def update(self):
        #ipdb.set_trace()
        if(self.counter>=80000):
            self.counter = 0
        self.counter = self.counter + 1
        QtGui.QApplication.processEvents()
        worker = Worker(self.ex_function, self.counter)
        worker.signals.result.connect(self.plot_data)
        self.threadpool.start(worker)
        
        QtCore.QTimer.singleShot(1, self.update)
        #timer = QtCore.QTimer(parent=self.win)
        #timer.timeout.connect(self.update)
        #timer.setSingleShot(True)
        #timer.start(1)

    def ex_function(self, *args):
        #ipdb.set_trace()
        data_x = self.x_pos[args[0]]
        data_y = self.y_pos[args[0]]
        val = np.random.random()*100
        #self.counter = self.counter+1
        return ([data_x, data_y], val)


    def plot_data(self, *args):
        #ipdb.set_trace()
        color_pts = self.colormap.map(args[0][1])
        brush = [QtGui.QBrush(QtGui.QColor(*color_pts))]
        self.scatter.addPoints(x=[args[0][0][0]], y=[args[0][0][1]], brush=brush)
        #QtGui.QApplication.processEvents()


if __name__ == '__main__': 
    app = QtGui.QApplication([])
    win = map_sim()
    app.exec_()
        
