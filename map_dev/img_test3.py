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

        self.img = np.zeros(img_size)
        
        self.dx = 1.*real_size[0]/img_size[0]
        self.dy = 1.*real_size[1]/img_size[1]
        
        #
        
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('scatt anim')
        self.win.show()

        self.lay1 = self.win.addLayout()

        
        self.plot1 = self.lay1.addPlot()
        self.plot1.disableAutoRange()

            
        self.win2 = pg.GraphicsWindow()
        self.lay2 = self.win2.addLayout()
        self.plot2 = self.lay2.addPlot()
        self.plot2.disableAutoRange()

        self.plot2.plot(self.x_pos[0:4000], self.y_pos[0:4000])
        self.win2.show()

        
        #self.plot1.setRange(xRange=[-1.*self.img_size[0]/2,1.*self.img_size[0]/2], yRange=[-self.img_size[1]/2,1.*self.img_size[1]/2])
        self.plot1.setRange(xRange=[-1.*self.real_size[0]/2,1.*self.real_size[0]/2], yRange=[-self.real_size[1]/2,1.*self.real_size[1]/2])

        self.plot1.showGrid(x=True, y=True)
    

        self.img1 = pg.ImageItem()
        self.img1.translate(-1.*self.real_size[0]/2, -1.*self.real_size[1]/2)
        self.img1.scale(self.dx, self.dy)
        


        self.plot1.addItem(self.img1)
        
        self.cmap = self.generatePgColormap('viridis') #the colormap to use


 
        self.hist = pg.HistogramLUTItem()
        self.lut = self.cmap.getLookupTable(0.0, 1.0, 256)
        self.img1.setLookupTable(self.lut)
        self.hist.gradient.setColorMap(self.cmap)
      
 
       
        ##This part of the code set the grid upside the image, but the zooming with the
        ##
         
        for key in self.plot1.axes:
            ax = self.plot1.getAxis(key)
            ax.setGrid(1 * 255)
            
            ax.setZValue(1)
    
        ###


        #create colorbar

        self.colorbar = pg.HistogramLUTItem()
        self.lay1.addItem(self.colorbar)
        self.colorbar.setLevels(np.min(self.img), np.max(self.img)) ##maybe fix this
        self.colorbar.gradient.setColorMap(self.cmap)
        
        self.max_px = np.max(self.img)
        self.min_px = np.min(self.img)
        self.colorbar.vb.setMouseEnabled(y=False, x=False)       
        self.colorbar.region.setMovable(False) #disbable the user interface


 
        self.img1.hoverEvent = self.imageHoverEvent #mouse event

        
        self.threadpool = QtCore.QThreadPool(parent=self.win)
        self.threadpool.setMaxThreadCount(1)
        self.update()




    def img_loc(self, x_pos, y_pos):
        """#TODO:check if the values are swapped
        """
        x_ind = int((x_pos+1.*self.real_size[0]/2)/self.dx)
        y_ind = int((y_pos+1.*self.real_size[1]/2)/self.dy)
        
        return (x_ind, y_ind)
    

    def generatePgColormap(self, cm_name):
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
        if(args[0][1]>self.max_px):
            self.max_px = args[0][1]
            self.colorbar.setLevels(self.min_px, self.max_px)
        
    
    
    def imageHoverEvent(self, event):
        """Show the position, pixel, and value under the mouse cursor.
        """
        if event.isExit():
            self.plot1.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.img.shape[0] - 1))
        j = int(np.clip(j, 0, self.img.shape[1] - 1))
        val = self.img[j, i]                    ##check if the axes are swapped in the image
        ppos = self.img1.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.plot1.setTitle("pos: (%0.1f, %0.1f)   value: %g" % (x, y, val))

        



if __name__ == '__main__': 
    app = QtGui.QApplication([])
    win = map_sim()
    app.exec_()


        
        









