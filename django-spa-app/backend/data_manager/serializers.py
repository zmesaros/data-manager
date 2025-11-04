from rest_framework import serializers
from .models import Item, Customer


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model.
    Handles automatic validation and conversion to/from JSON.
    """
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'quantity', 'price',
            'category', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    Handles automatic validation and conversion to/from JSON.
    """
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'country', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
