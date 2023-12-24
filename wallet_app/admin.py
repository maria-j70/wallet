from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_filter = ["owner"]
    list_display = ["id", "owner", "balance", "is_deleted", "created_at", "updated_at"]
