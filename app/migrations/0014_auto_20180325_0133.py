# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_diary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='f_end',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='diary',
            name='f_start',
            field=models.CharField(max_length=150),
        ),
    ]