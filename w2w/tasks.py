from celery import shared_task

from utils.internal_exceptions import (
    RepetitiveTransactionError,
    DestinationWalletDoesNotExistError,
    TransactionAmountIncorrectError,
    SourceWalletNotEnoughBalanceError,
    TrackerIdDuplicatedError,
)
from .models import W2WDelay
from django.utils import timezone
from utils.base_moldel import FeaturesStatus


@shared_task()
def run_w2w_delay():
    print("im here")
    w2w_query = W2WDelay.objects.filter(apply_at__lte=timezone.now(), status=FeaturesStatus.pending)
    for w2w_delay_oj in w2w_query:
        try:
            w2w_delay_oj.apply()

        except RepetitiveTransactionError:
            pass

        except (
            DestinationWalletDoesNotExistError,
            TrackerIdDuplicatedError,
            TransactionAmountIncorrectError,
            SourceWalletNotEnoughBalanceError,
        ):
            w2w_delay_oj.reject()
