from django.shortcuts import render,redirect
from .utils import detectUser,send_email,check_role_cust,check_role_vendor
from django.utils.http import urlsafe_base64_decode
from vendor.forms import vendorForm
from .forms import userForm
from .models import User, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
from orders.models import Order
import datetime


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'Please logout before registering a new account.')
        return redirect('myAccount')
    if request.method=='POST':
        form=userForm(request.POST)
        if form.is_valid():
            #create the user using the form
            # user=form.save(commit=False)
            # user.set_password(form.cleaned_data['password']) ###hash password
            # user.role=User.CUSTOMER
            # user.save()
            # form.save()

            #reate the user using create_user method
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()

            #SEND VERIFICATION EMAIL
            send_email(request,user)
            messages.success(request,'Hi '+str(username)+', your account is successfully created!')
            # messages.error(request,'Hi '+str(username)+', your account is successfully created!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = userForm()
    context={
        'form':form,
    }
    return render(request, 'accounts/registerUser.html',context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'Please logout before registering a new account.')
        return redirect('myAccount')
    if request.method=='POST':
        # store the data and create the user
        form=userForm(request.POST)
        v_form=vendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            vendor.vendor_slug=slugify(v_form.cleaned_data['vendor_name'])+'-'+str(user.id)
            vendor.user_profile=UserProfile.objects.get(user=user)
            vendor.save()

            send_email(request,user)

            messages.success(request,'Hi '+str(username)+', you are registered successfully. Please wait for the approval.')
            return redirect(registerVendor)
        else:
            print('invalid form')
            print(form.errors)
    else:
        form=userForm()
        v_form=vendorForm()

    context={
        'form':form,
        'v_form':v_form
    }
    return render(request, 'accounts/registerVendor.html',context=context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in.')
        return redirect('myAccount')
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'Hi, you are logged in!')
            return redirect('myAccount')

        else:
            messages.error(request,'Wrong email or password. Please check.')
            return redirect('login')
    return render(request,'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out.')
    return redirect('home')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_cust)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': reversed(recent_orders),
    }
    return render(request,'accounts/custDashboard.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor=Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    recent_orders = orders[:10]


    # current month's revenue
    current_month = datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']
    

    # total revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']

    context={
        'orders': orders,
        'orders_count': orders.count(),
        # 'recent_orders': reversed(recent_orders),
        'recent_orders': reversed(recent_orders),
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request,'accounts/vendorDashboard.html',context=context)


def activate(request,uidb64,token):
    # activate the user by setting the is_active to True
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! Your Email is verified!')
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('myAccount')

def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)

            #send reset password email
            mail_subject='Reset your password'
            email_temp='accounts/emails/reset_password_email.html'
            send_email(request,user,mail_subject,email_temp)
            messages.success(request,'Password reset link has been sent to your Email address.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist. Please double-check the Email address.')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    #validate the user by decoding the token and user pk
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'Please reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired!')
        return redirect('myAcount')

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Password is reset successfully!')
            return redirect('login')
        else:
            messages.error(request,'Passwords do not match.')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')



