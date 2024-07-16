from django.conf.urls import include, url, handler404, handler500

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories', views.CategorieViewSet)
router.register(r'unite', views.UniteViewSet)
router.register(r'categorie_unite', views.CategorieUniteViewSet)
router.register(r'bon_reception', views.BonReceptionViewSet)
router.register(r'demande_achat', views.DemandeAchatViewSet)
router.register(r'reglement', views.ConditionReglementViewSet)


urlpatterns=[

     url(r'all_article_serv_ref', views.get_json_article, name='module_achat_get_article_of_service_referent'),
     url(r'stock_serv_ref', views.get_json_articles_stock_emplacement, name='module_achat_get_stock_article_of_service_referent'),
     url(r'all_ligne_expression', views.get_json_ligne_expression, name='module_achat_get_lignes_of_expression'),
     url(r'all_ligne_demande', views.get_json_ligne_demande, name='module_achat_get_lignes_of_demande'),
     url(r'all_lignes_bon_commande_non_facture', views.get_json_lignes_bon_commande_non_facture, name='module_achat_get_lignes_bon_commande_non_facture'),
     url(r'all_asset_of_article', views.get_details_list_asset_of_article, name='module_achat_get_assets_of_article'),
]


#Tableau de bord
urlpatterns.append(url(r'^tableau', views.get_dashboard, name = 'module_achat_tableau_de_bord'))
urlpatterns.append(url(r'^dashboard_expression_ajax',views.get_expression_de_besoin_to_dashbord, name='module_achat_tableau_de_bord_expression_ajax'))
urlpatterns.append(url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_achat_notification'))

#Api
urlpatterns.append(url(r'^api/', include(router.urls)))

#Bon de reception
#Bon Commande use bon reception
urlpatterns.append(url(r'^bon_commande/list', views.get_lister_bon_reception, name = 'module_achat_list_bon_reception'))
urlpatterns.append(url(r'^bon_commande/add', views.get_creer_bon_reception, name = 'module_achat_add_bon_reception'))
urlpatterns.append(url(r'^bon_commande/post_add', views.post_creer_bon_reception, name = 'module_achat_post_add_bon_reception'))
urlpatterns.append(url(r'^bon_commande/item/(?P<ref>[0-9]+)/$', views.get_details_bon_reception, name = 'module_achat_detail_bon_reception'))
urlpatterns.append(url(r'^bon_commande/print', views.get_print_reception, name = 'module_achat_bon_reception_print'))
urlpatterns.append(url(r'^ligne_commande/list', views.get_lister_ligne_reception, name = 'module_achat_list_ligne_reception'))
urlpatterns.append(url(r'^ligne_commande/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_reception, name = 'module_achat_detail_ligne_reception'))
urlpatterns.append(url(r'^bon_commande/workflow_post', views.post_workflow_reception, name = 'module_achat_bon_reception_workflow_post'))

urlpatterns.append(url(r'^bon_commande/item/(?P<ref>[0-9]+)/update/$', views.get_update_bon_reception, name='module_achat_update_bon_reception'))
urlpatterns.append(url(r'^bon_commande/item/post_update/$', views.post_update_bon_reception, name='module_achat_modifier_bon_commande'))
urlpatterns.append(url(r'^bon_commande/Mois/(?P<ref>[0-9]+)/$', views.get_lister_bon_reception_month, name = 'module_achat_detail_number_bon_reception'))
urlpatterns.append(url(r'^bon_commande/rapport/printing/', views.get_printing_bon_commande, name = 'module_achat_printing_bon_commande'))

urlpatterns.append(url(r'^bon_commande/post_traitement_duree', views.get_traitement_duree_bc, name = 'module_achat_post_get_traitement_duree_bc'))
urlpatterns.append(url(r'^bon_commande/traitement/item/$', views.get_detail_traitement, name = 'module_achat_get_detail_traitement'))



#Fournisseurs
urlpatterns.append(url(r'^fournisseur/list', views.get_lister_fournisseurs, name='module_achat_list_fournisseurs'))
urlpatterns.append(url(r'^fournisseur/add', views.get_creer_fournisseur, name='module_achat_add_fournisseur'))
urlpatterns.append(url(r'^fournisseur/post_add', views.post_creer_fournisseur, name='module_achat_post_add_fournisseur'))
urlpatterns.append(url(r'^fournisseur/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_fournisseur, name='module_achat_update_fournisseur'))
urlpatterns.append(url(r'^fournisseur/item/post_update/$', views.post_modifier_fournisseur, name='module_achat_post_update_fournisseur'))
urlpatterns.append(url(r'^fournisseur/item/(?P<ref>[0-9]+)/$', views.get_details_fournisseur, name='module_achat_details_fournisseur'))

#Demande d'achat
urlpatterns.append(url(r'^demande_achat/list', views.get_lister_demande, name = 'module_achat_list_demande_achat'))
urlpatterns.append(url(r'^demande_achat/treat', views.get_treat_demande, name = 'module_achat_treat_demande_achat'))
urlpatterns.append(url(r'^demande_achat/post_treat', views.post_treat_demande, name = 'module_achat_treat_post_treat_demande_achat'))
urlpatterns.append(url(r'^demande_achat/add', views.get_creer_demande, name = 'module_achat_add_demande_achat'))
urlpatterns.append(url(r'^demande_achat/post_add', views.post_creer_demande, name = 'module_achat_post_add_demande_achat'))
urlpatterns.append(url(r'^demande_achat/item/(?P<ref>[0-9]+)/$', views.get_details_demande, name = 'module_achat_detail_demande_achat'))
urlpatterns.append(url(r'^demande_achat/workflow_post', views.post_workflow_demande, name = 'module_achat_demande_achat_workflow_post'))
urlpatterns.append(url(r'^demande_achat/print', views.get_print_demande, name = 'module_achat_demande_achat_print'))

urlpatterns.append(url(r'^demande_achat/cancel_workflow/(?P<ref>[0-9]+)/', views.post_cancel_workflow_demande, name = 'module_achat_demande_cancel_workflow_post'))
urlpatterns.append(url(r'^demande_achat/rapport/printing/', views.get_printing_demande, name = 'module_achat_printing_demande'))
#----------------------------------------------------suppression----------------------------------------------------------------------------------------------------------
#urlpatterns.append(url(r'^demande_achat/supprimer/',views.post_supprimmer_demande_achat, name='module_achat_supprimer_demande_achat'))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------


#Expression de besoin

urlpatterns.append(url(r'^expression/list', views.get_lister_expression, name = 'module_achat_list_expression'))
urlpatterns.append(url(r'^expression/add', views.get_creer_expression, name = 'module_achat_add_expression'))
urlpatterns.append(url(r'^expression/post_add', views.post_creer_expression, name = 'module_achat_post_add_expression'))
urlpatterns.append(url(r'^expression/item/(?P<ref>[0-9]+)/$', views.get_details_expression, name = 'module_achat_detail_expression'))
urlpatterns.append(url(r'^expression/workflow_post', views.post_workflow_expression, name = 'module_achat_expression_workflow_post'))
urlpatterns.append(url(r'^expression/print', views.get_print_expression, name = 'module_achat_expression_print'))
urlpatterns.append(url(r'^expression/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_expression, name='module_achat_update_expression'))
urlpatterns.append(url(r'^expression/item/post_update/$', views.post_modifier_expression, name='module_achat_post_update_expression'))

urlpatterns.append(url(r'^expression/cancel_workflow/(?P<ref>[0-9]+)/', views.post_cancel_workflow_expression, name = 'module_achat_expression_cancel_workflow_post'))

urlpatterns.append(url(r'^rapports/expressions', views.get_expression_rapports, name='module_achat_rapports_expression'))
urlpatterns.append(url(r'^expression/rapport/printing/', views.get_printing_expression, name = 'module_achat_printing_expression'))

#Catégorie Articles
urlpatterns.append(url(r'^categorie/article/list', views.get_lister_categorie_articles, name = 'module_achat_list_categorie_article'))
urlpatterns.append(url(r'^categorie/article/add', views.get_creer_categorie_articles, name = 'module_achat_add_categorie_articles'))
urlpatterns.append(url(r'^categorie/article/post_add', views.post_creer_categorie_articles, name = 'module_achat_post_add_categorie_articles'))
urlpatterns.append(url(r'^categories/article/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_articles, name='module_achat_details_categorie_articles'))
urlpatterns.append(url(r'^categories/article/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_catagorie_articles, name='module_achat_update_categorie_articles'))
urlpatterns.append(url(r'^categories/article/item/post_update/$', views.post_modifier_categorie_articles, name='module_achat_post_update_categorie_articles'))


#Catégorie Unite
urlpatterns.append(url(r'^categorie/unite/list', views.get_lister_categorie_unites, name = 'module_achat_list_categorie_unite'))
urlpatterns.append(url(r'^categorie/unite/add', views.get_creer_categorie_unites, name = 'module_achat_add_categorie_unites'))
urlpatterns.append(url(r'^categorie/unite/post_add', views.post_creer_categorie_unites, name = 'module_achat_post_add_categorie_unites'))
urlpatterns.append(url(r'^categories/unite/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_unites, name='module_achat_details_categorie_unites'))
urlpatterns.append(url(r'^categories/unite/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_catagorie_unites, name='module_achat_update_categorie_unites'))
urlpatterns.append(url(r'^categories/unite/item/post_update/$', views.post_modifier_categorie_unites, name='module_achat_post_update_categorie_unites'))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------

#Unites de mésure
urlpatterns.append(url(r'^unite/list', views.get_lister_unites, name='module_achat_list_unite'))
urlpatterns.append(url(r'^unite/add', views.get_creer_unite, name='module_achat_add_unite'))
urlpatterns.append(url(r'^unite/post_add', views.post_creer_unite, name='module_achat_post_add_unite'))
urlpatterns.append(url(r'^unite/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_unite, name='module_achat_update_unite'))
urlpatterns.append(url(r'^unite/item/post_update/$', views.post_modifier_unite, name='module_achat_post_update_unite'))
urlpatterns.append(url(r'^unite/item/(?P<ref>[0-9]+)/$', views.get_details_unite, name='module_achat_details_unite'))


#Conditions de regelements
urlpatterns.append(url(r'^reglement/list', views.get_lister_reglement, name='module_achat_list_reglement'))
urlpatterns.append(url(r'^reglement/add', views.get_creer_reglement, name='module_achat_add_reglement'))
urlpatterns.append(url(r'^reglement/post_add', views.post_creer_reglement, name='module_achat_post_add_reglement'))
urlpatterns.append(url(r'^reglement/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_reglement, name='module_achat_update_reglement'))
urlpatterns.append(url(r'^reglement/item/post_update/$', views.post_modifier_reglement, name='module_achat_post_update_reglement'))
urlpatterns.append(url(r'^reglement/item/(?P<ref>[0-9]+)/$', views.get_details_reglement, name='module_achat_details_reglement'))


#Articles
urlpatterns.append(url(r'^articles/list', views.get_lister_article, name='module_achat_list_articles'))
urlpatterns.append(url(r'^articles/add', views.get_creer_article, name='module_achat_add_article'))
urlpatterns.append(url(r'^articles/post_add', views.post_creer_article, name='module_achat_post_add_article'))
urlpatterns.append(url(r'^articles/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_article, name='module_achat_update_article'))
urlpatterns.append(url(r'^articles/item/post_update/$', views.post_modifier_article, name='module_achat_post_update_article'))
urlpatterns.append(url(r'^articles/item/(?P<ref>[0-9]+)/$', views.get_details_article, name='module_achat_details_article'))
urlpatterns.append(url(r'^article/get_prix', views.get_json_get_prix_article, name='module_achat_article_prix'))
urlpatterns.append(url(r'^article/details', views.get_details_article_fourni, name='module_achat_details_article_fourni'))


#BUSINESS INTELLIGENCE
urlpatterns.append(url(r'^rapports/index', views.get_generate_report, name='module_achat_rapports_index'))
urlpatterns.append(url(r'^rapports/result', views.post_generate_report, name='module_achat_post_generate_report'))



urlpatterns.append(url(r'^rapports/demandes', views.get_demande_rapports, name='module_achat_rapports_demande'))
urlpatterns.append(url(r'^rapports/reception', views.get_reception_rapports, name='module_achat_rapports_reception'))

urlpatterns.append(url(r'^rapports/generate_analyse_achat', views.get_generer_analyse_achat, name='module_achat_rapports_generer_analyse_achat'))
urlpatterns.append(url(r'^rapports/analyse_achat', views.post_generer_analyse_achat, name='module_achat_post_generer_analyse_achat'))
urlpatterns.append(url(r'^analyse/w/print', views.post_imprimer_analyse_achat, name='module_budget_post_imprimer_analyse_achat'))


'''urlpatterns.append(url(r'^avis_appel_offre/list', views.get_lister_avis_appel_offre, name = 'module_achat_list_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/add', views.get_creer_avis_appel_offre, name = 'module_achat_add_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/post_add', views.post_creer_avis_appel_offre, name = 'module_achat_post_add_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/item/(?P<ref>[0-9]+)/$', views.get_details_avis_appel_offre, name = 'module_achat_detail_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/item/post_update/$', views.post_modifier_avis_appel_offre, name = 'module_achat_post_update_avis_appel_offre'))
urlpatterns.append(url(r'^avis_appel_offre/item/(?P<ref>[0-9]+)/update$', views.get_modifier_avis_appel_offre, name = 'module_achat_update_avis_appel_offre'))


urlpatterns.append(url(r'^avis_appel_offre/modelprint', views.get_modelprint, name = 'module_achat_modelprint_avis_appel_offre'))'''