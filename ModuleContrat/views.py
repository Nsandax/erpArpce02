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
from ErpBackOffice.utils.separateur import makeFloat
from ErpBackOffice.utils.tools import ErpModule
from ErpBackOffice.utils.wkf_task import wkf_task
import datetime
import json
from ModuleContrat.dao.dao_categorie_operation_contrat import dao_categorie_operation_contrat
from ModuleContrat.dao.dao_type_operation_contrat import dao_type_operation_contrat
#Import from ModuleConversation
from ModuleConversation.dao.dao_notif import dao_notif
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ModuleAchat.dao.dao_demande_achat import dao_demande_achat
from ModuleContrat.dao.dao_utils import dao_utils

from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleContrat.dao.dao_contrat import dao_contrat
from ModuleContrat.dao.dao_demande_cotation import dao_demande_cotation
from ModuleContrat.dao.dao_lettre_commande import dao_lettre_commande
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.utils.auth import auth
from ModuleContrat.dao.dao_typemarche import dao_typemarche
from ErpBackOffice.dao.dao_model import dao_model
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ErpBackOffice.utils.pagination import pagination
from ModuleContrat.dao.dao_avis_appel_offre import dao_avis_appel_offre
from ModuleBudget.dao.dao_dashbord import dao_dashbord
from ErpBackOffice.utils.wkf_task import wkf_task
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleContrat.dao.dao_operation_contrat import dao_operation_contrat
from ErpBackOffice.dao.dao_document import dao_document


#LOGGING
import logging, inspect
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ErpBackOffice.utils.print import weasy_print
monLog = logging.getLogger("logger")
module= "ModuleContrat"
var_module_id = 100


def get_index(request):
	permission_number = 635
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_contrat.toListContrats(), permission_number, groupe_permissions, identite.utilisateur(request))
	# #print('******* End Regle *******************')
	module_name = "MODULE_CONTRAT"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()
	print("La Notif Nomber", temp_notif_count)
	mois,values, nbrebc = dao_dashbord.toGetLastBCMonth()
	bcvalide,lesjours,lesvaleurs = dao_dashbord.toGetCBValide()
	typemarche = dao_typemarche.toListTypemarche()
	lastcontrat = dao_dashbord.lastcontrat()
	lettreCommande = dao_dashbord.lastlettreCommande()
	avisappel = dao_dashbord.CountAppOffre()
	demandeDC = dao_dashbord.CountDC()
	lettreC= dao_dashbord.CountlettreC()
	labelcontrat, valuecontrat = dao_dashbord.getfrequenceContratYear()
	dataC = dao_dashbord.getfrequencecontratMounth()

	context = {
		'title' : 'Tableau de Bord',
		'model' : model,
		'temp_notif_count':temp_notif_count,
		'temp_notif_list':temp_notif_list,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100,
		'mois':mois,'values':values, 'nbrebc':nbrebc,
		'lesjours':lesjours,'lesvaleurs':lesvaleurs,
		'types': typemarche,'lastcontrat':lastcontrat,'lettreCommande':lettreCommande,'avisappel':avisappel,'demandeDC':demandeDC,
		'lettreC':lettreC, 'labelcontrat':labelcontrat, 'valuecontrat':valuecontrat,'dataC':dataC,'contratSign':dao_dashbord.contratSign(),
		'contratWaiting': dao_dashbord.contratWaiting()
	}
	template = loader.get_template("ErpProject/ModuleContrat/index.html")
	return HttpResponse(template.render(context, request))

def get_lister_marche_travaux(request):
	type_marche, permission_number = 1, 646
	return get_lister_marche(request, type_marche, permission_number)

def get_lister_marche_fournitures(request):
	type_marche, permission_number = 2, 647
	return get_lister_marche(request, type_marche, permission_number)

def get_lister_marche_prestations(request):
	type_marche, permission_number = 3, 648
	return get_lister_marche(request, type_marche, permission_number)

def get_lister_marche_services(request):
	type_marche, permission_number = 4, 649
	return get_lister_marche(request, type_marche, permission_number)


def get_lister_marche(request, type_id, permission_number):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		type_id=int(type_id)
		type_marche = dao_typemarche.toGetTypemarche(type_id)

		appels = dao_avis_appel_offre.toListAppelOffreByTypeMarche(type_id)
		demandes = dao_demande_cotation.toListDemandeCotationByTypeMarche(type_id)
		lettres = dao_lettre_commande.toListLettreCommandeByTypeMarche(type_id)

		template = loader.get_template('ErpProject/ModuleContrat/typemarche/marche/list.html')
		context ={
			'title' : f"{type_marche.designation}",
			'appels' : appels,
			'demandes': demandes,
			'lettres': lettres,
			'model': type_marche,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_CONTRAT,
			'organisation':dao_organisation.toGetMainOrganisation(),
			'menu' : 4
		}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS get_lister_marche \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_contrat_list_typemarche'))


def get_lister_avis_appel_offre(request):
	try:
		permission_number = 640
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		model = dao_model.toListModel(dao_avis_appel_offre.toListAvis_appel_offre(), permission_number, groupe_permissions, identite.utilisateur(request))

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : "Liste des avis d'appel d'offre",
			'model' : model,
			'utilisateur' : utilisateur,
			'view' : view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#'roles' : roles,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_CONTRAT,
			'menu' : 1
		}
		template = loader.get_template('ErpProject/ModuleContrat/avis_appel_offre/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleContrat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA LISTE AViS FOURNISSEUR\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		##print('Erreur Liste Avis Appel offre')
		##print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_contrat_index'))

def get_creer_avis_appel_offre(request, ref = None):
	permission_number = 641
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	etat_actuel_id = 0
	etape_wkf_id = 0
	demande_wkf_id = 0
	etat = ""
	devise = dao_devise.toGetDeviseReference()

	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		#print("Aucune demande d'achat trouvée")
		pass

	demandes = dao_demande_achat.toListDemandesPourAvisAppelOffre()

	context ={'title' : "Création Avis d'appel d'offre",
				'etat_actuel_id' : etat_actuel_id,
				'etape_wkf' : etape_wkf_id,
				'etat':etat,
				'devise': devise,
				'demande_wkf' : demande_wkf_id,
				'demandes':demandes,
				'type_marche': dao_typemarche.toGetTypemarche(ref) if ref else None,
				'utilisateur' : utilisateur,
				'actions':auth.toGetActions(modules,utilisateur),
				'organisation': dao_organisation.toGetMainOrganisation(),
				'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_CONTRAT,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleContrat/avis_appel_offre/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_avis_appel_offre(request):
	type_marche_id = request.POST['type_marche_id']
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_signature"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		#numero_reference = request.POST['numero_reference']
		numero_dossier = request.POST['numero_dossier']
		designation_commission = request.POST['designation_commission']
		objet_appel = request.POST['objet_appel']
		financement = request.POST['financement']
		type_appel_offre = int(request.POST['type_appel_offre'])
		lieu_consultation = request.POST['lieu_consultation']
		qualification = request.POST['qualification']
		conditions = request.POST['conditions']
		date_signature = request.POST['date_signature']
		lieu_depot = request.POST['lieu_depot']
		date_depot = request.POST['date_depot']
		delai_engagement = request.POST['delai_engagement']
		montant_commission = request.POST['montant_commission']
		demande_id = request.POST["demande_id"]
		desc = request.POST['desc']
		nombre_lots = request.POST['nombre_lots']
		montant = makeFloat(request.POST['montant'])
		devise_id = request.POST['devise_id']
		val = "AOR"
		if type_appel_offre == 0: val = "AOR"
		elif type_appel_offre == 1: val = "AON"
		elif type_appel_offre == 2: val = "AOI"
		numero_reference = dao_utils.genererNumero(dao_typemarche.toGetTypemarche(type_marche_id).code, val, dao_demande_cotation.toListDemande_cotation().count())


		if montant < makeFloat(50000000):
			messages.add_message(request, messages.ERROR, "Le montant est en dessous du seuil pour un appel d'avis (50 000 000) FCFA")
			return HttpResponseRedirect(reverse('module_contrat_add_avis_appel_offre', args=(type_marche_id,)))


		auteur = identite.utilisateur(request)

		if (demande_id == "") or (demande_id == 0) :
			demande_id = None

		date_signature = date_signature[6:10] + '-' + date_signature[3:5] + '-' + date_signature[0:2]
		date_signature = datetime.datetime.strptime(date_signature, "%Y-%m-%d").date()

		date_depot = date_depot[6:10] + '-' + date_depot[3:5] + '-' + date_depot[0:2]
		date_depot = datetime.datetime.strptime(date_depot, "%Y-%m-%d").date()

		avis_appel_offre=dao_avis_appel_offre.toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,objet_appel,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc,demande_id, type_marche_id, nombre_lots, montant, devise_id)
		avis_appel_offre=dao_avis_appel_offre.toSaveAvis_appel_offre(auteur, avis_appel_offre)


		#Initialisation du workflow avis appel offre
		wkf_task.initializeWorkflow(auteur,avis_appel_offre, "Appel d'offre")

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# return HttpResponseRedirect(reverse('module_contrat_list_avis_appel_offre'))
		return HttpResponseRedirect(reverse("module_contrat_detail_avis_appel_offre", args=(avis_appel_offre.id,)))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER AVIS_APPEL_OFFRE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_contrat_add_avis_appel_offre', args=(type_marche_id,)))


def get_details_avis_appel_offre(request,ref):
	try:
		permission_number = 640
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#print("**-------****")

		ref=int(ref)
		avis_appel_offre=dao_avis_appel_offre.toGetAvis_appel_offre(ref)

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,avis_appel_offre)
		template = loader.get_template('ErpProject/ModuleContrat/avis_appel_offre/item.html')
		context ={
					'title' : "Détails sur l'appel d'offre N° " + avis_appel_offre.numero_reference,
					'model' : avis_appel_offre,
					'utilisateur' : utilisateur,
					'actions':auth.toGetActions(modules,utilisateur),
					'organisation': dao_organisation.toGetMainOrganisation(),
					'modules' : modules,
					'sous_modules': sous_modules,
					'module' : ErpModule.MODULE_CONTRAT,
					'historique' : historique,
					'roles':groupe_permissions,
					'etapes_suivantes' : transition_etape_suivant,
					'signee' : signee,
					'content_type_id':content_type_id,
					'documents':documents,
					'organisation':dao_organisation.toGetMainOrganisation(),
					'menu' : 4
					}


		return HttpResponse(template.render(context, request))
	except Exception as e:
		##print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS AVIS_APPEL_OFFRE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_contrat_list_avis_appel_offre'))

def get_modifier_avis_appel_offre(request,ref):
	permission_number = 639
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "Modifier un avis d'appel d'offre",
		'model':model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_CONTRAT,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleContrat/avis_appel_offre/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_avis_appel_offre(request):

	id = int(request.POST['ref'])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_signature"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		numero_reference = request.POST['numero_reference']
		numero_dossier = request.POST['numero_dossier']
		designation_commission = request.POST['designation_commission']
		objet_appel = request.POST['objet_appel']
		financement = request.POST['financement']
		type_appel_offre = request.POST['type_appel_offre']
		lieu_consultation = request.POST['lieu_consultation']
		qualification = request.POST['qualification']
		conditions = request.POST['conditions']
		date_signature = request.POST['date_signature']
		lieu_depot = request.POST['lieu_depot']
		date_depot = request.POST['date_depot']
		delai_engagement = request.POST['delai_engagement']
		montant_commission = request.POST['montant_commission']
		desc = request.POST['desc']
		auteur = identite.utilisateur(request)

		date_signature = date_signature[6:10] + '-' + date_signature[3:5] + '-' + date_signature[0:2]
		date_signature = datetime.datetime.strptime(date_signature, "%Y-%m-%d").date()

		date_depot = date_depot[6:10] + '-' + date_depot[3:5] + '-' + date_depot[0:2]
		date_depot = datetime.datetime.strptime(date_depot, "%Y-%m-%d").date()

		avis_appel_offre=dao_avis_appel_offre.toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,objet_appel,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc)
		avis_appel_offre=dao_avis_appel_offre.toUpdateAvis_appel_offre(id, avis_appel_offre)
		return HttpResponseRedirect(reverse('module_contrat_list_avis_appel_offre'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER AVIS_APPEL_OFFRE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_avis_appel_offre'))





def get_lister_typemarche(request):
	permission_number = 636
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_typemarche.toListTypemarche(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	module_name = "MODULE_CONTRAT"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)

	# model = dao_typemarche.toListTypemarche()
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)
	context ={'title' : 'Les types de marché',
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/typemarche/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_typemarche(request):
	permission_number = 638
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_typemarche.toListTypemarche(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	context ={
		'title' : 'Créer un type de marché',
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/typemarche/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_typemarche(request):

	try:
		designation = request.POST['designation']
		code = request.POST['code']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		typemarche=dao_typemarche.toCreateTypemarche(designation,code,description)
		typemarche=dao_typemarche.toSaveTypemarche(auteur, typemarche)
		return HttpResponseRedirect(reverse('module_contrat_list_typemarche'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TYPEMARCHE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_typemarche'))


def get_details_typemarche(request,ref):
	permission_number = 636
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response
	try:
		ref=int(ref)
		typemarche=dao_typemarche.toGetTypemarche(ref)
		array_data,arraydata2 = dao_typemarche.torefallitems(ref)
		template = loader.get_template('ErpProject/ModuleContrat/typemarche/item.html')
		context ={
			'title' : 'Details sur un type de marché',
			'typemarche' : typemarche,
			'sous_modules':sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
			# "modules" : dao_module.toListModulesInstalles(),
			"module" : ErpModule.MODULE_CONTRAT,
			"menu" : 100,
			'array_data':array_data,'array_data2':arraydata2
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		##print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TYPEMARCHE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_list_typemarche'))

def get_modifier_typemarche(request,ref):
	permission_number = 637
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	ref = int(ref)
	model = dao_typemarche.toGetTypemarche(ref)
	context ={
		'title' : 'Modifier les informations sur un type de marché',
		'model':model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/typemarche/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_typemarche(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		code = request.POST['code']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		typemarche=dao_typemarche.toCreateTypemarche(designation,code,description)
		typemarche=dao_typemarche.toUpdateTypemarche(id, typemarche)
		return HttpResponseRedirect(reverse('module_contrat_list_typemarche'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER TYPEMARCHE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_typemarche'))


def get_lister_lettre_commande(request):
	permission_number = 626
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_lettre_commande.toListLettre_commande(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	module_name = "MODULE_CONTRAT"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)
	marche = dao_typemarche.toListTypemarche()

	# model = dao_lettre_commande.toListLettre_commande()
	context ={
		'title' : 'Liste des lettres commandes',
		'model' : model,
		'sous_modules':sous_modules,
		'marche': marche,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/lettre_commande/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_lettre_commande(request, ref = None):
	permission_number = 628
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	etat_actuel_id = 0
	etape_wkf_id = 0
	demande_wkf_id = 0
	etat = ""
	montant = 0
	devise = dao_devise.toGetDeviseReference()


	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		##print("Aucune demande d'achat trouvée")
		pass

	demandes = dao_demande_achat.toListDemandesPourAvisAppelOffre()


	context ={
		'title' : 'Création Lettre de Commande',
		'sous_modules':sous_modules,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'etat':etat,
		'demande_wkf' : demande_wkf_id,
		'demandes':demandes,
		'montant': montant,
		'devise':devise,
		'type_marche': dao_typemarche.toGetTypemarche(ref) if ref else None,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/lettre_commande/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_lettre_commande(request):
	type_marche_id = request.POST['type_marche_id']
	try:
		#numero = request.POST['numero']

		demande_id = request.POST['demande_id']
		montant = makeFloat(request.POST['montant'])
		devise_id = request.POST['devise_id']
		description = request.POST['description']
		intitule = request.POST['intitule']
		financement = request.POST['financement']
		nombre_lots = request.POST['nombre_lots']
		auteur = identite.utilisateur(request)

		numero = dao_utils.genererNumero(dao_typemarche.toGetTypemarche(type_marche_id).code, "LC", dao_lettre_commande.toListLettre_commande().count())
		if montant > makeFloat(10000000):
			messages.add_message(request, messages.ERROR, "Vous avez dépassé le seuil pour une lettre de commande (10 000 000) FCFA")
			return HttpResponseRedirect(reverse('module_contrat_add_lettre_commande', args=(type_marche_id,)))


		lettre_commande=dao_lettre_commande.toCreateLettre_commande(numero,demande_id,montant,devise_id,type_marche_id,description, intitule, financement, nombre_lots)
		lettre_commande=dao_lettre_commande.toSaveLettre_commande(auteur, lettre_commande)
		wkf_task.initializeWorkflow(auteur,lettre_commande)

		return HttpResponseRedirect(reverse('module_contrat_detail_lettre_commande', args=(lettre_commande.id,)))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER LETTRE_COMMANDE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_lettre_commande', args=(type_marche_id,)))


def get_details_lettre_commande(request,ref):
	permission_number = 626
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response
	try:
		ref=int(ref)
		lettre_commande=dao_lettre_commande.toGetLettre_commande(ref)
		template = loader.get_template('ErpProject/ModuleContrat/lettre_commande/item.html')
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,lettre_commande)
		context ={
			'title' : 'Details sur lettre_commande',
			'model' : lettre_commande,
			'sous_modules':sous_modules,
			'historique' : historique,
			'roles':groupe_permissions,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'documents':documents,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
			# "modules" : dao_module.toListModulesInstalles(),
			"module" : ErpModule.MODULE_CONTRAT,
			"menu" : 100
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		##print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS LETTRE_COMMANDE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_list_lettre_commande'))

def get_modifier_lettre_commande(request,ref):
	permission_number = 627
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	ref = int(ref)
	model = dao_lettre_commande.toGetLettre_commande(ref)
	context ={
		'title' : 'Modifier Lettre commande',
		'model':model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/lettre_commande/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_lettre_commande(request):

	id = int(request.POST['ref'])
	try:
		numero = request.POST['numero']
		demande_achat_id = request.POST['demande_achat_id']
		montant = makeFloat(request.POST['montant'])
		devise_id = request.POST['devise_id']
		type_marche_id = request.POST['type_marche_id']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		lettre_commande=dao_lettre_commande.toCreateLettre_commande(numero,demande_achat_id,montant,devise_id,type_marche_id,description)
		lettre_commande=dao_lettre_commande.toUpdateLettre_commande(id, lettre_commande)
		return HttpResponseRedirect(reverse('module_contrat_list_lettre_commande'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER LETTRE_COMMANDE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_lettre_commande', args=(id,)))

def get_lister_demande_cotation(request):
	permission_number = 629
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response


	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_demande_cotation.toListDemande_cotation(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	module_name = "MODULE_CONTRAT"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)

	# model = dao_typemarche.toListTypemarche()
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)
	# model = dao_demande_cotation.toListDemande_cotation()
	context ={
		'title' : 'Liste de demande de cotation',
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/demande_cotation/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_demande_cotation(request, ref = None):
	permission_number = 630
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_demande_cotation.toListDemande_cotation(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	etat_actuel_id = 0
	etape_wkf_id = 0
	demande_wkf_id = 0
	etat = ""
	devise = dao_devise.toGetDeviseReference()
	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		##print("Aucune demande d'achat trouvée")
		pass

	demandes = dao_demande_achat.toListDemandesPourAvisAppelOffre()

	context ={
		'title' : 'Création Demande de cotation',
		'model' : model,
		'devise': devise,
		'sous_modules':sous_modules,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'etat':etat,
		'demande_wkf' : demande_wkf_id,
		'demandes':demandes,
		'type_marche': dao_typemarche.toGetTypemarche(ref) if ref else None,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/demande_cotation/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_demande_cotation(request):
	type_marche_id = request.POST['type_marche_id']
	try:
		#numero = request.POST['numero']
		demande_id = request.POST['demande_id']
		montant = makeFloat(request.POST['montant'])
		devise_id = request.POST['devise_id']
		intitule = request.POST['intitule']
		financement = request.POST['financement']
		nombre_lots = request.POST['nombre_lots']
		fournisseur_id = request.POST['fournisseur_id'] if int(request.POST['fournisseur_id']) > 0 else None
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		numero = dao_utils.genererNumero(dao_typemarche.toGetTypemarche(type_marche_id).code, "CF", dao_demande_cotation.toListDemande_cotation().count())
		if montant > makeFloat(50000000) or montant < makeFloat(10000000):
			messages.add_message(request, messages.ERROR, "Vous avez dépassé le seuil pour une demande de cotation (10 000 000 à 50 000 000) FCFA")
			return HttpResponseRedirect(reverse('module_contrat_add_demande_cotation', args=(type_marche_id,)))


		demande_cotation=dao_demande_cotation.toCreateDemande_cotation(numero,demande_id,montant,devise_id,fournisseur_id,type_marche_id,description, intitule, financement, nombre_lots)
		demande_cotation=dao_demande_cotation.toSaveDemande_cotation(auteur, demande_cotation)

		wkf_task.initializeWorkflow(auteur,demande_cotation)

		return HttpResponseRedirect(reverse('module_contrat_detail_demande_cotation', args=(demande_cotation.id,)))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER DEMANDE_COTATION \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_demande_cotation', args=(type_marche_id,)))


def get_details_demande_cotation(request,ref):
	permission_number = 629
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response
	try:
		ref=int(ref)
		demande_cotation=dao_demande_cotation.toGetDemande_cotation(ref)
		template = loader.get_template('ErpProject/ModuleContrat/demande_cotation/item.html')
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,demande_cotation)
		context ={
			'title' : 'Details sur demande de cotation',
			'model' : demande_cotation,
			'historique' : historique,
			'roles':groupe_permissions,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'documents':documents,
			'sous_modules':sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
			# "modules" : dao_module.toListModulesInstalles(),
			"module" : ErpModule.MODULE_CONTRAT,
			"menu" : 100
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail get_details_demande_cotation')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS DEMANDE_COTATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_contrat_list_demande_cotation'))
def get_modifier_demande_cotation(request,ref):
	permission_number = 631
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	ref = int(ref)
	model = dao_demande_cotation.toGetDemande_cotation(ref)
	context ={
		'title' : 'Modifier Demande de cotation',
		'model':model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
		}
	template = loader.get_template('ErpProject/ModuleContrat/demande_cotation/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_demande_cotation(request):

	id = int(request.POST['ref'])
	try:
		numero = request.POST['numero']
		demande_achat_id = int(request.POST['demande_achat_id'])
		montant = float(request.POST['montant'])
		devise_id = int(request.POST['devise_id'])
		fournisseur_id = int(request.POST['fournisseur_id'])
		type_marche_id = int(request.POST['type_marche_id'])
		description = request.POST['description']
		auteur = identite.utilisateur(request)


		demande_cotation=dao_demande_cotation.toCreateDemande_cotation(numero,demande_achat_id,montant,devise_id,fournisseur_id,type_marche_id,description)
		demande_cotation=dao_demande_cotation.toUpdateDemande_cotation(id, demande_cotation)
		return HttpResponseRedirect(reverse('module_contrat_list_demande_cotation'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER DEMANDE_COTATION \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_demande_cotation'))


def get_lister_contrat(request, ref = None):
	permission_number = 632
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	if ref:
		type_marche = dao_typemarche.toGetTypemarche(ref)
		model = dao_contrat.toListByTypeMarche(ref)
		title = f"Contrats {type_marche.designation}"
	else:
		model = dao_contrat.toListContrats()
		title = "Tous les contrats"

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	# model = dao_contrat.toListContrats()
	context ={
		'title' : title,
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/contrat/list.html')
	return HttpResponse(template.render(context, request))

def get_lister_contrat_garantie(request, ref = None):
    permission_number = 5555
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:return response

    if ref:
    	type_marche = dao_typemarche.toGetTypemarche(ref)
    	model = dao_contrat.toListByTypeMarche(ref)
    	title = f"Contrats {type_marche.designation}"
    else:
    	model = dao_contrat.toListContrats_Garantie()
    	title = "les contrats: Garantie de bonne Execution"

	#*******Filtre sur les règles **********#
    model = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    try:
    	view = str(request.GET.get("view","list"))
    except Exception as e:
    	view = "list"

	#Pagination
    model = pagination.toGet(request, model)

	# model = dao_contrat.toListContrats()
    context ={
		'title' : title,
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
    template = loader.get_template('ErpProject/ModuleContrat/contrat/list_garantie.html')
    return HttpResponse(template.render(context, request))

def get_lister_contrat_rec_pro(request, ref = None):
    permission_number = 5556
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:return response

    if ref:
    	type_marche = dao_typemarche.toGetTypemarche(ref)
    	model = dao_contrat.toListByTypeMarche(ref)
    	title = f"Contrats {type_marche.designation}"
    else:
    	model = dao_contrat.toListContrats_receptio_pro()
    	title = "les contrats: Réception Provisior"

	#*******Filtre sur les règles **********#
    model = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    try:
    	view = str(request.GET.get("view","list"))
    except Exception as e:
    	view = "list"

	#Pagination
    model = pagination.toGet(request, model)

	# model = dao_contrat.toListContrats()
    context ={
		'title' : title,
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
    template = loader.get_template('ErpProject/ModuleContrat/contrat/list_garantie.html')
    return HttpResponse(template.render(context, request))

def get_lister_contrat_recep_def(request, ref = None):
    permission_number = 5557
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:return response

    if ref:
    	type_marche = dao_typemarche.toGetTypemarche(ref)
    	model = dao_contrat.toListByTypeMarche(ref)
    	title = f"Contrats {type_marche.designation}"
    else:
    	model = dao_contrat.toListContrats_reception_def()
    	title = "les contrats: Réception Définitive"

	#*******Filtre sur les règles **********#
    model = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    try:
    	view = str(request.GET.get("view","list"))
    except Exception as e:
    	view = "list"

	#Pagination
    model = pagination.toGet(request, model)

	# model = dao_contrat.toListContrats()
    context ={
		'title' : title,
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
    template = loader.get_template('ErpProject/ModuleContrat/contrat/list_garantie.html')
    return HttpResponse(template.render(context, request))

def get_creer_contrat(request, source = ""):

	permission_number = 633
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	devise = dao_devise.toGetDeviseReference()
	type_marche = None

	etat_actuel_id = 0
	etape_wkf_id = 0
	etat = None
	Nreference= dao_contrat.toGenerateNumeroContrat()
	try:
		etat_actuel_id = request.POST["doc_id"]
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
		if source == "demande_cotation":
			etat = dao_demande_cotation.toGetDemande_cotation(etat_actuel_id)
		elif source == "appel_offre":
			etat = dao_avis_appel_offre.toGetAvis_appel_offre(etat_actuel_id)
		type_marche = etat.type_marche
	except Exception as e:
		##print("Aucune demande d'achat trouvée")
		pass

	context ={
		'title' : 'Création Contrat',
		'devise': devise,
		'etat_actuel_id' : etat_actuel_id,
		'etape_wkf' : etape_wkf_id,
		'etat':etat,
		'source': source,
		'type_marche': type_marche,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100,
		'Nreference':Nreference
	}
	template = loader.get_template('ErpProject/ModuleContrat/contrat/add.html')
	return HttpResponse(template.render(context, request))


def get_creer_contrat_from_demande_cotation(request):
	source = "demande_cotation"
	return get_creer_contrat(request, source)

def get_creer_contrat_from_appel_offre(request):
	source = "appel_offre"
	return get_creer_contrat(request, source)

def post_creer_contrat(request):

	try:
		numero_reference = request.POST['numero_reference']
		objet = request.POST['objet']
		fournisseur_id = request.POST['fournisseur_id']
		montant = makeFloat(request.POST['montant'])
		devise_id = request.POST['devise_id']
		modalite = request.POST['modalite']
		type_marche_id = request.POST['type_marche_id']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		if date_fin: date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		else: date_fin = None
		demande_cotation_id = request.POST["demande_cotation_id"] if "demande_cotation_id" in request.POST else None
		appel_offre_id = request.POST["appel_offre_id"] if "appel_offre_id" in request.POST else None
		auteur = identite.utilisateur(request)


		contrat = dao_contrat.toCreateContrat(numero_reference, objet, montant, devise_id, type_marche_id, date_debut, fournisseur_id, date_fin, demande_cotation_id, appel_offre_id, modalite)
		contrat=dao_contrat.toSaveContrat(auteur, contrat)

		wkf_task.initializeWorkflow(auteur,contrat)

		return HttpResponseRedirect(reverse('module_contrat_detail_contrat', args=(contrat.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CONTRAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_contrat'))


def get_details_contrat(request,ref):
	permission_number = 632
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response
	try:
		ref=int(ref)
		contrat=dao_contrat.toGetContrat(ref)
		template = loader.get_template('ErpProject/ModuleContrat/contrat/item.html')
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,contrat)
		context ={
			'title' : 'Details sur contrat',
			'model' : contrat,
			'sous_modules':sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'typeOperation': dao_type_operation_contrat.toListTypeOperation(),
			'categorieOperation': dao_categorie_operation_contrat.toListCategorieOperation(),
			'utilisateur' : utilisateur,
			'historique' : historique,
			'roles':groupe_permissions,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'documents':documents,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
			# "modules" : dao_module.toListModulesInstalles(),
			"module" : ErpModule.MODULE_CONTRAT,
			"menu" : 100
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		##print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CONTRAT \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_list_contrat'))

def get_modifier_contrat(request,ref):
	permission_number = 634
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	ref = int(ref)
	model = dao_contrat.toGetContrat(ref)
	context ={
		'title' : 'Modifier le Contrat',
		'model':model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/contrat/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_contrat(request):

	id = int(request.POST['ref'])
	try:
		objet = request.POST['objet']
		titulaire = request.POST['titulaire']
		telephone = int(request.POST['telephone'])
		montant = float(request.POST['montant'])
		devise_id = int(request.POST['devise_id'])
		financement = request.POST['financement']
		date_contrat = request.POST['date_contrat']
		document_id = int(request.POST['document_id'])
		auteur = identite.utilisateur(request)

		date_contrat = date_contrat[6:10] + '-' + date_contrat[3:5] + '-' + date_contrat[0:2]

		# objet_modele = dao_contrat.toGetContrat(id)
		objet_modele = None

		contrat=dao_contrat.toCreateContrat(objet,titulaire,telephone,montant,devise_id,financement,date_contrat,objet_modele)
		contrat=dao_contrat.toUpdateContrat(id, contrat)
		return HttpResponseRedirect(reverse('module_contrat_list_contrat'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CONTRAT \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_contrat'))




# ********************************** GRE A GRE

def get_lister_gre_a_gre(request):
	permission_number = 642
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_avis_appel_offre.toListAvis_appel_offre(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	# model = dao_typemarche.toListTypemarche()
	#print('Gre_Gre',model)
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)
	# #print('Gre_Gre',model)
	context ={'title' : 'Liste de Gré à Gré',
		'model' : model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/Gre_Gre/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_gre_a_gre(request, ref = None):
	permission_number = 643
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	etat_actuel_id = 0
	etape_wkf_id = 0
	demande_wkf_id = 0
	etat = ""
	devise = dao_devise.toGetDeviseReference()

	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		#print("Aucune demande d'achat trouvée")
		pass

	demandes = dao_demande_achat.toListDemandesPourAvisAppelOffre()


	context ={
		'title' : 'Création Gré à Gré',
		'etat_actuel_id' : etat_actuel_id,
		'etape_wkf' : etape_wkf_id,
		'etat':etat,
		'devise': devise,
		'demande_wkf' : demande_wkf_id,
		'demandes':demandes,
		'sous_modules':sous_modules,
		'type_marche': dao_typemarche.toGetTypemarche(ref) if ref else None,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/Gre_Gre/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_gre_a_gre(request):

	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		#if not auth.toPostValidityDate(var_module_id, request.POST["date_signature"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		numero_dossier = request.POST['numero_dossier']
		designation_commission = ''
		objet_appel = request.POST['objet_appel']
		financement = request.POST['financement']
		type_marche_id = request.POST['type_marche_id']
		type_appel_offre = request.POST['type_appel_offre']
		lieu_consultation = ''
		qualification = ''
		conditions = ''
		date_signature = None #request.POST['date_signature']
		lieu_depot = ''
		date_depot = None
		delai_engagement = ''
		montant_commission = ''
		demande_id = request.POST["demande_id"]
		desc = request.POST['desc']
		nombre_lots = request.POST['nombre_lots']
		montant = makeFloat(request.POST['montant'])
		devise_id = request.POST['devise_id']

		numero_reference = dao_utils.genererNumero(dao_typemarche.toGetTypemarche(type_marche_id).code, "ED", dao_demande_cotation.toListDemande_cotation().count())


		auteur = identite.utilisateur(request)


		avis_appel_offre=dao_avis_appel_offre.toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,objet_appel,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc,demande_id, type_marche_id, nombre_lots, montant, devise_id)
		avis_appel_offre=dao_avis_appel_offre.toSaveAvis_appel_offre(auteur, avis_appel_offre)

		#Initialisation du workflow avis appel offre
		wkf_task.initializeWorkflow(auteur,avis_appel_offre, "Gre a Gre")

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# return HttpResponseRedirect(reverse('module_contrat_list_avis_appel_offre'))
		return HttpResponseRedirect(reverse("module_contrat_detail_gre_a_gre", args=(avis_appel_offre.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement', e)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TYPEMARCHE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_gre_a_gre'))

def get_details_gre_a_gre(request,ref):
	permission_number = 642
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response
	try:
		#print("**********************")
		ref=int(ref)
		avis_appel_offre=dao_avis_appel_offre.toGetAvis_appel_offre(ref)
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,avis_appel_offre)


		template = loader.get_template('ErpProject/ModuleContrat/Gre_Gre/item.html')
		context ={
			'title' : 'Details sur Offre Gré à Gré',
			'model' : avis_appel_offre,
			'sous_modules':sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'modules' : modules,
			'historique' : historique,
			'roles':groupe_permissions,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'documents':documents,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
			# "modules" : dao_module.toListModulesInstalles(),
			"module" : ErpModule.MODULE_CONTRAT,
			"menu" : 100
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TYPEMARCHE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_contrat_lister_gre_a_gre'))

def get_modifier_gre_a_gre(request,ref):
	permission_number = 644
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:return response

	ref = int(ref)
	model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context ={
		'title' : 'Modifier Appel offre de type Gré à Gré',
		'model':model,
		'sous_modules':sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		"module" : ErpModule.MODULE_CONTRAT,
		"menu" : 100
	}
	template = loader.get_template('ErpProject/ModuleContrat/Gre_Gre/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_gre_a_gre(request):

	id = int(request.POST['ref'])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_signature"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		numero_reference = request.POST['numero_reference']
		numero_dossier = request.POST['numero_dossier']
		designation_commission = request.POST['designation_commission']
		objet_appel = request.POST['objet_appel']
		financement = request.POST['financement']
		type_appel_offre = request.POST['type_appel_offre']
		lieu_consultation = request.POST['lieu_consultation']
		qualification = request.POST['qualification']
		conditions = request.POST['conditions']
		date_signature = request.POST['date_signature']
		lieu_depot = request.POST['lieu_depot']
		date_depot = request.POST['date_depot']
		delai_engagement = request.POST['delai_engagement']
		montant_commission = request.POST['montant_commission']
		desc = request.POST['desc']
		auteur = identite.utilisateur(request)

		date_signature = date_signature[6:10] + '-' + date_signature[3:5] + '-' + date_signature[0:2]
		date_signature = datetime.datetime.strptime(date_signature, "%Y-%m-%d").date()

		date_depot = date_depot[6:10] + '-' + date_depot[3:5] + '-' + date_depot[0:2]
		date_depot = datetime.datetime.strptime(date_depot, "%Y-%m-%d").date()

		avis_appel_offre=dao_avis_appel_offre.toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,objet_appel,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc)
		avis_appel_offre=dao_avis_appel_offre.toUpdateAvis_appel_offre(id, avis_appel_offre)

		return HttpResponseRedirect(reverse('module_contrat_lister_gre_a_gre'))
	except Exception as e:
		##print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER TYPEMARCHE \n {}'.format(auteur.nom_complet, module,e))
		##print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_gre_a_gre'))



def get_modelprint_lettrecomande(request):
	permission_number = 626
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "Lettre de Commande",
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 100
	}
	return weasy_#print("ErpProject/ModuleAchat/reporting/lettrecomande.html", "commande.pdf", context)

def get_modelprint_appel_offre(request):
	permission_number = 626
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "Appel d\'offre",
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 100
	}
	return weasy_#print("ErpProject/ModuleAchat/reporting/model_appel_offre.html", "appel_offre.pdf", context)

def get_modelprint_demande_cotation(request):
	permission_number = 626
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "Demande de Cotation",
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 100
	}
	return weasy_#print("ErpProject/ModuleAchat/reporting/demande_cotation.html", "cotation.pdf", context) #COTATION

def get_modelprint_pv(request):
	permission_number = 626
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "PV",
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 100
	}
	return weasy_#print("ErpProject/ModuleAchat/reporting/model_pv.html", "modelepv.pdf", context)   #MODELE PV


def post_creer_operation_contrat(request):
	contrat_id = int(request.POST['contrat_id'])
	try:
		categorie = request.POST['categorie']
		designation = request.POST['designation']
		type = request.POST['type']
		valeur = makeFloat(request.POST['valeur'])
		description = request.POST['description']
		reference_document = request.POST['reference_document']

		auteur = identite.utilisateur(request)

		operation_contrat = dao_operation_contrat.toCreateOperationContrat(designation, contrat_id, categorie, type, valeur, None, description, reference_document)
		operation_contrat = dao_operation_contrat.toSaveOperationContrat(auteur, operation_contrat)

		if 'file_upload' in request.FILES:
			files = request.FILES.getlist("file_upload",None)
			dao_document.toUploadDocument(auteur,files,operation_contrat.contrat)

		return HttpResponseRedirect(reverse('module_contrat_detail_contrat', args=(contrat_id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CONTRAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_contrat_add_contrat'))


