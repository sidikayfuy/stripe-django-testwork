from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:pk>', views.buy, name='buy'),
    path('item/<int:pk>', views.item, name='item'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('makeorder/', views.makeorder, name='makeorder'),
    path('buyorder/', views.buyorder, name='buyorder'),
    path('checkcoupon/', views.checkcoupon, name='checkcoupon'),
]