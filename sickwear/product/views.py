from django.shortcuts import render
from user.models import Category, Product

# Create your views here.
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.all()
    return render(request, 'product/category.html', {'products': products, 'category': category})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'product/product_detail.html', {'product': product})
