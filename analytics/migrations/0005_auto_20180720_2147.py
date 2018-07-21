# Generated by Django 2.0.6 on 2018-07-21 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_vendor'),
        ('analytics', '0004_auto_20180720_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booksalesreport',
            name='book',
        ),
        migrations.AddField(
            model_name='booksalesreport',
            name='book',
            field=models.ManyToManyField(blank=True, to='books.Book'),
        ),
        migrations.RemoveField(
            model_name='publishersalesreport',
            name='publisher',
        ),
        migrations.AddField(
            model_name='publishersalesreport',
            name='publisher',
            field=models.ManyToManyField(blank=True, to='books.Book'),
        ),
    ]