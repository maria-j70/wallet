from django.contrib.auth.models import  AbstractUser
from django.db import models
from user_config.models import Config


class User(AbstractUser):
    config = models.ForeignKey(Config, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.config:
            self.config = Config.objects.filter(default=True).first()

        super().save(*args, **kwargs)

