import numpy as np
import cv2
import math

def extract(mask):
    
    height, width = mask.shape
    pixels = height * width
    
    # spatial and central moments
    moments = cv2.moments(mask, binary = 1)
    huMoments = cv2.HuMoments(moments)
    
    # distances from the gravity point
    contour_seq = cv2.findContours(np.array(mask), cv2.CV_RETR_TREE, cv2.CV_CHAIN_APPROX_SIMPLE)
    gravity_center = (int(moments.m10/moments.m00), int(moments.m01/moments.m00)) # (x, y)
    gx, gy = gravity_center
    distances = np.array([math.sqrt((gx - x)**2 + (gy - y)**2) for (x,y) in contour_seq])
    dist_distri, bin_dist = np.histogram(distances, bins=10, normed=True)
    dist_max = np.max(distances)
    dist_min = np.min(distances)
    dist_ratio_min_max = dist_min / dist_max
    dist_mean = np.mean(distances)
    dist_std = np.std(distances)
    
    # number of petals
    nbPetals = np.sum([min(x1,x2) < dist_mean < max(x1,x2) for x1,x2 in zip(distances[:-1], distances[1:])])/2
    
    # normalize distance min and max
    dist_max = dist_max / pixels
    dist_min = dist_min / pixels
    dist_mean = dist_mean / pixels
    dist_std = dist_std / pixels
    
    poly_seq = cv2.approxPolyDP(contour_seq, 2.8, True)
    
    convex_hull = cv2.convexHull(poly_seq)
    convexity_defects = cv2.convexityDefects(poly_seq, convex_hull)
    
    # number of defects
    nbDefects = len(convexity_defects)
    
    convexity_depths = np.array([cd[3] for cd in convexity_defects])
    convexity_depth_max = np.max(convexity_depths)
    convexity_depth_min = np.min(convexity_depths)
    convexity_depth_ratio_min_max = convexity_depth_min / convexity_depth_max
    
    #normalize
    convexity_depth_max = convexity_depth_max / pixels
    
    area = cv2.contourArea(contour_seq)
    perimeter = cv2.arcLength(contour_seq, True)
    perimeterOarea = perimeter/area

    features = []
    features += list(huMoments) # 7
    features += list(dist_distri) # 10
    features += dist_ratio_min_max, nbPetals, nbDefects #, dist_max, dist_min, dist_mean, dist_std
    features += convexity_depth_ratio_min_max, convexity_depth_max, perimeterOarea
    
    return features

