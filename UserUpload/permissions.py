from rest_framework.permissions import BasePermission


class CanGenerateLink(BasePermission):
    def has_permission(self, request, view):
        return request.user.tier.can_generate_link
