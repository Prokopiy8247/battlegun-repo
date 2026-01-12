from django.urls import path
from . import views

urlpatterns = [
    path('start/<uuid:order_id>/', views.payment_start, name='payment_start'),
    path('create/<uuid:order_id>/', views.create_payment, name='payment_create'),
    path('webhook/', views.webhook, name='payment_webhook'),
]
