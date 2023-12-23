from django.contrib import admin
from .models import Transaction, Action

# Register your models here.


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["created_at", "content_type"]


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_filter = ["wallet"]
    list_display = ["transaction", "wallet", "amount", "action_type", "created_at"]
