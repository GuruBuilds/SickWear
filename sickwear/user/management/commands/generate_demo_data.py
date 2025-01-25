from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint
from user.models import User, Category, Product, ProductVariant, Cart, CartItem, Order, OrderItem, Review, Wishlist, ProductImage, Address
import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Generate demo data for the e-commerce app"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate a single user with username 'admin' and password 'admin'
        user = User.objects.create_user(
            username='admin',
            email=fake.email(),
            password='admin',  # Fixed password
            phone_number="9876543211"
        )
        self.stdout.write(self.style.SUCCESS(f"User {user.username} created."))

        # Add Addresses for this user
        for _ in range(randint(1, 3)):  # 1-3 addresses per user
            Address.objects.create(
                user=user,
                street_address=fake.street_address(),
                apartment_number=fake.building_number(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                pincode=fake.zipcode(),
                is_default=randint(0, 1) == 1  # Randomly set the default address
            )
        self.stdout.write(self.style.SUCCESS(f"Addresses created for user {user.username}."))

        # Generate Categories
        categories = []
        for _ in range(5):  # 5 demo categories
            category = Category.objects.create(
                name=fake.word().capitalize(),
                slug=fake.slug(),
                description=fake.text(),
            )
            # Fetch an image from Lorem Picsum and save it to the backend
            response = requests.get('https://picsum.photos/400/400', stream=True)
            if response.status_code == 200:
                category.image.save(f"{category.name}.jpg", ContentFile(response.content))
            categories.append(category)
        self.stdout.write(self.style.SUCCESS("5 Categories created."))

        # Generate Products
        products = []
        for _ in range(10):  # 10 demo products
            product = Product.objects.create(
                name=fake.word().capitalize(),
                slug=fake.slug(),
                description=fake.text(),
                price=round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2),
                stock=randint(10, 100),
                category=choice(categories),
            )
            # Fetch an image from Lorem Picsum and save it to the backend
            response = requests.get('https://picsum.photos/400/400', stream=True)
            if response.status_code == 200:
                product.image.save(f"{product.name}.jpg", ContentFile(response.content))
            products.append(product)
        self.stdout.write(self.style.SUCCESS("10 Products created."))

        # Generate Product Variants
        variants = []
        sizes = ['XS', 'S', 'M', 'L', 'XL']
        colors = ['Red', 'Blue', 'Green', 'Black', 'White']
        for product in products:
            for _ in range(3):  # 3 variants per product
                variant = ProductVariant.objects.create(
                    product=product,
                    size=choice(sizes),
                    color=choice(colors),
                    additional_price=round(fake.pydecimal(left_digits=2, right_digits=2, positive=True), 2),
                    stock=randint(5, 50)
                )
                variants.append(variant)
        self.stdout.write(self.style.SUCCESS(f"{len(variants)} Product Variants created."))

        # Generate Product Images
        for product in products:
            for _ in range(randint(1, 3)):  # 1-3 images per product
                response = requests.get('https://picsum.photos/400/400', stream=True)
                if response.status_code == 200:
                    product_image = ProductImage.objects.create(
                        product=product,
                        is_main=False,
                    )
                    product_image.image.save(f"{product.name}_{fake.word()}.jpg", ContentFile(response.content))
            
            # Ensure at least one main image
            main_image = ProductImage.objects.create(
                product=product,
                is_main=True,
            )
            response = requests.get('https://picsum.photos/400/400', stream=True)
            if response.status_code == 200:
                main_image.image.save(f"{product.name}_main.jpg", ContentFile(response.content))

        # Generate Carts and CartItems for the single user
        cart = Cart.objects.create(user=user)
        for _ in range(randint(1, 5)):  # 1-5 items per cart
            CartItem.objects.create(
                cart=cart,
                product_variant=choice(variants),
                quantity=randint(1, 5)
            )
        self.stdout.write(self.style.SUCCESS("Cart and CartItems created for user."))

        # Generate Orders and OrderItems for the user
        for _ in range(randint(1, 3)):  # 1-3 orders per user
            order = Order.objects.create(
                user=user,
                total_price=round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2),
                status=choice([status[0] for status in Order.STATUS_CHOICES])
            )
            for _ in range(randint(1, 5)):  # 1-5 items per order
                OrderItem.objects.create(
                    order=order,
                    product_variant=choice(variants),
                    quantity=randint(1, 5),
                    price=round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)
                )
        self.stdout.write(self.style.SUCCESS("Orders and OrderItems created for user."))

        # Generate Reviews for the user
        for _ in range(randint(1, 5)):  # 1-5 reviews for the user
            Review.objects.create(
                product=choice(products),
                user=user,
                rating=randint(1, 5),
                comment=fake.sentence()
            )
        self.stdout.write(self.style.SUCCESS("Reviews created for user."))

        # Generate Wishlists for the user
        for _ in range(randint(1, 5)):  # 1-5 wishlist items for the user
            Wishlist.objects.create(
                user=user,
                product=choice(products)
            )
        self.stdout.write(self.style.SUCCESS("Wishlists created for user."))
