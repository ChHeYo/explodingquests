# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 02:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0003_auto_20170907_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='explosion_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 10, 2, 58, 57, 393793, tzinfo=utc)),
        ),
    ]