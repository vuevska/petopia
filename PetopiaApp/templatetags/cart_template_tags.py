from django import template
from PetopiaApp.models import ShoppingCart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = ShoppingCart.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].get_total_num_items()
    return 0
