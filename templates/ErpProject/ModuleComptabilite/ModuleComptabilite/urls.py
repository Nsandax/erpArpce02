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

    #NOTES CAS PAR CAS

    #Note 1
    url(r'^annexe/note1/list', views.get_details_note_annexe_1, name='module_comptabilite_list_note_cas_1'),
    url(r'^annexe/cas_1', views.post_imprimer_cas_1, name='module_comptabilite_imprimer_cas_1'),

    #Note 2
    url(r'^annexe/note2/list', views.get_details_note_annexe_2, name='module_comptabilite_list_note_cas_2'),
    url(r'^annexe/cas_2/print', views.post_imprimer_cas_2, name='module_comptabilite_print_cas_2'),

    #Note 3
    url(r'^annexe/note3/list', views.get_details_note_annexe_3, name='module_comptabilite_list_note_cas_3'),
    url(r'^annexe/imprime/cas_3', views.post_imprimer_cas_3, name='module_comptabilite_imprimer_modele_3'),

    #Note 3B
    url(r'^annexe/note3B/list', views.get_details_note_annexe_3B, name='module_comptabilite_list_note_cas_3B'),
    url(r'^annexe/imprime3B/cas_3B', views.post_imprimer_cas_3B, name='module_comptabilite_imprimer_modele_3B'),

    #Note 3C
    url(r'^annexe/note3C/list', views.get_details_note_annexe_3C, name='module_comptabilite_list_note_cas_3C'),
    url(r'^annexe/imprime3C/cas_3C', views.post_imprimer_cas_3C, name='module_comptabilite_imprimer_modele_3C'),

    #Note 3D
    url(r'^annexe/note3D/list', views.get_details_note_annexe_3D, name='module_comptabilite_list_note_cas_3D'),
    url(r'^annexe/imprime3D/cas_3D', views.post_imprimer_cas_3D, name='module_comptabilite_imprimer_modele_3D'),

    #Note 3E
    url(r'^annexe/note3E/list', views.get_details_note_annexe_3E, name='module_comptabilite_list_note_cas_3E'),
    url(r'^annexe/imprime3E/cas_3E', views.post_imprimer_cas_3E, name='module_comptabilite_imprimer_modele_3E'),

    #Note 4
    url(r'^annexe/note4/list', views.get_details_note_annexe_4, name='module_comptabilite_list_note_cas_4'),
    url(r'^annexe/imprime4/cas_4', views.post_imprimer_cas_4, name='module_comptabilite_imprimer_modele_4'),

    #Note 5
    url(r'^annexe/note5/list', views.get_details_note_annexe_5, name='module_comptabilite_list_note_cas_5'),
    url(r'^annexe/imprime5/cas_5', views.post_imprimer_cas_5, name='module_comptabilite_imprimer_modele_5'),

    #Note 6
    url(r'^annexe/note6/list', views.get_details_note_annexe_6, name='module_comptabilite_list_note_cas_6'),
    url(r'^annexe/imprime6/cas_6', views.post_imprimer_cas_6, name='module_comptabilite_imprimer_modele_6'),

    #Note 7
    url(r'^annexe/note7/list', views.get_details_note_annexe_7, name='module_comptabilite_list_note_cas_7'),
    url(r'^annexe/imprime7/cas_7', views.post_imprimer_cas_7, name='module_comptabilite_imprimer_modele_7'),

    #Note 8
    url(r'^annexe/note8/list', views.get_details_note_annexe_8, name='module_comptabilite_list_note_cas_8'),
    url(r'^annexe/imprime8/cas_8', views.post_imprimer_cas_8, name='module_comptabilite_imprimer_modele_8'),

    #Note 9
    url(r'^annexe/note9/list', views.get_details_note_annexe_9, name='module_comptabilite_list_note_cas_9'),
    url(r'^annexe/imprime9/cas_9', views.post_imprimer_cas_9, name='module_comptabilite_imprimer_modele_9'),

    #Note 10
    url(r'^annexe/note10/list', views.get_details_note_annexe_10, name='module_comptabilite_list_note_cas_10'),
    url(r'^annexe/imprime10/cas_10', views.post_imprimer_cas_10, name='module_comptabilite_imprimer_modele_10'),

    #Note 11
    url(r'^annexe/note11/list', views.get_details_note_annexe_11, name='module_comptabilite_list_note_cas_11'),
    url(r'^annexe/imprime11/cas_11', views.post_imprimer_cas_11, name='module_comptabilite_imprimer_modele_11'),

    #Note 12
    url(r'^annexe/note12/list', views.get_details_note_annexe_12, name='module_comptabilite_list_note_cas_12'),
    url(r'^annexe/imprime12/cas_12', views.post_imprimer_cas_12, name='module_comptabilite_imprimer_modele_12'),

    #Note 13
    url(r'^annexe/note13/list', views.get_details_note_annexe_13, name='module_comptabilite_list_note_cas_13'),
    url(r'^annexe/imprime13/cas_13', views.post_imprimer_cas_13, name='module_comptabilite_imprimer_modele_13'),

    #Note 14
    url(r'^annexe/note14/list', views.get_details_note_annexe_14, name='module_comptabilite_list_note_cas_14'),
    url(r'^annexe/imprime14/cas_14', views.post_imprimer_cas_14, name='module_comptabilite_imprimer_modele_14'),

    #Note 15
    url(r'^annexe/note15/list', views.get_details_note_annexe_15, name='module_comptabilite_list_note_cas_15'),
    url(r'^annexe/imprime15/cas_15', views.post_imprimer_cas_15, name='module_comptabilite_imprimer_modele_15'),

    #Note 15B
    url(r'^annexe/note15B/list', views.get_details_note_annexe_15B, name='module_comptabilite_list_note_cas_15B'),
    url(r'^annexe/imprime15B/cas_15B', views.post_imprimer_cas_15B, name='module_comptabilite_imprimer_modele_15B'),

    #Note 16A
    url(r'^annexe/note16A/list', views.get_details_note_annexe_16A, name='module_comptabilite_list_note_cas_16A'),
    url(r'^annexe/imprime16A/cas_16A', views.post_imprimer_cas_16A, name='module_comptabilite_imprimer_modele_16A'),

    #Note 16B
    url(r'^annexe/note16B/list', views.get_details_note_annexe_16B, name='module_comptabilite_list_note_cas_16B'),
    url(r'^annexe/imprime16B/cas_16B', views.post_imprimer_cas_16B, name='module_comptabilite_imprimer_modele_16B'),

    #Note 16C
    url(r'^annexe/note16C/list', views.get_details_note_annexe_16C, name='module_comptabilite_list_note_cas_16C'),
    url(r'^annexe/imprime16C/cas_16C', views.post_imprimer_cas_16C, name='module_comptabilite_imprimer_modele_16C'),

    #Note 17
    url(r'^annexe/note17/list', views.get_details_note_annexe_17, name='module_comptabilite_list_note_cas_17'),
    url(r'^annexe/imprime17/cas_17', views.post_imprimer_cas_17, name='module_comptabilite_imprimer_modele_17'),

    #Note 18
    url(r'^annexe/note18/list', views.get_details_note_annexe_18, name='module_comptabilite_list_note_cas_18'),
    url(r'^annexe/imprime18/cas_18', views.post_imprimer_cas_18, name='module_comptabilite_imprimer_modele_18'),

    #Note 19
    url(r'^annexe/note19/list', views.get_details_note_annexe_19, name='module_comptabilite_list_note_cas_19'),
    url(r'^annexe/imprime19/cas_19', views.post_imprimer_cas_19, name='module_comptabilite_imprimer_modele_19'),

    #Note 20
    url(r'^annexe/note20/list', views.get_details_note_annexe_20, name='module_comptabilite_list_note_cas_20'),
    url(r'^annexe/imprime20/cas_20', views.post_imprimer_cas_20, name='module_comptabilite_imprimer_modele_20'),

    #Note 21
    url(r'^annexe/note21/list', views.get_details_note_annexe_21, name='module_comptabilite_list_note_cas_21'),
    url(r'^annexe/imprime21/cas_21', views.post_imprimer_cas_21, name='module_comptabilite_imprimer_modele_21'),

    #Note 22
    url(r'^annexe/note22/list', views.get_details_note_annexe_22, name='module_comptabilite_list_note_cas_22'),
    url(r'^annexe/imprime22/cas_22', views.post_imprimer_cas_22, name='module_comptabilite_imprimer_modele_22'),

    #Note 23
    url(r'^annexe/note23/list', views.get_details_note_annexe_23, name='module_comptabilite_list_note_cas_23'),
    url(r'^annexe/imprime23/cas_23', views.post_imprimer_cas_23, name='module_comptabilite_imprimer_modele_23'),

    #Note 24
    url(r'^annexe/note24/list', views.get_details_note_annexe_24, name='module_comptabilite_list_note_cas_24'),
    url(r'^annexe/imprime24/cas_24', views.post_imprimer_cas_24, name='module_comptabilite_imprimer_modele_24'),

    #Note 25
    url(r'^annexe/note25/list', views.get_details_note_annexe_25, name='module_comptabilite_list_note_cas_25'),
    url(r'^annexe/imprime25/cas_25', views.post_imprimer_cas_25, name='module_comptabilite_imprimer_modele_25'),

    #Note 26
    url(r'^annexe/note26/list', views.get_details_note_annexe_26, name='module_comptabilite_list_note_cas_26'),
    url(r'^annexe/imprime26/cas_26', views.post_imprimer_cas_26, name='module_comptabilite_imprimer_modele_26'),

    #Note 27A
    url(r'^annexe/note27/list', views.get_details_note_annexe_27, name='module_comptabilite_list_note_cas_27'),
    url(r'^annexe/imprime27/cas_27', views.post_imprimer_cas_27, name='module_comptabilite_imprimer_modele_27'),

    #Note 27B
    url(r'^annexe/note27B/list', views.get_details_note_annexe_27B, name='module_comptabilite_list_note_cas_27B'),
    url(r'^annexe/imprime27B/cas_27B', views.post_imprimer_cas_27B, name='module_comptabilite_imprimer_modele_27B'),

    #Note 28
    url(r'^annexe/note28/list', views.get_details_note_annexe_28, name='module_comptabilite_list_note_cas_28'),
    url(r'^annexe/imprime28/cas_28', views.post_imprimer_cas_28, name='module_comptabilite_imprimer_modele_28'),

    #Note 29
    url(r'^annexe/note29/list', views.get_details_note_annexe_29, name='module_comptabilite_list_note_cas_29'),
    url(r'^annexe/imprime29/cas_29', views.post_imprimer_cas_29, name='module_comptabilite_imprimer_modele_29'),

    #Note 30
    url(r'^annexe/note30/list', views.get_details_note_annexe_30, name='module_comptabilite_list_note_cas_30'),
    url(r'^annexe/imprime30/cas_30', views.post_imprimer_cas_30, name='module_comptabilite_imprimer_modele_30'),

    #Note 31
    url(r'^annexe/note31/list', views.get_details_note_annexe_31, name='module_comptabilite_list_note_cas_31'),
    url(r'^annexe/imprime31/cas_31', views.post_imprimer_cas_31, name='module_comptabilite_imprimer_modele_31'),

    #Note 32
    url(r'^annexe/note32/list', views.get_details_note_annexe_32, name='module_comptabilite_list_note_cas_32'),
    url(r'^annexe/imprime32/cas_32', views.post_imprimer_cas_32, name='module_comptabilite_imprimer_modele_32'),

    #Note 33
    url(r'^annexe/note33/list', views.get_details_note_annexe_33, name='module_comptabilite_list_note_cas_33'),
    url(r'^annexe/imprime33/cas_33', views.post_imprimer_cas_33, name='module_comptabilite_imprimer_modele_33'),

    #Note 34
    url(r'^annexe/note34/list', views.get_details_note_annexe_34, name='module_comptabilite_list_note_cas_34'),
    url(r'^annexe/imprime34/cas_34', views.post_imprimer_cas_34, name='module_comptabilite_imprimer_modele_34'),

    #Note 35
    url(r'^annexe/note35/list', views.get_details_note_annexe_35, name='module_comptabilite_list_note_cas_35'),
    url(r'^annexe/imprime35/cas_35', views.post_imprimer_cas_35, name='module_comptabilite_imprimer_modele_35'),

    #Note 36
    url(r'^annexe/note36/list', views.get_details_note_annexe_36, name='module_comptabilite_list_note_cas_36'),
    url(r'^annexe/imprime36/cas_36', views.post_imprimer_cas_36, name='module_comptabilite_imprimer_modele_36'),


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

