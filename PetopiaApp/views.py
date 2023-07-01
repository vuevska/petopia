from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from PetopiaApp.filters import ProductFilter
from PetopiaApp.forms import PetCategoryForm, CheckoutForm, ProductForm
from PetopiaApp.models import Product, PetCategory, ShoppingCart, CartItem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Q


# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def home(request, category=None):
    all_products = Product.objects.all()
    search_query = request.GET.get('search_query')
    if category is not None and request.GET.get('search_query') is None:
        all_products = Product.objects.filter(pet_category=category).all()
    elif (category is None or category is not None) and request.GET.get('search_query') is not None:
        all_products = Product.objects.filter(Q(name__icontains=search_query) |
                                              Q(short_description__icontains=search_query)).all()

    pet_categories = PetCategory.objects.all()
    filter_form = ProductFilter(request.GET, queryset=all_products)

    p = Paginator(all_products, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    all_products = page_obj

    context = {'products': all_products, 'pet_categories': pet_categories, 'filter': filter_form}
    return render(request, "home.html", context)


@login_required(login_url="/accounts/login/?next=/")
def add_pet_category(request):
    if request.method == "POST":
        form_data = PetCategoryForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            pet_category = form_data.save(commit=False)
            pet_category.save()
            return redirect("PetopiaApp:home")
    return render(request, "admin-actions/add_pet_category.html", context={"form": PetCategoryForm})


@login_required(login_url="/accounts/login/?next=/")
def add_product(request):
    if request.method == "POST":
        form_data = ProductForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            print('form data is valid')
            product_obj = form_data.save(commit=False)
            product_obj.name = form_data.cleaned_data.get('name')
            product_obj.price = form_data.cleaned_data.get('price')
            product_obj.image = form_data.cleaned_data.get('image')
            product_obj.short_description = form_data.cleaned_data.get('short_description')
            product_obj.detailed_description = form_data.cleaned_data.get('detailed_description')
            product_obj.pet_category = form_data.cleaned_data.get('pet_category')
            product_obj.product_category = form_data.cleaned_data.get('product_category')
            product_obj.brand = form_data.cleaned_data.get('brand')
            product_obj.slug = form_data.cleaned_data.get('slug')
            product_obj.save()
            return redirect("PetopiaApp:home")
    return render(request, "admin-actions/add_product.html", context={"form": ProductForm})


def product(request, name, slug):
    product_object = Product.objects.filter(slug=slug)[0]
    context = {'object': product_object, 'pet_category': name}
    return render(request, "product.html", context)


@login_required(login_url="/accounts/login/?next=/")
def shopping_cart(request):
    try:
        cart = ShoppingCart.objects.get(user=request.user, ordered=False)
    except ObjectDoesNotExist:
        date_ordered = timezone.now()
        cart = ShoppingCart.objects.create(user=request.user, date_ordered=date_ordered)
    context = {'object': cart}
    return render(request, "cart/shopping_cart.html", context)


@login_required(login_url="/accounts/login/?next=/")
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False)
    cart_qs = ShoppingCart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(product__slug=product.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, "The item quantity was increased!")
            return redirect("PetopiaApp:shopping_cart")
        else:
            messages.info(request, "This item was added to your cart!")
            cart.items.add(cart_item)
            return redirect("PetopiaApp:shopping_cart")
    else:
        date_ordered = timezone.now()
        cart = ShoppingCart.objects.create(user=request.user, date_ordered=date_ordered)
        cart.items.add(cart_item)
        messages.info(request, "This item was added to your cart!")
        return redirect("PetopiaApp:shopping_cart")


@login_required(login_url="/accounts/login/?next=/")
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = ShoppingCart.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item = CartItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "The item was removed from your cart!")
            return redirect("PetopiaApp:shopping_cart")
        else:
            messages.info(request, "This item was not in your cart!")
            return redirect("PetopiaApp:product", slug=slug)
    else:
        messages.info(request, "You do not have an active shopping cart.")
        return redirect("PetopiaApp:product", slug=slug)


@login_required(login_url="/accounts/login/?next=/")
def remove_one_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = ShoppingCart.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item = CartItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "The item quantity was decreased.")
            return redirect("PetopiaApp:shopping_cart")
        else:
            messages.info(request, "This item was not in your cart!")
            return redirect("PetopiaApp:product", slug=slug)
    else:
        messages.info(request, "You do not have an active shopping cart.")
        return redirect("PetopiaApp:product", slug=slug)


@login_required(login_url="/accounts/login/?next=/")
def checkout(request):
    if request.method == 'GET':
        form = CheckoutForm()
        cart = ShoppingCart.objects.get(user=request.user, ordered=False)
        context = {'form': form, 'object': cart}
        return render(request, 'cart/checkout.html', context)
    if request.method == "POST":
        form = CheckoutForm(data=request.POST)
        try:
            cart = ShoppingCart.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')
                cart.save()
                if payment_option == 'S':
                    return redirect('PetopiaApp:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('PetopiaApp:payment', payment_option='paypal')
            else:
                messages.warning(request, "Failed Checkout")
                return render(request, 'cart/checkout.html', {'form': form})
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active shopping cart!")
            return redirect("PetopiaApp:shopping_cart")


@login_required(login_url="/accounts/login/?next=/")
def payment(request, payment_option):
    if request.method == "GET":
        cart = ShoppingCart.objects.get(user=request.user, ordered=False)
        context = {'payment_option': payment_option, 'object': cart}
        return render(request, "cart/payment.html", context)
    if request.method == "POST":
        cart = ShoppingCart.objects.get(user=request.user, ordered=False)
        cart.ordered = True
        cart.date_ordered = timezone.now()
        cart.save()
        messages.success(request, "Your order was successful!")
        return redirect("PetopiaApp:home")


@login_required(login_url="/accounts/login/?next=/")
def orders(request):
    query = ShoppingCart.objects.filter(user=request.user, ordered=True)
    context = {'orders': query}
    return render(request, "cart/orders.html", context)
