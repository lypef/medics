# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-15 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='medics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=60)),
                ('telefono', models.CharField(max_length=60)),
                ('movil', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
