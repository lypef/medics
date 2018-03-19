# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class patients (models.Model):
    expediente = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    a_paterno = models.CharField(max_length=150)
    a_materno = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)
    celular = models.CharField(max_length=150)
    f_nacimiento = models.DateField(null=True)
    sexo = models.CharField(max_length=150)
    e_civil = models.CharField(max_length=150)
    ocupacion = models.CharField(max_length=150)
    religion = models.CharField(max_length=150)
    tipo_sanguinio = models.CharField(max_length=150)
    domicilio = models.CharField(max_length=150)
    colonia = models.CharField(max_length=150)
    cp = models.CharField(max_length=150)
    mail = models.EmailField()
    estado = models.CharField(max_length=150)
    municipio = models.CharField(max_length=150)