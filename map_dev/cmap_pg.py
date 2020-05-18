import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import sys
import cv2

app = QtGui.QApplication([])
win = pg.GraphicsLayoutWidget()
win.show()
view = win.addPlot()#win.addViewBox()
img = pg.ImageItem(border='w')
view.addItem(img)


hist = pg.HistogramLUTItem()
hist.setImageItem(img)
#view.addItem(hist)

data = cv2.imread('holo.png')[:,:,0]

img.setImage(data)
pos = np.array([0., 1., 0.5, 0.25, 0.75])
color = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255], (0, 255, 255, 255), (255, 255, 0, 255)], dtype=np.ubyte)
cmap = pg.ColorMap(pos, color)
lut = cmap.getLookupTable(0.0, 1.0, 256)
img.setLookupTable(lut)
hist.gradient.setColorMap(cmap)

view.autoRange()

app.exec_()

