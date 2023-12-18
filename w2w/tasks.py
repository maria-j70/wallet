from celery import shared_task

from utils.internal_exceptions import (
    RepetitiveTransactionError,
    DestinationWalletDoesNotExistError,
    TransactionAmountIncorrectError,
    SourceWalletNotEnoughBalanceError,
    TrackerIdDuplicatedError, InvalidSourceAndDestinationWalletsError,
)
from .models import W2WDelay
from django.utils import timezone
from utils.base_moldel import FeaturesStatus
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task()
def run_w2w_delay():
    w2w_query = W2WDelay.objects.filter(apply_at__lte=timezone.now(), status=FeaturesStatus.pending)
    for w2w_delay_oj in w2w_query:
        try:
            w2w_delay_oj.apply()

        except RepetitiveTransactionError:
            pass

        except (
                TransactionAmountIncorrectError,
                InvalidSourceAndDestinationWalletsError,
                SourceWalletNotEnoughBalanceError,
                DestinationWalletDoesNotExistError,

        ):
            w2w_delay_oj.reject()
        except Exception as e:
            logger.exception(e)
            w2w_delay_oj.reject()

