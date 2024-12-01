from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import os


# Create your views here.
def log(req):
    if 'admin' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        print(username+password)
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['admin']=username
                return redirect(admin_home)
            else:
                req.session['user']=username
                return redirect(user_home)
        else:
            messages.warning(req, " Invalid username or password.")
            return redirect(log)
    else:
        return render(req,'login.html')
    
def admin_home(req):
    return render(req,'admin/home.html')

# Logout function..

def admin_logout(req):
    logout(req)
    req.session.flush()
    return redirect(log)



# add product

def add_pro(req):
    if 'admin' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            dis=req.POST['dis']
            price=req.POST['price']
            off_price=req.POST['off_price']
            stock=req.POST['stock']
            file=req.FILES['img']
            category=req.POST['category']
            data=Product.objects.create(pid=pid,name=name,dis=dis,price=price,off_price=off_price,stock=stock,img=file,category=category)
            data.save()
            return redirect(admin_home)
        else:
            return render(req,'admin/add_pro.html')
    else:
        return redirect(log)
    

# admin home 
    
def admin_home(req):
    if 'admin' in req.session:
        # data=Product.objects.all()
        return render(req,'admin/home.html')
    else:
        return redirect(log)
    
def pro_list(req):
    if 'admin' in req.session:
        data=Product.objects.all()
        return render(req,'admin/pro_list.html',{'products':data})
    else:
        return redirect(log)



# user home

def user_home(req):
    return render(req,'user/uhome.html')


# registration page

def reg(req):
    if req.method=='POST':
        username=req.POST['username']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=username,email=email,username=email,password=password)
            data.save()
        except:
            messages.warning(req, " This Email Already In Use.")
            return redirect(reg)
        return redirect(log)
    else:
     return render(req,'user/register.html')

# def user_home(req):
#     if 'user' in req.session:
#         data=Product.objects.all()
#         return render(req,"user/home.html",{"products":data})
#     else:
#         return redirect(log)