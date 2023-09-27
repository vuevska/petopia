from django.core.paginator import Paginator
from django.test import TestCase, Client
from django.urls import reverse

from PetopiaApp.models import PetCategory, Brand, Product
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('PetopiaApp:home')
        self.product_url = reverse('PetopiaApp:product', args=['Test Category', 'product-1'])
        self.add_product_url = reverse('PetopiaApp:add_product')
        self.category = PetCategory.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Brand')
        self.product1 = Product.objects.create(
            name='Product 1',
            pet_category=self.category,
            short_description='Short description 1',
            price=10,
            brand=self.brand,
            image="#",
            slug='product-1'
        )
        self.username = 'testuser'
        self.password = 'TestPassword123!'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        self.pet_category_url = reverse('PetopiaApp:add_pet_category')

    def test_petopia_list_GET(self):
        response = self.client.get(self.home_url)

        products = Product.objects.all()
        all_products = Paginator(products, 8)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.assertIn('products', response.context)

        response_products = response.context['products']
        self.assertEqual(list(response_products), list(all_products.page(1)))

    def test_product_view(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'product.html')
        self.assertIn('object', response.context)
        self.assertIn('pet_category', response.context)

        self.assertEqual(response.context['object'], self.product1)
        self.assertEqual(response.context['pet_category'], 'Test Category')

    def test_add_pet_category_GET(self):
        response = self.client.get(self.pet_category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-actions/add_pet_category.html')

    def test_add_pet_category_POST(self):
        data = {'name': 'New Category'}
        response = self.client.post(self.pet_category_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PetCategory.objects.filter(name='New Category').exists())

    def test_add_product_GET(self):
        response = self.client.get(self.add_product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin-actions/add_product.html')
