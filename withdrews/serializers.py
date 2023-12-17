from rest_framework import serializers
from .models import Withdrew


class WithdrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrew
        fields = ["id", "created_at", "tracker_id", "amount", "wallet"]
        read_only_fields = ["id"]
