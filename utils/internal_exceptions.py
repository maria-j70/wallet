from rest_framework.exceptions import PermissionDenied


class SourceWalletNotEnoughBalanceError(Exception):
    pass


class TransactionAmountIncorrectError(Exception):
    pass


class TrackerIdDuplicatedError(Exception):
    pass


class InvalidSourceAndDestinationWalletsError(Exception):
    pass

class DestinationWalletDoesNotExistError(Exception):
    pass


class RepetitiveTransactionError(Exception):
    pass
