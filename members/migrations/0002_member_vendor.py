# Generated by Django 2.0.6 on 2018-07-21 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.Vendor'),
        ),
    ]