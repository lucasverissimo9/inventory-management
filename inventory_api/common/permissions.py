from django.conf import settings
from rest_framework.permissions import BasePermission

class InternalRequest(BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("X-Internal-Token")

        if not token:
            return False

        return token == settings.INTERNAL_API_TOKEN