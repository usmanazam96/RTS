# Generated by Django 2.2.7 on 2020-06-13 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0002_auto_20200613_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting_detail',
            old_name='detail_type',
            new_name='owner_type',
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_status',
            field=models.CharField(choices=[('approve', 'Approve'), ('cancel', 'Cancel'), ('re_scheduled', 'Re Schedule'), ('complete', 'Complete'), ('request', 'Request'), ('system_cancel', 'Canceled by System')], max_length=20),
        ),
    ]