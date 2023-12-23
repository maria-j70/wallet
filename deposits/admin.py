import logging

from django.contrib import admin
from django.contrib import messages

from utils.internal_exceptions import (
    IncorrectAmountError,
    TrackerIdDuplicatedError,
    SourceWalletNotEnoughBalanceError,
    DestinationWalletDoesNotExistError,
    RepetitiveTransactionError, ErrorCode,
)
from .models import Deposit

logger = logging.getLogger(__name__)


@admin.action(description="Approve")
def approve_deposit(modeladmin, request, queryset):
    for deposit_obj in queryset:
        try:
            deposit_obj.apply()
        except (IncorrectAmountError, TrackerIdDuplicatedError, SourceWalletNotEnoughBalanceError,
                DestinationWalletDoesNotExistError) as e:
            deposit_obj.reject(reject(reject_description=e.default_detail, reject_status=e.default_code))
            messages.error(request, e.default_detail)

        except RepetitiveTransactionError as e:
            messages.error(request, e.default_detail)

        except Exception as e:
            logger.exception(e)
            deposit_obj.reject(reject_description="unknown", reject_status=ErrorCode.Unknown)
            messages.error(request, "Unexpected error")



@admin.action(description="Reject")
def reject(modeladmin, request, queryset):
    for object_obj in queryset:
        object_obj.reject(reject_description="admin reject", reject_status=ErrorCode.Admin)


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_filter = ["wallet"]
    list_display = ["wallet", "status", "amount", "tracker_id", "created_at"]
    actions = [reject, approve_deposit]
