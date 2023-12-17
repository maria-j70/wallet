from rest_framework.permissions import BasePermission
from .models import Wallet


class WalletRetrieveDestroyPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Wallet):
        return obj.owner == request.user
