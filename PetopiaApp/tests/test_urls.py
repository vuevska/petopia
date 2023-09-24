from django.test import SimpleTestCase
from django.urls import resolve, reverse
from PetopiaApp.views import home, add_product, add_pet_category,\
    product, shopping_cart, add_to_cart, remove_from_cart,\
    remove_one_item_from_cart, checkout, payment, orders


class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse("PetopiaApp:home")
        self.assertEqual(resolve(url).func, home)

    def test_pet_category_url(self):
        url = reverse("PetopiaApp:add_pet_category")
        self.assertEqual(resolve(url).func, add_pet_category)

    def test_add_product_url(self):
        url = reverse("PetopiaApp:add_product")
        self.assertEqual(resolve(url).func, add_product)

    def test_product_url(self):
        url = reverse("PetopiaApp:product", args=['name', 'slug'])
        self.assertEqual(resolve(url).func, product)

    def test_shopping_cart_url(self):
        url = reverse("PetopiaApp:shopping_cart")
        self.assertEqual(resolve(url).func, shopping_cart)

    def test_add_to_cart_url(self):
        url = reverse("PetopiaApp:add_to_cart", args=['slug'])
        self.assertEqual(resolve(url).func, add_to_cart)

    def test_remove_from_cart_url(self):
        url = reverse("PetopiaApp:remove_from_cart", args=['slug'])
        self.assertEqual(resolve(url).func, remove_from_cart)

    def test_remove_one_item_from_cart_url(self):
        url = reverse("PetopiaApp:remove_one_item_from_cart", args=['slug'])
        self.assertEqual(resolve(url).func, remove_one_item_from_cart)

    def test_checkout_url(self):
        url = reverse("PetopiaApp:checkout")
        self.assertEqual(resolve(url).func, checkout)

    def test_payment_url(self):
        url = reverse("PetopiaApp:payment", args=['payment_option'])
        self.assertEqual(resolve(url).func, payment)

    def test_orders_url(self):
        url = reverse("PetopiaApp:orders")
        self.assertEqual(resolve(url).func, orders)
