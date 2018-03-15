# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class medics(models.Model): 
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=254) 
    name = models.CharField(max_length=60) 
    telefono = models.CharField(max_length=60) 
    movil = models.CharField(max_length=60) 
    email = models.EmailField()