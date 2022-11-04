import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import random
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from buyer.models import Blog, User, Donation
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
        #DRY : Don't Repeat Yourself
        return redirect('index')
    else:
        try:
            global user_object
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
    try:
        user_object = User.objects.get(email = request.session['email'])
        if request.method == 'GET':
            
            return render(request, 'profile.html', {'user_object': user_object})
        else:
            
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
    except:
        return render(request, 'login.html')


def add_blog(request):
    try:
        user_object = User.objects.get(email = request.session['email'])
        if request.method == 'POST':
            if request.FILES:
                Blog.objects.create(
                    title = request.POST['title'],
                    content = request.POST['des'],
                    writer = user_object,
                    pic = request.FILES['pic']
                )
            else:
                Blog.objects.create(
                    title = request.POST['title'],
                    content = request.POST['des'],
                    writer = user_object,
                )
            return render(request, 'add_blog.html', {'user_object': user_object})
        else:
            return render(request, 'add_blog.html', {'user_object': user_object})
    except:
        return render(request, 'login.html')


def my_blog(request):
    try:
        user_object = User.objects.get(email = request.session['email'])
        my_blogs = Blog.objects.filter(writer = user_object)
        return render(request, 'my_blog.html', {'blogs': my_blogs, 'user_object': user_object})
    except:
        return render(request, 'login.html')


def view_blog(request):
    blogs = Blog.objects.all()
    user_object = User.objects.get(email= request.session['email'])
    return render(request, 'view_blog.html', {'blogs':blogs, 'user_object': user_object})


def donate(request, pk):
    #PAYMENT
    #donation row create 
    return HttpResponse('Done!!')


def donate_page(request, pk):
    global blog_donate_id
    blog_donate_id = pk
    blog_obj = Blog.objects.get(id = pk)
    return render(request, 'donate.html', {'single_blog': blog_obj})
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def donate_init(request):
    currency = 'INR'
    global amount
    amount = int(request.POST['amount']) * 100  # Rs. 200
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'pay_init.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is not None:
             # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                Donation.objects.create(
                    amount = amount,
                    blog = Blog.objects.get(id = blog_donate_id),
                    user = User.objects.get(email= request.session['email'])
                )
                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
        
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()