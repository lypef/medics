# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-31 05:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_diary_medic'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='share',
            field=models.BooleanField(default=False),
        ),
    ]
