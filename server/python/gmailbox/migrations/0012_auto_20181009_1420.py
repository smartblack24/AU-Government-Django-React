# Generated by Django 2.0 on 2018-10-09 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmailbox', '0011_auto_20180928_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
