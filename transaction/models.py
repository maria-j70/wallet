from typing import Callable

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction

from utils.internal_exceptions import (
    IncorrectAmountError,
    SourceWalletNotEnoughBalanceError,
    DestinationWalletDoesNotExistError,
    SameSourceAndDestinationWalletsError,
)
from wallet_app.models import Wallet
from . import constans

User = get_user_model()


class TransactionStatus(models.IntegerChoices):
    pending = 0
    done = 1
    failed = 2


class ActionChoices(models.IntegerChoices):
    w2w = 0
    deposit = 1
    withdrew = 2
    wage = 3



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
        source_wallet: Wallet,
        destination_wallet: Wallet,
        amount: int,
        content_type_id: int,
        object_id: int,
        pre_func: Callable[[], None] = None,
        post_func: Callable[[], None] = None,
    ) -> "Transaction":

        if pre_func and not callable(pre_func):
            raise ValueError("The pre_func must be callable or None")
        if post_func and not callable(post_func):
            raise ValueError("The pre_func must be callable or None")

        if amount < 1:
            Wallet.objects.filter()
            raise IncorrectAmountError
        if source_wallet.id == destination_wallet.id:
            raise SameSourceAndDestinationWalletsError

        with transaction.atomic():
            if pre_func:
                pre_func()

            transaction_obj = Transaction.objects.create(content_type_id=content_type_id, object_id=object_id)

            # withdraw from source wallet
            is_withdrawn = Wallet.objects.filter(id=source_wallet.id, balance__gte=amount).update(
                balance=models.F("balance") - amount
            )
            if is_withdrawn != 1:
                raise SourceWalletNotEnoughBalanceError

            # Deposit to destination wallet
            is_deposit = Wallet.objects.filter(id=destination_wallet.id).update(balance=models.F("balance") + amount)
            if is_deposit != 1:
                raise DestinationWalletDoesNotExistError

            Action.objects.create(
                transaction=transaction_obj,
                wallet=source_wallet,
                amount=-amount,
                type=ActionChoices.w2w,
                description=constans.DESCRIPTION_W2W.format(
                    source=source_wallet.owner.username, destination=destination_wallet.owner.username
                ),
            )
            Action.objects.create(
                transaction=transaction_obj,
                wallet=destination_wallet,
                amount=amount,
                type=ActionChoices.w2w,
                description=constans.DESCRIPTION_W2W.format(
                    source=source_wallet.owner.username, destination=destination_wallet.owner.username
                ),
            )
            source_wallet.balance -= amount
            destination_wallet.balance += amount
            if post_func:
                post_func()

        return transaction_obj


class Action(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="actions")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="actions")
    amount = models.IntegerField()
    io = models.BooleanField(default=None)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    action_type = models.IntegerField(choices=ActionChoices.choices, default=None)

    def save(self, *args, **kwargs):
        # Set io based on the sign of the amount
        self.io = self.amount >= 0
        super().save(*args, **kwargs)



    class Meta:
        ordering = ["-id"]
