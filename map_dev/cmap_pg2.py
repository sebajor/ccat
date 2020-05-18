import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import matplotlib.pyplot as plt
import sys
import cv2



def plot_image(data):
    """
    Plot array as an image.
    :param data: 2-D array
    """
    pl = pg.plot()
    image = pg.ImageItem(border='w')

    pl.addItem(image)

    hist = pg.HistogramLUTItem()
    # Contrast/color control
    hist.setImageItem(image)
    # pl.addItem(hist)

    image.setImage(data)
    pos = np.array([0., 1., 0.5, 0.25, 0.75])
    color = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255], (0, 255, 255, 255), (255, 255, 0, 255)],
                 dtype=np.ubyte)
    cmap = pg.ColorMap(pos, color)
    lut = cmap.getLookupTable(0.0, 1.0, 256)
    image.setLookupTable(lut)

    hist.gradient.setColorMap(cmap)
    pl.autoRange()



def generatePgColormap(cm_name):
    pltMap = plt.get_cmap(cm_name)
    colors = pltMap.colors
    colors = [c + [1.] for c in colors]
    positions = np.linspace(0, 1, len(colors))
    pgMap = pg.ColorMap(positions, colors)
    return pgMap


def plot_image2(data, cmap):
    """
    Plot array as an image.
    :param data: 2-D array
    """
    pl = pg.plot()
    image = pg.ImageItem(border='w')

    pl.addItem(image)

    hist = pg.HistogramLUTItem()
    # Contrast/color control
    hist.setImageItem(image)
    # pl.addItem(hist)

    image.setImage(data)
    #pos = np.array([0., 1., 0.5, 0.25, 0.75])
    #color = np.array([[0, 0, 255, 255], [255, 0, 0, 255], [0, 255, 0, 255], (0, 255, 255, 255), (255, 255, 0, 255)],
    #             dtype=np.ubyte)
    #cmap = pg.ColorMap(pos, color)
    lut = cmap.getLookupTable(0.0, 1.0, 256)
    image.setLookupTable(lut)

    hist.gradient.setColorMap(cmap)
    pl.autoRange()



def play(data, cmap):

    win = pg.GraphicsLayoutWidget()
    win.show()
    view = win.addPlot()#win.addViewBox()
    img = pg.ImageItem(border='w')
    view.addItem(img)

    img.setImage(data)
    lut = cmap.getLookupTable(0.0, 1.0, 256)
    img.setLookupTable(lut)







