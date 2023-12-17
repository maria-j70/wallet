import logging

from django.contrib import admin
from django.contrib import messages

from utils.internal_exceptions import TransactionAmountIncorrectError, TrackerIdDuplicatedError, \
    SourceWalletNotEnoughBalanceError, DestinationWalletDoesNotExistError, RepetitiveTransactionError
from .models import Deposit

logger = logging.getLogger(__name__)


@admin.action(description="Approve")
def approve_deposit(modeladmin, request, queryset):
    for deposit_obj in queryset:
        try:
            deposit_obj.apply()
        except TransactionAmountIncorrectError:
            deposit_obj.reject()
            messages.error(request, "amount must be greater than 0")

        except TrackerIdDuplicatedError:
            deposit_obj.reject()
            messages.error(request, "Tracker id is duplicated")

        except SourceWalletNotEnoughBalanceError:
            deposit_obj.reject()
            messages.error(request, "source wallet have not enough balance.")

        except DestinationWalletDoesNotExistError:
            deposit_obj.reject()
            messages.error(request, "Failed to deposit into destination")

        except RepetitiveTransactionError:
            messages.error(request, "This Transaction already has been done ")

        except Exception as e:
            logger.exception(e)
            deposit_obj.reject()
            messages.error(request, "Unexpected error")


@admin.action(description="Reject")
def reject(modeladmin, request, queryset):
    for object_obj in queryset:
        object_obj.reject()


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_filter = ['wallet']
    list_display = ['wallet', 'status', 'amount', 'tracker_id', 'created_at']
    actions = [reject, approve_deposit]
