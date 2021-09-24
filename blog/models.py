import os

from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # 카테고리 페이지의 URL를 반환하는 함수
    def get_absolute_url(self):
        # 카테고리 페이지의 URL을 구성한다.
        # 카테고리 페이지 URL은 '/blog/category/[카테고리의 slug 필드 값]/' 이다.
        # 예) [문화 & 예술] 카테고리는 '/blog/category/문화-예술/'로 만들어진다.
        # 키워드 f는 format의 약자로 변수와 문자열로 구성하여 하나의 문자열을 완성시킨다.
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # CASCADE: 작성자 정보가 User 테이블에서 삭제되면 작성했던 글도 함께 삭제
    # SET_NULL: 작성자 정보가 User 테이블에서 삭제되면 작성했던 글은 유지(author는 null)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 관리자 페이지에서 작성한 Post의 제목 구성을 바꾸고 싶을 때
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}' # f는 format을 의미

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]


