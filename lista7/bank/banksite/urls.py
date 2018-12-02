from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='banksite-home'),
    path('payments/', views.payments, name='banksite-payments'),
    path('payment/',views.payment, name='banksite-payment'),
    path('awaiting/', views.awaiting_payments, name='banksite-awaiting'),
    path('confirm/',views.payment_confirm, name='banksite-payment-confirm'),
    path('summary/',views.payment_summary, name='banksite-payment-summary'),
    path('find_payment/',views.find_payment, name='banksite-find_payment'),
]
