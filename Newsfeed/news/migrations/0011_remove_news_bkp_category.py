# Generated by Django 3.2.13 on 2022-06-07 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20220607_0655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='bkp_category',
        ),
    ]