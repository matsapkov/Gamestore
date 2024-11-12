from django.contrib import admin
from django.urls import path
from products.models import Product, ProductCategory, Basket
from django.http import HttpResponse
from docxtpl import DocxTemplate

# Register your models here.

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'sales')
    fields = ['name', 'description', ('price', 'quantity'), 'image', 'category', 'sales']
    readonly_fields = ['description', 'sales']
    search_fields = ('name',)
    ordering = ('name', 'price', 'quantity', 'category', 'sales')

    change_list_template = "admin/report_template.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-report/', self.generate_report, name='generate-report'),
        ]
        return custom_urls + urls

    def generate_report(self):

        top_games = Product.objects.order_by('-sales')[:3]

        context = {
            'game1_name': top_games[0].name if top_games.count() > 0 else "Нет данных",
            'game1_sales': top_games[0].sales if top_games.count() > 0 else 0,
            'game2_name': top_games[1].name if top_games.count() > 1 else "Нет данных",
            'game2_sales': top_games[1].sales if top_games.count() > 1 else 0,
            'game3_name': top_games[2].name if top_games.count() > 2 else "Нет данных",
            'game3_sales': top_games[2].sales if top_games.count() > 2 else 0,
        }

        doc = DocxTemplate("products/templates/docx/product_admin_top_template.docx")
        doc.render(context)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="report.docx"'
        doc.save(response)
        return response


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity']
    readonly_fields = ('created_at',)
    extra = 0
