from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category, name='category'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
]