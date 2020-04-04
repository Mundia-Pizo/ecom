from django.shortcuts import render, reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from blogs.models import Payment, Order , BillingAddress, OrderItem
from blogs.blog_forms import CheckoutForm


@csrf_exempt
def payment_done(request):
    order_item=OrderItem()
    order_item.ordered=True
    order =Order.objects.get(user=request.user, ordered=False)
    payment=Payment()
    billing_address=BillingAddress()
    billing_address.user=request.user
    # billing_address.street_address=request.street_address
    # billing_address.apartment_address=request.apartment_address
    # billing_address.country=request.country
    payment.user=request.user
    payment.amount =order.get_total_and_shipping()
    payment.save()
    order_item =order.items.all()
    order_item.update(ordered=True)
    for item in order_item:
        item.save()
    order.payment=payment
    order.ordered=True
    order.save()
    # form = CheckoutForm()
    # form.save()
    return render(request, 'paypal/payment_done.html')

@csrf_exempt
def payment_cancelled(request):
	return render(request, 'paypal/payment_cancelled.html')

@csrf_exempt
def payment_process(request, *args, **kwargs):
    order =Order.objects.get(user=request.user, ordered=False)
    # What you want the button to do.

    paypal_dict = {
        "business": "sb-z7smm532234@business.example.com",
        "amount": order.get_total_and_shipping(),
        "item_name": order.items.all(),
        "invoice": None,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancelled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "order":order}
    return render(request, "paypal/payment.html", context)






    