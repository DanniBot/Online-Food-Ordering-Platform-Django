from multiprocessing import context
from django.shortcuts import render,redirect
from .utils import detectUser

from vendor.forms import vendorForm
from .forms import userForm
from .models import User, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

# Restrict vendors from accessing customer pages
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

# Restrict customers from accessing vendor pages
def check_role_cust(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

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
            vendor.user_profile=UserProfile.objects.get(user=user)
            vendor.save()
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
    return render(request,'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')



