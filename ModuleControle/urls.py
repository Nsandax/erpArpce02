from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ModuleControle.cubesviewer.views.cubesviewer import CubesViewerView
from ModuleControle.cubesviewer.api import proxy
from ModuleControle.cubesviewer.api.view import ViewSaveView, ViewListView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        #url(r'^$', views.get_index, name='module_controle_index'),
        url(r'^tableau', views.get_index, name='module_controle_tableau'),

        ###CUBES
        url(r'^explore', views.get_cubeviewer, name="module_controle_explore_index" ),
        url(r'^explore/view/list/$', ViewListView.as_view(), name="module_controle_explore_list" ),
        url(r'^explore/view/save/$', csrf_exempt(ViewSaveView.as_view()), name="module_controle_explore_save" ),
        url(r'^explore/cubes/', login_required(proxy.connection), name="module_controle_explore_cubes"),
        ###END CUBES


        # ANALYSE-BUDGETAIRE URLS
        url(r'^analyse/generate', views.get_generer_analyse_budgetaire, name='module_controle_analyse_budgetaire'),
        url(r'^analyse/post_generate', views.post_generer_analyse_budgetaire, name='module_controle_post_analyse_budgetaire'),
        url(r'^analyse/print', views.get_analyse_bgt, name = 'module_controle_analyse_print'),




        #JOURNAL
        url(r'^journal/generate', views.get_generer_journal, name='module_controle_generer_journal'),
        url(r'^journal/post_generate', views.post_generer_journal, name='module_controle_post_generer_journal'),
        url(r'^journal/print', views.post_imprimer_journal, name='module_controle_post_imprimer_journal'),

        #GL
        url(r'^livre/generate', views.get_generer_grand_livre, name='module_controle_generer_grand_livre'),
        url(r'^livre/post_generate', views.post_generer_grand_livre, name='module_controle_post_generer_grand_livre'),
        url(r'^livre/print', views.post_imprimer_grand_livre, name='module_controle_post_imprimer_grand_livre'),

        #BALANCE
        url(r'^balance/generate', views.get_generer_balance_generale, name='module_controle_generer_balance_generale'),
        url(r'^balance/post_generate', views.post_generer_balance_generale, name='module_controle_post_generer_balance_generale'),
        url(r'^balance/print', views.post_imprimer_balance_generale, name='module_controle_post_imprimer_balance_generale'), 

        # BILAN URLS
        url(r'^bilan/generate', views.get_generer_bilan, name='module_controle_generer_bilan'),
        url(r'^bilan/post_generate', views.post_generer_bilan, name='module_controle_post_generer_bilan'),
        url(r'^bilan/print', views.post_imprimer_bilan, name='module_controle_post_imprimer_bilan'),

        # RESULTAT URLS
        url(r'^resultat/generate', views.get_generer_resultat, name='module_controle_generer_resultat'),
        url(r'^resultat/post_generate', views.post_generer_resultat, name='module_controle_post_generer_resultat'),
        url(r'^resultat/print', views.post_imprimer_resultat, name='module_controle_post_imprimer_resultat'),

         # TABLEAU DE FLUX DE TRESORERIE URLS
        url(r'^tresorerie/generate', views.get_generer_tresorerie, name='module_controle_generer_tresorerie'),
        url(r'^tresorerie/post_generate', views.post_generer_tresorerie, name='module_controle_post_generer_tresorerie'),
        url(r'^tresorerie/print', views.post_imprimer_tresorerie, name='module_controle_post_imprimer_tresorerie'),
        
        # NOTES ANNEXES URLS
        url(r'^annexe/generate', views.get_generer_annexe, name='module_controle_generer_annexe'),
        url(r'^annexe/post_generate', views.post_generer_annexe, name='module_controle_post_generer_annexe'),

        # BALANCE DES TIERS URLS
        url(r'^balance_tiers/generate', views.get_generer_balance_tiers, name='module_controle_generer_balance_tiers'),
        url(r'^balance_tiers/post_generate', views.post_generer_balance_tiers, name='module_controle_post_generer_balance_tiers'),
        url(r'^balance_tiers/print', views.post_imprimer_balance_tiers, name='module_controle_post_imprimer_balance_tiers'),
                
        # BALANCE AGEE URLS
        url(r'^balance_agee/client/generate', views.get_generer_balance_agee_client, name='module_controle_generer_balance_agee_client'),
        url(r'^balance_agee/client/post_generate', views.post_generer_balance_agee_client, name='module_controle_post_generer_balance_agee_client'),
        url(r'^balance_agee/client/print', views.post_imprimer_balance_agee_client, name='module_controle_post_imprimer_balance_agee_client'),
        url(r'^balance_agee/fournisseur/generate', views.get_generer_balance_agee_fournisseur, name='module_controle_generer_balance_agee_fournisseur'),
        url(r'^balance_agee/fournisseur/post_generate', views.post_generer_balance_agee_fournisseur, name='module_controle_post_generer_balance_agee_fournisseur'),
        url(r'^balance_agee/fournisseur/print', views.post_imprimer_balance_agee_fournisseur, name='module_controle_post_imprimer_balance_agee_fournisseur'),

        url(r'^centre_cout/item/ecriture_analytique/(?P<ref>[0-9]+)/$', views.get_details_ecriture_analytique_of_centre_cout, name = 'module_controle_detail_ecriture_analytique_centre_cout'),






        ]
urlpatterns.append(url(r'^operationnalisation_module/show', views.get_show_module, name = 'module_controle_list_show_module'))
urlpatterns.append(url(r'^operationnalisation_module/list/(?P<ref>[0-9]+)/', views.get_lister_operationnalisation_module, name = 'module_controle_list_operationnalisation_module'))
urlpatterns.append(url(r'^operationnalisation_module/add/(?P<ref>[0-9]+)/', views.get_creer_operationnalisation_module, name = 'module_controle_add_operationnalisation_module'))
urlpatterns.append(url(r'^operationnalisation_module/status/post', views.post_status_operationnalisation_module, name = 'module_controle_post_status_operationnalisation_module'))
urlpatterns.append(url(r'^operationnalisation_module/post_add', views.post_creer_operationnalisation_module, name = 'module_controle_post_add_operationnalisation_module'))
urlpatterns.append(url(r'^operationnalisation_module/item/(?P<ref>[0-9]+)/$', views.get_details_operationnalisation_module, name = 'module_controle_detail_operationnalisation_module'))
urlpatterns.append(url(r'^operationnalisation_module/item/post_update/$', views.post_modifier_operationnalisation_module, name = 'module_controle_post_update_operationnalisation_module'))
urlpatterns.append(url(r'^operationnalisation_module/item/(?P<ref>[0-9]+)/update$', views.get_modifier_operationnalisation_module, name = 'module_controle_update_operationnalisation_module'))




# CENTRE DE COUT URLS
urlpatterns.append(url(r'^centre_cout/list', views.get_lister_centre_cout, name = 'module_controle_list_centre_cout'))
urlpatterns.append(url(r'^centre_cout/add', views.get_creer_centre_cout, name = 'module_controle_add_centre_cout'))
urlpatterns.append(url(r'^centre_cout/post_add', views.post_creer_centre_cout, name = 'module_controle_post_add_centre_cout'))
urlpatterns.append(url(r'^centre_cout/item/(?P<ref>[0-9]+)/$', views.get_details_centre_cout, name = 'module_controle_detail_centre_cout'))
urlpatterns.append(url(r'^centre_cout/item/post_update/$', views.post_modifier_centre_cout, name = 'module_controle_post_update_centre_cout'))
urlpatterns.append(url(r'^centre_cout/item/(?P<ref>[0-9]+)/update$', views.get_modifier_centre_cout, name = 'module_controle_update_centre_cout'))



urlpatterns.append(url(r'^groupeanalytique/list', views.get_lister_groupeanalytique, name = 'module_controle_list_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/add', views.get_creer_groupeanalytique, name = 'module_controle_add_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/post_add', views.post_creer_groupeanalytique, name = 'module_controle_post_add_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/(?P<ref>[0-9]+)/$', views.get_details_groupeanalytique, name = 'module_controle_detail_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/post_update/$', views.post_modifier_groupeanalytique, name = 'module_controle_post_update_groupeanalytique'))
urlpatterns.append(url(r'^groupeanalytique/item/(?P<ref>[0-9]+)/update$', views.get_modifier_groupeanalytique, name = 'module_controle_update_groupeanalytique'))



urlpatterns.append(url(r'^activity/list', views.get_lister_activity, name = 'module_controle_list_activity'))
urlpatterns.append(url(r'^activity/item/(?P<ref>[0-9]+)/$', views.get_details_activity, name = 'module_controle_detail_activity'))

urlpatterns.append(url(r'^employe/listyear', views.get_employes_annee_to_dashbord, name = 'module_controle_get_employes_annee_to_dashbord'))