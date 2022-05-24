from rest_framework import permissions


class IsLoggedUserEqualUserDetails(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS and obj.guest == request.user


class IsAdminOrLoggedInUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class LoggedInUserOrAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user == obj.guest:
            return True
        return obj.guest == request.user