# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    is_customer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

    def items_count(self):
        cart = self.cart.first()
        if cart:
            return cart.items.count()
        return 0

    def cart_subtotal(self):
        cart = self.cart.first()  # Get the first cart for the user
        if cart:
            subtotal = sum(
                (item.product_variant.product.price + item.product_variant.additional_price) * item.quantity 
                for item in cart.items.all())
            return subtotal
        return 0.0  # Return 0 if no cart exists

    def wishlist_subtotal(self):
        wishlist_items = self.wishlist.all()  # Get all wishlist items for the user
        subtotal = sum(item.product.price for item in wishlist_items)
        return subtotal


class Address(models.Model):
    """Model to store user addresses."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.street_address}, {self.city}, {self.pincode}")


class Category(models.Model):
    """Model to store product categories."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """Model to store product information."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class ProductVariant(models.Model):
    """Model to store product variants with different sizes and colors."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=10)  # e.g., XS, S, M, L, XL
    color = models.CharField(max_length=50)  # e.g., Red, Blue, Green
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return str(f"{self.product.name} - {self.size}/{self.color}")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE, blank=True, null=True)
    variant = models.ForeignKey(ProductVariant, related_name='variant_images', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/')  # Image for the product or variant
    is_main = models.BooleanField(default=False)  # To mark the main image

    def __str__(self):
        if self.product:
            return f"Image for {self.product.name}"
        if self.variant:
            return f"Image for {self.variant.product.name} - {self.variant.size}/{self.variant.color}"
        return "Unnamed image"

    class Meta:
        # You can choose to add ordering logic to ensure the main image is always the first one for the product/variant
        ordering = ['-is_main']


class Cart(models.Model):
    """Model to store user shopping carts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """Model to store items in a shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(f"{self.quantity} x {self.product_variant}")


class Order(models.Model):
    """Model to store user orders."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    """Model to store items in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(f"{self.quantity} x {self.product_variant}")


class Review(models.Model):
    """Model to store product reviews."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.rating} - {str(self.user)}")


class Wishlist(models.Model):
    """Model to store user wishlists."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{str(self.user)} - {self.product.name}")
