# Generated by Django 2.2 on 2019-05-01 20:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20190429_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 1, 20, 51, 48, 100814)),
        ),
        migrations.AlterField(
            model_name='todo',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 1, 20, 51, 48, 100849)),
        ),
    ]
