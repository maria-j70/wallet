# Register your models here.

from django.contrib import admin

from .models import Scope


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
