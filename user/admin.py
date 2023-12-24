from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_filter = ["username", "config"]
    list_display = ["username", "first_name", "last_name", "config", "email"]
