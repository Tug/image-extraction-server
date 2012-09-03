import numpy as np
import cv2

def extractCentralComponent(mask):
    sqrSize2 = 2
    mheight, mwidth = mask.shape
    markers = np.zeros(mask.shape, np.uint8)
    minSize = min(mheight, mwidth)
    minSize2 = minSize/2
    centerX = mwidth/2
    centerY = mheight/2
    while sqrSize2 < minSize2 - 20:
        starty = centerY-sqrSize2
        endy = centerY+sqrSize2+1
        startx = centerX-sqrSize2
        endx = centerX+sqrSize2+1
        markers[starty:endy, startx:endx] = 255
        seeds = markers & mask
        seed_point = np.argmax(seeds)
        seed_point = np.unravel_index(seed_point, mask.shape)
        max = mask[seed_point]
        if max != 255:
            sqrSize2 = sqrSize2+3
        else:
            cv2.floodFill(mask, np.zeros((mheight+2, mwidth+2), np.uint8), (seed_point[1], seed_point[0]), 127)
            mask[mask != 127] = 0
            histo, bins = np.histogram(mask, bins=[0, 127, 255])
            if histo[1] < 100: #object too small, remove it
                mask[mask == 127] = 0
            else:
                mask[mask == 127] = 255
                break
