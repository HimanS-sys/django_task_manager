# Generated by Django 4.2.2 on 2023-09-13 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0007_task_version"),
    ]

    operations = [
        migrations.CreateModel(
            name="Email",
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
                ("email", models.EmailField(max_length=254)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails",
                        to="tasks.task",
                    ),
                ),
            ],
        ),
    ]
