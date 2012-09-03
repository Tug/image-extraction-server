
from numpy import array, float32, int8, int32, max, min
from scipy.stats import threshold
from scipy.cluster.vq import vq, kmeans2, whiten
from scipy.ndimage.measurements import watershed_ift

from scipy.misc.pilutil import imread, imsave
from matplotlib.pyplot import imshow
import color

img = imread("blue.jpg")
markers = imread("bluem2.jpg")
markers = int32(markers[:, :, 1])
markers = threshold(markers, 100, None, 1) # black to 1
print max(markers)
print min(markers)
markers = threshold(markers, None, 200, -1) # white to -1
print max(markers)
print min(markers)
markers = threshold(markers, None, 2, 0) # gray to 0
markers = int8(markers)
mask = watershed_ift(img[:, :, 1], markers)

print mask
mask = mask + 1
print mask
print max(mask)
mask = threshold(mask, None, 1, 1)
print max(mask)
mask = 255 * mask
imsave("mask_watershed.jpg", mask)

a = 1
