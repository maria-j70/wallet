from django.contrib.auth.models import AbstractUser
from django.db import models

from scopes.models import Scope
from user_config.models import Config


class User(AbstractUser):
    config = models.ForeignKey(Config, on_delete=models.CASCADE, null=True, blank=True)
    scopes = models.ManyToManyField(Scope)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.config:
            self.config = Config.objects.filter(default=True).first()

        if update_fields:
            update_fields = [i for i in update_fields] + ["config"]
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
