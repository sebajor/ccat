import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import matplotlib.pyplot as plt
import sys, time
import ipdb


def mapping_init(min_val,max_val,cmap='viridis'):
    """Initialize a object who translate the values to a 
       given colormap
    """
    a = min_val
    b = max_val
    colormap = plt.get_cmap(cmap)
    positions = np.linspace(a,b,len(colormap.colors), endpoint=True)
    brush = pg.ColorMap(pos=positions, color=colormap.colors)
    return brush


def color_values(values):
    """ obtain the color map for a given set of values
    """
    brush.map(values)



def init_func():
    global scatter, colormap, win, counter, x_pos, y_pos
    counter = 0
    x_pos = np.loadtxt('x_val')
    y_pos = np.loadtxt('y_val')
    win = pg.GraphicsLayoutWidget()
    win.setWindowTitle('scatt anim')
    win.show()
    p = win.addPlot()
    p.setRange(xRange=[-10, 10], yRange=[-10, 10])
    scatter = pg.ScatterPlotItem()
    p.addItem(scatter)
    colormap= mapping_init(0, 100)
    update()

    

    


def update():
    global counter
    start = time.time()
    #ipdb.set_trace()
    data_x = x_pos[counter]
    data_y = y_pos[counter]
    if(counter<80000):
        counter = counter +1
    else:
        counter = 0
    #[data_x, data_y, val] = [(np.random.random()-0.5)*2*500, (np.random.random()-0.5)*2*500, np.random.random()*100]
    val = np.random.random()*100
    #ipdb.set_trace()
    color_pts = colormap.map(val)
    brush = [QtGui.QBrush(QtGui.QColor(*color_pts))]

    scatter.addPoints(x=[data_x], y=[data_y], brush=brush)
    QtGui.QApplication.processEvents()
    print(time.time()-start)
    timer = QtCore.QTimer(parent=win)
    timer.timeout.connect(update)
    timer.setSingleShot(True)
    timer.start(1)
    
        
    

if __name__ == '__main__': 
    app = QtGui.QApplication([])
    init_func()
    sys.exit(app.exec_())



