# Generated by Django 3.2.5 on 2022-10-26 13:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_data',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]