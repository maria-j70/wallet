import logging

from django.contrib import admin

from utils.internal_exceptions import TransactionAmountIncorrectError, TrackerIdDuplicatedError, \
    SourceWalletNotEnoughBalanceError, RepetitiveTransactionError, DestinationWalletDoesNotExistError
from.models import Withdrew

from django.contrib import messages

# Register your models here.

logger = logging.getLogger(__name__)



@admin.action(description="Approve")
def approve_withdrew(modeladmin, request, queryset):
    for withdrew_obj in queryset:
        try:
            result = withdrew_obj.apply()

        except TransactionAmountIncorrectError:
            withdrew_obj.reject()
            messages.error(request, "amount must be greater than 0")

        except TrackerIdDuplicatedError:
            withdrew_obj.reject()
            messages.error(request, "Tracker id is duplicated")

        except SourceWalletNotEnoughBalanceError:
            withdrew_obj.reject()
            messages.error(request, "wallet have not enough balance.")

        except DestinationWalletDoesNotExistError:
            withdrew_obj.reject()
            messages.error(request, "destination wallet does not exist")

        except RepetitiveTransactionError:
            messages.error(request, "This Transaction already has been done.")
            
        except Exception as e:
            logger.exception(e)
            withdrew_obj.reject()
            messages.error(request, "Unexpected error")


@admin.action(description="Reject")
def reject(modeladmin, request, queryset):
    for withdrew_obj in queryset:
        withdrew_obj.reject()


@admin.register(Withdrew)
class WithdrewAdmin(admin.ModelAdmin):
    list_filter = ['wallet']
    list_display = ['wallet', 'status', 'amount', 'tracker_id', 'created_at']
    actions = [reject, approve_withdrew]
