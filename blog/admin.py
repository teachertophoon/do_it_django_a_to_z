from django.contrib import admin
from .models import Post # 우리가 만든 Post 클래스 불러오기

admin.site.register(Post) # Post 클래스를 관리자 사이트에 등록
