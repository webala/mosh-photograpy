# Generated by Django 4.1.1 on 2022-09-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_rename_flename_galleryimage_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='download_url',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
