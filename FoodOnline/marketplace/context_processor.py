from .models import Cart, Tax
from menu.models import foodItem

def get_cart_counter(request):
    cart_count=0
    if request.user.is_authenticated:
        try:
            cart_items=Cart.objects.filter(user=request.user)
            if cart_items:
                for item in cart_items:
                    cart_count+=item.quantity
            else:
                cart_count=0
        except:
            cart_count=0
    return dict(cart_count=cart_count)

def get_cart_amount(request):
    subtotal=0
    tax=0
    total=0
    if request.user.is_authenticated:
        cart_item=Cart.objects.filter(user=request.user)
        for item in cart_item:
            fooditem=foodItem.objects.get(pk=item.fooditem.id)
            subtotal+=(fooditem.price*item.quantity)

        get_tax=Tax.objects.filter(is_active=True)
        for i in get_tax:
            tax_percentage=i.tax_percentage
            tax+=round((tax_percentage*subtotal)/100,2)
        total=subtotal+tax
    return dict(subtotal=subtotal,tax=tax,total=total)