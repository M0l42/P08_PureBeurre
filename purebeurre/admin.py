from django.contrib import admin
from .models import Category, Product, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tags', 'products')
    search_fields = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'nutrition_grade')
    search_fields = ('name', )
    list_filter = ['category']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user', 'product', )
    list_filter = ['user', 'product']
