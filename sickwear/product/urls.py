from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category, name='category'),
    path('product-detail/<slug:slug>/', views.product_detail, name='product_detail')
]
