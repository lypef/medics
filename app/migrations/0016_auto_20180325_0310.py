# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_diary_receta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='receta',
            field=models.CharField(max_length=150),
        ),
    ]