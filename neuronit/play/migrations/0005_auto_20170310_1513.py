# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-10 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0004_auto_20170310_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_inform',
            field=models.CharField(max_length=200),
        ),
    ]
