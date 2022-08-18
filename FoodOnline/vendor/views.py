from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from menu.models import foodItem
from menu.models import Category
from accounts.models import UserProfile
from .models import Vendor
from .forms import vendorForm
from accounts.forms import userProfileForm
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.utils import check_role_vendor
from menu.forms import CategoryForm,foodAddForm,foodEditForm
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor


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

@login_required(login_url='login')
def menu_builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor).order_by('created_at')
    context={
        'categories':categories,

    }
    return render(request,'vendor/menu_builder.html',context=context)

@login_required(login_url='login')
def fooditems_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=foodItem.objects.filter(vendor=vendor,category=category)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'vendor/fooditems_by_category.html',context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_cat(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            # category.slug=slugify(form.cleaned_data['category_name'])
            category.save() ##get cat's id
            category.slug=slugify(category.category_name)+'-'+str(category.id)
            category.save() 
            messages.success(request,'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form=CategoryForm()
    context={
        'form':form
    }
    return render(request,'vendor/add_cat.html',context=context)


@login_required(login_url='login')
def edit_cat(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(form.cleaned_data['category_name'])
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category
    }
    return render(request,'vendor/edit_cat.html',context)

@login_required(login_url='login')
def del_cat(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category removed successfully!')
    return redirect('menu_builder')


@login_required(login_url='login')
def add_food(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=foodAddForm(request.POST,request.FILES)
        if form.is_valid():
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(form.cleaned_data['food_name'])
            food.category=category
            form.save()
            messages.success(request,'Food added successfully!')
            return redirect('fooditems_by_category',pk)
        else:
            print(form.errors)
    else:
        form=foodAddForm()
        
    context={
        'form':form,
        'category':category
    }

    return render(request,'vendor/add_food.html',context=context)


@login_required(login_url='login')
def del_food(request,pk=None):
    food=get_object_or_404(foodItem,pk=pk)
    cat=food.category
    food.delete()
    messages.success(request,'Food removed successfully!')
    return redirect('fooditems_by_category',cat.id)


@login_required(login_url='login')
def edit_food(request,pk=None):
    food=get_object_or_404(foodItem,pk=pk)
    cat=food.category
    if request.method=='POST':
        form=foodEditForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(form.cleaned_data['food_name'])
            form.save()
            messages.success(request,'Food updated successfully!')
            return redirect('fooditems_by_category',cat.id)
        else:
            print(form.errors)
    else:
        form=foodEditForm(instance=food)
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form,
        'food':food
    }
    return render(request,'vendor/edit_food.html',context)