"Ejemplos: https://docs.djangoproject.com/en/1.11/topics/http/urls/"

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import login
from app import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^manager/', views.user_login),
    url(r'^logout/', views.user_logout),
    url(r'^patient/', views.patient),
    url(r'^patient_edit/(?P<id>[^/]+)/$', views.patient_Edit),
    url(r'^patient_delete/', views.patient_Delete),
]
