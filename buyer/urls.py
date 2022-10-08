from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp/', views.otp, name='otp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_profile/', views.change_profile, name='change_profile'),
    path('', views.index, name='index'),
   
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]