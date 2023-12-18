from django.contrib.auth import get_user_model
from django.db import models

from utils.base_moldel import Features, FeaturesStatus
from utils.internal_exceptions import TrackerIdDuplicatedError
from wallet_app.models import Wallet
from django.db.utils import IntegrityError
User = get_user_model()


class W2W(Features):
    ACTIVE_SINGLE_EXECUTION = True
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="w2ws_source")
    destination_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="w2ws_destinations")
    amount = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    tracker_id = models.CharField(max_length=255, null=True, default=None)
    status = models.IntegerField(default=FeaturesStatus.pending, choices=FeaturesStatus.choices)

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["tracker_id"],
                name="unique_tracker_id_w2w",
            ),
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        except IntegrityError as e:
            if self.__class__.objects.filter(tracker_id=self.tracker_id).exists():
                raise TrackerIdDuplicatedError from None
            raise e


class W2WDelay(Features):
    ACTIVE_SINGLE_EXECUTION = True
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="w2ws_delay_source")
    destination_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="w2ws_delay_destinations")
    amount = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    tracker_id = models.CharField(max_length=255, unique=True, null=True, default=None)
    apply_at = models.DateTimeField(null=False)
    status = models.IntegerField(default=FeaturesStatus.pending, choices=FeaturesStatus.choices)

    class Meta:
        ordering = ["-id"]
