import json
from http import HTTPStatus
from urllib import response
from django.http import HttpResponseRedirect, HttpResponse
import uuid
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from yookassa import Configuration, Payment
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from orders.forms import OrderForm
from common.views import TitleMixin
from orders.models import Order
from products.models import Basket

# Create your views here.

Configuration.account_id = '489714'
Configuration.secret_key = 'test_LQid0l33iT21Inu3FVUhk-BwUKLZkxBWdRboEO3j35w'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Gamestore - Orders'
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(OrderListView,self).get_queryset()
        return queryset.filter(initiator = self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Gamestore - Order #{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Gamestore - Order Create'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)

        baskets = Basket.objects.filter(user=self.request.user)

        total_sum = sum(basket.quantity * basket.product.price for basket in baskets)
        description = ", ".join([f"{basket.product.name} (x{basket.quantity})" for basket in baskets])

        payment = Payment.create({
            'amount': {
                'value': f'{total_sum:.2f}',
                'currency': 'RUB',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:submit_order'))
            },
            'metadata':{
                'order_id': self.object.id
            },
            'capture': True,
            'description': f' Заказ: {description}'
        }, uuid.uuid4())

        if payment.status == 'pending' and payment.confirmation.confirmation_url:
            return redirect(payment.confirmation.confirmation_url)

        return response

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def yookassa_webhook_view(request):
    payload = request.body.decode('utf-8')
    payload_dict = json.loads(payload)
    metadata = payload_dict['object']['metadata']
    """names = metadata['name'].split(';;;')
    names.remove('')
    quantities = metadata['quantity'].split(';;;')
    quantities.remove('')
    prices = metadata['price'].split(';;;')
    prices.remove('')"""
    print(f'metadata -- {metadata}')
    order_id = int(metadata['order_id'])
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
    return HttpResponse(status=200)


class SubmitOrderView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Submit Order'


