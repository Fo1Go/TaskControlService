from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import ROLES


class IsUserCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=ROLES.CUSTOMER).exists()


class IsUserEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=ROLES.EMPLOYER).exists()


class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=ROLES.ADMIN).exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.customer == request.user
                or obj.employer == request.user)


class IsNoEmployer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.employer is None


class UpdateDoneTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not(request.method in ('PATCH', 'PUT') and obj.is_done())
