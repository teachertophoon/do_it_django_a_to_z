from django.db import models

# Book 테이블을 설계하세요.
# - 책 제목: title (CharField, 30자 제한)
# - 저자: book_author (CharField, 128자 제한)
# - 출판사: publisher (CharField, 255자 제한)
# - 가격: price (IntegerField)
# - 출시일: release_date (DateTimeField)
# - 등록일: created_at (DateTimeField)
# - 수정일: updated_at (DateTimeField)
# - 책 설명: content (TextField)
class Book(models.Model):
    title = models.CharField(max_length=30)
    book_author = models.CharField(max_length=128)
    publisher = models.CharField(max_length=255)
    price = models.IntegerField()
    release_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True)

    def __str__(self):
        return f'[{self.pk}] {self.title}'
