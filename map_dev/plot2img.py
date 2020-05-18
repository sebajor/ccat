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
#view.setAspectLocked(True)
img = pg.ImageItem(border='w')
view.addItem(img)


view2 = win.addPlot()#win.addViewBox()
#view2.setAspectLocked(True)
img2 = pg.ImageItem(border='r')
view2.addItem(img2)
#view2.setRange(QtCore.QRectF(0, 0, 100, 100))


asd = cv2.imread('holo.png')
qwe = cv2.imread('clb.png')


img.setImage(asd)
img2.setImage(asd)
QtGui.QApplication.processEvents()

app.exec_()




