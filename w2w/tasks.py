from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from utils.base_moldel import FeaturesStatus
from utils.internal_exceptions import (
    RepetitiveTransactionError,
    IncorrectAmountError,
    SourceWalletNotEnoughBalanceError, SameSourceAndDestinationWalletsError, DestinationWalletDoesNotExistError,
    ErrorCode,
)
from .models import W2WDelay

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
                SameSourceAndDestinationWalletsError, IncorrectAmountError, SourceWalletNotEnoughBalanceError,
                DestinationWalletDoesNotExistError,

        ) as e:
            w2w_delay_oj.reject(reject_description=e.default_detail, reject_status=e.default_code)
            raise e

        except Exception as e:
            logger.exception(reject_description="unknown", reject_status=ErrorCode.Unknown)
            w2w_delay_oj.reject()
