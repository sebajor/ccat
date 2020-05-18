import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore


title = "Pyqtgraph basic plot"

t = np.arange(100)
sig = np.sin(2*np.pi*t/100)
sig2 = np.cos(2*np.pi*t/100)


#create the window

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="subplotting")
win.resize(1000,600)


pg.setConfigOptions(antialias=True)


fig = win.addPlot(title='cos')






#create plot
#fig = pg.plot()
fig.showGrid(x=True, y=True)
fig.addLegend()

# set properties

fig.setLabel('left', 'Value', units='V')
fig.setLabel('bottom', 'Time', units='s')
fig.setXRange(0, 100)
fig.setYRange(-1,1)
fig.setWindowTitle(title)

#plot data

c1 = fig.plot(t,sig, pen='b', symbol='x', symbolPen='b', SymbolBrush=0.2, name='Sine')
c2 = fig.plot(t,sig2, pen='r', symbol='o', symbolPen='r', SymbolBrush=0.2, name='Cosine')



###add second plot



fig1 = win.addPlot(title='asdqwe')
fig1.showGrid(x=True, y=True)
fig1.addLegend()

# set properties

fig1.setLabel('left', 'Value', units='V')
fig1.setLabel('bottom', 'Time', units='s')
fig1.setXRange(0, 100)
fig1.setYRange(-1,1)
fig1.setWindowTitle(title)

#plot data

c1 = fig1.plot(t,sig, pen='b', symbol='x', symbolPen='b', SymbolBrush=0.2, name='Sine')
c2 = fig1.plot(t,sig2, pen='r', symbol='o', symbolPen='r', SymbolBrush=0.2, name='Cosine')
















if __name__ == '__main__':
    import sys
    if sys.flags.interactive !=1 or not hasattr(pg.QTCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
