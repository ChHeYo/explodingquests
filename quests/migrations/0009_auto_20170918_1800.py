# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 22:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0008_auto_20170910_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='explosion_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 19, 22, 0, 53, 466532, tzinfo=utc)),
        ),
    ]
