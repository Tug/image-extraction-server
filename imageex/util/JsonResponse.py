from django.http import HttpResponse
from django.utils import simplejson

class JsonResponse(HttpResponse):
    def __init__(self, data):
        content = simplejson.dumps(data)
        super(JsonResponse, self).__init__(content, 'application/json; charset=utf8')

