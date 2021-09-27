from django.contrib import admin
from .models import Post, Category, Tag  # 우리가 만든 Post 클래스 불러오기

admin.site.register(Post) # Post 클래스를 관리자 사이트에 등록

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Tag 테이블을 관리하기 위한 메뉴를 관리자 페이지에 추가
class TagAdmin(admin.ModelAdmin):
    # 태그가 추가되기 직전에 입력한 name 값을 slug에 자동 입력하도록 설정 
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

# 태그 관리 메뉴를 커스텀한 방식으로 추가
admin.site.register(Tag, TagAdmin)

