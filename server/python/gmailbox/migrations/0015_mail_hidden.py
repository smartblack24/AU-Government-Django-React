# Generated by Django 2.0 on 2019-01-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmailbox', '0014_attachment_inline'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]