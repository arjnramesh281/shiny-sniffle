from django.urls import path
from . import views


urlpatterns=[
    
    # login 
    path('',views.log),
    
    # admin page
    path('admin_home',views.admin_home),
    path('pro_list',views.pro_list),

    # add brand.
    path('add_brand',views.add_brand),
    path('delete_brand/<int:id>/', views.delete_brand, name='delete_brand'),


    # add category
    path('add_category',views.add_category),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

    # add product
    path('add_pro', views.add_pro, name='add_pro'),
    path('add_stock', views.add_size_stock, name='add_stock'),

    # edit product
    path('edit_pro/<id>',views.edit_pro),

    # delete product
       path('delete_pro/<int:id>/', views.delete_pro, name='delete_pro'),

    # add carousel
    path('carousel_edit',views.carousel),

    # logout
    path('logout',views.admin_logout),
    

# ------------------ user side --------------------


    # user registration
    path('registration',views.reg),

    # user home
    path('userhome',views.user_home),
    
    # about page
    path('about',views.about),

    # contact page
    path('contact/', views.contact_view, name='contact'),

    # view product 
    path("view_product/<id>",views.view_product),
    
    path('allpro',views.allpro),

    path('menpro',views.men_pro),

    path('women',views.women_pro),
    path('new_arrivals',views.arrival),

# ------------------cart-------------

    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_cart/<int:cid>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),

]