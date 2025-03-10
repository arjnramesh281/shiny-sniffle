from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
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
            return redirect(add_size_stock)
        else:
            # Fetch categories and brands to populate dropdowns
            categories = Category.objects.all()
            brands = Brand.objects.all()
            return render(req, 'admin/add_pro.html', {'categories': categories, 'brands': brands})
    else:
        return redirect(log)
    

#------------------ add stock--------------------



def add_size_stock(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            products = req.POST['name']  
            pro=Product.objects.get(pk=products)
            s_size = req.POST['s_size'].strip().upper()
            if s_size=='':
                s_size=None
            p_size = req.POST.get('p_size')
            if p_size.isdigit():
                print(p_size,type(p_size)) 
                pass
            else:
                p_size=None
            stock = req.POST['stock']
            data=Size.objects.create(product=pro,s_size=s_size,p_size=p_size,  stock=stock)
            data.save()
            return redirect(add_size_stock)
        else:
            products = Product.objects.all()
            return render(req, 'admin/stock.html',{'products': products})
    else:
        return redirect(log)  


# -----------------edit Product----------------
def edit_pro(req,id):
    if 'admin' in req.session:  # Check if admin is logged in
        try:
            # Fetch the existing product by ID
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            # Handle the case where the product does not exist
            return redirect(add_pro)

        if req.method == 'POST':
            # Update product details
            product.name = req.POST['name']
            product.dis = req.POST['dis']
            product.price = req.POST['price']
            product.off_price = req.POST['off_price']
            product.gender = req.POST['gender'].lower()

            # Check if an image was uploaded
            if 'img' in req.FILES:
                product.img = req.FILES['img']

            # Update the related Category and Brand
            pro_category_id = req.POST['pro_category']
            pro_brand_id = req.POST['pro_brand']
            product.pro_category = Category.objects.get(id=pro_category_id)
            product.pro_brand = Brand.objects.get(id=pro_brand_id)

            product.save()  # Save the updated product
            return redirect(add_pro)  # Redirect to product list or desired page
        else:
            # Fetch categories and brands to populate dropdowns
            categories = Category.objects.all()
            brands = Brand.objects.all()
            return render(req, 'admin/edit_pro.html', {
                'product': product,
                'categories': categories,
                'brands': brands
            })
    else:
        return redirect(log)  # Redirect to login if not an admin


# ---------------delete product----------------

def delete_pro(req, id):
    if 'admin' in req.session:
        try:
            brand = Product.objects.get(id=id)
            brand.delete()
        except Product.DoesNotExist:
            pass  
        return redirect(add_pro)
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



# --------------about page-----------------

def about(req):
    return render(req,'user/about.html')





# ---------------user view product---------------------


def view_product(req,id):
    data= Product.objects.get(pk=id)
    siz=Size.objects.filter(product=data)

    return render(req,'user/view_pro.html',{'product': data,'sizes':siz})



#--------------- view all products--------------


def allpro(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,"user/allpro.html",{"products":data})
    else:
        return redirect(log)
    

# ---------------view mens products---------------

def men_pro(req):
    if 'user' in req.session:
        data=Product.objects.filter(gender='men')
        return render(req,"user/menpro.html",{"products":data})
    


# ---------------view womens products---------------

def women_pro(req):
    if 'user' in req.session:
        data=Product.objects.filter(gender='women')
        return render(req,"user/women.html",{"products":data})


# ----------------new arrivals-------------------

def arrival(req):
    if 'user' in req.session:
        data=Product.objects.all()[::-1][:10]
        return render(req,"user/arrivals.html",{"products":data})
    else:
        return redirect(log)



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



# -----------------home products display-------------------

def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()[::-1][:3]
        data1=Product.objects.filter(gender='women')[::-1][:3]
        data2=Product.objects.filter(pro_brand='3')[::-1]
        return render(req,"user/uhome.html",{"products":data,'womens':data1, 'armani':data2})
    else:
        return redirect(log)




def contact_view(request):
    if request.method == "POST":
        # Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the message to the database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Show success message to the user
        messages.success(request, "Your message has been sent successfully. We will get back to you soon!")
        return redirect('contact')  # Redirect to the contact page after submission

    return render(request, 'user/contact.html')



# ----------------------cart-----------------------

def view_cart(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        cart_items = Cart.objects.filter(user=user)

        cart_total = 0  # Initialize total

        # Add calculated prices to each cart item
        for item in cart_items:
            # Determine the price for the product (off_price if available, else regular price)
            display_price = item.product.off_price if item.product.off_price else item.product.price
            item.display_price = display_price

            # Calculate total price for the item (quantity * price)
            item.total_price = item.quantity * item.display_price

            # Add the item total price to the cart total
            cart_total += item.total_price

        # Pass the cart items and cart total to the template
        return render(req, 'user/cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
    else:
        return redirect('login')




# -------------add---------------

def add_to_cart(request, pid):
    if 'user' in request.session:
        user = User.objects.get(username=request.session['user'])
        product = get_object_or_404(Product, pk=pid)
        size_id = request.GET.get('size_id', None)

        size = Size.objects.filter(pk=size_id, product=product).first() if size_id else None
        product_price = product.off_price if product.off_price else product.price

        try:
            cart = Cart.objects.get(user=user, product=product, size=size)
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            Cart.objects.create(user=user, product=product, size=size, quantity=1)

        return redirect('view_cart')
    else:
        return redirect('login')
    
# ---------------update-------------


def update_quantity(req, item_id):
    # Check if the user is logged in via session
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        item = get_object_or_404(Cart, pk=item_id, user=user)

        # Handle the action to increase or decrease quantity
        action = req.POST.get('action')
        quantity = int(req.POST.get('quantity'))

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        else:
            return redirect('view_cart')

        # Update the total price based on the new quantity
        item.save()

        return redirect('view_cart')
    else:
        return redirect('login')


# ---------------------remove----------------------


def remove_cart(request, cid):
    if 'user' in request.session:
        user = User.objects.get(username=request.session['user'])
        cart_item = get_object_or_404(Cart, pk=cid, user=user)
        cart_item.delete()
        return redirect('view_cart')
    else:
        return redirect('login')


# -----------------checkout----------------------


def checkout(request):
    if 'user' in request.session:
        user = User.objects.get(username=request.session['user'])
        cart_items = Cart.objects.filter(user=user)
        cart_total = 0  # Initialize total

        # Add calculated prices to each cart item
        for item in cart_items:
            # Determine the price for the product (off_price if available, else regular price)
            display_price = item.product.off_price if item.product.off_price else item.product.price
            item.display_price = display_price

            # Calculate total price for the item (quantity * price)
            item.total_price = item.quantity * item.display_price

            # Add the item total price to the cart total
            cart_total += item.total_price+1

        if not cart_items.exists():
            return redirect('view_cart')

        if request.method == "POST":
            # Handle checkout process
            return render(request, 'user/checkout_success.html')
        

        return render(request, 'user/checkout.html', {'cart': cart_items,'cart_total': cart_total})
    else:
        return redirect('login')