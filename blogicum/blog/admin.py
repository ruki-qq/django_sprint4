from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'is_published')
    search_fields = ('title', 'author')
    list_filter = ('category',)
    list_display_links = ('title',)
