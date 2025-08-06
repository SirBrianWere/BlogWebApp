from django.contrib import admin
from .models import Product, Comment

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'author', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('slug',)  # Since you're auto-generating it

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)