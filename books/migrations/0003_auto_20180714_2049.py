# Generated by Django 2.0.6 on 2018-07-15 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_promotioncodes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotioncodes',
            old_name='genre',
            new_name='genres',
        ),
    ]
