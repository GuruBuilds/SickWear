from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index),
    path('pay/', views.pay, name="pay"),
    path('return-to-me/', views.payment_return, name="return-to-me"),
]
