from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from user.models import Category, Product, ProductVariant, Cart, CartItem, Wishlist, Address
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

    # send user addrss to the template
    user_address = Address.objects.filter(user=request.user).first()

    return render(request, 'product/view_cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user_address': user_address
    })

def update_cart_item_quantity(request):
    """AJAX handler to update the quantity of a cart item."""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

        # Get the CartItem object
        cart_item = get_object_or_404(CartItem, id=item_id)

        # Check if enough stock is available
        if cart_item.product_variant.stock < quantity:
            return JsonResponse({
                'success': False,
                'error': 'Not enough stock available.',
            }, status=400)

        # Update the quantity
        cart_item.quantity = quantity
        cart_item.save()

        # Calculate total price for the item and the cart
        item_total = cart_item.quantity * (cart_item.product_variant.product.price + cart_item.product_variant.additional_price)
        cart_total = sum(
            item.quantity * (item.product_variant.product.price + item.product_variant.additional_price)
            for item in cart_item.cart.items.all()
        )

        return JsonResponse({
            'success': True,
            'item_total': item_total,
            'cart_total': cart_total,
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


def remove_cart_item(request):
    """AJAX handler to remove an item from the cart."""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        # Get the CartItem object
        cart_item = get_object_or_404(CartItem, id=item_id)

        # Remove the item
        cart = cart_item.cart
        cart_item.delete()

        # Recalculate the total price of the cart
        cart_total = sum(
            item.quantity * (item.product_variant.product.price + item.product_variant.additional_price)
            for item in cart.items.all()
        )

        return JsonResponse({
            'success': True,
            'cart_total': cart_total,
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

def add_or_edit_address(request):
    if request.method == 'POST':
        street_address = request.POST['street_address']
        apartment_number = request.POST.get('apartment_number', '')
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        is_default = 'is_default' in request.POST  # Checking if the address is marked as default

        # Create an Address instance for the user
        new_address = Address(
            user=request.user,
            street_address=street_address,
            apartment_number=apartment_number,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            is_default=is_default
        )
        new_address.save()
        messages.success(request, 'Address added successfully.')
        return JsonResponse({'message': 'Address added successfully.'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def wish_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    total_price = sum(item.product.price for item in wishlist_items)
    return render(request, 'product/wish_list.html', {'wishlist_items': wishlist_items, 'total_price': total_price})


def profile(request):
    return render(request, 'product/profile.html')