# Generated by Django 3.2.5 on 2022-10-26 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0004_auto_20221025_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info_data',
            name='signature',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
