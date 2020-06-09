# Generated by Django 3.0.5 on 2020-05-30 06:41

from django.db import migrations
import faculty.myFields


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0002_auto_20200529_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='day',
            field=faculty.myFields.DayOfTheWeekField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], default='1', max_length=1),
            preserve_default=False,
        ),
    ]