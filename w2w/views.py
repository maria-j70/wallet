import logging

from rest_framework import views, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)

from transaction.serializers import TransactionSerializer
from utils.internal_exceptions import (
    InvalidSourceAndDestinationWalletsError,
    DestinationWalletDoesNotExistError,
    RepetitiveTransactionError,
    SourceWalletNotEnoughBalanceError,
    TrackerIdDuplicatedError,
    TransactionAmountIncorrectError,
)
from .models import W2WDelay
from .serializers import W2WDelaySerializer, W2WModelSerializer

logger = logging.getLogger(__name__)


class W2WView(views.APIView):
    serializer = W2WModelSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):  # noqa C901
        serializer = self.serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        source_wallet = data["source_wallet"]
        if not self.request.user.id == source_wallet.owner.id:
            return Response(data={
                "error": "source wallet id was not found"
            }, status=HTTP_404_NOT_FOUND)

        try:
            w2w_obj = serializer.save(created_by=request.user)

        except TrackerIdDuplicatedError:
            return Response(data={
                "error": "Tracker id is duplicated"
            }, status=HTTP_400_BAD_REQUEST)

        try:
            result = w2w_obj.apply()
            return Response(TransactionSerializer(result).data)

        except InvalidSourceAndDestinationWalletsError:
            w2w_obj.reject()
            return Response(data={
                "error": "source and destination are same wallets"
            }, status=HTTP_400_BAD_REQUEST)

        except TransactionAmountIncorrectError:
            w2w_obj.reject()
            return Response(data={
                "error": "amount must be greater than 0"
            }, status=HTTP_400_BAD_REQUEST)

        except SourceWalletNotEnoughBalanceError:
            w2w_obj.reject()
            return Response(data={
                "error": "source wallet have not enough balance."
            }, status=HTTP_400_BAD_REQUEST)

        except RepetitiveTransactionError:
            return Response(data={
                "error": "This Transaction has been done"
            }, status=HTTP_400_BAD_REQUEST)

        except DestinationWalletDoesNotExistError:
            w2w_obj.reject()
            return Response(data={
                "error": "Failed to deposit into destination"
            }, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)
            w2w_obj.reject()
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)


class W2WDelayView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = W2WDelaySerializer

    def get_queryset(self):
        user = self.request.user
        return W2WDelay.objects.filter(created_by=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not serializer.validated_data["source_wallet"].owner_id == user.id:
            raise PermissionDenied

        serializer.save(created_by=user)
