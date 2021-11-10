from django.http import JsonResponse
from django.views import View

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
