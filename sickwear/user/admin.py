from django.contrib import admin
from user.models import User, Category, Product, ProductVariant, Cart, CartItem, Order, Wishlist

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Wishlist)
