from django.contrib.auth import get_user_model
from django.db import models
from django.db.utils import IntegrityError

from transaction.data import TransactionData
from transaction.enums import ActionChoices
from utils.base_moldel import Features, FeaturesStatus
from utils.internal_exceptions import TrackerIdDuplicatedError
from wallet_app.constants import InternalWallets
from wallet_app.models import Wallet

User = get_user_model()


class W2W(Features):
    ACTIVE_SINGLE_EXECUTION = True
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_source_wallet')
    destination_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_destination_wallet')
    amount = models.PositiveBigIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tracker_id = models.CharField(max_length=255, null=True, default=None)
    status = models.IntegerField(default=FeaturesStatus.pending, choices=FeaturesStatus.choices)
    reject_status = models.IntegerField(default=None, null=True)
    reject_description = models.CharField(max_length=1000, null=True, default=None)

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["tracker_id"],
                name="unique_tracker_id_w2w",
            ),
        ]

    def get_action_type(self):
        return ActionChoices.w2w

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        except IntegrityError as e:
            if self.__class__.objects.filter(tracker_id=self.tracker_id).exists():
                raise TrackerIdDuplicatedError from None
            raise e

    def get_transaction_list(self):
        transaction_list = [
            TransactionData(
                source_wallet=self.source_wallet,
                destination_wallet=self.destination_wallet,
                amount=self.amount,
                action_type=self.get_action_type(),
                description=f"transfer money from wallet with ID "
                            f"{self.source_wallet_id} to wallet with ID {self.destination_wallet_id}"
            )

        ]
        wage_amount = self.calc_wage()
        if wage_amount:
            transaction_list.append(TransactionData(
                source_wallet=self.source_wallet,
                destination_wallet=InternalWallets.SYSTEM,
                amount=wage_amount,
                action_type=ActionChoices.wage,
                description=f"transfer money from wallet with ID "
                            f"{self.source_wallet_id} to wallet with ID system for wage"
            ))
        return transaction_list

    def calc_wage(self):
        config = self.created_by.config
        wage_amount = self.amount * config.wage_rate

        if wage_amount < config.min:
            return config.min
        elif wage_amount > config.max:
            return config.max
        return wage_amount


class W2WDelay(W2W):
    apply_at = models.DateTimeField(null=False)

    def get_action_type(self):
        return ActionChoices.w2w_delay
