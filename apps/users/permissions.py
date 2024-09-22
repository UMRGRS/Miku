from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    #Custom permission to only allow owner to access, modify or delete
    def has_object_permission(self, request, view, obj):
        return obj == request.user