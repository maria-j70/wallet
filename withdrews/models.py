from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from utils.base_moldel import FeaturesStatus, Features
from wallet_app.models import Wallet
from utils.internal_exceptions import TrackerIdDuplicatedError
from django.db.utils import IntegrityError

User = get_user_model()


class Withdrew(Features):
    ACTIVE_SINGLE_EXECUTION = True
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now=True)
    tracker_id = models.CharField(max_length=255, null=True, default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=FeaturesStatus.pending, choices=FeaturesStatus.choices)
    reject_status = models.IntegerField(default=None, null=True)
    reject_description = models.CharField(max_length=1000, null=True, default=None)

    def get_destination_wallet(self):
        return Wallet.objects.get(owner__username="system")

    def get_source_wallet(self):
        return self.wallet

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["tracker_id"],
                name="unique_tracker_id_withdraw",
            ),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        except IntegrityError as e:
            if self.__class__.objects.filter(tracker_id=self.tracker_id).exists():
                raise TrackerIdDuplicatedError from None
            raise e
