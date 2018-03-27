from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


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
    heredados = models.TextField()
    nopatologicos = models.TextField()
    patologicos = models.TextField()
    ginecologos = models.TextField()
    andrologicos = models.TextField()
    perinatales = models.TextField()
    quirurgicos = models.TextField()
    alergias = models.TextField()
    observaciones = models.TextField()

class Procedure (models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    agendar = models.BooleanField(default=False)

class receta (models.Model):
    patient = models.ForeignKey(patients)
    edad = models.CharField(max_length=150)
    temperatura = models.CharField(max_length=150)
    peso = models.CharField(max_length=150)
    estatura = models.CharField(max_length=150)
    presion_arterial = models.CharField(max_length=150)
    talla = models.CharField(max_length=150)
    imc = models.CharField(max_length=150)
    cabeza = models.TextField()
    torax = models.TextField()
    abdomen = models.TextField()
    genitales = models.TextField()
    piel = models.TextField()
    diagnostico = models.TextField()
    pronostico = models.TextField()
    terapeuticas = models.TextField()
    f_consulta = models.DateTimeField()
    user = models.ForeignKey(User)
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

class receta_procedures (models.Model):
    receta = models.ForeignKey(receta)
    procedure = models.ForeignKey(Procedure)
    costo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

class diary (models.Model):
    patient = models.ForeignKey(patients)
    receta = models.CharField(max_length=150)
    f_start = models.CharField(max_length=150)

class properties (models.Model):
    direccion = models.CharField(max_length=600)
    correo = models.CharField(max_length=600)
    telefono = models.CharField(max_length=600)
    facebook = models.CharField(max_length=600)
    twitter = models.CharField(max_length=600)
    youtube = models.CharField(max_length=600)
    lema = models.CharField(max_length=600)
