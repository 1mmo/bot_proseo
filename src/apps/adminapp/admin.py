from django.contrib import admin
from .models import Users, Url, Chats, Category, Post


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("__str__", "username", "status", "subscribe", "black_list")
    list_filter = ("username", "black_list")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('title',)
    ordering = ['title']


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "description", 'get_category', "black_list")
    list_filter = ("url", "category", "black_list")


@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "description", "get_category", "black_list")
    list_filter = ("url", "category", "black_list")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
