# Generated by Django 4.1.1 on 2022-09-09 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_galleryimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galleryimage',
            old_name='flename',
            new_name='filename',
        ),
    ]
