from rest_framework.exceptions import APIException
from rest_framework import status


class WalletAccessException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Access to this wallet is not allowed'
    default_code = 'Forbidden'
