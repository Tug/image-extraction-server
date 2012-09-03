from django.http import HttpResponseBadRequest, HttpResponse
from imageex.util.JsonResponse import JsonResponse
from django.shortcuts import render_to_response
from imageex.algo.segmentation.labelize import kmeans, grabCut, watershed2
from imageex.util import imconvert, imtransform, stringutil, rectangleutil
import numpy as np
import os
import re
import cv2
import Image
from django.utils import simplejson
from django.conf import settings
from imageex.algo.segmentation import maskop

def labelize_kmeans(request):
    img = getOriginalImage(request)
    if img is not None:
        mask = kmeans(img)
        postProcMask(mask)
        saveMask(request, mask)
        return JsonResponse({'img': imconvert.array_2_base64(mask)})
    else:
        return HttpResponseBadRequest()
    
def labelize_grabcut(request):
    img = getOriginalImage(request)
    rect = receiveRectangle(request)
    markers = constructMarkers4(request)
    if img is not None:
        mask = grabCut(img, rect, markers)
        postProcMask(mask)
        saveMask(request, mask)
        return JsonResponse({'img': imconvert.array_2_base64(mask)})
    else:
        return HttpResponseBadRequest()

def labelize_watershed(request):
    img = getOriginalImage(request)
    markers = constructMarkers3(request)
    if img is not None and markers is not None:
        mask = watershed2(img, markers)
        postProcMask(mask)
        saveMask(request, mask)
        return JsonResponse({'img': imconvert.array_2_base64(mask)})
    else:
        return HttpResponseBadRequest()


def receiveImageAsArray(request, label):
    pilImg = receivePILImage(request, label)
    if pilImg is not None:
        return imconvert.PIL_2_array(pilImg)
    return None


def postProcMask(mask):
    maskop.extractCentralComponent(mask)


def receivePILImage(request, label):
    if request.method != 'POST':
        return None
    if label in request.POST:
        imgData64 = request.POST[label]
        if imgData64 is not None and len(imgData64) > 0:
            im = imconvert.base64_2_PIL(imgData64)
    elif label in request.FILES:
        file = request.FILES[label]
        if file is not None:
            imgData = file.read()
            if imgData is not None and len(imgData) > 0:
                im = imconvert.binary_2_PIL(imgData)
    else:
        return None
    if im is not None and im.mode == "RGBA": # canvas image is sent with an alpha layer
        # Create a new image with a solid color
        background = Image.new('RGBA', im.size, (255, 255, 255))
        # Paste the image on top of the background
        background.paste(im, im)
        im = background.convert('RGB')
        return im
    return None

def receiveMarkers(request):
    markers = receiveImageAsArray(request, label='mask')
    if markers is not None:
        return markers[:,:,0]
    return None

def constructMarkers3(request):
    newmarkers = receiveMarkers(request)
    if newmarkers is not None:
        current_markers = getCurrentMarkers(request)
        if current_markers is not None:
            current_markers = imtransform.mergeMasks(current_markers, newmarkers)
        else:
            current_markers = newmarkers
            fileName = stringutil.genRandomString(10) + '.png'
            request.session['current_markers'] = fileName
        cv2.imwrite(settings.UPLOAD_FOLDER + '/' + request.session['current_markers'], current_markers)
        return current_markers
    return None

def constructMarkers4(request):
    markers = constructMarkers3(request)
    if markers is not None:
        markers = imtransform.setMarkersValues(markers, black=cv2.GC_FGD, gray=cv2.GC_BGD, white=cv2.GC_PR_BGD)
        current_mask = getMask(request)
        if current_mask is not None:
            # set to probable foreground where the mask is white
            markers[(current_mask >= 250) & (markers == cv2.GC_PR_BGD)] = cv2.GC_PR_FGD
        if cv2.GC_FGD not in markers and cv2.GC_PR_FGD not in markers:
            markers[markers == cv2.GC_PR_BGD] = cv2.GC_PR_FGD
    return markers

def getOriginalImage(request):
    filePath = getOriginalImagePath(request)
    if filePath is not None and os.path.exists(filePath):
        return cv2.imread(filePath)
    return None

def getCurrentMarkers(request):
    filePath = getCurrentMarkersPath(request)
    if filePath is not None:
        if os.path.exists(filePath):
            return cv2.imread(filePath)
        else:
            del request.session['current_markers']
    return None
    
def getMask(request):
    filePath = getMaskPath(request)
    if filePath is not None and os.path.exists(filePath):
        return cv2.imread(filePath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    return None

def saveMask(request, mask):
    maskPath = getMaskPath(request)
    if maskPath is None:
        request.session['mask'] = stringutil.genRandomString(10) + '.png'
        maskPath = getMaskPath(request)
    if mask is not None:
        cv2.imwrite(maskPath, mask)

def getCurrentRectangle(request):
    if not request.session.get('current_rectangle', False):
        return None
    return request.session['current_rectangle']

def receiveRectangle(request):
    if not all(test in request.POST for test in ('rectangle[x]',
                                              'rectangle[y]',
                                              'rectangle[width]',
                                              'rectangle[height]')):
        return getCurrentRectangle(request)
    x = int(request.POST['rectangle[x]'])
    y = int(request.POST['rectangle[y]'])
    width = int(request.POST['rectangle[width]'])
    height = int(request.POST['rectangle[height]'])
    rectangle = (x, y, width, height)
    request.session['current_rectangle'] = rectangle
    return rectangle


def reset(request):
    if request.session.get('mask', False):
        del request.session['mask']
    if request.session.get('current_markers', False):
        filePath = settings.UPLOAD_FOLDER + '/' + request.session['current_markers']
        os.remove(filePath)
        del request.session['current_markers']
    if request.session.get('rectangle', False):
        del request.session['rectangle']
    return HttpResponse()


    
def getOriginalImagePath(request):
    if not request.session.get('original_image', False):
        return None
    return settings.UPLOAD_FOLDER + '/' + request.session['original_image']
    
def getCurrentMarkersPath(request):
    if not request.session.get('current_markers', False):
        return None
    return settings.UPLOAD_FOLDER + '/' + request.session['current_markers']

def getMaskPath(request):
    if not request.session.get('mask', False):
        return None
    return settings.UPLOAD_FOLDER + '/segmentation/' + request.session['mask']




