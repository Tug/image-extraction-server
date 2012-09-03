import numpy as np

def checkRectangleBounds(rect, shape):
    x, y, w, h = rect
    imgH, imgW = shape
    return (max(0, x), max(0, y), min(w, imgW-x), min(h, imgH-y))

def rectangle2mask(rect, shape):
    mask = np.zeros(shape, np.uint8)
    x, y, w, h = rect
    mask[y:y+h, x:x+w] = 255
    return mask