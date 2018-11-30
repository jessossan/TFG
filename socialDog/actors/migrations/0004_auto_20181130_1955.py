# Generated by Django 2.1.2 on 2018-11-30 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0003_breeder_breeds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='cif',
            field=models.CharField(help_text='Requerido. CIF para escuelas; Código de Centro para academías.', max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='El código de identificación debe estar compuesto de 8 dígitos o 9 dígitos.', regex='^([G]1)(\\d{8})$')], verbose_name='CIF or Center Code'),
        ),
    ]
