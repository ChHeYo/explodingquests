# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-23 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0004_auto_20170722_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quest',
            name='explosion_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='quest',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]