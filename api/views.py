import json

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from api.models import Car, DHT

# CBV 방식
class TestView(View):

    # GET 요청을 처리하기 위해서 get 함수를 재정의
    def get(self, request, *args, **kwargs):
        # python의 딕셔너리를 이용해서 클라이언트로 전달할 데이터를 작성
        data = {
            'message': 'success'
        }

        # data 딕셔너리를 직렬화된 JSON 객체로 변경하여
        # 아두이노 클라이언트로 전달한다.
        return JsonResponse(data, status=200)

class CarView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CarView, self).dispatch(request, *args, **kwargs)

    # POST 요청을 처리하기 위해서 post 함수를 재정의
    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == 'application/json':
            req = json.loads(request.body)
            print('name: ' + req['name'] + '\n')
            print('brand: ' + req['brand'] + '\n')
            print('price: ' + str(req['price']) + '\n')

            car = Car(name=req['name'], brand=req['brand'], price=req['price'])
            car.save()

            data = {
                'message': 'success'
            }
            return JsonResponse(data, status=200)

        data = {
            'message': 'failed'
        }
        return JsonResponse(data, status=404)

class DHTView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DHTView, self).dispatch(request, *args, **kwargs)

    # GET 요청을 처리하기 위해서 get 함수를 재정의
    def get(self, request, *args, **kwargs):

        # DHT.objects.all()의 결과는 QuerySet 타입이다.
        # 아래 코드는 QuerySet 타입을 json 타입으로 변경하고
        # json 객체를 직렬화 한 것이다.
        dhts = serializers.serialize("json", DHT.objects.all())
        print(dhts)
        return JsonResponse(dhts, # 직렬화한 json 객체
                            safe=False, # 첫번째 파라미터의 타입이 딕셔너리가 아닐경우
                            json_dumps_params={'ensure_ascii': False}, # 한글지원
                            status=200)

    # POST 요청을 처리하기 위해서 post 함수를 재정의
    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == 'application/json':
            req = json.loads(request.body)
            print('humidity: ' + str(req['humidity']) + '\n')
            print('temperature: ' + str(req['temperature']) + '\n')

            dht = DHT(humidity=req['humidity'], temperature=req['temperature'])
            dht.save()

            data = {
                'message': 'success'
            }
            return JsonResponse(data, status=200)

        data = {
            'message': 'failed'
        }
        return JsonResponse(data, status=404)