from django.conf.urls import include, url
from . import views


urlpatterns=[

    url(r'^client/upload/add', views.get_upload_client, name='module_comptabilite_get_upload_client'),
    url(r'^client/upload/post_add', views.post_upload_client, name='module_comptabilite_post_upload_client'),

]

#TABLEAU DE BORD
urlpatterns.append(url(r'^tableau', views.get_dashboard, name = 'module_vente_tableau_de_bord'))
#ARTICLE 
urlpatterns.append(url(r'^articles/list', views.get_lister_article, name='module_vente_list_articles'))
urlpatterns.append(url(r'^articles/add', views.get_creer_article, name='module_vente_add_article'))
urlpatterns.append(url(r'^articles/post_add', views.post_creer_article, name='module_vente_post_add_article'))
urlpatterns.append(url(r'^articles/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_article, name='module_vente_update_article'))
urlpatterns.append(url(r'^articles/item/post_update/$', views.post_modifier_article, name='module_vente_post_update_article'))
urlpatterns.append(url(r'^articles/item/(?P<ref>[0-9]+)/$', views.get_details_article, name='module_vente_details_article'))
urlpatterns.append(url(r'^articles/get_prix', views.get_json_get_prix_article, name='module_vente_article_prix'))
urlpatterns.append(url(r'^articles/details', views.get_details_article_fourni, name='module_vente_details_article_fourni'))

#CATEGORIE ARTICLE
urlpatterns.append(url(r'^categorie/article/list', views.get_lister_categorie_articles, name = 'module_vente_list_categorie_articles'))
urlpatterns.append(url(r'^categorie/article/add', views.get_creer_categorie_articles, name = 'module_vente_add_categorie_articles'))
urlpatterns.append(url(r'^categorie/article/post_add', views.post_creer_categorie_articles, name = 'module_vente_post_add_categorie_articles'))
urlpatterns.append(url(r'^categories/article/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_articles, name='module_vente_details_categorie_articles'))
urlpatterns.append(url(r'^categories/article/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_catagorie_articles, name='module_vente_update_categorie_articles'))
urlpatterns.append(url(r'^categories/article/item/post_update/$', views.post_modifier_categorie_articles, name='module_vente_post_update_categorie_articles'))

#CLIENT
urlpatterns.append(url(r'^client/list', views.get_lister_clients, name='module_vente_list_clients'))
urlpatterns.append(url(r'^client/add', views.get_creer_client, name='module_vente_add_client'))
urlpatterns.append(url(r'^client/post_add', views.post_creer_client, name='module_vente_post_add_client'))
urlpatterns.append(url(r'^client/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_client, name='module_vente_update_client'))
urlpatterns.append(url(r'^client/item/post_update/$', views.post_modifier_client, name='module_vente_post_update_client'))
urlpatterns.append(url(r'^client/item/(?P<ref>[0-9]+)/$', views.get_details_client, name='module_vente_details_client'))

#BON DE COMMANDE
urlpatterns.append(url(r'^bon_commande/list', views.get_lister_bon_commande, name = 'module_vente_list_bon_commande'))
urlpatterns.append(url(r'^bon_commande/add', views.get_creer_bon_commande, name = 'module_vente_add_bon_commande'))
urlpatterns.append(url(r'^bon_commande/post_add', views.post_creer_bon_commande, name = 'module_vente_post_add_bon_commande'))
urlpatterns.append(url(r'^bon_commande/item/(?P<ref>[0-9]+)/$', views.get_details_bon_commande, name = 'module_vente_detail_bon_commande'))
urlpatterns.append(url(r'^ligne_commande/list', views.get_lister_ligne_commande, name = 'module_achat_list_ligne_commande'))

#LIGNE DE COMMANDE
urlpatterns.append(url(r'^ligne_commande/list', views.get_lister_ligne_commande, name = 'module_vente_list_ligne_commande'))
urlpatterns.append(url(r'^ligne_commande/add', views.get_creer_ligne_commande, name = 'module_vente_add_ligne_commande'))
urlpatterns.append(url(r'^ligne_commande/post_add', views.post_creer_ligne_commande, name = 'module_vente_post_add_ligne_commande'))
urlpatterns.append(url(r'^ligne_commande/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_commande, name = 'module_vente_detail_ligne_commande'))

#CONDITION DE REGLEMENT
urlpatterns.append(url(r'^reglement/list', views.get_lister_condition_reglement, name = 'module_vente_list_reglement'))
urlpatterns.append(url(r'^reglement/add', views.get_creer_condition_reglement, name = 'module_vente_add_reglement'))
urlpatterns.append(url(r'^reglement/post_add', views.post_creer_condition_reglement, name = 'module_vente_post_add_reglement'))
urlpatterns.append(url(r'^reglement/item/(?P<ref>[0-9]+)/$', views.get_details_condition_reglement, name = 'module_vente_details_reglement'))
urlpatterns.append(url(r'^reglement/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_condition_reglement, name='module_vente_update_reglement'))
urlpatterns.append(url(r'^reglement/item/post_update/$', views.post_modifier_condition_reglement, name='module_vente_post_update_reglement'))

#BON DE LIVRAISON
urlpatterns.append(url(r'^bon_livraison/list', views.get_lister_bon_livraison, name = 'module_vente_list_bon_livraison'))
urlpatterns.append(url(r'^bon_livraison/add', views.get_creer_bon_livraison, name = 'module_vente_add_bon_livraison'))
urlpatterns.append(url(r'^bon_livraison/post_add', views.post_creer_bon_livraison, name = 'module_vente_post_add_bon_livraison'))
urlpatterns.append(url(r'^bon_livraison/item/(?P<ref>[0-9]+)/$', views.get_details_bon_livraison, name = 'module_vente_detail_bon_livraison'))

#TRANSACTION CLIENT
urlpatterns.append(url(r'^transaction_client/list', views.get_lister_transaction_client, name = 'module_vente_list_transaction_client'))
urlpatterns.append(url(r'^transaction_client/add', views.get_creer_transaction_client, name = 'module_vente_add_transaction_client'))
urlpatterns.append(url(r'^transaction_client/post_add', views.post_creer_transaction_client, name = 'module_vente_post_add_transaction_client'))
urlpatterns.append(url(r'^transaction_client/item/(?P<ref>[0-9]+)/$', views.get_details_transaction_client, name = 'module_vente_detail_transaction_client'))

#PAIEMENT CLIENT
urlpatterns.append(url(r'^paiement/list', views.get_lister_paiement_client, name = 'module_vente_list_paiement_client'))
urlpatterns.append(url(r'^paiement/add', views.get_creer_paiement_client, name = 'module_vente_add_paiement_client'))
urlpatterns.append(url(r'^paiement/post_add', views.post_creer_paiement_client, name = 'module_vente_post_add_paiement_client'))
urlpatterns.append(url(r'^paiement/item/(?P<ref>[0-9]+)/$', views.get_details_paiement_client, name = 'module_vente_detail_paiement_client'))


#CATEGORIE UNITE
urlpatterns.append(url(r'^categorie/unite/list', views.get_lister_categorie_unites, name = 'module_vente_list_categorie_unite'))
urlpatterns.append(url(r'^categorie/unite/add', views.get_creer_categorie_unites, name = 'module_vente_add_categorie_unites'))
urlpatterns.append(url(r'^categorie/unite/post_add', views.post_creer_categorie_unites, name = 'module_vente_post_add_categorie_unites'))
urlpatterns.append(url(r'^categories/unite/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_unites, name='module_vente_details_categorie_unites'))
urlpatterns.append(url(r'^categories/unite/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_catagorie_unites, name='module_vente_update_categorie_unites'))
urlpatterns.append(url(r'^categories/unite/item/post_update/$', views.post_modifier_categorie_unites, name='module_vente_post_update_categorie_unites'))


#UNITE DE MESURE
urlpatterns.append(url(r'^unite/list', views.get_lister_unites, name='module_vente_list_unite'))
urlpatterns.append(url(r'^unite/add', views.get_creer_unite, name='module_vente_add_unite'))
urlpatterns.append(url(r'^unite/post_add', views.post_creer_unite, name='module_vente_post_add_unite'))
urlpatterns.append(url(r'^unite/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_unite, name='module_vente_update_unite'))
urlpatterns.append(url(r'^unite/item/post_update/$', views.post_modifier_unite, name='module_vente_post_update_unite'))
urlpatterns.append(url(r'^unite/item/(?P<ref>[0-9]+)/$', views.get_details_unite, name='module_vente_details_unite'))

#FACTURE CLIENT
urlpatterns.append(url(r'^factures/list', views.get_lister_factures_client, name='module_vente_list_facture_client'))
urlpatterns.append(url(r'^factures/item/(?P<ref>[0-9]+)/$', views.get_details_facture_client, name='module_vente_details_facture_client'))
urlpatterns.append(url(r'^factures/add/(?P<ref>[0-9]+)/$', views.get_creer_facture_client, name='module_vente_add_facture_client'))
urlpatterns.append(url(r'^factures/item/validate', views.post_valider_facture_client, name='module_vente_validate_facture_client'))
urlpatterns.append(url(r'^factures/post_add', views.post_creer_facture_client, name='module_vente_post_add_facture_client'))
urlpatterns.append(url(r'^factures/(?P<ref>[0-9]+)/update/$', views.get_modifier_facture_client, name='module_vente_update_facture_client'))
urlpatterns.append(url(r'^factures/post_update/$', views.post_modifier_facture_client, name='module_vente_post_update_facture_client'))
urlpatterns.append(url(r'^factures/workflow_post', views.post_workflow_facture, name = 'module_vente_facture_workflow_post'))


#ETAT DE FACTURATION
urlpatterns.append(url(r'^etatfacturation/list', views.get_lister_etat_facturation, name='module_vente_list_etat_facturation'))
urlpatterns.append(url(r'^etatfacturation/item/(?P<ref>[0-9]+)/$', views.get_details_etat_facturation, name='module_vente_details_etat_facturation'))
urlpatterns.append(url(r'^etatfacturation/add/', views.get_creer_etat_facturation, name='module_vente_add_etat_facturation'))
urlpatterns.append(url(r'^etatfacturation/post_add', views.post_creer_etat_facturation, name='module_vente_post_add_etat_facturation'))
#urlpatterns.append(url(r'^factures/(?P<ref>[0-9]+)/update/$', views.get_modifier_facture_client, name='module_vente_update_facture_client'))
#urlpatterns.append(url(r'^factures/post_update/$', views.post_modifier_facture_client, name='module_vente_post_update_facture_client'))
urlpatterns.append(url(r'^etatfacturation/workflow_post', views.post_workflow_etat_facturation, name = 'module_vente_etat_facturation_workflow_post'))


#CIVILITE
urlpatterns.append(url(r'^civilite/list', views.get_lister_civilite, name = 'module_vente_list_civilite'))
urlpatterns.append(url(r'^civilite/add', views.get_creer_civilite, name = 'module_vente_add_civilite'))
urlpatterns.append(url(r'^civilite/post_add', views.post_creer_civilite, name = 'module_vente_post_add_civilite'))
urlpatterns.append(url(r'^civilite/item/(?P<ref>[0-9]+)/$', views.get_details_civilite, name='module_vente_details_civilite'))
urlpatterns.append(url(r'^civilite/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_civilite, name='module_vente_update_civilite'))
urlpatterns.append(url(r'^civilite/item/post_update/$', views.post_modifier_civilite, name='module_vente_post_update_civilite'))

# RECOUVREMENT URL
# =======================================================

# RECOUVREMENT URLS
urlpatterns.append(url(r'^recouvrement/list', views.get_lister_recouvrement, name = 'module_vente_list_recouvrement'))
urlpatterns.append(url(r'^recouvrement/add', views.get_creer_recouvrement, name = 'module_vente_add_recouvrement'))
urlpatterns.append(url(r'^recouvrement/item/(?P<ref>[0-9]+)/$', views.get_details_recouvrement, name = 'module_vente_detail_recouvrement'))
urlpatterns.append(url(r'^recouvrement/post_add', views.post_creer_recouvrement, name = 'module_vente_post_add_recouvrement'))
urlpatterns.append(url(r'^recouvrement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_recouvrement, name = 'module_vente_update_recouvrement'))
urlpatterns.append(url(r'^recouvrement/post_update', views.post_modifier_recouvrement, name = 'module_vente_post_update_recouvrement'))

# RELANCE RECOUVREMENT URLS
urlpatterns.append(url(r'^recouvrement/relance/list', views.get_lister_relance_recouvrement, name = 'module_vente_list_relance_recouvrement'))
urlpatterns.append(url(r'^recouvrement/relance/add', views.get_creer_relance_recouvrement, name = 'module_vente_add_relance_recouvrement'))
urlpatterns.append(url(r'^recouvrement/relance/item/(?P<ref>[0-9]+)/$', views.get_details_relance_recouvrement, name = 'module_vente_detail_relance_recouvrement'))
urlpatterns.append(url(r'^recouvrement/relance/post_add', views.post_creer_relance_recouvrement, name = 'module_vente_post_add_relance_recouvrement'))
urlpatterns.append(url(r'^recouvrement/relance/item/(?P<ref>[0-9]+)/update$', views.get_modifier_relance_recouvrement, name = 'module_vente_update_relance_recouvrement'))
urlpatterns.append(url(r'^recouvrement/relance/post_update', views.post_modifier_relance_recouvrement, name = 'module_vente_post_update_relance_recouvrement'))

# BALANCE CLIENT URLS
urlpatterns.append(url(r'^balance/client/generate', views.get_generer_balance_client, name = 'module_vente_generer_balance_client'))
urlpatterns.append(url(r'^balance/client/post_generate', views.post_generer_balance_client, name = 'module_vente_post_generer_balance_client'))

# EXTRAIT DE COMPTE CLIENT URLS
urlpatterns.append(url(r'^extrait/compte/generate', views.get_generer_extrait_compte, name = 'module_vente_generer_extrait_compte'))
urlpatterns.append(url(r'^extrait/compte/post_generate', views.post_generer_extrait_compte, name = 'module_vente_post_generer_extrait_compte'))
urlpatterns.append(url(r'^extrait/compte/print', views.post_imprimer_extrait_compte, name = 'module_vente_post_imprimer_extrait_compte'))

# BALANCE AGEE CLIENT URLS
urlpatterns.append(url(r'^balance_agee/client/generate', views.get_generer_balance_agee_client, name='module_vente_generer_balance_agee_client'))
urlpatterns.append(url(r'^balance_agee/client/post_generate', views.post_generer_balance_agee_client, name='module_vente_post_generer_balance_agee_client'))

urlpatterns.append(url(r'^typefactureclient/list', views.get_lister_typefactureclient, name = 'module_vente_list_typefactureclient'))
urlpatterns.append(url(r'^typefactureclient/add', views.get_creer_typefactureclient, name = 'module_vente_add_typefactureclient'))
urlpatterns.append(url(r'^typefactureclient/post_add', views.post_creer_typefactureclient, name = 'module_vente_post_add_typefactureclient'))
urlpatterns.append(url(r'^typefactureclient/item/(?P<ref>[0-9]+)/$', views.get_details_typefactureclient, name = 'module_vente_detail_typefactureclient'))
urlpatterns.append(url(r'^typefactureclient/item/post_update/$', views.post_modifier_typefactureclient, name = 'module_vente_post_update_typefactureclient'))
urlpatterns.append(url(r'^typefactureclient/item/(?P<ref>[0-9]+)/update$', views.get_modifier_typefactureclient, name = 'module_vente_update_typefactureclient'))