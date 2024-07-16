# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.utils.auth import auth
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
import datetime
import json
import os
import pandas as pd
import calendar
import base64
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_devise import dao_devise

from ModuleRessourcesHumaines.dao.dao_demande_achat import dao_demande_achat
from ModuleRessourcesHumaines.dao.dao_ligne_demande_achat import dao_ligne_demande_achat
from ModuleRessourcesHumaines.dao.dao_requete_demande import dao_requete_demande
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_presence import dao_presence
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
import datetime
from ErpBackOffice.models import Model_Type_conge
from ModuleRessourcesHumaines.dao.dao_conge import dao_conge

from ErpBackOffice import models
from ModuleRessourcesHumaines import serializer
from rest_framework import viewsets
from ErpBackOffice.utils.wkf_task import wkf_task

#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module = "ModuleRessourcesHumaines"
 
#Pagination
from ErpBackOffice.utils.pagination import pagination


from ModuleRessourcesHumaines.dao.dao_type_conge import dao_type_conge

def get_index_conge(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response


		model = dao_type_conge.toListType_conge()
		context ={
		'modules':modules,'sous_modules': sous_modules,
		'title' : 'Gestion des congés','model' : model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/index.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Types Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))


def get_lister_type_conge(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response


		model = dao_type_conge.toListType_conge()
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Liste de type  de congé','model' : model,'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_conge/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Types Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_type_conge(request):
	try:
		permission_number = 161
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Nouveau type de conge', 'isPopup':isPopup, 'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_conge/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Types Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_type_conge"))

def post_creer_type_conge(request):

	try:
		designation = request.POST['designation']
		nombre_limite = request.POST['nombre_limite']
		#is_active = request.POST['is_active']
		max_leaves = request.POST['max_leaves']
		#leaves_taken = request.POST['leaves_taken']
		leaves_taken = 0
		#remaining = request.POST['remaining']
		remaining = int(max_leaves)
		#double_validation = request.POST['double_validation']
		auteur = identite.utilisateur(request)

		is_active = False
		if "is_active" in request.POST : is_active = True
		double_validation = False
		if "double_validation" in request.POST : double_validation = True

		type_conge=dao_type_conge.toCreateType_conge(designation,nombre_limite,is_active,max_leaves,leaves_taken,remaining,double_validation)
		type_conge=dao_type_conge.toSaveType_conge(auteur, type_conge)

		url = '<a class="lien chargement-au-click" href="/ressourceshumaines/type_conge/item/'+ str(type_conge.id) +'/">'+ type_conge.designation + '</a>'
		#leaves_taken = '<a class="lien chargement-au-click" href="/ressourceshumaines/type_conge/conge/'+ str(type_conge.id) +'/">'+ leaves_taken + '</a>'

		type_conge.url = url
		#type_conge.leaves_taken = leaves_taken
		type_conge.save()



		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_conge'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer Types Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_type_conge'))


def get_details_type_conge(request,ref):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response


		ref=int(ref)
		type_conge=dao_type_conge.toGetType_conge(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_conge/item.html')
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Détails d\'un type de congé','type_conge' : type_conge,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}

		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Types Congés')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_conge'))


def get_modifier_type_conge(request,ref):
	try:
		permission_number = 162
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		ref = int(ref)
		model = dao_type_conge.toGetType_conge(ref)
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Modifier Type de congé','model':model, 'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_conge/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur modifier Types Congés')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_conge'))

def post_modifier_type_conge(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		nombre_limite = request.POST['nombre_limite']
		#is_active = request.POST['is_active']
		max_leaves = request.POST['max_leaves']
		leaves_taken =0
		remaining = 0
		#double_validation = request.POST['double_validation']
		auteur = identite.utilisateur(request)
		is_active = False
		if "is_active" in request.POST : is_active = True
		double_validation = False
		if "double_validation" in request.POST : double_validation = True

		type_conge=dao_type_conge.toCreateType_conge(designation,nombre_limite,is_active,max_leaves,leaves_taken,remaining,double_validation)
		type_conge=dao_type_conge.toUpdateType_conge(id, type_conge)

		#leaves_taken = '<a class="lien chargement-au-click" href="/ressourceshumaines/type_conge/conge/'+ str(type_conge.id) +'/">'+ leaves_taken + '</a>'
		#type_conge.leaves_taken = leaves_taken
		#type_conge.save()

		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_conge'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER TYPES CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier Types Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_type_conge'))

def get_lister_conge(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		model = dao_conge.toListConge()
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)

		is_gestion = True
		context ={
			'modules':modules,'sous_modules': sous_modules,
			'title' : 'Gestion de congés',
			'view':view,
			'model' : model,'is_gestion':is_gestion,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 1
			}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))


def get_lister_demande_conge(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response


		model = dao_conge.toListConge()
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		is_gestion = True
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Demande de congés','view':view,'model' : model,'is_gestion':is_gestion,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER CONGES DEMANDES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Congés demandés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))


def get_lister_conge_approuve(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		model = dao_conge.toListCongeApprouve()
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		is_gestion = False
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Congés approuvés','view':view,'model' : model,'is_gestion':is_gestion,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER CONGES APPROUVES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Congés approuvés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_conge_reject(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		model = dao_conge.toListCongeRejete()
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		is_gestion = False
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Congés rejetés','view':view,'model' : model,'is_gestion':is_gestion,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER CONGES REJETE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Congés rejeté')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_congebyType(request,types):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		types = int(types)
		untype = dao_type_conge.toGetType_conge(types)
		model = dao_conge.toListCongeofType(types)
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Liste de congés pris', 'untype':untype,'model' : model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/type_conge/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_conge(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		model = dao_employe.toListEmployes()
		model2 = dao_type_conge.toListType_conge()
		model3 = dao_employe.toListEmployes()

		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Nouvelle demande de congé', 'isPopup':isPopup, 'model':model,'model2':model2,'model3':model3,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER CONGES DEMANDES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Congés demandés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_conge"))

def post_creer_conge(request):

	try:
		#print("jsqjskqjskqjsqkj")
		description = request.POST['description']
		employe_id = request.POST['employe_id']
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
		type_conge_id = request.POST['type_conge_id']
		type = request.POST['type']
		observation = request.POST['observation']
		auteur = identite.utilisateur(request)
		temp2 = datetime.datetime.strptime(date_to,'%Y-%M-%d')
		temp1 = datetime.datetime.strptime(date_from,'%Y-%M-%d')
		temp = temp2 - temp1
		#print(temp)
		nombre_jour = temp.days
		nombre_jour_temp = nombre_jour
		employe = dao_employe.toGetEmploye(employe_id)
		user_id = employe.user_id

		#MiseAJourNombreTypeConge Restant
		dao_type_conge.toComputeDayOfTypeConge(type_conge_id)
		numero_conge = dao_conge.toGenerateNumeroDemandeConge()

		conge=dao_conge.toCreateConge(description,numero_conge,employe_id,user_id,date_from,date_to,type_conge_id,type,nombre_jour,nombre_jour_temp,observation)
		conge=dao_conge.toSaveConge(auteur, conge)


		#Initialisation du workflow expression
		wkf_task.initializeWorkflow(auteur,conge)


		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_conge', args=(conge.id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER CONGES DEMANDES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer Congés demandés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_conge"))


def get_details_conge(request,ref):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response !=None:
			return response

		ref=int(ref)
		conge=dao_conge.toGetConge(ref)
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,conge)

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/item.html')
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Détails d\'une demande de conge',
					'model' : conge,
					'historique':historique,
					'etapes_suivantes':transition_etape_suivant,
					'signee':signee,
					'content_type_id':content_type_id,
					'utilisateur' : utilisateur,
					'actions':auth.toGetActions(modules,utilisateur),
					'organisation': dao_organisation.toGetMainOrganisation(),
					#'roles':roles,
					'modules' : modules,
					'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
					'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detailler Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_conge'))


def get_modifier_conge(request,ref):
	try:
		permission_number = 162
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		model = dao_conge.toGetConge(ref)
		model2 = dao_employe.toListEmployes()
		context ={'modules':modules,'sous_modules': sous_modules,'title' : 'Modifier une demande de congé','model':model,'model2':model2, 'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/conge/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER CONGES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Congés')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_conge'))

def post_modifier_conge(request):

	id = int(request.POST['ref'])
	try:
		description = request.POST['description']
		etat = request.POST['etat']
		employe_id = request.POST['employe_id']
		#user_id = request.POST['user_id']
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
		type_conge_id = request.POST['type_conge_id']
		type = request.POST['type']
		#nombre_jour = request.POST['nombre_jour']
		#nombre_jour_temp = request.POST['nombre_jour_temp']
		observation = request.POST['observation']
		auteur = identite.utilisateur(request)
		temp1 = datetime.datetime.strptime(date_from,'%Y-%M-%d')
		temp2 = datetime.datetime.strptime(date_to,'%Y-%M-%d')
		temp = temp2 - temp1
		nombre_jour = temp.days
		nombre_jour_temp = nombre_jour
		employe = dao_employe.toGetEmploye(employe_id)
		#type_conge = dao_type_conge.toGetType_conge(type_conge_id)
		user_id = employe.user_id

		conge=dao_conge.toCreateConge(description,"",employe_id,user_id,date_from,date_to,type_conge_id,type,nombre_jour,nombre_jour_temp,observation)
		conge=dao_conge.toUpdateConge(id, conge)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_conge'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CONGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_conge'))

def get_upload_type_conge(request):
	try:
		permission_number = 161
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		
		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des types de congé",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/type_conge/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD TYPE CONGE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_type_conge"))


@transaction.atomic
def post_upload_type_conge(request):
	sid = transaction.savepoint()
	try:
		#print("upload_type_conge")
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		file_name = ""
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES["file_upload"]
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + ".xlsx")
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ""
		sheet = str(request.POST["sheet"])

		#print("Sheet : {} file: {}".format(sheet, file_name))
		df = pd.read_excel(io=file_name, sheet_name=sheet)
		auteur = identite.utilisateur(request)
				
		for i in df.index:
			designation = str(df['designation'][i])
			nombre_limite = str(df['nombre_limite'][i])
			max_leaves = str(df['max_leaves'][i])
			niveau = str(df['niveau'][i])
			is_active = str(df['est_active'][i])
			double_validation = str(df['a_double_validation'][i])

			if "oui" in is_active.lower():
				is_active = True
			else : is_active = False
   
			if "oui" in double_validation.lower():
				double_validation = True
			else : double_validation = False

			leaves_taken = 0
			remaining = int(max_leaves)

			type_conge=dao_type_conge.toCreateType_conge(designation,nombre_limite,is_active,max_leaves,leaves_taken,remaining,double_validation)
			type_conge=dao_type_conge.toSaveType_conge(auteur, type_conge)			
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_type_conge"))
	
	except Exception as e:
		#print("ERREUR POST TYPE CONGE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD TYPE CONGE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_type_conge"))


def get_upload_conge(request):
	try:
		permission_number = 160
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		
		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des congés",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/conge/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD CONGE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_conge"))


@transaction.atomic
def post_upload_conge(request):
	sid = transaction.savepoint()
	try:
		#print("upload_conge")
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		file_name = ""
		randomId = randint(111, 999)
		if 'file_upload' in request.FILES:
			file = request.FILES["file_upload"]
			account_file_dir = 'excel/'
			media_dir = media_dir + '/' + account_file_dir
			save_path = os.path.join(media_dir, str(randomId) + ".xlsx")
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			file_name = default_storage.save(save_path, file)
		else: file_name = ""
		sheet = str(request.POST["sheet"])

		#print("Sheet : {} file: {}".format(sheet, file_name))
		df = pd.read_excel(io=file_name, sheet_name=sheet)
		auteur = identite.utilisateur(request)
		
		
		for i in df.index:
			observation = str(df['observation'][i])
			description = str(df['description'][i])
			type = str(df['type'][i])

			employe_id = None
			user_id = None
			matricule = str(df['matricule'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None : 
				employe_id = employe.agent.id
				#user_id = employe.agent.user_id

			type_conge_id = None
			type_conge = str(df['type_conge'][i])
			type_conge = models.Model_Type_conge.objects.filter(designation__icontains = type_conge).first()
			if type_conge != None : type_conge_id = type_conge.id

			date_from = str(df['date_from'][i])
			date_to = str(df['date_to'][i])

			date_from = date_from[0:10]
			date_to = date_to[0:10]

			temp2 = datetime.datetime.strptime(date_to,'%Y-%M-%d')
			temp1 = datetime.datetime.strptime(date_from,'%Y-%M-%d')
			temp = temp2 - temp1
			#print(temp)
			nombre_jour = temp.days
			nombre_jour_temp = nombre_jour



			#MiseAJourNombreTypeConge Restant
			dao_type_conge.toComputeDayOfTypeConge(type_conge_id)
			numero_conge = dao_conge.toGenerateNumeroDemandeConge()

			conge=dao_conge.toCreateConge(description,numero_conge,employe_id,user_id,date_from,date_to,type_conge_id,type,nombre_jour,nombre_jour_temp,observation)
			conge=dao_conge.toSaveConge(auteur, conge)			
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_demande_conge"))
	
	except Exception as e:
		#print("ERREUR POST CONGE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD CONGE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_conge"))

class TypeCongeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Type_conge.objects.all()
	serializer_class = serializer.TypeCongeSerializer

class CongeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Conge.objects.all()
	serializer_class = serializer.CongeSerializer

class CongeDemandeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Conge.objects.filter(etat = "initié")
	serializer_class = serializer.CongeSerializer

class CongeApprouveViewsSet(viewsets.ModelViewSet):
	queryset = models.Model_Conge.objects.filter(etat = "accordé")
	serializer_class = serializer.CongeSerializer

class CongeRejeterViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Conge.objects.filter(etat = "rejeté")
	serializer_class = serializer.CongeSerializer

class CongeByTypeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Conge.objects.all()
	serializer_class = serializer.CongeSerializer