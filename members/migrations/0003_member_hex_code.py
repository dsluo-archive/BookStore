# Generated by Django 2.0.6 on 2018-07-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_receive_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='hex_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
