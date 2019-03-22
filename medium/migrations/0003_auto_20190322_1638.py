# Generated by Django 2.1.7 on 2019-03-22 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("medium", "0002_auto_20190322_0620")]

    operations = [
        migrations.CreateModel(
            name="UserEnrichmentData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=256)),
                ("last_name", models.CharField(max_length=256)),
                ("country", models.CharField(max_length=256)),
                ("company_clearbit_id", models.CharField(max_length=64)),
                ("company_name", models.CharField(max_length=256)),
                ("company_legal_name", models.CharField(max_length=256)),
                ("company_domain", models.CharField(max_length=256)),
                ("company_employees_range", models.CharField(max_length=256)),
            ],
            options={"db_table": "medium_user_enrichment_data"},
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
        migrations.AddField(
            model_name="userenrichmentdata",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
