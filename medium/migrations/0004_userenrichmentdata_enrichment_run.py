# Generated by Django 2.1.7 on 2019-03-23 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("medium", "0003_auto_20190322_1638")]

    operations = [
        migrations.AddField(
            model_name="userenrichmentdata",
            name="enrichment_run",
            field=models.BooleanField(default=False),
        )
    ]
