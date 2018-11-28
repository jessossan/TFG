# Generated by Django 2.1.2 on 2018-11-27 18:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_auto_20181125_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='age',
            field=models.PositiveIntegerField(default=0, help_text='Edad, requerido', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='dog',
            name='awards',
            field=models.CharField(blank=True, help_text='Premios, no requerido', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dog',
            name='descendant',
            field=models.CharField(blank=True, help_text='Descendencia, no requerido', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dog',
            name='details',
            field=models.CharField(blank=True, help_text='Detalles, no requerido', max_length=200, null=True),
        ),
    ]
