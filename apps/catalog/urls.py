from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<uuid:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_modal, name='cart_modal'),
    path('cart/add/<uuid:pk>/', views.cart_add, name='cart_add'),
]
