from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.get_index, name='module_stock_index'),
    url(r'^tableau', views.get_index, name='module_stock_index'),
]

urlpatterns.append(url(r'^entrepot/list', views.get_lister_entrepot, name = 'module_Stock_list_entrepot'))
urlpatterns.append(url(r'^entrepot/add', views.get_creer_entrepot, name = 'module_Stock_add_entrepot'))
urlpatterns.append(url(r'^entrepot/post_add', views.post_creer_entrepot, name = 'module_Stock_post_add_entrepot'))
urlpatterns.append(url(r'^entrepot/item/(?P<ref>[0-9]+)/$', views.get_details_entrepot, name = 'module_Stock_detail_entrepot'))
urlpatterns.append(url(r'^entrepot/item/post_update/$', views.post_modifier_entrepot, name = 'module_Stock_post_update_entrepot'))
urlpatterns.append(url(r'^entrepot/item/(?P<ref>[0-9]+)/update$', views.get_modifier_entrepot, name = 'module_Stock_update_entrepot'))


urlpatterns.append(url(r'^type_emplacement/list', views.get_lister_type_emplacement, name = 'module_Stock_list_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/add', views.get_creer_type_emplacement, name = 'module_Stock_add_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/post_add', views.post_creer_type_emplacement, name = 'module_Stock_post_add_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/(?P<ref>[0-9]+)/$', views.get_details_type_emplacement, name = 'module_Stock_detail_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/post_update/$', views.post_modifier_type_emplacement, name = 'module_Stock_post_update_type_emplacement'))
urlpatterns.append(url(r'^type_emplacement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_emplacement, name = 'module_Stock_update_type_emplacement'))


urlpatterns.append(url(r'^emplacementstock/list', views.get_lister_emplacementstock, name = 'module_Stock_list_emplacementstock'))
urlpatterns.append(url(r'^emplacementstock/add', views.get_creer_emplacementstock, name = 'module_Stock_add_emplacementstock'))
urlpatterns.append(url(r'^emplacementstock/post_add', views.post_creer_emplacementstock, name = 'module_Stock_post_add_emplacementstock'))
urlpatterns.append(url(r'^emplacementstock/item/(?P<ref>[0-9]+)/$', views.get_details_emplacementstock, name = 'module_Stock_detail_emplacementstock'))
urlpatterns.append(url(r'^emplacementstock/item/post_update/$', views.post_modifier_emplacementstock, name = 'module_Stock_post_update_emplacementstock'))
urlpatterns.append(url(r'^emplacementstock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_emplacementstock, name = 'module_Stock_update_emplacementstock'))


urlpatterns.append(url(r'^stockage/list', views.get_lister_stockage, name = 'module_Stock_list_stockage'))
urlpatterns.append(url(r'^stockage/add', views.get_creer_stockage, name = 'module_Stock_add_stockage'))
urlpatterns.append(url(r'^stockage/post_add', views.post_creer_stockage, name = 'module_Stock_post_add_stockage'))
urlpatterns.append(url(r'^stockage/item/(?P<ref>[0-9]+)/$', views.get_details_stockage, name = 'module_Stock_detail_stockage'))
urlpatterns.append(url(r'^stockage/item/post_update/$', views.post_modifier_stockage, name = 'module_Stock_post_update_stockage'))
urlpatterns.append(url(r'^stockage/item/(?P<ref>[0-9]+)/update$', views.get_modifier_stockage, name = 'module_Stock_update_stockage'))


urlpatterns.append(url(r'^type_operation_stock/list', views.get_lister_type_operation_stock, name = 'module_Stock_list_type_operation_stock'))
urlpatterns.append(url(r'^type_operation_stock/add', views.get_creer_type_operation_stock, name = 'module_Stock_add_type_operation_stock'))
urlpatterns.append(url(r'^type_operation_stock/post_add', views.post_creer_type_operation_stock, name = 'module_Stock_post_add_type_operation_stock'))
urlpatterns.append(url(r'^type_operation_stock/item/(?P<ref>[0-9]+)/$', views.get_details_type_operation_stock, name = 'module_Stock_detail_type_operation_stock'))
urlpatterns.append(url(r'^type_operation_stock/item/post_update/$', views.post_modifier_type_operation_stock, name = 'module_Stock_post_update_type_operation_stock'))
urlpatterns.append(url(r'^type_operation_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_operation_stock, name = 'module_Stock_update_type_operation_stock'))

urlpatterns.append(url(r'^statut_operation_stock/list', views.get_lister_statut_operation_stock, name = 'module_Stock_list_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/add', views.get_creer_statut_operation_stock, name = 'module_Stock_add_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/post_add', views.post_creer_statut_operation_stock, name = 'module_Stock_post_add_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/(?P<ref>[0-9]+)/$', views.get_details_statut_operation_stock, name = 'module_Stock_detail_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/post_update/$', views.post_modifier_statut_operation_stock, name = 'module_Stock_post_update_statut_operation_stock'))
urlpatterns.append(url(r'^statut_operation_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_statut_operation_stock, name = 'module_Stock_update_statut_operation_stock'))


urlpatterns.append(url(r'^operation_stock/list', views.get_lister_operation_stock, name = 'module_Stock_list_operation_stock'))
urlpatterns.append(url(r'^operation_stock/add', views.get_creer_operation_stock, name = 'module_Stock_add_operation_stock'))
urlpatterns.append(url(r'^operation_stock/post_add', views.post_creer_operation_stock, name = 'module_Stock_post_add_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/(?P<ref>[0-9]+)/$', views.get_details_operation_stock, name = 'module_Stock_detail_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/post_update/$', views.post_modifier_operation_stock, name = 'module_Stock_post_update_operation_stock'))
urlpatterns.append(url(r'^operation_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_operation_stock, name = 'module_Stock_update_operation_stock'))


urlpatterns.append(url(r'^ligne_operation_stock/list', views.get_lister_ligne_operation_stock, name = 'module_Stock_list_ligne_operation_stock'))
urlpatterns.append(url(r'^ligne_operation_stock/add', views.get_creer_ligne_operation_stock, name = 'module_Stock_add_ligne_operation_stock'))
urlpatterns.append(url(r'^ligne_operation_stock/post_add', views.post_creer_ligne_operation_stock, name = 'module_Stock_post_add_ligne_operation_stock'))
urlpatterns.append(url(r'^ligne_operation_stock/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_operation_stock, name = 'module_Stock_detail_ligne_operation_stock'))
urlpatterns.append(url(r'^ligne_operation_stock/item/post_update/$', views.post_modifier_ligne_operation_stock, name = 'module_Stock_post_update_ligne_operation_stock'))
urlpatterns.append(url(r'^ligne_operation_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ligne_operation_stock, name = 'module_Stock_update_ligne_operation_stock'))


urlpatterns.append(url(r'^type_mvt_stock/list', views.get_lister_type_mvt_stock, name = 'module_Stock_list_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/add', views.get_creer_type_mvt_stock, name = 'module_Stock_add_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/post_add', views.post_creer_type_mvt_stock, name = 'module_Stock_post_add_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/(?P<ref>[0-9]+)/$', views.get_details_type_mvt_stock, name = 'module_Stock_detail_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/post_update/$', views.post_modifier_type_mvt_stock, name = 'module_Stock_post_update_type_mvt_stock'))
urlpatterns.append(url(r'^type_mvt_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_mvt_stock, name = 'module_Stock_update_type_mvt_stock'))


urlpatterns.append(url(r'^mvt_stock/list', views.get_lister_mvt_stock, name = 'module_Stock_list_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/add', views.get_creer_mvt_stock, name = 'module_Stock_add_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/post_add', views.post_creer_mvt_stock, name = 'module_Stock_post_add_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/(?P<ref>[0-9]+)/$', views.get_details_mvt_stock, name = 'module_Stock_detail_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/post_update/$', views.post_modifier_mvt_stock, name = 'module_Stock_post_update_mvt_stock'))
urlpatterns.append(url(r'^mvt_stock/item/(?P<ref>[0-9]+)/update$', views.get_modifier_mvt_stock, name = 'module_Stock_update_mvt_stock'))


urlpatterns.append(url(r'^rebut/list', views.get_lister_rebut, name = 'module_Stock_list_rebut'))
urlpatterns.append(url(r'^rebut/add', views.get_creer_rebut, name = 'module_Stock_add_rebut'))
urlpatterns.append(url(r'^rebut/post_add', views.post_creer_rebut, name = 'module_Stock_post_add_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/$', views.get_details_rebut, name = 'module_Stock_detail_rebut'))
urlpatterns.append(url(r'^rebut/item/post_update/$', views.post_modifier_rebut, name = 'module_Stock_post_update_rebut'))
urlpatterns.append(url(r'^rebut/item/(?P<ref>[0-9]+)/update$', views.get_modifier_rebut, name = 'module_Stock_update_rebut'))


urlpatterns.append(url(r'^statut_ajustement/list', views.get_lister_statut_ajustement, name = 'module_Stock_list_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/add', views.get_creer_statut_ajustement, name = 'module_Stock_add_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/post_add', views.post_creer_statut_ajustement, name = 'module_Stock_post_add_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/(?P<ref>[0-9]+)/$', views.get_details_statut_ajustement, name = 'module_Stock_detail_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/post_update/$', views.post_modifier_statut_ajustement, name = 'module_Stock_post_update_statut_ajustement'))
urlpatterns.append(url(r'^statut_ajustement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_statut_ajustement, name = 'module_Stock_update_statut_ajustement'))


urlpatterns.append(url(r'^ajustement/list', views.get_lister_ajustement, name = 'module_Stock_list_ajustement'))
urlpatterns.append(url(r'^ajustement/add', views.get_creer_ajustement, name = 'module_Stock_add_ajustement'))
urlpatterns.append(url(r'^ajustement/post_add', views.post_creer_ajustement, name = 'module_Stock_post_add_ajustement'))
urlpatterns.append(url(r'^ajustement/item/(?P<ref>[0-9]+)/$', views.get_details_ajustement, name = 'module_Stock_detail_ajustement'))
urlpatterns.append(url(r'^ajustement/item/post_update/$', views.post_modifier_ajustement, name = 'module_Stock_post_update_ajustement'))
urlpatterns.append(url(r'^ajustement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ajustement, name = 'module_Stock_update_ajustement'))


urlpatterns.append(url(r'^ligne_ajustement/list', views.get_lister_ligne_ajustement, name = 'module_Stock_list_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/add', views.get_creer_ligne_ajustement, name = 'module_Stock_add_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/post_add', views.post_creer_ligne_ajustement, name = 'module_Stock_post_add_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/(?P<ref>[0-9]+)/$', views.get_details_ligne_ajustement, name = 'module_Stock_detail_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/post_update/$', views.post_modifier_ligne_ajustement, name = 'module_Stock_post_update_ligne_ajustement'))
urlpatterns.append(url(r'^ligne_ajustement/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ligne_ajustement, name = 'module_Stock_update_ligne_ajustement'))

#BON ENTREE
urlpatterns.append(url(r'^bons_stock/list', views.get_lister_bons_reception, name='module_stock_list_bon_receptions'))
urlpatterns.append(url(r'^bons_stock/item/(?P<ref>[0-9]+)/$', views.get_details_bon_reception, name='module_stock_details_bon_reception'))
urlpatterns.append(url(r'^bons_stock/item/(?P<ref>[0-9]+)/receive/$', views.get_receptionner_bon_reception, name='module_stock_receive_bon_reception'))
urlpatterns.append(url(r'^bons_stock/item/post_receive/$', views.post_receptionner_bon_reception, name='module_stock_post_receive_bon_reception'))

urlpatterns.append(url(r'^bons_entrees_stock/list', views.get_lister_bons_entrees, name='module_stock_list_bons_entrees'))
urlpatterns.append(url(r'^bons_entrees_stock/item/(?P<ref>[0-9]+)/$', views.get_details_bons_entrees, name='module_stock_details_bons_entrees'))
urlpatterns.append(url(r'^bons_entrees_stock/workflow_post', views.post_workflow_bon_entree_depot, name = 'module_stock_bon_entrees_workflow_post'))

urlpatterns.append(url(r'^bons_entrees_stock/item/release_asset/$', views.get_to_asset_of_bons_entrees, name='module_stock_get_assetiser_bons_entrees'))
urlpatterns.append(url(r'^bons_entrees_stock/item/post_release_asset/$', views.post_to_asset_of_bons_entrees, name='module_stock_post_assetiser_bons_entrees'))


