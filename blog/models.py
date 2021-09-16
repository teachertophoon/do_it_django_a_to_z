import os

from django.contrib.auth.models import User
from django.db import models

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

    # 관리자 페이지에서 작성한 Post의 제목 구성을 바꾸고 싶을 때
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}' # f는 format을 의미

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]