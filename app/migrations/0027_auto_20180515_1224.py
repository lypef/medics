# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-15 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_receta_cintura'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='file0',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file1',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file2',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file3',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file4',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file5',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file6',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file7',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file8',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
        migrations.AddField(
            model_name='receta',
            name='file9',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
    ]