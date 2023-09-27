from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PetopiaApp.forms import PetCategoryForm, ProductForm, RegisterForm, CheckoutForm


class FormsTestCase(TestCase):

    def setUp(self):
        self.pet_category_data = {'name': 'Cat'}
        self.brand = {'name': 'Brand'}
        image_data = SimpleUploadedFile("media_root/images/product_images/cat_carrier1.jpg",
                                        b"file_content", content_type="image/jpeg")

        self.product_data = {'name': 'Product 1', 'price': 19.99, 'short_description': 'Short description',
                             'detailed_description': 'Detailed description', 'slug': 'product-1',
                             'pet_category': self.pet_category_data.get('id'), 'brand': self.brand.get('id'),
                             'image': image_data}

        self.register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        self.checkout_data = {
            'street_address': '1234 Main St',
            'apartment_address': 'Apt 101',
            'country': 'US',
            'zip': '12345',
            'same_shipping_address': True,
            'save_info': True,
            'payment_option': 'S',
        }

    def test_pet_category_form(self):
        form = PetCategoryForm(data=self.pet_category_data)
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        form = RegisterForm(data=self.register_data)
        self.assertTrue(form.is_valid())

    def test_checkout_form(self):
        form = CheckoutForm(data=self.checkout_data)
        self.assertTrue(form.is_valid())

    def test_invalid_checkout_form(self):
        invalid_data = {
            'street_address': '',
            'country': 'INVALID_COUNTRY',
        }
        form = CheckoutForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_checkout_form_view(self):
        response = self.client.get(reverse('PetopiaApp:checkout'))
        self.assertEqual(response.status_code, 302)
