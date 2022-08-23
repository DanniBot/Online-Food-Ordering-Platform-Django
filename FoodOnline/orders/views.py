from multiprocessing import context
from django.shortcuts import render, redirect
from menu.models import foodItem
from marketplace.models import Cart
from marketplace.context_processor import get_cart_amount
from .forms import OrderForm
from .models import Order,Payment,OrderedFood
from strgen import StringGenerator as SG
from .utils import generate_order_number
from django.http import HttpResponse, JsonResponse
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
import simplejson as json

# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('marketplace')

    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)

    total_data = {}
    k = {}

    for i in cart_items:
        fooditem = foodItem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price * i.quantity)
            k[v_id] = subtotal

        total_data.update({fooditem.vendor.id: str(subtotal)})




    subtotal=get_cart_amount(request)['subtotal']
    tax=get_cart_amount(request)['tax']
    total=get_cart_amount(request)['total']

    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order=Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = total
            # order.total_data = json.dumps(total_data)
            order.tax = tax
            order.total_data = json.dumps(total_data)
            order.payment_method = request.POST['payment_method']
            order.save() # order id/ pk is generated
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            # order.vendors.add(*vendors_ids)
            context={
                'order':order,
                'cart_items':cart_items,
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    # check is the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
       
        order_number = request.POST.get('order_number')
        # transaction_id = request.POST.get('transaction_id')
        transaction_id = SG(r"[\w]{30}").render()
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        # store the payment details in the payment model
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        # update the order model
        order.payment = payment
        order.is_ordered = True
        order.save()

        # move the cart items to ordered food model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity # total amount
            ordered_food.save()

        # send confirmation email to the customer
        mail_subject="Here's your foodOnline order confirmation" + order_number
        mail_template='orders/confirmation.html'
        context={
            'user':request.user,
            'order':order,
            'to_email':order.email,
        }
        send_notification(mail_subject,mail_template,context)

        # send order receive email to the vendor
        mail_subject = 'You have received a new order.'
        mail_template = 'orders/new_order_received.html'
        to_emails = set()
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.add(i.fooditem.vendor.user.email)

                # ordered_food_to_vendor = OrderedFood.objects.filter(order=order, fooditem__vendor=i.fooditem.vendor)

        
                context = {
                    'order': order,
                    'to_email': i.fooditem.vendor.user.email,
                    # 'ordered_food_to_vendor': ordered_food_to_vendor,
                    # 'vendor_subtotal': order_total_by_vendor(order, i.fooditem.vendor.id)['subtotal'],
                    # 'tax_data': order_total_by_vendor(order, i.fooditem.vendor.id)['tax_dict'],
                    # 'vendor_grand_total': order_total_by_vendor(order, i.fooditem.vendor.id)['grand_total'],
                }
                send_notification(mail_subject, mail_template, context)


        # clear the cart if the payment is completed
        # cart_items.delete()



        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
            'to_email':order.email
        }
        return JsonResponse(response)



@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
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
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')
    

    

    

    

    

    