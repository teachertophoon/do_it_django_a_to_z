from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author: 추후 작성 예정

    # 관리자 페이지에서 작성한 Post의 제목 구성을 바꾸고 싶을 때
    def __str__(self):
        return f'[{self.pk}] {self.title}' # f는 format을 의미

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
