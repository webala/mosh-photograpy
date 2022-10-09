# Generated by Django 4.1.1 on 2022-10-09 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0018_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyMessage",
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
                ("message", models.CharField(max_length=300)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "replied_message",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.message",
                    ),
                ),
            ],
        ),
    ]
