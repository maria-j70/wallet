from rest_framework import serializers
from .models import Transaction, Action
from wallet_app.serializers import WalletCompleteSerializer


class ActionSerializer(serializers.ModelSerializer):
    wallet = WalletCompleteSerializer()

    class Meta:
        model = Action
        fields = ["id", "wallet", "amount", "action_type", "description", "created_at"]
        read_only_fields = ["id", "wallet", "amount", "action_type", "description", "created_at"]





class SimpleActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ["id", "wallet", "amount", "action_type", "description", "created_at"]
        read_only_fields = ["id", "wallet", "amount", "action_type", "description", "created_at", "mirror_code"]


class TransactionSerializer(serializers.ModelSerializer):
    actions = SimpleActionSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "created_at", "actions"]
        read_only_fields = ["id", "created_at"]