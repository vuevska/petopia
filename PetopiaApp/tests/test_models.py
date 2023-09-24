from django.test import TestCase
from PetopiaApp.models import Product, PetCategory, Brand, CartItem, ShoppingCart
from django.urls import reverse
from django.contrib.auth.models import User


class TestModels(TestCase):

    def setUp(self):
        self.category = PetCategory.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Brand')
        self.product1 = Product.objects.create(
            name='Product 1',
            pet_category=self.category,
            short_description='Short description 1',
            price=20.0,
            brand=self.brand,
            image="#",
            slug='product-1'
        )
        self.user = User.objects.create_user(username='testuser', password='testPassword!1')
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product1,
            quantity=3,
            ordered=False
        )

        self.cart_item1 = CartItem.objects.create(
            user=self.user,
            product=self.product1,
            quantity=2,
            ordered=False
        )

        self.shopping_cart = ShoppingCart.objects.create(
            user=self.user,
            date_created=None,
            date_ordered=None,
            ordered=False
        )
        self.shopping_cart.items.add(self.cart_item, self.cart_item1)

    def test_product_get_absolute_url(self):
        url = self.product1.get_absolute_url()
        expected_url = reverse("PetopiaApp:product", kwargs={
            'slug': self.product1.slug,
            'name': self.category.name
        })
        self.assertEqual(url, expected_url)

    def test_get_total_cart_item_price(self):
        total_price = self.cart_item.get_total_cart_item_price()
        expected_total_price = 3 * 20.0
        self.assertEqual(total_price, expected_total_price)

    def test_get_total(self):
        total = self.shopping_cart.get_total()
        expected_total = (2 * 20.0) + (3 * 20.0)
        self.assertEqual(total, expected_total)

    def test_get_total_num_items(self):
        total_num_items = self.shopping_cart.get_total_num_items()
        expected_total_num_items = 2 + 3
        self.assertEqual(total_num_items, expected_total_num_items)