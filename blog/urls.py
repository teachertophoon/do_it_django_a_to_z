from django.urls import path
from . import views

urlpatterns = [
    path('ajax/', views.ajax),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),

    # /blog/포스트 글번호/new_comment/ 요청을 받으면
    # views.py의 new_comment FBV방식으로 보낸다.
    path('<int:pk>/new_comment/', views.new_comment),

    path('update_post/<int:pk>/', views.PostUpdate.as_view()),

    # /blog/create_post/ 요청을 받으면
    # CBV 방식으로 PostCreate 클래스의 as_view() 함수를 호출한다.
    path('create_post/', views.PostCreate.as_view()),

    # 카테고리 페이지 url 처리를 위해 아래 코드를 작성
    # slug는 문자열 형태이므로 str 키워드를 사용 (아래 <int:pk>와 비교해보세요)
    # 두 번째 파라메터는 첫 번째 파라메터 형식의 URL을 입력했을 때 실행할 view를 지정
    # 여기서는 FBV 방식으로 views.py 파일의 tag_page(slug) 함수를 호출
    path('tag/<str:slug>/', views.tag_page),

    # 카테고리 페이지 url 처리를 위해 아래 코드를 작성
    # slug는 문자열 형태이므로 str 키워드를 사용 (아래 <int:pk>와 비교해보세요)
    # 두 번째 파라메터는 첫 번째 파라메터 형식의 URL을 입력했을 때 실행할 view를 지정
    # 여기서는 FBV 방식으로 views.py 파일의 category_page(slug) 함수를 호출
    path('category/<str:slug>/', views.category_page),
    
    path('<int:pk>/', views.PostDetail.as_view()),
    # path('<int:pk>/', views.single_post_page), # 서버주소/blog/<int:pk>/
    path('', views.PostList.as_view()),
    # path('', views.index), # 서버주소/blog/ 경로 접근 시 views.py의 index 함수
]