from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics,permissions

class AddProduct(generics.CreateAPIView):
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        """
        Add a new product.
        Only available to admins
        """
        return super().post(request, *args, **kwargs)

class Products(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Lists all available products.
        Available to both authenticated and unauthenticated users
        """
        return super().get(request, *args, **kwargs)

class ProductDetail(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Get a product by with its ID.
        Available to both authenticated and unauthenticated users
        """
        return super().get(request, *args, **kwargs)

class ModifyProduct(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAdminUser]
    
    def put(self, request, *args, **kwargs):
        """
        Retrieves a product to update. 
        Only available to admins.
        """
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """
        Retrieves a product to update. 
        Only available to admins.
        """
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """
        Retrieves a product to delete. 
        Only available to admins.
        """
        return super().delete(request, *args, **kwargs)