from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:slug>/', views.category, name='category'),
    path('product-detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('view-cart', views.view_cart, name='view_cart'),
    path('wish-list', views.wish_list, name='wish_list'),
    # path('add-to-wishlist', views.add_to_wishlist, name='add_to_wishlist'),
    # path('remove-from-cart', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_item_quantity, name='update_cart_item'),
    path('cart/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('add-or-edit-address', views.add_or_edit_address, name='add_or_edit_address'),
]
