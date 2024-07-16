# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.template.response import SimpleTemplateResponse, TemplateResponse
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
import os, calendar
import json
import pandas as pd
from rest_framework.decorators import api_view
import base64, uuid
from locale import atof, setlocale, LC_NUMERIC
import numpy as np
from dateutil.relativedelta import relativedelta
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from django.db import transaction
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique import dao_wkf_historique
from ErpBackOffice.dao.dao_document import dao_document
from ErpBackOffice.models import *
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task
from ErpBackOffice.utils.endpoint import endpoint
from ErpBackOffice.utils.print import weasy_print


#LOGGING
import logging, inspect, unidecode
from ModuleRecouvrement.models import *
monLog = logging.getLogger("logger")
module= "ModuleRecouvrement"
var_module_id = 24
vars_module = {"name" : "MODULE_RECOUVREMENT", "value" : 21 }


def get_index(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)
		if response != None:
			return response

		context = {
			"title" : "Tableau de Bord",
			"utilisateur" : utilisateur,
			"organisation": dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			"module" : vars_module
		}

		template = loader.get_template("ErpProject/ModuleRecouvrement/index.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

# DOSSIER_RECOUVREMENT CONTROLLERS
from ModuleRecouvrement.dao.dao_dossier_recouvrement import dao_dossier_recouvrement

def get_lister_dossier_recouvrement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
			if query == '': query = None
		except Exception as e:
			view = 'list'
			query = None

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_dossier_recouvrement.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des dossiers de recouvrement',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_dossier_recouvrement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Dossier de recouvrement',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Dossier_recouvrement(),
			'clients' : Model_Client.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_dossier_recouvrement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_recouvrement_add_dossier_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		client_id = makeIntId(request.POST['client_id'])
		if client_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Client\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])

		auteur = identite.utilisateur(request)

		dossier_recouvrement = dao_dossier_recouvrement.toCreate(designation = designation, client_id = client_id, description = description)
		saved, dossier_recouvrement, message = dao_dossier_recouvrement.toSave(auteur, dossier_recouvrement)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_dossier_recouvrement.toListById(dossier_recouvrement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(dossier_recouvrement.id),'obj': str(dossier_recouvrement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_dossier_recouvrement', args=(dossier_recouvrement.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_dossier_recouvrement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		dossier_recouvrement = auth.toGetWithRules(dao_dossier_recouvrement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if dossier_recouvrement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Dossier de recouvrement : {}'.format(dossier_recouvrement),
			'model' : dossier_recouvrement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_list_dossier_recouvrement'))

def get_modifier_dossier_recouvrement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_dossier_recouvrement.toGet(ref)
		context = {
			'title' : 'Modifier Dossier de recouvrement',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'clients' : Model_Client.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_dossier_recouvrement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_recouvrement_update_dossier_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		client_id = makeIntId(request.POST['client_id'])
		if client_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Client\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])
		auteur = identite.utilisateur(request)

		dossier_recouvrement = dao_dossier_recouvrement.toCreate(designation = designation, client_id = client_id, description = description)
		saved, dossier_recouvrement, message = dao_dossier_recouvrement.toUpdate(id, dossier_recouvrement)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_dossier_recouvrement.toListById(dossier_recouvrement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_dossier_recouvrement', args=(dossier_recouvrement.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_dossier_recouvrement(request,ref):
	try:
		same_perm_with = 'module_recouvrement_add_dossier_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_dossier_recouvrement.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'clients' : Model_Client.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_dossier_recouvrement(request,ref):
	try:
		same_perm_with = 'module_recouvrement_list_dossier_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		dossier_recouvrement = auth.toGetWithRules(dao_dossier_recouvrement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if dossier_recouvrement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Dossier de recouvrement : {}'.format(dossier_recouvrement),
			'model' : dossier_recouvrement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleRecouvrement/reporting/print_dossier_recouvrement.html', 'print_dossier_recouvrement.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_dossier_recouvrement(request):
	try:
		same_perm_with = 'module_recouvrement_add_dossier_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des dossiers de recouvrement',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_dossier_recouvrement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			client_id = makeIntId(str(df['client_id'][i]))
			if client_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Client\' est obligatoire, Veuillez le renseigner SVP!')
			description = str(df['description'][i])

			dossier_recouvrement = dao_dossier_recouvrement.toCreate(designation = designation, client_id = client_id, description = description)
			saved, dossier_recouvrement, message = dao_dossier_recouvrement.toSave(auteur, dossier_recouvrement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_list_dossier_recouvrement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# DOSSIER_RECOUVREMENT REPORTING CONTROLLERS
def get_generer_dossier_recouvrement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Rapport dossier de recouvrement',
			'devises' : dao_devise.toListDevisesActives(),
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/generate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_traiter_dossier_recouvrement(request, utilisateur = None, modules = [], sous_modules = [], enum_module = vars_module):
	#On recupère et format les inputs reçus
	date_debut = request.POST['date_debut']
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST['date_fin']
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#On récupère les données suivant le filtre défini
	model = Model_Dossier_recouvrement.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')

	context = {
		'title' : 'Rapport Dossier de recouvrement',
		'model' : model,
		'date_debut' : request.POST['date_debut'],
		'date_fin' : request.POST['date_fin'],
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : enum_module,
		'organisation' : dao_organisation.toGetMainOrganisation(),
	}
	return context

def post_generer_dossier_recouvrement(request):
	try:
		same_perm_with = 'module_recouvrement_get_generer_dossier_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = post_traiter_dossier_recouvrement(request, utilisateur, modules, sous_modules)
		template = loader.get_template('ErpProject/ModuleRecouvrement/dossier_recouvrement/generated.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_imprimer_rapport_dossier_recouvrement(request):
	try:
		context = post_traiter_dossier_recouvrement(request)
		return weasy_print('ErpProject/ModuleRecouvrement/reporting/rapport_dossier_recouvrement.html', 'rapport_dossier_recouvrement.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_get_generer_dossier_recouvrement'))

# DOSSIER_RECOUVREMENT API CONTROLLERS
def get_list_dossier_recouvrement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		filtered = False
		if 'filtered' in request.GET : filtered = str(request.GET['filtered'])
		date_from = None
		if 'date_from' in request.GET : date_from = request.GET['date_from']
		date_to = None
		if 'date_to' in request.GET : date_to = request.GET['date_to']
		query = ''
		if 'query' in request.GET : query = str(request.GET['query'])

		listes = []
		model = dao_dossier_recouvrement.toList()
		#model = pagination.toGet(request, model)

		for item in model:
			element = {
				'id' : item.id,
				'designation' : str(item.designation),
				'client_id' : makeIntId(item.client_id),
				'description' : str(item.description),
				'statut_id' : makeIntId(item.statut_id),
				'etat' : str(item.etat),
				'creation_date' : item.creation_date,
				'update_date' : item.update_date,
				'auteur_id' : makeIntId(item.auteur_id),
			}
			listes.append(element)

		context = {
			'error' : False,
			'message' : 'Liste récupérée',
			'datas' : listes
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)

def get_item_dossier_recouvrement(request):
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')

		id = 0
		if 'id' in request.GET : id = int(request.GET['id'])

		item = {}
		model = dao_dossier_recouvrement.toGet(id)
		if model != None :
			item = {
				'id' : model.id,
				'designation' : str(model.designation),
				'client_id' : makeIntId(model.client_id),
				'description' : str(model.description),
				'statut_id' : makeIntId(model.statut_id),
				'etat' : str(model.etat),
				'creation_date' : model.creation_date,
				'update_date' : model.update_date,
				'auteur_id' : makeIntId(model.auteur_id),
			}

		context = {
			'error' : False,
			'message' : 'Objet récupéré',
			'item' : item
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		return auth.toReturnApiFailed(request, e)

@api_view(['POST'])
@transaction.atomic
def post_create_dossier_recouvrement(request):
	sid = transaction.savepoint()
	try:
		context = {}
		#token = request.META.get('HTTP_TOKEN')
		#if not token: raise Exception('Erreur, Token manquant')


		designation = ''
		if 'designation' in request.POST : designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnApiFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		client_id = None
		if 'client' in request.POST : client_id = makeIntId(request.POST['client_id'])
		if client_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Client\' est obligatoire, Veuillez le renseigner SVP!')

		description = ''
		if 'description' in request.POST : description = str(request.POST['description'])

		auteur_id = None
		if 'auteur' in request.POST : auteur_id = makeIntId(request.POST['auteur_id'])

		auteur = dao_utilisateur.toGetUtilisateur(auteur_id)

		dossier_recouvrement = dao_dossier_recouvrement.toCreate(designation = designation, client_id = client_id, description = description)
		saved, dossier_recouvrement, message = dao_dossier_recouvrement.toSave(auteur, dossier_recouvrement)

		if saved == False: raise Exception(message)

		objet = {
			'id' : dossier_recouvrement.id,
			'designation' : str(dossier_recouvrement.designation),
			'client_id' : makeIntId(dossier_recouvrement.client_id),
			'description' : str(dossier_recouvrement.description),
			'statut_id' : makeIntId(dossier_recouvrement.statut_id),
			'etat' : str(dossier_recouvrement.etat),
			'creation_date' : dossier_recouvrement.creation_date,
			'update_date' : dossier_recouvrement.update_date,
			'auteur_id' : makeIntId(dossier_recouvrement.auteur_id),
		}
		transaction.savepoint_commit(sid)

		context = {
			'error' : False,
			'message' : 'Enregistrement éffectué avec succès',
			'item' : objet
		}
		return JsonResponse(context, safe=False)
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnApiFailed(request, e)

# SCENARIO_RELANCE CONTROLLERS
from ModuleRecouvrement.dao.dao_scenario_relance import dao_scenario_relance

def get_lister_scenario_relance(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
			if query == '': query = None
		except Exception as e:
			view = 'list'
			query = None

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_scenario_relance.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des scénarios de relance',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_scenario_relance(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Scénario de relance',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Scenario_relance(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_scenario_relance(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_recouvrement_add_scenario_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])

		auteur = identite.utilisateur(request)

		scenario_relance = dao_scenario_relance.toCreate(designation = designation, description = description)
		saved, scenario_relance, message = dao_scenario_relance.toSave(auteur, scenario_relance)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_scenario_relance.toListById(scenario_relance.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		#Ajout Champ (OneToMany - Creation)
		action_scenario_scenario_ids = request.POST.getlist('action_scenario_scenario_ids', [])
		for i in range(0, len(action_scenario_scenario_ids)):
			try:
				objet = Model_Action_scenario.objects.get(pk = action_scenario_scenario_ids[i])
				objet.scenario = scenario_relance
				objet.save()
			except Exception as e: pass

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(scenario_relance.id),'obj': str(scenario_relance)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_scenario_relance', args=(scenario_relance.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_scenario_relance(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		scenario_relance = auth.toGetWithRules(dao_scenario_relance.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if scenario_relance == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Scénario de relance : {}'.format(scenario_relance),
			'model' : scenario_relance,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_list_scenario_relance'))

def get_modifier_scenario_relance(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_scenario_relance.toGet(ref)
		context = {
			'title' : 'Modifier Scénario de relance',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_scenario_relance(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_recouvrement_update_scenario_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])
		auteur = identite.utilisateur(request)

		scenario_relance = dao_scenario_relance.toCreate(designation = designation, description = description)
		saved, scenario_relance, message = dao_scenario_relance.toUpdate(id, scenario_relance)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_scenario_relance.toListById(scenario_relance.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		#MAJ Champ (OneToMany - Modification)
		action_scenario_scenario_ids = request.POST.getlist('action_scenario_scenario_ids', [])
		scenario_relance.action_scenarios_scenario.all().update(scenario = None)
		for i in range(0, len(action_scenario_scenario_ids)):
			try:
				objet = Model_Action_scenario.objects.get(pk = action_scenario_scenario_ids[i])
				objet.scenario = scenario_relance
				objet.save()
			except Exception as e: pass

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_scenario_relance', args=(scenario_relance.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_scenario_relance(request,ref):
	try:
		same_perm_with = 'module_recouvrement_add_scenario_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_scenario_relance.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_scenario_relance(request,ref):
	try:
		same_perm_with = 'module_recouvrement_list_scenario_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		scenario_relance = auth.toGetWithRules(dao_scenario_relance.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if scenario_relance == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Scénario de relance : {}'.format(scenario_relance),
			'model' : scenario_relance,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleRecouvrement/reporting/print_scenario_relance.html', 'print_scenario_relance.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_scenario_relance(request):
	try:
		same_perm_with = 'module_recouvrement_add_scenario_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des scénarios de relance',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_scenario_relance(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			description = str(df['description'][i])

			scenario_relance = dao_scenario_relance.toCreate(designation = designation, description = description)
			saved, scenario_relance, message = dao_scenario_relance.toSave(auteur, scenario_relance)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_list_scenario_relance'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# SCENARIO_RELANCE REPORTING CONTROLLERS
def get_generer_scenario_relance(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Rapport scénario de relance',
			'devises' : dao_devise.toListDevisesActives(),
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/generate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_traiter_scenario_relance(request, utilisateur = None, modules = [], sous_modules = [], enum_module = vars_module):
	#On recupère et format les inputs reçus
	date_debut = request.POST['date_debut']
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST['date_fin']
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#On récupère les données suivant le filtre défini
	model = Model_Scenario_relance.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')

	context = {
		'title' : 'Rapport Scénario de relance',
		'model' : model,
		'date_debut' : request.POST['date_debut'],
		'date_fin' : request.POST['date_fin'],
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : enum_module,
		'organisation' : dao_organisation.toGetMainOrganisation(),
	}
	return context

def post_generer_scenario_relance(request):
	try:
		same_perm_with = 'module_recouvrement_get_generer_scenario_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = post_traiter_scenario_relance(request, utilisateur, modules, sous_modules)
		template = loader.get_template('ErpProject/ModuleRecouvrement/scenario_relance/generated.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_imprimer_rapport_scenario_relance(request):
	try:
		context = post_traiter_scenario_relance(request)
		return weasy_print('ErpProject/ModuleRecouvrement/reporting/rapport_scenario_relance.html', 'rapport_scenario_relance.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_get_generer_scenario_relance'))

# ACTION_SCENARIO CONTROLLERS
from ModuleRecouvrement.dao.dao_action_scenario import dao_action_scenario

def get_lister_action_scenario(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
			if query == '': query = None
		except Exception as e:
			view = 'list'
			query = None

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_action_scenario.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des actions du scénario de relance',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_scenario/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_action_scenario(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Action du scénario de relance',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Action_scenario(),
			'scenario_relances' : Model_Scenario_relance.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_scenario/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_action_scenario(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_recouvrement_add_action_scenario'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		nb_jours = makeInt(request.POST['nb_jours'])
		if nb_jours in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Nombre de jours\' est obligatoire, Veuillez le renseigner SVP!')

		type_action = str(request.POST['type_action'])
		if type_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Type action\' est obligatoire, Veuillez le renseigner SVP!')

		scenario_id = makeIntId(request.POST['scenario_id'])

		est_automatique = True if 'est_automatique' in request.POST else False

		description = str(request.POST['description'])

		sujet = str(request.POST['sujet'])

		message = str(request.POST['message'])

		langue = str(request.POST['langue'])

		auteur = identite.utilisateur(request)

		action_scenario = dao_action_scenario.toCreate(designation = designation, nb_jours = nb_jours, type_action = type_action, scenario_id = scenario_id, est_automatique = est_automatique, description = description, sujet = sujet, message = message, langue = langue)
		saved, action_scenario, message = dao_action_scenario.toSave(auteur, action_scenario)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_action_scenario.toListById(action_scenario.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(action_scenario.id),'obj': str(action_scenario)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_action_scenario', args=(action_scenario.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_action_scenario(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		action_scenario = auth.toGetWithRules(dao_action_scenario.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if action_scenario == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Action du scénario de relance : {}'.format(action_scenario),
			'model' : action_scenario,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_scenario/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_list_action_scenario'))

def get_modifier_action_scenario(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_action_scenario.toGet(ref)
		context = {
			'title' : 'Modifier Action du scénario de relance',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'scenario_relances' : Model_Scenario_relance.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_scenario/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_action_scenario(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_recouvrement_update_action_scenario'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		nb_jours = makeInt(request.POST['nb_jours'])
		if nb_jours in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Nombre de jours\' est obligatoire, Veuillez le renseigner SVP!')

		type_action = str(request.POST['type_action'])
		if type_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Type action\' est obligatoire, Veuillez le renseigner SVP!')

		scenario_id = makeIntId(request.POST['scenario_id'])

		est_automatique = True if 'est_automatique' in request.POST else False

		description = str(request.POST['description'])

		sujet = str(request.POST['sujet'])

		message = str(request.POST['message'])

		langue = str(request.POST['langue'])
		auteur = identite.utilisateur(request)

		action_scenario = dao_action_scenario.toCreate(designation = designation, nb_jours = nb_jours, type_action = type_action, scenario_id = scenario_id, est_automatique = est_automatique, description = description, sujet = sujet, message = message, langue = langue)
		saved, action_scenario, message = dao_action_scenario.toUpdate(id, action_scenario)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_action_scenario.toListById(action_scenario.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_action_scenario', args=(action_scenario.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_action_scenario(request,ref):
	try:
		same_perm_with = 'module_recouvrement_add_action_scenario'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_action_scenario.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'scenario_relances' : Model_Scenario_relance.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_scenario/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_action_scenario(request,ref):
	try:
		same_perm_with = 'module_recouvrement_list_action_scenario'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		action_scenario = auth.toGetWithRules(dao_action_scenario.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if action_scenario == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Action du scénario de relance : {}'.format(action_scenario),
			'model' : action_scenario,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleRecouvrement/reporting/print_action_scenario.html', 'print_action_scenario.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_action_scenario(request):
	try:
		same_perm_with = 'module_recouvrement_add_action_scenario'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des actions du scénario de relance',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_scenario/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_action_scenario(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			nb_jours = makeInt(df['nb_jours'][i])
			if nb_jours in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Nombre de jours\' est obligatoire, Veuillez le renseigner SVP!')
			type_action = str(df['type_action'][i])
			if type_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Type action\' est obligatoire, Veuillez le renseigner SVP!')
			scenario_id = makeIntId(str(df['scenario_id'][i]))
			est_automatique = True if str(df['est_automatique'][i]) == 'True' else False
			description = str(df['description'][i])
			sujet = str(df['sujet'][i])
			message = str(df['message'][i])
			langue = str(df['langue'][i])

			action_scenario = dao_action_scenario.toCreate(designation = designation, nb_jours = nb_jours, type_action = type_action, scenario_id = scenario_id, est_automatique = est_automatique, description = description, sujet = sujet, message = message, langue = langue)
			saved, action_scenario, message = dao_action_scenario.toSave(auteur, action_scenario)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_list_action_scenario'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# ACTION_RELANCE CONTROLLERS
from ModuleRecouvrement.dao.dao_action_relance import dao_action_relance

def get_lister_action_relance(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
			if query == '': query = None
		except Exception as e:
			view = 'list'
			query = None

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_action_relance.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des relances',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_action_relance(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Relance',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Action_relance(),
			'dossier_recouvrements' : Model_Dossier_recouvrement.objects.all(),
			'factures' : Model_Facture.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_action_relance(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_recouvrement_add_action_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		date_action = str(request.POST['date_action'])
		if date_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Date\' est obligatoire, Veuillez le renseigner SVP!')
		date_action = date(int(date_action[6:10]), int(date_action[3:5]), int(date_action[0:2]))

		montant_action = makeFloat(request.POST['montant_action'])

		type_action = str(request.POST['type_action'])

		observation = str(request.POST['observation'])

		statut_action = makeInt(request.POST['statut_action'])
		if statut_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Statut de l\'action\' est obligatoire, Veuillez le renseigner SVP!')

		dossier_recouvrement_id = makeIntId(request.POST['dossier_recouvrement_id'])
		if dossier_recouvrement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Dossier recouvremnet\' est obligatoire, Veuillez le renseigner SVP!')

		facture_id = makeIntId(request.POST['facture_id'])
		if facture_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Facture\' est obligatoire, Veuillez le renseigner SVP!')

		auteur = identite.utilisateur(request)

		action_relance = dao_action_relance.toCreate(designation = designation, date_action = date_action, montant_action = montant_action, type_action = type_action, observation = observation, statut_action = statut_action, dossier_recouvrement_id = dossier_recouvrement_id, facture_id = facture_id)
		saved, action_relance, message = dao_action_relance.toSave(auteur, action_relance)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_action_relance.toListById(action_relance.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(action_relance.id),'obj': str(action_relance)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_action_relance', args=(action_relance.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_action_relance(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		action_relance = auth.toGetWithRules(dao_action_relance.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if action_relance == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Relance : {}'.format(action_relance),
			'model' : action_relance,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_list_action_relance'))

def get_modifier_action_relance(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_action_relance.toGet(ref)
		context = {
			'title' : 'Modifier Relance',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossier_recouvrements' : Model_Dossier_recouvrement.objects.all(),
			'factures' : Model_Facture.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_action_relance(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_recouvrement_update_action_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		date_action = str(request.POST['date_action'])
		if date_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Date action\' est obligatoire, Veuillez le renseigner SVP!')
		date_action = date(int(date_action[6:10]), int(date_action[3:5]), int(date_action[0:2]))

		montant_action = makeFloat(request.POST['montant_action'])

		type_action = str(request.POST['type_action'])

		observation = str(request.POST['observation'])

		statut_action = makeInt(request.POST['statut_action'])
		if statut_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Statut action\' est obligatoire, Veuillez le renseigner SVP!')

		dossier_recouvrement_id = makeIntId(request.POST['dossier_recouvrement_id'])
		if dossier_recouvrement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Dossier recouvremnet\' est obligatoire, Veuillez le renseigner SVP!')

		facture_id = makeIntId(request.POST['facture_id'])
		if facture_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Facture\' est obligatoire, Veuillez le renseigner SVP!')
		auteur = identite.utilisateur(request)

		action_relance = dao_action_relance.toCreate(designation = designation, date_action = date_action, montant_action = montant_action, type_action = type_action, observation = observation, statut_action = statut_action, dossier_recouvrement_id = dossier_recouvrement_id, facture_id = facture_id)
		saved, action_relance, message = dao_action_relance.toUpdate(id, action_relance)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_action_relance.toListById(action_relance.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_action_relance', args=(action_relance.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_action_relance(request,ref):
	try:
		same_perm_with = 'module_recouvrement_add_action_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_action_relance.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossier_recouvrements' : Model_Dossier_recouvrement.objects.all(),
			'factures' : Model_Facture.objects.all(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_action_relance(request,ref):
	try:
		same_perm_with = 'module_recouvrement_list_action_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		action_relance = auth.toGetWithRules(dao_action_relance.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if action_relance == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Relance : {}'.format(action_relance),
			'model' : action_relance,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleRecouvrement/reporting/print_action_relance.html', 'print_action_relance.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_action_relance(request):
	try:
		same_perm_with = 'module_recouvrement_add_action_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des relances',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_action_relance(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			date_action = str(df['date_action'][i])
			if date_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Date action\' est obligatoire, Veuillez le renseigner SVP!')
			date_action = date(int(date_action[6:10]), int(date_action[3:5]), int(date_action[0:2]))
			montant_action = makeStringFromFloatExcel(df['montant_action'][i])
			type_action = str(df['type_action'][i])
			observation = str(df['observation'][i])
			statut_action = makeInt(df['statut_action'][i])
			if statut_action in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Statut action\' est obligatoire, Veuillez le renseigner SVP!')
			dossier_recouvrement_id = makeIntId(str(df['dossier_recouvrement_id'][i]))
			if dossier_recouvrement_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Dossier recouvremnet\' est obligatoire, Veuillez le renseigner SVP!')
			facture_id = makeIntId(str(df['facture_id'][i]))
			if facture_id in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Facture\' est obligatoire, Veuillez le renseigner SVP!')

			action_relance = dao_action_relance.toCreate(designation = designation, date_action = date_action, montant_action = montant_action, type_action = type_action, observation = observation, statut_action = statut_action, dossier_recouvrement_id = dossier_recouvrement_id, facture_id = facture_id)
			saved, action_relance, message = dao_action_relance.toSave(auteur, action_relance)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_list_action_relance'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# ACTION_RELANCE REPORTING CONTROLLERS
def get_generer_action_relance(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Rapport relance',
			'devises' : dao_devise.toListDevisesActives(),
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/generate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_traiter_action_relance(request, utilisateur = None, modules = [], sous_modules = [], enum_module = vars_module):
	#On recupère et format les inputs reçus
	date_debut = request.POST['date_debut']
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST['date_fin']
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#On récupère les données suivant le filtre défini
	model = Model_Action_relance.objects.filter(creation_date__range = [date_debut, date_fin]).order_by('-creation_date')

	context = {
		'title' : 'Rapport Relance',
		'model' : model,
		'date_debut' : request.POST['date_debut'],
		'date_fin' : request.POST['date_fin'],
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : enum_module,
		'organisation' : dao_organisation.toGetMainOrganisation(),
	}
	return context

def post_generer_action_relance(request):
	try:
		same_perm_with = 'module_recouvrement_get_generer_action_relance'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = post_traiter_action_relance(request, utilisateur, modules, sous_modules)
		template = loader.get_template('ErpProject/ModuleRecouvrement/action_relance/generated.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def post_imprimer_rapport_action_relance(request):
	try:
		context = post_traiter_action_relance(request)
		return weasy_print('ErpProject/ModuleRecouvrement/reporting/rapport_action_relance.html', 'rapport_action_relance.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_get_generer_action_relance'))

# SECTEUR_ACTIVITE CONTROLLERS
from ModuleRecouvrement.dao.dao_secteur_activite import dao_secteur_activite

def get_lister_secteur_activite(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
			if query == '': query = None
		except Exception as e:
			view = 'list'
			query = None

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_secteur_activite.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des secteurs activité',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/secteur_activite/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_secteur_activite(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Secteur Activité',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Secteur_activite(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/secteur_activite/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_secteur_activite(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_recouvrement_add_secteur_activite'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])

		auteur = identite.utilisateur(request)

		secteur_activite = dao_secteur_activite.toCreate(designation = designation, description = description)
		saved, secteur_activite, message = dao_secteur_activite.toSave(auteur, secteur_activite)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_secteur_activite.toListById(secteur_activite.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(secteur_activite.id),'obj': str(secteur_activite)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_secteur_activite', args=(secteur_activite.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_secteur_activite(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		secteur_activite = auth.toGetWithRules(dao_secteur_activite.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if secteur_activite == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Secteur Activité : {}'.format(secteur_activite),
			'model' : secteur_activite,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/secteur_activite/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_list_secteur_activite'))

def get_modifier_secteur_activite(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_secteur_activite.toGet(ref)
		context = {
			'title' : 'Modifier Secteur Activité',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/secteur_activite/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_secteur_activite(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_recouvrement_update_secteur_activite'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])
		auteur = identite.utilisateur(request)

		secteur_activite = dao_secteur_activite.toCreate(designation = designation, description = description)
		saved, secteur_activite, message = dao_secteur_activite.toUpdate(id, secteur_activite)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_secteur_activite.toListById(secteur_activite.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_secteur_activite', args=(secteur_activite.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_secteur_activite(request,ref):
	try:
		same_perm_with = 'module_recouvrement_add_secteur_activite'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_secteur_activite.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/secteur_activite/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_secteur_activite(request,ref):
	try:
		same_perm_with = 'module_recouvrement_list_secteur_activite'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		secteur_activite = auth.toGetWithRules(dao_secteur_activite.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if secteur_activite == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Secteur Activité : {}'.format(secteur_activite),
			'model' : secteur_activite,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleRecouvrement/reporting/print_secteur_activite.html', 'print_secteur_activite.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_secteur_activite(request):
	try:
		same_perm_with = 'module_recouvrement_add_secteur_activite'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des secteurs activité',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/secteur_activite/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_secteur_activite(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			description = str(df['description'][i])

			secteur_activite = dao_secteur_activite.toCreate(designation = designation, description = description)
			saved, secteur_activite, message = dao_secteur_activite.toSave(auteur, secteur_activite)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_list_secteur_activite'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

# PROFIL_RECOUVREMENT CONTROLLERS
from ModuleRecouvrement.dao.dao_profil_recouvrement import dao_profil_recouvrement

def get_lister_profil_recouvrement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		try:
			view = str(request.GET.get('view','list'))
			query = str(request.GET.get('q',''))
			if query == '': query = None
		except Exception as e:
			view = 'list'
			query = None

		#*******Filtre sur les règles **********#
		model = auth.toListWithRules(dao_profil_recouvrement.toList(query), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des profils recouvrement',
			'model' : model,
			'view' : view,
			'query' : query,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/profil_recouvrement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_creer_profil_recouvrement(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		context = {
			'title' : 'Créer un nouvel objet Profil recouvrement',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'model' : Model_Profil_recouvrement(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/profil_recouvrement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_profil_recouvrement(request):
	sid = transaction.savepoint()
	try:
		same_perm_with = 'module_recouvrement_add_profil_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])

		auteur = identite.utilisateur(request)

		profil_recouvrement = dao_profil_recouvrement.toCreate(designation = designation, description = description)
		saved, profil_recouvrement, message = dao_profil_recouvrement.toSave(auteur, profil_recouvrement)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_profil_recouvrement.toListById(profil_recouvrement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la création', msg = 'Vous n\'êtes pas habilité(e) de créer cet objet avec certaines informations que vous avez saisies !')

		if 'isPopup' in request.POST:
			popup_response_data = json.dumps({'value': str(profil_recouvrement.id),'obj': str(profil_recouvrement)})
			return TemplateResponse(request, 'ErpProject/ErpBackOffice/popup_response.html', { 'popup_response_data': popup_response_data })

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_profil_recouvrement', args=(profil_recouvrement.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_details_profil_recouvrement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		profil_recouvrement = auth.toGetWithRules(dao_profil_recouvrement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if profil_recouvrement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Profil recouvrement : {}'.format(profil_recouvrement),
			'model' : profil_recouvrement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/profil_recouvrement/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_recouvrement_list_profil_recouvrement'))

def get_modifier_profil_recouvrement(request,ref):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request)
		if response != None: return response

		ref = int(ref)
		model = dao_profil_recouvrement.toGet(ref)
		context = {
			'title' : 'Modifier Profil recouvrement',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/profil_recouvrement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_profil_recouvrement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		same_perm_with = 'module_recouvrement_update_profil_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response


		designation = str(request.POST['designation'])
		if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')

		description = str(request.POST['description'])
		auteur = identite.utilisateur(request)

		profil_recouvrement = dao_profil_recouvrement.toCreate(designation = designation, description = description)
		saved, profil_recouvrement, message = dao_profil_recouvrement.toUpdate(id, profil_recouvrement)

		if saved == False: raise Exception(message)

		#*******Filtre sur les règles **********#
		model = auth.toGetWithRules(dao_profil_recouvrement.toListById(profil_recouvrement.id), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if model == None: 
			transaction.savepoint_rollback(sid)
			return auth.toReturnFailed(request, 'Erreur: Violation de règle sur la modification', msg = 'Vous n\'êtes pas habilité(e) de modifier cet objet avec certaines informations que vous avez saisies !')

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'La modification est effectuée avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_detail_profil_recouvrement', args=(profil_recouvrement.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)

def get_dupliquer_profil_recouvrement(request,ref):
	try:
		same_perm_with = 'module_recouvrement_add_profil_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)
		model = dao_profil_recouvrement.toGet(ref)
		context = {
			'title' : 'Créer nouvel objet',
			'model':model,
			'utilisateur': utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/profil_recouvrement/duplicate.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_imprimer_profil_recouvrement(request,ref):
	try:
		same_perm_with = 'module_recouvrement_list_profil_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		ref = int(ref)

		#*******Filtre sur les règles **********#
		profil_recouvrement = auth.toGetWithRules(dao_profil_recouvrement.toListById(ref), permission, groupe_permissions, utilisateur)
		#******* End Regle *******************#

		if profil_recouvrement == None:  return HttpResponseRedirect(reverse('backoffice_erreur_autorisation'))

		context = {
			'title' : 'Détails sur l\'objet Profil recouvrement : {}'.format(profil_recouvrement),
			'model' : profil_recouvrement,
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation': dao_organisation.toGetMainOrganisation(),
		}

		return weasy_print('ErpProject/ModuleRecouvrement/reporting/print_profil_recouvrement.html', 'print_profil_recouvrement.pdf', context)
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_upload_profil_recouvrement(request):
	try:
		same_perm_with = 'module_recouvrement_add_profil_recouvrement'
		modules, sous_modules, utilisateur, groupe_permissions, permission, actions, response = auth.toGetAuthPerm(request, same_perm_with)
		if response != None: return response

		context = {
			'title' : 'Import de la liste des profils recouvrement',
			'utilisateur' : utilisateur,
			'user_actions': actions,
			'isPopup': True if 'isPopup' in request.GET else False,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : vars_module,
			'organisation' : dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template('ErpProject/ModuleRecouvrement/profil_recouvrement/upload.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_upload_profil_recouvrement(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		file_name = ''
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES['file_upload']
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + '.xlsx')
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ''
		sheet = str(request.POST['sheet'])

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna('') #Replace all nan value

		auteur = identite.utilisateur(request)

		for i in df.index:
			designation = str(df['designation'][i])
			if designation in (None, '') : return auth.toReturnFailed(request, 'Champ obligatoire non saisi', msg = 'Le Champ \'Désignation\' est obligatoire, Veuillez le renseigner SVP!')
			description = str(df['description'][i])

			profil_recouvrement = dao_profil_recouvrement.toCreate(designation = designation, description = description)
			saved, profil_recouvrement, message = dao_profil_recouvrement.toSave(auteur, profil_recouvrement)

			if saved == False: raise Exception(message)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'Les enregistrements se sont effectué avec succès!')
		return HttpResponseRedirect(reverse('module_recouvrement_list_profil_recouvrement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e)