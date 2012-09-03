from django.http import HttpResponseNotAllowed
from django.shortcuts import render_to_response


def home(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return render_to_response('index.html')


