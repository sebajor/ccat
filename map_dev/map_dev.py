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
            self.signals.result.emit(result)


class map(QtGui.QMainWindow):



    def __init__(self, xlen, ylen, cmap='viridis')
        super(map, self).__init__()
        
        self.win = pg.GraphicsWindow()
        self.fig0 = self.win.addPlot(title='Relative Magnitude')
        self.fig0.setRange(yRange=[-ylen/2., ylen/2.], xRange=[-xlen/2., xlen/2.])
        self.fig0.showGrid(x=True, y=True)
        self.pow = pg.ScatterPlotItem()        
        self.fig0.addItem(self.pow)
        self.color_pow = color_mapping(0, 100, cmap=cmap)
        


        self.fig1 = self.win.addPlot(title='Relative Phase')
        self.fig1.setRange(yRange=[-ylen/2, ylen/2], xRange=[-xlen/2., xlen/2.])
        self.fig1.showGrid(x=True, y=True)
        self.ang = pg.ScatterPlotItem()
        self.fig1.addItem(self.ang)
        self.color_ang = color_mapping(-180, 180, cmap=cmap)


        self.threadpool = QtCore.QThreadPool(parent=self.win)
        #creo que tengo que colocar un lim en la cantidad de 
        #threads....
        
        

        
    def color_mapping(min_val, max_val, cmap='viridis'):
        a = min_val
        b = max_val
        colormap = plt.get_cmap(cmap)
        positions = np.linspace(a,b,len(colormap.colors), endpoint=True)
        brush = pg.ColorMap(pos=positions, color=colormap.colors)
        return brush

    
    def measure(self):
        QtGui.QApplication.processEvents()
        worker = Worker(self.get_data)
        worker.signals.result.connect(self.process_data)
        self.threadpool.start(worker)
        
        timer = QtCore.QTimer(parent=self.win)
        timer.timeout.connect(self.measure)
        timer.setSingleShot(True)
        timer.start(1)



    def get_data(self):
        [x,y] = get_pos()  ###simular!!
        [A, B, re, im] = get_vals()     #ver como importarlo..
        pow_diff = 10*(np.log10(A+1)-np.log10(B+1))        
        ang_diff = np.rad2deg(np.arctan2(im, re))
        
        return [[x,y], [pow_diff, ang_diff]]


    def process_data(self, *args)
        
        color_ang = self.color_ang.map(args[1][1])
        brush_ang = [QtGui.QBrush(QtGui.QColor(*color_ang))]
        self.ang.addPoints(x=[args[0][0]], y=[args[0][1]], brush=brush_ang)
        
        color_pow = self.color_pow.map(args[1][0])
        brush_pow = [QtGui.QBrush(QtGui.QColor(*color_pow))]
        self.pow.addPoints(x=[args[0][0]], y=[args[0][1]], brush=brush_pow)
        





##################################
"""
Para correrlo falta hacer

app = QtGui.QApplication([])
asd = map(xlen=1000, y_len=1000 )
asd.measure()
sys.exit(app.exec_())   #no estoy tan seguro de si el 
                        #sys exit no me mata todo al llamarlo :P




"""







    

    




