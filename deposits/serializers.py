from rest_framework import serializers
from .models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["id", "created_at", "tracker_id", "amount", "wallet"]
        read_only_fields = ["id"]
