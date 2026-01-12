from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.webhook, name='payment_webhook'),
    path('waiting/<str:order_number>/', views.payment_waiting, name='payment_waiting'),
    path('success/<str:order_number>/', views.payment_success, name='payment_success'),
    path('failed/<str:order_number>/', views.payment_failed, name='payment_failed'),
]
