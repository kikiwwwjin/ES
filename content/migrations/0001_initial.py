# Generated by Django 4.1 on 2023-08-08 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Model_result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hashcode", models.TextField()),
                ("title", models.TextField()),
                ("option_name", models.TextField()),
                ("manufacturer", models.TextField()),
                ("brand", models.TextField()),
                ("model_name", models.TextField()),
                ("unit_count", models.TextField()),
            ],
        ),
    ]
