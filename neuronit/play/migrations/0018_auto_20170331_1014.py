# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-31 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='reseau',
            name='network_layers',
            field=models.CharField(blank=True, help_text=b'x,x,..x please', max_length=20, null=True, verbose_name=b'hidden_layers'),
        ),
        migrations.AlterField(
            model_name='reseau',
            name='defeat',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'defeat_punishement'),
        ),
        migrations.AlterField(
            model_name='reseau',
            name='victory',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'victory_reward'),
        ),
        migrations.AlterField(
            model_name='reseau',
            name='weight',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'weight_scaling'),
        ),
    ]
