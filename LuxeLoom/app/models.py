from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    c_name=models.CharField(max_length=50)

class Brand(models.Model):
    b_name=models.CharField(max_length=50)

    

class Product(models.Model):
    pid=models.CharField(max_length=20)
    name=models.CharField(max_length=100)
    dis=models.TextField()
    price=models.PositiveIntegerField()
    off_price=models.PositiveIntegerField()
    img=models.FileField()
    gender=models.CharField(max_length=50)
    pro_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    pro_brand=models.ForeignKey(Brand,on_delete=models.CASCADE)

class Size(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    s_size=models.CharField(null=True,max_length=10)
    p_size=models.PositiveIntegerField(null=True)
    stock=models.PositiveIntegerField()
