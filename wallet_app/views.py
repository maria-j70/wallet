from .models import Wallet
from .serializers import WalletCompleteSerializer, WalletSimpleSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import WalletRetrieveDestroyPermission


class WalletListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method.upper() == "GET":
            return WalletSimpleSerializer
        return WalletCompleteSerializer

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


class WalletRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, WalletRetrieveDestroyPermission]
    serializer_class = WalletCompleteSerializer

    queryset = Wallet.objects.filter(is_deleted=False)
    lookup_field = "id"
    lookup_url_kwarg = "wallet_id"

    def perform_destroy(self, instance):
        instance.is_deleted = False
        instance.save()
