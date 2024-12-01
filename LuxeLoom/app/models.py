from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    pid=models.CharField(max_length=20)
    name=models.CharField(max_length=100)
    dis=models.TextField()
    price=models.PositiveIntegerField()
    off_price=models.PositiveIntegerField()
    stock=models.PositiveIntegerField()
    img=models.FileField()
    category=models.CharField(max_length=50)
