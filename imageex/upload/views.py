from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.conf import settings
from imageex.util.JsonResponse import JsonResponse
from os import path
from forms import UploadFileForm
from imageex.util import stringutil, fileutil, imconvert, imtransform
import Image

def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        return saveImage(request, file.read())
    else:
        return HttpResponseBadRequest()

def upload_file_raw(request):
    if request.method == 'POST':
        fileData = request.raw_post_data
        return saveImage(request, fileData)
    else:
        return HttpResponseBadRequest()

def saveImage(request, data):
    randomStr = stringutil.genRandomString(10)
    fileNameServer = randomStr + '.jpg'
    destinationFile = settings.UPLOAD_FOLDER + '/' + fileNameServer
    imgPIL = imconvert.binary_2_PIL(data)
    if 'canvas-size[width]' in request.GET.keys() and 'canvas-size[height]' in request.GET.keys():
        canvasWidth = int(request.GET['canvas-size[width]'])
        canvasHeight = int(request.GET['canvas-size[height]'])
        imtransform.scalePILImage(imgPIL, (canvasWidth, canvasHeight))
    imgPIL.save(destinationFile, "JPEG")
    request.session['original_image'] = fileNameServer
    return JsonResponse({'imgUrl': settings.UPLOAD_URL + "/" + fileNameServer})
