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

class IsAliasOrEntryOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.owner == request.user
    
class HasLessThanTenAliases(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = request.user.profile
        except:
            self.message = 'You need to have a profile to create aliases'
            return False
        if len(profile.alias.all())>=10:
            self.message = "You can't create more than 10 aliases"
            return False
        else:
            return True