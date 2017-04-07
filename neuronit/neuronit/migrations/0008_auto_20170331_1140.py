# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-31 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neuronit', '0007_auto_20170324_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(blank=True, null=True)),
                ('link', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='carousel',
            name='intro_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
