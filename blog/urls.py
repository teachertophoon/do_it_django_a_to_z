from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), # 서버주소/blog/ 경로 접근 시 views.py의 index 함수
]