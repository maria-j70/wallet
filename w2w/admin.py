from django.contrib import admin
from .models import W2W, W2WDelay


# Register your models here.

@admin.register(W2W)
class W2WAdmin(admin.ModelAdmin):
    list_filter = ['source_wallet', 'destination_wallet', 'created_by']
    list_display = ['source_wallet', 'destination_wallet', 'amount', 'tracker_id', 'created_by', 'created_at', 'status']


@admin.register(W2WDelay)
class W2WDelayAdmin(admin.ModelAdmin):
    list_filter = ['status', 'apply_at', 'source_wallet', 'created_by']
    list_display = ['source_wallet', 'destination_wallet', 'amount', 'tracker_id', 'created_by', 'created_at',
                    'apply_at', 'status']
