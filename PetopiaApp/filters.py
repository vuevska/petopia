import django_filters
from PetopiaApp.models import Product


class ProductFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)

        for field in self.form:
            field.field.widget.attrs["id"] = "product-category-select"
            field.field.widget.attrs["class"] = "form-select"

    class Meta:
        models = Product
        fields = ['category', ]
