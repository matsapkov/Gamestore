# Create your views here.

from django.shortcuts import render


def index(request):
    context = {'title': 'Gamestore'}

    return render(request,"products/index.html", context)


def products(request):
    context = {'title': 'Gamestore - Products'}

    return render(request, "products/products.html", context)
