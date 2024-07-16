from django.conf.urls import include, url
from . import views
urlpatterns = [
        url(r'^tableau', views.get_index, name='module_archivage_index'),
    url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_archivage_notification'),
        ]
 
urlpatterns.append(url(r'^tableau', views.get_index, name='module_archivage_index'))
urlpatterns.append(url(r'^doc_and_dossier_json', views.get_dossier_doc_to_dashbord, name='module_archivage_doc_dos_json'))
urlpatterns.append(url(r'^dossier/list', views.get_lister_dossier, name = 'module_archivage_list_dossier'))
urlpatterns.append(url(r'^dossier/Children/(?P<ref>[0-9]+)/$', views.get_lister_dossier_byClick, name = 'module_archivageListDossierByClick'))
urlpatterns.append(url(r'^dossier/add', views.get_creer_dossier, name = 'module_archivage_add_dossier'))
urlpatterns.append(url(r'^dossier/post_add', views.post_creer_dossier, name = 'module_archivage_post_add_dossier'))
urlpatterns.append(url(r'^dossier/item/(?P<ref>[0-9]+)/$', views.get_details_dossier, name = 'module_archivage_detail_dossier'))
urlpatterns.append(url(r'^dossier/item/post_update/$', views.post_modifier_dossier, name = 'module_archivage_post_update_dossier'))
urlpatterns.append(url(r'^dossier/item/(?P<ref>[0-9]+)/update$', views.get_modifier_dossier, name = 'module_archivage_update_dossier'))



urlpatterns.append(url(r'^document/list', views.get_lister_document, name = 'module_archivage_list_document'))
urlpatterns.append(url(r'^document/add', views.get_creer_document, name = 'module_archivage_add_document'))
urlpatterns.append(url(r'^document/post_add', views.post_creer_document, name = 'module_archivage_post_add_document'))
urlpatterns.append(url(r'^document/item/(?P<ref>[0-9]+)/$', views.get_details_document, name = 'module_archivage_detail_document'))
urlpatterns.append(url(r'^document/item/post_update/$', views.post_modifier_document, name = 'module_archivage_post_update_document'))
urlpatterns.append(url(r'^document/item/(?P<ref>[0-9]+)/update$', views.get_modifier_document, name = 'module_archivage_update_document'))
urlpatterns.append(url(r'^document/search', views.get_search, name = 'module_archivage_search_document'))
