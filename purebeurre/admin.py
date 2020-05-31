from django.contrib import admin
from .models import Category, Product, Favorite, UserInfos


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
    list_display = ('user', 'substitute')
    search_fields = ('user', 'substitute', )
    list_filter = ['user', 'substitute']


@admin.register(UserInfos)
class UserInfosAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
