"Ejemplos: https://docs.djangoproject.com/en/1.11/topics/http/urls/"

from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/', views.login),
]
