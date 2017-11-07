from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

verify_token = 'testest'
access_token = 'insert_page_access_token'


@csrf_exempt
def web_hook(request):
    print(request)
    if request.method == 'GET':
        if (request.GET.get('hub.mode') == 'subscribe' and request.GET.get(
                'hub.verify_token') == verify_token) and request.GET.get('hub.challenge'):
            return HttpResponse(request.GET.get('hub.challenge'))
    elif request.method == 'POST':
        print(request.body)
        data = json.loads(request.body.decode('UTF-8'))
        return JsonResponse(data)
        return HttpResponse('Failed to request', status=404)
