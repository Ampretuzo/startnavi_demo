# Generated by Django 2.1.7 on 2019-03-22 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("medium", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
            options={"db_table": "medium_post_like"},
        ),
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=256)),
                ("text", models.TextField()),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={"db_table": "medium_post"},
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "medium_user_profile"},
        ),
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="medium.UserProfile"
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="medium.Post"
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="user_profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="medium.UserProfile"
            ),
        ),
    ]
