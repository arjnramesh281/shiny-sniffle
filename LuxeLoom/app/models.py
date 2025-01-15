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
    s_size=models.CharField(null=True,max_length=10,blank=True)
    p_size=models.PositiveIntegerField(null=True,blank=True)
    stock=models.PositiveIntegerField()

    def __str__(self):
        if self.s_size:
            return f"{self.s_size}"
        return f"{self.p_size}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  # Link to the Size model
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def total_discounted_price(self):
        return self.quantity * self.product.off_price


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)