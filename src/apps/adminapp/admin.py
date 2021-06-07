from django.contrib import admin
from .models import Users, Url, Chats


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("chat_id", "username", "status", "subscribe", "black_list")
    list_filter = ("chat_id", "username", "black_list")


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "black_list")
    list_filter = ("url", "black_list")


@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "black_list")
    list_filter = ("url", "black_list")
