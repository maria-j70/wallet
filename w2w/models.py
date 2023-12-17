from django.contrib.auth import get_user_model

from django.db import models

from utils.base_moldel import Features, FeaturesStatus
from wallet_app.models import Wallet

User = get_user_model()


class W2W(Features):
    ACTIVE_SINGLE_EXECUTION = True
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="w2ws_source")
    destination_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="w2ws_destinations")
    amount = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    tracker_id = models.CharField(max_length=255, unique=True, null=True, default=None)
    status = models.IntegerField(default=FeaturesStatus.pending, choices=FeaturesStatus.choices)

    class Meta:
        ordering = ["-id"]


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
