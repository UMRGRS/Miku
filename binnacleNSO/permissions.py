from rest_framework import permissions

#Custom permissions to only allow owner to access, modify or delete

class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class NoProfileCreated(permissions.BasePermission):
    message = 'You already have a profile created'
    def has_permission(self, request, view):
        try:
            request.user.profile
            return False
        except:
            return True

class IsAliasOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.owner == request.user
    
class IsEntryOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.owner == request.user