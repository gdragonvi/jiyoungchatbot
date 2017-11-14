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
                    if 'quick_reply' in  message['message']:
                        payload = message['message']['quick_reply']['payload']
                        if payload == '1':
                            send_message = Message(text='1. 평일 아침 8시 이전 주문건까지 대부분 당일 배송됩니다. \n2. 8시 이후 주문건은 다음날 배송됩니다. \n금요일 8시 이후 주문건은 다음주 월요일에 배송됩니다.\n3. 브라운백 커피는 CJ 대한통운을 통해 커피를 보내드립니다.\n쇼핑몰에서 구매하신 경우, 택배 출고시 문자메시지로 송장 번호를 안내해드립니다. \n문자로 받으신 송장번호를 복사하셔서 아래 CJ 대한통운 배송조회 사이트에서 조회해주시면 됩니다.\n4. 콜드브루와 원두를 같이 주문하시면 각각 다른 곳에서 배송되어, 택배를 두개로 나눠 받으십니다.\n더 궁금하신 점은 언제든 문의주세요. 감사합니다^^')
                        elif payload == '2':
                            send_message = Message(text='1. 샘플 신청 : 아래 링크를 눌러 샘플 발송에 필요한 정보를 입력해주시면 됩니다.\n맛 보시고 궁금하신 사항이나 추가 요청 사항이 있으시면 언제든 문의주세요!\n2. 샘플 배송 : 신청해주신 후 2~3일 이내 배송이 시작됩니다. \n신청이 들어온 순서대로 순차적으로 배송해드리오니 조금만 기다려주세요^^')
                    else:
                        text = message['message']['text']
                        send_message = Message(text='안녕하세요. 브라운백 커피입니다.궁금하신 점은 본 공식 카카오톡 아이디 / 공식 전화 1644-1530 로 연락 주시면 언제든지 친절히 답변드리겠습니다! \n\n"선택"을 입력해주세요.')
                        if text == '안녕':
                            send_message = Message(text='안녕하세요. 브라운백커피입니다. 친구 추가해 주셔서 감사합니다.앞으로 다양한 소식과 혜택/정보를 메시지로 받으실 수 있습니다.브라운백커피를 친구추가해주셔서 감사합니다!궁금하신 점은 본 공식 카카오톡 아이디 / 공식 전화 1644-1530 로 연락 주시면 언제든지 친절히 답변드리겠습니다!최고의 원두를 정말 좋은 가격으로 드리겠습니다. 오늘도 좋은 하루 되세요 ^^')
                        elif text =='선택':
                            quick_replies = [QuickReplyTextItem(title='제품 배송 일정', payload='1', image_url=None),
                                             QuickReplyTextItem(title='샘플 신청 방법과 샘플 배송', payload='2', image_url=None)]
                            send_message = Message(text='원하시는 버튼을 선택해주세요', quick_replies=QuickReply(quick_reply_items=quick_replies))


                    req.send_message(RequestDataFormat(recipient=Recipient(recipient_id=receiver),
                                                           message=send_message))
        return JsonResponse(data)
    return HttpResponse('Failed to request', status=404)
