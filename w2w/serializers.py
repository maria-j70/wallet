from rest_framework import serializers
from wallet_app.serializers import WalletCompleteSerializer
from .models import W2W, W2WDelay


# class W2WSerializer(serializers.Serializer):
#     source = serializers.IntegerField(write_only=True)
#     destination = serializers.IntegerField()
#     tracker_id = serializers.CharField()
#     amount = serializers.IntegerField(min_value=1, write_only=True)
#
#     def update(self, instance, validated_data):
#         raise NotImplemented
#
#     def create(self, validated_data):
#         raise NotImplemented


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
