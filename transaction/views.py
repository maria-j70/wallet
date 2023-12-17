from rest_framework import generics, views
from .serializers import TransactionSerializer, ActionSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Action, ActionChoices



class HistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActionSerializer

    lookup_url_kwarg = 'wallet_id'

    def get_queryset(self):
        user = self.request.user
        wallet_id = self.kwargs['wallet_id']
        return Action.objects.filter(wallet__owner=user, wallet_id=wallet_id)


