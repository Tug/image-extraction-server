import cv2
import numpy as np
import numpy.ma as ma
import color

def hs_histogram(img, mask, bins=10, normed=False):
    hsv = color.rgb2hsv(img)
    
    maskedH = ma.array(hsv[:,:,0], mask=mask)
    maskedS = ma.array(hsv[:,:,1], mask=mask)
    histH, bin_edges_h = np.histogram(maskedH.compressed(), bins=bins, range=None, normed=normed)
    histS, bin_edges_s = np.histogram(maskedS.compressed(), bins=bins, range=None, normed=normed)
    
    return histH, histS


def cv_hs_histogram_(img, mask):
    hsv = color.rgb2hsv(img)

    h_bins = 30
    s_bins = 32
    hist_size = [h_bins, s_bins]
    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]
    # saturation varies from 0 (black-gray-white) to
    # 255 (pure spectrum color)
    s_ranges = [0, 255]
    ranges = [h_ranges, s_ranges]
    hist = cv2.calcHist(hsv, [0, 1], mask, hist_size, ranges)
    
    return hist
