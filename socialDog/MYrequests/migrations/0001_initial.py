# Generated by Django 2.1.2 on 2018-12-09 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptada', 'Aceptada'), ('Denegada', 'Denegada')], default='Pendiente', max_length=10)),
                ('description', models.CharField(help_text='Requerido. 200 carácteres como máximo', max_length=200)),
            ],
            options={
                'verbose_name': 'Petición',
                'verbose_name_plural': 'Peticiones',
            },
        ),
    ]
