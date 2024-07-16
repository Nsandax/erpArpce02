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
from ErpBackOffice.dao.dao_model import dao_model
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
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise

from ModuleArchivage.dao.dao_dossier import dao_dossier
from ModuleArchivage.dao.dao_document import dao_document
from ModuleArchivage.archive import archive
import os.path
from pprint import pprint
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleConversation.dao.dao_notif import dao_notif
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification




from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
from pytesseract import image_to_string
import os

import urllib


from ModuleArchivage.document import PostDocument
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elasticsearch_dsl import Search


#LOGGING
import logging, inspect
monLog = logging.getLogger("logger")
module= "ModuleArchivage"
var_module_id = 17


def get_index(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(14, request)
	if response != None:
		return response
	#WAY OF NOTIFCATION
	module_name = "MODULE_ARCHIVAGE"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()

	dossier=dao_dossier.ListeNumberofDirectories()
	document=dao_document.ListeNumberofDoc()

	all_doc_year = dao_dossier.toListDossier()
	all_dos_year=dao_document.toListDocument()
	year=[]
	for item in all_doc_year:
		year.append(item.created_at.year)
	for item in all_dos_year:
		year.append(item.created_at.year)

	year=set(year)

	dos=dao_dossier.toListDossier_childRoot()
	doc=dao_document.toListDocumentLinkedInRoot()

	#END WAY 
	context = {
	'modules':modules,'sous_modules':sous_modules,
	"title" : "Module de gestion des archives",
	'actions':auth.toGetActions(modules,utilisateur),
	'dossier_tree':dos,
	'document_tree':doc,
	'organisation': dao_organisation.toGetMainOrganisation(),
	'temp_notif_count':temp_notif_count,
	'temp_notif_list':temp_notif_list,
	"utilisateur" : utilisateur,
	"modules" : modules,
	"module" : ErpModule.MODULE_ARCHIVAGE,
	"menu" : 1,
	"dossier": dossier,
	"document": document,
	"doc_by_year":year}
	template = loader.get_template("ErpProject/ModuleArchivage/index.html")
	return HttpResponse(template.render(context, request))

# Tableau de board


def get_dossier_doc_to_dashbord(request):
	try:
		mYear = request.GET['year']
		data=[]
		dossier=dao_dossier.ListeNumberofDirectories(mYear)
		document =dao_document.ListeNumberofDoc(mYear)
		data=[dossier,document]

		#print('les doc et dos %s' % (data))

		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("probleme get_inventer_to_dashbord %s"%(e))
		return JsonResponse([], safe=False)

def get_update_notification(request,ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	return get_index(request)

def get_lister_dossier_byClick(request,ref):
	try:
		permission_number = 290
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_dossier.toListDossier()
		ref=int(ref)
		#print('REF ######### ',ref)
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_dossier.toListDossierChildbyId(ref), permission_number, groupe_permissions, identite.utilisateur(request))
		#print('MODEL MODEL ',model)
		for i in model.dossier_fk_xjc.all():
			type = i.type_document
			#print('VALLEUR LINKED ',i.type_document)
		#******* End Regle *******************#
		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste de dossier','model' : model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/vueDossier.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('ERROR ARCHIVAGE ',e)
		return HttpResponseRedirect(reverse('module_archivage_index'))
		


def get_lister_dossier(request):
	permission_number = 290
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	# model = dao_dossier.toListDossier()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_dossier.toListDossier(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste de dossier','model' : model,
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleArchivage/dossier/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_dossier(request):
	permission_number = 289
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	model = dao_dossier.toListDossier()

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Nouvelle dossier','model':model,
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleArchivage/dossier/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_dossier(request):

	try:
		designation = request.POST['designation']
		description = request.POST['description']
		dossier_id = request.POST['dossier_id']
		if dossier_id == "0":
			dossier_id = None
		auteur = identite.utilisateur(request)
		dossier=dao_dossier.toCreateDossier(designation,description,dossier_id)
		dossier=dao_dossier.toSaveDossier(auteur, dossier)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# return HttpResponseRedirect(reverse('module_archivage_list_dossier'))
		return HttpResponseRedirect(reverse('module_archivage_detail_dossier', args=(dossier.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER DOSSIER \n {}'.format(auteur.nom_complet, module,e))
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_archivage_add_dossier'))


def get_details_dossier(request,ref):
	permission_number = 290
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		dossier=dao_dossier.toGetDossier(ref)
		template = loader.get_template('ErpProject/ModuleArchivage/dossier/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,dossier)

		context ={
			'modules':modules,
			'sous_modules':sous_modules,
			'title' : 'Details d\'un dossier',
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'dossier' : dossier,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'modules' : modules,
			'module' : ErpModule.MODULE_ARCHIVAGE,
			'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS DOSSIER \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_archivage_list_dossier'))

def get_modifier_dossier(request,ref):
	permission_number = 291
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_dossier.toGetDossier(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier un dossier',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model':model, 'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleArchivage/dossier/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_dossier(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		dossier_id = request.POST['dossier_id']
		auteur = identite.utilisateur(request)

		dossier=dao_dossier.toCreateDossier(designation,description,dossier_id)
		dossier=dao_dossier.toUpdateDossier(id, dossier)
		return HttpResponseRedirect(reverse('module_archivage_list_dossier'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER DOSSIER \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_archivage_add_dossier'))

def get_lister_document(request):
	permission_number = 294
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_document.toListDocument().order_by("-id")
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_document.toListDocument().order_by("-id"), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste de document',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : model,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleArchivage/document/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_document(request):
	permission_number = 293
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	model = dao_dossier.toListDossier()


	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Nouveau document',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model':model,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleArchivage/document/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_document(request):

	try:

		type_document = request.POST['type_document']
		#url_document = request.POST['url_document']
		url_document = ""
		numero_document = request.POST['numero_document']
		description = request.POST['description']
		#est_verifie = request.POST['est_verifie']
		est_verifie = False
		#status = request.POST['status']
		status = "uploaded"
		#print("unos")
		#metadonnees = request.POST['metadonnees']
		metadonnees=""
		dossier_id = request.POST['dossier_id']
		auteur = identite.utilisateur(request)
		
		#print(request.FILES["file_upload"])
		if 'file_upload' in request.FILES:
			document = request.FILES["file_upload"]
			nom_document = request.FILES['file_upload'].name

			archive.archiver(document, nom_document,type_document,numero_document,auteur.id,description,dossier_id, est_verifie)
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_archivage_list_document'))
		#return HttpResponseRedirect(reverse('module_archivage_detail_document')))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER DOCUMENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_archivage_add_document'))


def get_details_document(request,ref):
	permission_number = 294
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		#print('REF DOC ',ref)
		document=dao_document.toGetDocument(ref)
		template = loader.get_template('ErpProject/ModuleArchivage/document/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,document)

		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details d\'un document','document' : document,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 4}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS DOCUMENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_archivage_index'))

def get_modifier_document(request,ref):
	permission_number = 295
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_document.toGetDocument(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier un document','model':model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		 'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleArchivage/document/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_document(request):

	id = int(request.POST['ref'])
	try:
		type_document = request.POST['type_document']
		url_document = request.POST['url_document']
		numero_document = request.POST['numero_document']
		description = request.POST['description']
		est_verifie = request.POST['est_verifie']
		status = request.POST['status']
		metadonnees = request.POST['metadonnees']
		dossier_id = request.POST['dossier_id']
		auteur = identite.utilisateur(request)

		document=dao_document.toCreateDocument(type_document,url_document,numero_document,description,est_verifie,status,metadonnees,dossier_id)
		document=dao_document.toUpdateDocument(id, document)
		return HttpResponseRedirect(reverse('module_archivage_list_document'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER DOCUMENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_archivage_add_document'))


def get_search(request):
	permission_number = 448
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response


	#print("AAAAAAAAAAAAAAAAAAAAAAA")
	q = request.GET.get('q')
	#print(q)

	if q:

		#posts = PostDocument.search().query("match", contenu=q)
		search = Search(index=['documents'])
		posts = search.query("multi_match", query=q, fields=['metadonnees', 'type_document'])

		#print("FOUNDDD")
	else:
		posts = 'Non trouvé'
		#print("NOTT FOUNNDDD")

	return render(request, 'ErpProject/ModuleArchivage/search/search.html', {'posts': posts,'title' : 'Moteur de recherche', 'utilisateur' : identite.utilisateur(request),'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_ARCHIVAGE,'menu' : 2})