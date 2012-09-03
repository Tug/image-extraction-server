import Image
import numpy as np
import cv2

def scalePILImage(pilImg, containerSize):
    imgWidth = pilImg.size[0]
    imgHeight = pilImg.size[1]
    containerWidth = containerSize[0]
    containerHeight = containerSize[1]
    imgRatio = float(imgHeight) / imgWidth
    containerRatio = float(containerHeight) / containerWidth
    if imgRatio > containerRatio:
        newHeight = containerHeight
        newWidth = int(containerHeight / imgRatio)
    else:
        newWidth = containerWidth
        newHeight = int(containerWidth * imgRatio)
    pilImg.thumbnail((newWidth, newHeight), Image.ANTIALIAS)

def rgb2hsv(img):
    return cv2.cvtColor(img, cv2.CV_RGB2HSV)

def rgb_2_greyscale(rgbImage):
    return np.uint8(0.2989 * rgbImage[:,:,0] + 0.5870*rgbImage[:,:,1] + 0.1140*rgbImage[:,:,2])

def mergeMasks(oldmask, newmask):
    return np.where(newmask >= 250, oldmask, newmask)

def setMarkersValues(markers, black=1, gray=-1, white=0):
    markers2 = np.int32(markers)
    markers2[markers <= 120] = black
    markers2[(120 < markers) & (markers <= 200)] = gray
    markers2[markers > 200] = white
    return markers2
