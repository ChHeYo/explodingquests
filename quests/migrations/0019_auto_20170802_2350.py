# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-03 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0018_quest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='explosion_date',
            field=models.DateField(),
        ),
    ]
