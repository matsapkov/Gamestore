from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from products.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator


def index(request):
    context = {'title': 'Gamestore'}

    return render(request,"products/index.html", context)


def products(request, category_id=None, page_number=1):
    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products_ = Product.objects.filter(category=category)
    else:
        products_ = Product.objects.all()

    per_page = 4
    paginator = Paginator(products_, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Gamestore - Products',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
    }

    return render(request, "products/products.html", context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

 # -------------------------api---------------------------


@require_POST
@csrf_exempt
def basket_update(request, basket_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))

        # Находим элемент корзины и обновляем его количество
        basket = Basket.objects.get(id=basket_id)
        basket.quantity = quantity
        basket.save()

        # Пересчитываем стоимость товара и общую стоимость корзины
        item_total = basket.product.price * basket.quantity
        cart_total = sum(item.product.price * item.quantity for item in Basket.objects.filter(user=request.user))

        return JsonResponse({
            'item_total': item_total,
            'cart_total': cart_total
        })
    except Basket.DoesNotExist:
        return JsonResponse({'error': 'Basket item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
