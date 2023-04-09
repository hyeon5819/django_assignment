from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('inbound_create/', views.inbound_create, name='inbound_create'),
    path('outbound_create/', views.outbound_create, name='outbound_create'),
    path('product_create/', views.product_create, name='product_create'),
    path('inventory/', views.inventory, name='inventory'),
    path('product_list/', views.product_list, name='product_list'),
    path('error/', views.error, name='error'),
]