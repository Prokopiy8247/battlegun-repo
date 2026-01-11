from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<uuid:product_id>/', views.add_to_cart, name='cart_add'),
    path('update/<uuid:item_id>/', views.update_cart_item, name='cart_update'),
    path('remove/<uuid:item_id>/', views.remove_from_cart, name='cart_remove'),
    path('count/', views.cart_count, name='cart_count'),
]
