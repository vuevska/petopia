from django.contrib import admin

from .models import PetCategory, Product, Brand, ShoppingCart, \
    CartItem


class ProductCategoryAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class BrandAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "pet_category", "product_category", "price"]
    list_filter = ["pet_category", "product_category"]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(CartItem)
admin.site.register(ShoppingCart)
admin.site.register(PetCategory)
