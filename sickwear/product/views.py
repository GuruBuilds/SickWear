from django.shortcuts import render, get_object_or_404
from user.models import Category, Product

# Create your views here.
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.all()
    return render(request, 'product/category.html', {'products': products, 'category': category})

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    suggested_products = Product.objects.exclude(id=product_id)[:4]  # Fetch 4 other products
    return render(request, 'product/product_details.html', {
        'product': product,
        'suggested_products': suggested_products
    })