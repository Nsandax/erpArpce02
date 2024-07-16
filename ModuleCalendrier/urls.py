from django.conf.urls import include, url, handler404, handler500
from . import views
from rest_framework import routers

urlpatterns=[]
# EVENEMENT URLS
urlpatterns.append(url(r'^evenement/list', views.get_lister_evenement, name = 'module_calendrier_list_evenement'))
urlpatterns.append(url(r'^evenement/add', views.get_creer_evenement, name = 'module_calendrier_add_evenement'))
urlpatterns.append(url(r'^evenement/item/(?P<ref>[0-9]+)/$', views.get_details_evenement, name = 'module_calendrier_details_evenement'))
urlpatterns.append(url(r'^evenement/post_add', views.post_creer_evenement, name = 'module_calendrier_post_add_evenement'))
urlpatterns.append(url(r'^evenement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_evenement, name = 'module_calendrier_update_evenement'))
urlpatterns.append(url(r'^evenement/post_update', views.post_modifier_evenement, name = 'module_calendrier_post_update_evenement'))

# TYPE EVENEMENT URLS
urlpatterns.append(url(r'^type_evenement/list', views.get_lister_type_evenement, name = 'module_calendrier_list_type_evenement'))
urlpatterns.append(url(r'^type_evenement/add', views.get_creer_type_evenement, name = 'module_calendrier_add_type_evenement'))
urlpatterns.append(url(r'^type_evenement/item/(?P<ref>[0-9]+)/$', views.get_details_type_evenement, name = 'module_calendrier_detail_type_evenement'))
urlpatterns.append(url(r'^type_evenement/post_add', views.post_creer_type_evenement, name = 'module_calendrier_post_add_type_evenement'))
urlpatterns.append(url(r'^type_evenement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_evenement, name = 'module_calendrier_update_type_evenement'))
urlpatterns.append(url(r'^type_evenement/post_update', views.post_modifier_type_evenement, name = 'module_calendrier_post_update_type_evenement'))

# ALARME URLS
urlpatterns.append(url(r'^alarme/list', views.get_lister_alarme, name = 'module_calendrier_list_alarme'))
urlpatterns.append(url(r'^alarme/add', views.get_creer_alarme, name = 'module_calendrier_add_alarme'))
urlpatterns.append(url(r'^alarme/item/(?P<ref>[0-9]+)/$', views.get_details_alarme, name = 'module_calendrier_detail_alarme'))
urlpatterns.append(url(r'^alarme/post_add', views.post_creer_alarme, name = 'module_calendrier_post_add_alarme'))
urlpatterns.append(url(r'^alarme/item/(?P<ref>[0-9]+)/update$', views.get_modifier_alarme, name = 'module_calendrier_update_alarme'))
urlpatterns.append(url(r'^alarme/post_update', views.post_modifier_alarme, name = 'module_calendrier_post_update_alarme'))