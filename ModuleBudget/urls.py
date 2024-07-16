from django.conf.urls import include, url, handler404, handler500
from . import views
from rest_framework import routers

"""
rest_framework nous permet de réaliser plusieurs choses. Et dans ce cas, il nous permettra de créer des
router avec 'routers' pour permettre d'afficher nos viewset.

Il sera utilisé si api est appelé dans l'url.
"""

router = routers.DefaultRouter()
router.register(r'budget', views.BudgetViewSet)
router.register(r'ligne_budgetaire', views.LigneBudgetaireViewSet)

urlpatterns=[
    # DASHBOARD URL
    url(r'^tableau', views.get_tableau_de_bord, name='module_budget_tableau_de_bord'),
    url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_budget_notification'),
    url(r'get_test_projet', views.get_json_groupement_analytique, name='module_budget_get_json_type_projet'),
    url(r'get_active_exercice_budgetaire', views.get_json_active_exercice_budgetaire, name='module_budget_get_active_exercice_budgetaire'),
    

    url(r'set_active_exercice_budgetaire', views.set_json_cloture_exercice_budgetaire, name='module_budget_set_active_exercice_budgetaire'),
    url(r'to_set_report_ligne_budgetaire', views.get_json_report_ligne_budgetaire, name='module_budget_to_set_report_ligne_budgetaire'),
    url(r'to_desactive_report_ligne_budgetaire', views.get_json_desactive_ligne_budgetaire_report, name='module_budget_to_desactive_ligne_budgetaire'),
    #

    # BUDGET
    url(r'^exercice/list', views.get_lister_budget, name = 'module_budget_list_budget'),
    url(r'^exercice/add', views.get_creer_budget, name = 'module_budget_add_budget'),
    url(r'^exercice/item/(?P<ref>[0-9]+)$', views.get_details_budget, name = 'module_budget_detail_budget'),
    url(r'^exercice/post_add', views.post_creer_budget, name = 'module_budget_post_add_budget'),
    url(r'^exercice/item/(?P<ref>[0-9]+)/update$', views.get_modifier_budget, name = 'module_budget_update_budget'),
    url(r'^exercice/post_update', views.post_modifier_budget, name = 'module_budget_post_update_budget'),


    # BUDGET DEPENSE ET RECETTE SPECIFIQUE
    url(r'^exercice/depense/list', views.get_lister_budget_depense, name = 'module_budget_list_budget_depense'),
    url(r'^exercice/recette/list', views.get_lister_budget_recette, name = 'module_budget_list_budget_recette'),
    url(r'^exercice/regroupement_b/list', views.get_lister_regroupement_b, name = 'module_budget_list_regroupement_b'),

    #REGROUPEMENT BUDGETAIRE
    url(r'^regroupement_ligne/list', views.get_lister_regroupement_lignebudgetaire, name = 'module_budget_lister_regroupement_lignebudgetaire'),
    url(r'^regroupement_ligne/add', views.get_creer_regroupement_lignebudgetaire, name = 'module_budget_creer_regroupement_lignebudgetaire'),
    url(r'^regroupement/json_list_combinaison', views.get_list_combinaison_b, name = 'module_budget_get_list_combinaison_b'),
    url(r'^regroupement/post_add', views.post_creer_regroupement_ligne_budgetaire, name = 'module_budget_post_creer_regroupement_ligne_budgetaire'),
    url(r'^regroupement/item/(?P<ref>[0-9]+)$', views.get_details_groupement_ligne_budget, name = 'module_budget_details_groupement_ligne_budget'),
    url(r'^regroupement/delete/(?P<ref>[0-9]+)$', views.get_delete_groupement_ligne_budget, name = 'module_budget_delete_groupement_ligne_budget'),

    url(r'^regroupement/delete/(?P<ref>[0-9]+)$', views.get_delete_groupement_ligne_budget, name = 'module_budget_delete_groupement_ligne_budget'),
    

    


    # LIGNE BUDGETAIRE
    url(r'^ligne_budgetaire/list', views.get_lister_ligne_budgetaire, name = 'module_budget_list_ligne_budgetaire'),
    url(r'^ligne_budgetaire/add', views.get_creer_ligne_budgetaire, name = 'module_budget_add_ligne_budgetaire'),
    url(r'^ligne_budgetaire/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_budgetaire, name = 'module_budget_detail_ligne_budgetaire'),
    url(r'^ligne_budgetaire/post_add', views.post_creer_ligne_budgetaire, name = 'module_budget_post_add_ligne_budgetaire'),
    url(r'^ligne_budgetaire/item/(?P<ref>[0-9]+)/$', views.get_modifier_ligne_budgetaire, name = 'module_budget_update_ligne_budgetaire'),
    url(r'^ligne_budgetaire/post_update', views.post_modifier_ligne_budgetaire, name = 'module_budget_post_update_ligne_budgetaire'),
    url(r'^ligne_budgetaire/upload/add', views.get_upload_ligne_budgetaire, name='module_budget_get_upload_ligne_budgetaire'),

    url(r'^ligne_budgetaire/item/ecriture_analytique/(?P<ref>[0-9]+)/$', views.get_details_ecriture_analytique_of_ligne_budgetaire, name = 'module_budget_detail_ecriture_analytique_ligne_budgetaire'),
    url(r'^ligne_budgetaire/item/ecriture_comptable/(?P<ref>[0-9]+)/$', views.get_details_ecriture_comptable_of_ligne_budgetaire, name = 'module_budget_detail_ecriture_comptable_ligne_budgetaire'),
    url(r'^centre_cout/item/ecriture_analytique/(?P<ref>[0-9]+)/$', views.get_details_ecriture_analytique_of_centre_cout, name = 'module_budget_detail_ecriture_analytique_centre_cout'),

    # ANALYSE-BUDGETAIRE URLS
    url(r'^analyse/generate', views.get_generer_analyse_budgetaire, name='module_budget_analyse_budgetaire'),
    url(r'^analyse/post_generate', views.post_generer_analyse_budgetaire, name='module_budget_post_analyse_budgetaire'),
    url(r'^analyse/w/print', views.post_imprimer_analyse_budgetaire, name='module_budget_post_imprimer_analyse_budgetaire'),


    # ANALYSE LIGNE BUDGETAIRE URLS
    url(r'^analyse/ligne/generate', views.get_generer_analyse_ligne_budgetaire, name='module_budget_analyse_ligne_budgetaire'),
    url(r'^analyse/ligne/post_generate', views.post_generer_analyse_ligne_budgetaire, name='module_budget_post_analyse_ligne_budgetaire'),
    url(r'^analyse/ligne/print', views.post_imprimer_analyse_ligne_budgetaire, name='module_budget_post_imprimer_analyse_ligne_budgetaire'),

	url(r'^categoriebudget/type/list', views.get_json_list_categorie_budget, name='module_budget_list_categorie_budget'),

    url(r'^analyse/print', views.get_analyse_bgt, name = 'module_budget_analyse_print')
]

urlpatterns.append(url(r'^exercicebudgetaire/list', views.get_lister_exercicebudgetaire, name = 'module_budget_list_exercicebudgetaire'))
urlpatterns.append(url(r'^exercicebudgetaire/add', views.get_creer_exercicebudgetaire, name = 'module_budget_add_exercicebudgetaire'))
urlpatterns.append(url(r'^exercicebudgetaire/post_add', views.post_creer_exercicebudgetaire, name = 'module_budget_post_add_exercicebudgetaire'))
urlpatterns.append(url(r'^exercicebudgetaire/item/(?P<ref>[0-9]+)/$', views.get_details_exercicebudgetaire, name = 'module_budget_detail_exercicebudgetaire'))
urlpatterns.append(url(r'^exercicebudgetaire/item/post_update/$', views.post_modifier_exercicebudgetaire, name = 'module_budget_post_update_exercicebudgetaire'))
urlpatterns.append(url(r'^exercicebudgetaire/item/(?P<ref>[0-9]+)/update$', views.get_modifier_exercicebudgetaire, name = 'module_budget_update_exercicebudgetaire'))

urlpatterns.append(url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_budget_notification'))

'''urlpatterns.append(url(r'^projet/list', views.get_lister_projet, name = 'module_budget_list_projet'))
urlpatterns.append(url(r'^projet/add', views.get_creer_projet, name = 'module_budget_add_projet'))
urlpatterns.append(url(r'^projet/post_add', views.post_creer_projet, name = 'module_budget_post_add_projet'))
urlpatterns.append(url(r'^projet/item/(?P<ref>[0-9]+)/$', views.get_details_projet, name = 'module_budget_detail_projet'))
urlpatterns.append(url(r'^projet/item/post_update/$', views.post_modifier_projet, name = 'module_budget_post_update_projet'))
urlpatterns.append(url(r'^projet/item/(?P<ref>[0-9]+)/update$', views.get_modifier_projet, name = 'module_budget_update_projet'))'''

urlpatterns.append(url(r'^transactionbudgetaire/list', views.get_lister_transactionbudgetaire, name = 'module_budget_list_transactionbudgetaire'))
urlpatterns.append(url(r'^transactionbudgetaire/add', views.get_creer_transactionbudgetaire, name = 'module_budget_add_transactionbudgetaire'))
urlpatterns.append(url(r'^transactionbudgetaire/post_add', views.post_creer_transactionbudgetaire, name = 'module_budget_post_add_transactionbudgetaire'))
urlpatterns.append(url(r'^transactionbudgetaire/item/(?P<ref>[0-9]+)/$', views.get_details_transactionbudgetaire, name = 'module_budget_detail_transactionbudgetaire'))
urlpatterns.append(url(r'^transactionbudgetaire/item/post_update/$', views.post_modifier_transactionbudgetaire, name = 'module_budget_post_update_transactionbudgetaire'))
urlpatterns.append(url(r'^transactionbudgetaire/item/(?P<ref>[0-9]+)/update$', views.get_modifier_transactionbudgetaire, name = 'module_budget_update_transactionbudgetaire'))

urlpatterns.append(url(r'^rapprochement_budgetaire/list', views.get_lister_rapprochement_transaction, name = 'module_budget_list_rapprochement_transaction'))
urlpatterns.append(url(r'^transactionbudgetaire/sans_bc/list', views.get_detail_ligne_budgetaire_without_bc, name = 'module_budget_get_detail_ligne_budgetaire_without_bc'))



'''urlpatterns.append(url(r'^typetransactionbudgetaire/list', views.get_lister_typetransactionbudgetaire, name = 'module_budget_list_typetransactionbudgetaire'))
urlpatterns.append(url(r'^typetransactionbudgetaire/add', views.get_creer_typetransactionbudgetaire, name = 'module_budget_add_typetransactionbudgetaire'))
urlpatterns.append(url(r'^typetransactionbudgetaire/post_add', views.post_creer_typetransactionbudgetaire, name = 'module_budget_post_add_typetransactionbudgetaire'))
urlpatterns.append(url(r'^typetransactionbudgetaire/item/(?P<ref>[0-9]+)/$', views.get_details_typetransactionbudgetaire, name = 'module_budget_detail_typetransactionbudgetaire'))
urlpatterns.append(url(r'^typetransactionbudgetaire/item/post_update/$', views.post_modifier_typetransactionbudgetaire, name = 'module_budget_post_update_typetransactionbudgetaire'))
urlpatterns.append(url(r'^typetransactionbudgetaire/item/(?P<ref>[0-9]+)/update$', views.get_modifier_typetransactionbudgetaire, name = 'module_budget_update_typetransactionbudgetaire'))'''
urlpatterns.append(url(r'^categoriebudget/list', views.get_lister_categoriebudget, name = 'module_budget_list_categoriebudget'))
urlpatterns.append(url(r'^categoriebudget/add', views.get_creer_categoriebudget, name = 'module_budget_add_categoriebudget'))
urlpatterns.append(url(r'^categoriebudget/post_add', views.post_creer_categoriebudget, name = 'module_budget_post_add_categoriebudget'))
urlpatterns.append(url(r'^categoriebudget/item/(?P<ref>[0-9]+)/$', views.get_details_categoriebudget, name = 'module_budget_detail_categoriebudget'))
urlpatterns.append(url(r'^categoriebudget/item/post_update/$', views.post_modifier_categoriebudget, name = 'module_budget_post_update_categoriebudget'))
urlpatterns.append(url(r'^categoriebudget/item/(?P<ref>[0-9]+)/update$', views.get_modifier_categoriebudget, name = 'module_budget_update_categoriebudget'))
urlpatterns.append(url(r'^rallonge/add/(?P<ref>[0-9]+)/$', views.get_creer_rallonge, name = 'module_budget_add_rallonge'))
urlpatterns.append(url(r'^rallonge/post_add', views.post_creer_rallonge, name = 'module_budget_post_add_rallonge'))
urlpatterns.append(url(r'^rallonge/item/(?P<ref>[0-9]+)/$', views.get_details_rallonge, name = 'module_budget_detail_rallonge'))
urlpatterns.append(url(r'^diminution/add/(?P<ref>[0-9]+)/$', views.get_creer_diminution, name = 'module_budget_add_diminution'))
urlpatterns.append(url(r'^diminution/post_add', views.post_creer_diminution, name = 'module_budget_post_add_diminution'))
urlpatterns.append(url(r'^diminution/item/(?P<ref>[0-9]+)/$', views.get_details_diminution, name = 'module_budget_detail_diminution'))




urlpatterns.append(url(r'^centre_cout/list', views.get_lister_centre_cout, name = 'module_budget_list_centre_cout'))
urlpatterns.append(url(r'^centre_cout/add', views.get_creer_centre_cout, name = 'module_budget_add_centre_cout'))
urlpatterns.append(url(r'^centre_cout/post_add', views.post_creer_centre_cout, name = 'module_budget_post_add_centre_cout'))
urlpatterns.append(url(r'^centre_cout/item/(?P<ref>[0-9]+)/$', views.get_details_centre_cout, name = 'module_budget_detail_centre_cout'))
urlpatterns.append(url(r'^centre_cout/item/post_update/$', views.post_modifier_centre_cout, name = 'module_budget_post_update_centre_cout'))
urlpatterns.append(url(r'^centre_cout/item/(?P<ref>[0-9]+)/update$', views.get_modifier_centre_cout, name = 'module_budget_update_centre_cout'))




urlpatterns.append(url(r'^activite/list', views.get_lister_activite, name = 'module_budget_list_activite'))
urlpatterns.append(url(r'^activite/add', views.get_creer_activite, name = 'module_budget_add_activite'))
urlpatterns.append(url(r'^activite/post_add', views.post_creer_activite, name = 'module_budget_post_add_activite'))
urlpatterns.append(url(r'^activite/item/(?P<ref>[0-9]+)/$', views.get_details_activite, name = 'module_budget_detail_activite'))
urlpatterns.append(url(r'^activite/item/post_update/$', views.post_modifier_activite, name = 'module_budget_post_update_activite'))
urlpatterns.append(url(r'^activite/item/(?P<ref>[0-9]+)/update$', views.get_modifier_activite, name = 'module_budget_update_activite'))
urlpatterns.append(url(r'^groupeanalytique/list', views.get_lister_groupeanalytique, name = 'module_budget_list_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/add', views.get_creer_groupeanalytique, name = 'module_budget_add_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/post_add', views.post_creer_groupeanalytique, name = 'module_budget_post_add_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/(?P<ref>[0-9]+)/$', views.get_details_groupeanalytique, name = 'module_budget_detail_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/post_update/$', views.post_modifier_groupeanalytique, name = 'module_budget_post_update_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/(?P<ref>[0-9]+)/update$', views.get_modifier_groupeanalytique, name = 'module_budget_update_groupeanalytique'))
urlpatterns.append(url(r'^poste_budgetaire/list', views.get_lister_poste_budgetaire, name = 'module_budget_list_poste_budgetaire'))
urlpatterns.append(url(r'^poste_budgetaire/add', views.get_creer_poste_budgetaire, name = 'module_budget_add_poste_budgetaire'))
urlpatterns.append(url(r'^poste_budgetaire/post_add', views.post_creer_poste_budgetaire, name = 'module_budget_post_add_poste_budgetaire'))
urlpatterns.append(url(r'^poste_budgetaire/item/(?P<ref>[0-9]+)/$', views.get_details_poste_budgetaire, name = 'module_budget_detail_poste_budgetaire'))
urlpatterns.append(url(r'^poste_budgetaire/item/post_update/$', views.post_modifier_poste_budgetaire, name = 'module_budget_post_update_poste_budgetaire'))
urlpatterns.append(url(r'^poste_budgetaire/item/(?P<ref>[0-9]+)/update$', views.get_modifier_poste_budgetaire, name = 'module_budget_update_poste_budgetaire'))


urlpatterns.append(url(r'^projet/list', views.get_lister_centre_projet, name = 'module_budget_list_projet_centre_cout'))
urlpatterns.append(url(r'^projet/add', views.get_creer_centre_projet, name = 'module_budget_add_projet_centre_cout'))
urlpatterns.append(url(r'^projet/post_add', views.post_creer_centre_projet, name = 'module_budget_post_add_projet_centre_cout'))
urlpatterns.append(url(r'^projet/item/(?P<ref>[0-9]+)/$', views.get_details_centre_projet, name = 'module_budget_detail_projet_centre_cout'))
urlpatterns.append(url(r'^projet/item/post_update/$', views.post_modifier_centre_projet, name = 'module_budget_post_update_projet_centre_cout'))
urlpatterns.append(url(r'^projet/item/(?P<ref>[0-9]+)/update$', views.get_modifier_centre_projet, name = 'module_budget_update_projet_centre_cout'))

urlpatterns.append(url(r'^exercice/ouverture/add', views.get_creer_ouverture_exercice, name='module_budget_add_ouverture_exercice'))
urlpatterns.append(url(r'^exercice/cloture/rapport', views.get_rapport_cloture_exercice, name='module_budget_rapport_cloture_exercice'))
urlpatterns.append(url(r'^exercice/print_rapport_cloture', views.get_print_rapport_cloture_exercice, name='module_budget_print_rapport_cloture_exercice'))
urlpatterns.append(url(r'^exercice/ouverture/post_add', views.post_creer_ouverture_exercice, name='module_budget_post_add_ouverture_exercice'))

#New Cloture
urlpatterns.append(url(r'^exercice/fermeture/', views.to_get_cloture_exercice, name='module_budget_to_get_cloture_exercice'))
urlpatterns.append(url(r'^exercice/close/', views.post_cloture_exercice_budgetaire, name='module_budget_post_cloture_exercice_budgetaire'))


# urlpatterns.append(url(r'^exercice/ouverture/post_add', views.post_creer_ouverture_exercice, name='module_budget_post_add_ouverture_exercice'))
urlpatterns.append(url(r'^is_blocud/combinaison_b', views.post_bloque_combinaison_b, name = 'module_budget_post_bloque_combinaison_b'))
urlpatterns.append(url(r'^combinaison/initiate_validation', views.post_initiate_blocus_status_change, name = 'module_budget_post_initiate_blocus_status_change'))

urlpatterns.append(url(r'all_lignes_bon_commande_non_facture_by_montant', views.get_json_lignes_bon_commande_non_facture_for_transaction, name='module_budget_get_lignes_bon_commande_non_facture_by_transaction'))
urlpatterns.append(url(r'^transaction/post_rapprochement', views.post_json_rapprocher_transaction, name='module_budget_post_rapprochement_transaction'))