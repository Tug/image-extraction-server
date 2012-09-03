import numpy as np
from scipy.cluster.vq import vq, kmeans2, whiten
from scipy.stats import threshold
from scipy.ndimage.measurements import watershed_ift
import imageex.algo.color.convert as color
from imageex.util import imtransform, rectangleutil
import cv2
from django.conf import settings


def kmeans(img):
    height, width, channels = img.shape
    lab_img = color.rgb2lab(img.astype(np.float32) / 255)
    ab_img = lab_img[:, :, 1:3].flatten()
    ab_img.shape = (ab_img.size / 2, 2)
    cluster_count = 2
    centroid, clusters = kmeans2(whiten(ab_img), cluster_count)
    clusters = 255 * clusters
    clusters.shape = (height, width)
    sumBorders = sum(clusters[0,:]) + sum(clusters[:,0]) + sum(clusters[-1,:]) + sum(clusters[:,-1])
    if sumBorders/(2*(height+width)) > 127:
        clusters = 255 - clusters
    mask = np.array(clusters, dtype=np.uint8)
    return mask

def watershed2(img, markers):
    markers = np.int8(imtransform.setMarkersValues(markers, black=1, gray=-1, white=0))
#    markers2 = np.zeros(markers.shape, np.uint8)
#    markers2[markers == 1] = 0
#    markers2[markers ==-1] = 127
#    markers2[markers == 0] = 255
#    imsave(settings.UPLOAD_FOLDER + '/markers222222.png', markers2)
    greyImg = imtransform.rgb_2_greyscale(img)
    mask = watershed_ift(greyImg, markers)
    mask[mask < 0] = 0
    mask = 255 * mask
    return np.array(mask, dtype=np.uint8)

def grabCut(img, rect=None, mask=None, ite=5):
    height, width, channels = img.shape
    # if no arguments, try to segment using a large rectangle
    if rect == None and mask == None:
        rect = (int(width*0.15), 15, int(width*0.85), height-15)
        initOpt = cv2.GC_INIT_WITH_RECT
    # if rectangle argument but no mask, init mask with rectangle
    elif mask == None:
        mask = np.zeros((height, width), np.uint8)
        initOpt = cv2.GC_INIT_WITH_RECT
    # if mask argument but no rectangle, use mask and let rect to None
    elif rect == None:
        initOpt = cv2.GC_INIT_WITH_MASK
        rect = (0, 0, width, height)
        mask = np.uint8(mask)
    # if mask argument and rectangle, set pixels outside the mask as background
    else:
        mask = np.uint8(mask)
        rect = rectangleutil.checkRectangleBounds(rect, mask.shape)
        maskRect = rectangleutil.rectangle2mask(rect, mask.shape)
        mask[maskRect == 0] = cv2.GC_BGD
        initOpt = cv2.GC_INIT_WITH_MASK
    #imageblured = np.zeros(img.shape, img.dtype)
    #cv2.smooth(img, imageblured, cv.CV_GAUSSIAN, 5)
    tmp1 = np.zeros((1, 13 * 5))
    tmp2 = np.zeros((1, 13 * 5))
    cv2.grabCut(img, mask, rect, tmp1, tmp2, ite, initOpt)
    mask[mask == cv2.GC_BGD] = 0
    mask[mask == cv2.GC_PR_BGD] = 0
    mask[mask == cv2.GC_FGD] = 255
    mask[mask == cv2.GC_PR_FGD] = 255
    return mask


