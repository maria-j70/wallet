import logging

from rest_framework import views, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from transaction.serializers import TransactionSerializer
from utils.internal_exceptions import (
    SameSourceAndDestinationWalletsError,
    DestinationWalletDoesNotExistError,
    SourceWalletNotEnoughBalanceError,
    IncorrectAmountError, SourceWalletDoesNotExistError, ErrorCode,
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
            raise SourceWalletDoesNotExistError

        w2w_obj = serializer.save(created_by=request.user)

        try:
            result = w2w_obj.apply()
            return Response(TransactionSerializer(result).data)

        except (SameSourceAndDestinationWalletsError, IncorrectAmountError, SourceWalletNotEnoughBalanceError,
                DestinationWalletDoesNotExistError) as e:
            w2w_obj.reject(reject_description=e.default_detail, reject_status=e.default_code)
            raise e

        except Exception as e:
            logger.exception(e)
            w2w_obj.reject(reject_description="unknown", reject_status=ErrorCode.Unknown)
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
