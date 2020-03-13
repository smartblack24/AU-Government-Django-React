# Generated by Django 2.0 on 2018-09-27 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gmailbox', '0010_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='mail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attachments', to='gmailbox.Mail'),
        ),
    ]
