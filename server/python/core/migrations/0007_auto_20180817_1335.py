# Generated by Django 2.0 on 2018-08-17 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_office_xero_branding_theme_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='xero_branding_theme_id',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='xero_branding_theme_name',
            field=models.CharField(max_length=30, null=True, blank=True, unique=True),
        ),
    ]