from django.shortcuts import render
from user.models import Category

# Create your views here.

def index(request):
    """
    Render the homepage.
    """
    categories = Category.objects.all()
    categories_chunked = list(chunk_queryset(categories, 3))
    return render(request, 'homepage/index.html', {'categories_chunked': categories_chunked, 'total_categories': categories.count()})

def chunk_queryset(queryset, chunk_size):
    """Split a queryset into chunks of specified size."""
    for i in range(0, len(queryset), chunk_size):
        yield queryset[i:i + chunk_size]
