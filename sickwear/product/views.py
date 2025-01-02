from django.shortcuts import render
from user.models import Category

# Create your views here.
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.all()
    return render(request, 'product/category.html', {'products': products, 'category': category})