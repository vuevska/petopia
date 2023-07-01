from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

PRODUCT_CATEGORIES = (
    ('food', 'food'),
    ('hygiene', 'hygiene'),
    ('toys', 'toys'),
    ('transport', 'transport')
)


class PetCategory(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/pet_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to="images/product_images/", null=True)
    short_description = models.CharField(max_length=255)
    detailed_description = models.TextField()
    pet_category = models.ForeignKey(PetCategory, on_delete=models.CASCADE)
    product_category = models.CharField(max_length=10, choices=PRODUCT_CATEGORIES)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def get_absolute_url(self):
        return reverse("PetopiaApp:product", kwargs={
            'slug': self.slug,
            'name': self.pet_category
        })


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    def get_total_cart_item_price(self):
        return self.quantity * self.product.price


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"{self.user.username}"

    def get_total(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.get_total_cart_item_price()
        return total

    def get_total_num_items(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.quantity
        return total

