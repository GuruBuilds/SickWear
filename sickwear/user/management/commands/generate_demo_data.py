from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, randint
from user.models import User, Category, Product, ProductVariant, Cart, CartItem, Order, OrderItem, Review, Wishlist
import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Generate demo data for the e-commerce app"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate Users
        users = []
        for _ in range(2):  # 20 demo users
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                phone_number=9876543211,
                address=fake.address()
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS("2 Users created."))

        # Generate Categories
        categories = []
        for _ in range(5):  # 5 demo categories
            category = Category.objects.create(
                name=fake.word().capitalize(),
                slug=fake.slug(),
                description=fake.text(),
            )
            # Fetch an image from Lorem Picsum
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

        # # Generate Carts and CartItems
        # for user in users:
        #     cart = Cart.objects.create(user=user)
        #     for _ in range(randint(1, 5)):  # 1-5 items per cart
        #         CartItem.objects.create(
        #             cart=cart,
        #             product_variant=choice(variants),
        #             quantity=randint(1, 5)
        #         )
        # self.stdout.write(self.style.SUCCESS("Carts and CartItems created."))

        # # Generate Orders and OrderItems
        # for user in users:
        #     for _ in range(randint(1, 3)):  # 1-3 orders per user
        #         order = Order.objects.create(
        #             user=user,
        #             total_price=round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2),
        #             status=choice([status[0] for status in Order.STATUS_CHOICES])
        #         )
        #         for _ in range(randint(1, 5)):  # 1-5 items per order
        #             OrderItem.objects.create(
        #                 order=order,
        #                 product_variant=choice(variants),
        #                 quantity=randint(1, 5),
        #                 price=round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)
        #             )
        # self.stdout.write(self.style.SUCCESS("Orders and OrderItems created."))

        # # Generate Reviews
        # for user in users:
        #     for _ in range(randint(1, 5)):  # 1-5 reviews per user
        #         Review.objects.create(
        #             product=choice(products),
        #             user=user,
        #             rating=randint(1, 5),
        #             comment=fake.sentence()
        #         )
        # self.stdout.write(self.style.SUCCESS("Reviews created."))

        # # Generate Wishlists
        # for user in users:
        #     for _ in range(randint(1, 5)):  # 1-5 wishlist items per user
        #         Wishlist.objects.create(
        #             user=user,
        #             product=choice(products)
        #         )
        # self.stdout.write(self.style.SUCCESS("Wishlists created."))
