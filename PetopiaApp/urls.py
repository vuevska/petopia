from django.urls import path
from PetopiaApp.views import home, add_pet_category, shopping_cart, add_to_cart, \
    remove_from_cart, product, remove_one_item_from_cart, checkout, add_product, payment, orders
from django.conf import settings
from django.conf.urls.static import static

app_name = 'PetopiaApp'

urlpatterns = [
    path("", home, name='home'),
    path(r"^/<category>", home, name='home'),

    path("add-pet-category/", add_pet_category, name='add_pet_category'),
    path("add-product", add_product, name='add_product'),

    path('product/<name>/<slug>', product, name='product'),

    path('cart/shopping-cart/', shopping_cart, name='shopping_cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('remove_one_item_from_cart/<slug>', remove_one_item_from_cart, name='remove_one_item_from_cart'),

    path('checkout/', checkout, name='checkout'),
    path('payment/<payment_option>/', payment, name='payment'),
    path('orders/', orders, name='orders')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
