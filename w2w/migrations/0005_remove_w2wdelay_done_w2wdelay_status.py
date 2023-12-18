# Generated by Django 4.2.5 on 2023-12-10 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("w2w", "0004_w2wdelay_done"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="w2wdelay",
            name="done",
        ),
        migrations.AddField(
            model_name="w2wdelay",
            name="status",
            field=models.IntegerField(choices=[(0, "Pending"), (1, "In Progress"), (2, "Done")], default=0),
        ),
    ]