# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-29 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0013_reseau_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reseau',
            name='info',
            field=models.CharField(default='toto', max_length=300),
        ),
        migrations.AlterField(
            model_name='reseau',
            name='type',
            field=models.CharField(choices=[('MLP', 'MLP'), ('Elman', 'Elman'), ('Jordan', 'Jordan')], default='MLP', max_length=100),
        ),
    ]