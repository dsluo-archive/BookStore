# Generated by Django 2.0.6 on 2018-07-21 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20180720_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lowinvreport',
            name='date',
        ),
        migrations.AlterField(
            model_name='publishersalesreport',
            name='publisher',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='books.Book'),
        ),
    ]
