from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import stripe

stripe.api_key = 'sk_test_51LjOPrK8VEc3Qx7nqZUSI1Ya2uyWdFlpQ52sQn5EIaoyGmjj1b9A2l21I8KDi1k9zFueQqTe9FQbXUz2roxIflCL007Fv5NQnC'


def index(request):
    return render(request, 'stripeapp/index.html', {'items': Item.objects.all()})


def buy(request, pk):
    item = Item.objects.get(pk=pk)
    count = request.GET.get('count')

    taxes = stripe.TaxRate.list(limit=3)
    tax = ''
    for i in taxes['data']:
        if i['country'] == 'RU':
            tax = i['id']

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': item.price,
            },
            'quantity': count,
            'tax_rates': [tax]
        },
        ],
        mode='payment',
        success_url='http://localhost:8000/success.html',
        cancel_url='http://localhost:8000/cancel.html',
    )
    return HttpResponse(session.id, status=200)


def item(request, pk):
    current_item = Item.objects.get(pk=pk)
    return render(request, 'stripeapp/item.html', {'item': current_item})


def success(request):
    return render(request, 'stripeapp/success.html', {})

def cancel(request):
    return render(request, 'stripeapp/index.html', {'items': Item.objects.all()})

def makeorder(request):
    return render(request, 'stripeapp/makeorder.html', {'items': Item.objects.all()})

def buyorder(request):
    items = request.GET.getlist('datas[]')

    taxes = stripe.TaxRate.list(limit=3)
    tax = ''
    for i in taxes['data']:
        if i['country']=='RU':
            tax = i['id']


    if len(request.GET.get('coupon'))>0 :
        promocode = Promocode.objects.get(code=request.GET.get('coupon'))
        session = stripe.checkout.Session.create(
            line_items=[{'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': Item.objects.get(pk=i.split(' ')[0]).name,
                },
                'unit_amount': Item.objects.get(pk=i.split(' ')[0]).price,
            },
                'quantity': int(i.split(' ')[1]), 'tax_rates': [tax]} for i in items],
            mode='payment',
            discounts=[{
                'coupon': promocode.coupon.id,
            }],
            success_url='http://localhost:8000/success.html',
            cancel_url='http://localhost:8000/cancel.html',
        )
    else:
        session = stripe.checkout.Session.create(
            line_items=[{'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': Item.objects.get(pk=i.split(' ')[0]).name,
                },
                'unit_amount': Item.objects.get(pk=i.split(' ')[0]).price,
            },
                'quantity': int(i.split(' ')[1]), 'tax_rates': [tax]} for i in items],
            mode='payment',
            discounts=[],
            success_url='http://localhost:8000/success.html',
            cancel_url='http://localhost:8000/cancel.html',
        )
    return HttpResponse(session.id, status=200)


def checkcoupon(request):
    coupon = request.GET.get('coupon')
    try:
        Promocode.objects.get(code=coupon)
        return HttpResponse(1, status=200)
    except:
        return HttpResponse(0, status=200)
