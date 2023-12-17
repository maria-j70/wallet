from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Wallet(models.Model):
    balance = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")

    class Meta:
        ordering = ["-id"]
