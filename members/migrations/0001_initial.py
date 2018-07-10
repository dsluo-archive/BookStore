# Generated by Django 2.0.6 on 2018-07-08 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import members.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_address', models.CharField(max_length=60)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=members.models.upload_location)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('birth_date', models.DateField(default=django.utils.timezone.now)),
                ('authentication_key', models.CharField(blank=True, max_length=8)),
                ('cart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
                ('order', models.ManyToManyField(blank=True, to='cart.Order')),
                ('purchased', models.ManyToManyField(blank=True, to='books.Book')),
                ('reserved', models.ManyToManyField(blank=True, to='books.Reservation')),
                ('saved_addresses', models.ManyToManyField(blank=True, related_name='address', to='members.Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.Vendor')),
            ],
        ),
    ]
