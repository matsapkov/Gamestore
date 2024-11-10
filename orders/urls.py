from django.urls import path, include
from . import views
from products.views import IndexView, ProductListView
from orders.views import OrderCreateView, SubmitOrderView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('success/', SubmitOrderView.as_view(), name='submit_order'),
    path('', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
]
