# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-29 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0012_auto_20170329_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='reseau',
            name='info',
            field=models.CharField(default=b'toto', max_length=300),
        ),
    ]
