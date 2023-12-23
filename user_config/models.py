from django.db import models

# Create your models here.


class UserConfig(models.Model):
    wage_rate = models.FloatField(default=0)


class Config(models.Model):
    wage_rate = models.FloatField(default=0)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.default:
            # Set all other instances' default to False
            Config.objects.exclude(pk=self.pk).update(default=False)

        super().save(*args, **kwargs)

