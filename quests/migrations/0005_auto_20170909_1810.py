# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 22:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0004_auto_20170908_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='explosion_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 10, 22, 10, 8, 451726, tzinfo=utc)),
        ),
    ]
