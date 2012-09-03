from models import *
from imageex.featureextraction.models import *
from django.http import HttpResponseBadRequest, HttpResponse
import numpy as np
from imageex.segmentation.views import getOriginalImage, getMask, getOriginalImagePath, getMaskPath
from imageex.featureextraction.views import extract, extractSample, saveSampleNotExtracted
from imageex.util import imtransform, imconvert
import json
from scikits.learn import svm, mixture
from imageex.util.JsonResponse import JsonResponse
from django.shortcuts import render_to_response
import Image
from django.conf import settings
import os

MAX_SAMPLES = 200
NB_CLASSES = 15
SHOW_NB_CLASSES = 3
IMG_PATH = "static/classes_icon/"

def predictClassHTML(request, classifier):
    flowers = predict(request, classifier)
    for flower in flowers:
        flower["src"] = IMG_PATH + flower["id"] + ".jpg"
    if flowers is None:
        return HttpResponseBadRequest()
    return render_to_response('result.html', {"results": flowers })

def predictClassHTMLimageinlined(request, classifier):
    flowers = predict(request, classifier)
    if flowers is None:
        return HttpResponseBadRequest()
    absImgPath = os.path.abspath(os.path.join(settings.DIRNAME, IMG_PATH))
    for flower in flowers:
        flower["src"] = imconvert.PIL_2_base64(Image.open(os.path.join(absImgPath, str(flower["id"]) + ".jpg")))
    return render_to_response('result.html', {"results": flowers })
    
def predictClassJSON(request, classifier):
    flowers = predict(request, classifier)
    if flowers is None:
        return HttpResponseBadRequest()
    return JsonResponse(flowers)





def learn2(request, classifier):
    saveSampleNotExtracted(request)
    return HttpResponse()

def learn(request, classifier):
    clf = loadLearningMachine(classifier)
    if clf is None:
        return HttpResponseBadRequest()
    extractSample(request)
    return learnAllSamples(request, classifier)

def predict(request, classifier):
    clf = loadLearningMachine(classifier)
    if clf is None:
        return None
    features = extract(request)
    clfObj = clf.getData()
    Y = clfObj.predict_proba([features])
    if Y is None:
        return None
    Y = Y[0]
    classes = np.argsort(Y)
    classes = classes[::-1]
    classes = classes[0:SHOW_NB_CLASSES]
    #flowers = Flower.objects.filter(pk__in=classes)
    flowers = []
    for c in classes:
        flowerid = c+1
        proba = Y[c]
        flower = Flower.objects.get(id=flowerid)
        if flower is None:
            continue
        flo = {}
        flo["id"] = flowerid
        flo["name"] = flower.name
        flo["proba"] =  "%.1f" % (proba * 100)
        flowers.append(flo)
    return flowers

def loadLearningMachine(classifier):
    classifiers = Classifier.objects.all()
    for clfObj in classifiers:
        if clfObj.name == classifier:
            return clfObj
    return None

def learnAllSamples(request, classifier):
    clf = loadLearningMachine(classifier)
    if clf is None:
        return HttpResponseBadRequest()
    samples = Sample.objects.all()
    clfObj = clf.getData()
    X = [json.loads(sample.features) for sample in samples]
    Y = [sample.flower.id for sample in samples]
    clfObj.fit(X,Y)
    clf.setData(clfObj)
    clf.save()
    return HttpResponse()

def createClassifiers(request):
    #Classifier.objects.all().delete()
    linearsvc = Classifier(name="svc1", serialized = serialize(svm.SVC(probability=True)))
    linearsvc.save()
    return HttpResponse()


