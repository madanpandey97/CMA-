from django.shortcuts import render
from django.http import HttpResponse
from home.models import Product

def home(request):
    product_list = Product.objects.filter(category='YG')
    context ={
        'product_list': product_list
    }
    return render(request, 'home/home.html', context)
    