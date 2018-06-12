# Generated by Django 2.0.6 on 2018-06-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_vendor_actual'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='primary_address',
            field=models.CharField(default='No Address', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
