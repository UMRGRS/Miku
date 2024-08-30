from rest_framework import permissions

#Custom permissions to only allow owner to access, modify or delete

class IsAliasOrEntryOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class HasLessThanTenAliases(permissions.BasePermission):
    def has_permission(self, request, view):
        if len(request.user.alias.all())>=10:
            self.message = "You can't create more than 10 aliases"
            return False
        else:
            return True