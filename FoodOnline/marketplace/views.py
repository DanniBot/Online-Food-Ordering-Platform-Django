from multiprocessing import context
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart
from menu.models import Category,foodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from .context_processor import get_cart_counter, get_cart_amount
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    count=vendors.count()
    context={
        'vendors':vendors,
        'v_count':count,
    }
    return render(request,'marketplace/listings.html',context=context)



def vendor_detail(request,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=foodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None

    context={
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }

    return render(request,'marketplace/vendor_detail.html',context=context)

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            #check if the food item exists
            try:
                fooditem=foodItem.objects.get(id=food_id)
                #check if the food is in the cart
                try:
                    checkcart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    if checkcart.quantity>1:
                        #decrease the quantity
                        checkcart.quantity-=1
                        checkcart.save()
                    else:
                        checkcart.delete()
                        checkcart.quantity=0
                    return JsonResponse({'status':'Success','message':'Quantity decreases.','cart_counter':get_cart_counter(request),'qty':checkcart.quantity,'cart_amount':get_cart_amount(request)})
                except:
                    return JsonResponse({'status':'Fail','message':'You do not have this item in your cart.'})
            except:
                return JsonResponse({'status':'Fail','message':'This food does not exist.'})
        else:
            return JsonResponse({'status':'Fail','message':'Invalid request.'})
        

    return JsonResponse({'status':'login_required','message':'Please log in first.'})


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            #check if the food item exists
            try:
                fooditem=foodItem.objects.get(id=food_id)
                #check if the food is in the cart
                try:
                    checkcart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    #increment the quantity
                    checkcart.quantity+=1
                    checkcart.save()
                    return JsonResponse({'status':'Success','message':'Quantity increases.','cart_counter':get_cart_counter(request),'qty':checkcart.quantity,'cart_amount':get_cart_amount(request)})
                except:
                    #add the food
                    checkcart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the food into the cart.','cart_counter':get_cart_counter(request),'qty':checkcart.quantity,'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status':'Fail','message':'This food does not exist.'})
        else:
            return JsonResponse({'status':'Fail','message':'Invalid request.'})
        
    
    return JsonResponse({'status':'login_required','message':'Please log in first.'})
    
@login_required(login_url='login')
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    context={
        'cart_items' :cart_items,
    }
    return render(request,'marketplace/cart.html',context)

def del_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                #check if the cart item exists
                cart_item=Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item has been deleted.','cart_counter':get_cart_counter(request),'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status':'Fail','message':'Cart item does not exist.'})

        else:
            return JsonResponse({'status':'Fail','message':'Invalid request.'})


                
