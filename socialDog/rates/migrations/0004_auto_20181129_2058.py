# Generated by Django 2.1.2 on 2018-11-29 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0004_dog_breeder'),
        ('news', '0003_auto_20181129_2025'),
        ('actors', '0001_initial'),
        ('events', '0004_auto_20181129_2023'),
        ('rates', '0003_rate_actor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='actor',
        ),
        migrations.AddField(
            model_name='rate',
            name='association',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='actors.Association'),
        ),
        migrations.AddField(
            model_name='rate',
            name='breeder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='actors.Breeder'),
        ),
        migrations.AddField(
            model_name='rate',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to='actors.Actor'),
        ),
        migrations.AddField(
            model_name='rate',
            name='dog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dogs.Dog'),
        ),
        migrations.AddField(
            model_name='rate',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.Event'),
        ),
        migrations.AddField(
            model_name='rate',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.News'),
        ),
    ]
