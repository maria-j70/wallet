from django.contrib.contenttypes.models import ContentType
from django.db import models

from transaction.models import Transaction
from .internal_exceptions import RepetitiveTransactionError


class Features(models.Model):
    ACTIVE_SINGLE_EXECUTION = False
    source_wallet = None
    destination_wallet = None
    amount = None

    def apply(self):
        transaction = Transaction.execute(
            source_wallet=self.get_source_wallet(),
            destination_wallet=self.get_destination_wallet(),
            amount=self.get_amount(),
            content_type_id=self.get_content_type_id(),
            object_id=self.get_object_id(),
            pre_func=self.get_pre_apply(),
            post_func=self.get_post_apply(),
        )
        return transaction

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

    def get_source_wallet(self):
        return self.source_wallet

    def get_destination_wallet(self):
        return self.destination_wallet

    def get_amount(self):
        return self.amount

    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self).id

    def get_object_id(self):
        return self.id

    class Meta:
        abstract = True


class FeaturesStatus(models.IntegerChoices):
    pending = 0
    done = 5
    failed = 10
