from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'is_preorder', 'stock']
    list_filter = ['available', 'created', 'updated', 'is_preorder']
    list_editable = ['price', 'available', 'is_preorder', 'stock']
    prepopulated_fields = {'slug': ('name',)}