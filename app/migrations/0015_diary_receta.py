# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-25 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180325_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='receta',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.receta'),
            preserve_default=False,
        ),
    ]
