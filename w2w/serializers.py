from rest_framework import serializers
from wallet_app.serializers import WalletCompleteSerializer
from .models import W2W, W2WDelay



class W2WModelSerializer(serializers.ModelSerializer):
    source_wallet = WalletCompleteSerializer
    destination_wallet = WalletCompleteSerializer

    class Meta:
        model = W2W
        fields = ["id", "source_wallet", "destination_wallet", "amount", "tracker_id"]


class W2WDelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = W2WDelay
        fields = ["id", "source_wallet", "destination_wallet", "amount", "tracker_id", "apply_at"]
