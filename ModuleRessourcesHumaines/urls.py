from django.conf.urls import include, url
from ModuleRessourcesHumaines import views
from ModuleRessourcesHumaines.payroll.views import get_calcul_paie_employe
from ModuleRessourcesHumaines.payroll.views import get_calcul_paie_dossier
from ModuleRessourcesHumaines.payroll.views import get_calcul_paie_list
from ModuleRessourcesHumaines.payroll.views import get_test_bareme
from ModuleRessourcesHumaines.presence import views as viewed
from ModuleRessourcesHumaines.conge import views as viewedconge


from ModuleRessourcesHumaines.parc_auto import views as viewedparc

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'employe', views.EmployeViewSet)
router.register(r'departement', views.DepartementViewSet)
router.register(r'poste', views.PosteViewSet)
router.register(r'lot', views.LotBulletinViewSet)
router.register(r'bulletin', views.BulletinViewSet)
router.register(r'element', views.ElementBulletinViewSet)
router.register(r'bareme', views.BaremeViewSet)
router.register(r'profilpaye', views.ProfilViewSet)
##
router.register(r'presence', viewed.PresenceViewSet)
router.register(r'presenceof', viewed.PresenceOfViewSet)
##
router.register(r'typeconge', viewedconge.TypeCongeViewSet)

router.register(r'conge', viewedconge.CongeDemandeViewSet)
router.register(r'congedemande', viewedconge.CongeDemandeViewSet)
router.register(r'congeapprouve', viewedconge.CongeApprouveViewsSet)
router.register(r'congerejeter', viewedconge.CongeRejeterViewSet)
router.register(r'congebytype', viewedconge.CongeByTypeViewSet)
##

router.register(r'modelvehicule', viewedparc.ModelVehiculeViewSet)
router.register(r'vehicule', viewedparc.VehiculeViewSet)
##


urlpatterns=[

    url(r'all_poste_departement', views.get_json_poste,
        name='module_rh_get_poste_of_departement'),
    url(r'all_employee_departement', views.get_json_employe,
        name='module_rh_get_employe_of_departement'),
    url(r'formation/personnels', views.lister_personnel_part_dep_json,
        name='module_rh_list_employe_formation'),
    url(r'all_formation_by_month', views.get_json_ListeFormation,
        name='module_rh_get_listeformation_by_month'),
    url(r'all_conge_by_month', views.get_json_ListeConge,
        name='module_rh_get_listeconge_by_month'),


    url(r'^pret/item/validate', views.post_valider_pret, name='module_ressourceshumaines_validate_pret'),
    url(r'get_poste_of_unite_fonctionnelle', views.get_json_poste_of_unite_fonctionnelle, name='module_rh_get_json_poste_of_ou'),

]


urlpatterns.append(url(r'^tableau', views.get_dashboard, name = 'module_rh_tableau_de_bord'))
urlpatterns.append(url(r'^notification/vue/(?P<ref>[0-9]+)/', views.get_update_notification, name = 'module_rh_notification'))

#Api
urlpatterns.append(url(r'^api/', include(router.urls)))

# EMPLOYES URLS
urlpatterns.append(url(r'^employe/list', views.get_lister_employe, name = 'module_rh_list_employe'))
urlpatterns.append(url(r'^employe/add', views.get_creer_employe, name = 'module_rh_add_employe'))
urlpatterns.append(url(r'^employe/post_add', views.post_creer_employe, name = 'module_rh_post_add_employe'))
urlpatterns.append(url(r'^employe/item/(?P<ref>[0-9]+)/$', views.get_details_employe, name = 'module_rh_detail_employe'))
urlpatterns.append(url(r'^employe/item/(?P<ref>[0-9]+)/carreer/$', views.get_details_carriere_employe, name = 'module_rh_detail_carriere_employe'))
urlpatterns.append(url(r'^employe/me/$', views.get_details_employe_me, name = 'module_rh_detail_employe_me'))
urlpatterns.append(url(r'^employes/departement/list/(?P<filter>[0-9]+)/$', views.get_lister_employes_of_departement, name='module_rh_list_employe_of_departement'))
urlpatterns.append(url(r'^employe/update/(?P<ref>[0-9]+)/$', views.get_modifier_employe, name = 'module_rh_update_employe'))
urlpatterns.append(url(r'^employe/post_update', views.post_modifier_employe, name = 'module_rh_post_update_employe'))
urlpatterns.append(url(r'^employe/upload/add', views.get_upload_employe, name='module_ressourceshumaines_get_upload_employe'))
urlpatterns.append(url(r'^employe/upload/post_add', views.post_upload_employe, name='module_ressourceshumaines_post_upload_employe'))
urlpatterns.append(url(r'^employe/upload_dependant/add', views.get_upload_dependant_employe, name='module_ressourceshumaines_get_upload_dependant_employe'))
urlpatterns.append(url(r'^employe/post_upload_dependant/add', views.post_upload_dependant, name='module_ressourceshumaines_post_upload_dependant'))
urlpatterns.append(url(r'^employe/upload_mail/add', views.get_upload_mailing_employe, name='module_ressourceshumaines_get_upload_mailing_employe'))
urlpatterns.append(url(r'^employe/upload_mail/post_add', views.post_upload_email_employe, name='module_ressourceshumaines_post_upload_email_employe'))
urlpatterns.append(url(r'^employe/statut/update/(?P<ref>[0-9]+)/$', views.get_modifier_statut_employe, name = 'module_rh_update_statut_employe'))
urlpatterns.append(url(r'^employe/statut/post_updad/', views.post_modifier_statut_employe, name='module_ressourceshumaines_post_update_statut_employe'))

#TYPE DIPLOME URLS
urlpatterns.append(url(r'^type_diplome/list', views.get_lister_type_diplome, name='module_ressourceshumaines_list_type_diplome'))
urlpatterns.append(url(r'^type_diplome/add', views.get_creer_typediplome, name = 'module_ressourceshumaines_add_type_diplome'))
urlpatterns.append(url(r'^type_diplome/post_add', views.post_creer_typediplome, name = 'module_ressourceshumaines_post_add_type_diplome'))
urlpatterns.append(url(r'^type_diplome/item/(?P<ref>[0-9]+)/$', views.get_details_type_diplome, name = 'module_ressourceshumaines_detail_type_diplome'))
urlpatterns.append(url(r'^type_diplome/update/(?P<ref>[0-9]+)/$', views.get_modifier_type_diplome, name = 'module_ressourceshumaines_update_type_diplome'))
urlpatterns.append(url(r'^type_diplome/post_update', views.post_modifier_type_diplome, name = 'module_ressourceshumaines_post_update_type_diplome'))

#DIPLOME URLS
urlpatterns.append(url(r'^diplome/list', views.get_lister_diplome, name='module_ressourceshumaines_list_diplome'))
urlpatterns.append(url(r'^diplome/add', views.get_creer_diplome, name = 'module_ressourceshumaines_add_diplome'))
urlpatterns.append(url(r'^diplome/post_add', views.post_creer_diplome, name = 'module_ressourceshumaines_post_add_diplome'))
urlpatterns.append(url(r'^diplome/item/(?P<ref>[0-9]+)/$', views.get_details_diplome, name = 'module_ressourceshumaines_detail_diplome'))
urlpatterns.append(url(r'^diplome/update/(?P<ref>[0-9]+)/$', views.get_modifier_diplome, name = 'module_ressourceshumaines_update_diplome'))
urlpatterns.append(url(r'^diplome/post_update', views.post_modifier_diplome, name = 'module_ressourceshumaines_post_update_diplome'))

urlpatterns.append(url(r'^employe/getAdressBanque_json',views.getAdressBanque_json, name='module_rh_getAdressBanque_json'))
# DEPARTEMENT URLS
urlpatterns.append(url(r'^departement/list', views.get_lister_departement, name = 'module_rh_list_departement'))
urlpatterns.append(url(r'^departement/type/(?P<ref>[0-9]+)/list', views.get_lister_departement_of_type, name = 'module_ressourceshumaines_list_departement'))
urlpatterns.append(url(r'^departement/(?P<ref>[0-9]+)/add', views.get_creer_departement, name = 'module_rh_add_departement'))
urlpatterns.append(url(r'^departement/post_add', views.post_creer_departement, name = 'module_rh_post_add_departement'))
urlpatterns.append(url(r'^departement/item/(?P<ref>[0-9]+)/$', views.get_details_departement, name = 'module_rh_detail_departement'))
urlpatterns.append(url(r'^departement/update/(?P<ref>[0-9]+)/$', views.get_modifier_departement, name = 'module_rh_update_departement'))
urlpatterns.append(url(r'^departement/post_update', views.post_modifier_departement, name = 'module_rh_post_update_departement'))

urlpatterns.append(url(r'^departement/(?P<idt>[0-9]+)/postes/item/(?P<ref>[0-9]+)/$', views.get_details_poste_of_departement, name='module_ressources_humaines_detail_poste_from_department'))
urlpatterns.append(url(r'^departement/(?P<ref>[0-9]+)/postes/add', views.get_creer_poste_of_departement, name='module_ressources_humaines_add_poste_from_department'))
urlpatterns.append(url(r'^departement/postes/post_add', views.post_creer_poste_of_departement, name='module_ressources_humaines_post_add_from_department'))

urlpatterns.append(url(r'^departement/(?P<idt>[0-9]+)/postes/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_poste_of_departement, name='module_ressources_humaines_update_poste_from_department'))
urlpatterns.append(url(r'^departement/postes/item/post_update/$', views.post_modifier_poste_of_departement, name='module_ressources_humaines_post_update_poste_from_department'))

urlpatterns.append(url(r'^departement/upload/add', views.get_upload_departement, name='module_ressourceshumaines_get_upload_departement'))
urlpatterns.append(url(r'^departement/upload/post_add', views.post_upload_departement, name='module_ressourceshumaines_post_upload_departement'))

# POSTES URLS
urlpatterns.append(url(r'^postes/list', views.get_lister_postes, name='module_ressources_humaines_list_postes'))

urlpatterns.append(url(r'^postes/add', views.get_creer_poste, name='module_ressources_humaines_add_poste'))
urlpatterns.append(url(r'^postes/post_add', views.post_creer_poste, name='module_ressources_humaines_post_add_poste'))
urlpatterns.append(url(r'^postes/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_poste, name='module_ressources_humaines_update_poste'))
urlpatterns.append(url(r'^postes/item/post_update/$', views.post_modifier_poste, name='module_ressources_humaines_post_update_poste'))
urlpatterns.append(url(r'^postes/item/(?P<ref>[0-9]+)/$', views.get_details_poste, name='module_ressources_humaines_details_poste'))
urlpatterns.append(url(r'^postes/upload/add', views.get_upload_poste, name='module_ressourceshumaines_get_upload_poste'))
urlpatterns.append(url(r'^postes/upload/post_add', views.post_upload_poste, name='module_ressourceshumaines_post_upload_poste'))

# DOSSIER SOCIAL DE L'EMPLOYE
urlpatterns.append(url(r'^dossier_social/list', views.get_lister_dossier_social, name='module_ressources_humaines_list_dossier_social'))
urlpatterns.append(url(r'^dossier_social/add', views.get_creer_dossier_social, name='module_ressources_humaines_add_dossier_social'))
urlpatterns.append(url(r'^dossier_social/post_add', views.post_creer_dossier_social, name='module_ressources_humaines_post_add_dossier_social'))
urlpatterns.append(url(r'^dossier_social/item/(?P<ref>[0-9]+)/$', views.get_details_dossier_social, name='module_ressources_humaines_details_dossier_social'))
urlpatterns.append(url(r'^dossier_social/update/item/(?P<ref>[0-9]+)/$', views.get_modifier_dossier_social, name='module_ressources_humaines_update_dossier_social'))
urlpatterns.append(url(r'^dossier_social/post_update', views.post_modifier_dossier_social, name='module_ressources_humaines_post_update_dossier_social'))

urlpatterns.append(url(r'^dossier_social/upload/add', views.get_upload_dossier_social, name='module_ressourceshumaines_get_upload_dossier_social'))
urlpatterns.append(url(r'^dossier_social/upload/post_add', views.post_upload_dossier_social, name='module_ressourceshumaines_post_upload_dossier_social'))

#FONCTION
urlpatterns.append(url(r'^fonction/add', views.get_creer_fonction,name='module_ressources_humaines_add_fonction'))
urlpatterns.append(url(r'^fonction/post_add', views.post_creer_fonction_of_departement,name='module_ressources_humaines_post_add_fonction'))
urlpatterns.append(url(r'^fonction/list', views.get_lister_fonction,name='module_ressources_humaines_list_fonction'))
urlpatterns.append(url(r'^fonction/item/(?P<ref>[0-9]+)/$', views.get_details_fonction,name='module_ressources_humaines_details_fonction'))
urlpatterns.append(url(r'^fonction/update/item/(?P<ref>[0-9]+)/$',views.get_modifier_fonction, name='module_ressources_humaines_update_fonction'))
urlpatterns.append(url(r'^fonction/post_update', views.post_modifier_fonction_of_departement,name='module_ressources_humaines_post_update_fonction'))

urlpatterns.append(url(r'^fonction/upload/add', views.get_upload_fonction, name='module_ressourceshumaines_get_upload_fonction'))
urlpatterns.append(url(r'^fonction/upload/post_add', views.post_upload_fonction, name='module_ressourceshumaines_post_upload_fonction'))

"""
urlpatterns.append(url(r'^grade/list', views.get_lister_grade, name = 'module_rh_list_grade'))
urlpatterns.append(url(r'^grade/add', views.get_creer_grade, name = 'module_rh_add_grade'))
urlpatterns.append(url(r'^grade/post_add', views.post_creer_grade, name = 'module_rh_post_add_grade'))
urlpatterns.append(url(r'^grade/item/(?P<ref>[0-9]+)/$', views.get_details_grade, name = 'module_rh_detail_grade'))
urlpatterns.append(url(r'^dependant/list', views.get_lister_dependant, name = 'module_rh_list_dependant'))
urlpatterns.append(url(r'^dependant/add', views.get_creer_dependant, name = 'module_rh_add_dependant'))
urlpatterns.append(url(r'^dependant/post_add', views.post_creer_dependant, name = 'module_rh_post_add_dependant'))
urlpatterns.append(url(r'^dependant/item/(?P<ref>[0-9]+)/$', views.get_details_dependant, name = 'module_rh_detail_dependant'))
urlpatterns.append(url(r'^profil_paie/list', views.get_lister_profil_paie, name = 'module_rh_list_profil_paie'))
urlpatterns.append(url(r'^profil_paie/add', views.get_creer_profil_paie, name = 'module_rh_add_profil_paie'))
urlpatterns.append(url(r'^profil_paie/post_add', views.post_creer_profil_paie, name = 'module_rh_post_add_profil_paie'))
urlpatterns.append(url(r'^profil_paie/item/(?P<ref>[0-9]+)/$', views.get_details_profil_paie, name = 'module_rh_detail_profil_paie'))
urlpatterns.append(url(r'^ordre_paie/list', views.get_lister_ordre_paie, name = 'module_rh_list_ordre_paie'))
urlpatterns.append(url(r'^ordre_paie/add', views.get_creer_ordre_paie, name = 'module_rh_add_ordre_paie'))
urlpatterns.append(url(r'^ordre_paie/post_add', views.post_creer_ordre_paie, name = 'module_rh_post_add_ordre_paie'))
urlpatterns.append(url(r'^ordre_paie/item/(?P<ref>[0-9]+)/$', views.get_details_ordre_paie, name = 'module_rh_detail_ordre_paie'))
urlpatterns.append(url(r'^pret/list', views.get_lister_pret, name = 'module_rh_list_pret'))
urlpatterns.append(url(r'^pret/add', views.get_creer_pret, name = 'module_rh_add_pret'))
urlpatterns.append(url(r'^pret/post_add', views.post_creer_pret, name = 'module_rh_post_add_pret'))
urlpatterns.append(url(r'^pret/item/(?P<ref>[0-9]+)/$', views.get_details_pret, name = 'module_rh_detail_pret'))
urlpatterns.append(url(r'^conge/list', views.get_lister_conge, name = 'module_rh_list_conge'))
urlpatterns.append(url(r'^conge/add', views.get_creer_conge, name = 'module_rh_add_conge'))
urlpatterns.append(url(r'^conge/post_add', views.post_creer_conge, name = 'module_rh_post_add_conge'))
urlpatterns.append(url(r'^conge/item/(?P<ref>[0-9]+)/$', views.get_details_conge, name = 'module_rh_detail_conge'))
"""

urlpatterns.append(url(r'^presence/list', viewed.get_lister_presence, name = 'module_ressourceshumaines_list_presence'))
urlpatterns.append(url(r'^presence/add', viewed.get_creer_presence, name = 'module_ressourceshumaines_add_presence'))
urlpatterns.append(url(r'^presence/post_add/(?P<boole>[0-9]+)/$', viewed.post_creer_presence, name = 'module_ressourceshumaines_post_add_presence'))
urlpatterns.append(url(r'^presence/item/(?P<ref>[0-9]+)/$', viewed.get_details_presence, name = 'module_ressourceshumaines_detail_presence'))
urlpatterns.append(url(r'^presence/item/post_update/$', viewed.post_modifier_presence, name = 'module_ressourceshumaines_post_update_presence'))
urlpatterns.append(url(r'^presence/item/(?P<ref>[0-9]+)/update$', viewed.get_modifier_presence, name = 'module_ressourceshumaines_update_presence'))
urlpatterns.append(url(r'^presence/employe', viewed.get_lister_employe, name = 'module_ressourceshumaines_list_presence_employe'))
urlpatterns.append(url(r'^presence/item_employe/(?P<ref>[0-9]+)/$', viewed.get_lister_presence_employe, name = 'module_ressourceshumaines_detail_presence_employe'))
urlpatterns.append(url(r'^presence/add_employe/(?P<ref>[0-9]+)/$', viewed.get_creer_presence_employe, name = 'module_ressourceshumaines_add_presence_employe'))
urlpatterns.append(url(r'^presence/update_employe/(?P<ref>[0-9]+)/$', viewed.get_creer_presence_employe, name = 'module_ressourceshumaines_add_presence_employe'))

urlpatterns.append(url(r'^type_conge/list', viewedconge.get_lister_type_conge, name = 'module_ressourceshumaines_list_type_conge'))
urlpatterns.append(url(r'^type_conge/conge/(?P<types>[0-9]+)/$', viewedconge.get_lister_congebyType, name = 'module_ressourceshumaines_list_conge_by_type'))
urlpatterns.append(url(r'^type_conge/add', viewedconge.get_creer_type_conge, name = 'module_ressourceshumaines_add_type_conge'))
urlpatterns.append(url(r'^type_conge/post_add', viewedconge.post_creer_type_conge, name = 'module_ressourceshumaines_post_add_type_conge'))
urlpatterns.append(url(r'^type_conge/item/(?P<ref>[0-9]+)/$', viewedconge.get_details_type_conge, name = 'module_ressourceshumaines_detail_type_conge'))
urlpatterns.append(url(r'^type_conge/item/post_update/$', viewedconge.post_modifier_type_conge, name = 'module_ressourceshumaines_post_update_type_conge'))
urlpatterns.append(url(r'^type_conge/item/(?P<ref>[0-9]+)/update$', viewedconge.get_modifier_type_conge, name = 'module_ressourceshumaines_update_type_conge'))

urlpatterns.append(url(r'^type_conge/upload/add', viewedconge.get_upload_type_conge, name='module_ressourceshumaines_get_upload_type_conge'))
urlpatterns.append(url(r'^type_conge/upload/post_add', viewedconge.post_upload_type_conge, name='module_ressourceshumaines_post_upload_type_conge'))

urlpatterns.append(url(r'^conge/accueil', viewedconge.get_index_conge, name = 'module_ressourceshumaines_index_conge'))

urlpatterns.append(url(r'^conge/add', viewedconge.get_creer_conge, name = 'module_ressourceshumaines_add_conge'))
urlpatterns.append(url(r'^conge/post_add', viewedconge.post_creer_conge, name = 'module_ressourceshumaines_post_add_conge'))
urlpatterns.append(url(r'^conge/item/(?P<ref>[0-9]+)/$', viewedconge.get_details_conge, name = 'module_ressourceshumaines_detail_conge'))
urlpatterns.append(url(r'^conge/item/post_update/$', viewedconge.post_modifier_conge, name = 'module_ressourceshumaines_post_update_conge'))
urlpatterns.append(url(r'^conge/item/(?P<ref>[0-9]+)/update$', viewedconge.get_modifier_conge, name = 'module_ressourceshumaines_update_conge'))

urlpatterns.append(url(r'^conge/list_demande', viewedconge.get_lister_demande_conge, name = 'module_ressourceshumaines_list_demande_conge'))
urlpatterns.append(url(r'^conge/list_approuve', viewedconge.get_lister_conge_approuve, name = 'module_ressourceshumaines_list_conge_approuve'))
urlpatterns.append(url(r'^conge/list_reject', viewedconge.get_lister_conge_reject, name = 'module_ressourceshumaines_list_conge_reject'))

urlpatterns.append(url(r'^conge/list', viewedconge.get_lister_conge, name = 'module_ressourceshumaines_list_conge'))

urlpatterns.append(url(r'^conge/upload/add', viewedconge.get_upload_conge, name='module_ressourceshumaines_get_upload_conge'))
urlpatterns.append(url(r'^conge/upload/post_add', viewedconge.post_upload_conge, name='module_ressourceshumaines_post_upload_conge'))



urlpatterns.append(url(r'^vehicule_model/list', viewedparc.get_lister_vehicule_model, name = 'module_ressourceshumaines_list_vehicule_model'))
urlpatterns.append(url(r'^vehicule_model/add', viewedparc.get_creer_vehicule_model, name = 'module_ressourceshumaines_add_vehicule_model'))
urlpatterns.append(url(r'^vehicule_model/post_add', viewedparc.post_creer_vehicule_model, name = 'module_ressourceshumaines_post_add_vehicule_model'))
urlpatterns.append(url(r'^vehicule_model/item/(?P<ref>[0-9]+)/$', viewedparc.get_details_vehicule_model, name = 'module_ressourceshumaines_detail_vehicule_model'))
urlpatterns.append(url(r'^vehicule_model/item/post_update/$', viewedparc.post_modifier_vehicule_model, name = 'module_ressourceshumaines_post_update_vehicule_model'))
urlpatterns.append(url(r'^vehicule_model/item/(?P<ref>[0-9]+)/update$', viewedparc.get_modifier_vehicule_model, name = 'module_ressourceshumaines_update_vehicule_model'))
urlpatterns.append(url(r'^vehicule/list', viewedparc.get_lister_vehicule, name = 'module_ressourceshumaines_list_vehicule'))
urlpatterns.append(url(r'^vehicule/add', viewedparc.get_creer_vehicule, name = 'module_ressourceshumaines_add_vehicule'))
urlpatterns.append(url(r'^vehicule/post_add', viewedparc.post_creer_vehicule, name = 'module_ressourceshumaines_post_add_vehicule'))
urlpatterns.append(url(r'^vehicule/item/(?P<ref>[0-9]+)/$', viewedparc.get_details_vehicule, name = 'module_ressourceshumaines_detail_vehicule'))
urlpatterns.append(url(r'^vehicule/item/post_update/$', viewedparc.post_modifier_vehicule, name = 'module_ressourceshumaines_post_update_vehicule'))
urlpatterns.append(url(r'^vehicule/item/(?P<ref>[0-9]+)/update$', viewedparc.get_modifier_vehicule, name = 'module_ressourceshumaines_update_vehicule'))

#Pret
urlpatterns.append(url(r'^pret/list', views.get_lister_prets, name='module_ressourceshumaines_list_pret'))
urlpatterns.append(url(r'^pret/add', views.get_creer_pret, name='module_ressourceshumaines_add_pret'))
urlpatterns.append(url(r'^pret/post_add', views.post_creer_pret, name='module_ressourceshumaines_post_add_pret'))
urlpatterns.append(url(r'^pret/item/(?P<ref>[0-9]+)/update/$', views.get_modifier_pret, name='module_ressourceshumaines_update_pret'))
urlpatterns.append(url(r'^pret/item/post_update/$', views.post_modifier_pret, name='module_ressourceshumaines_post_update_pret'))
urlpatterns.append(url(r'^pret/item/(?P<ref>[0-9]+)/$', views.get_details_pret, name='module_ressourceshumaines_details_pret'))

#Paiement Interne
urlpatterns.append(url(r'^paiement/list', views.get_lister_paiement_internes, name='module_ressourceshumaines_list_paiement_interne'))
urlpatterns.append(url(r'^paiement/item/(?P<ref>[0-9]+)/$', views.get_details_paiement_interne, name='module_ressourceshumaines_details_paiement_interne'))
#urlpatterns.append(url(r'^paiement/alloc/add/(?P<ref>[0-9]+)/$', views.get_paiement_allocation, name='module_ressourceshumaines_add_paiement_allocation'))
urlpatterns.append(url(r'^paiement/alloc/post_add', views.post_paiement_allocation, name='module_ressourceshumaines_post_add_paiement_allocation'))
#urlpatterns.append(url(r'^paiement/pret/add/(?P<ref>[0-9]+)/$', views.get_paiement_pret, name='module_ressourceshumaines_add_paiement_pret'))
urlpatterns.append(url(r'^paiement/pret/post_add', views.post_paiement_pret, name='module_ressourceshumaines_post_add_paiement_pret'))


urlpatterns.append(url(r'^categorie_employe/list', views.get_lister_categorie_employe, name = 'module_ressourceshumaines_list_categorie_employe'))
urlpatterns.append(url(r'^categorie_employe/add', views.get_creer_categorie_employe, name = 'module_ressourceshumaines_add_categorie_employe'))
urlpatterns.append(url(r'^categorie_employe/post_add', views.post_creer_categorie_employe, name = 'module_ressourceshumaines_post_add_categorie_employe'))
urlpatterns.append(url(r'^categorie_employe/item/(?P<ref>[0-9]+)/$', views.get_details_categorie_employe, name = 'module_ressourceshumaines_detail_categorie_employe'))
urlpatterns.append(url(r'^categorie_employe/item/post_update/$', views.post_modifier_categorie_employe, name = 'module_ressourceshumaines_post_update_categorie_employe'))
urlpatterns.append(url(r'^categorie_employe/item/(?P<ref>[0-9]+)/update$', views.get_modifier_categorie_employe, name = 'module_ressourceshumaines_update_categorie_employe'))

urlpatterns.append(url(r'^categorie_employe/upload/add', views.get_upload_categorie_employe, name='module_ressourceshumaines_get_upload_categorie_employe'))
urlpatterns.append(url(r'^categorie_employe/upload/post_add', views.post_upload_categorie_employe, name='module_ressourceshumaines_post_upload_categorie_employe'))


urlpatterns.append(url(r'^syndicat/list', views.get_lister_syndicat, name = 'module_ressourceshumaines_list_syndicat'))
urlpatterns.append(url(r'^syndicat/add', views.get_creer_syndicat, name = 'module_ressourceshumaines_add_syndicat'))
urlpatterns.append(url(r'^syndicat/post_add', views.post_creer_syndicat, name = 'module_ressourceshumaines_post_add_syndicat'))
urlpatterns.append(url(r'^syndicat/item/(?P<ref>[0-9]+)/$', views.get_details_syndicat, name = 'module_ressourceshumaines_detail_syndicat'))
urlpatterns.append(url(r'^syndicat/item/post_update/$', views.post_modifier_syndicat, name = 'module_ressourceshumaines_post_update_syndicat'))
urlpatterns.append(url(r'^syndicat/item/(?P<ref>[0-9]+)/update$', views.get_modifier_syndicat, name = 'module_ressourceshumaines_update_syndicat'))

urlpatterns.append(url(r'^syndicat/item/(?P<ref>[0-9]+)/ligne_syndicat$', views.get_creer_ligne_syndicat, name = 'module_ressourceshumaines_add_ligne_syndicat'))

urlpatterns.append(url(r'^syndicat/ligne_syndicat/post_add', views.post_creer_ligne_syndicat, name = 'module_ressourceshumaines_post_add_ligne_syndicat'))

urlpatterns.append(url(r'^syndicat/upload/add', views.get_upload_syndicat, name='module_ressourceshumaines_get_upload_syndicat'))
urlpatterns.append(url(r'^syndicat/upload/post_add', views.post_upload_syndicat, name='module_ressourceshumaines_post_upload_syndicat'))

urlpatterns.append(url(r'^employe/evaluation/list', views.get_lister_employe_for_evaluation, name = 'module_ressourceshumaines_list_employe_for_evaluation'))

urlpatterns.append(url(r'^employe/competence/list', views.get_lister_employe_for_competence, name = 'module_ressourceshumaines_list_employe_for_competence'))
urlpatterns.append(url(r'^competence/item/(?P<idt>[0-9]+)/$', views.get_details_competence, name = 'module_ressourceshumaines_detail_competence'))
urlpatterns.append(url(r'^employe/(?P<idt>[0-9]+)/competence/add', views.get_creer_ligne_competence, name = 'module_ressourceshumaines_add_competence'))
urlpatterns.append(url(r'^competence/post_add', views.post_creer_ligne_competence, name = 'module_ressourceshumaines_post_add_competence'))

urlpatterns.append(url(r'^competence/upload/add', views.get_upload_competence, name='module_ressourceshumaines_get_upload_competence'))
urlpatterns.append(url(r'^competence/upload/post_add', views.post_upload_competence, name='module_ressourceshumaines_post_upload_competence'))

#RH_Mouvement Personnel
urlpatterns.append(url(r'^employe/overview', views.list_more_info_personnel_mouvement, name = 'module_ressourceshumaines_list_more_info_personnel_mouvement'))


# RH_INDICATEURS
urlpatterns.append(url(r'^indicateurs/suivi', views.get_indicateurs_principaux_de_suivi, name = 'module_ressourceshumaines_get_indicateurs_principaux_de_suivi'))
urlpatterns.append(url(r'^indicateurs/formation_pro', views.get_indicateurs_formation_prof, name = 'module_ressourceshumaines_get_indicateurs_formation_prof'))
urlpatterns.append(url(r'^indicateurs/formation_famille', views.get_indicateurs_formation_famille_prof, name = 'module_ressourceshumaines_get_indicateurs_formation_famille_prof'))
#RH_Masse_salariale Update Mouvement Personnel information
urlpatterns.append(url(r'^employe/post_ms_overview', views.post_mouvement_Personnel_masse_salariale, name = 'module_ressourceshumaines_post_mouvement_Personnel_masse_salariale'))
urlpatterns.append(url(r'^employe/post_ps_overview', views.post_mouvement_Personnel_propagatio_stage, name = 'module_ressourceshumaines_post_mouvement_Personnel_propagationstage'))
urlpatterns.append(url(r'^employe/post_st_overview', views.post_mouvement_Personnel_total_mise_stage, name = 'module_ressourceshumaines_post_mouvement_Personnel_total_mise_stage'))
urlpatterns.append(url(r'^employe/post_D_Def_overview', views.post_mouvement_Personnel_depart_def, name = 'module_ressourceshumaines_post_mouvement_Personnel_Depart_def'))
urlpatterns.append(url(r'^employe/post_D_Prov_overview', views.post_mouvement_Personnel_Depart_provoir, name = 'module_ressourceshumaines_post_mouvement_Personnel_Depart_prov'))
urlpatterns.append(url(r'^employe/post_Eff_physique_overview', views.post_mouvement_Personnel_eff_physique, name = 'module_ressourceshumaines_post_mouvement_Personnel_eff_physique'))
urlpatterns.append(url(r'^employe/post_D_vol_overview', views.post_mouvement_Personnel_Depart_vol, name = 'module_ressourceshumaines_post_mouvement_Personnel_D_vol'))
urlpatterns.append(url(r'^employe/post_Demission_overview', views.post_mouvement_Personnel_Demission, name = 'module_ressourceshumaines_post_mouvement_Personnel_Demision'))
urlpatterns.append(url(r'^employe/post_arriver_overview', views.post_mouvement_Personnel_arriver, name = 'module_ressourceshumaines_post_mouvement_Personnel_Arriver'))
urlpatterns.append(url(r'^employe/post_post_vac_overview', views.post_mouvement_Personnel_post_vacant, name = 'module_ressourceshumaines_post_mouvement_Personnel_post_vac'))
urlpatterns.append(url(r'^employe/post_vac_prevu_overview', views.post_mouvement_Personnel_poste_vacant_pouvu, name = 'module_ressourceshumaines_post_mouvement_Personnel_poste_vacant_pouvu'))
urlpatterns.append(url(r'^employe/post_recru_overview', views.post_mouvement_Personnel_recru_emploi_permanent, name = 'module_ressourceshumaines_post_mouvement_Personnel_recru_emploi_permanent'))
urlpatterns.append(url(r'^employe/post_concour_overview', views.post_mouvement_Personnel_concours, name = 'module_ressourceshumaines_post_mouvement_Personnel_concours'))
urlpatterns.append(url(r'^employe/post_mutation_overview', views.post_mouvement_Personnel_mutation, name = 'module_ressourceshumaines_post_mouvement_Personnel_mutation'))
urlpatterns.append(url(r'^employe/post_detachement_overview', views.post_mouvement_Personnel_detachement, name = 'module_ressourceshumaines_post_mouvement_Personnel_detachement'))
urlpatterns.append(url(r'^employe/post_recru_direct_overview', views.post_mouvement_Personnel_recru_direct, name = 'module_ressourceshumaines_post_mouvement_Personnel_recru_direct'))
urlpatterns.append(url(r'^employe/post_total_recru_overview', views.post_mouvement_Personnel_total_recru, name = 'module_ressourceshumaines_post_mouvement_Personnel_total_recru'))
urlpatterns.append(url(r'^employe/post_interimaire_overview', views.post_mouvement_Personnel_interimaire, name = 'module_ressourceshumaines_post_mouvement_Personnel_interimaire'))


urlpatterns.append(url(r'^employe/(?P<idt>[0-9]+)/evaluation/list', views.get_lister_evaluation, name = 'module_ressourceshumaines_list_evaluation'))
urlpatterns.append(url(r'^employe/(?P<idt>[0-9]+)/evaluation/add', views.get_creer_evaluation, name = 'module_ressourceshumaines_add_evaluation'))
urlpatterns.append(url(r'^evaluation/post_add', views.post_creer_evaluation, name = 'module_ressourceshumaines_post_add_evaluation'))
urlpatterns.append(url(r'^evaluation/item/(?P<idt>[0-9]+)/(?P<ref>[0-9]+)/$', views.get_details_evaluation, name = 'module_ressourceshumaines_detail_evaluation'))
urlpatterns.append(url(r'^evaluation/item/post_update/$', views.post_modifier_evaluation, name = 'module_ressourceshumaines_post_update_evaluation'))
urlpatterns.append(url(r'^evaluation/item/(?P<idt>[0-9]+)/(?P<ref>[0-9]+)/update$', views.get_modifier_evaluation, name = 'module_ressourceshumaines_update_evaluation'))

urlpatterns.append(url(r'^employe/emploi/list', views.get_lister_employe_for_emploi, name = 'module_ressourceshumaines_list_employe_for_emploi'))
urlpatterns.append(url(r'^employe/(?P<idt>[0-9]+)/emploi/list', views.get_lister_emploi, name = 'module_ressourceshumaines_list_emploi'))
urlpatterns.append(url(r'^employe/(?P<idt>[0-9]+)/emploi/add', views.get_creer_emploi, name = 'module_ressourceshumaines_add_emploi'))
urlpatterns.append(url(r'^emploi/post_add', views.post_creer_emploi, name = 'module_ressourceshumaines_post_add_emploi'))

urlpatterns.append(url(r'^emploi/upload/add', views.get_upload_emploi, name='module_ressourceshumaines_get_upload_emploi'))
urlpatterns.append(url(r'^emploi/upload/post_add', views.post_upload_emploi, name='module_ressourceshumaines_post_upload_emploi'))

urlpatterns.append(url(r'^emploi/item/(?P<idt>[0-9]+)/(?P<ref>[0-9]+)/$', views.get_details_emploi, name = 'module_ressourceshumaines_detail_emploi'))
urlpatterns.append(url(r'^emploi/item/post_update/$', views.post_modifier_emploi, name = 'module_ressourceshumaines_post_update_emploi'))
urlpatterns.append(url(r'^emploi/item/(?P<idt>[0-9]+)/(?P<ref>[0-9]+)/update$', views.get_modifier_emploi, name = 'module_ressourceshumaines_update_emploi'))

#RH_MOBILITE
urlpatterns.append(url(r'^mobilite/overview', views.list_more_info_mobility, name = 'module_ressourceshumaines_list_more_info_mobility'))
urlpatterns.append(url(r'^mobilite/list', views.get_lister_mobilite, name = 'module_ressourceshumaines_list_mobilite'))
urlpatterns.append(url(r'^mobilite/add', views.get_creer_mobilite, name = 'module_ressourceshumaines_add_mobilite'))
urlpatterns.append(url(r'^mobilite/post_add', views.post_creer_mobilite, name = 'module_ressourceshumaines_post_add_mobilite'))
urlpatterns.append(url(r'^mobilite/item/(?P<ref>[0-9]+)/$', views.get_details_mobilite, name = 'module_ressourceshumaines_detail_mobilite'))
urlpatterns.append(url(r'^mobilite/item/(?P<ref>[0-9]+)/update$', views.get_modifier_mobilite, name = 'module_ressourceshumaines_update_mobilite'))
urlpatterns.append(url(r'^mobilite/item/post_update/$', views.post_modifier_mobilite, name = 'module_ressourceshumaines_post_update_mobilite'))

urlpatterns.append(url(r'^mobilite/upload/add', views.get_upload_mobilite, name='module_ressourceshumaines_get_upload_mobilite'))
urlpatterns.append(url(r'^mobilite/upload/post_add', views.post_upload_mobilite, name='module_ressourceshumaines_post_upload_mobilite'))


urlpatterns.append(url(r'^formation/list', views.get_lister_formation, name = 'module_ressourceshumaines_list_formation'))
urlpatterns.append(url(r'^formation/add', views.get_creer_formation, name = 'module_ressourceshumaines_add_formation'))
urlpatterns.append(url(r'^formation/post_add', views.post_creer_formation, name = 'module_ressourceshumaines_post_add_formation'))
urlpatterns.append(url(r'^formation/item/(?P<ref>[0-9]+)/$', views.get_details_formation, name = 'module_ressourceshumaines_detail_formation'))
urlpatterns.append(url(r'^formation/item/post_update/$', views.post_modifier_formation, name = 'module_ressourceshumaines_post_update_formation'))
urlpatterns.append(url(r'^formation/item/(?P<ref>[0-9]+)/update$', views.get_modifier_formation, name = 'module_ressourceshumaines_update_formation'))

urlpatterns.append(url(r'^formation/item/cancel(?P<ref>[0-9]+)/$', views.get_cancel_formation, name = 'module_ressourceshumaines_cancel_formation'))

urlpatterns.append(url(r'^formation/item/(?P<ref>[0-9]+)/ligne_formation$', views.get_creer_ligne_formation, name = 'module_ressourceshumaines_add_ligne_formation'))
urlpatterns.append(url(r'^formation/ligne_formation/post_add', views.post_creer_ligne_formation, name = 'module_ressourceshumaines_post_add_ligne_formation'))

urlpatterns.append(url(r'^formation/upload/add', views.get_upload_formation, name='module_ressourceshumaines_get_upload_formation'))
urlpatterns.append(url(r'^formation/upload/post_add', views.post_upload_formation, name='module_ressourceshumaines_post_upload_formation'))

#################
urlpatterns.append(url(r'^evolution/list', views.get_lister_evolution, name = 'module_ressourceshumaines_list_evolution'))
urlpatterns.append(url(r'^evolution/employe/item/(?P<idt>[0-9]+)/$', views.get_lister_evolution_personnelle, name = 'module_ressourceshumaines_list_evolution_employe'))


urlpatterns.append(url(r'^releve/list', views.get_lister_plan_releve, name = 'module_ressourceshumaines_list_plan_releve'))
urlpatterns.append(url(r'^employe/(?P<ref>[0-9]+)/releve/add', views.get_creer_releve, name = 'module_ressourceshumaines_add_plan_releve'))
urlpatterns.append(url(r'^releve/item/(?P<ref>[0-9]+)/$', views.get_details_releve, name = 'module_ressourceshumaines_details_plan_releve'))
urlpatterns.append(url(r'^releve/post_add/$', views.post_creer_releve, name = 'module_ressourceshumaines_post_add_plan_releve'))

urlpatterns.append(url(r'^reconversion/list', views.get_lister_reconversion_professionnelle, name = 'module_ressourceshumaines_list_reconversion_professionnelle'))

#urlpatterns.append(url(r'^evolution/list', views.get_lister_evolution, name = 'module_ressourceshumaines_list_evolution'))

## Projet professionnel
urlpatterns.append(url(r'^projet_professionnel/list', views.get_lister_projet_professionnel, name = 'module_ressourceshumaines_list_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/add', views.get_creer_projet_professionnel, name = 'module_ressourceshumaines_add_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/post_add', views.post_creer_projet_professionnel, name = 'module_ressourceshumaines_post_add_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/item/(?P<ref>[0-9]+)/$', views.get_details_projet_professionnel, name = 'module_ressourceshumaines_detail_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/item/post_update/$', views.post_modifier_projet_professionnel, name = 'module_ressourceshumaines_post_update_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/item/(?P<ref>[0-9]+)/update$', views.get_modifier_projet_professionnel, name = 'module_ressourceshumaines_update_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/employe/list', views.get_lister_projet, name = 'module_ressourceshumaines_list_projet_professionnel_employe'))
urlpatterns.append(url(r'^projet_professionnel/employe/item/(?P<idt>[0-9]+)/$', views.get_lister_projet_employe, name = 'module_ressourceshumaines_list_projet_employe'))

urlpatterns.append(url(r'^projet_professionnel/upload/add', views.get_upload_projet_professionnel, name='module_ressourceshumaines_get_upload_projet_professionnel'))
urlpatterns.append(url(r'^projet_professionnel/upload/post_add', views.post_upload_projet_professionnel, name='module_ressourceshumaines_post_upload_projet_professionnel'))

##Recrutement
urlpatterns.append(url(r'^recrutement_interne/list', views.get_lister_recrutement_interne, name = 'module_ressourceshumaines_list_recrutement_interne'))
urlpatterns.append(url(r'^recrutement_interne/add', views.get_creer_recrutement_interne, name = 'module_ressourceshumaines_add_recrutement_interne'))
urlpatterns.append(url(r'^recrutement_interne/post_add', views.post_creer_recrutement_interne, name = 'module_ressourceshumaines_post_add_recrutement_interne'))
urlpatterns.append(url(r'^recrutement_interne/item/(?P<ref>[0-9]+)/$', views.get_details_recrutement_interne, name = 'module_ressourceshumaines_detail_recrutement_interne'))
urlpatterns.append(url(r'^recrutement_interne/item/(?P<ref>[0-9]+)/update$', views.get_modifier_recrutement_interne, name = 'module_ressourceshumaines_update_recrutement_interne'))
urlpatterns.append(url(r'^recrutement_interne/item/post_update/$', views.post_modifier_recrutement_interne, name = 'module_ressourceshumaines_post_update_recrutement_interne'))

urlpatterns.append(url(r'^recrutement_interne/upload/add', views.get_upload_recrutement_interne, name='module_ressourceshumaines_get_upload_recrutement_interne'))
urlpatterns.append(url(r'^recrutement_interne/upload/post_add', views.post_upload_recrutement_interne, name='module_ressourceshumaines_post_upload_recrutement_interne'))

#Requetes
urlpatterns.append(url(r'^requete/list', views.get_lister_requete, name = 'module_ressourceshumaines_list_requete'))
urlpatterns.append(url(r'^requete/employe/list/$', views.get_lister_requete_by_user, name = 'module_ressourceshumaines_list_requete_employe'))
urlpatterns.append(url(r'^requete/add', views.get_creer_requete, name = 'module_ressourceshumaines_add_requete'))
urlpatterns.append(url(r'^requete/post_add', views.post_creer_requete, name = 'module_ressourceshumaines_post_add_requete'))
urlpatterns.append(url(r'^requete/item/(?P<ref>[0-9]+)/$', views.get_details_requete, name = 'module_ressourceshumaines_detail_requete'))
urlpatterns.append(url(r'^requete/item/post_update/$', views.post_modifier_requete, name = 'module_ressourceshumaines_post_update_requete'))
urlpatterns.append(url(r'^requete/item/(?P<ref>[0-9]+)/update$', views.get_modifier_requete, name = 'module_ressourceshumaines_update_requete'))

#Ordre de mission

urlpatterns.append(url(r'^ordre_de_mission/list', views.get_lister_ordre_de_mission, name = 'module_ressourceshumaines_list_ordre_de_mission'))
urlpatterns.append(url(r'^ordre_de_mission/employe/list/$', views.get_lister_ordre_by_user, name = 'module_ressourceshumaines_list_ordre_de_mission_employe'))
urlpatterns.append(url(r'^ordre_de_mission/add', views.get_creer_ordre_de_mission, name = 'module_ressourceshumaines_add_ordre_de_mission'))
urlpatterns.append(url(r'^ordre_de_mission/post_add', views.post_creer_ordre_de_mission, name = 'module_ressourceshumaines_post_add_ordre_de_mission'))
urlpatterns.append(url(r'^ordre_de_mission/item/(?P<ref>[0-9]+)/$', views.get_details_ordre_de_mission, name = 'module_ressourceshumaines_detail_ordre_de_mission'))
urlpatterns.append(url(r'^ordre_de_mission/item/post_update/$', views.post_modifier_ordre_de_mission, name = 'module_ressourceshumaines_post_update_ordre_de_mission'))
urlpatterns.append(url(r'^ordre_de_mission/item/(?P<ref>[0-9]+)/update$', views.get_modifier_ordre_de_mission, name = 'module_ressourceshumaines_update_ordre_de_mission'))
urlpatterns.append(url(r'^ordre_de_mission/print/', views.get_print_ordre_mission, name='module_ressourceshumaines_print_ordre_de_mission'))

######## RAPPORT #######

urlpatterns.append(url(r'^suivi_carriere/list', views.get_lister_employe_suivi_carriere, name='module_ressourceshumaines_list_suivi_carriere_employe'))
urlpatterns.append(url(r'^suivi_carriere/item/(?P<ref>[0-9]+)/$', views.get_suivi_carriere_employe, name='module_ressourceshumaines_item_suivi_carriere_employe'))
#RH_Overview Rapport
urlpatterns.append(url(r'^rapport/overview', views. get_overview_rapport, name = 'module_ressourceshumaines_get_overview_rapport'))

# get_suivi_carriere_employe

urlpatterns.append(url(r'^requete_competence/list', views.get_lister_requete_competence, name = 'module_ressourceshumaines_list_requete_competence'))
urlpatterns.append(url(r'^requete_competence/add', views.get_creer_requete_competence, name = 'module_ressourceshumaines_add_requete_competence'))
urlpatterns.append(url(r'^requete_competence/post_add', views.post_creer_requete_competence, name = 'module_ressourceshumaines_post_add_requete_competence'))
urlpatterns.append(url(r'^requete_competence/item/(?P<ref>[0-9]+)/$', views.get_details_requete_competence, name = 'module_ressourceshumaines_detail_requete_competence'))
urlpatterns.append(url(r'^requete_competence/item/post_update/$', views.post_modifier_requete_competence, name = 'module_ressourceshumaines_post_update_requete_competence'))
urlpatterns.append(url(r'^requete_competence/item/(?P<ref>[0-9]+)/update$', views.get_modifier_requete_competence, name = 'module_ressourceshumaines_update_requete_competence'))

# reporting
urlpatterns.append(url(r'^dossier_social/reporting/(?P<ref>[0-9]+)/$', views.get_print_rapport_dossier_social, name='module_ressources_humaines_reporting_dossier_social'))
urlpatterns.append(url(r'^suivi_carriere/reporting/(?P<ref>[0-9]+)/$', views.get_print_rapport_suivi_carriere_employe, name='module_ressourceshumaines_reporting_item_suivi_carriere_employe'))

# TYPE UNITE FONCTIONNELLE URLS
urlpatterns.append(url(r'^type_unite_fonctionnelle/list', views.get_lister_type_unite_fonctionnelle, name = 'module_ressourceshumaines_list_type_unite_fonctionnelle'))
urlpatterns.append(url(r'^type_unite_fonctionnelle/add', views.get_creer_type_unite_fonctionnelle, name = 'module_ressourceshumaines_add_type_unite_fonctionnelle'))
urlpatterns.append(url(r'^type_unite_fonctionnelle/item/(?P<ref>[0-9]+)/$', views.get_details_type_unite_fonctionnelle, name = 'module_ressourceshumaines_detail_type_unite_fonctionnelle'))
urlpatterns.append(url(r'^type_unite_fonctionnelle/post_add', views.post_creer_type_unite_fonctionnelle, name = 'module_ressourceshumaines_post_add_type_unite_fonctionnelle'))
urlpatterns.append(url(r'^type_unite_fonctionnelle/item/(?P<ref>[0-9]+)/update$', views.get_modifier_type_unite_fonctionnelle, name = 'module_ressourceshumaines_update_type_unite_fonctionnelle'))
urlpatterns.append(url(r'^type_unite_fonctionnelle/post_update', views.post_modifier_type_unite_fonctionnelle, name = 'module_ressourceshumaines_post_update_type_unite_fonctionnelle'))

# Categorie
urlpatterns.append(url(r'^CategorieDesignation/get/add', views.get_creer_Categorie, name='module_ressources_humaines_add_CategorieDesignation'))
urlpatterns.append(url(r'^CategorieDesignation/liste', views.get_lister_CategorieDesignation, name='module_ressources_humaines_liste_CategorieDesignation'))
urlpatterns.append(url(r'^CategorieDesignation/item/(?P<ref>[0-9]+)/$', views.get_details_Categorie, name = 'module_ressources_humaines_detail_CategorieDesignation'))
urlpatterns.append(url(r'^CategorieDesignation/post/add', views.post_add_CategorieDesignation, name='module_ressources_humaines_post_CategorieDesignation'))
urlpatterns.append(url(r'^CategorieDesignation/item/(?P<ref>[0-9]+)/update$', views.get_update_Categorie, name = 'module_ressources_humaines_get_CategorieDesignation'))
urlpatterns.append(url(r'^CategorieDesignation/post/update', views.post_update_CategorieDesignation, name='module_ressources_humaines_post_update_CategorieDesignation'))

#
urlpatterns.append(url(r'^EchelonDesignation/get/add', views.get_creer_Echelon, name='module_ressources_humaines_add_EchelonDesignation'))
urlpatterns.append(url(r'^EchelonDesignation/liste', views.get_lister_EchelonDesignation, name='module_ressources_humaines_liste_EchelonDesignation'))
urlpatterns.append(url(r'^EchelonDesignation/item/(?P<ref>[0-9]+)/$', views.get_details_Echelon, name = 'module_ressources_humaines_detail_EchelonDesignation'))
urlpatterns.append(url(r'^EchelonDesignation/post/add', views.post_add_EchelonDesignation, name='module_ressources_humaines_post_EchelonDesignation'))
urlpatterns.append(url(r'^EchelonDesignation/item/(?P<ref>[0-9]+)/update$', views.get_update_Echelon, name = 'module_ressources_humaines_get_EchelonDesignation'))
urlpatterns.append(url(r'^EchelonDesignation/post/update', views.post_update_EchelonDesignation, name='module_ressources_humaines_post_update_EchelonDesignation'))

#
urlpatterns.append(url(r'^StatusDesignation/get/add', views.get_creer_StatusDesignation, name='module_ressources_humaines_add_StatutDesignation'))
urlpatterns.append(url(r'^StatusDesignation/liste', views.get_lister_StatusDesignationDesignation, name='module_ressources_humaines_liste_StatutDesignation'))
urlpatterns.append(url(r'^StatusDesignation/item/(?P<ref>[0-9]+)/$', views.get_details_StatusDesignation, name = 'module_ressources_humaines_detail_StatutDesignation'))
urlpatterns.append(url(r'^StatusDesignation/post/add', views.post_add_StatusDesignationDesignation, name='module_ressources_humaines_post_StatutDesignation'))
urlpatterns.append(url(r'^StatusDesignation/item/(?P<ref>[0-9]+)/update$', views.get_update_StatusDesignation, name = 'module_ressources_humaines_get_StatutDesignation'))
urlpatterns.append(url(r'^StatusDesignation/post/update', views.post_update_StatusDesignationDesignation, name='module_ressources_humaines_post_update_StatutDesignation'))

urlpatterns.append(url(r'^departement/vue_exploratoire', views.get_vue_exploratoire, name='module_ressources_humaines_get_vue_exploratoire'))

#LIEU DE TRAVAIL URLS
urlpatterns.append(url(r'^LieuTravail/list', views.get_lister_lieu_travail, name='module_ressources_humaines_list_lieu_travail'))
urlpatterns.append(url(r'^LieuTravail/add', views.get_creer_lieu_travail, name = 'module_ressources_humaines_add_lieu_travail'))
urlpatterns.append(url(r'^LieuTravail/post/add', views.post_creer_lieu_travail, name='module_ressources_humaines_post_lieu_travail'))
urlpatterns.append(url(r'^LieuTravail/item/(?P<ref>[0-9]+)/$', views.get_details_lieu_travail, name = 'module_ressourceshumaines_detail_lieu_travail'))
urlpatterns.append(url(r'^LieuTravail/item/(?P<ref>[0-9]+)/update$', views.get_modifier_lieu_travail, name = 'module_ressources_humaines_get_update_lieu_travail'))
urlpatterns.append(url(r'^LieuTravail/post/update', views.post_modifier_lieu_travail, name='module_ressources_humaines_post_update_lieu_travail'))



#POST Mobilité
urlpatterns.append(url(r'^mobilite_employe/post_add', views.post_creer_mobilite_employe, name = 'module_rh_post_add_mobilite_employe'))

#Rapport
urlpatterns.append(url(r'^Rapporting_employe/create', views.get_generate_rapport_employe, name = 'module_rh_get_generate_rapport_employe'))
urlpatterns.append(url(r'^Rapporting_employe/post/add', views.post_generate_rapport_employe, name='module_rh_post_generate_rapport_employe'))
urlpatterns.append(url(r'^Rapporting_dependant/generate', views.get_generate_rapport_dependant, name = 'module_rh_get_generate_rapport_dependante'))

