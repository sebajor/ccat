from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
import sys
import ipdb
from twilight import _twilight_data

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
    def __init__(self,img_size=[500,500], real_size=[22,22]):
        """ img_size=[xlen, ylen] is the image size
            real_size=[x_size, y_size] is the real values that are 
            mapped to the image.
            The image is in the ((-x_size/2, x_size/2),(-y_size/2, y_size/2))
        """
        super(map_sim, self).__init__()

        ## simulation variables..
        undersamp = 4
        self.index = 0
        self.x_pos = np.loadtxt('x_val')[::undersamp]
        self.y_pos = np.loadtxt('y_val')[::undersamp]
        ##


        self.img_size = img_size
        self.real_size = real_size
        
        self.pow = np.zeros(img_size)
        self.ang = np.zeros(img_size)        
        ##there could be a problem.. like we initialize all the 
        ##array in zero if the actual phase is zero it will not 
        ##look good....

        self.dx = 1.*real_size[0]/img_size[0]
        self.dy = 1.*real_size[1]/img_size[1]
        

        #Create windows and plots
       
        self.win1 = pg.GraphicsWindow()
        self.win1.setWindowTitle('Relative Power')
        self.win1.show() 
        self.win2 = pg.GraphicsWindow()
        self.win2.setWindowTitle('Relative Phase')
        self.win2.show()


        self.plot1 = self.win1.addPlot()
        self.plot1.disableAutoRange()
        self.plot1.setRange(xRange=[-1.*self.real_size[0]/2,1.*self.real_size[0]/2], yRange=[-self.real_size[1]/2,1.*self.real_size[1]/2])
        self.plot1.showGrid(x=True, y=True)

        self.plot2 = self.win2.addPlot()
        self.plot2.disableAutoRange()
        self.plot2.setRange(xRange=[-1.*self.real_size[0]/2,1.*self.real_size[0]/2], yRange=[-self.real_size[1]/2,1.*self.real_size[1]/2])
        self.plot2.showGrid(x=True, y=True)



        self.img_pow = pg.ImageItem()
        self.img_pow.translate(-1.*self.real_size[0]/2, -1.*self.real_size[1]/2)
        self.img_pow.scale(self.dx, self.dy)
        self.plot1.addItem(self.img_pow)
        self.cmap_pow = self.generatePgColormap('viridis') #the colormap to use

        self.hist_pow = pg.HistogramLUTItem()
        self.lut_pow = self.cmap_pow.getLookupTable(0.0, 1.0, 256)
        self.img_pow.setLookupTable(self.lut_pow)
        self.hist_pow.gradient.setColorMap(self.cmap_pow)                
    

        self.img_ang = pg.ImageItem()
        self.img_ang.translate(-1.*self.real_size[0]/2, -1.*self.real_size[1]/2)
        self.img_ang.scale(self.dx, self.dy)
        self.plot2.addItem(self.img_ang)
        self.cmap_ang = self.generatePgColormap('twilight') 

        self.hist_ang = pg.HistogramLUTItem()
        self.lut_ang = self.cmap_ang.getLookupTable(0.0, 1.0, 256)
        self.img_ang.setLookupTable(self.lut_ang)
        self.hist_ang.gradient.setColorMap(self.cmap_ang)

        ##This part of the code set the grid upside the image, but the zooming with the
        ##
         
        for key in self.plot1.axes:
            ax = self.plot1.getAxis(key)
            ax.setGrid(1 * 255)
            
            ax.setZValue(1)
    
        for key in self.plot2.axes:
            ax = self.plot2.getAxis(key)
            ax.setGrid(1 * 255)

            ax.setZValue(1)
        ###
        
        #create colorbars

        self.colorbar_pow = pg.HistogramLUTItem()
        self.win1.addItem(self.colorbar_pow)
        self.colorbar_pow.setLevels(np.min(self.pow), np.max(self.pow))
        self.colorbar_pow.gradient.setColorMap(self.cmap_pow)
        
        self.max_pow_px = np.max(self.pow)
        self.min_pow_px = np.min(self.pow)
        self.colorbar_pow.vb.setMouseEnabled(y=False, x=False)       
        self.colorbar_pow.region.setMovable(False) #disbable the user interface


 
        self.img_pow.hoverEvent = self.imageHoverEvent_pow #mouse event 
        

        self.colorbar_ang = pg.HistogramLUTItem()
        self.win2.addItem(self.colorbar_ang)
        self.colorbar_ang.setLevels(np.min(self.ang), np.max(self.ang))
        self.colorbar_ang.gradient.setColorMap(self.cmap_ang)
        self.max_ang_px = np.max(self.ang)
        self.min_ang_px = np.min(self.ang)
        self.colorbar_ang.vb.setMouseEnabled(y=False, x=False)
        self.colorbar_ang.region.setMovable(False) #disbable the user interface



        self.img_ang.hoverEvent = self.imageHoverEvent_ang #mouse event 
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.update()


    def img_loc(self, x_pos, y_pos):
        """#TODO:check if the values are swapped
        """
        x_ind = int((x_pos+1.*self.real_size[0]/2)/self.dx)
        y_ind = int((y_pos+1.*self.real_size[1]/2)/self.dy)
        
        return (x_ind, y_ind)


    def generatePgColormap(self, cm_name):
        if(cm_name=='twilight'):
            colors = _twilight_data
        else:
            pltMap = plt.get_cmap(cm_name)
            colors = pltMap.colors
        colors = [c + [1.] for c in colors]
        positions = np.linspace(0, 1, len(colors))
        pgMap = pg.ColorMap(positions, colors)
        return pgMap


    
    def update(self):
        #print(self.index)
        if(self.index>19997):
            self.index = 0
        self.index = self.index+1
        QtGui.QApplication.processEvents()
        worker = Worker(self.ex_function, self.index)        
        worker.signals.result.connect(self.plot_data)
        self.threadpool.start(worker)
        
        timer = QtCore.QTimer(parent=self.win1)
        timer.timeout.connect(self.update)
        timer.setSingleShot(True)
        timer.start(1)


    def ex_function(self, *args):
        """Simulated values
        """
        data_x = self.x_pos[args[0]]
        data_y = self.y_pos[args[0]]
        pow_val = np.random.random()*100
        ang_val = (np.random.random()-0.5)*360
        return ([data_x, data_y], [pow_val, ang_val])
        

    def plot_data(self, *args):
        #ipdb.set_trace()
        [x,y] = self.img_loc(args[0][0][0],args[0][0][1])
        self.pow[x,y] = args[0][1][0]
        self.img_pow.setImage(self.pow, lut=self.lut_pow)
        self.ang[x,y] = args[0][1][1]
        self.img_ang.setImage(self.ang, lut=self.lut_ang)
        if(args[0][1][0]>self.max_pow_px):
            self.max_pow_px = args[0][1][0]
            self.colorbar_pow.setLevels(self.min_pow_px, self.max_pow_px)
        if(args[0][1][1]>self.max_ang_px):
            self.max_ang_px = args[0][1][1]
            self.colorbar_ang.setLevels(self.min_ang_px, self.max_ang_px)
        if(args[0][1][1]<self.min_ang_px):
            self.min_ang_px = args[0][1][1]
            self.colorbar_ang.setLevels(self.min_ang_px, self.max_ang_px)
           
    
    def imageHoverEvent_pow(self, event):
        """Show the position, pixel, and value under the mouse cursor.
        """
        if event.isExit():
            self.plot1.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.pow.shape[0] - 1))
        j = int(np.clip(j, 0, self.pow.shape[1] - 1))
        val = self.pow[j, i]                    ##check if the axes are swapped in the image
        ppos = self.img_pow.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.plot1.setTitle("pos: (%0.1f, %0.1f)   value: %g" % (x, y, val))


    def imageHoverEvent_ang(self, event):
        """Show the position, pixel, and value under the mouse cursor.
        """
        if event.isExit():
            self.plot2.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.ang.shape[0] - 1))
        j = int(np.clip(j, 0, self.ang.shape[1] - 1))
        val = self.ang[j, i]                    ##check if the axes are swapped in the image
        ppos = self.img_ang.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.plot2.setTitle("pos: (%0.1f, %0.1f)   value: %g" % (x, y, val))



if __name__ == '__main__': 
    app = QtGui.QApplication([])
    win = map_sim()
    app.exec_()






