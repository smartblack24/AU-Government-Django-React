# Generated by Django 2.0 on 2018-09-03 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20180816_1109'),
        ('accounts', '0006_auto_20180817_1335'),
        ('gmailbox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_type', models.CharField(choices=[('Inbox', 'Inbox'), ('Sent', 'Sent'), ('Draft', 'Draft')], max_length=25)),
                ('sender', models.EmailField(max_length=254, null=True)),
                ('recipient', models.EmailField(max_length=254, null=True)),
                ('subject', models.CharField(max_length=512, null=True)),
                ('content', models.TextField(null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Contact')),
                ('matter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.Matter')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Organisation')),
            ],
        ),
        migrations.DeleteModel(
            name='Email',
        ),
        migrations.AlterField(
            model_name='gmailaccount',
            name='token',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]