from django.urls import path

from api import views

urlpatterns = [
    path('test/', views.TestView.as_view()),
    path('car/', views.CarView.as_view()),
    path('dht/', views.DHTView.as_view()),
]