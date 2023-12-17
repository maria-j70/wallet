from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["id", "first_name", "last_name"]
