# Generated by Django 2.1.2 on 2018-12-09 21:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('breeds', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('provinces', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('phone', models.CharField(help_text='Requerido. Patrón de 9 dígitos.', max_length=9, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{9})$')])),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('people', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('userAccount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User Account')),
            ],
            options={
                'verbose_name': 'Actor',
                'verbose_name_plural': 'Actores',
            },
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('centerName', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50, unique=True)),
                ('address', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50)),
                ('postalCode', models.CharField(help_text='Requerido. 5 dígitos como máximo.', max_length=5, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{5})$')], verbose_name='Código postal')),
                ('cif', models.CharField(help_text='Requerido. CIF para asociaciones. Empieza por G, seguido de 8 dígitos', max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='El código de identificación debe estar compuesto de 9 dígitos.', regex='^([G]{1})(\\d{8})$')], verbose_name='CIF or Center Code')),
                ('opening', models.TimeField()),
                ('closing', models.TimeField()),
                ('private', models.BooleanField(default=True)),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='provinces.Province')),
            ],
            options={
                'verbose_name': 'Asociación',
                'verbose_name_plural': 'Asociaciones',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Breeder',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('centerName', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50, unique=True)),
                ('address', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50)),
                ('postalCode', models.CharField(help_text='Requerido. 5 dígitos como máximo.', max_length=5, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{5})$')], verbose_name='Postal Code')),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
                ('opening', models.TimeField()),
                ('closing', models.TimeField()),
                ('private', models.BooleanField(default=True)),
                ('breeds', models.ManyToManyField(to='breeds.Breed')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='provinces.Province')),
            ],
            options={
                'verbose_name': 'Criador',
                'verbose_name_plural': 'Criadores',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            bases=('actors.actor',),
        ),
    ]
