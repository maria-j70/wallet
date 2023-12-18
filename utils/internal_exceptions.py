from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    pass


class WalletAccessException(BaseCustomException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Access to this wallet is not allowed"
    default_code = "Forbidden"


class SourceWalletNotEnoughBalanceError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "source wallet have not enough balance."
    default_code = "error"


class TransactionAmountIncorrectError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "amount must be greater than 0"
    default_code = "error"


class TrackerIdDuplicatedError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Tracker id is duplicated"
    default_code = "error"


class SameSourceAndDestinationWalletsError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "source and destination are same wallets"
    default_code = "error"


class DestinationWalletDoesNotExistError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "destination wallet does not exists"
    default_code = "error"


class RepetitiveTransactionError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "This transaction has been verified "
    default_code = "error"


class WalletAccessError(BaseCustomException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Access to this wallet is not allowed"
    default_code = "Forbidden"
