# Generated by Django 2.0.6 on 2018-06-16 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='vendor',
        ),
        migrations.AddField(
            model_name='member',
            name='vendor',
            field=models.ManyToManyField(blank=True, null=True, to='vendors.Vendor'),
        ),
    ]
