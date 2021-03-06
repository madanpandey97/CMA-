from django.urls import path
from .views import (HomeView ,
                    ItemDetailView,
                     add_to_cart,
                     remove_from_cart,
                    OrderSummaryView,
                    remove_single_product_from_cart,
                    CheckOutView, PaymentView, handle_request)
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('product/<slug>',ItemDetailView.as_view(), name = 'product' ),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-single-product-from-cart/<slug>/',
         remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('handle_payment/', handle_request, name='payment_handler')



]