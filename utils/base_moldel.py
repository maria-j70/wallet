from abc import abstractmethod

from django.contrib.contenttypes.models import ContentType
from django.db import models

from transaction.data import TransactionData
from transaction.models import Transaction
from utils.internal_exceptions import RepetitiveTransactionError


class Features(models.Model):
    ACTIVE_SINGLE_EXECUTION = False
    source_wallet = None
    destination_wallet = None
    amount = None

    class Meta:
        abstract = True

    def apply(self):
        transaction = Transaction.execute(
            transaction_list=self.get_transaction_list(),
            content_type_id=self.get_content_type_id(),
            object_id=self.get_object_id(),
            pre_func=self.get_pre_apply(),
            post_func=self.get_post_apply(),
        )
        return transaction

    @abstractmethod
    def get_transaction_list(self):
        raise NotImplementedError


    def reject(self, reject_description, reject_status):
        self.__class__.objects.filter(id=self.id, status=FeaturesStatus.pending). \
            update(status=FeaturesStatus.failed,
                   reject_status=reject_status,
                   reject_description=reject_description
                   )

    def get_pre_apply(self):
        return self.pre_single_execution if self.ACTIVE_SINGLE_EXECUTION else None

    def pre_single_execution(self):
        has_update = self.__class__.objects.filter(id=self.id, status=FeaturesStatus.pending).update(
            status=FeaturesStatus.done
        )
        if has_update == 0:
            raise RepetitiveTransactionError

    def get_post_apply(self):
        pass

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id

    def get_object_id(self):
        return self.id




class FeaturesStatus(models.IntegerChoices):
    pending = 0
    done = 5
    failed = 10
