from django.shortcuts import render, get_object_or_404
from user.models import Category, Product

# Create your views here.
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.all()
    return render(request, 'product/category.html', {'products': products, 'category': category})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    suggested_products = Product.objects.exclude(slug=slug)[:4]
    return render(request, 'product/product_detail.html', {
        'product': product,
        'suggested_products': suggested_products
    })
