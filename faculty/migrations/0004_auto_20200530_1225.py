# Generated by Django 3.0.5 on 2020-05-30 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0003_schedule_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]
