"Ejemplos: https://docs.djangoproject.com/en/1.11/topics/http/urls/"

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import login
from app import views
from django.conf import settings
from django.views.static import serve

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
    url(r'^consulta_pdf/(?P<id>[^/]+)/$', views.recipe_consulta),
    url(r'^update_profile/', views.profile_update),
    url(r'^users/', views._users),
    url(r'^user_delete/', views._users_Delete),
    url(r'^user_update/', views._users_Update),
    url(r'^user_add/', views._users_Add),
    url(r'^report_procedures/', views._report_procedures),
    url(r'^report_patients/', views._report_patients),
    url(r'^report_recipes/', views._report_recipes),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    url(r'^report_heredofamiliares/(?P<id>[^/]+)/$', views.report_heredofamiliares),
    url(r'^report_datos_paciente/(?P<id>[^/]+)/$', views.report_datos_paciente),
    url(r'^delete_recipe/', views.delete_recipe),
    url(r'^delete_recipe_history/', views.delete_recipe_history),
    url(r'^shareyes_recipe/', views.shareyes_recipe),
    url(r'^shareno_recipe/', views.shareno_recipe),
    url(r'^sharesi_paciente/', views.shareyes_paciente),
    url(r'^shareno_paciente/', views.shareno_paciente),
]
