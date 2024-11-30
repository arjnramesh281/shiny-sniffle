from django.urls import path
from . import views


urlpatterns=[
    
    # login 
    path('',views.log),
    # admin page
    path('admin_home',views.admin_home),
    # logout
    path('logout',views.admin_logout),

    # user registration
    path('registration',views.reg),

    # user home
    path('userhome',views.user_home),

]