# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-31 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0014_auto_20170330_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reseau',
            name='type',
            field=models.CharField(choices=[(b'select_type', b'select_type'), (b'MLP', b'MLP'), (b'Elman', b'Elman'), (b'Jordan', b'Jordan')], default=b'select', max_length=100),
        ),
    ]
