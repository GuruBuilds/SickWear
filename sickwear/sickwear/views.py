from django.shortcuts import render
from user.models import Category, Product

# Create your views here.

def index(request):
    """
    Render the homepage.
    """
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)
    popular_products = Product.objects.all().order_by('-views')[:10]
    newly_added_products = Product.objects.all().order_by('-created_at')[:10]
    context = {
        'categories': categories,
        'total_categories': categories.count(),
        'featured_products': featured_products,
        'popular_products': popular_products,
        'newly_added_products': newly_added_products,
    }
    return render(request, 'homepage/index.html', context)

# def chunk_queryset(queryset, chunk_size):
#     """Split a queryset into chunks of specified size."""
#     for i in range(0, len(queryset), chunk_size):
#         yield queryset[i:i + chunk_size]
