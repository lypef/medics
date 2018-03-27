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
    url(r'^procedures/', views.procedures),
    url(r'^procedures_edit/(?P<id>[^/]+)/$', views.procedures_Edit),
    url(r'^procedures_delete/', views.procedure_Delete),
    url(r'^consultation/', views.consultation),
    url(r'^recipe/', views.recipe),
    url(r'^recipe_history/(?P<id>[^/]+)/$', views.recipe_history),
    url(r'^diary/', views.diary_f),
    url(r'^consultation_diary/(?P<id_agenda>[^/]+)/(?P<id_paciente>[^/]+)/$', views.consultation_agenda),
    url(r'^properties_update/', views.properties_update_),
    url(r'^recipe_pdf/(?P<id>[^/]+)/$', views.recipe_receta),

]
