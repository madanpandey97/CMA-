from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            messages.success(self.request, "Your Order summery is loaded.")
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
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()

            messages.info(request, "This item is already in your cart,  Qunatity is  updated")
            return redirect("core:product", slug = slug)

        else:
            messages.info(request,"This item is added to your cart")
            order.items.add(order_item )
            return redirect("core:product", slug = slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")

        return redirect("core:product", slug = slug)

# def add_to_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     # print(item.title,item.price,item.slug)
#     order_item, created = OrderItem.objects.get_or_create(
#         item=item, user=request.user, ordered=False)
#     # print(order_item)==admin
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     # print(order_qs) ==return queryset[]
#     # if there is a order
#     if order_qs.exists():
#         order = order_qs[0]
#         #print(order)  == admin
#         #print(item.slug) == denim-pant
#
#         # check if the order item is in the order ==(order ache,for same-orderitem
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("order-summary")
#         else:
#             # ==(order ache, different-orderitem ache)
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("order-summary")

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
            messages.warning(request, "This item was removed from your cart")
            return redirect("core:product", slug=slug)

        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")

        return redirect("core:product", slug=slug)
        #add a message saying the user does not have an order



