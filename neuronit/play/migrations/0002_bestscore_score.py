# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-10 14:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=200)),
                ('game_name', models.CharField(max_length=200)),
                ('best_score', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=200)),
                ('game_name', models.CharField(max_length=200)),
                ('score', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
        ),
    ]
