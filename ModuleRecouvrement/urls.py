from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.get_index, name='module_recouvrement_index'),
    url(r'^tableau', views.get_index, name='module_recouvrement_tableau_de_bord'),
]
    
#DOSSIER_RECOUVREMENT URLS
#=====================================
#DOSSIER_RECOUVREMENT CRUD URLS
urlpatterns.append(url(r'^dossier_recouvrement/list', views.get_lister_dossier_recouvrement, name = 'module_recouvrement_list_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/add', views.get_creer_dossier_recouvrement, name = 'module_recouvrement_add_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/post_add', views.post_creer_dossier_recouvrement, name = 'module_recouvrement_post_add_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/item/(?P<ref>[0-9]+)/$', views.get_details_dossier_recouvrement, name = 'module_recouvrement_detail_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/item/post_update/$', views.post_modifier_dossier_recouvrement, name = 'module_recouvrement_post_update_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_dossier_recouvrement, name = 'module_recouvrement_update_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_dossier_recouvrement, name = 'module_recouvrement_duplicate_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_dossier_recouvrement, name = 'module_recouvrement_print_dossier_recouvrement'))
#DOSSIER_RECOUVREMENT UPLOAD URLS
urlpatterns.append(url(r'^dossier_recouvrement/upload/add', views.get_upload_dossier_recouvrement, name = 'module_recouvrement_get_upload_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/upload/post_add', views.post_upload_dossier_recouvrement, name = 'module_recouvrement_post_upload_dossier_recouvrement'))

#DOSSIER_RECOUVREMENT REPORTING URLS
urlpatterns.append(url(r'^dossier_recouvrement/generate', views.get_generer_dossier_recouvrement, name = 'module_recouvrement_get_generer_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/post_generate', views.post_generer_dossier_recouvrement, name = 'module_recouvrement_post_generer_dossier_recouvrement'))
urlpatterns.append(url(r'^dossier_recouvrement/print_generate', views.post_imprimer_rapport_dossier_recouvrement, name = 'module_recouvrement_post_imprimer_rapport_dossier_recouvrement'))

#DOSSIER_RECOUVREMENT API URLS
urlpatterns.append(url(r'^api/dossier_recouvrement/list', views.get_list_dossier_recouvrement, name = 'module_recouvrement_api_list_dossier_recouvrement'))
urlpatterns.append(url(r'^api/dossier_recouvrement/item', views.get_item_dossier_recouvrement, name = 'module_recouvrement_api_item_dossier_recouvrement'))
urlpatterns.append(url(r'^api/dossier_recouvrement/create', views.post_create_dossier_recouvrement, name = 'module_recouvrement_api_create_dossier_recouvrement'))

#SCENARIO_RELANCE URLS
#=====================================
#SCENARIO_RELANCE CRUD URLS
urlpatterns.append(url(r'^scenario_relance/list', views.get_lister_scenario_relance, name = 'module_recouvrement_list_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/add', views.get_creer_scenario_relance, name = 'module_recouvrement_add_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/post_add', views.post_creer_scenario_relance, name = 'module_recouvrement_post_add_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/item/(?P<ref>[0-9]+)/$', views.get_details_scenario_relance, name = 'module_recouvrement_detail_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/item/post_update/$', views.post_modifier_scenario_relance, name = 'module_recouvrement_post_update_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/item/(?P<ref>[0-9]+)/update$', views.get_modifier_scenario_relance, name = 'module_recouvrement_update_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_scenario_relance, name = 'module_recouvrement_duplicate_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_scenario_relance, name = 'module_recouvrement_print_scenario_relance'))
#SCENARIO_RELANCE UPLOAD URLS
urlpatterns.append(url(r'^scenario_relance/upload/add', views.get_upload_scenario_relance, name = 'module_recouvrement_get_upload_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/upload/post_add', views.post_upload_scenario_relance, name = 'module_recouvrement_post_upload_scenario_relance'))

#SCENARIO_RELANCE REPORTING URLS
urlpatterns.append(url(r'^scenario_relance/generate', views.get_generer_scenario_relance, name = 'module_recouvrement_get_generer_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/post_generate', views.post_generer_scenario_relance, name = 'module_recouvrement_post_generer_scenario_relance'))
urlpatterns.append(url(r'^scenario_relance/print_generate', views.post_imprimer_rapport_scenario_relance, name = 'module_recouvrement_post_imprimer_rapport_scenario_relance'))

#ACTION_SCENARIO URLS
#=====================================
#ACTION_SCENARIO CRUD URLS
urlpatterns.append(url(r'^action_scenario/list', views.get_lister_action_scenario, name = 'module_recouvrement_list_action_scenario'))
urlpatterns.append(url(r'^action_scenario/add', views.get_creer_action_scenario, name = 'module_recouvrement_add_action_scenario'))
urlpatterns.append(url(r'^action_scenario/post_add', views.post_creer_action_scenario, name = 'module_recouvrement_post_add_action_scenario'))
urlpatterns.append(url(r'^action_scenario/item/(?P<ref>[0-9]+)/$', views.get_details_action_scenario, name = 'module_recouvrement_detail_action_scenario'))
urlpatterns.append(url(r'^action_scenario/item/post_update/$', views.post_modifier_action_scenario, name = 'module_recouvrement_post_update_action_scenario'))
urlpatterns.append(url(r'^action_scenario/item/(?P<ref>[0-9]+)/update$', views.get_modifier_action_scenario, name = 'module_recouvrement_update_action_scenario'))
urlpatterns.append(url(r'^action_scenario/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_action_scenario, name = 'module_recouvrement_duplicate_action_scenario'))
urlpatterns.append(url(r'^action_scenario/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_action_scenario, name = 'module_recouvrement_print_action_scenario'))
#ACTION_SCENARIO UPLOAD URLS
urlpatterns.append(url(r'^action_scenario/upload/add', views.get_upload_action_scenario, name = 'module_recouvrement_get_upload_action_scenario'))
urlpatterns.append(url(r'^action_scenario/upload/post_add', views.post_upload_action_scenario, name = 'module_recouvrement_post_upload_action_scenario'))

#ACTION_RELANCE URLS
#=====================================
#ACTION_RELANCE CRUD URLS
urlpatterns.append(url(r'^action_relance/list', views.get_lister_action_relance, name = 'module_recouvrement_list_action_relance'))
urlpatterns.append(url(r'^action_relance/add', views.get_creer_action_relance, name = 'module_recouvrement_add_action_relance'))
urlpatterns.append(url(r'^action_relance/post_add', views.post_creer_action_relance, name = 'module_recouvrement_post_add_action_relance'))
urlpatterns.append(url(r'^action_relance/item/(?P<ref>[0-9]+)/$', views.get_details_action_relance, name = 'module_recouvrement_detail_action_relance'))
urlpatterns.append(url(r'^action_relance/item/post_update/$', views.post_modifier_action_relance, name = 'module_recouvrement_post_update_action_relance'))
urlpatterns.append(url(r'^action_relance/item/(?P<ref>[0-9]+)/update$', views.get_modifier_action_relance, name = 'module_recouvrement_update_action_relance'))
urlpatterns.append(url(r'^action_relance/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_action_relance, name = 'module_recouvrement_duplicate_action_relance'))
urlpatterns.append(url(r'^action_relance/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_action_relance, name = 'module_recouvrement_print_action_relance'))
#ACTION_RELANCE UPLOAD URLS
urlpatterns.append(url(r'^action_relance/upload/add', views.get_upload_action_relance, name = 'module_recouvrement_get_upload_action_relance'))
urlpatterns.append(url(r'^action_relance/upload/post_add', views.post_upload_action_relance, name = 'module_recouvrement_post_upload_action_relance'))

#ACTION_RELANCE REPORTING URLS
urlpatterns.append(url(r'^action_relance/generate', views.get_generer_action_relance, name = 'module_recouvrement_get_generer_action_relance'))
urlpatterns.append(url(r'^action_relance/post_generate', views.post_generer_action_relance, name = 'module_recouvrement_post_generer_action_relance'))
urlpatterns.append(url(r'^action_relance/print_generate', views.post_imprimer_rapport_action_relance, name = 'module_recouvrement_post_imprimer_rapport_action_relance'))

#SECTEUR_ACTIVITE URLS
#=====================================
#SECTEUR_ACTIVITE CRUD URLS
urlpatterns.append(url(r'^secteur_activite/list', views.get_lister_secteur_activite, name = 'module_recouvrement_list_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/add', views.get_creer_secteur_activite, name = 'module_recouvrement_add_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/post_add', views.post_creer_secteur_activite, name = 'module_recouvrement_post_add_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/item/(?P<ref>[0-9]+)/$', views.get_details_secteur_activite, name = 'module_recouvrement_detail_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/item/post_update/$', views.post_modifier_secteur_activite, name = 'module_recouvrement_post_update_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/item/(?P<ref>[0-9]+)/update$', views.get_modifier_secteur_activite, name = 'module_recouvrement_update_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_secteur_activite, name = 'module_recouvrement_duplicate_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_secteur_activite, name = 'module_recouvrement_print_secteur_activite'))
#SECTEUR_ACTIVITE UPLOAD URLS
urlpatterns.append(url(r'^secteur_activite/upload/add', views.get_upload_secteur_activite, name = 'module_recouvrement_get_upload_secteur_activite'))
urlpatterns.append(url(r'^secteur_activite/upload/post_add', views.post_upload_secteur_activite, name = 'module_recouvrement_post_upload_secteur_activite'))

#PROFIL_RECOUVREMENT URLS
#=====================================
#PROFIL_RECOUVREMENT CRUD URLS
urlpatterns.append(url(r'^profil_recouvrement/list', views.get_lister_profil_recouvrement, name = 'module_recouvrement_list_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/add', views.get_creer_profil_recouvrement, name = 'module_recouvrement_add_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/post_add', views.post_creer_profil_recouvrement, name = 'module_recouvrement_post_add_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/item/(?P<ref>[0-9]+)/$', views.get_details_profil_recouvrement, name = 'module_recouvrement_detail_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/item/post_update/$', views.post_modifier_profil_recouvrement, name = 'module_recouvrement_post_update_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_profil_recouvrement, name = 'module_recouvrement_update_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/item/(?P<ref>[0-9]+)/duplicate$', views.get_dupliquer_profil_recouvrement, name = 'module_recouvrement_duplicate_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/item/(?P<ref>[0-9]+)/print$', views.get_imprimer_profil_recouvrement, name = 'module_recouvrement_print_profil_recouvrement'))
#PROFIL_RECOUVREMENT UPLOAD URLS
urlpatterns.append(url(r'^profil_recouvrement/upload/add', views.get_upload_profil_recouvrement, name = 'module_recouvrement_get_upload_profil_recouvrement'))
urlpatterns.append(url(r'^profil_recouvrement/upload/post_add', views.post_upload_profil_recouvrement, name = 'module_recouvrement_post_upload_profil_recouvrement'))
