# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-29 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0010_bestscore_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reseau',
            name='input',
        ),
        migrations.AddField(
            model_name='reseau',
            name='defeat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reseau',
            name='victory',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reseau',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reseau',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
