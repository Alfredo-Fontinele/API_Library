from rest_framework import permissions
from .models import Following

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_collaborator is False
class IsTheSameStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj:Following):
        return request.user.is_authenticated and request.user.id == obj.student.id