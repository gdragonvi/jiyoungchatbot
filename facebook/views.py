from django.shortcuts import render

# Create your views here.
import json
from blueforge.apis.facebook import CreateFacebookApiClient, RequestDataFormat, Recipient, Message, QuickReply, QuickReplyTextItem
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

verify_token = 'testest'
access_token = 'EAAcD9VAasYwBANt3KcuSfusZCaCPUQi6lhYXAvg8JuLZC7U6znuWKPkj9DHz3UBsYaKNARsIVB4l1WBEHaDp9uVHUfMA8j3xPYaLDjMwFE8qVqoSC8gRmpKTvrQc7ZCLo9j4L2zqJaeti5tpcyp2rmP7qHZAcNMp3SlZARZAHI7QZDZD'

req = CreateFacebookApiClient(access_token=access_token)


@csrf_exempt
def web_hook(request):
    print(request)
    if request.method == 'GET':
        if request.GET.get('hub.verify_token') == verify_token:
            return HttpResponse(request.GET.get('hub.challenge'))
    elif request.method == 'POST':
        print(request.body)
        data = json.loads(request.body.decode('UTF-8'))

        for entry in data['entry']:
            for message in entry['messaging']:
                receiver = message['sender']['id']
                if 'message' in message:
                    text = message['message']['text']
                    if text == '안녕':
                        send_message = Message(text='반가워')
                    elif text =='나이':
                        quick_replies = [QuickReplyTextItem(title='10살', payload='10', image_url=None),
                                         QuickReplyTextItem(title='20살', payload='20', image_url=None)]
                        send_message = Message(text='알아 맞춰봐~ ', quick_replies=QuickReply(quick_reply_items=quick_replies))
                    else:
                        send_message = Message(text=text)

                    req.send_message(RequestDataFormat(recipient=Recipient(recipient_id=receiver),
                                                           message=send_message))
        return JsonResponse(data)
    return HttpResponse('Failed to request', status=404)
