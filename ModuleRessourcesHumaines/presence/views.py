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
import datetime
import json
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.utils.auth import auth
from ModuleRessourcesHumaines.dao.dao_demande_achat import dao_demande_achat
from ModuleRessourcesHumaines.dao.dao_ligne_demande_achat import dao_ligne_demande_achat
from ModuleRessourcesHumaines.dao.dao_requete_demande import dao_requete_demande
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_presence import dao_presence
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation

from ModuleConversation.dao.dao_notification import dao_notification

from ErpBackOffice import models
from ModuleRessourcesHumaines import serializer
from rest_framework import viewsets

#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module = "ModuleRessourcesHumaines"


def get_lister_presence(request):
	try:
		droit="LISTER_PRESENCE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		#model = dao_presence.toListPresence()
		auteur = identite.utilisateur(request)
		#print(auteur.id)
		model = dao_presence.toListPresence()
		
		context = {
			'title' : 'Liste de présences',
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 1
			}

		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER PRESENCE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister présence')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_presence(request):
	try:
		droit="CREER_PRESENCE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response


		model = dao_employe.toListEmployes()	
		context ={'title' : 'Nouveau prélèvement de présence','model':model, 'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER PRESENCE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Présences')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def post_creer_presence(request,boole):

	try:
		#print('post creer presence')
		employe_id = request.POST['employe_id']
		employe = dao_employe.toGetEmploye(employe_id)
		#unite_fonctionelle_id = request.POST['unite_fonctionelle_id']
		#print(employe.unite_fonctionnelle_id)
		unite_fonctionelle_id = employe.unite_fonctionnelle_id
		#print(unite_fonctionelle_id)
		date = request.POST["date"]
		arrive = request.POST['arrive']
		depart = request.POST['depart']
		auteur = identite.utilisateur(request)

		presence=dao_presence.toCreatePresence(employe_id,unite_fonctionelle_id,date,arrive,depart)
		presence=dao_presence.toSavePresence(auteur, presence)
		boole = int(boole)
		#print(boole)
		if boole == 1:
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_presence_employe', args=(employe_id,)))
		else:
			return HttpResponseRedirect(reverse('module_ressourceshumaines_list_presence'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER PRESENCE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer Présences')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_presence'))


def get_details_presence(request,ref):
	try:
		droit="LISTER_PRESENCE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		ref=int(ref)
		presence=dao_presence.toGetPresence(ref)
		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/item.html')
		context ={'title' : 'Détails d\'une présence','presence' : presence,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAIILER PRESENCE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Présences')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_presence'))

def get_modifier_presence(request,ref):
	try:
		droit="MODIFIER_PRESENCE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response


		ref = int(ref)
		model = dao_presence.toGetPresence(ref)
		context ={'title' : 'Modifier une présence','model':model, 'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER PRESENCE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Présences')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_presence'))

def post_modifier_presence(request):

	id = int(request.POST['ref'])
	try:
		employe_id = request.POST['employe_id']
		employe = dao_employe.toGetEmploye(employe_id)
		#unite_fonctionelle_id = request.POST['unite_fonctionelle_id']
		#print(employe.unite_fonctionnelle_id)
		unite_fonctionelle_id = employe.unite_fonctionnelle_id
		arrive = request.POST['arrive']
		depart = request.POST['depart']
		auteur = identite.utilisateur(request)

		presence=dao_presence.toCreatePresence(employe_id,unite_fonctionelle_id,arrive,depart)
		presence=dao_presence.toUpdatePresence(id, presence)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_presence'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER PRESENCE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post Modifier Présences')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_presence'))



def get_lister_employe(request):
	try:
		droit="LISTER_EMPLOYE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		model = dao_employe.toListEmployes()
		
		context ={
			'title' : 'Vos employés',
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 1
			}
		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister employé')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_presence_employe(request,ref):
	try:
		droit="LISTER_PRESENCE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

			
		ref = int(ref)
		employe = dao_employe.toGetEmploye(ref)
		model = dao_presence.toGetPresenceOfEmploye(ref)
		context ={'title' : 'Présence des employés','employe':employe,'model' : model,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/employe/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER PRESENCE D'UN EMPLOYE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister présence d\'un employé')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_presence_employe(request,ref):
	try:
		droit="LISTER_PRESENCE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		ref = int(ref)
		auteur = identite.utilisateur(request)
		employe = dao_employe.toGetEmploye(ref)
		model = dao_employe.toListEmployes()	
		context ={'title' : 'Nouveau prélèvement de présence','employe':employe,'model':model, 'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourceshumaines/presence/employe/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER PRESENCE EMPLOYE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur créer présence employé')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_presence_employe"))


## DataTable Server Side

class PresenceViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Presence.objects.all()
	serializer_class = serializer.PresenceSerializer

class PresenceOfViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Presence.objects.all()
	serializer_class = serializer.PresenceSerializer