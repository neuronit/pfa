# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-24 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about-us', '0002_teammember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='description_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='image',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]
