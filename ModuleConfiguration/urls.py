from django.conf.urls import include, url
from . import views

urlpatterns = [
	# DASHBOARD URL
	url(r'^dashboard', views.get_dashboard, name='module_configuration_dashboard'),


	#JSON
	url(r'all_sous_module_of_module', views.get_json_sous_modules, name='module_configuration_get_json_sous_modules'),
	 
	# UTILISATEUR URLS
	url(r'^utilisateurs/list', views.get_lister_utilisateurs, name='module_configuration_list_utilisateurs'),
	url(r'^utilisateurs/add', views.get_creer_utilisateur, name='module_configuration_add_utilisateur'),
	url(r'^utilisateurs/post_add', views.post_creer_utilisateur, name='module_configuration_post_add_utilisateur'),
	url(r'^utilisateurs/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_utilisateur, name='module_configuration_update_utilisateur'),
	url(r'^utilisateurs/item/post_update/$', views.post_modifier_utilisateur, name='module_configuration_post_update_utilisateur'),
	url(r'^utilisateurs/item/(?P<ref>[0-9]+)/$', views.get_details_utilisateur, name='module_configuration_details_utilisateur'),

	# ROLES URLS
	url(r'^roles/list', views.get_lister_roles, name='module_configuration_list_roles'),
	url(r'^roles/add', views.get_creer_role, name='module_configuration_add_role'),
	url(r'^roles/post_add', views.post_creer_role, name='module_configuration_post_add_role'),
	url(r'^roles/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_role, name='module_configuration_update_role'),

	
	url(r'^roles/item/post_update/$', views.post_modifier_role, name='module_configuration_post_update_role'),
	url(r'^roles/item/(?P<ref>[0-9]+)/$', views.get_details_role, name='module_configuration_details_role'),
	url(r'^roles/item/(?P<ref>[0-9]+)/rights/add/$', views.get_ajouter_droits, name='module_configuration_add_rights'),
	url(r'^roles/item/rights/post_add/$', views.post_ajouter_droits, name='module_configuration_post_add_rights'),
	url(r'^roles/item/(?P<ref>[0-9]+)/rights/remove/$', views.get_retirer_droits, name='module_configuration_remove_rights'),
	url(r'^roles/item/rights/post_remove/$', views.post_retirer_droits, name='module_configuration_post_remove_rights'),

	
	# DROIT URLS
	#url(r'^droit/add', views.get_creer_droits, name='module_configuration_add_droits'),
	#url(r'^droit/list', views.get_lister_droits, name='module_configuration_list_droits'),
	#url(r'^droit/item/(?P<ref>[0-9]+)/$', views.get_details_droits, name='module_configuration_details_droit'),

	# ROLES UTILISATEUR
	url(r'^utilisateurs/item/(?P<ref>[0-9]+)/roles/attribute/$', views.get_attribuer_role, name='module_configuration_attribuer_role'),
	url(r'^utilisateurs/item/roles/post_attribute/$', views.post_attribuer_role, name='module_configuration_post_attribuer_role'),
	url(r'^utilisateurs/item/(?P<ref_utilisateur>[0-9]+)/roles/item/(?P<ref_role>[0-9]+)/retire/$', views.get_retirer_role, name='module_configuration_retirer_role'),

	# PLACE URLS
	url(r'^places/filles', views.get_json_list_places_filles, name='module_configuration_list_places_filles'),
	
	#EMPLOYEE URLS JSON

	url(r'^json/employee', views.get_json_employee, name='module_configuration_list_json_employee'),

	# CONFIGURATION URLS	
	url(r'^configuration', views.get_configuration, name='module_configuration_configuration'),
	url(r'^configuration/post_update/$', views.post_modifier_configuration, name='module_configuration_post_modifier_configuration'),	
	
	

	#MODULE URLS
	url(r'^modules/list', views.get_lister_modules, name='module_configuration_list_modules'),
	url(r'^modules/add', views.get_creer_module, name='module_configuration_add_module'),
	url(r'^modules/post_add', views.post_creer_module, name='module_configuration_post_add_module'),
	url(r'^modules/item/(?P<ref>[0-9]+)/$', views.get_details_module, name='module_configuration_details_module'),
	url(r'^modules/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_module, name='module_configuration_update_module'),
	url(r'^modules/item/post_update/$', views.post_modifier_module, name='module_configuration_post_update_module'),
	url(r'^modules/item/(?P<ref>[0-9]+)/addModel/$', views.get_creer_modele, name='module_configuration_add_modele'),
	url(r'^modules/item/(?P<ref>[0-9]+)/post_addModel/$', views.post_creer_modele, name='module_configuration_post_add_modele'),

	#SQUELETTE module_configuration_add_dao_template
	url(r'^framework/generate', views.get_creer_framework, name='module_configuration_generate_framework'),
	url(r'^framework/post_generate', views.post_creer_framework, name='module_configuration_post_generate_framework'),

	#TEST UNIT
	url(r'^test/generate', views.get_creer_test, name='module_configuration_generate_test'),
	url(r'^test/post_generate', views.post_creer_test, name='module_configuration_post_generate_test'),

	#TEST SELENIUM
	url(r'^selenium/generate', views.get_creer_selenium, name='module_configuration_generate_selenium'),
	url(r'^selenium/post_generate', views.post_creer_selenium, name='module_configuration_post_generate_selenium'),

	#DAO ET TEMPLATES
	url(r'^modules/dao_template/add', views.get_creer_dao_template, name='module_configuration_add_dao_template'),
	url(r'^modules/dao_template/post_add', views.post_creer_dao_template, name='module_configuration_post_add_dao_template'),

	#SOUS MODULES
	url(r'^sous_modules/list/(?P<ref>[0-9]+)/$', views.get_lister_sous_modules_of_module, name='module_configuration_list_sous_modules'),
	url(r'^sous_modules/add/(?P<ref>[0-9]+)/$', views.get_creer_sous_module_of_module, name='module_configuration_add_sous_module'),
	url(r'^sous_modules/post_add/(?P<ref>[0-9]+)/$', views.post_creer_sous_module_of_module, name='module_configuration_post_add_sous_module'),
	url(r'^sous_modules/item/(?P<ref>[0-9]+)/(?P<ref2>[0-9]+)/$', views.get_details_sous_module_of_module, name='module_configuration_details_sous_module'),
	url(r'^sous_modules/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_sous_module_of_module, name='module_configuration_update_sous_module'),
	url(r'^sous_modules/item/module/post_update', views.post_modifier_sous_module_of_module, name='module_configuration_post_update_sous_module'),
    url(r'^ajax/sous_modules/get/model/related/$', views.ajax_get_related_models, name="ajax_get_related_models"),
	
	#WORKFLOW
	url(r'^workflow/list', views.get_lister_workflow, name='module_configuration_list_workflow'),
	url(r'^workflow/add', views.get_creer_workflow, name='module_configuration_add_workflow'),
	url(r'^workflow/post_add', views.post_creer_workflow, name='module_configuration_post_add_workflow'),
	url(r'^workflow/item/(?P<ref>[0-9]+)/$', views.get_details_workflow, name='module_configuration_detail_workflow'),

	#ETAPE
	#url(r'^etape/list', views.get_lister_etape, name='module_configuration_list_etape'),
	url(r'^etape/add/(?P<ref>[0-9]+)', views.get_creer_etape, name='module_configuration_add_etape'),
	url(r'^etape/post_add', views.post_creer_etape, name='module_configuration_post_add_etape'),

	# TRANSITION
	url(r'^transition/add/(?P<ref>[0-9]+)', views.get_creer_transition, name='module_configuration_add_transition'),
	url(r'^transition/post_add', views.post_creer_transition, name='module_configuration_post_add_transition'),


	# REGLES URLS
	url(r'^regle/list', views.get_lister_regle, name='module_configuration_list_regle'),
	url(r'^regle/add', views.get_creer_regle, name='module_configuration_add_regle'),
	url(r'^regle/item/(?P<ref>[0-9]+)/$', views.get_details_regle, name='module_configuration_details_regle'),
	url(r'^regle/post_add', views.post_creer_regle, name='module_configuration_post_add_regle'),
	
]
urlpatterns.append(url(r'^permission/list', views.get_lister_permission, name = 'module_Configuration_list_permission'))
urlpatterns.append(url(r'^permission/add', views.get_creer_permission, name = 'module_Configuration_add_permission'))
urlpatterns.append(url(r'^permission/post_add', views.post_creer_permission, name = 'module_Configuration_post_add_permission'))
urlpatterns.append(url(r'^permission/item/(?P<ref>[0-9]+)/$', views.get_details_permission, name = 'module_Configuration_detail_permission'))
urlpatterns.append(url(r'^permission/item/post_update/$', views.post_modifier_permission, name = 'module_Configuration_post_update_permission'))
urlpatterns.append(url(r'^permission/item/(?P<ref>[0-9]+)/update$', views.get_modifier_permission, name = 'module_Configuration_update_permission'))
urlpatterns.append(url(r'^actionutilisateur/list', views.get_lister_actionutilisateur, name = 'module_Configuration_list_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/add', views.get_creer_actionutilisateur, name = 'module_Configuration_add_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/post_add', views.post_creer_actionutilisateur, name = 'module_Configuration_post_add_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/item/(?P<ref>[0-9]+)/$', views.get_details_actionutilisateur, name = 'module_Configuration_detail_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/item/post_update/$', views.post_modifier_actionutilisateur, name = 'module_Configuration_post_update_actionutilisateur'))
urlpatterns.append(url(r'^actionutilisateur/item/(?P<ref>[0-9]+)/update$', views.get_modifier_actionutilisateur, name = 'module_Configuration_update_actionutilisateur'))
urlpatterns.append(url(r'^sousmodule/list', views.get_lister_sousmodule, name = 'module_Configuration_list_sousmodule'))
urlpatterns.append(url(r'^sousmodule/add', views.get_creer_sousmodule, name = 'module_Configuration_add_sousmodule'))
urlpatterns.append(url(r'^sousmodule/post_add', views.post_creer_sousmodule, name = 'module_Configuration_post_add_sousmodule'))
urlpatterns.append(url(r'^sousmodule/item/(?P<ref>[0-9]+)/$', views.get_details_sousmodule, name = 'module_Configuration_detail_sousmodule'))
urlpatterns.append(url(r'^sousmodule/item/post_update/$', views.post_modifier_sousmodule, name = 'module_Configuration_post_update_sousmodule'))
urlpatterns.append(url(r'^sousmodule/item/(?P<ref>[0-9]+)/update$', views.get_modifier_sousmodule, name = 'module_Configuration_update_sousmodule'))
urlpatterns.append(url(r'^groupemenu/list', views.get_lister_groupemenu, name = 'module_Configuration_list_groupemenu'))
urlpatterns.append(url(r'^groupemenu/add', views.get_creer_groupemenu, name = 'module_Configuration_add_groupemenu'))
urlpatterns.append(url(r'^groupemenu/post_add', views.post_creer_groupemenu, name = 'module_Configuration_post_add_groupemenu'))
urlpatterns.append(url(r'^groupemenu/item/(?P<ref>[0-9]+)/$', views.get_details_groupemenu, name = 'module_Configuration_detail_groupemenu'))
urlpatterns.append(url(r'^groupemenu/item/post_update/$', views.post_modifier_groupemenu, name = 'module_Configuration_post_update_groupemenu'))
urlpatterns.append(url(r'^groupemenu/item/(?P<ref>[0-9]+)/update$', views.get_modifier_groupemenu, name = 'module_Configuration_update_groupemenu'))


urlpatterns.append(url(r'^sousmodule/wizard', views.get_creer_wizard_menu, name = 'module_Configuration_add_wizard_menu'))
urlpatterns.append(url(r'^sousmodule/post_wizard', views.post_creer_wizard_menu, name = 'module_Configuration_post_add_wizard_menu'))
