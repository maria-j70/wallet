from django.contrib.auth import get_user_model
from django.contrib import admin
from user_config.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_filter = ['wage_rate', 'default']
    list_display = ['wage_rate', 'default']
