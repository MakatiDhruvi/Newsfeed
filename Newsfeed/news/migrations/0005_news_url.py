# Generated by Django 3.2.13 on 2022-05-28 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20220527_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
