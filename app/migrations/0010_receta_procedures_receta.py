# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_receta_procedures'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta_procedures',
            name='receta',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.receta'),
            preserve_default=False,
        ),
    ]
