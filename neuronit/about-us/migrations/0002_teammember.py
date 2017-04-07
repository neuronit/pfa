# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-24 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about-us', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=b'')),
                ('title', models.CharField(max_length=200)),
                ('description_text', models.TextField()),
            ],
        ),
    ]
