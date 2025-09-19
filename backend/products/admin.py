from django.contrib import admin
from .models import Product, Order, ProductOrder


class ProductOrderInline(admin.TabularInline):  # или StackedInline
    model = ProductOrder
    extra = 1

    def product_price(self, obj):
        if obj.product:
            return obj.product.price
        return "-"
    product_price.short_description = "Цена"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_amount")
    inlines = [ProductOrderInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")
