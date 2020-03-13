from datetime import datetime

from django.db import migrations, models


def populate_date_time(apps, schema_editor):
    TimeEntry = apps.get_model('billing', 'TimeEntry')
    for time_entry in TimeEntry.objects.all():
        time_entry.date = datetime.combine(
            time_entry.date,
            datetime.strptime('12:00', '%H:%M').time()
            )
        time_entry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0012_merge_20181002_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeentry',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.RunPython(populate_date_time)
    ]
