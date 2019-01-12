# Generated by Django 2.1.2 on 2019-01-12 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190112_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='finishTime',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='event',
            name='startTime',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='event',
            name='finishDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='startDate',
            field=models.DateField(),
        ),
    ]
