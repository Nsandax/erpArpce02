from django.conf.urls import include, url
from . import views
urlpatterns = [
        url(r'^$', views.get_index, name='module_contrat_index'),
        url(r'^tableau', views.get_index, name='module_contrat_index'),
        ]

urlpatterns.append(url(r'^marche/list/(?P<ref>[0-9]+)/', views.get_lister_avis_appel_offre, name = 'module_contrat_list_avis_appel_offre'))

urlpatterns.append(url(r'^avis_appel_offre/list', views.get_lister_avis_appel_offre, name = 'module_contrat_list_avis_appel_offre'))

#Regex [0-9 ]* rendant possible la passation d'une URL qui peut prendre un chiffre ou pas
urlpatterns.append(url(r'^avis_appel_offre/add/(?P<ref>[0-9]*)', views.get_creer_avis_appel_offre, name = 'module_contrat_add_avis_appel_offre'))

urlpatterns.append(url(r'^avis_appel_offre/post_add', views.post_creer_avis_appel_offre, name = 'module_contrat_post_add_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/item/(?P<ref>[0-9]+)/$', views.get_details_avis_appel_offre, name = 'module_contrat_detail_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/item/post_update/$', views.post_modifier_avis_appel_offre, name = 'module_contrat_post_update_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/item/(?P<ref>[0-9]+)/update$', views.get_modifier_avis_appel_offre, name = 'module_contrat_update_avis_appel_offre'))


urlpatterns.append(url(r'^marche/travaux/list', views.get_lister_marche_travaux, name = 'module_contrat_list_marche_travaux'))
urlpatterns.append(url(r'^marche/fournitures/list', views.get_lister_marche_fournitures, name = 'module_contrat_list_marche_fournitures'))
urlpatterns.append(url(r'^marche/prestations/list', views.get_lister_marche_prestations, name = 'module_contrat_list_marche_prestations'))
urlpatterns.append(url(r'^marche/services/list', views.get_lister_marche_services, name = 'module_contrat_list_marche_services'))

urlpatterns.append(url(r'^contrat/cotation/add', views.get_creer_contrat_from_demande_cotation, name = 'module_contrat_add_contrat_from_demande_cotation'))
urlpatterns.append(url(r'^appel_offre/cotation/add', views.get_creer_contrat_from_appel_offre, name = 'module_contrat_add_contrat_from_appel_offre'))

#GRE A GRE
urlpatterns.append(url(r'^gre_gre/list', views.get_lister_gre_a_gre, name = 'module_contrat_lister_gre_a_gre'))
urlpatterns.append(url(r'^gre_gre/add/(?P<ref>[0-9]*)', views.get_creer_gre_a_gre, name = 'module_contrat_add_gre_a_gre'))
urlpatterns.append(url(r'^gre_gre/post_add', views.post_creer_gre_a_gre, name = 'module_contrat_post_add_gre_a_gre'))
urlpatterns.append(url(r'^gre_gre/item/(?P<ref>[0-9]+)/$', views.get_details_gre_a_gre, name = 'module_contrat_detail_gre_a_gre'))
urlpatterns.append(url(r'^gre_gre/item/post_update/$', views.post_modifier_gre_a_gre, name = 'module_contrat_post_update_gre_a_gre'))
urlpatterns.append(url(r'^gre_gre/item/(?P<ref>[0-9]+)/update$', views.get_modifier_gre_a_gre, name = 'module_contrat_update_gre_a_gre'))



urlpatterns.append(url(r'^typemarche/list', views.get_lister_typemarche, name = 'module_contrat_list_typemarche'))
urlpatterns.append(url(r'^typemarche/add', views.get_creer_typemarche, name = 'module_contrat_add_typemarche'))
urlpatterns.append(url(r'^typemarche/post_add', views.post_creer_typemarche, name = 'module_contrat_post_add_typemarche'))
urlpatterns.append(url(r'^typemarche/item/(?P<ref>[0-9]+)/$', views.get_details_typemarche, name = 'module_contrat_detail_typemarche'))
urlpatterns.append(url(r'^typemarche/item/post_update/$', views.post_modifier_typemarche, name = 'module_contrat_post_update_typemarche'))
urlpatterns.append(url(r'^typemarche/item/(?P<ref>[0-9]+)/update$', views.get_modifier_typemarche, name = 'module_contrat_update_typemarche'))
urlpatterns.append(url(r'^lettre_commande/list', views.get_lister_lettre_commande, name = 'module_contrat_list_lettre_commande'))

#Regex [0-9 ]* rendant possible la passation d'une URL qui peut prendre un chiffre ou pas
urlpatterns.append(url(r'^lettre_commande/add/(?P<ref>[0-9]*)', views.get_creer_lettre_commande, name = 'module_contrat_add_lettre_commande'))

urlpatterns.append(url(r'^lettre_commande/post_add', views.post_creer_lettre_commande, name = 'module_contrat_post_add_lettre_commande'))
urlpatterns.append(url(r'^lettre_commande/item/(?P<ref>[0-9]+)/$', views.get_details_lettre_commande, name = 'module_contrat_detail_lettre_commande'))
urlpatterns.append(url(r'^lettre_commande/item/post_update/$', views.post_modifier_lettre_commande, name = 'module_contrat_post_update_lettre_commande'))
urlpatterns.append(url(r'^lettre_commande/item/(?P<ref>[0-9]+)/update$', views.get_modifier_lettre_commande, name = 'module_contrat_update_lettre_commande'))
urlpatterns.append(url(r'^demande_cotation/list', views.get_lister_demande_cotation, name = 'module_contrat_list_demande_cotation'))

#Regex [0-9 ]* rendant possible la passation d'une URL qui peut prendre un chiffre ou pas
urlpatterns.append(url(r'^demande_cotation/add/(?P<ref>[0-9]*)', views.get_creer_demande_cotation, name = 'module_contrat_add_demande_cotation'))

urlpatterns.append(url(r'^demande_cotation/post_add', views.post_creer_demande_cotation, name = 'module_contrat_post_add_demande_cotation'))
urlpatterns.append(url(r'^demande_cotation/item/(?P<ref>[0-9]+)/$', views.get_details_demande_cotation, name = 'module_contrat_detail_demande_cotation'))
urlpatterns.append(url(r'^demande_cotation/item/post_update/$', views.post_modifier_demande_cotation, name = 'module_contrat_post_update_demande_cotation'))
urlpatterns.append(url(r'^demande_cotation/item/(?P<ref>[0-9]+)/update$', views.get_modifier_demande_cotation, name = 'module_contrat_update_demande_cotation'))
urlpatterns.append(url(r'^contrat/list', views.get_lister_contrat, name = 'module_contrat_list_contrat'))
urlpatterns.append(url(r'^contrat/marche/(?P<ref>[0-9]+)', views.get_lister_contrat, name = 'module_contrat_list_contrat_marche'))
urlpatterns.append(url(r'^contrat/add', views.get_creer_contrat, name = 'module_contrat_add_contrat'))
urlpatterns.append(url(r'^contrat/garantie_exect/list', views.get_lister_contrat_garantie, name = 'module_contrat_list_contrat_garantie_exect'))
urlpatterns.append(url(r'^contrat/reception_pro/list', views.get_lister_contrat_rec_pro, name = 'module_contrat_get_lister_contrat_rec_pro'))
urlpatterns.append(url(r'^contrat/recption_def/list', views.get_lister_contrat_recep_def, name = 'module_contrat_get_lister_contrat_recep_def'))


urlpatterns.append(url(r'^contrat/post_add', views.post_creer_contrat, name = 'module_contrat_post_add_contrat'))
urlpatterns.append(url(r'^contrat/item/(?P<ref>[0-9]+)/$', views.get_details_contrat, name = 'module_contrat_detail_contrat'))
urlpatterns.append(url(r'^contrat/item/post_update/$', views.post_modifier_contrat, name = 'module_contrat_post_update_contrat'))
urlpatterns.append(url(r'^contrat/item/(?P<ref>[0-9]+)/update$', views.get_modifier_contrat, name = 'module_contrat_update_contrat'))

urlpatterns.append(url(r'^operation_contrat/post_add', views.post_creer_operation_contrat, name = 'module_contrat_post_add_operation_contrat'))


#MODEL DOCUMENT
urlpatterns.append(url(r'^lettrecomande/modelprint', views.get_modelprint_lettrecomande, name = 'module_achat_modelprint_lettrecomande'))
urlpatterns.append(url(r'^avis_appel_offre/modelprint', views.get_modelprint_appel_offre, name = 'module_achat_modelprint_avis_appel_offre'))
urlpatterns.append(url(r'^demande_cotation/modelprint', views.get_modelprint_demande_cotation, name = 'module_achat_modelprint_demande_cotation'))
urlpatterns.append(url(r'^pv/modelprint', views.get_modelprint_pv, name = 'module_achat_modelprint_pv'))