from django.urls import path
from . import views


urlpatterns=[
    
    # login 
    path('',views.log),
    
    # admin page
    path('admin_home',views.admin_home),
    path('pro_list',views.pro_list),

    # add category
    path('add_category',views.add_category),

    # add product
    path('add_pro',views.add_pro),

    # add carousel
    path('carousel_edit',views.carousel),

    # logout
    path('logout',views.admin_logout),
    

    # user registration
    path('registration',views.reg),

    # user home
    path('userhome',views.user_home),
    
    path('about',views.about),

]