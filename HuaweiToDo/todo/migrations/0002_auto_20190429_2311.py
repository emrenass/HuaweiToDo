# Generated by Django 2.2 on 2019-04-29 23:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 29, 23, 11, 4, 559418)),
        ),
        migrations.AlterField(
            model_name='todo',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 29, 23, 11, 4, 559440)),
        ),
    ]
