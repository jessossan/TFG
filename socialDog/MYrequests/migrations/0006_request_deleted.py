# Generated by Django 2.1.2 on 2019-02-05 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MYrequests', '0005_request_copy'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
