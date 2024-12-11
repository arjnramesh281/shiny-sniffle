from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import os


# Create your views here.

# ----------------login ---------------

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

# --------------Logout function----------------

def admin_logout(req):
    logout(req)
    req.session.flush()
    return redirect(log)


# --------------add category and display-------------

def add_category(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            c_name = req.POST['c_name']
            Category.objects.create(c_name=c_name.lower())
            categories = Category.objects.all()
            return render(req, 'admin/add_category.html', {'categories': categories})
        else:
            categories = Category.objects.all()
            return render(req, 'admin/add_category.html', {'categories': categories})
    else:
        return redirect(log)

# ------------------to delete category----------------
def delete_category(req, id):
    if 'admin' in req.session:
        try:
            category = Category.objects.get(id=id)
            category.delete()
        except Category.DoesNotExist:
            pass  # You can add an error message here if needed
        return redirect(add_category)
    else:
        return redirect(log)



# ------------------to add brand ----------------

def add_brand(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            b_name = req.POST['b_name']
            Brand.objects.create(b_name=b_name.lower())
            brands = Brand.objects.all()
            return render(req, 'admin/add_brand.html', {'brands': brands})
        else:
            
            brands = Brand.objects.all()
            return render(req, 'admin/add_brand.html', {'brands': brands})
    else:
        return redirect(log)

# -----------------to delete a brand -----------------

def delete_brand(req, id):
    if 'admin' in req.session:
        try:
            brand = Brand.objects.get(id=id)
            brand.delete()
        except Brand.DoesNotExist:
            pass  
        return redirect(add_brand)
    else:
        return redirect(log)
    



#----------------- add product --------------------

def add_pro(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            pid = req.POST['pid']
            name = req.POST['name']
            dis = req.POST['dis']
            price = req.POST['price']
            off_price = req.POST['off_price']
            file = req.FILES['img']
            gender = req.POST['gender']
            pro_category_id = req.POST['pro_category']  # Get selected category ID
            pro_brand_id = req.POST['pro_brand']  # Get selected brand ID
            
            # Fetch the related Category and Brand objects
            pro_category = Category.objects.get(id=pro_category_id)
            pro_brand = Brand.objects.get(id=pro_brand_id)
            
            # Save the product with the related Category and Brand
            data = Product.objects.create(
                pid=pid,
                name=name,
                dis=dis,
                price=price,
                off_price=off_price,
                img=file,
                gender=gender.lower(),
                pro_category=pro_category,
                pro_brand=pro_brand
            )
            data.save()
            return redirect(add_pro)
        else:
            # Fetch categories and brands to populate dropdowns
            categories = Category.objects.all()
            brands = Brand.objects.all()
            return render(req, 'admin/add_pro.html', {'categories': categories, 'brands': brands})
    else:
        return redirect(log)
    

# ----------------admin home---------------- 
    
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

# -----------------to change carousel--------------------

def carousel(req):
    return render(req,'admin/carousel.html')







# ---------------------user home --------------------------

def user_home(req):
    return render(req,'user/uhome.html')


def about(req):
    return render(req,'user/about.html')


# ------------------------registration function------------------------

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

def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,"user/uhome.html",{"products":data})
    else:
        return redirect(log)

