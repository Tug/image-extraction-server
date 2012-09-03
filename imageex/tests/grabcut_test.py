import cv2
import numpy as np
img = cv2.imread("./pglwCBXQzV.jpg")
height, width, channels = img.shape
mask = np.zeros((height, width), np.uint8)
tmp1 = np.zeros((1, 13 * 5))
tmp2 = np.zeros((1, 13 * 5))
ite = 5
initOpt = cv2.GC_INIT_WITH_RECT
rect = (50, 50, width-50, height-50)
cv2.grabCut(img, mask, rect, tmp1, tmp2, ite, initOpt)
exit()
