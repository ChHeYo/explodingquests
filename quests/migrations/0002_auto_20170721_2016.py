# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-22 00:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quest',
            name='date_modified',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='difficulty',
        ),
    ]