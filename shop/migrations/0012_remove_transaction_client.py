# Generated by Django 4.1.1 on 2022-09-26 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0011_transaction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="client",
        ),
    ]
