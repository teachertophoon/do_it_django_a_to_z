import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

# CBV 방식
from django.views.decorators.csrf import csrf_exempt

from api.models import Car


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
