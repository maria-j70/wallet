from rest_framework import status
from rest_framework.exceptions import APIException
from django.db import models


class ErrorCode(models.IntegerChoices):
    Unknown = 0
    Forbidden = 1
    NotEnoughBalance = 2
    IncorrectValue = 3
    Repetitive = 4
    Admin = 5


class BaseCustomException(APIException):
    pass


class SourceWalletNotEnoughBalanceError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "source wallet does not have enough balance."
    default_code = ErrorCode.NotEnoughBalance


class IncorrectAmountError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "amount must be greater than 0"
    default_code = ErrorCode.IncorrectValue


class TrackerIdDuplicatedError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Tracker id is duplicated"
    default_code = ErrorCode.IncorrectValue


class SameSourceAndDestinationWalletsError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "source and destination are same wallets"
    default_code = ErrorCode.IncorrectValue


class DestinationWalletDoesNotExistError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "destination wallet does not exists"
    default_code = ErrorCode.IncorrectValue


class SourceWalletDoesNotExistError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "source wallet does not exists"
    default_code = ErrorCode.IncorrectValue


class RepetitiveTransactionError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "This transaction has been verified "
    default_code = ErrorCode.Repetitive


class WalletAccessError(BaseCustomException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Access to this wallet is not allowed"
    default_code = ErrorCode.Forbidden
