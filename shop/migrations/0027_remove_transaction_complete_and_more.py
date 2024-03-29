# Generated by Django 4.1.1 on 2023-05-04 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0026_alter_service_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="complete",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="phone_number",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="receipt_number",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="request_id",
        ),
        migrations.RemoveField(
            model_name="transaction",
            name="viewed",
        ),
        migrations.AddField(
            model_name="transaction",
            name="confirmation_code",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="order_tracking_id",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="transaction",
            name="payment_currency",
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="payment_method",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="payment_status",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="payment_status_description",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
