from .models import Order
from customers.models import Customer
from customers.permissions import isOwner
from rest_framework import generics,permissions
from .serializers import OrderSerializer,DeliverSerializer

class Deliver(generics.UpdateAPIView):
    queryset=Order.objects.all()
    serializer_class=DeliverSerializer
    permission_classes=[permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        """Allows admins to mark an order as delivered"""
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """Allows admins to mark an order as delivered"""
        return super().patch(request, *args, **kwargs)

class Orders(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        """
        Lists all the orders for all the customers.
        Only available to admins
        """
        return super().get(request, *args, **kwargs)

class OrdersList(generics.ListCreateAPIView):
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Allows logged in user to make an order"""
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Lists all the orders of the logged in user"""
        return super().get(request, *args, **kwargs)

    def perform_create(self,serializer):
        """Attach the order to the logged in user"""
        customer=Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)

    def get_queryset(self):
        customer=Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[isOwner]

    def get(self, request, *args, **kwargs):
        """
        Retrieves an order. 
        Only available to the owner of the order.
        """
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        Retrieves an order to update. 
        Only available to the owner of the order.
        """
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """
        Retrieves an order to update. 
        Only available to the owner of the order.
        """
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """
        Retrieves an order to delete. 
        Only available to the owner of the order.
        """
        return super().delete(request, *args, **kwargs)