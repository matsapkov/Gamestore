# Create your views here.

from django.shortcuts import render
from products.models import Product, ProductCategory


def index(request):
    context = {'title': 'Gamestore'}

    return render(request,"products/index.html", context)


def products(request):
    context = {
        'title': 'Gamestore - Products',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
               }

    return render(request, "products/products.html", context)
