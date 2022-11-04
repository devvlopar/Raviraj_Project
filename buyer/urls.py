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
    path('add_blog/', views.add_blog, name='add_blog'),
    path('my_blog/', views.my_blog, name='my_blog'),
    path('view_blog/', views.view_blog, name='view_blog'),
    path('donate/<int:pk>', views.donate, name='donate'),
    path('donate_init/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('donate_page/<int:pk>', views.donate_page, name="donate_page"),
    path('donate_init/', views.donate_init, name="donate_init"),



]