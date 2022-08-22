from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from accounts.forms import userProfileForm,userInfoForm
from django.contrib import messages
from orders.models import Order,OrderedFood

# Create your views here.
@login_required(login_url='login')
def c_profile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        profile_form=userProfileForm(request.POST,request.FILES,instance=profile)
        user_form=userInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile is updated.')
            return redirect('c_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:

        profile_form=userProfileForm(instance=profile)
        user_form=userInfoForm(instance=request.user)

    

    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request,'customer/c_profile.html',context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'customer/my_orders.html', context)


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        tax=order.tax
        total=order.total
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax': tax,
            'total':total,
        }
        return render(request, 'customer/order_detail.html', context)
    except:
        return redirect('customer')