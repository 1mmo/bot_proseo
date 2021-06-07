from django.contrib import admin
from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "black_list")
    list_filter = ("url", "black_list")
