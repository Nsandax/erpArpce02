from django.conf.urls import include, url
from . import views


urlpatterns=[]
urlpatterns.append(url(r'^tableau', views.get_dashboard, name = 'module_inventaire_tableau_de_bord'))
urlpatterns.append(url(r'^Quantite_to_dashbord',views.get_inventer_to_dashbord, name='module_inventaire_jso_demande_fournie_de_bord'))
urlpatterns.append(url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_inventaire_notification'))


# INVENTAIRE URLS
urlpatterns.append(url(r'^bon_inventaire/list', views.get_lister_bon_inventaire, name = 'module_inventaire_list_bon_inventaire'))
urlpatterns.append(url(r'^bon_inventaire/add', views.get_creer_bon_inventaire, name = 'module_inventaire_add_bon_inventaire'))
urlpatterns.append(url(r'^bon_inventaire/validate', views.get_demarrer_bon_inventaire, name='module_inventaire_demarrer_bon_inventaire'))
urlpatterns.append(url(r'^bon_inventaire/post_add', views.post_creer_bon_inventaire, name = 'module_inventaire_post_add_bon_inventaire'))
urlpatterns.append(url(r'^bon_inventaire/item/(?P<ref>[0-9]+)/$', views.get_details_bon_inventaire, name = 'module_inventaire_detail_bon_inventaire'))
urlpatterns.append(url(r'^bon_inventaire/post_inventaire_initial', views.post_valider_inventaire_initial, name='module_inventaire_post_valider_inventaire_initial'))

# TRANSFERT URLS
urlpatterns.append(url(r'^bon_transfert/list', views.get_lister_bon_transfert, name = 'module_inventaire_list_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/add', views.get_creer_bon_transfert, name = 'module_inventaire_add_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/validate', views.get_valider_bon_transfert, name='module_inventaire_valider_bontransfert'))
urlpatterns.append(url(r'^bon_transfert/post_add', views.post_valider_bon_transfert, name = 'module_inventaire_post_valider_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/release/$', views.get_realiser_bon_transfert, name='module_inventaire_realiser_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/post_release/$', views.post_realiser_bon_transfert, name='module_inventaire_post_realiser_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/$', views.get_details_bon_transfert, name='module_inventaire_detail_bon_transfert'))

urlpatterns.append(url(r'^bon_transfert/item/(?P<ref>[0-9]+)/complete/$', views.get_completer_bon_transfert, name='module_inventaire_completer_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/post_complete/$', views.post_completer_bon_transfert, name='module_inventaire_post_completer_bon_transfert'))

urlpatterns.append(url(r'^bon_transfert/item/release_asset/$', views.get_to_asset_of_bon_transfert, name='module_inventaire_get_assetiser_bon_transfert'))
urlpatterns.append(url(r'^bon_transfert/item/post_release_asset/$', views.post_to_asset_of_bon_transfert, name='module_inventaire_post_assetiser_bon_transfert'))

urlpatterns.append(url(r'^bon_transfert/workflow_post', views.post_workflow_bon_transfert, name = 'module_inventaire_bon_transfert_workflow_post'))

# MOUVEMENTS STOCK URLS
urlpatterns.append(url(r'^mouvement_stock/list', views.get_lister_mouvement_stock, name = 'module_inventaire_list_mouvement_stock'))
urlpatterns.append(url(r'^mouvement_stock/item/(?P<ref>[0-9]+)/$', views.get_details_mouvement_stock, name = 'module_inventaire_detail_mouvement_stock'))
urlpatterns.append(url(r'^mouvements/list/item/(?P<ref>[0-9]+)/$', views.get_lister_mouvements_stock_article, name='module_inventaire_list_mouvements_stock_article'))

# ARTICLES STOCKABLES URLS
urlpatterns.append(url(r'^article/list', views.get_lister_articles_stockables, name='module_inventaire_list_articles_stockables'))
urlpatterns.append(url(r'^articles/add', views.get_creer_article, name='module_inventaire_add_article'))
urlpatterns.append(url(r'^articles/post_add', views.post_creer_article, name='module_inventaire_post_add_article'))
urlpatterns.append(url(r'^articles/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_article, name='module_inventaire_update_article'))
urlpatterns.append(url(r'^articles/item/post_update/$', views.post_modifier_article, name='module_inventaire_post_update_article'))
urlpatterns.append(url(r'^articles/item/(?P<ref>[0-9]+)/$', views.get_details_article, name='module_inventaire_details_article'))
urlpatterns.append(url(r'^article/details', views.get_details_article_fourni, name='module_inventaire_details_article_fourni'))
urlpatterns.append(url(r'^article/item/emplacement/$', views.get_article_of_emplacement, name='module_inventaire_article_of_emplacement'))

# EMPLACEMENT URLS
urlpatterns.append(url(r'^entrepots/list', views.get_lister_entrepots, name='module_inventaire_list_entrepots'))
urlpatterns.append(url(r'^emplacements/list', views.get_lister_emplacements, name='module_inventaire_list_emplacements'))
urlpatterns.append(url(r'^articles/emplacement', views.get_lister_articles_in_emplacement, name='module_inventaire_list_articles_emplacement'))

# TYPE OPERATION URLS
urlpatterns.append(url(r'^operations/stock/list', views.get_lister_operations_stock, name='module_inventaire_list_operations_stock'))
urlpatterns.append(url(r'^operations/stock/add', views.get_creer_operations_stock, name='module_inventaire_add_operations_stock'))
urlpatterns.append(url(r'^operations/stock/post_add', views.post_creer_operations_stock, name='module_inventaire_post_add_operations_stock'))
urlpatterns.append(url(r'^operations/stock/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_operations_stock, name='module_inventaire_update_operations_stock'))
urlpatterns.append(url(r'^operations/stock/item/post_update/$', views.post_modifier_operations_stock, name='module_inventaire_post_update_operations_stock'))
urlpatterns.append(url(r'^operations/stock/item/(?P<ref>[0-9]+)/$', views.get_details_operations_stock, name='module_inventaire_details_operations_stock'))

# CONFIGURATION URLS
urlpatterns.append(url(r'^configuration', views.get_configuration, name='module_inventaire_configuration'))
urlpatterns.append(url(r'^configuration/post_update/$', views.post_modifier_configuration, name='module_inventaire_post_modifier_configuration'))

# FOURNITURES URLS --- Demande Mr Thomas -----
urlpatterns.append(url(r'^fournitures/list', views.get_lister_fournitures, name='module_inventaire_list_fournitures'))
urlpatterns.append(url(r'^fournitures/item/(?P<ref>[0-9]+)/$', views.get_details_fourniture, name='module_inventaire_details_fourniture'))
urlpatterns.append(url(r'^fournitures/add', views.get_creer_fourniture, name='module_inventaire_add_fourniture'))
urlpatterns.append(url(r'^fournitures/validate', views.get_valider_fourniture, name='module_inventaire_valider_fourniture'))
urlpatterns.append(url(r'^fournitures/post_validate/$', views.post_valider_fourniture, name='module_inventaire_post_valider_fourniture'))
urlpatterns.append(url(r'^fournitures/lignes', views.get_lister_lignes_fourniture, name='module_inventaire_list_fourniture'))

# BONS D'ACHAT URLS --- Demande Mr Thomas -----
urlpatterns.append(url(r'^bons/list', views.get_lister_bons_reception, name='module_inventaire_list_bon_receptions'))
urlpatterns.append(url(r'^bons/item/(?P<ref>[0-9]+)/$', views.get_details_bon_reception, name='module_inventaire_details_bon_reception'))
urlpatterns.append(url(r'^bons/item/(?P<ref>[0-9]+)/receive/$', views.get_receptionner_bon_reception, name='module_inventaire_receive_bon_reception'))
urlpatterns.append(url(r'^bons/item/post_receive/$', views.post_receptionner_bon_reception, name='module_inventaire_post_receive_bon_reception'))

urlpatterns.append(url(r'^bons_entrees/list', views.get_lister_bons_entrees, name='module_inventaire_list_bons_entrees'))
urlpatterns.append(url(r'^bons_entrees/item/(?P<ref>[0-9]+)/$', views.get_details_bons_entrees, name='module_inventaire_details_bons_entrees'))
urlpatterns.append(url(r'^bons_entrees/workflow_post', views.post_workflow_bon_entree_depot, name = 'module_inventaire_bon_entrees_workflow_post'))

urlpatterns.append(url(r'^bons_entrees/item/release_asset/$', views.get_to_asset_of_bons_entrees, name='module_inventaire_get_assetiser_bons_entrees'))
urlpatterns.append(url(r'^bons_entrees/item/post_release_asset/$', views.post_to_asset_of_bons_entrees, name='module_inventaire_post_assetiser_bons_entrees'))

#SORTIE MATERIEL SMG
urlpatterns.append(url(r'^bon_sortie_smg/list', views.get_lister_bon_sortie_smg, name='module_inventaire_list_sortie_mat_smg'))
urlpatterns.append(url(r'^bon_sortie_smg/add', views.get_creer_bon_sortie_smg, name='module_inventaire_add_creer_bon_sortie_smg'))
urlpatterns.append(url(r'^bon_sortie_smg/validate', views.get_valider_bon_sortie_smg, name='module_inventaire_valider_bon_sortie_smg'))
urlpatterns.append(url(r'^bon_sortie/post_validate', views.post_valider_bon_sortie_, name='module_inventaire_post_valider_bon_sortie_'))

# TRANSFERT INTERNAL URLS
urlpatterns.append(url(r'^affectation/list', views.get_lister_transfert_internal, name='module_inventaire_list_transfert_internal'))
urlpatterns.append(url(r'^affectation/add', views.get_creer_transfert_internal, name='module_inventaire_add_transfert_internal'))
urlpatterns.append(url(r'^affectation/validate', views.get_valider_transfert_internal, name='module_inventaire_valider_transfert_internal'))
urlpatterns.append(url(r'^affectation/post_validate', views.post_valider_transfert_internal, name='module_inventaire_post_valider_transfert_internal'))
urlpatterns.append(url(r'^affectation/item/(?P<ref>[0-9]+)/release/$', views.get_realiser_transfert_internal, name='module_inventaire_realiser_transfert_internal'))
urlpatterns.append(url(r'^affectation/item/post_release/$', views.post_realiser_transfert_internal, name='module_inventaire_post_realiser_transfert_internal'))
urlpatterns.append(url(r'^affectation/item/(?P<ref>[0-9]+)/$', views.get_details_transfert_internal, name='module_inventaire_details_transfert_internal'))

urlpatterns.append(url(r'^affectation/item/(?P<ref>[0-9]+)/complete/$', views.get_completer_transfert_internal, name='module_inventaire_completer_transfert_internal'))
urlpatterns.append(url(r'^affectation/item/post_complete/$', views.post_completer_transfert_internal, name='module_inventaire_post_completer_transfert_internal'))

urlpatterns.append(url(r'^affectation/workflow_post', views.post_workflow_affectation, name = 'module_inventaire_affectation_workflow_post'))

urlpatterns.append(url(r'^affectation/item/release_asset/$', views.get_to_asset_of_transfert_internal, name='module_inventaire_get_assetiser_transfert_internal'))
urlpatterns.append(url(r'^affectation/item/post_release_asset/$', views.post_to_asset_of_transfert_internal, name='module_inventaire_post_assetiser_transfert_internal'))

#IMMOBILIER

urlpatterns.append(url(r'^asset/list', views.get_lister_asset, name = 'module_inventaire_list_asset'))
urlpatterns.append(url(r'^asset/add', views.get_creer_asset, name = 'module_inventaire_add_asset'))
urlpatterns.append(url(r'^asset/post_add', views.post_creer_asset, name = 'module_inventaire_post_add_asset'))
urlpatterns.append(url(r'^asset/item/(?P<ref>[0-9]+)/$', views.get_details_asset, name = 'module_inventaire_detail_asset'))
urlpatterns.append(url(r'^asset/item/post_update/$', views.post_modifier_asset, name = 'module_inventaire_post_update_asset'))
urlpatterns.append(url(r'^asset/item/(?P<ref>[0-9]+)/update$', views.get_modifier_asset, name = 'module_inventaire_update_asset'))

#STOCK DES EMPLACEMENTS
urlpatterns.append(url(r'^stock/(?P<ref>[0-9]+)/$', views.get_details_stock_emplacement, name = 'module_inventaire_item_stock_emplacement'))
urlpatterns.append(url(r'^stock/emplacements', views.get_lister_stock_emplacement, name='module_inventaire_list_stock_emplacements'))


urlpatterns.append(url(r'^assets/emplacement/(?P<ref>[0-9]+)/$', views.get_details_asset_emplacement, name = 'module_inventaire_item_asset_emplacement'))
urlpatterns.append(url(r'^assets/emplacements', views.get_lister_asset_emplacement, name='module_inventaire_list_asset_emplacements'))

# IMMOBILISATION
urlpatterns.append(url(r'^immobilisations/list', views.get_lister_immobilisations, name='module_inventaire_list_immobilisations'))
urlpatterns.append(url(r'^immobilisations/item/(?P<ref>[0-9]+)/$', views.get_details_immobilisation, name='module_inventaire_details_immobilisation'))


urlpatterns.append(url(r'^traitement_immobilisation/list', views.get_lister_traitement_immobilisation, name = 'module_inventaire_list_traitement_immobilisation'))
urlpatterns.append(url(r'^traitement_immobilisation/add', views.get_creer_traitement_immobilisation, name = 'module_inventaire_add_traitement_immobilisation'))
urlpatterns.append(url(r'^traitement_immobilisation/post_add', views.post_creer_traitement_immobilisation, name = 'module_inventaire_post_add_traitement_immobilisation'))
urlpatterns.append(url(r'^traitement_immobilisation/item/(?P<ref>[0-9]+)/$', views.get_details_traitement_immobilisation, name = 'module_inventaire_detail_traitement_immobilisation'))
urlpatterns.append(url(r'^traitement_immobilisation/item/post_update/$', views.post_modifier_traitement_immobilisation, name = 'module_inventaire_post_update_traitement_immobilisation'))
urlpatterns.append(url(r'^traitement_immobilisation/item/(?P<ref>[0-9]+)/update$', views.get_modifier_traitement_immobilisation, name = 'module_inventaire_update_traitement_immobilisation'))

#---------------- Repporting -------------------------------
urlpatterns.append(url(r'^fournitures/rapport/(?P<ref>[0-9]+)/$', views.get_print_rapport_details_fourniture, name='module_inventaire_get_print_rapport_details_fourniture'))


#RETOUR MATERIEL
urlpatterns.append(url(r'^retour/list', views.get_lister_retour_internal, name='module_inventaire_list_retour_internal'))
urlpatterns.append(url(r'^retour/add', views.get_creer_retour_internal, name='module_inventaire_add_retour_internal'))
urlpatterns.append(url(r'^retour/validate', views.get_valider_retour_internal, name='module_inventaire_valider_retour_internal'))
urlpatterns.append(url(r'^retour/post_validate', views.post_valider_retour_internal, name='module_inventaire_post_valider_retour_internal'))
urlpatterns.append(url(r'^retour/item/(?P<ref>[0-9]+)/release/$', views.get_realiser_retour_internal, name='module_inventaire_realiser_retour_internal'))
urlpatterns.append(url(r'^retour/item/post_release/$', views.post_realiser_retour_internal, name='module_inventaire_post_realiser_retour_internal'))
urlpatterns.append(url(r'^retour/item/(?P<ref>[0-9]+)/$', views.get_details_retour_internal, name='module_inventaire_details_retour_internal'))

urlpatterns.append(url(r'^retour/item/(?P<ref>[0-9]+)/complete/$', views.get_completer_retour_internal, name='module_inventaire_completer_retour_internal'))
urlpatterns.append(url(r'^retour/item/post_complete/$', views.post_completer_retour_internal, name='module_inventaire_post_completer_retour_internal'))

urlpatterns.append(url(r'^retour/workflow_post', views.post_workflow_retour, name = 'module_inventaire_retour_workflow_post'))

urlpatterns.append(url(r'^retour/item/release_asset/$', views.get_to_asset_of_retour_internal, name='module_inventaire_get_assetiser_retour_internal'))
urlpatterns.append(url(r'^retour/item/post_release_asset/$', views.post_to_asset_of_retour_internal, name='module_inventaire_post_assetiser_retour_internal'))

#REBUT
urlpatterns.append(url(r'^rebut/list', views.get_lister_rebut, name='module_inventaire_list_rebut'))
urlpatterns.append(url(r'^rebut/add', views.get_creer_rebut, name='module_inventaire_add_rebut'))
urlpatterns.append(url(r'^rebut/post_rebut/$', views.post_valider_rebut, name='module_inventaire_post_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/$', views.get_detail_rebut, name='module_inventaire_details_rebut'))

#RAPPORT MVT STOCK
urlpatterns.append(url(r'^rapport_mvt/add', views.get_rapport_mvt_stock, name='module_inventaire_create_rapport_stock'))
urlpatterns.append(url(r'^rapport/post_mvt/$', views.get_detail_rapport_mvt_stock, name='module_inventaire_post_mvt_stock'))

#RAPPORT ARTICLE STOCK
urlpatterns.append(url(r'^rapport_article/add', views.get_rapport_article_stock, name='module_inventaire_create_rapport_article_stock'))
urlpatterns.append(url(r'^rapport/post_article_stock/$', views.get_detail_article_stock, name='module_inventaire_post_article_in_stock'))
#AJAX
urlpatterns.append(url(r'all_categorie_of_article', views.get_list_categorie_of_article, name='module_inventaire_get_categorie_of_article'))
