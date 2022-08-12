from multiprocessing import context
from django.shortcuts import render,redirect

from vendor.forms import vendorForm
from .forms import userForm
from .models import User, UserProfile
from django.contrib import messages

# Create your views here.
def registerUser(request):
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
