# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-01 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_remove_receta_indicaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='indicaciones',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
