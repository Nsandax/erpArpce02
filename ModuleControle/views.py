# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
from datetime import time, timedelta, datetime
import json
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_session import dao_session
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ModuleControle.dao.dao_operationnalisation_module import dao_operationnalisation_module
from django.conf import settings
from ErpBackOffice.utils.print import weasy_print
from ErpBackOffice.models import Model_Facture
from ModuleComptabilite.views import post_traiter_journal, post_traiter_grand_livre, post_traiter_balance_generale, post_traiter_balance_tiers, post_traiter_balance_agee_client, post_traiter_balance_agee_fournisseur, post_traiter_bilan, post_traiter_resultat, post_traiter_tresorerie, post_traiter_annexe
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModuleComptabilite.dao.dao_type_journal import dao_type_journal
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleComptabilite.dao.dao_compte import dao_compte
from ModuleVente.dao.dao_client import dao_client
from ModuleComptabilite.dao.dao_type_compte import dao_type_compte
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ErpBackOffice.utils.endpoint import endpoint
from ModuleControle.dao.dao_centre_cout import dao_centre_cout
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.utils.pagination import pagination
from ModuleControle.dao.dao_groupeanalytique import dao_groupeanalytique
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire
from ModuleComptabilite.dao.dao_ecriture_analytique import dao_ecriture_analytique
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ModuleVente.dao.dao_recouvrement import dao_recouvrement
from ModuleVente.dao.dao_relance_recouvrement import dao_relance_recouvrement
from ModuleVente.dao.dao_client import dao_client
from ModuleVente.dao.dao_etat_facturation import dao_etat_facturation
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_conge import dao_conge
from ModuleRessourcesHumaines.dao.dao_formation import dao_formation
from ModuleRessourcesHumaines.dao.dao_ordre_de_mission import dao_ordre_de_mission
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur

#LOGGING
import logging, inspect
monLog = logging.getLogger("logger")
module= "ModuleControle"
var_module_id = 20


def get_index(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(20, request)
	module_name = "MODULE_CONTROL"
	if response != None:
		return response

	#utilisateurs connectés
	users_connected = sorted(dao_utilisateur.toListUtilisateur()[:3], key=lambda t: t.is_connected, reverse=True) #Filtrage des resultats sur une clé property
	#notifications
	notifications = dao_notification.toListNotification()[:5]

	employes=dao_employe.toListnombreEmployéParMoisAnneeEncours()
	year_employe=dao_employe.toListEmployes_years()
	#fin traitement des données
	##############################################
	# Nombre de bon de commande
	NbreCommande=dao_bon_reception.toGetBonReceptionCount()
	# Nombre de recouvrement
	NbreRecouvrement=dao_recouvrement.togetNombreRecouvrement()
	#Nombre de relance
	NbreRelance=dao_relance_recouvrement.togetNombreRelanceRecouvrement()
	#NombreClient
	NbreClientClient = dao_client.toListClientsActifs().count()
	#Nombre des états de facturations
	Nbrefacturation=dao_etat_facturation.togetNombreEtatFacturation()
	#Nombre d'employés
	Nbremployes=dao_employe.togetNombreEmployesActifs()
	#Nombre d'unité fonctionnel
	NbrUniteFonction=dao_unite_fonctionnelle.togetNombreUniteFonctionnelle()
	#Nombre de congés approuvé
	NbrCongeaprouve = dao_conge.toListCongeApprouve().count()
	#Nombre de formation effectué
	NbrFromationeffectuer= dao_formation.toListFormationByStatus("success").count()
	#Nombre d'ordre de mission
	NbrOrdreMission=dao_ordre_de_mission.toListOrdre_de_mission().count()
	#Liste de derniers connectés
	rencteConnected=dao_utilisateur.toListnombreEmployéConnecteRecement()

	context = {
			"title" : "Module de controle de Gestion",
			"utilisateur" : utilisateur,
			"users_connected":users_connected,
			"notifications": notifications,
			"sous_modules": sous_modules,
			"employes":employes,
			"Nbremployes":Nbremployes,
			'actions':auth.toGetActions(modules,utilisateur),
			"modules" : modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_CONTROLE,
			"menu" : 1,
			"module_name":module_name,
			"year_employe":year_employe,
			"NbreCommande":NbreCommande,
			"NbreRecouvrement":NbreRecouvrement,
			"NbreRelance":NbreRelance,
			"NbreClientClient":NbreClientClient,
			"Nbrefacturation":Nbrefacturation,
			"NbrUniteFonction":NbrUniteFonction,
			"NbrCongeaprouve":NbrCongeaprouve,
			"NbrFromationeffectuer":NbrFromationeffectuer,
			"NbrOrdreMission":NbrOrdreMission,
			"rencteConnected":rencteConnected
			}
	template = loader.get_template("ErpProject/ModuleControle/index.html")
	return HttpResponse(template.render(context, request))

# Ajax envois des expression des besois
def get_employes_annee_to_dashbord(request):
    #print('Touched ajax Quantite')
    try:
        mYear = request.GET['year']
        data=[]
        employeByMonth = dao_employe.toListnombreEmployéParMoisAnneeEncours(mYear)
        data = [employeByMonth]

        #print('les doc et dos %s' % (data))

        return JsonResponse(data, safe=False)
    except Exception as e:
        #print("probleme get_inventer_to_dashbord %s"%(e))
        return JsonResponse([], safe=False)

def get_cubeviewer(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(20, request)
	if response != None:
		return response
	context = {
			"title" : "Exploration",
			"utilisateur" : utilisateur,
			"sous_modules": sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"modules" : modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_CONTROLE,
			"menu" : 1,
			"cubesviewer_cubes_url":settings.CUBESVIEWER_CUBES_URL,
			"cubesviewer_backend_url":settings.CUBESVIEWER_BACKEND_URL
			}

	template = loader.get_template("ErpProject/ModuleControle/cube/index.html")
	return HttpResponse(template.render(context, request))

def get_show_module(request):
	permission_number = 500
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response
	model = dao_module.toListModulesInstalles()
	context ={'title' : 'Liste des modules','model' : model,"sous_modules": sous_modules,'utilisateur' : utilisateur,'organisation': dao_organisation.toGetMainOrganisation(),'modules' : modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleControle/operationnalisation_module/show.html')
	return HttpResponse(template.render(context, request))


def get_lister_operationnalisation_module(request, ref):
	permission_number = 500
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response

	# model = dao_centre_cout.toListCentre_cout()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_operationnalisation_module.toGetOperationnalisationModuleOf(ref), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	my_module = dao_module.toGetModule(ref)

	context ={'title' : 'Module %s : Liste des opérations' % my_module.nom_module, 'view':view, 'my_module':my_module,'organisation': dao_organisation.toGetMainOrganisation(), 'model' : model,'utilisateur' : utilisateur,"sous_modules": sous_modules,'modules' : modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleControle/operationnalisation_module/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_operationnalisation_module(request,ref):
	permission_number = 499
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response

	my_module = dao_module.toGetModule(ref)
	context ={'title' : 'Module %s : Ajout d\'une période' % my_module.nom_module,'my_module':my_module, 'organisation': dao_organisation.toGetMainOrganisation(),'utilisateur' : utilisateur,"sous_modules": sous_modules,'modules' : modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleControle/operationnalisation_module/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_operationnalisation_module(request):
	module_id = request.POST['module_id']
	try:
		designation = request.POST['designation']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		est_active = False #request.POST['est_active']
		est_cloture = False #request.POST['est_cloture']
		observation = request.POST['observation']

		auteur = identite.utilisateur(request)

		operationnalisation_module=dao_operationnalisation_module.toCreateOperationnalisation_module(designation,date_debut,date_fin,est_active,est_cloture,observation,module_id)
		operationnalisation_module=dao_operationnalisation_module.toSaveOperationnalisation_module(auteur, operationnalisation_module)
		return HttpResponseRedirect(reverse('module_controle_list_operationnalisation_module', args=(module_id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER OPERATIONNALISATION_MODULE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_add_operationnalisation_module', args=(module_id,)))


def get_details_operationnalisation_module(request,ref):
	permission_number = 500
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response
	ref=int(ref)
	try:
		model=dao_operationnalisation_module.toGetOperationnalisation_module(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)


		template = loader.get_template('ErpProject/ModuleControle/operationnalisation_module/item.html')
		context ={'title' : 'Détails sur %s' % model.designation ,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'organisation': dao_organisation.toGetMainOrganisation(),'model' : model,'utilisateur' : utilisateur,"sous_modules": sous_modules,'modules' : modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		print('**Erreut Get Detail Module Control')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS OPERATIONNALISATION_MODULE \n {}'.format(auteur.nom_complet, module,e))
		print(e)
		return HttpResponseRedirect(reverse('module_controle_list_operationnalisation_module', args=(ref,)))
def get_modifier_operationnalisation_module(request,ref):
	permission_number = 501
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response

	ref = int(ref)
	model = dao_operationnalisation_module.toGetOperationnalisation_module(ref)
	context ={'title' : 'Modifier Operationnalisation_module','organisation': dao_organisation.toGetMainOrganisation(),'model':model, 'utilisateur': utilisateur,'modules' : modules,"sous_modules": sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleControle/operationnalisation_module/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_operationnalisation_module(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		date_debut = request.POST['date_debut']
		date_fin = request.POST['date_fin']
		est_active = request.POST['est_active']
		est_cloture = request.POST['est_cloture']
		observation = request.POST['observation']
		module_id = request.POST['module_id']
		auteur = identite.utilisateur(request)

		operationnalisation_module=dao_operationnalisation_module.toCreateOperationnalisation_module(designation,date_debut,date_fin,est_active,est_cloture,observation,module_id)
		operationnalisation_module=dao_operationnalisation_module.toUpdateOperationnalisation_module(id, operationnalisation_module)
		return HttpResponseRedirect(reverse('module_controle_list_operationnalisation_module'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER OPERATIONNALISATION_MODULE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_add_operationnalisation_module'))


def post_status_operationnalisation_module(request):

	id = int(request.POST['ref'])
	try:
		status = int(request.POST['status'])

		is_update=dao_operationnalisation_module.toSetStatusOperationnalisation(id, status)
		if is_update:
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
		return HttpResponseRedirect(reverse('module_controle_detail_operationnalisation_module', args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST STATUS OPERATIONNALISATION_MODULE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_detail_operationnalisation_module', args=(id,)))

#CENTRE DE COUT
def get_lister_centre_cout(request):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 504
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_centre_cout.toListCentre_cout()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_centre_cout.toListCentre_cout(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	context ={'title' : 'Liste de centre des coûts','model' : model,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleControle/centre_cout/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_centre_cout(request):
	# droit='CREER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 503
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	centre_cout = dao_centre_cout.toListCentreCoutOfTypeView()
	groupes = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Ajouter un centre de coût','centre_cout':centre_cout, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'groupes':groupes,
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleControle/centre_cout/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_centre_cout(request):

	try:
		designation = request.POST['designation']
		code = request.POST['code']
		centre_cout_id = request.POST['centre_cout_id']
		abbreviation = request.POST['abbreviation']
		type_centre = request.POST['type_centre']
		groupe_analytique_id = request.POST['groupe_analytique_id']

		groupe_analytique = dao_groupeanalytique.toGetGroupeanalytique(groupe_analytique_id)
		date_debut = None
		date_fin = None

		if groupe_analytique.est_projet:
			date_debut = request.POST["date_debut"]
			date_debut = date_debut[6:10] + '-' + date_debut[3:5] + '-' + date_debut[0:2]
			date_debut = datetime.datetime.strptime(date_debut, "%Y-%m-%d").date()

			date_fin = request.POST["date_fin"]
			date_fin = date_fin[6:10] + '-' + date_fin[3:5] + '-' + date_fin[0:2]
			date_fin = datetime.datetime.strptime(date_fin, "%Y-%m-%d").date()


		if centre_cout_id == "":
			centre_cout_id = None
		auteur = identite.utilisateur(request)

		centre_cout=dao_centre_cout.toCreateCentre_cout(designation,code,type_centre,abbreviation,centre_cout_id, groupe_analytique_id)
		centre_cout=dao_centre_cout.toSaveCentre_cout(auteur, centre_cout)
		centre_cout.date_debut = date_debut
		centre_cout.date_fin = date_fin
		centre_cout.save()
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_controle_detail_centre_cout', args=(centre_cout.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_add_centre_cout'))


def get_details_centre_cout(request,ref):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 504
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		centre_cout=dao_centre_cout.toGetCentre_cout(ref)
		if centre_cout.typeCentre == 1:
			lignes = dao_centre_cout.toListLigneOfCentreTypeView(centre_cout.id)
		else:
			lignes = dao_centre_cout.toListLigneOfCentreTypeAccount(centre_cout.id)

		#print('lignes', lignes)

		montant_alloue = 0
		montant_consomme = 0

		for ligne in lignes:
			montant_alloue += ligne.montant_alloue
			montant_consomme += float(ligne.valeur_total_consommee)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,centre_cout)


		template = loader.get_template('ErpProject/ModuleControle/centre_cout/item.html')
		context ={'title' : centre_cout.designation + ' : Détails','centre_cout' : centre_cout,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'montant_alloue':montant_alloue,
		'montant_consomme':montant_consomme,
		'ligne_budgetaire':lignes,
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_list_centre_cout'))
def get_modifier_centre_cout(request,ref):
	# droit='MODIFIER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 505
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_centre_cout.toGetCentre_cout(ref)
	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	centre_cout = dao_centre_cout.toListCentre_cout()
	context ={'title' : 'Modifier le centre de coût','model':model, 'utilisateur': utilisateur,
	'groupe_analytique':groupe_analytique,
	'centre_cout':centre_cout,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleControle/centre_cout/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_centre_cout(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		code = request.POST['code']
		centre_cout_id = request.POST['centre_cout_id']
		abbreviation = request.POST['abbreviation']
		type_centre = request.POST['type_centre_cout']
		groupe_analytique_id = request.POST['groupe_analytique_id']

		auteur = identite.utilisateur(request)

		centre_cout=dao_centre_cout.toCreateCentre_cout(designation,code,type_centre, abbreviation,centre_cout_id, groupe_analytique_id)
		centre_cout=dao_centre_cout.toUpdateCentre_cout(id, centre_cout)
		return HttpResponseRedirect(reverse('module_controle_list_centre_cout'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_add_centre_cout'))

# GROUPE ANALYTIQUE
def get_lister_groupeanalytique(request):
	# droit='LISTER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 509
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_groupeanalytique.toListGroupeanalytique()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_groupeanalytique.toListGroupeanalytique(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	context ={'title' : 'Liste des groupes analytiques','model' : model,
	'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleControle/groupeanalytique/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_groupeanalytique(request):
	# droit='CREER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 507
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Ajouter un groupe analytique','utilisateur' : utilisateur,
	'groupe_analytique':groupe_analytique,
	'isPopup': True if 'isPopup' in request.GET else False,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleControle/groupeanalytique/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_groupeanalytique(request):

	try:
		designation = request.POST['designation']
		description = request.POST['description']
		groupe_analytique_id = request.POST['groupe_analytique_id']
		if groupe_analytique_id == '':
			groupe_analytique_id = None

		est_projet = False
		if "est_projet" in request.POST : est_projet = True

		auteur = identite.utilisateur(request)

		isPopup = request.POST["isPopup"]

		groupeanalytique=dao_groupeanalytique.toCreateGroupeanalytique(designation,description,groupe_analytique_id, est_projet)
		groupeanalytique=dao_groupeanalytique.toSaveGroupeanalytique(auteur, groupeanalytique)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_controle_detail_groupeanalytique', args=(groupeanalytique.id,))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_add_groupeanalytique'))


def get_details_groupeanalytique(request,ref):
	# droit='LISTER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 509
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		groupeanalytique=dao_groupeanalytique.toGetGroupeanalytique(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,groupeanalytique)

		template = loader.get_template('ErpProject/ModuleControle/groupeanalytique/item.html')
		context ={'title' : 'Details sur un groupe analytique','groupeanalytique' : groupeanalytique,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_list_groupeanalytique'))

def get_modifier_groupeanalytique(request,ref):
	# droit='MODIFIER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 510
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_groupeanalytique.toGetGroupeanalytique(ref)
	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Modifier un groupe analytique','model':model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'groupe_analytique':groupe_analytique,
	'utilisateur': utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleControle/groupeanalytique/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_groupeanalytique(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		groupe_analytique_id = request.POST['groupe_analytique_id']
		auteur = identite.utilisateur(request)

		if groupe_analytique_id == '':
			groupe_analytique_id = None

		est_projet = False
		if "est_projet" in request.POST : est_projet = True

		groupeanalytique=dao_groupeanalytique.toCreateGroupeanalytique(designation,description,groupe_analytique_id, est_projet)
		groupeanalytique=dao_groupeanalytique.toUpdateGroupeanalytique(id, groupeanalytique)
		return HttpResponseRedirect(reverse('module_controle_list_groupeanalytique'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_add_groupeanalytique'))

def get_details_ecriture_analytique_of_centre_cout(request, ref):
	try:
		# droit="LISTER_CENTRE_COUT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 504
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return None

		ref = int(ref)
		centre_cout = dao_centre_cout.toGetCentre_cout(ref)
		exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		devise = dao_devise.toGetDeviseReference()
		if exercice:
			if centre_cout.typeCentre == 1:
				#Allez recuperer les sous centre des cout d'un centre de cout
				lignes = dao_centre_cout.toListLigneOfCentreTypeView(centre_cout.id)
				ecritures_analytiques = dao_centre_cout.toListEcritureAnalytiqueOfCentreTypeView(ref, exercice.date_debut, exercice.date_fin)
			else:
				lignes = dao_centre_cout.toListLigneOfCentreTypeAccount(centre_cout.id)
				ecritures_analytiques = dao_ecriture_analytique.toListEcritureAnalytiqueOfCentreCout(ref, exercice.date_debut, exercice.date_fin)
		else:
			messages.add_message(request, messages.ERROR, "Aucun exercice budgétaire actif")
			return HttpResponseRedirect(reverse('module_controle_list_centre_cout'))


		#print('lignes', lignes)

		montant_alloue = 0
		montant_consomme = 0
		charge = 0
		produit = 0

		for ligne in lignes:
			#Montant alloué via les lignes budgétaires
			montant_alloue += ligne.montant_alloue
		for ecriture in ecritures_analytiques:
			#Montant consommé via les écritures
			montant_consomme += ecriture.montant
			if ecriture.montant >= 0:
				produit += ecriture.montant
			else:
				charge += ecriture.montant


		#print("lslssl")

		balance = montant_alloue + produit + charge
		if montant_alloue > 0:
			pourcentage = 100 * makeFloat(montant_consomme) / makeFloat(montant_alloue)
		else:
			pourcentage = 0
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,centre_cout)

		context ={
		'title' : 'Ecritures analytiques du centre de coût',
		'centre_cout':centre_cout,
		'utilisateur' : utilisateur,
		'reel': montant_consomme,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'charge': abs(charge),
		'produit': produit,
		'montant_alloue': montant_alloue,
		'pourcentage' : pourcentage,
		'balance': balance,
		'devise': devise,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'ecritures_analytiques':ecritures_analytiques,
		'module' : ErpModule.MODULE_CONTROLE,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleControle/centre_cout/ecriture_analytique/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleControle'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR DETAILLER Ecriture")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_controle_list_centre_cout'))




#ACTIVITE
def get_lister_activity(request):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 522
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_centre_cout.toListCentre_cout()
	#*******Filtre sur les règles **********#
	model = sorted(dao_utilisateur.toListUtilisateur(), key=lambda t: t.is_connected, reverse=True) #Filtrage des resultats sur une clé property
	model = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#


	context ={'title' : 'Liste des utilisateurs', 'model': model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleControle/activity/list.html')
	return HttpResponse(template.render(context, request))

def get_details_activity(request,ref):
	permission_number = 522
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		model = dao_utilisateur.toGetUtilisateur(ref)
		sessions = dao_utilisateur.toListSessionOfUtilisateur(model.user_id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)


		context ={
			'title' : model.nom_complet,
			'model':model,
			'sessions': sessions,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTROLE,'menu' : 4}

		template = loader.get_template('ErpProject/ModuleControle/activity/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_controle_list_activity'))










# JOURNAUX OUTPUT PDF VIEWS
def get_generer_journal(request):

	# droit="GENERER_JOURNAL"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 512
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer un journal',
		"journaux" : dao_journal.toListJournaux(),
		"devises" : dao_devise.toListDevisesActives(),
		"types_journal" : dao_type_journal.toListTypesJournal(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 5
	}
	template = loader.get_template("ErpProject/ModuleControle/journal/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_journal(request):
	try:
		#Authentification
		# droit="GENERER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 512
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_journal(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		template = loader.get_template("ErpProject/ModuleControle/journal/generated.html")
		docHtml = template.render(context)
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_journal"))

def post_imprimer_journal(request):
	try:
		#Authentification
		# droit="IMPRIMER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 512
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_journal(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/journal.html", "journal.pdf", context)

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_journal"))


# GRANDS LIVRES OUTPUT PDF
def get_generer_grand_livre(request):

	# droit="GENERER_GRANDLIVRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 513
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer un grand-livre',
		"comptes" : dao_compte.toListComptes(),
		"devises" : dao_devise.toListDevisesActives(),
		"types_compte" : dao_type_compte.toListTypesCompte(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 6
	}
	template = loader.get_template("ErpProject/ModuleControle/livre/generate.html")
	return HttpResponse(template.render(context, request))

def post_generer_grand_livre(request):
	try:
		# droit="GENERER_GRANDLIVRE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 513
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_grand_livre(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)

		template = loader.get_template("ErpProject/ModuleControle/livre/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_grand_livre"))

def post_imprimer_grand_livre(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 513
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_grand_livre(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/grand_livre.html", "grand_livre.pdf", context)


	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_grand_livre"))



# BALANCE GENERALE OUTPUT PDF
def get_generer_balance_generale(request):

	# droit="GENERER_BALANCE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 514
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer la balance générale',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModuleControle/balance/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_balance_generale(request):
	try:
		# droit="GENERER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 514
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_generale(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)


		template = loader.get_template("ErpProject/ModuleControle/balance/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_generale"))

def post_imprimer_balance_generale(request):
	try:
		# droit="IMPRIMER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 514
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = post_traiter_balance_generale(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/balance.html", "balance.pdf", context)

	except Exception as e:
		#print("ERREUR print BALANCE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_generale"))



# BALANCE DES TIERS
def get_generer_balance_tiers(request):

	# droit="GENERER_BALANCE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 519
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer la balance des tiers',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModuleControle/balance_tiers/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_balance_tiers(request):
	try:
		# droit="GENERER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 519
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_tiers(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)

		template = loader.get_template("ErpProject/ModuleControle/balance_tiers/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_tiers"))

def post_imprimer_balance_tiers(request):
	try:
		# droit="IMPRIMER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 519
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_tiers(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/balance_tiers.html", "balance_tiers.pdf", context)

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_tiers"))


# BALANCE AGEE
def get_generer_balance_agee_client(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 520
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		type_date = request.GET.get("type_date","")

		if type_date == "1":
			#Aujourd'hui
			date_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
		elif type_date == "2":
			#Fin du mois dernier
			today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			first_day = today.replace(day=1)
			date_fin = first_day - timedelta(days=1)
		elif type_date == "3":
			#Fin du dernier trimestre
			date_today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			first_day = date_today.replace(day=1)
			date_last_month = first_day - timedelta(days=1)
			date_segond = date_last_month.replace(day=1) - timedelta(days=1)
			date_fin = date_segond.replace(day=1) - timedelta(days=1)
		elif type_date == "4":
			#Fin de la dernière periode #TODO récupérer la date fin de la dernière année fiscale
			date_today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			first_day_year = date_today.replace(day=1, month=1)
			date_fin = first_day_year - timedelta(days=1)
		else:
			# si non précisé prendre #Aujourd'hui
			date_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			type_date = "1"


		devise = dao_devise.toGetDeviseReference()

		#On declare les tableaux et variable qui seront renvoyés en output
		clients = []
		factures = []

		list_clients = dao_client.toListClientsActifs()
		for client in list_clients:
			factures_clients = Model_Facture.objects.filter(type = "CLIENT", client_id = client.id, est_soldee = False, date_facturation__lte = date_fin).order_by("-date_facturation")
			nbr_fac = factures_clients.count()
			#print("nbr_fac: {}".format(nbr_fac))
			if nbr_fac == 0: continue # le client n'a pas de facture non soldée
			#On initialise le variable des totaux
			client_montant_au_jour = 0.0
			client_montant_1_30 = 0.0
			client_montant_31_60 = 0.0
			client_montant_61_90 = 0.0
			client_montant_91_plus = 0.0

			for facture in factures_clients:
				#Pour chaque facture non soldée, on rajoute le montant dû dans chaque periode
				#Pour la periode (Encours)
				if facture.date_echeance >= date_fin:
					facture.montant_au_jour = facture.montant
					client_montant_au_jour = float(client_montant_au_jour) + float(facture.montant)
				else: facture.montant_au_jour = 0.0

				#Pour la periode (1 - 30 jours échu)
				# end_date : Ici c'est le jour d'avant le jour en cours
				end_date = (date_fin + timedelta(days=-1))
				start_date = (end_date + timedelta(days=-30))
				#On prend toute la journée de ce jour
				allday_start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
				#print("De {} a {}".format(allday_start_date.strftime("%d/%m/%Y %H:%M"), end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance >= allday_start_date and facture.date_echeance <= end_date :
					facture.montant_1_30 = facture.montant
					client_montant_1_30 = float(client_montant_1_30) + float(facture.montant)
				else: facture.montant_1_30 = 0.0

				#Pour la periode (31 - 60 jours échu)
				# end_date : Ici c'est le jour d'avant le 30e jour
				end_date = (start_date + timedelta(days=-1))
				start_date = (end_date + timedelta(days=-30))
				#On prend toute la journée de ce jour
				allday_start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
				#print("De {} a {}".format(allday_start_date.strftime("%d/%m/%Y %H:%M"), end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance >= allday_start_date and facture.date_echeance <= end_date :
					facture.montant_31_60 = facture.montant
					client_montant_31_60 = float(client_montant_31_60) + float(facture.montant)
				else: facture.montant_31_60 = 0.0

				#Pour la periode (61 - 90 jours échu)
				# end_date : Ici c'est le jour d'avant le 60e jour
				end_date = (start_date + timedelta(days=-1))
				start_date = (end_date + timedelta(days=-30))
				#On prend toute la journée de ce jour
				allday_start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
				#print("De {} a {}".format(allday_start_date.strftime("%d/%m/%Y %H:%M"), end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance >= allday_start_date and facture.date_echeance <= end_date :
					facture.montant_61_90 = facture.montant
					client_montant_61_90 = float(client_montant_61_90) + float(facture.montant)
				else: facture.montant_61_90 = 0.0

				#Pour la periode (plus de 90 jours échu)
				# end_date : Ici c'est le jour d'avant le 90e jour
				end_date = (start_date + timedelta(days=-1))
				#print("Avant {}".format(end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance <= end_date :
					facture.montant_91_plus = facture.montant
					client_montant_91_plus = float(client_montant_91_plus) + float(facture.montant)
				else: facture.montant_91_plus = 0.0
				factures.append(facture)

			#On affecte les totaux
			client.montant_au_jour = client_montant_au_jour
			client.montant_1_30 = client_montant_1_30
			client.montant_31_60 = client_montant_31_60
			client.montant_61_90 = client_montant_61_90
			client.montant_91_plus = client_montant_91_plus
			clients.append(client)

		#On trie les clients et factures récupérés
		clients = sorted(clients, key=lambda client: client.nom_complet, reverse=False)
		factures = sorted(factures, key=lambda facture: facture.date_facturation, reverse=True)

		#On initialise les totaux de la balance agée
		total_montant_au_jour = 0.0
		total_montant_1_30 = 0.0
		total_montant_31_60 = 0.0
		total_montant_61_90 = 0.0
		total_montant_91_plus = 0.0

		# On récupere les soldes initiaux à partir des écritures d'avant période
		for client in clients:
			total_montant_au_jour = total_montant_au_jour + float(client.montant_au_jour)
			total_montant_1_30 = total_montant_1_30 + float(client.montant_1_30)
			total_montant_31_60 = total_montant_31_60 + float(client.montant_31_60)
			total_montant_61_90 = total_montant_61_90 + float(client.montant_61_90)
			total_montant_91_plus = total_montant_91_plus + float(client.montant_91_plus)

		context = {
			'title' : "Balance agée clients",
			"factures" : factures,
			"clients" : clients,
			"type_date" : type_date,
			'total_montant_au_jour' : "%.2f" % total_montant_au_jour,
			'total_montant_1_30' : "%.2f" % total_montant_1_30,
			'total_montant_31_60' : "%.2f" % total_montant_31_60,
			'total_montant_61_90' : "%.2f" % total_montant_61_90,
			'total_montant_91_plus' : "%.2f" % total_montant_91_plus,
			"date_fin" : date_fin.strftime("%d/%m/%Y"),
			"devise" : devise,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : utilisateur,
   			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_CONTROLE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleControle/balance_agee/client/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_tableau_de_bord"))

def post_generer_balance_agee_client(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 520
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_balance_agee_client(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)

		template = loader.get_template("ErpProject/ModuleControle/balance_agee/client/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST GENERATE BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_agee_client"))


def post_imprimer_balance_agee_client(request):
	try:
		# droit="IMPRIMER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 520
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_agee_client(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/balance_agee_client.html", "balance_agee_client.pdf", context)

	except Exception as e:
		#print("ERREUR print BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_agee_client"))




# BALANCE AGEE FOURNISSEUR
def get_generer_balance_agee_fournisseur(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 521
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		type_date = request.GET.get("type_date","")

		if type_date == "1":
			#Aujourd'hui
			date_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
		elif type_date == "2":
			#Fin du mois dernier
			today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			first_day = today.replace(day=1)
			date_fin = first_day - timedelta(days=1)
		elif type_date == "3":
			#Fin du dernier trimestre
			date_today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			first_day = date_today.replace(day=1)
			date_last_month = first_day - timedelta(days=1)
			date_segond = date_last_month.replace(day=1) - timedelta(days=1)
			date_fin = date_segond.replace(day=1) - timedelta(days=1)
		elif type_date == "4":
			#Fin de la dernière periode #TODO récupérer la date fin de la dernière année fiscale
			date_today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			first_day_year = date_today.replace(day=1, month=1)
			date_fin = first_day_year - timedelta(days=1)
		else:
			# si non précisé prendre #Aujourd'hui
			date_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
			type_date = "1"


		devise = dao_devise.toGetDeviseReference()

		#On declare les tableaux et variable qui seront renvoyés en output
		fournisseurs = []
		factures = []

		list_fournisseurs = dao_fournisseur.toListFournisseursActifs()
		for fournisseur in list_fournisseurs:
			factures_fournisseurs = Model_Facture.objects.filter(type = "FOURNISSEUR", fournisseur_id = fournisseur.id, est_soldee = False, date_facturation__lte = date_fin).order_by("-date_facturation")
			nbr_fac = factures_fournisseurs.count()
			#print("nbr_fac: {}".format(nbr_fac))
			if nbr_fac == 0: continue # le fournisseur n'a pas de facture non soldée
			#On initialise le variable des totaux
			fournisseur_montant_au_jour = 0.0
			fournisseur_montant_1_30 = 0.0
			fournisseur_montant_31_60 = 0.0
			fournisseur_montant_61_90 = 0.0
			fournisseur_montant_91_plus = 0.0

			for facture in factures_fournisseurs:
				#Pour chaque facture non soldée, on rajoute le montant dû dans chaque periode
				#Pour la periode (Encours)
				if facture.date_echeance >= date_fin:
					facture.montant_au_jour = facture.montant
					fournisseur_montant_au_jour = float(fournisseur_montant_au_jour) + float(facture.montant)
				else: facture.montant_au_jour = 0.0

				#Pour la periode (1 - 30 jours échu)
				# end_date : Ici c'est le jour d'avant le jour en cours
				end_date = (date_fin + timedelta(days=-1))
				start_date = (end_date + timedelta(days=-30))
				#On prend toute la journée de ce jour
				allday_start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
				#print("De {} a {}".format(allday_start_date.strftime("%d/%m/%Y %H:%M"), end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance >= allday_start_date and facture.date_echeance <= end_date :
					facture.montant_1_30 = facture.montant
					fournisseur_montant_1_30 = float(fournisseur_montant_1_30) + float(facture.montant)
				else: facture.montant_1_30 = 0.0

				#Pour la periode (31 - 60 jours échu)
				# end_date : Ici c'est le jour d'avant le 30e jour
				end_date = (start_date + timedelta(days=-1))
				start_date = (end_date + timedelta(days=-30))
				#On prend toute la journée de ce jour
				allday_start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
				#print("De {} a {}".format(allday_start_date.strftime("%d/%m/%Y %H:%M"), end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance >= allday_start_date and facture.date_echeance <= end_date :
					facture.montant_31_60 = facture.montant
					fournisseur_montant_31_60 = float(fournisseur_montant_31_60) + float(facture.montant)
				else: facture.montant_31_60 = 0.0

				#Pour la periode (61 - 90 jours échu)
				# end_date : Ici c'est le jour d'avant le 60e jour
				end_date = (start_date + timedelta(days=-1))
				start_date = (end_date + timedelta(days=-30))
				#On prend toute la journée de ce jour
				allday_start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
				#print("De {} a {}".format(allday_start_date.strftime("%d/%m/%Y %H:%M"), end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance >= allday_start_date and facture.date_echeance <= end_date :
					facture.montant_61_90 = facture.montant
					fournisseur_montant_61_90 = float(fournisseur_montant_61_90) + float(facture.montant)
				else: facture.montant_61_90 = 0.0

				#Pour la periode (plus de 90 jours échu)
				# end_date : Ici c'est le jour d'avant le 90e jour
				end_date = (start_date + timedelta(days=-1))
				#print("Avant {}".format(end_date.strftime("%d/%m/%Y %H:%M")))
				if facture.date_echeance <= end_date :
					facture.montant_91_plus = facture.montant
					fournisseur_montant_91_plus = float(fournisseur_montant_91_plus) + float(facture.montant)
				else: facture.montant_91_plus = 0.0
				factures.append(facture)

			#On affecte les totaux
			fournisseur.montant_au_jour = fournisseur_montant_au_jour
			fournisseur.montant_1_30 = fournisseur_montant_1_30
			fournisseur.montant_31_60 = fournisseur_montant_31_60
			fournisseur.montant_61_90 = fournisseur_montant_61_90
			fournisseur.montant_91_plus = fournisseur_montant_91_plus
			fournisseurs.append(fournisseur)

		#On trie les fournisseurs et factures récupérés
		fournisseurs = sorted(fournisseurs, key=lambda fournisseur: fournisseur.nom_complet, reverse=False)
		factures = sorted(factures, key=lambda facture: facture.date_facturation, reverse=True)

		#On initialise les totaux de la balance agée
		total_montant_au_jour = 0.0
		total_montant_1_30 = 0.0
		total_montant_31_60 = 0.0
		total_montant_61_90 = 0.0
		total_montant_91_plus = 0.0

		# On récupere les soldes initiaux à partir des écritures d'avant période
		for fournisseur in fournisseurs:
			total_montant_au_jour = total_montant_au_jour + float(fournisseur.montant_au_jour)
			total_montant_1_30 = total_montant_1_30 + float(fournisseur.montant_1_30)
			total_montant_31_60 = total_montant_31_60 + float(fournisseur.montant_31_60)
			total_montant_61_90 = total_montant_61_90 + float(fournisseur.montant_61_90)
			total_montant_91_plus = total_montant_91_plus + float(fournisseur.montant_91_plus)

		context = {
			'title' : "Balance agée fournisseurs",
			"factures" : factures,
			"fournisseurs" : fournisseurs,
			"type_date" : type_date,
			'total_montant_au_jour' : "%.2f" % total_montant_au_jour,
			'total_montant_1_30' : "%.2f" % total_montant_1_30,
			'total_montant_31_60' : "%.2f" % total_montant_31_60,
			'total_montant_61_90' : "%.2f" % total_montant_61_90,
			'total_montant_91_plus' : "%.2f" % total_montant_91_plus,
			"date_fin" : date_fin.strftime("%d/%m/%Y"),
			"devise" : devise,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : utilisateur,
   			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_CONTROLE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleControle/balance_agee/fournisseur/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_tableau_de_bord"))


def post_generer_balance_agee_fournisseur(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 521
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_agee_fournisseur(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)


		template = loader.get_template("ErpProject/ModuleControle/balance_agee/fournisseur/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST GENERATE BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_agee_fournisseur"))


def post_imprimer_balance_agee_fournisseur(request):
	try:
		# droit="IMPRIMER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 521
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_agee_fournisseur(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/balance_agee_fournisseur.html", "balance_agee_fournisseur.pdf", context)

	except Exception as e:
		#print("ERREUR POST print BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_balance_agee_fournisseur"))


# BILAN OUTPUT PDF
def get_generer_bilan(request):

	# droit="GENERER_BILAN"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 515
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le bilan',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 8
	}
	template = loader.get_template("ErpProject/ModuleControle/bilan/generate.html")
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_generer_bilan(request):
	sid = transaction.savepoint()
	try:
		# droit="GENERER_BILAN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 515
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_bilan(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)

		template = loader.get_template("ErpProject/ModuleControle/bilan/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_bilan"))

def post_imprimer_bilan(request):
	try:
		# droit="IMPRIMER_BILAN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 515
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_bilan(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/bilan.html", "bilan.pdf", context)

	except Exception as e:
		#print("ERREUR print BILAN")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_bilan"))


# RESULTAT OUTPUT PDF
def get_generer_resultat(request):

	# droit="GENERER_COMPTE_RESULTAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 516
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le tableau de résultat',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleControle/resultat/generate.html")
	return HttpResponse(template.render(context, request))

def post_generer_resultat(request):
	try:
		# droit="GENERER_COMPTE_RESULTAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 516
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		#print("post_generer_resultat")
		context = post_traiter_resultat(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)

		template = loader.get_template("ErpProject/ModuleControle/resultat/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_resultat"))

def post_imprimer_resultat(request):
	try:
		# droit="IMPRIMER_COMPTE_RESULTAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 516
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_resultat(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/compte_resultat.html", "compte_resultat.pdf", context)

	except Exception as e:
		#print("ERREUR print COMPTE RESULTAT")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_resultat"))


#  TABLEAU DE FLUX DE TRESORERIE
def get_generer_tresorerie(request):

	# droit="GENERER_FLUX_TRESORERIE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 517
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le tableau des flux de trésorerie',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'actions':auth.toGetActions(modules,utilisateur),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleControle/flux_tresorerie/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_tresorerie(request):
	try:
		# droit="GENERER_FLUX_TRESORERIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 517
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_tresorerie(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)


		template = loader.get_template("ErpProject/ModuleControle/flux_tresorerie/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_tresorerie"))


def post_imprimer_tresorerie(request):
	try:
		# droit="IMPRIMER_FLUX_TRESORERIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 517
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_tresorerie(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)
		return weasy_print("ErpProject/ModuleControle/reporting/flux_tresorerie.html", "flux_tresorerie.pdf", context)
	except Exception as e:
		#print("ERREUR print FLUX TRESORERIE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_tresorerie"))


#  NOTES ANNEXES
def get_generer_annexe(request):

	# droit="GENERER_FLUX_TRESORERIE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 518
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le tableau des flux de trésorerie',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'actions':auth.toGetActions(modules,utilisateur),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_CONTROLE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleControle/annexe/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_annexe(request):
	try:
		# droit="GENERER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 518
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_annexe(request, utilisateur, modules, sous_modules, ErpModule.MODULE_CONTROLE)

		template = loader.get_template("ErpProject/ModuleControle/annexe/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_generer_annexe"))



# ANALYSE BDGT OUTPUT PDF
def get_generer_analyse_budgetaire(request):
	try:
		# droit="CREER_RAPPORT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 527
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		context = {
			'title' : 'Générer une analyse budgetaire',
			"comptes" : dao_compte.toListComptes(),
			"devises" : dao_devise.toListDevisesActives(),
			"types_compte" : dao_type_compte.toListTypesCompte(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'exercices': dao_exercicebudgetaire.toListExercicebudgetaire(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_CONTROLE,
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleControle/rapport/generate.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleControle'
		monLog.error("{} :: {}::\nERREUR LORS DE GENERER analyse budgetaire \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur générer analyse budgetaire ')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_tableau"))

def post_generer_analyse_budgetaire(request):

	try:

		# droit="CREER_RAPPORT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 527
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		date_debut = request.POST["date_debut"]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

		date_fin = request.POST["date_fin"]
		annee_date_fin = int(date_fin[6:10])
		mois_date_fin = int(date_fin[3:5])
		jour_date_fin = int(date_fin[0:2])
		if jour_date_fin == 31:
			if mois_date_fin == 12:
				annee_date_fin = annee_date_fin + 1
				mois_date_fin = 1
				jour_date_fin = 1
			else:
				mois_date_fin = mois_date_fin + 1
				jour_date_fin = 1
		elif jour_date_fin == 28 or jour_date_fin == 29:
			if mois_date_fin == 2:
				mois_date_fin = 3
				jour_date_fin = 1
		else:
				jour_date_fin = jour_date_fin + 1

		date_fin = timezone.datetime(annee_date_fin, mois_date_fin, jour_date_fin).date()

		devise_id = int(request.POST["devise_id"])
		devise = dao_devise.toGetDevise(devise_id)
		devise_ref = dao_devise.toGetDeviseReference()

		comptes = []
		ecritures_comptables = []

		title = ""
		groupe = int(request.POST["groupe"])
		if groupe == 0:
			title = "Grand-Livre de tous les comptes"
			ecritures_comptables = dao_ecriture_comptable.toListEcrituresComptablesInPeriode(date_debut, date_fin)
			for item in ecritures_comptables:
				compte = dao_compte.toGetCompte(item.compte_id)
				if len(comptes) == 0: comptes.append(compte)
				else:
					existe_deja = False
					for compte_added in comptes:
						if compte_added.id == compte.id:
							existe_deja = True
							break
					if existe_deja == False: comptes.append(compte)
		elif groupe == -1:
			title = "Grand-Livre de certains comptes"
			list_compte_id = request.POST.getlist('compte_id', None)

			if len(list_compte_id) == 0:
				messages.add_message(request, messages.ERROR, "Echec: Veuillez sélectionner au moins un compte comme vous voulez avoir le grand-livre de certains comptes.")
				return HttpResponseRedirect(reverse("module_controle_analyse_budgetaire"))

			for i in range(0, len(list_compte_id)) :
				compte_id = int(list_compte_id[i])
				compte = dao_compte.toGetCompte(compte_id)
				comptes.append(compte)
				ecritures_comptables.extend(dao_ecriture_comptable.toListEcrituresComptablesDuCompteInPeriode(compte.id, date_debut, date_fin))
		else:
			type_compte = dao_type_compte.toGetTypeCompte(groupe)
			comptes = dao_compte.toListComptesOf(type_compte.id)
			title = "Grand-Livre des comptes %s" % type_compte.designation
			for compte in comptes:
				ecritures_comptables.extend(dao_ecriture_comptable.toListEcrituresComptablesDuCompteInPeriode(compte.id, date_debut, date_fin))

		comptes = sorted(comptes, key=lambda compte: compte.designation, reverse=False)
		ecritures_comptables = sorted(ecritures_comptables, key=lambda ecriture: ecriture.date_creation, reverse=True)

		equilibre_credit = 0
		equilibre_debit = 0

		for item in ecritures_comptables:
			equilibre_credit = equilibre_credit + makeFloat(item.credit)
			equilibre_debit = equilibre_debit + makeFloat(item.debit)

		context = {
			'title' : title,
			"comptes" : comptes,
			"model" : ecritures_comptables,
			"equilibre_credit" : "%.2f" % equilibre_credit,
			"equilibre_debit" : "%.2f" % equilibre_debit,
			"date_debut" : request.POST["date_debut"],
			"date_fin" : request.POST["date_fin"],
			"devise" : devise,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_BUDGET,
			'format' : 'landscape',
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleControle/rapport/generated.html")
		docHtml = template.render(context)
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleControle'
		monLog.error("{} :: {}::\nErreur lors génération analyse budgetaire \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur generer analyse budgetaire ')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_controle_analyse_budgetaire"))


def get_analyse_bgt(request):
	try:
		# droit="CREER_RAPPORT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 527
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response



		date_debut = request.POST["date_debut"]
		#date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		#date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		type_extraction = request.POST["type_extraction"]

		end = endpoint.reportingEndPoint()

		context = {
			'title' : 'Analyse Budgétaire',
			'endpoint' : end,
			'date_debut' : date_debut,
			'date_fin' : date_fin,
			'type_extraction' : type_extraction,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_CONTROLE,
			'menu' : 4,
			'sous_modules': sous_modules,

		}
		template = loader.get_template('ErpProject/ModuleControle/rapport/print.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleControle'
		monLog.error("{} :: {}::\nERREUR LORS DU print ANALYSE BUDGETAIRE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_controle_analyse_budgetaire'))

























