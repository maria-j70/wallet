from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import WithdrewSerializer
from .models import Withdrew

from .exceptions import WalletAccessException


class WithdrewCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrewSerializer

    def get_queryset(self):
        user = self.request.user
        return Withdrew.objects.filter(created_by=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not serializer.validated_data["wallet"].owner_id == user.id:
            raise WalletAccessException

        serializer.save(created_by=user)
