# Generated by Django 2.0 on 2018-09-14 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180911_1319'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='accountnumber',
            unique_together={('entry_type', 'gst_status')},
        ),
    ]