from rest_framework import serializers
from .models import Wallet
from user.serializers import UserSerializer, SimpleUserSerializer


class WalletCompleteSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'is_deleted', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['id', 'balance', 'is_deleted', 'created_at', 'updated_at', 'owner']


class WalletSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ['id', 'balance', 'is_deleted', 'created_at', 'updated_at']






