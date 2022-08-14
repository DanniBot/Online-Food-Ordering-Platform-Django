from pyexpat.errors import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from accounts.models import UserProfile
from .models import Vendor
from .forms import vendorForm
from accounts.forms import userProfileForm
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.utils import check_role_vendor


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)

    if request.method=='POST':
        profile_form=userProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=vendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated.')
            return redirect('v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=userProfileForm(instance=profile)
        vendor_form=vendorForm(instance=vendor)

    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/v_profile.html',context=context)