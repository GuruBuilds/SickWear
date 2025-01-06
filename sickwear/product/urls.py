from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category, name='category'),
    path('product-detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('view-cart', views.view_cart, name='view_cart'),
]
