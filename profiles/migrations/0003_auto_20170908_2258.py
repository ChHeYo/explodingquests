# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_defusemessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='defusemessage',
            name='trash_by_receiver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='defusemessage',
            name='trash_by_sender',
            field=models.BooleanField(default=False),
        ),
    ]
