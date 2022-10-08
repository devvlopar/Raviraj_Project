import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from buyer.models import User
# Create your views here.
def index(request):
    try:
        request.session['email']
        user_object = User.objects.get(email= request.session['email'])
        return render(request, 'index.html', {'user_object': user_object})
    except:
        return render(request, 'login.html')
  

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        global user_data
        user_data = {
            'first_name' : request.POST['fname'],
            'last_name' : request.POST['lname'],
            'email' : request.POST['email'],
            'mobile' : request.POST['mobile'],
            'password' : request.POST['password'],
            're_password' : request.POST['cpassword']  
        }
        if user_data['password'] == user_data['re_password']:
            global c_otp
            c_otp = random.randint(1000, 9999)
            message = f'Hi your OTP is {c_otp}.'
            subject = 'BlogSpot Registration.'
            from_email = settings.EMAIL_HOST_USER

            send_mail(subject, message, from_email,[user_data['email']])
            return render(request, 'otp.html', {'msg':'Check Your MailBox'})
        else:
            return render(request, 'register.html', {'msg':'passwords do not match'})
    

def otp(request):
    if request.method == 'POST':
        if c_otp == int(request.POST['uotp']):
            User.objects.create(
                first_name = user_data['first_name'],
                last_name = user_data['last_name'],
                email = user_data['email'],
                mobile = user_data['mobile'],
                password = user_data['password'],
            )
            return render(request, 'login.html', {'msg':'Account Successfully Created!!'})    
        else:
            return render(request, 'otp.html', {'msg': 'OTP is Wrong!!'})
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            user_object = User.objects.get(email = request.POST['email'])
            if user_object.password == request.POST['password']:
                request.session['email'] = request.POST['email']
                return render(request, 'index.html', {'user_object': user_object})
            else:
                return render(request, 'login.html', {'msg': 'Invalid Password'})
        except:
            return render(request, 'login.html', {'msg':'Email is Not Registered!!'})


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')
    else:
        try:
            user_object = User.objects.get(email = request.POST['email'])
            send_mail('Account Recovery', f'Your password is {user_object.password}.', settings.EMAIL_HOST_USER, [user_object.email])
            return render(request, 'login.html', {'msg':'Check Your MailBox!!'})

        except:
            return render(request, 'forgot_password.html', {'msg':'Email Does not Exists!!'})
        

def logout(request):
    try:
        del request.session['email']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')


def change_profile(request):
    if request.method == 'GET':
        user_object = User.objects.get(email = request.session['email'])
        return render(request, 'profile.html', {'user_object': user_object})
    else:
        user_object = User.objects.get(email = request.session['email'])
        user_object.first_name = request.POST['fname']
        user_object.last_name = request.POST['lname']
        user_object.mobile = request.POST['mobile']
        user_object.address = request.POST['address']
        user_object.bio = request.POST['bio']

        try:
            request.FILES['pic']
            user_object.pic = request.FILES['pic']
        except:
            pass
        user_object.save()
        return render(request, 'profile.html', {'user_object': user_object})