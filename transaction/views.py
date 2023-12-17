from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Action
from .serializers import ActionSerializer


class HistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActionSerializer

    lookup_url_kwarg = "wallet_id"

    def get_queryset(self):
        user = self.request.user
        wallet_id = self.kwargs["wallet_id"]
        return Action.objects.filter(wallet__owner=user, wallet_id=wallet_id)
