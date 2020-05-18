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
    def __init__(self,img_size=[1000,1000], real_size=[22,22]):
        """ img_size=[xlen, ylen] is the image size
            real_size=[x_size, y_size] is the real values that are 
            mapped to the image.
            The image is in the ((-x_size/2, x_size/2),(-y_size/2, y_size/2))
        """

        super(map_sim, self).__init__()

        ## simulation variables..
        undersamp = 2
        self.index = 0
        self.x_pos = np.loadtxt('x_val')[::undersamp]
        self.y_pos = np.loadtxt('y_val')[::undersamp]

        ##

        self.img_size = img_size
        self.real_size = real_size        

        self.img = np.zeros(img_size)
        
        self.dx = 1.*real_size[0]/img_size[0]
        self.dy = 1.*real_size[1]/img_size[1]
        
        #
        
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('scatt anim')
        self.win.show()
        self.plot1 = self.win.addPlot()
        self.plot1.disableAutoRange()
        self.plot1.setRange(xRange=[0,self.img_size[0]], yRange=[0,self.img_size[1]])
        
        self.img1 = pg.ImageItem()
        self.plot1.addItem(self.img1)
        
        self.lut = plt.get_cmap('viridis').colors
        
        self.threadpool = QtCore.QThreadPool(parent=self.win)
        self.threadpool.setMaxThreadCount(1)
        self.update()




    def img_loc(self, x_pos, y_pos):
        x_ind = int((x_pos+1.*self.real_size[0]/2)/self.dx)
        y_ind = int((y_pos+1.+self.real_size[1]/2)/self.dy)
        
        return (x_ind, y_ind)


    def update(self):
        if(self.index>16000):
            self.index = 0
        self.index = self.index+1
        QtGui.QApplication.processEvents()
        worker = Worker(self.ex_function, self.index)        
        worker.signals.result.connect(self.plot_data)
        self.threadpool.start(worker)
        
        timer = QtCore.QTimer(parent=self.win)
        timer.timeout.connect(self.update)
        timer.setSingleShot(True)
        timer.start(1)
        
    def ex_function(self, *args):
        """Simulated values
        """
        data_x = self.x_pos[args[0]]
        data_y = self.y_pos[args[0]]
        val = np.random.random()*100
        return ([data_x, data_y], val)


    def plot_data(self, *args):
        #ipdb.set_trace()
        [x,y] = self.img_loc(args[0][0][0],args[0][0][1])
        self.img[x,y] = args[0][1]
        self.img1.setImage(self.img, lut=self.lut)
        
        



if __name__ == '__main__': 
    app = QtGui.QApplication([])
    win = map_sim()
    app.exec_()


        
        









