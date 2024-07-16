from django.conf.urls import include, url
from . import views
urlpatterns = [
        url(r'^$', views.get_dashboard, name='module_payroll_tableau'),
        url(r'^tableau', views.get_dashboard, name='module_payroll_tableau_de_bord'),

        url(r'process_calcul_payment', views.post_calcul_paie, name='module_payroll_process_calcul_payment'),
        url(r'process_cloture', views.post_cloture_dossier_paie, name='module_payroll_process_cloture'),

        url(r'activer_lot_bulletin', views.post_activer_lot_bulletin, name='module_payroll_activer_lot_bulletin'),
        url(r'generate_ecriture_comptable', views.post_generer_ecriture_comptable, name='module_payroll_generer_ecriture_comptable'),


        url(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status'),

        url(r'^pret/item/validate', views.post_valider_pret_payroll, name='module_payroll_validate_pret'),

        # CONFIGURATIONS URLS
        url(r'^configuration/update', views.get_modifier_parametre_payroll, name='module_payroll_modifier_configuration'),
        url(r'^configuration/post_update', views.post_modifier_parametre_payroll, name='module_payroll_post_modifier_configuration'),
]

# LOT BULLETIN URLS
urlpatterns.append(url(r'^lotbulletin/list', views.get_lister_lotbulletin, name='module_payroll_list_lotbulletin'))
urlpatterns.append(url(r'^lotbulletin/add', views.get_creer_lotbulletin, name='module_payroll_add_lotbulletin'))
urlpatterns.append(url(r'^lotbulletin/post_add', views.post_creer_lotbulletin, name='module_payroll_post_add_lotbulletin'))
urlpatterns.append(url(r'^lotbulletin/item/(?P<ref>[0-9]+)/update$', views.get_modifier_lotbulletin, name='module_payroll_update_lotbulletin'))
urlpatterns.append(url(r'^lotbulletin/post_update', views.post_modifier_lotbulletin, name='module_payroll_post_update_lotbulletin'))
urlpatterns.append(url(r'^lotbulletin/item/(?P<ref>[0-9]+)/$', views.get_details_lotbulletin, name='module_payroll_details_lotbulletin'))
urlpatterns.append(url(r'^lotbulletin/calcul/paye/(?P<ref>[0-9]+)/$', views.get_calcul_paie_dossier, name='module_payroll_calcul_dossier_paie'))
urlpatterns.append(url(r'^lignelotbulletin/generate', views.post_generer_lignes_lot, name='module_payroll_post_generer_ligne_lot'))

urlpatterns.append(url(r'^lotbulletin/print/(?P<ref>[0-9]+)/$', views.post_generer_lot_bulletin, name='module_payroll_post_generer_lot_bulletin'))

# BULLETIN URLS
urlpatterns.append(url(r'^bulletin/list', views.get_lister_bulletin, name='module_payroll_list_bulletin'))
urlpatterns.append(url(r'^bulletin/add', views.get_creer_bulletin, name='module_payroll_add_bulletin'))
urlpatterns.append(url(r'^bulletin/post', views.post_creer_bulletin, name='module_payroll_post_add_bulletin'))
urlpatterns.append(url(r'^bulletin/generate', views.post_generer_bulletin, name='module_payroll_post_generer_bulletin'))
urlpatterns.append(url(r'^bulletin/item/(?P<ref>[0-9]+)/$', views.get_details_bulletin, name='module_payroll_details_bulletin'))
urlpatterns.append(url(r'^bulletin/recalcul/(?P<ref>[0-9]+)/$', views.get_recalcul_paie_bulletin, name='module_payroll_recalcul_bulletin'))

urlpatterns.append(url(r'^bulletin/printing/(?P<ref>[0-9]+)/$', views.post_printing_Bulletin_paie, name='module_payroll_post_printing_Bulletin_paie'))

# ELEMENT BULLETIN URLS
urlpatterns.append(url(r'^element/list', views.get_lister_element, name='module_payroll_list_element'))
urlpatterns.append(url(r'^element/add', views.get_creer_element, name='module_payroll_add_element'))
urlpatterns.append(url(r'^element/post_add', views.post_creer_element, name='module_payroll_post_add_element'))
urlpatterns.append(url(r'^element/item/(?P<ref>[0-9]+)/$', views.get_details_element, name='module_payroll_details_element'))

# BAREME URLS
urlpatterns.append(url(r'^bareme/list', views.get_lister_bareme, name='module_payroll_list_bareme'))
urlpatterns.append(url(r'^bareme/add', views.get_creer_bareme, name='module_payroll_add_bareme'))
urlpatterns.append(url(r'^bareme/post_add', views.post_creer_bareme, name='module_payroll_post_add_bareme'))
urlpatterns.append(url(r'^bareme/item/(?P<ref>[0-9]+)/$', views.get_details_bareme, name='module_payroll_details_bareme'))

# PROFIL PAIE URLS
urlpatterns.append(url(r'^profilpaie/list', views.get_lister_profilpaie, name='module_payroll_list_profilpaie'))
urlpatterns.append(url(r'^profilpaie/add', views.get_creer_profilpaie, name='module_payroll_add_profilpaie'))
urlpatterns.append(url(r'^profilpaie/post_add', views.post_creer_profilpaie, name='module_payroll_post_add_profilpaie'))
urlpatterns.append(url(r'^profilpaie/item/(?P<ref>[0-9]+)/$', views.get_details_profilpaie, name='module_payroll_details_profilpaie'))
urlpatterns.append(url(r'^calcul/paye/(?P<ref>[0-9]+)/$', views.get_calcul_paie_employe, name='module_payroll_calcul_paie'))

# EMPLOYE URLS
urlpatterns.append(url(r'^salarie/list', views.get_list_salarie, name='module_payroll_list_salarie'))
urlpatterns.append(url(r'^salarie/item/(?P<ref>[0-9]+)/$', views.get_details_salarie, name = 'module_payroll_detail_employe'))

# TYPE STRUCTURE SALARIALE URLS
urlpatterns.append(url(r'^type_structure/list', views.get_lister_type_structure, name = 'module_payroll_list_type_structure'))
urlpatterns.append(url(r'^type_structure/add', views.get_creer_type_structure, name = 'module_payroll_add_type_structure'))
urlpatterns.append(url(r'^type_structure/item/(?P<ref>[0-9]+)/$', views.get_details_type_structure, name = 'module_payroll_details_type_structure'))
urlpatterns.append(url(r'^type_structure/post_add', views.post_creer_type_structure, name = 'module_payroll_post_add_type_structure'))
urlpatterns.append(url(r'^type_structure/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_structure, name = 'module_payroll_update_type_structure'))
urlpatterns.append(url(r'^type_structure/post_update', views.post_modifier_type_structure, name = 'module_payroll_post_update_type_structure'))

urlpatterns.append(url(r'^type_structure/upload/add', views.get_upload_type_structure, name='module_payroll_get_upload_type_structure'))
urlpatterns.append(url(r'^type_structure/upload/post_add', views.post_upload_type_structure, name='module_payroll_post_upload_type_structure'))

# STRUCTURE SALARIALE URLS
urlpatterns.append(url(r'^structure_salariale/list', views.get_lister_structure_salariale, name='module_payroll_list_structure_salariale'))
urlpatterns.append(url(r'^structure_salariale/add', views.get_creer_structure_salariale, name='module_payroll_add_structure_salariale'))
urlpatterns.append(url(r'^structure_salariale/post_add', views.post_creer_structure_salariale, name='module_payroll_post_add_structure_salariale'))
urlpatterns.append(url(r'^structure_salariale/item/(?P<ref>[0-9]+)/$', views.get_details_structure_salariale, name='module_payroll_details_structure_salariale'))
urlpatterns.append(url(r'^structure_salariale/item/(?P<ref>[0-9]+)/update$', views.get_modifier_structure_salariale, name = 'module_payroll_update_structure_salariale'))
urlpatterns.append(url(r'^structure_salariale/post_update', views.post_modifier_structure_salariale, name = 'module_payroll_post_update_structure_salariale'))

# CATEGORIE REGLE SALARIALE URLS
urlpatterns.append(url(r'^categorie_regle/list', views.get_lister_categorie_regle, name = 'module_payroll_list_categorie_regle'))
urlpatterns.append(url(r'^categorie_regle/add', views.get_creer_categorie_regle, name = 'module_payroll_add_categorie_regle'))
urlpatterns.append(url(r'^categorie_regle/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_regle, name = 'module_payroll_details_categorie_regle'))
urlpatterns.append(url(r'^categorie_regle/post_add', views.post_creer_categorie_regle, name = 'module_payroll_post_add_categorie_regle'))
urlpatterns.append(url(r'^categorie_regle/item/(?P<ref>[0-9]+)/update$', views.get_modifier_categorie_regle, name = 'module_payroll_update_categorie_regle'))
urlpatterns.append(url(r'^categorie_regle/post_update', views.post_modifier_categorie_regle, name = 'module_payroll_post_update_categorie_regle'))

urlpatterns.append(url(r'^categorie_regle/upload/add', views.get_upload_categorie_regle, name='module_payroll_get_upload_categorie_regle'))
urlpatterns.append(url(r'^categorie_regle/upload/post_add', views.post_upload_categorie_regle, name='module_payroll_post_upload_categorie_regle'))

# REGLE SALARIALE URLS
urlpatterns.append(url(r'^regle_salariale/list', views.get_lister_regle_salariale, name = 'module_payroll_list_regle_salariale'))
urlpatterns.append(url(r'^regle_salariale/add', views.get_creer_regle_salariale, name = 'module_payroll_add_regle_salariale'))
urlpatterns.append(url(r'^regle_salariale/item/(?P<ref>[0-9]+)/$', views.get_details_regle_salariale, name = 'module_payroll_details_regle_salariale'))
urlpatterns.append(url(r'^regle_salariale/post_add', views.post_creer_regle_salariale, name = 'module_payroll_post_add_regle_salariale'))
urlpatterns.append(url(r'^regle_salariale/item/(?P<ref>[0-9]+)/update$', views.get_modifier_regle_salariale, name = 'module_payroll_update_regle_salariale'))
urlpatterns.append(url(r'^regle_salariale/post_update', views.post_modifier_regle_salariale, name = 'module_payroll_post_update_regle_salariale'))


# RUBRIQUE URLS
urlpatterns.append(url(r'^rubrique/list', views.get_lister_rubrique, name = 'module_payroll_list_rubrique'))
urlpatterns.append(url(r'^rubrique/add', views.get_creer_rubrique, name = 'module_payroll_add_rubrique'))
urlpatterns.append(url(r'^rubrique/item/(?P<ref>[0-9]+)/$', views.get_details_rubrique, name = 'module_payroll_details_rubrique'))
urlpatterns.append(url(r'^rubrique/post_add', views.post_creer_rubrique, name = 'module_payroll_post_add_rubrique'))
urlpatterns.append(url(r'^rubrique/item/(?P<ref>[0-9]+)/update$', views.get_modifier_rubrique, name = 'module_payroll_update_rubrique'))
urlpatterns.append(url(r'^rubrique/post_update', views.post_modifier_rubrique, name = 'module_payroll_post_update_rubrique'))

# CONSTANTE URLS
urlpatterns.append(url(r'^constante/list', views.get_lister_constante, name = 'module_payroll_list_constante'))
urlpatterns.append(url(r'^constante/add', views.get_creer_constante, name = 'module_payroll_add_constante'))
urlpatterns.append(url(r'^constante/item/(?P<ref>[0-9]+)/$', views.get_details_constante, name = 'module_payroll_details_constante'))
urlpatterns.append(url(r'^constante/type/post_add', views.post_creer_choix_constante, name = 'module_payroll_post_add_choice_constante'))
urlpatterns.append(url(r'^constante/post_add', views.post_creer_constante, name = 'module_payroll_post_add_constante'))
urlpatterns.append(url(r'^constante/item/(?P<ref>[0-9]+)/update$', views.get_modifier_constante, name = 'module_payroll_update_constante'))
urlpatterns.append(url(r'^constante/post_update', views.post_modifier_constante, name = 'module_payroll_post_update_constante'))

# BULLETIN MODELE URLS
urlpatterns.append(url(r'^modele_bulletin/list', views.get_lister_modele_bulletin, name='module_payroll_list_modele_bulletin'))
urlpatterns.append(url(r'^modele_bulletin/add', views.get_creer_modele_bulletin, name='module_payroll_add_modele_bulletin'))
urlpatterns.append(url(r'^modele_bulletin/post_add', views.post_creer_modele_bulletin, name='module_payroll_post_add_modele_bulletin'))
urlpatterns.append(url(r'^modele_bulletin/item/(?P<ref>[0-9]+)/$', views.get_details_modele_bulletin, name='module_payroll_details_modele_bulletin'))
urlpatterns.append(url(r'^modele_bulletin/item/(?P<ref>[0-9]+)/update$', views.get_modifier_modele_bulletin, name = 'module_payroll_update_modele_bulletin'))
urlpatterns.append(url(r'^modele_bulletin/post_update', views.post_modifier_modele_bulletin, name = 'module_payroll_post_update_modele_bulletin'))

# ANALYSE PAYROLL
urlpatterns.append(url(r'^analyse/payroll', views.get_analyse_payroll, name='module_payroll_analyse_payrol'))

# DECLARATION NOMINATIVE URLS
urlpatterns.append(url(r'^declaration_nominative/add', views.get_add_declaration_nominative, name='module_payroll_add_declaration_nominative'))
urlpatterns.append(url(r'^declaration_nominative/generated', views.post_generated_declaration_nominative, name='module_payroll_generated_declaration_nominative'))

# ETAT IMPOT URLS
urlpatterns.append(url(r'^etat_impot/add', views.get_add_etat_impot, name='module_payroll_add_etat_impot'))
urlpatterns.append(url(r'^etat_impot/generated', views.post_generated_etat_impot, name='module_payroll_generated_etat_impot'))

# PRET URLS
urlpatterns.append(url(r'^pret/list', views.get_lister_prets_payroll, name='module_payroll_list_pret'))
urlpatterns.append(url(r'^pret/add', views.get_creer_pret_payroll, name='module_payroll_add_pret'))
urlpatterns.append(url(r'^pret/post_add', views.post_creer_pret_payroll, name='module_payroll_post_add_pret'))
urlpatterns.append(url(r'^pret/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_pret_payroll, name='module_payroll_update_pret'))
urlpatterns.append(url(r'^pret/item/post_update/$', views.post_modifier_pret_payroll, name='module_payroll_post_update_pret'))
urlpatterns.append(url(r'^pret/item/(?P<ref>[0-9]+)/$', views.get_details_pret_payroll, name='module_payroll_details_pret'))

# PAIEMENT INTERNE URLS
urlpatterns.append(url(r'^paiement/list', views.get_lister_paiement_internes, name='module_payroll_list_paiement_interne'))
urlpatterns.append(url(r'^paiement/item/(?P<ref>[0-9]+)/$', views.get_details_paiement_interne, name='module_payroll_details_paiement_interne'))
#urlpatterns.append(url(r'^paiement/alloc/add/(?P<ref>[0-9]+)/$', views.get_paiement_allocation, name='module_payroll_add_paiement_allocation'))
urlpatterns.append(url(r'^paiement/alloc/post_add', views.post_paiement_allocation, name='module_payroll_post_add_paiement_allocation'))
#urlpatterns.append(url(r'^paiement/pret/add/(?P<ref>[0-9]+)/$', views.get_paiement_pret, name='module_payroll_add_paiement_pret'))
urlpatterns.append(url(r'^paiement/pret/post_add', views.post_paiement_pret, name='module_payroll_post_add_paiement_pret'))

#GENERATE RAPPORT
urlpatterns.append(url(r'^rapport/balance_paie/generate', views.get_generer_balance_paie, name='module_payroll_generate_Balance_paie'))
urlpatterns.append(url(r'^rapport/bulletin_individuel/generate', views.get_generer_Bulletin_individuel, name='module_payroll_generate_Billetin_individuel'))
urlpatterns.append(url(r'^rapport/paiement_salaire/generate', views.get_generer_Paiement_salaire, name='module_payroll_generate_Paiement_salaire'))
urlpatterns.append(url(r'^rapport/prelevement_sur_salaire/generate', views.get_generer_Prelevement_sur_salaire, name='module_payroll_generate_Prelevement_sur_salaire'))
urlpatterns.append(url(r'^rapport/provision_conge/generate', views.get_generer_Provision_conge, name='module_payroll_generate_Provision_conge'))
urlpatterns.append(url(r'^rapport/provision_depart_retraite/generate', views.get_generer_Provision_depart_retraite, name='module_payroll_generate_Provision_depart_retraite'))
urlpatterns.append(url(r'^rapport/bulletin_paie/generate', views.get_generer_Bulletin_paie, name='module_payroll_generate_Bulletin_paie'))
urlpatterns.append(url(r'^rapport/caisse/generate', views.get_generer_caisse, name='module_payroll_generate_caisse'))
urlpatterns.append(url(r'^rapport/journal_compa/generate', views.get_generer_journal_comp, name='module_payroll_get_generer_journal_comp'))
urlpatterns.append(url(r'^rapport/journalglobal/generate', views.get_generer_journal_global, name='module_payroll_get_generer_journal_global'))



#POST GENERATED RAPPORT
urlpatterns.append(url(r'^balance_paie/post_generate', views.post_generer_balance_paie, name='module_payroll_post_generer_Balance_paie'))
urlpatterns.append(url(r'^provision_conge/post_generate', views.post_generer_provision_conge, name='module_payroll_post_generer_Provision_conge'))
urlpatterns.append(url(r'^Provision_depart_retraite/post_generate', views.post_generer_Provision_depart_retraite, name='module_payroll_post_generer_Provision_depart_retraite'))
urlpatterns.append(url(r'^Paiement_salaire/post_generate', views.post_generer_Paiement_salaire, name='module_payroll_post_generer_Paiement_salaire'))
urlpatterns.append(url(r'^Prelevement_sur_salaire/post_generate', views.post_generer_Prelevement_sur_salaire, name='module_payroll_post_generer_Prelevement_sur_salaire'))
urlpatterns.append(url(r'^bulletin/print/(?P<ref>[0-9]+)/$', views.post_generer_Bulletin_paie, name='module_payroll_post_generer_Bulletin_paie'))
urlpatterns.append(url(r'^caisse/post_generate', views.post_generer_caisse, name='module_payroll_post_generer_caisse'))

urlpatterns.append(url(r'^journal/post_generate', views.post_generer_journal_comp, name='module_payroll_post_generer_journal_comp'))
urlpatterns.append(url(r'^journalglobal/post_generate', views.post_generer_journalglobal_paie, name='module_payroll_post_generer_journalglobal_paie'))
urlpatterns.append(url(r'^bulletin_individuel/post_generate', views.post_generer_bulletin_individuel, name='module_payroll_post_bulletin_individuel'))
urlpatterns.append(url(r'^dossier_paie/list', views.get_lister_dossier_paie, name = 'module_payroll_list_dossier_paie'))
urlpatterns.append(url(r'^dossier_paie/ouverture/post_add', views.post_creer_dossier_paie, name = 'module_payroll_post_add_dossier_paie'))
urlpatterns.append(url(r'^dossier_paie/item/(?P<ref>[0-9]+)/$', views.get_details_dossier_paie, name = 'module_payroll_detail_dossier_paie'))


#PRINTING LINK
urlpatterns.append(url(r'^declaration_nom/print/post_generate', views.to_print_declaration_nom, name='module_payroll_to_print_declaration_nom'))
urlpatterns.append(url(r'^etat_impot/print/post_generate', views.to_print_etat_impot, name='module_payroll_to_print_etat_impot'))
urlpatterns.append(url(r'^paiement_sal/print/post_generate', views.to_print_paiement_sal, name='module_payroll_to_print_paiement_sal'))
urlpatterns.append(url(r'^prelevement_salaire/print/post_generate', views.to_Prelevement_sur_salaire_print, name='module_payroll_to_Prelevement_sur_salaire_print'))
urlpatterns.append(url(r'^provision_conge/print/post_generate', views.to_print_provision_conge, name='module_payroll_to_print_provision_conge'))
urlpatterns.append(url(r'^provision_depart_retrt/print/post_generate', views.to_print_provision_depart_retrt, name='module_payroll_to_print_provision_depart_retrt'))
urlpatterns.append(url(r'^provision_depart_caisse_virement/print/post_generate', views.to_print_provision_depart_caisse_virement, name='module_payroll_to_print_provision_depart_caisse_virement'))
urlpatterns.append(url(r'^caisse/print/post_generate', views.to_print_caisse, name='module_payroll_to_print_caisse'))
urlpatterns.append(url(r'^bulletin_individuel/print/post_generate', views.to_print_bulletin_individuel, name='module_payroll_to_print_bulletin_individuel'))
urlpatterns.append(url(r'^balance/print/post_generate', views.to_print_balance_paie, name='module_payroll_to_print_balance_paie'))

urlpatterns.append(url(r'^journal/print/post_generate', views.to_print_journal_comparatif, name='module_payroll_to_print_journal_comparatif'))
urlpatterns.append(url(r'^journalglobal/print/post_generated', views.to_print_journal_global, name='module_payroll_to_print_journal_global'))
# urlpatterns.append(url(r'^periodepaie/add', views.get_creer_periodepaie, name = 'module_payroll_add_periodepaie'))
# urlpatterns.append(url(r'^periodepaie/post_add', views.post_creer_periodepaie, name = 'module_payroll_post_add_periodepaie'))
# urlpatterns.append(url(r'^periodepaie/item/(?P<ref>[0-9]+)/$', views.get_details_periodepaie, name = 'module_payroll_detail_periodepaie'))
# urlpatterns.append(url(r'^periodepaie/item/post_update/$', views.post_modifier_periodepaie, name = 'module_payroll_post_update_periodepaie'))
# urlpatterns.append(url(r'^periodepaie/item/(?P<ref>[0-9]+)/update$', views.get_modifier_periodepaie, name = 'module_payroll_update_periodepaie'))