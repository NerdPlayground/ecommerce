from rest_framework import permissions

class isOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        # Write permissions to object owners
        return obj.customer.user==request.user