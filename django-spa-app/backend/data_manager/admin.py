from django.contrib import admin
from .models import Item, Customer


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Item model.
    """
    list_display = ['id', 'name', 'category', 'quantity', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description', 'category']
    list_editable = ['is_active']
    ordering = ['-created_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.
    """
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'country', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['is_active']
    ordering = ['last_name', 'first_name']
