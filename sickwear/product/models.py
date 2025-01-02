# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()
# # Create your models here.

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)

#     def __str__(self):
#         return self.name
    
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
#     image = models.ImageField(upload_to='products/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class ProductVariant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
#     size = models.CharField(max_length=10)  # e.g., XS, S, M, L, XL
#     color = models.CharField(max_length=50)  # e.g., Red, Blue, Green
#     additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     stock = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.product.name} - {self.size}/{self.color}"

# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField()  # e.g., 1 to 5
#     comment = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.rating} - {self.user.username}"
    
# class Wishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}"