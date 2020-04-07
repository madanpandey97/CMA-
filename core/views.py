from django.contrib import messages
from payu.gateway import payu_url, get_hash
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from uuid import uuid4
from paytm import checksum
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse

# Payu Url
payu_r= payu_url()
payu_url = ''
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"


class CheckOutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context ={
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(form.data)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                pincode = form.cleaned_data.get('pincode')
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    pincode=pincode
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                print("The form is valid")
                print(order.get_total())
                print(order.id)
                order = Order.objects.get(user=self.request.user, ordered=False)
                #Request paytm to transfer the amount to your bank


                paytmParams = {

                    # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                    "MID": "WorldP64425807474247",

                    # Find your WEBSITE in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                    "WEBSITE": "EStore",

                    # Find your INDUSTRY_TYPE_ID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                    "INDUSTRY_TYPE_ID": "Retail",

                    # WEB for website and WAP for Mobile-websites or App
                    "CHANNEL_ID": "WEB",

                    # Enter your unique order id
                    "ORDER_ID": "989898",

                    # unique id that belongs to your customer
                    "CUST_ID": str('EOrder00'+str(order.id)),

                    # customer's mobile number
                    "MOBILE_NO": "8873220555",

                    # customer's email
                    "EMAIL": str(self.request.user.email),

                    # Amount in INR that is payble by customer
                    # this should be numeric with optionally having two decimal points
                    "TXN_AMOUNT": str(order.get_total()),

                    # on completion of transaction, we will send you the response on this URL
                    "CALLBACK_URL": "http://127.0.0.1:8000/handle_payment/",
                    }


                print(paytmParams)
                paytmParams["CHECKSUMHASH"] = checksum.generate_checksum(paytmParams, MERCHANT_KEY)

                return render(self.request, 'paytm.html', {'parm_dict': paytmParams })

            # messages.warning(self.request, "Checkout Failed.")
            # return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any active order.")
            return redirect('core:order-summary')


class PaymentView(View):

    def get(self, *args, **kwargs):

        return render(self.request, 'payment.html')


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            #messages.success(self.request, "Your Order summery is loaded.")
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any active order.")
            return redirect('/')


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug= slug )
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user= request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()

            messages.info(request, "This item is already in your cart,  Qunatity is  updated")
            return redirect("core:order-summary")

        else:
            messages.info(request,"This item is added to your cart")
            order.items.add(order_item )
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")

        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug= slug )
    order_qs = Order.objects.filter(
        user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                            item=item,
                            user= request.user,
                            ordered=False)[0]
            print(order_item)

            order.items.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your cart")
            return redirect("core:product", slug=slug)

        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")

        return redirect("core:product", slug=slug)


@login_required
def remove_single_product_from_cart (request, slug):
    item = get_object_or_404(Item, slug= slug )
    order_qs = Order.objects.filter(
        user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                            item=item,
                            user= request.user,
                            ordered=False)[0]
            if order_item.quantity==1:
                order_item.quantity -= 1
                order.items.remove(order_item)
                messages.warning(request, "The item is removed from your cart")
                return redirect("core:order-summary")

            order_item.quantity -= 1
            order_item.save()
            messages.warning(request, "The item quantity is updated")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")

        return redirect("core:product", slug=slug)
        #add a message saying the user does not have an order


@csrf_exempt
def handle_request(request):
    return HttpResponse('done')
