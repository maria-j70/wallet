import uuid
from typing import Callable, List

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction

from transaction.data import TransactionData
from utils.internal_exceptions import (
    IncorrectAmountError,
    SourceWalletNotEnoughBalanceError,
    DestinationWalletDoesNotExistError,
    SameSourceAndDestinationWalletsError,
)
from wallet_app.models import Wallet
from .enums import ActionChoices

User = get_user_model()


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1, editable=False)
    object_id = models.PositiveBigIntegerField(default=None, editable=False)
    content_object = GenericForeignKey()

    class Meta:
        ordering = ["-id"]

    @classmethod
    def execute(
            cls,
            transaction_list: List[TransactionData],
            content_type_id: int,
            object_id: int,
            pre_func: Callable[[], None] = None,
            post_func: Callable[[], None] = None,
    ) -> "Transaction":

        if pre_func and not callable(pre_func):
            raise ValueError("The pre_func must be callable or None")
        if post_func and not callable(post_func):
            raise ValueError("The pre_func must be callable or None")

        with transaction.atomic():
            if pre_func:
                pre_func()

            transaction_obj = Transaction.objects.create(content_type_id=content_type_id, object_id=object_id)

            for transaction_data in transaction_list:
                amount = transaction_data.amount
                source_wallet = transaction_data.source_wallet
                destination_wallet = transaction_data.destination_wallet
                index = transaction_data.index
                action_type = transaction_data.action_type
                description = transaction_data.description

                if amount < 0:
                    raise IncorrectAmountError(index=index)
                if source_wallet.id == destination_wallet.id:
                    raise SameSourceAndDestinationWalletsError(index=index)

                # withdraw from source wallet
                is_withdrawn = Wallet.objects.filter(id=source_wallet.id, balance__gte=amount).update(
                    balance=models.F("balance") - amount
                )
                if is_withdrawn != 1:
                    raise SourceWalletNotEnoughBalanceError(index=index)

                # Deposit to destination wallet
                is_deposit = Wallet.objects.filter(id=destination_wallet.id).update(
                    balance=models.F("balance") + amount)
                if is_deposit != 1:
                    raise DestinationWalletDoesNotExistError(index=index)

                random_uuid_str = str(uuid.uuid4())

                Action.objects.create(
                    transaction=transaction_obj,
                    wallet=source_wallet,
                    amount=-amount,
                    action_type=action_type,
                    description=description,
                    mirror_code=random_uuid_str,
                )
                Action.objects.create(
                    transaction=transaction_obj,
                    wallet=destination_wallet,
                    amount=amount,
                    action_type=action_type,
                    description=description,
                    mirror_code=random_uuid_str,
                )
                source_wallet.balance -= amount
                destination_wallet.balance += amount
            if post_func:
                post_func()

        return transaction_obj


class Action(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name="actions")
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="actions")
    amount = models.IntegerField()
    description = models.TextField(null=True, default=None)
    io = models.BooleanField(default=None, help_text="Determine the action is Input to wallet or Output."
                                                     " True means Input and False means Output.")
    mirror_code = models.TextField(null=False)
    action_type = models.IntegerField(choices=ActionChoices.choices, default=None)

    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # Set io based on the sign of the amount
        self.io = self.amount >= 0
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]
