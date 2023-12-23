# Generated by Django 4.2.5 on 2023-12-23 20:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transaction", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="action",
            name="type",
        ),
        migrations.AddField(
            model_name="action",
            name="action_type",
            field=models.IntegerField(choices=[(0, "W2W"), (1, "Deposit"), (2, "Withdrew"), (3, "Wage")], default=None),
        ),
        migrations.AddField(
            model_name="action",
            name="io",
            field=models.BooleanField(default=None),
        ),
    ]
