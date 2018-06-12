# Generated by Django 2.0.4 on 2018-06-11 23:19

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
            name='vendor_actual',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor'),
        ),
    ]