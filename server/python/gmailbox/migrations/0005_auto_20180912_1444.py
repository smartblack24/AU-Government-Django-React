# Generated by Django 2.0 on 2018-09-12 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gmailbox', '0004_auto_20180911_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='contact',
            new_name='contacts',
        ),
        migrations.RenameField(
            model_name='mail',
            old_name='organisation',
            new_name='organisations',
        ),
    ]
