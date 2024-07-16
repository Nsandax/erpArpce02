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

from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ErpBackOffice.dao.dao_fourniture import dao_fourniture
from ErpBackOffice.dao.dao_bon_special import dao_bon_special
from ErpBackOffice.dao.dao_item_bon_special import dao_item_bon_special
from ModuleInventaire.dao.dao_document_bon_entree import dao_document_bon_entree

from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ErpBackOffice.dao.dao_wkf_historique_bon_entree_depot import dao_wkf_historique_bon_entree_depot

from ErpBackOffice.dao.dao_ligne_fourniture import dao_ligne_fourniture
from ModuleAchat.dao.dao_stock_article import dao_stock_article
from ModuleInventaire.dao.dao_mouvement_stock import dao_mouvement_stock

#
from ModuleStock.dao.dao_entrepot import dao_entrepot
from ModuleStock.dao.dao_type_emplacement import dao_type_emplacement
from ModuleStock.dao.dao_emplacementstock import dao_emplacementstock
from ModuleStock.dao.dao_stockage import dao_stockage
from ModuleStock.dao.dao_type_operation_stock import dao_type_operation_stock
from ModuleStock.dao.dao_statut_operation_stock import dao_statut_operation_stock
from ModuleStock.dao.dao_operation_stock import dao_operation_stock
from ModuleStock.dao.dao_ligne_operation_stock import dao_ligne_operation_stock
from ModuleStock.dao.dao_type_mvt_stock import dao_type_mvt_stock
from ModuleStock.dao.dao_mvt_stock import dao_mvt_stock
from ModuleStock.dao.dao_rebut import dao_rebut
from ModuleStock.dao.dao_statut_ajustement import dao_statut_ajustement
from ModuleStock.dao.dao_ajustement import dao_ajustement
from ModuleStock.dao.dao_ligne_ajustement import dao_ligne_ajustement

#LOGGING
import logging, inspect, unidecode
from ModuleStock.models import *
monLog = logging.getLogger("logger")
module= "ModuleStock"
var_module_id = 23
vars_module = {"name" : "MODULE_STOCK", "value" : 13 }


def get_index(request):
	# try:
	permission_number = 1035
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	# modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(var_module_id, request)
	if response != None:
		return response

	#*******Filtre sur les règles **********#
	# print('*******FILTRE WORK**********')
	model = dao_model.toListModel(dao_stockage.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
	# #print('******* End Regle *******************')
	# print('*******BEFORE CONTENT**********')

	context = {
		"title" : "Tableau de Bord",
		"utilisateur" : utilisateur,
		"organisation": dao_organisation.toGetMainOrganisation(),
		"sous_modules":sous_modules,
		"modules" : modules,
		"module" : vars_module,
		'actions':auth.toGetActions(modules,utilisateur),
		'model' : model,
		"utilisateur" : identite.utilisateur(request),
		# "modules" : dao_module.toListModulesInstalles(),
		# "module" : ErpModule.MODULE_STOCK,
		"menu" : 13,
	}
	# print('*******AFTER CONTENT**********')

	template = loader.get_template("ErpProject/ModuleStock/index.html")
	return HttpResponse(template.render(context, request))
	# except Exception as e:
	# 	print(e)
	# 	return auth.toReturnFailed(request, e)


def get_lister_entrepot(request):
	try:
		permission_number = 990
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_entrepot.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des entrepots',
		'model' : model,
		'utilisateur': utilisateur,
		'modules' : dao_module.toListModulesInstalles(),
		"module" : vars_module,
		'menu' : 1,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"sous_modules":sous_modules,
		"modules" : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'view': view,
		}
		template = loader.get_template('ErpProject/ModuleStock/entrepot/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def get_creer_entrepot(request):
	try:
		permission_number = 991
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		unite_fonctionnelle = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		context ={'title' : 'Nouvel entrepot','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"sous_modules":sous_modules,'services':unite_fonctionnelle,
		"modules" : modules,'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/entrepot/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_entrepot(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		designation_court = request.POST['designation_court']

		services_ref_id = int(request.POST['services_ref_id'])
		auteur = identite.utilisateur(request)
		est_principal = False
		if "est_principal" in request.POST : est_principal = True

		entrepot=dao_entrepot.toCreate(designation,designation_court,est_principal,services_ref_id)
		entrepot=dao_entrepot.toSave(auteur, entrepot)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_entrepot'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_entrepot'))


def get_details_entrepot(request,ref):
	try:
		permission_number = 990
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		entrepot=dao_entrepot.toGet(ref)
		template = loader.get_template('ErpProject/ModuleStock/entrepot/item.html')
		context ={'title' : 'Details d\'un entrepot','entrepot' : entrepot,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"sous_modules":sous_modules,
		"modules" : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_entrepot'))

def get_modifier_entrepot(request,ref):
	try:
		permission_number = 992
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		ref = int(ref)
		unite_fonctionnelle = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		model = dao_entrepot.toGet(ref)
		context ={'title' : 'Modifier Entrepot','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
		'actions':auth.toGetActions(modules,utilisateur),'organisation': dao_organisation.toGetMainOrganisation(),
		'sous_modules':sous_modules,"modules" : modules,'service':unite_fonctionnelle,
		}
		template = loader.get_template('ErpProject/ModuleStock/entrepot/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_entrepot(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		designation_court = request.POST['designation_court']
		# est_principal = request.POST['est_principal']
		services_ref_id = request.POST['services_ref_id']
		auteur = identite.utilisateur(request)

		est_principal = False
		if "est_principal" in request.POST : est_principal = True

		entrepot=dao_entrepot.toCreate(designation,designation_court,est_principal,services_ref_id)
		entrepot=dao_entrepot.toUpdate(id, entrepot)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_Stock_list_entrepot'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_entrepot'))

#TYPE EMPLACEMENT
def get_lister_type_emplacement(request):
	try:
		permission_number = 993
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_type_emplacement.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		dao_type_emplacement
		# print('MODEL', dao_type_emplacement.toList())
		# print('TYPE EMPL', Model_Type_Emplacement.objects.all())
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste de Type Emplacement','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),'menu' : 1,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"sous_modules":sous_modules,
		"modules" : modules,
		"module" : vars_module,
		'actions':auth.toGetActions(modules,utilisateur),
		'view' : view,
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_type_emplacement(request):
	try:
		permission_number = 995
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context ={'title' : 'Nouveau Type Emplacement','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"sous_modules":sous_modules,
		"modules" : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print(e)
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_type_emplacement(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		type_emplacement=dao_type_emplacement.toCreate(designation)
		type_emplacement=dao_type_emplacement.toSave(auteur, type_emplacement)
		# print(type_emplacement)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_type_emplacement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_type_emplacement'))


def get_details_type_emplacement(request,ref):
	try:
		permission_number = 993
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		type_emplacement=dao_type_emplacement.toGet(ref)
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/item.html')
		context ={'title' : 'Details d\'un Type Emplacement','type_emplacement' : type_emplacement,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_type_emplacement'))

def get_modifier_type_emplacement(request,ref):
	try:
		permission_number = 994
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		ref = int(ref)
		model = dao_type_emplacement.toGet(ref)
		context ={'title' : 'Modifier Type Emplacement','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_emplacement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_type_emplacement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		type_emplacement=dao_type_emplacement.toCreate(designation)
		type_emplacement=dao_type_emplacement.toUpdate(id, type_emplacement)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_type_emplacement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_type_emplacement'))


#EMPLACEMENT
def get_lister_emplacementstock(request):
	try:
		permission_number = 996
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_emplacementstock.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste d\'emplacement de stock','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'view': view,
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacementstock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def get_creer_emplacementstock(request):
	try:
		permission_number = 997
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		TypeEmplacement = dao_type_emplacement.toList()
		entrepot = dao_entrepot.toList()
		model = dao_emplacementstock.toList()

		context ={'title' : 'Nouvel emplacement de stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
		'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,'TypeEmplacement':TypeEmplacement,
			"modules" : modules,'entrepot':entrepot,'model':model,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacementstock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_emplacementstock(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		type_id = int(request.POST['type_id'])
		entrepot_id = int(request.POST['entrepot_id'])
		couloir = request.POST['couloir']
		rayon = request.POST['rayon']
		hauteur = request.POST['hauteur']
		auteur = identite.utilisateur(request)

		# parent_id = ""
		# if 'parent_id' in request.POST: parent_id = int(request.POST['parent_id'])

		emplacementstock=dao_emplacementstock.toCreate(designation,type_id,entrepot_id,couloir,rayon,hauteur)
		emplacementstock=dao_emplacementstock.toSave(auteur, emplacementstock)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_emplacementstock'))
	except Exception as e:
		print('ERREUR', e)
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_emplacementstock'))

def get_details_emplacementstock(request,ref):
	try:
		permission_number = 996
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		emplacementstock=dao_emplacementstock.toGet(ref)
		template = loader.get_template('ErpProject/ModuleStock/emplacementstock/item.html')
		context ={'title' : 'Detail d\'un emplacement stock','emplacementstock' : emplacementstock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_emplacementstock'))

def get_modifier_emplacementstock(request,ref):
	try:
		permission_number = 998
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_emplacementstock.toGet(ref)
		TypeEmplacement = dao_type_emplacement.toList()
		entrepot = dao_entrepot.toList()
		context ={'title' : 'Modifier Emplacement stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,'entrepot':entrepot,
			"modules" : modules,'TypeEmplacement':TypeEmplacement,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/emplacementstock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_emplacementstock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		type_id = int(request.POST['type_id'])
		entrepot_id = int(request.POST['entrepot_id'])
		couloir = request.POST['couloir']
		rayon = request.POST['rayon']
		hauteur = request.POST['hauteur']
		auteur = identite.utilisateur(request)

		emplacementstock=dao_emplacementstock.toCreate(designation,type_id,entrepot_id,couloir,rayon,hauteur)
		emplacementstock=dao_emplacementstock.toUpdate(id, emplacementstock)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_emplacementstock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_emplacementstock'))

# RECEPTION ARTICLES


# BON ACHAT EN ATTENTE DE RECEPTION CONTROLLER
def get_lister_bons_reception(request):
    permission_number = 1000
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #model = dao_fourniture.toListBonsAchatEnAttente()

    # model = dao_fourniture.toListBonsAchatEnAttente()
    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_fourniture.toListBonsAchatEnAttente(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

    context = {
        'modules':modules,'sous_modules':sous_modules,
        'title' : "Liste des bons à receptionner",
        'model' : model,
        "utilisateur" : utilisateur,
        "modules" : modules,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "module" : vars_module,
        'menu' : 1
    }
    template = loader.get_template("ErpProject/ModuleStock/bons/list.html")
    return HttpResponse(template.render(context, request))

def get_details_bon_reception(request, ref):

    try:
        permission_number = 1000
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)
        bon_reception = dao_fourniture.toGetFourniture(ref)
        lignes = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_reception)

        context = {
            'modules':modules,'sous_modules':sous_modules,
            'title' : "Bon de commande N°%s" % bon_reception.numero_reception,
            'model' : bon_reception,
            'lignes' : lignes,
            "historique": historique,
            "etapes_suivantes": etapes_suivantes,
            "signee": signee,
            "content_type_id": content_type_id,
            "documents": documents,
            "roles": groupe_permissions,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : vars_module,
            'menu' : 1
        }
        template = loader.get_template("ErpProject/ModuleStock/bons/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_stock_list_bon_receptions'))


def get_receptionner_bon_reception(request, ref):

    try:
        permission_number = 1000
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response

        ref = int(ref)
        bon_reception = dao_fourniture.toGetFourniture(ref)
        if bon_reception.est_realisee == True : return HttpResponseRedirect(reverse('module_achat_list_bons_achat'))

        lignes = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        context = {
            'title' : "Bon de reception relatif au bon de commande N°%s" % bon_reception.numero_reception,
            'model' : bon_reception,
            'lignes' : lignes,
            'agents' : dao_employe.toListEmployesActifs(),
            "utilisateur" : utilisateur,
            'sous_modules':sous_modules,
            'actions':auth.toGetActions(modules,utilisateur),
		    'organisation': dao_organisation.toGetMainOrganisation(),
            "modules" : modules,
            "module" : vars_module,
            'menu' : 1
        }
        template = loader.get_template("ErpProject/ModuleStock/bons/receive.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_stock_list_bon_receptions'))

@transaction.atomic
def post_receptionner_bon_reception(request):
    sid = transaction.savepoint()
    bon_id = int(request.POST["bon_id"])
    try:
        #Test de la validité de la date en fonction de l'activation d'une période dans un module
        if not auth.toPostValidityDate(var_module_id, datetime.datetime.now().strftime("%d/%m/%Y")): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

        auteur = identite.utilisateur(request)
        receveur_id = int(request.POST["receveur_id"])
        reference_document = request.POST["reference_document"]
        commentaire = request.POST["commentaire"]
        est_realisee = True


        bon_reception = dao_fourniture.toGetFourniture(bon_id)
        ##print("Bon achat {0} recupere ".format(bon_reception.id))
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        for i in range(0, len(list_ligne_id)) :
            ligne_id = int(list_ligne_id[i])
            quantite_fournie = makeFloat(list_quantite_fournie[i])

            #On recupère l'objet de la ligne fourniture
            ligne_fourniture = dao_ligne_fourniture.toGetLigneFourniture(ligne_id)
            ##print("Ligne fourniture {0} recupere ".format(ligne_fourniture.id))
            #Si la quantité demandée est superieure à la somme des quantitées déjà fournies, on ne receptionne pas pcq on n'a pas encore tout reçu
            #if ligne_fourniture.quantite_demande > ligne_fourniture.quantite_fournie + quantite_fournie : est_realisee = False

            # On ajoute la nouvelle quantité reçue
            ligne_fourniture.quantite_fournie = ligne_fourniture.quantite_fournie + quantite_fournie
            ligne_fourniture.save()
            ##print("Ligne fourniture {0} modifie ".format(ligne_fourniture.id))

            # On recuper le stock de l'article de la ligne du bon d'achat (ici l'emplacement d'entrée)
            stock = dao_stock_article.toGetStockArticle(ligne_fourniture.stock_article_id)
            ##print("Stock article {0} recupere ".format(stock.id))

            # AUGMENTATION DE LA QUANTITE DU STOCK CONCERNE (Emplacement d'entrée)
            stock.quantite_disponible = stock.quantite_disponible + quantite_fournie
            loud = dao_stock_article.toUpdateStockArticle(ligne_fourniture.stock_article_id, stock)
            ##print("Stock article {0} recupere ".format(stock.id))

            #ENREGISTRER LE MOUVEMENT
            if quantite_fournie > 0:
                mouvement_stock = dao_mouvement_stock.toCreateMouvementStock(quantite_fournie,"","ACHAT",ligne_fourniture.stock_article_id,None,None,bon_id)
                mouvement_stock = dao_mouvement_stock.toSaveMouvementStock(auteur, mouvement_stock)
                ##print("Mouvement stock {0} cree ".format(mouvement_stock.id))

        bon_reception.est_realisee = est_realisee
        bon_reception.receveur_id = receveur_id
        bon_reception.save()
        ##print("Bon Achat {0} modifie ".format(bon_reception.id))

        # ON CREE LE BON ENTREE STOCK (Model_Bon)
        lignes_fourniture = dao_ligne_fourniture.toListLignesFourniture(bon_reception.id)
        #dao_bon_special.toCreateBonSpecial("",)
        bon_entree = dao_bon_special.toCreateBonSpecial("",  None,bon_reception.id, None, reference_document, bon_reception.devise_id, bon_reception.receveur_id, commentaire)
        bon_entree = dao_bon_special.toSaveBonSpecial(auteur, bon_entree)

        # WORKFLOWS INITIALS
        type_document = "Bon d'entrée depot"
        wkf_task.initializeWorkflow(auteur,bon_entree,type_document)

        #Gref, Bon reception passe d'article
        wkf_task.passingStepWorkflow(auteur,bon_reception)


        ##print("Bon Special {0} cree ".format(bon_entree.id))
        #On enregistre le ligne du bon d'entree
        for item in lignes_fourniture:
            ##print("before ligne", lignes_fourniture)
            ligne_bon_entree = dao_item_bon_special.toCreateItemBonSpecial(bon_entree.id, item.article_id, item.quantite_demande, item.quantite_fournie, item.unite_achat)
            ##print("after ligne")
            ligne_bon_entree = dao_item_bon_special.toSaveItemBonSpecial(auteur,ligne_bon_entree)
            ##print("Ligne bon d'entrée {0} cree ".format(ligne_bon_entree.id))



        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('module_stock_details_bons_entrees', args=(bon_entree.id,)))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_stock_receive_bon_reception', args=(bon_entree.id,)))


@transaction.atomic
def post_workflow_reception(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        etape_id = request.POST["etape_id"]
        demande_id = request.POST["doc_id"]

        ##print("print 1 %s %s %s" % (utilisateur_id, etape_id, demande_id))

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        demande_achat = dao_demande_achat.toGetDemande(demande_id)

        ##print("print 2 %s %s %s " % (employe, etape, demande_achat))

        transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(demande_achat.statut_id)
        for item in transitions_etapes_suivantes:

            # Gestion des transitions dans le document
            demande_achat.statut_id = etape.id
            demande_achat.etat = etape.designation
            demande_achat.save()

        historique = dao_wkf_historique_demande.toCreateHistoriqueWorkflow(employe.id, etape.id, demande_achat.id)
        historique = dao_wkf_historique_demande.toSaveHistoriqueWorkflow(historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            ##print("OKAY")
            return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande_id,)))

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        return HttpResponseRedirect(reverse('module_achat_add_bon_achat'))


# BON ENTREE DEPOT CONTROLLER
def get_lister_bons_entrees(request):
    permission_number = 1000
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    #*******Filtre sur les règles **********#
    model = dao_model.toListModel(dao_bon_special.toListBonsEntrees(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
    try:
	    view = str(request.GET.get("view","list"))
    except Exception as e:
	    view = "list"

    #Pagination
    model = pagination.toGet(request, model)

    context = {
        'modules':modules,
        'sous_modules':sous_modules,
        'title' : "Liste des bons des réceptions",
        'model' : model,
        "utilisateur" : utilisateur,
        'view' : view,
        'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
        "modules" : modules,
        "module" : vars_module,
        'menu' : 3
    }
    template = loader.get_template("ErpProject/ModuleStock/bons_entrees/list.html")
    return HttpResponse(template.render(context, request))


def get_details_bons_entrees(request, ref):
    permission_number = 1000
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
    if response != None:
        return response

    try:
        ref = int(ref)
        bon_entree = dao_bon_special.toGetBonSpecial(ref)
        lignes = dao_item_bon_special.toListItemBons(bon_entree.id)
        historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_entree)
        context = {
            'modules':modules,
            'sous_modules':sous_modules,
            'title' : "Bon de reception N°%s" % bon_entree.numero,
            'model' : bon_entree,
            'lignes' : lignes,
            'signee' : signee,
            'historique':historique,
            'roles':groupe_permissions,
            'content_type_id':content_type_id,
            'documents': documents,
            'etapes_suivantes':transition_etape_suivant,
            "utilisateur" : utilisateur,
            'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
           	"module" : vars_module,
            'menu' : 3
        }
        template = loader.get_template("ErpProject/ModuleStock/bons_entrees/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_stock_list_bons_entrees'))


@transaction.atomic
def post_workflow_bon_entree_depot(request):
    sid = transaction.savepoint()
    try:
        utilisateur_id = request.user.id
        auteur = identite.utilisateur(request)
        base_dir = settings.BASE_DIR
        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        etape_id = request.POST["etape_id"]
        entree_id = request.POST["doc_id"]

        ##print("print 1 %s %s %s" % (utilisateur_id, etape_id, entree_id))

        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        bon_entree = dao_bon_special.toGetBonSpecial(entree_id)

        ##print("print 2 %s %s %s " % (employe, etape, bon_entree))

        transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_entree.statut_id)
        for item in transitions_etapes_suivantes:

            if item.condition.designation == "Upload":
                ##print("Upload")
                if 'file_upload' in request.FILES:
                    nom_fichier = request.FILES['file_upload']
                    doc = dao_document.toUploadDocument(auteur, nom_fichier, bon_entree)

                    bon_entree.statut_id = etape.id
                    bon_entree.etat = etape.designation
                    bon_entree.save()
                    document = dao_document_bon_entree.toCreateDocument("Bon de reception",doc.url_document, bon_entree.etat,entree_id)
                    document = dao_document_bon_entree.toSaveDocument(auteur, document)

                    ##print("docu saved")
                else:
                    pass

            else:
                # Gestion des transitions dans le document
                bon_entree.statut_id = etape.id
                bon_entree.etat = etape.designation
                bon_entree.save()

        historique = dao_wkf_historique_bon_entree_depot.toCreateHistoriqueWorkflow(employe.id, etape.id, bon_entree.id)
        historique = dao_wkf_historique_bon_entree_depot.toSaveHistoriqueWorkflow(historique)

        if historique != None :
            transaction.savepoint_commit(sid)
            #return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
            ##print("OKAY")
            return HttpResponseRedirect(reverse('module_stock_details_bons_entrees', args=(entree_id,)))
        else:
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_stock_details_bons_entrees', args=(entree_id,)))

    except Exception as e:
        ##print("ERREUR")
        ##print(e)
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_stock_list_bons_entrees'))



def get_to_asset_of_bons_entrees(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["doc_id"])
    try:
        permission_number = 1000
        modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
        if response != None:
            return response



        #Aux allures de Get
        # modules = dao_module.toListModulesInstalles()
        # utilisateur = identite.utilisateur(request)
        #Fin allure Get

        # auteur = identite.utilisateur(request)
        #responsable_id = int(request.POST["responsable_id"])
        #agent_id = int(request.POST["agent_id"])
        est_realisee = True

        #bon_transfert = dao_bon_transfert.toGetBonTransfert(ordre_id)
        bon_entree = dao_bon_special.toGetBonSpecial(ordre_id)
        #operation_stock = dao_operation_stock.toGetOperationStock(bon_transfert.operation_stock_id)
        #emplacement_destination = dao_emplacement.toGetEmplacement(bon_transfert.emplacement_destination_id)
        list_ligne_id = request.POST.getlist('ligne_id', None)
        list_quantite_fournie = request.POST.getlist("quantite_fournie", None)

        is_done = True
        if is_done == True :

            lignes = dao_item_bon_special.toListItemBons(ordre_id)
            context = {
                'modules':modules,'sous_modules':sous_modules,
                'title' : "Enregistrer les assets relatifs au bon N°%s" % bon_entree.numero,
                'model' : bon_entree,
                'lignes' : lignes,
                "utilisateur" : utilisateur,
                "module" : vars_module,
                'actions':auth.toGetActions(modules,utilisateur),
                'sous_modules':sous_modules,
		        'organisation': dao_organisation.toGetMainOrganisation(),
                "modules": modules,
                'roles':groupe_permissions,
                'menu' : 11
            }

            template = loader.get_template("ErpProject/ModuleStock/bons_entrees/asset.html")
            return HttpResponse(template.render(context, request))
        else:

            return HttpResponseRedirect(reverse('module_stock_details_bons_entrees', args=(ordre_id,)))
    except Exception as e:
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_stock_details_bons_entrees', args=(ordre_id,)))

@transaction.atomic
def post_to_asset_of_bons_entrees(request):
    sid = transaction.savepoint()
    ordre_id = int(request.POST["ordre_id"])
    try:
        auteur = identite.utilisateur(request)
        est_realisee = True
        document = request.POST["document"]

        bon_entree = dao_bon_special.toGetBonSpecial(ordre_id)

		# operation = Model_Operation_Stock()

        #Flow
        wkf_task.passingStepWorkflow(auteur,bon_entree)
        #Traitement des assets
        list_numero_serie = request.POST.getlist('numero_serie', None)
        list_description = request.POST.getlist('description', None)
        list_article_id = request.POST.getlist('article_id', None)
        type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
        emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
        for i in range(0, len(list_numero_serie)):
            num_serie = list_numero_serie[i]
            descript = list_description[i]
            art_id = list_article_id[i]
            article = dao_article.toGetArticle(art_id)
            asset = dao_asset.toCreateAsset(num_serie,"ARTICLES",art_id,None,emplacement.id,descript)
            asset = dao_asset.toSaveAsset(auteur,asset)
            asset.bon_entree = bon_entree
            asset.bon_reception = bon_entree.bon_reception
            asset.save()
            asset_historique = dao_asset_historique.toCreateAssetHistorique(bon_entree.numero,document,asset.id,bon_entree,None,True)
            asset_historique = dao_asset_historique.toSaveAssetHistorique(auteur,asset_historique)

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(ordre_id,)))

    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request,e)
        return HttpResponseRedirect(reverse('module_inventaire_details_bons_entrees', args=(ordre_id,)))


#STOCKAGE
def get_lister_stockage(request):
	try:
		permission_number = 999
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_stockage.toListStockage(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des stockages','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_stockage(request):
	try:
		permission_number = 1000
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouveau stockage','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_stockage(request):
	sid = transaction.savepoint()
	try:
		emplacement_id = request.POST['emplacement_id']
		article_id = request.POST['article_id']
		quantite = request.POST['quantite']
		unite_id = request.POST['unite_id']
		auteur = identite.utilisateur(request)

		stockage=dao_stockage.toCreateStockage(emplacement_id,article_id,quantite,unite_id)
		stockage=dao_stockage.toSaveStockage(auteur, stockage)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_stockage'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_stockage'))


def get_details_stockage(request,ref):
	try:
		permission_number = 999
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		stockage=dao_stockage.toGetStockage(ref)
		template = loader.get_template('ErpProject/ModuleStock/stockage/item.html')
		context ={'title' : 'Detail d\'un stockage','stockage' : stockage,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_stockage'))


def get_modifier_stockage(request,ref):
	try:
		permission_number = 1001
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_stockage.toGetStockage(ref)
		context ={'title' : 'Modifier Stockage','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/stockage/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_stockage(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		emplacement_id = request.POST['emplacement_id']
		article_id = request.POST['article_id']
		quantite = request.POST['quantite']
		unite_id = request.POST['unite_id']
		auteur = identite.utilisateur(request)

		stockage=dao_stockage.toCreateStockage(emplacement_id,article_id,quantite,unite_id)
		stockage=dao_stockage.toUpdateStockage(id, stockage)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_stockage'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_stockage'))

# TYPE OPERATION STOCK
def get_lister_type_operation_stock(request):
	try:
		permission_number = 1002
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_type_operation_stock.toListType_operation_stock(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste de type d\'operation stock','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_operation_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def get_creer_type_operation_stock(request):
	try:
		permission_number = 1003
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouveau Type operation Stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_operation_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_type_operation_stock(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		type_operation_stock=dao_type_operation_stock.toCreateType_operation_stock(designation)
		type_operation_stock=dao_type_operation_stock.toSaveType_operation_stock(auteur, type_operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_type_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_type_operation_stock'))


def get_details_type_operation_stock(request,ref):
	try:
		permission_number = 1002
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		type_operation_stock=dao_type_operation_stock.toGetType_operation_stock(ref)
		template = loader.get_template('ErpProject/ModuleStock/type_operation_stock/item.html')
		context ={'title' : 'Details d une type_operation_stock','type_operation_stock' : type_operation_stock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_type_operation_stock'))

def get_modifier_type_operation_stock(request,ref):
	try:
		permission_number = 1004
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_type_operation_stock.toGetType_operation_stock(ref)
		context ={'title' : 'Modifier Type Operation stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_operation_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_type_operation_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		type_operation_stock=dao_type_operation_stock.toCreateType_operation_stock(designation)
		type_operation_stock=dao_type_operation_stock.toUpdateType_operation_stock(id, type_operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_type_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_type_operation_stock'))

#STATUT OPERATION
def get_lister_statut_operation_stock(request):
	try:
		permission_number = 1005
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_statut_operation_stock.toListStatut_operation_stock(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste de statut d\'operation stock','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_statut_operation_stock(request):
	try:
		permission_number = 1006
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouveau statut operation stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_statut_operation_stock(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		statut_operation_stock=dao_statut_operation_stock.toCreateStatut_operation_stock(designation)
		statut_operation_stock=dao_statut_operation_stock.toSaveStatut_operation_stock(auteur, statut_operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_statut_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_statut_operation_stock'))

def get_details_statut_operation_stock(request,ref):
	try:
		permission_number = 1005
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		statut_operation_stock=dao_statut_operation_stock.toGetStatut_operation_stock(ref)
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/item.html')
		context ={'title' : 'Detail d\'un statut Operation_stock','statut_operation_stock' : statut_operation_stock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_modifier_statut_operation_stock(request,ref):
	try:
		permission_number = 1007
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_statut_operation_stock.toGetStatut_operation_stock(ref)
		context ={'title' : 'Modifier Statut Operation stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_operation_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_statut_operation_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		statut_operation_stock=dao_statut_operation_stock.toCreateStatut_operation_stock(designation)
		statut_operation_stock=dao_statut_operation_stock.toUpdateStatut_operation_stock(id, statut_operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_statut_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_statut_operation_stock'))


# OPERATION STOCK
def get_lister_operation_stock(request):
	try:
		permission_number = 1008
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_operation_stock.toListOperation_stock(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)


		context ={'title' : 'Liste d\'operation stock','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_operation_stock(request):
	try:
		permission_number = 1009
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouvelle operation_stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_operation_stock(request):
	sid = transaction.savepoint()
	try:
		numero = request.POST['numero']
		type_id = request.POST['type_id']
		emplacement_id = request.POST['emplacement_id']
		emplacement_destination_id = request.POST['emplacement_destination_id']
		document = request.POST['document']
		statut_id = request.POST['statut_id']
		operation_parent_id = request.POST['operation_parent_id']
		auteur = identite.utilisateur(request)

		operation_stock=dao_operation_stock.toCreateOperation_stock(numero,type_id,emplacement_id,emplacement_destination_id,document,statut_id,operation_parent_id)
		operation_stock=dao_operation_stock.toSaveOperation_stock(auteur, operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_operation_stock'))

def get_details_operation_stock(request,ref):
	try:
		permission_number = 1008
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		operation_stock=dao_operation_stock.toGetOperation_stock(ref)
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/item.html')
		context ={'title' : 'Détail d\'une operation stock','operation_stock' : operation_stock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

def get_modifier_operation_stock(request,ref):
	try:
		permission_number = 1010
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_operation_stock.toGetOperation_stock(ref)
		context ={'title' : 'Modifier Operation Stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/operation_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_operation_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		numero = request.POST['numero']
		type_id = request.POST['type_id']
		emplacement_id = request.POST['emplacement_id']
		emplacement_destination_id = request.POST['emplacement_destination_id']
		document = request.POST['document']
		statut_id = request.POST['statut_id']
		operation_parent_id = request.POST['operation_parent_id']
		auteur = identite.utilisateur(request)

		operation_stock=dao_operation_stock.toCreateOperation_stock(numero,type_id,emplacement_id,emplacement_destination_id,document,statut_id,operation_parent_id)
		operation_stock=dao_operation_stock.toUpdateOperation_stock(id, operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_operation_stock'))


#LIGNE OPERATION
def get_lister_ligne_operation_stock(request):
	try:
		permission_number = 1011
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_ligne_operation_stock.toListLigne_operation_stock(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des lignes d\'operations stocks','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_operation_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def get_creer_ligne_operation_stock(request):
	try:
		permission_number = 1012
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouvelle ligne d\'operation stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_operation_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_ligne_operation_stock(request):
	sid = transaction.savepoint()
	try:
		operation_id = request.POST['operation_id']
		article_id = request.POST['article_id']
		series_id = request.POST['series_id']
		quantite_demandee = request.POST['quantite_demandee']
		quantite_fait = request.POST['quantite_fait']
		prix_unitaire = request.POST['prix_unitaire']
		unite_id = request.POST['unite_id']
		devise_id = request.POST['devise_id']
		description = request.POST['description']
		fait = request.POST['fait']
		auteur = identite.utilisateur(request)

		ligne_operation_stock=dao_ligne_operation_stock.toCreateLigne_operation_stock(operation_id,article_id,series_id,quantite_demandee,quantite_fait,prix_unitaire,unite_id,devise_id,description,fait)
		ligne_operation_stock=dao_ligne_operation_stock.toSaveLigne_operation_stock(auteur, ligne_operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_ligne_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_ligne_operation_stock'))

def get_details_ligne_operation_stock(request,ref):
	try:
		permission_number = 1011
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		ligne_operation_stock=dao_ligne_operation_stock.toGetLigne_operation_stock(ref)
		template = loader.get_template('ErpProject/ModuleStock/ligne_operation_stock/item.html')
		context ={'title' : 'Detail d\'une ligne operation stock','ligne_operation_stock' : ligne_operation_stock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_ligne_operation_stock'))

def get_modifier_ligne_operation_stock(request,ref):
	try:
		permission_number = 1013
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_ligne_operation_stock.toGetLigne_operation_stock(ref)
		context ={'title' : 'Modifier Ligne operation stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_operation_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_ligne_operation_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		operation_id = request.POST['operation_id']
		article_id = request.POST['article_id']
		series_id = request.POST['series_id']
		quantite_demandee = request.POST['quantite_demandee']
		quantite_fait = request.POST['quantite_fait']
		prix_unitaire = request.POST['prix_unitaire']
		unite_id = request.POST['unite_id']
		devise_id = request.POST['devise_id']
		description = request.POST['description']
		fait = request.POST['fait']
		auteur = identite.utilisateur(request)

		ligne_operation_stock=dao_ligne_operation_stock.toCreateLigne_operation_stock(operation_id,article_id,series_id,quantite_demandee,quantite_fait,prix_unitaire,unite_id,devise_id,description,fait)
		ligne_operation_stock=dao_ligne_operation_stock.toUpdateLigne_operation_stock(id, ligne_operation_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_ligne_operation_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_ligne_operation_stock'))


# TYPE MOUVEMENT STOCK
def get_lister_type_mvt_stock(request):
	try:
		permission_number = 1014
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_type_mvt_stock.toListType_mvt_stock(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste de types des mouvements stocks','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_type_mvt_stock(request):
	try:
		permission_number = 1015
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouveau Type de mouvement de stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_type_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		type_mvt_stock=dao_type_mvt_stock.toCreateType_mvt_stock(designation)
		type_mvt_stock=dao_type_mvt_stock.toSaveType_mvt_stock(auteur, type_mvt_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_type_mvt_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_type_mvt_stock'))


def get_details_type_mvt_stock(request,ref):
	try:
		permission_number = 1014
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		type_mvt_stock=dao_type_mvt_stock.toGetType_mvt_stock(ref)
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/item.html')
		context ={'title' : 'Details d\'un Type de mouvement de stock','type_mvt_stock' : type_mvt_stock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_type_mvt_stock'))

def get_modifier_type_mvt_stock(request,ref):
	try:
		permission_number = 1016
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_type_mvt_stock.toGetType_mvt_stock(ref)
		context ={'title' : 'Modifier Type Mouvement stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/type_mvt_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_type_mvt_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		type_mvt_stock=dao_type_mvt_stock.toCreateType_mvt_stock(designation)
		type_mvt_stock=dao_type_mvt_stock.toUpdateType_mvt_stock(id, type_mvt_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_type_mvt_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_type_mvt_stock'))


#MOUVEMENT STOCK
def get_lister_mvt_stock(request):
	try:
		permission_number = 1017
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_mvt_stock.toListMvt_stock(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des Mouvements des stocks','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_mvt_stock(request):
	try:
		permission_number = 1018
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouveau Mouvement de stock','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_mvt_stock(request):
	sid = transaction.savepoint()
	try:
		type_id = request.POST['type_id']
		article_id = request.POST['article_id']
		series_id = request.POST['series_id']
		emplacement_id = request.POST['emplacement_id']
		operation_id = request.POST['operation_id']
		ajustement_id = request.POST['ajustement_id']
		rebut_id = request.POST['rebut_id']
		document = request.POST['document']
		quantite_initiale = request.POST['quantite_initiale']
		unite_initiale_id = request.POST['unite_initiale_id']
		quantite = request.POST['quantite']
		unite_id = request.POST['unite_id']
		est_fabrication = request.POST['est_fabrication']
		est_destruction = request.POST['est_destruction']
		est_ajustement = request.POST['est_ajustement']
		est_rebut = request.POST['est_rebut']
		auteur = identite.utilisateur(request)

		mvt_stock=dao_mvt_stock.toCreateMvt_stock(type_id,article_id,series_id,emplacement_id,operation_id,ajustement_id,rebut_id,document,quantite_initiale,unite_initiale_id,quantite,unite_id,est_fabrication,est_destruction,est_ajustement,est_rebut)
		mvt_stock=dao_mvt_stock.toSaveMvt_stock(auteur, mvt_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_mvt_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_mvt_stock'))

def get_details_mvt_stock(request,ref):
	try:
		permission_number = 1017
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		mvt_stock=dao_mvt_stock.toGetMvt_stock(ref)
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/item.html')
		context ={'title' : 'Detail d\'un Mouvement Stock','mvt_stock' : mvt_stock,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e,reverse('module_Stock_list_mvt_stock'))


def get_modifier_mvt_stock(request,ref):
	try:
		permission_number = 1019
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_mvt_stock.toGetMvt_stock(ref)
		context ={'title' : 'Modifier Mouvement stock','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/mvt_stock/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_mvt_stock(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		type_id = request.POST['type_id']
		article_id = request.POST['article_id']
		series_id = request.POST['series_id']
		emplacement_id = request.POST['emplacement_id']
		operation_id = request.POST['operation_id']
		ajustement_id = request.POST['ajustement_id']
		rebut_id = request.POST['rebut_id']
		document = request.POST['document']
		quantite_initiale = request.POST['quantite_initiale']
		unite_initiale_id = request.POST['unite_initiale_id']
		quantite = request.POST['quantite']
		unite_id = request.POST['unite_id']
		est_fabrication = request.POST['est_fabrication']
		est_destruction = request.POST['est_destruction']
		est_ajustement = request.POST['est_ajustement']
		est_rebut = request.POST['est_rebut']
		auteur = identite.utilisateur(request)

		mvt_stock=dao_mvt_stock.toCreateMvt_stock(type_id,article_id,series_id,emplacement_id,operation_id,ajustement_id,rebut_id,document,quantite_initiale,unite_initiale_id,quantite,unite_id,est_fabrication,est_destruction,est_ajustement,est_rebut)
		mvt_stock=dao_mvt_stock.toUpdateMvt_stock(id, mvt_stock)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_mvt_stock'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_mvt_stock'))


#REBUT
def get_lister_rebut(request):
	try:
		permission_number = 1020
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_rebut.toListRebut(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste de rebut','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_rebut(request):
	try:
		permission_number = 1021
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouvau rebut','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_rebut(request):
	sid = transaction.savepoint()
	try:
		numero = request.POST['numero']
		article_id = request.POST['article_id']
		serie_article_id = request.POST['serie_article_id']
		quantite = request.POST['quantite']
		unite_id = request.POST['unite_id']
		emplacement_id = request.POST['emplacement_id']
		emplacement_rebut_id = request.POST['emplacement_rebut_id']
		document = request.POST['document']
		auteur = identite.utilisateur(request)

		rebut=dao_rebut.toCreateRebut(numero,article_id,serie_article_id,quantite,unite_id,emplacement_id,emplacement_rebut_id,document,)
		rebut=dao_rebut.toSaveRebut(auteur, rebut)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_rebut'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_rebut'))


def get_details_rebut(request,ref):
	try:
		permission_number = 1020
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		rebut=dao_rebut.toGetRebut(ref)
		template = loader.get_template('ErpProject/ModuleStock/rebut/item.html')
		context ={'title' : 'Detail d\'un rebut','rebut' : rebut,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
						'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_rebut'))

def get_modifier_rebut(request,ref):
	try:
		permission_number = 1022
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_rebut.toGetRebut(ref)
		context ={'title' : 'Modifier Rebut','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
						'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/rebut/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_modifier_rebut(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		numero = request.POST['numero']
		article_id = request.POST['article_id']
		serie_article_id = request.POST['serie_article_id']
		quantite = request.POST['quantite']
		unite_id = request.POST['unite_id']
		emplacement_id = request.POST['emplacement_id']
		emplacement_rebut_id = request.POST['emplacement_rebut_id']
		document = request.POST['document']
		auteur = identite.utilisateur(request)

		rebut=dao_rebut.toCreateRebut(numero,article_id,serie_article_id,quantite,unite_id,emplacement_id,emplacement_rebut_id,document,)
		rebut=dao_rebut.toUpdateRebut(id, rebut)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_rebut'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_rebut'))


# STATUT AJUSTEMENT
def get_lister_statut_ajustement(request):
	try:
		permission_number = 1023
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_statut_ajustement.toListStatut_ajustement(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des statuts d\'ajustements','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def get_creer_statut_ajustement(request):
	try:
		permission_number = 1024
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouveau statut d\'ajustement','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_statut_ajustement(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		statut_ajustement=dao_statut_ajustement.toCreateStatut_ajustement(designation)
		statut_ajustement=dao_statut_ajustement.toSaveStatut_ajustement(auteur, statut_ajustement)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_statut_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_statut_ajustement'))

def get_details_statut_ajustement(request,ref):
	try:
		permission_number = 1023
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		statut_ajustement=dao_statut_ajustement.toGetStatut_ajustement(ref)
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/item.html')
		context ={'title' : 'Detail d\'un statut d\'ajustement','statut_ajustement' : statut_ajustement,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_statut_ajustement'))

def get_modifier_statut_ajustement(request,ref):
	try:
		permission_number = 1025
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_statut_ajustement.toGetStatut_ajustement(ref)
		context ={'title' : 'Modifier Statut d\'ajustement','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/statut_ajustement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_statut_ajustement'))

@transaction.atomic
def post_modifier_statut_ajustement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		statut_ajustement=dao_statut_ajustement.toCreateStatut_ajustement(designation)
		statut_ajustement=dao_statut_ajustement.toUpdateStatut_ajustement(id, statut_ajustement)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_statut_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_statut_ajustement'))


#AJUSTEMENT
def get_lister_ajustement(request):
	try:
		permission_number = 1026
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_ajustement.toListAjustement(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des ajustements','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def get_creer_ajustement(request):
	try:
		permission_number = 1027
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouvel ajustement','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_ajustement(request):
	sid = transaction.savepoint()
	try:
		reference = request.POST['reference']
		emplacement_id = request.POST['emplacement_id']
		statut_id = request.POST['statut_id']
		inventaire_de = request.POST['inventaire_de']
		document = request.POST['document']
		auteur = identite.utilisateur(request)

		ajustement=dao_ajustement.toCreateAjustement(reference,emplacement_id,statut_id,inventaire_de,document)
		ajustement=dao_ajustement.toSaveAjustement(auteur, ajustement)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_ajustement'))

def get_details_ajustement(request,ref):
	try:
		permission_number = 1027
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		ajustement=dao_ajustement.toGetAjustement(ref)
		template = loader.get_template('ErpProject/ModuleStock/ajustement/item.html')
		context ={'title' : 'Detail d\'un ajustement','ajustement' : ajustement,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_ajustement'))

def get_modifier_ajustement(request,ref):
	try:
		permission_number = 1028
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_ajustement.toGetAjustement(ref)
		context ={'title' : 'Modifier Ajustement','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ajustement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_ajustement'))

@transaction.atomic
def post_modifier_ajustement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		reference = request.POST['reference']
		emplacement_id = request.POST['emplacement_id']
		statut_id = request.POST['statut_id']
		inventaire_de = request.POST['inventaire_de']
		document = request.POST['document']
		auteur = identite.utilisateur(request)

		ajustement=dao_ajustement.toCreateAjustement(reference,emplacement_id,statut_id,inventaire_de,document)
		ajustement=dao_ajustement.toUpdateAjustement(id, ajustement)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_ajustement'))


#LIGNE AJUSTEMENT
def get_lister_ligne_ajustement(request):
	try:
		permission_number = 1029
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		#*******Filtre sur les règles **********#
		model =  dao_model.toListModel(dao_ligne_ajustement.toListLigne_ajustement(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={'title' : 'Liste des lignes d\'ajustements','model' : model,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 1,
						'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def get_creer_ligne_ajustement(request):
	try:
		permission_number = 1030
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context ={'title' : 'Nouvelle ligne d\'ajustement','utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
						'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e)

@transaction.atomic
def post_creer_ligne_ajustement(request):
	sid = transaction.savepoint()
	try:
		ajustement_id = request.POST['ajustement_id']
		article_id = request.POST['article_id']
		series_id = request.POST['series_id']
		quantite_theorique = request.POST['quantite_theorique']
		quantite_reelle = request.POST['quantite_reelle']
		unite_id = request.POST['unite_id']
		fait = request.POST['fait']
		auteur = identite.utilisateur(request)

		ligne_ajustement=dao_ligne_ajustement.toCreateLigne_ajustement(ajustement_id,article_id,series_id,quantite_theorique,quantite_reelle,unite_id,fait)
		ligne_ajustement=dao_ligne_ajustement.toSaveLigne_ajustement(auteur, ligne_ajustement)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_ligne_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_ligne_ajustement'))


def get_details_ligne_ajustement(request,ref):
	try:
		permission_number = 1029
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref=int(ref)
		ligne_ajustement=dao_ligne_ajustement.toGetLigne_ajustement(ref)
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/item.html')
		context ={'title' : 'Detail d\'une ligne Ajustement','ligne_ajustement' : ligne_ajustement,'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 4,
					'organisation': dao_organisation.toGetMainOrganisation(),
			"sous_modules":sous_modules,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_ligne_ajustement'))

def get_modifier_ligne_ajustement(request, ref):
	try:
		permission_number = 1031
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		model = dao_ligne_ajustement.toGetLigne_ajustement(ref)
		context ={'title' : 'Modifier Ligne ajustement','model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),"module" : vars_module,'menu' : 2,
					'organisation': dao_organisation.toGetMainOrganisation(),
				"sous_modules":sous_modules,
				"modules" : modules,
				'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template('ErpProject/ModuleStock/ligne_ajustement/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		return auth.toReturnFailed(request, e, reverse('module_Stock_list_ligne_ajustement'))

@transaction.atomic
def post_modifier_ligne_ajustement(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		ajustement_id = request.POST['ajustement_id']
		article_id = request.POST['article_id']
		series_id = request.POST['series_id']
		quantite_theorique = request.POST['quantite_theorique']
		quantite_reelle = request.POST['quantite_reelle']
		unite_id = request.POST['unite_id']
		fait = request.POST['fait']
		auteur = identite.utilisateur(request)

		ligne_ajustement=dao_ligne_ajustement.toCreateLigne_ajustement(ajustement_id,article_id,series_id,quantite_theorique,quantite_reelle,unite_id,fait)
		ligne_ajustement=dao_ligne_ajustement.toUpdateLigne_ajustement(id, ligne_ajustement)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.SUCCESS, 'L\'enregistrement est effectué avec succès!')
		return HttpResponseRedirect(reverse('module_Stock_list_ligne_ajustement'))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		return auth.toReturnFailed(request, e, reverse('module_Stock_add_ligne_ajustement'))