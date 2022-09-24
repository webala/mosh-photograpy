# Generated by Django 4.1.1 on 2022-09-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_galleryimage_download_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='name',
        ),
        migrations.AddField(
            model_name='package',
            name='category',
            field=models.CharField(blank=True, choices=[('BRONZE', 'BRONZE'), ('SILVER', 'SILVER'), ('GOLD', 'GOLD')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='nature',
            field=models.CharField(blank=True, choices=[('PHOTOGRAHY', 'PHOTOGRAHY'), ('VIDEOGRAPHY', 'VIDEOGRAPHY')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='type',
            field=models.CharField(choices=[('WEDDING', 'WEDDING'), ('PORTRAIT', 'PORTRAIT'), ('RURACIO', 'RURACIO')], default='WEDDING', max_length=10),
        ),
        migrations.DeleteModel(
            name='PackageCateagory',
        ),
    ]