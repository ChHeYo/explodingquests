# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-10 02:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0005_auto_20170909_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='explosion_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 11, 2, 14, 37, 757614, tzinfo=utc)),
        ),
    ]
