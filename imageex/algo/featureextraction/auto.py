import cv2

def extract(greyscaleImg, mask):
    featurePoints(greyscaleImg, mask)

def featurePoints(greyscaleImg, mask):
    surf_keypoints = cv2.SURF.detect(greyscaleImg, mask)
    #params = (maxSize, responseThreshold, lineThresholdProjected, lineThresholdBinarized, suppressNonmaxSize)
    #star_keypoints = cv.GetStarKeypoints(greyscaleImg, (8, 30, 10, 8, 3))
    return [surf_keypoints]#, star_keypoints]