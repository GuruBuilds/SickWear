from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from user.models import Category, Product, ProductVariant, Cart, CartItem, Wishlist
from django.contrib import messages

# Create your views here.
def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.all()
    return render(request, 'product/category.html', {'products': products, 'category': category})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_varients = ProductVariant.objects.filter(product=product)
    suggested_products = Product.objects.exclude(slug=slug)[:4]
    return render(request, 'product/product_detail.html', {
        'product': product,
        'product_varients': product_varients,
        'suggested_products': suggested_products
    })


def add_to_cart(request):
    if request.method == 'POST':
        product_detail = request.POST.get('product_id')
        varient_id = request.POST.get('selected_varient')
        quantity = int(request.POST.get('quantity', 1))  # Default quantity to 1
        user = request.user

        # Validate inputs
        if not product_detail or not varient_id:
            return JsonResponse({'error': 'Invalid product or variant selection'}, status=400)

        try:
            # Fetch or create the user's cart
            cart, _ = Cart.objects.get_or_create(user=user)

            # Add the item to the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_variant_id=varient_id,
                defaults={'quantity': quantity}
            )
            if not created:
                # Update quantity if the item already exists
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, 'You have successfully added the item to the cart.')
            product = Product.objects.get(id=product_detail)
            return render(request, 'product/product_detail.html', {
                'product': product,
                'product_varients': ProductVariant.objects.filter(product=product),
                'suggested_products': Product.objects.exclude(slug=product.slug)[:4]
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    # add the total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product_variant.product.price * item.quantity
        item.total_price += item.product_variant.additional_price * item.quantity

    # Calculate the total cost of the cart
    cart_total = sum(item.product_variant.product.price * item.quantity for item in cart_items)
    return render(request, 'product/view_cart.html', {'cart_items': cart_items, 'cart_total': cart_total})



def wish_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    total_price = sum(item.product.price for item in wishlist_items)
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items, 'total_price': total_price})
