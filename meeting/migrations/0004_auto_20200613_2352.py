# Generated by Django 2.2.7 on 2020-06-13 18:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0003_auto_20200613_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='initiate_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='meeting_detail',
            name='initiate_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='meeting_detail',
            name='meeting_status',
            field=models.CharField(choices=[('message', 'message'), ('approve', 'Approve'), ('cancel', 'Cancel'), ('re_scheduled', 'Re Schedule'), ('complete', 'Complete'), ('request', 'Request'), ('system_cancel', 'Canceled by System')], max_length=20),
        ),
        migrations.AlterField(
            model_name='meeting_detail',
            name='owner_type',
            field=models.CharField(choices=[('r', 'requester'), ('f', 'faculty'), ('s', 'System')], max_length=2),
        ),
    ]
