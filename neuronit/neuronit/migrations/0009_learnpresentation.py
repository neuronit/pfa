# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-31 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neuronit', '0008_auto_20170331_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnPresentation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]