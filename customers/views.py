from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics,permissions

class UserList(generics.ListAPIView):
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Lists all registers users. 
        Only available to admins
        """
        return super().get(request, *args, **kwargs)

class UserDetail(generics.RetrieveAPIView):
    lookup_field="username"
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Retrieves a user with the given username. 
        Available to authenticated and unauthenticated users.
        """
        return super().get(request, *args, **kwargs)

class CurrentUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieves the information of the current authenticated user"""
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """Allows the current authenticated user to update their information"""
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """Allows the current authenticated user to update their information"""
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """Allows the current authenticated user to delete their information"""
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        return self.request.user