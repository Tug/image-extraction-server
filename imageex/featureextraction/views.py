from models import *
from django.http import HttpResponseBadRequest, HttpResponse
import numpy.ma as ma
import cv2
from imageex.segmentation.views import getOriginalImage, getMask, getOriginalImagePath, getMaskPath
from imageex.algo.featureextraction import color, shape
from imageex.util import imtransform
import json

def extractSample(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return None
    name = request.POST['name']
    features = extract(request)
    if features is None:
        return None
    sample = Sample(flower = getFlowerByName(name), features = json.dumps(features))
    sample.save()
    return sample

def extract(request):
    img = getOriginalImage(request)
    mask = getMask(request)
    if img == None or mask == None:
        return None
    features = extractFeatures(img, mask)
    return features

def extractFeatures(img, mask):
    features  = color.extract(img, mask)
    features += shape.extract(mask)
    return features

def getFlowerByName(name):
    flowers = Flower.objects.filter(name=name)
    if flowers.count() == 0:
        flower = Flower(name = name)
        flower.save()
    else:
        flower = flowers[0]
    return flower

def saveSampleNotExtracted(request):
    if request.method != 'POST' or 'name' not in request.POST:
        return None
    name = request.POST['name']
    img = getOriginalImagePath(request)
    mask = getMaskPath(request)
    if img == None or mask == None:
        return None
    saveNotExtracted(img, mask, name)

def saveNotExtracted(img, mask, name):
    sample = SampleNotExtracted(flower = getFlowerByName(name), image = img, mask = mask)
    sample.save()

def extractSamplesNotExtracted(request):
    samplesNotEx = SampleNotExtracted.objects.all()
    for sampleNotEx in samplesNotEx:
        img = cv2.imread(sampleNotEx.image)
        mask = cv2.imread(sampleNotEx.mask)
        features = extractFeatures(img, mask)
        featuresString = json.dumps(features)
        sample = Sample(flower = sampleNotEx.flower, features = featuresString)
        sample.save()
    return HttpResponse()

