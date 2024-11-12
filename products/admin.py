from django.contrib import admin
from products.models import Product, ProductCategory, Basket

# Register your models here.

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'sales')
    fields = ['name', 'description', ('price', 'quantity'), 'image', 'category', 'sales']
    readonly_fields = ['description', 'sales']
    search_fields = ('name',)
    ordering = ('name', 'price', 'quantity', 'category', 'sales')


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity']
    readonly_fields = ('created_at',)
    extra = 0
