from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from utils.base_moldel import FeaturesStatus, Features
from wallet_app.models import Wallet

User = get_user_model()


class Withdrew(Features):
    ACTIVE_SINGLE_EXECUTION = True
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now=True)
    tracker_id = models.CharField(max_length=255, unique=True, null=True, default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=FeaturesStatus.pending, choices=FeaturesStatus.choices)

    def get_destination_wallet(self):
        return Wallet.objects.get(owner__username="system")

    def get_source_wallet(self):
        return self.wallet

    class Meta:
        ordering = ["-id"]
