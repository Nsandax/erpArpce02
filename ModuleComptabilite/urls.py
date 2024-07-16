from django.conf.urls import include, url
from . import views

urlpatterns=[
    # DASHBOARD URL
    url(r'^tableau', views.get_tableau_de_bord, name='module_comptabilite_tableau_de_bord'),
    url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_comptabilite_notification'),

    url(r'^rapport/tresorerie/synthese/generate', views.get_generer_rapport_synthese, name='module_comptabilite_generate_rapport_synthese'),
    url(r'^rapport/tresorerie/synthese/print', views.post_rapport_synthese, name = 'module_comptabilite_print_rapport_synthese'),
    url(r'^rapport/tresorerie/synthese/detail', views.post_rapport_pre_synthese, name = 'module_comptabilite_post_pre_rapport_synthese'),

    url(r'^rapport/tresorerie/rapprochement/generate', views.get_generer_rapport_rapprochement, name='module_comptabilite_generate_rapport_rapprochement'),
    url(r'^rapport/tresorerie/rapprochement/print', views.post_rapport_rapprochement, name = 'module_comptabilite_print_rapport_rapprochement'),

    url(r'^rapport/tresorerie/print/rapprochement/', views.post_rapport_rapprochement, name = 'module_comptabilite_print_rapport_rapprochement_bancaire'),

    #Json Get facture
    url(r'all_facture_non_solved', views.get_json_facture, name='module_comptabilite_get_facture_non_solde'),
    #Get select facture info
    url(r'facture_select', views.get_json_select_facture, name='module_comptabilite_get_select_facture'),


    url(r'^compte_analytique/item/ecriture_analytique/(?P<ref>[0-9]+)/$', views.get_details_ecriture_analytique_of_compte_analytique, name = 'module_comptabilite_detail_ecriture_analytique_compte_analytique'),


    url(r'check_json_active_operation_in_poste', views.check_json_active_operation_in_poste, name='module_comptabilite_check_active_operation_in_poste'),



    # ECRITURES COMPTABLES URLS
    url(r'^ecritures/list', views.get_lister_ecritures, name='module_comptabilite_lister_ecritures'),

    # PIECES COMPTABLES URLS
    url(r'^pieces/list', views.get_lister_pieces_comptables, name='module_comptabilite_lister_pieces'),
    url(r'^pieces/add', views.get_creer_piece_comptable, name='module_comptabilite_creer_piece'),
    url(r'^pieces/post_add', views.post_creer_piece_comptable, name='module_comptabilite_post_creer_piece'),
    url(r'^pieces/item/(?P<ref>[0-9]+)/$', views.get_details_piece, name='module_comptabilite_details_piece'),
    url(r'^pieces/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_piece_comptable, name='module_comptabilite_modifier_piece'),
    url(r'^pieces/item/post_update/$', views.post_modifier_piece_comptable, name='module_comptabilite_post_modifier_piece'),
    url(r'^pieces/upload/add', views.get_upload_piece_comptable, name='module_comptabilite_get_upload_piece'),
    url(r'^pieces/upload/post_add', views.post_upload_piece_comptable, name='module_comptabilite_post_upload_piece'),

    # COMPTES URLS
    url(r'^comptes/list', views.get_lister_comptes, name='module_comptabilite_lister_comptes'),
    url(r'^comptes/add', views.get_creer_compte, name='module_comptabilite_creer_compte'),
    url(r'^comptes/post_add', views.post_creer_compte, name='module_comptabilite_post_creer_compte'),
    url(r'^comptes/item/(?P<ref>[0-9]+)/$', views.get_details_compte, name='module_comptabilite_details_compte'),
    url(r'^comptes/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_compte, name='module_comptabilite_modifier_compte'),
    url(r'^comptes/item/post_update/$', views.post_modifier_compte, name='module_comptabilite_post_modifier_compte'),
    url(r'^comptes/search/result/$', views.get_lister_comptes_correspondants, name='module_comptabilite_lister_comptes_correspondants'),

    # JOURNAUX URLS
    url(r'^journaux/list', views.get_lister_journaux, name='module_comptabilite_lister_journaux'),
    url(r'^journaux/add', views.get_creer_journal, name='module_comptabilite_creer_journal'),
    url(r'^journaux/post_add', views.post_creer_journal, name='module_comptabilite_post_creer_journal'),
    url(r'^journaux/item/(?P<ref>[0-9]+)/$', views.get_details_journal, name='module_comptabilite_details_journal'),
    url(r'^journaux/item/(?P<ref>[0-9]+)/assign/default/$', views.get_set_journal_defaut, name='module_comptabilite_assigner_journal_defaut'),
    url(r'^journaux/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_journal, name='module_comptabilite_modifier_journal'),
    url(r'^journaux/item/post_update/$', views.post_modifier_journal, name='module_comptabilite_post_modifier_journal'),
    url(r'^journal/generate', views.get_generer_journal, name='module_comptabilite_generer_journal'),
    url(r'^journal/post_generate', views.post_generer_journal, name='module_comptabilite_post_generer_journal'),
    url(r'^journal/print', views.post_imprimer_journal, name='module_comptabilite_post_imprimer_journal'),

    # GRANDS-LIVRES URLS
    url(r'^livre/generate', views.get_generer_grand_livre, name='module_comptabilite_generer_grand_livre'),
    url(r'^livre/post_generate', views.post_generer_grand_livre, name='module_comptabilite_post_generer_grand_livre'),
    url(r'^livre/print', views.post_imprimer_grand_livre, name='module_comptabilite_post_imprimer_grand_livre'),

    # BALANCES-GENERALES URLS
    url(r'^balance/generate', views.get_generer_balance_generale, name='module_comptabilite_generer_balance_generale'),
    url(r'^balance/post_generate', views.post_generer_balance_generale, name='module_comptabilite_post_generer_balance_generale'),
    url(r'^balance/print', views.post_imprimer_balance_generale, name='module_comptabilite_post_imprimer_balance_generale'),

    # BALANCE DES TIERS URLS
    url(r'^balance_tiers/generate', views.get_generer_balance_tiers, name='module_comptabilite_generer_balance_tiers'),
    url(r'^balance_tiers/post_generate', views.post_generer_balance_tiers, name='module_comptabilite_post_generer_balance_tiers'),
    url(r'^balance_tiers/print', views.post_imprimer_balance_tiers, name='module_comptabilite_post_imprimer_balance_tiers'),

    # BALANCE AGEE URLS
    url(r'^balance_agee/client/generate', views.get_generer_balance_agee_client, name='module_comptabilite_generer_balance_agee_client'),
    url(r'^balance_agee/client/post_generate', views.post_generer_balance_agee_client, name='module_comptabilite_post_generer_balance_agee_client'),
    url(r'^balance_agee/client/print', views.post_imprimer_balance_agee_client, name='module_comptabilite_post_imprimer_balance_agee_client'),
    url(r'^balance_agee/fournisseur/generate', views.get_generer_balance_agee_fournisseur, name='module_comptabilite_generer_balance_agee_fournisseur'),
    url(r'^balance_agee/fournisseur/post_generate', views.post_generer_balance_agee_fournisseur, name='module_comptabilite_post_generer_balance_agee_fournisseur'),
    url(r'^balance_agee/fournisseur/print', views.post_imprimer_balance_agee_fournisseur, name='module_comptabilite_post_imprimer_balance_agee_fournisseur'),

    # BILAN URLS
    url(r'^bilan/generate', views.get_generer_bilan, name='module_comptabilite_generer_bilan'),
    url(r'^bilan/post_generate', views.post_generer_bilan, name='module_comptabilite_post_generer_bilan'),
    url(r'^bilan/print', views.post_imprimer_bilan, name='module_comptabilite_post_imprimer_bilan'),

    # RESULTAT URLS
    url(r'^resultat/generate', views.get_generer_resultat, name='module_comptabilite_generer_resultat'),
    url(r'^resultat/post_generate', views.post_generer_resultat, name='module_comptabilite_post_generer_resultat'),
    url(r'^resultat/print', views.post_imprimer_resultat, name='module_comptabilite_post_imprimer_resultat'),

    # TABLEAU DE BORD DE FLUX TRESORERIE URLS
    url(r'^tb_tresorerie/generate', views.get_generer_tb_tresorerie, name='module_comptabilite_generer_tb_tresorerie'),
    url(r'^tb_tresorerie/post_generate', views.post_generer_tb_tresorerie, name='module_comptabilite_post_generer_tb_tresorerie'),


    # TABLEAU DE FLUX DE TRESORERIE URLS
    url(r'^tresorerie/generate', views.get_generer_tresorerie, name='module_comptabilite_generer_tresorerie'),
    url(r'^tresorerie/post_generate', views.post_generer_tresorerie, name='module_comptabilite_post_generer_tresorerie'),
    url(r'^tresorerie/print', views.post_imprimer_tresorerie, name='module_comptabilite_post_imprimer_tresorerie'),

    # NOTES ANNEXES URLS
    url(r'^annexe/generate', views.get_generer_annexe, name='module_comptabilite_generer_annexe'),
    url(r'^annexe/post_generate', views.post_generer_annexe, name='module_comptabilite_post_generer_annexe'),
    url(r'^annexe/print', views.post_imprimer_annexe, name='module_comptabilite_post_imprimer_annexe'),

    # DEVISES URLS
    url(r'^devises/list', views.get_lister_devises, name='module_comptabilite_lister_devises'),
    url(r'^devises/add', views.get_creer_devise, name='module_comptabilite_creer_devise'),
    url(r'^devises/post_add', views.post_creer_devise, name='module_comptabilite_post_creer_devise'),
    url(r'^devises/item/(?P<ref>[0-9]+)/$', views.get_details_devise, name='module_comptabilite_details_devise'),
    url(r'^devises/item/(?P<ref>[0-9]+)/activate/$', views.get_activer_devise, name='module_comptabilite_activer_devise'),
    url(r'^devises/item/(?P<ref>[0-9]+)/deactivate/$', views.get_desactiver_devise, name='module_comptabilite_desactiver_devise'),
    url(r'^devises/item/(?P<ref>[0-9]+)/reference/$', views.get_referencer_devise, name='module_comptabilite_referencer_devise'),
    url(r'^devises/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_devise, name='module_comptabilite_modifier_devise'),
    url(r'^devises/item/post_update/$', views.post_modifier_devise, name='module_comptabilite_post_modifier_devise'),

    # TAUX DE CHANGE URLS
    url(r'^taux/list', views.get_lister_taux_change, name='module_comptabilite_lister_taux_change'),
    url(r'^devises/item/(?P<ref>[0-9]+)/taux/add', views.get_creer_taux_change, name='module_comptabilite_creer_taux_change'),
    url(r'^taux/post_add', views.post_creer_taux_change, name='module_comptabilite_post_creer_taux_change'),

    # CONFIGURATIONS URLS
    url(r'^configuration/update', views.get_modifier_parametre, name='module_comptabilite_modifier_configuration'),
    url(r'^configuration/post_update', views.post_modifier_configuration, name='module_comptabilite_post_modifier_configuration'),

    #FACTURE FOURNISSEUR
    url(r'^factures/fournisseur/list', views.get_lister_factures_fournisseur, name='module_comptabilite_list_factures_fournisseur'),
    url(r'^factures/item/add', views.get_creer_facture, name='module_comptabilite_add_facture_fournisseur'),
    url(r'^factures/item/validate', views.post_valider_facture, name='module_comptabilite_validate_facture_fournisseur'),
    url(r'^factures/item/post_add', views.post_creer_facture, name='module_comptabilite_post_add_facture_fournisseur'),
    url(r'^factures/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_facture, name='module_comptabilite_update_facture_fournisseur'),
    url(r'^factures/item/post_update/$', views.post_modifier_facture, name='module_comptabilite_post_update_facture_fournisseur'),
    url(r'^factures/item/(?P<ref>[0-9]+)/$', views.get_details_facture, name='module_comptabilite_details_facture_fournisseur'),
    url(r'^factures/fournisseur/print', views.get_imprimer_facture_fournisseur, name='module_comptabilite_imprimer_facture_fournisseur'),

    #FACTURE D'AVOIR
    url(r'^factures/avoir/add/(?P<ref>[0-9]+)/$', views.get_creer_facture_avoir, name='module_comptabilite_add_facture_avoir'),
    url(r'^factures/avoir/validate', views.post_valider_facture_avoir, name='module_comptabilite_validate_facture_avoir'),
    url(r'^factures/avoir/post_add', views.post_creer_facture_avoir, name='module_comptabilite_post_add_facture_avoir'),

    #FACTURE FOURNISSEUR AVANCE
    url(r'^factures/avance/list', views.get_lister_facture_avance, name='module_comptabilite_list_facture_fournisseur_avance'),
    url(r'^factures/avance/add/(?P<ref>[0-9]+)/$', views.get_creer_facture_avance, name='module_comptabilite_add_facture_fournisseur_avance'),
    url(r'^factures/avance/item/validate', views.post_valider_facture_avance, name='module_comptabilite_validate_facture_fournisseur_avance'),
    url(r'^factures/avance/item/post_add', views.post_creer_facture_avance, name='module_comptabilite_post_add_facture_fournisseur_avance'),
    url(r'^factures/avance/item/(?P<ref>[0-9]+)/$', views.get_details_facture, name='module_comptabilite_details_facture_fournisseur'),
    # url(r'^factures/avance/print/(?P<ref>[0-9]+)/$', views.get_imprimer_facture_fournisseur, name='module_comptabilite_print_facture_fournisseur'),

    # PAIEMENT FACTURE FOURNISSEUR
    url(r'^paiements/fournisseurs/list', views.get_lister_paiements_fournisseur, name='module_comptabilite_list_paiements_fournisseur'),
    url(r'^paiements/fournisseur/add/$', views.get_creer_paiement_fournisseur, name='module_comptabilite_add_paiement_fournisseur'),
    url(r'^factures/fournisseur/(?P<ref>[0-9]+)/paiements/add/$', views.get_creer_paiement_facture_fournisseur, name='module_comptabilite_add_paiement_facture_fournisseur'),
    url(r'^paiements/fournisseur/post_add/$', views.post_creer_paiement_fournisseur, name='module_comptabilite_post_add_paiement_fournisseur'),
    url(r'^paiements/fournisseur/item/(?P<ref>[0-9]+)/$', views.get_details_paiement_fournisseur, name='module_comptabilite_details_paiement_fournisseur'),

    url(r'^factures/fournisseur/workflow_post', views.post_workflow_facture_fournisseur, name = 'module_comptabilite_facture_fournisseur_workflow_post'),

    #FACTURE CLIENT
    url(r'^factures/client/list', views.get_lister_factures_client, name='module_comptabilite_list_factures_client'),
    url(r'^factures/client/item/(?P<ref>[0-9]+)/$', views.get_details_facture_client, name='module_comptabilite_details_facture_client'),
    url(r'^factures/client/add', views.get_creer_facture_client, name='module_comptabilite_add_facture_client'),
    url(r'^factures/client/item/validate', views.post_valider_facture_client, name='module_comptabilite_validate_facture_client'),
    url(r'^factures/client/post_add', views.post_creer_facture_client, name='module_comptabilite_post_add_facture_client'),
    url(r'^factures/client/(?P<ref>[0-9]+)/update/$', views.get_modifier_facture_client, name='module_comptabilite_update_facture_client'),
    url(r'^factures/client/post_update/$', views.post_modifier_facture_client, name='module_comptabilite_post_update_facture_client'),
    url(r'^factures/client/workflow_post', views.post_workflow_facture_client, name = 'module_comptabilite_facture_client_workflow_post'),
    url(r'^facture/client/print', views.get_print_facture_client, name = 'module_comptabilite_print_facture_client'),
    url(r'^factures/client/print', views.get_imprimer_facture_client, name='module_comptabilite_imprimer_facture_client'),
   url(r'all_type_not_billed', views.get_json_type_fact_client, name='module_comptabilite_get_type_facture_client_not_billed'),

    # PAIEMENT FACTURE CLIENT
    url(r'^paiements/client/list', views.get_lister_paiements_client, name='module_comptabilite_list_paiements_client'),
    url(r'^paiements/client/add/$', views.get_creer_paiement_client, name='module_comptabilite_add_paiement_client'),
    url(r'^factures/client/(?P<ref>[0-9]+)/paiements/add/$', views.get_creer_paiement_facture_client, name='module_comptabilite_add_paiement_facture_client'),
    url(r'^paiements/client/post_add/$', views.post_creer_paiement_client, name='module_comptabilite_post_add_paiement_client'),
    url(r'^paiements/client/post_validate/$', views.post_valider_paiement_client, name='module_comptabilite_post_validate_paiement_client'),
    url(r'^paiements/client/item/(?P<ref>[0-9]+)/$', views.get_details_paiement_client, name='module_comptabilite_details_paiement_client'),
    url(r'^paiements/client/post_workflow/$', views.post_workflow_paiement_client, name='module_comptabilite_post_workflow_paiement_client'),

    # RECEPTION FACTURE CLIENT URLS --- Demande Mr Thomas -----
    url(r'^bons/list', views.get_lister_bons_achat, name='module_comptabilite_list_bons_achat'),
    url(r'^bons/item/(?P<ref>[0-9]+)/$', views.get_details_bon_achat, name='module_comptabilite_details_bon_achat'),

    # IMMOBILISATION URLS
    url(r'^immobilisations/list', views.get_lister_immobilisations, name='module_comptabilite_list_immobilisations'),

    url(r'^immobilisations/tableau', views.get_creer_tableau_immobilisation, name='module_comptabilite_tab_immobilisations'),

    url(r'^immobilisations/add', views.get_creer_immobilisation, name='module_comptabilite_add_immobilisation'),
    url(r'^immobilisations/post_add', views.post_creer_immobilisation,name='module_comptabilite_post_add_immobilisation'),
    url(r'^immobilisations/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_immobilisation, name='module_comptabilite_update_immobilisation'),
    url(r'^immobilisations/item/post_update/$', views.post_modifier_immobilisation, name='module_comptabilite_post_update_immobilisation'),
    url(r'^immobilisations/item/(?P<ref>[0-9]+)/$', views.get_details_immobilisation, name='module_comptabilite_details_immobilisation'),

    url(r'^immobilisations/piece/add', views.get_creer_piece_immobilisation, name='module_comptabilite_add_piece_immobilisation'),
    url(r'^immobilisations/piece/post_add', views.post_creer_piece_immobilisation, name='module_comptabilite_post_add_piece_immobilisation'),

    url(r'^traitement_immobilisation/piece/add', views.get_creer_piece_traitement, name='module_comptabilite_add_piece_traitement_immobilisation'),
    url(r'^traitement_immobilisation/piece/post_add', views.post_creer_piece_traitement, name='module_comptabilite_post_add_piece_traitement_immobilisation'),


    #ARTICLES
    url(r'^articles/list', views.get_lister_article, name='module_comptabilite_list_article'),
    url(r'^articles/item/(?P<ref>[0-9]+)/$', views.get_details_article, name = 'module_comptabilite_detail_article'),
    url(r'^articles/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_article, name = 'module_comptabilite_update_article'),
    url(r'^articles/post_update', views.post_modifier_article, name = 'module_comptabilite_post_update_article'),

    #Fournisseur
    url(r'^fournisseur/list', views.get_lister_fournisseurs, name='module_comptabilite_list_fournisseur'),
    url(r'^fournisseur/item/(?P<ref>[0-9]+)/$', views.get_details_fournisseur, name = 'module_comptabilite_detail_fournisseur'),
    url(r'^fournisseur/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_fournisseur, name = 'module_comptabilite_update_fournisseur'),
    url(r'^fournisseur/post_update', views.post_modifier_fournisseur, name = 'module_comptabilite_post_update_fournisseur'),





]


urlpatterns.append(url(r'^taxe/list', views.get_lister_taxe, name = 'module_comptabilite_list_taxe'))
urlpatterns.append(url(r'^taxe/add', views.get_creer_taxe, name = 'module_comptabilite_add_taxe'))
urlpatterns.append(url(r'^taxe/post_add', views.post_creer_taxe, name = 'module_comptabilite_post_add_taxe'))
urlpatterns.append(url(r'^taxe/item/(?P<ref>[0-9]+)/$', views.get_details_taxe, name = 'module_comptabilite_detail_taxe'))
urlpatterns.append(url(r'^taxe/item/post_update/$', views.post_modifier_taxe, name = 'module_comptabilite_post_update_taxe'))
urlpatterns.append(url(r'^taxe/item/(?P<ref>[0-9]+)/update$', views.get_modifier_taxe, name = 'module_comptabilite_update_taxe'))




urlpatterns.append(url(r'^annee_fiscale/list', views.get_lister_annee_fiscale, name = 'module_comptabilite_list_annee_fiscale'))
urlpatterns.append(url(r'^annee_fiscale/add', views.get_creer_annee_fiscale, name = 'module_comptabilite_add_annee_fiscale'))
urlpatterns.append(url(r'^annee_fiscale/post_add', views.post_creer_annee_fiscale, name = 'module_comptabilite_post_add_annee_fiscale'))
urlpatterns.append(url(r'^annee_fiscale/item/(?P<ref>[0-9]+)/$', views.get_details_annee_fiscale, name = 'module_comptabilite_detail_annee_fiscale'))
urlpatterns.append(url(r'^annee_fiscale/item/post_update/$', views.post_modifier_annee_fiscale, name = 'module_comptabilite_post_update_annee_fiscale'))
urlpatterns.append(url(r'^annee_fiscale/item/(?P<ref>[0-9]+)/update$', views.get_modifier_annee_fiscale, name = 'module_comptabilite_update_annee_fiscale'))
urlpatterns.append(url(r'^local/list', views.get_lister_local, name = 'module_comptabilite_list_local'))
urlpatterns.append(url(r'^local/add', views.get_creer_local, name = 'module_comptabilite_add_local'))
urlpatterns.append(url(r'^local/post_add', views.post_creer_local, name = 'module_comptabilite_post_add_local'))
urlpatterns.append(url(r'^local/item/(?P<ref>[0-9]+)/$', views.get_details_local, name = 'module_comptabilite_detail_local'))
urlpatterns.append(url(r'^local/item/post_update/$', views.post_modifier_local, name = 'module_comptabilite_post_update_local'))
urlpatterns.append(url(r'^local/item/(?P<ref>[0-9]+)/update$', views.get_modifier_local, name = 'module_comptabilite_update_local'))
urlpatterns.append(url(r'^lettrage/list', views.get_lister_lettrage, name = 'module_comptabilite_list_lettrage'))
urlpatterns.append(url(r'^lettrage/add', views.get_creer_lettrage, name = 'module_comptabilite_add_lettrage'))
urlpatterns.append(url(r'^lettrage/post_add', views.post_creer_lettrage, name = 'module_comptabilite_post_add_lettrage'))
urlpatterns.append(url(r'^lettrage/item/(?P<ref>[0-9]+)/$', views.get_details_lettrage, name = 'module_comptabilite_detail_lettrage'))
urlpatterns.append(url(r'^lettrage/item/post_update/$', views.post_modifier_lettrage, name = 'module_comptabilite_post_update_lettrage'))
urlpatterns.append(url(r'^lettrage/item/(?P<ref>[0-9]+)/update$', views.get_modifier_lettrage, name = 'module_comptabilite_update_lettrage'))
urlpatterns.append(url(r'^compte_banque/list', views.get_lister_compte_banque, name = 'module_comptabilite_list_compte_banque'))
urlpatterns.append(url(r'^compte_banque/add', views.get_creer_compte_banque, name = 'module_comptabilite_add_compte_banque'))
urlpatterns.append(url(r'^compte_banque/post_add', views.post_creer_compte_banque, name = 'module_comptabilite_post_add_compte_banque'))
urlpatterns.append(url(r'^compte_banque/item/(?P<ref>[0-9]+)/$', views.get_details_compte_banque, name = 'module_comptabilite_detail_compte_banque'))
urlpatterns.append(url(r'^compte_banque/item/post_update/$', views.post_modifier_compte_banque, name = 'module_comptabilite_post_update_compte_banque'))
urlpatterns.append(url(r'^compte_banque/item/(?P<ref>[0-9]+)/update$', views.get_modifier_compte_banque, name = 'module_comptabilite_update_compte_banque'))
urlpatterns.append(url(r'^caisse/list', views.get_lister_caisse, name = 'module_comptabilite_list_caisse'))
urlpatterns.append(url(r'^caisse/add', views.get_creer_caisse, name = 'module_comptabilite_add_caisse'))
urlpatterns.append(url(r'^caisse/post_add', views.post_creer_caisse, name = 'module_comptabilite_post_add_caisse'))
urlpatterns.append(url(r'^caisse/item/(?P<ref>[0-9]+)/$', views.get_details_caisse, name = 'module_comptabilite_detail_caisse'))
urlpatterns.append(url(r'^caisse/item/post_update/$', views.post_modifier_caisse, name = 'module_comptabilite_post_update_caisse'))
urlpatterns.append(url(r'^caisse/item/(?P<ref>[0-9]+)/update$', views.get_modifier_caisse, name = 'module_comptabilite_update_caisse'))

urlpatterns.append(url(r'^operationtresorerie/(?P<ref>[0-9]+)/(?P<filter>[\w-]+)/list', views.get_lister_operationtresorerie, name = 'module_comptabilite_list_operationtresorerie'))
urlpatterns.append(url(r'^operationtresorerie/(?P<ref>[0-9]+)/(?P<filter>[\w-]+)/add', views.get_creer_operationtresorerie, name = 'module_comptabilite_add_operationtresorerie'))


urlpatterns.append(url(r'^operationtresorerie/post_add', views.post_creer_operationtresorerie, name = 'module_comptabilite_post_add_operationtresorerie'))
urlpatterns.append(url(r'^operationtresorerie/item/(?P<ref>[0-9]+)/$', views.get_details_operationtresorerie, name = 'module_comptabilite_detail_operationtresorerie'))
urlpatterns.append(url(r'^operationtresorerie/item/post_update/$', views.post_modifier_operationtresorerie, name = 'module_comptabilite_post_update_operationtresorerie'))
urlpatterns.append(url(r'^operationtresorerie/item/(?P<ref>[0-9]+)/update$', views.get_modifier_operationtresorerie, name = 'module_comptabilite_update_operationtresorerie'))


urlpatterns.append(url(r'^operationtresorerie/item/(?P<ref>[0-9]+)/lettrage$', views.get_creer_lettrage_operationtresorerie, name = 'module_comptabilite_add_lettrage_operationtresorerie'))
urlpatterns.append(url(r'^operationtresorerie/lettrage/post_add', views.post_creer_lettrage_operationtresorerie, name = 'module_comptabilite_post_add_lettrage_operationtresorerie'))



urlpatterns.append(url(r'^bank/list', views.get_lister_bank, name = 'module_comptabilite_list_bank'))
urlpatterns.append(url(r'^bank/add', views.get_creer_bank, name = 'module_comptabilite_add_bank'))
urlpatterns.append(url(r'^bank/post_add', views.post_creer_bank, name = 'module_comptabilite_post_add_bank'))
urlpatterns.append(url(r'^bank/item/(?P<ref>[0-9]+)/$', views.get_details_bank, name = 'module_comptabilite_detail_bank'))
urlpatterns.append(url(r'^bank/item/post_update/$', views.post_modifier_bank, name = 'module_comptabilite_post_update_bank'))
urlpatterns.append(url(r'^bank/item/(?P<ref>[0-9]+)/update$', views.get_modifier_bank, name = 'module_comptabilite_update_bank'))


urlpatterns.append(url(r'operationtresorerie/closed/(?P<ref>[0-9]+)/$', views.get_closed_operationtresorerie, name='module_comptabilite_closed_operationtresorerie'))
urlpatterns.append(url(r'^ecriture_analytique/list', views.get_lister_ecriture_analytique, name = 'module_comptabilite_list_ecriture_analytique'))
urlpatterns.append(url(r'^ecriture_analytique/add', views.get_creer_ecriture_analytique, name = 'module_comptabilite_add_ecriture_analytique'))
urlpatterns.append(url(r'^ecriture_analytique/post_add', views.post_creer_ecriture_analytique, name = 'module_comptabilite_post_add_ecriture_analytique'))
urlpatterns.append(url(r'^ecriture_analytique/item/(?P<ref>[0-9]+)/$', views.get_details_ecriture_analytique, name = 'module_comptabilite_detail_ecriture_analytique'))
urlpatterns.append(url(r'^ecriture_analytique/item/post_update/$', views.post_modifier_ecriture_analytique, name = 'module_comptabilite_post_update_ecriture_analytique'))
urlpatterns.append(url(r'^ecriture_analytique/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ecriture_analytique, name = 'module_comptabilite_update_ecriture_analytique'))


###################### RAPPORT ###############################

# generer_facture_avoir get_facture_client_extend
urlpatterns.append(url(r'^facture_avoir/add', views.generer_facture_avoir, name = 'module_comptabilite_adding_facture_avoir'))
urlpatterns.append(url(r'^facture_avoir/list', views.get_lister_factures_avoir, name='module_comptabilite_list_facture_avoir'))

urlpatterns.append(url(r'^ajax/facture', views.get_facture_client_extend, name = 'module_comptabilite_ajax_facture_extend'))
urlpatterns.append(url(r'^facture_avoir/post_add', views.post_generer_facture_avoir, name = 'module_comptabilite_post_facture_avoir'))

# OUVERTURE URLS
urlpatterns.append(url(r'^organisation/ouverture/add', views.get_creer_ouverture_organisation, name='module_comptabilite_add_ouverture_organisation'))
urlpatterns.append(url(r'^organisation/ouverture/post_add', views.post_creer_ouverture_organisation, name='module_comptabilite_post_add_ouverture_organisation'))
urlpatterns.append(url(r'^comptes/ouverture/add', views.get_creer_ouverture_compte, name='module_comptabilite_add_ouverture_compte'))
urlpatterns.append(url(r'^comptes/ouverture/post_add', views.post_creer_ouverture_compte, name='module_comptabilite_post_add_ouverture_compte'))
urlpatterns.append(url(r'^comptes/ouverture/upload', views.get_upload_ouverture_compte, name='module_comptabilite_upload_ouverture_compte'))
urlpatterns.append(url(r'^comptes/ouverture/post_upload', views.post_upload_ouverture_compte, name='module_comptabilite_post_upload_ouverture_compte'))
urlpatterns.append(url(r'^caisse/ouverture/post_add', views.post_creer_ouverture_caisse, name = 'module_comptabilite_post_add_ouverture_caisse'))
urlpatterns.append(url(r'^banque/ouverture/post_add', views.post_creer_ouverture_banque, name = 'module_comptabilite_post_add_ouverture_banque'))
urlpatterns.append(url(r'^annee_fiscale/ouverture/post_add', views.post_creer_ouverture_annee_fiscale, name='module_comptabilite_post_add_ouverture_annee_fiscale'))
urlpatterns.append(url(r'^devises/actives/list', views.get_json_list_devises_actives, name='module_comptabilite_list_devises_actives'))
urlpatterns.append(url(r'^analyse/factures/(?P<ref>[0-9]+)/$', views.get_analyse_factures, name='module_comptabilite_analyse_factures'))
urlpatterns.append(url(r'^comptabilite/cloture/periode', views.get_cloture_periode, name='module_comptabilite_cloture_periode'))
urlpatterns.append(url(r'^operation_tresorerie/billeterie/post_add', views.post_creer_billeterie_operation_budgetaire, name='module_comptabilite_post_add_billeterie_operation_budgetaire'))

urlpatterns.append(url(r'^rapport/operationtresorerie/',views.get_rapport_sur_ligne_operation_tresorerie, name='module_comptabilite_rapport_operationtresorerie'))
urlpatterns.append(url(r'^all_rapport/operationtresorerie/all', views.get_rapport_operationtresorerie,name='module_comptabilite_get_rapport_operationtresorerie'))

urlpatterns.append(url(r'^compte_analytique/list', views.get_lister_compte_analytique, name = 'module_comptabilite_list_compte_analytique'))
urlpatterns.append(url(r'^compte_analytique/add', views.get_creer_compte_analytique, name = 'module_comptabilite_add_compte_analytique'))
urlpatterns.append(url(r'^compte_analytique/post_add', views.post_creer_compte_analytique, name = 'module_comptabilite_post_add_compte_analytique'))
urlpatterns.append(url(r'^compte_analytique/item/(?P<ref>[0-9]+)/$', views.get_details_compte_analytique, name = 'module_comptabilite_detail_compte_analytique'))
urlpatterns.append(url(r'^compte_analytique/item/post_update/$', views.post_modifier_compte_analytique, name = 'module_comptabilite_post_update_compte_analytique'))
urlpatterns.append(url(r'^compte_analytique/item/(?P<ref>[0-9]+)/update$', views.get_modifier_compte_analytique, name = 'module_comptabilite_update_compte_analytique'))

urlpatterns.append(url(r'^groupeanalytique/list', views.get_lister_groupeanalytique, name = 'module_comptabilite_list_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/add', views.get_creer_groupeanalytique, name = 'module_comptabilite_add_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/post_add', views.post_creer_groupeanalytique, name = 'module_comptabilite_post_add_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/(?P<ref>[0-9]+)/$', views.get_details_groupeanalytique, name = 'module_comptabilite_detail_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/post_update/$', views.post_modifier_groupeanalytique, name = 'module_comptabilite_post_update_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/(?P<ref>[0-9]+)/update$', views.get_modifier_groupeanalytique, name = 'module_comptabilite_update_groupeanalytique'))

urlpatterns.append(url(r'^ordre_paiement/list', views.get_lister_ordre_paiement, name = 'module_comptabilite_list_ordre_paiement'))
urlpatterns.append(url(r'^ordre_paiement/add', views.get_creer_ordre_paiement, name = 'module_comptabilite_add_ordre_paiement'))
urlpatterns.append(url(r'^ordre_paiement/post_add', views.post_creer_ordre_paiement, name = 'module_comptabilite_post_add_ordre_paiement'))
urlpatterns.append(url(r'^ordre_paiement/item/(?P<ref>[0-9]+)/$', views.get_details_ordre_paiement, name = 'module_comptabilite_detail_ordre_paiement'))
urlpatterns.append(url(r'^ordre_paiement/item/post_update/$', views.post_modifier_ordre_paiement, name = 'module_comptabilite_post_update_ordre_paiement'))
urlpatterns.append(url(r'^ordre_paiement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ordre_paiement, name = 'module_comptabilite_update_ordre_paiement'))

urlpatterns.append(url(r'^ordre_paiement/print/item/(?P<ref>[0-9]+)/$', views.post_imprimer_ordre_paiement, name = 'module_comptabilite_post_imprimer_ordre_paiement'))

urlpatterns.append(url(r'^ordre_paiement/paiement/add', views.get_creer_paiement_of_ordre_paiement, name = 'module_comptabilite_add_paiment_of_ordre_paiement'))
urlpatterns.append(url(r'^ordre_paiement/paiement/post_add', views.post_creer_paiement_of_ordre_paiement, name = 'module_comptabilite_post_add_paiment_of_ordre_paiement'))

