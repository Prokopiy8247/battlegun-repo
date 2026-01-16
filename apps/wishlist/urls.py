
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_list, name='wishlist_list'),
    path('toggle/<uuid:product_id>/', views.toggle_wishlist, name='wishlist_toggle'),
    path('remove/<uuid:product_id>/', views.remove_wishlist_item, name='wishlist_remove'),
]
