import numpy as np
import cv2
import numpy.ma as ma
import imageex.util.imtransform as imtransform

def extract(img, mask):
    
    hsv = imtransform.rgb2hsv(img)
    
    h = np.array(hsv[:,:,0])
    s = np.array(hsv[:,:,1])
    maskedH = ma.array(h, mask=mask)
    maskedS = ma.array(s, mask=mask)
    objH = maskedH.compressed()
    objS = maskedS.compressed()
    
    # histogram
    histH, bin_edges_h = np.histogram(objH, bins=10, normed=True)
    
    # color moments
    moments = cv2.moments(h, binary = 0)
    huMoments = cv2.HuMoments(moments)
    
    # 1D moments
    # mean
    moment_H_1 = objH.mean()
    # standard deviation
    moment_H_2 = objH.std()
    # skewness
    objHtemp = (objH - moment_H_1) ** 3
    objmean = objHtemp.mean()
    sign = objmean/abs(objmean)
    moment_H_3 = sign * (abs(objmean) ** (1./3))
    
    #normalize
    moment_H_1 = moment_H_1/255
    moment_H_2 = moment_H_2/255
    moment_H_3 = moment_H_3/255
    
    features = []
    features += list(histH) # 10
    features += list(huMoments) # 7
    #features += moment_H_1, moment_H_2, moment_H_3 # 3
    
    return features # 17 # 20
