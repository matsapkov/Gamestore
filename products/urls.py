from django.urls import path

from products.views import products, piski

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
]

