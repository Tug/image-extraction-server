from scipy.misc.pilutil import imread, imsave
import numpy.ma as ma
import cv
import numpy as np
import Image
import numpy.ma as ma
from scikits.learn import mixture
import numpy.random as random
import itertools
import pylab as pl
import matplotlib as mpl
import math

def rgb2hsv(img):
    # Convert to HSV
    hsv = np.zeros(img.shape, img.dtype)
    cv.CvtColor(img, hsv, cv.CV_RGB2HSV)
    return hsv

def rgb_2_greyscale(rgbImage):
    return np.uint8(0.2989 * rgbImage[:,:,0] + 0.5870*rgbImage[:,:,1] + 0.1140*rgbImage[:,:,2])


def shapeAnalysis(mask):
    
    height, width = mask.shape
    pixels = height * width
    
    # spatial and central moments
    moments = cv.Moments(mask, binary = 1)
    huMoments = cv.GetHuMoments(moments)
    print "Shape hu moments", huMoments
    
    # distances from the gravity point
    contour_seq = cv.FindContours(np.array(mask), cv.CreateMemStorage(), cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE)
    gravity_center = (int(moments.m10/moments.m00), int(moments.m01/moments.m00)) # (x, y)
    gx, gy = gravity_center
    distances = np.array([math.sqrt((gx - x)**2 + (gy - y)**2) for (x,y) in contour_seq])
    dist_distri, bin_dist  = np.histogram(distances, bins=10, range=None, normed=True)
    print "dist distribution", dist_distri
    dist_max = np.max(distances)
    dist_min = np.min(distances)
    dist_ratio_min_max = dist_min / dist_max
    print "dist ratio min max", dist_ratio_min_max
    dist_mean = np.mean(distances)
    dist_std = np.std(distances)
    
    # normalize distance min and max
    dist_max = dist_max / pixels
    dist_min = dist_min / pixels
    dist_mean = dist_mean / pixels
    dist_std = dist_std / pixels
    print "dist max", dist_max
    print "dist min", dist_min
    print "dist mean", dist_mean
    print "dist std", dist_std
    
    # number of petals
    nbPetals = np.sum([min(x1,x2) < dist_mean < max(x1,x2) for x1,x2 in zip(distances[:-1], distances[1:])])/2
    print "petals", nbPetals
    
    poly_seq = cv.ApproxPoly(contour_seq, cv.CreateMemStorage(), cv.CV_POLY_APPROX_DP, 2.8)
    ppimg = np.zeros(mask.shape)
    for (x, y) in poly_seq:
        ppimg[y, x] = 255
    imsave('/home/cplab/workspace/imageex/src/imageex/static/POLYYYAAAAA.png', ppimg)
    
    convex_hull = cv.ConvexHull2(poly_seq, cv.CreateMemStorage())
    convexity_defects = cv.ConvexityDefects(poly_seq, convex_hull, cv.CreateMemStorage())
    
    # number of defects
    nbDefects = len(convexity_defects)
    print "defects", nbDefects
    
    convexity_seq = sum([[cd[0], cd[2], cd[1]] for cd in convexity_defects], [])
    ppimg = np.zeros(mask.shape)
    for (x, y) in convexity_seq:
        ppimg[y, x] = 255
    imsave('/home/cplab/workspace/imageex/src/imageex/static/CONVEXXAAAAA.png', ppimg)
    
    convexity_depths = np.array([cd[3] for cd in convexity_defects])
    convexity_depth_max = np.max(convexity_depths)
    convexity_depth_min = np.min(convexity_depths)
    convexity_depth_ratio_min_max = convexity_depth_min / convexity_depth_max
    print "convexity depth ratio min max", convexity_depth_ratio_min_max
    
    #normalize
    convexity_depth_max = convexity_depth_max / pixels
    
    print "convexity depth max", convexity_depth_max
    
    area = cv.ContourArea(contour_seq)
    perimeter = cv.ArcLength(contour_seq)
    perimeterOarea = perimeter/area
    print "perimeter over area", perimeterOarea

    features = []
    features += list(huMoments)
    features += dist_distri, dist_ratio_min_max, dist_max, dist_min, dist_mean, dist_std
    features += nbPetals, nbDefects
    features += convexity_depth_ratio_min_max, convexity_depth_max, perimeterOarea
    
    return features
    
def colorAnalysis(hsv, mask):
    h = np.array(hsv[:,:,0])
    s = np.array(hsv[:,:,1])
    maskedH = ma.array(h, mask=mask)
    maskedS = ma.array(s, mask=mask)
    objH = maskedH.compressed()
    objS = maskedS.compressed()
    
    # histogram
    histH, bin_edges_h = np.histogram(objH, bins=10, range=None, normed=True)
    histS, bin_edges_s = np.histogram(objS, bins=10, range=None, normed=True)
    print "Hue histogram", histH
    
    # color moments
    moments = cv.Moments(h, binary = 0)
    huMoments = cv.GetHuMoments(moments)
    print "Color hu moments", huMoments
    
    # 1D moments
    # mean
    moment_H_1 = objH.mean()
    moment_S_1 = objS.mean()
    # standard deviation
    moment_H_2 = objH.std()
    moment_S_2 = objS.std()
    # skewness
    objHtemp = objH - moment_H_1
    objStemp = objS - moment_S_1
    objHtemp = ma.power(objHtemp, 3)
    objStemp = ma.power(objStemp, 3)
    moment_H_3 = objHtemp.mean() ** (1./3)
    moment_S_3 = objStemp.mean() ** (1./3)
    
    #normalize
    moment_H_1 = moment_H_1/255
    moment_H_2 = moment_H_2/255
    moment_H_3 = moment_H_3/255
    
    
    features = []
    features += list(histH)
    features += list(huMoments)
    features += moment_H_1, moment_H_2, moment_H_3
    
    return features



def featurePoints(greyscaleImg, mask):
    surf_keypoints, surf_descriptors = cv.ExtractSURF(greyscaleImg, mask, cv.CreateMemStorage(), (1, 3000, 3, 4))
    img2 = np.array(img)
    for ((x, y), laplacian, size, dir, hessian) in surf_keypoints:
        if laplacian == -1:
            img2[int(y),int(x), 0] = 255
            img2[int(y),int(x), 1] = 0
            img2[int(y),int(x), 2] = 0
        else:
            img2[int(y),int(x), 0] = 0
            img2[int(y),int(x), 1] = 0
            img2[int(y),int(x), 2] = 255
    imsave('/home/cplab/workspace/imageex/src/imageex/static/SURFFFFFF.png', img2)

    #params = (maxSize, responseThreshold, lineThresholdProjected, lineThresholdBinarized, suppressNonmaxSize)
    star_keypoints = cv.GetStarKeypoints(greyscaleImg, cv.CreateMemStorage(), (8, 30, 10, 8, 3))
    img3 = np.array(img)
    for ((x, y), size, response) in star_keypoints:
        if response >= 0:
            img3[int(y),int(x), 0] = 255
            img3[int(y),int(x), 1] = 0
            img3[int(y),int(x), 2] = 0
        else:
            img3[int(y),int(x), 0] = 0
            img3[int(y),int(x), 1] = 0
            img3[int(y),int(x), 2] = 255
    imsave('/home/cplab/workspace/imageex/src/imageex/static/STARRRRR.png', img3)
    return []

#img = imread('/home/cplab/workspace/imageex/src/imageex/static/uploads/EPZZtChQXE.JPG')
#mask = imread('/home/cplab/workspace/imageex/src/imageex/static/uploads/segmentation/AxHBuxBWZE.png')
img = imread('/home/cplab/workspace/imageex/src/imageex/static/uploads/IwmzjtKPUf.jpg')
mask = imread('/home/cplab/workspace/imageex/src/imageex/static/uploads/segmentation/CidVVYLJfe.png')
hsv = rgb2hsv(img)
greyscaleImg = rgb_2_greyscale(img)

features  = shapeAnalysis(mask)
features += colorAnalysis(hsv, mask)
#features += featurePoints(greyscaleImg, mask)
print "features : ", features

nbFeatures = len(features)

n, m = 100, 2

# generate random sample, two components
np.random.seed(0)
C = np.random.randn(n, nbFeatures)
X = np.r_[np.dot(np.random.randn(nbFeatures, n), C), np.random.randn(n, nbFeatures) + C]

clf = mixture.GMM(n_states=10, cvtype='tied')
clf.fit(X)
print clf.decode(X)

splot = pl.subplot(111, aspect='equal')
color_iter = itertools.cycle (['r', 'g', 'b', 'c'])

Y_ = clf.predict(X)

for i, (mean, covar, color) in enumerate(zip(clf.means, clf.covars, color_iter)):
    v, w = np.linalg.eigh(covar)
    u = w[0] / np.linalg.norm(w[0])
    pl.scatter(X[Y_==i, 0], X[Y_==i, 1], .8, color=color)
    angle = np.arctan(u[1]/u[0])
    angle = 180 * angle / np.pi # convert to degrees
    ell = mpl.patches.Ellipse (mean, v[0], v[1], 180 + angle, color=color)
    ell.set_clip_box(splot.bbox)
    ell.set_alpha(0.5)
    splot.add_artist(ell)

pl.show()
