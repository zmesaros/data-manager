from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Item, Customer
from .serializers import ItemSerializer, CustomerSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Item model.
    Provides CRUD operations with automatic pagination.
    
    Endpoints:
    - GET /api/items/ - List all items (paginated)
    - POST /api/items/ - Create a new item
    - GET /api/items/{id}/ - Retrieve a specific item
    - PUT /api/items/{id}/ - Update an item (full update)
    - PATCH /api/items/{id}/ - Partial update an item
    - DELETE /api/items/{id}/ - Delete an item
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Custom endpoint to get only active items.
        Access via: GET /api/items/active/
        """
        active_items = Item.objects.filter(is_active=True)
        page = self.paginate_queryset(active_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_items, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer model.
    Provides CRUD operations with automatic pagination.
    
    Endpoints:
    - GET /api/customers/ - List all customers (paginated)
    - POST /api/customers/ - Create a new customer
    - GET /api/customers/{id}/ - Retrieve a specific customer
    - PUT /api/customers/{id}/ - Update a customer (full update)
    - PATCH /api/customers/{id}/ - Partial update a customer
    - DELETE /api/customers/{id}/ - Delete a customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Custom endpoint to get only active customers.
        Access via: GET /api/customers/active/
        """
        active_customers = Customer.objects.filter(is_active=True)
        page = self.paginate_queryset(active_customers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_customers, many=True)
        return Response(serializer.data)
