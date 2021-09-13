from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    # path('<int:pk>/', views.single_post_page), # 서버주소/blog/<int:pk>/
    path('', views.PostList.as_view()),
    # path('', views.index), # 서버주소/blog/ 경로 접근 시 views.py의 index 함수
]