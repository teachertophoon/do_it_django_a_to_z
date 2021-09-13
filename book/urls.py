from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.book_detail), # FBV 방식
    path('', views.book_list) # FBV 방식
]