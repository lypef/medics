# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-27 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_properties'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='r_social',
            field=models.CharField(default=0, max_length=600),
            preserve_default=False,
        ),
    ]