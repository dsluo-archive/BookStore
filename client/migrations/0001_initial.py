# Generated by Django 2.0.4 on 2018-06-11 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analytics', '0002_auto_20180611_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_sales_report', models.ManyToManyField(blank=True, related_name='_client_book_sales_report_+', to='analytics.BookSalesReport')),
                ('end_of_day_report', models.ManyToManyField(blank=True, related_name='_client_end_of_day_report_+', to='analytics.EodReport')),
                ('low_inventory_report', models.ManyToManyField(blank=True, related_name='_client_low_inventory_report_+', to='analytics.LowInvReport')),
            ],
        ),
    ]
