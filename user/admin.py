from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    def get_fieldsets(self, request, obj=None):
        field_sets = super().get_fieldsets(request=request, obj=obj)
        scopes_field = [(_("Scope"), {
            "fields": ["scopes"]
        })]
        config_field = [(_("Config"), {
            "fields": ["config"]
        })]

        field_sets = list(field_sets) + scopes_field + config_field
        return field_sets
