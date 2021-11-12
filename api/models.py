from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}::{self.name}::{self.created_at}'

class DHT(models.Model):
    humidity = models.FloatField()
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}::{self.created_at}'
