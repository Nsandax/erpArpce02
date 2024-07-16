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
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_droit import dao_droit
from ModuleRessourcesHumaines.dao.dao_vehicule import dao_vehicule
from ModuleRessourcesHumaines.dao.dao_vehicule_model import dao_vehicule_model
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.dao.dao_document import dao_document
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe

from ErpBackOffice import models
from ModuleRessourcesHumaines import serializer
from rest_framework import viewsets

#LOGGING
import logging, inspect
monLog = logging.getLogger("logger")
module= "ModuleRessourcesHumaines"


def get_lister_vehicule_model(request):
	try:
		droit="LISTER_VEHICULE_MODEL"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		model = dao_vehicule_model.toListVehicule_model()
		context = {
			'title' : 'Liste de modèle de véhicules',
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 1
			}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule_model/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER MODEL DE VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister modèle de Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_vehicule_model(request):
	try:
		droit="CREER_VEHICULE_MODEL"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		context = {
			'title' : 'Nouveau modèle de véhicule',
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'actions':auth.toGetActions(modules,utilisateur),
			'menu' : 2
			}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule_model/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER MODEL DE VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur créer modèle de Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_vehicule_model"))

def post_creer_vehicule_model(request):

	try:
		nom = request.POST['nom']
		type = request.POST['type']
		logo = request.POST['logo']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		vehicule_model=dao_vehicule_model.toCreateVehicule_model(nom,type,logo,description)
		vehicule_model=dao_vehicule_model.toSaveVehicule_model(auteur, vehicule_model)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_vehicule_model'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER MODEL DE VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post créer modèle de Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_vehicule_model'))


def get_details_vehicule_model(request,ref):
	try:
		droit="LISTER_VEHICULE_MODEL"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		ref=int(ref)
		vehicule_model=dao_vehicule_model.toGetVehicule_model(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule_model/item.html')
		context = {
			'title' : 'Details d\'un modèle de véhicule',
			'vehicule_model' : vehicule_model,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4,
			'actions':auth.toGetActions(modules,utilisateur)
			}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER MODEL DE VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler modèle de Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_vehicule_model'))

def get_modifier_vehicule_model(request,ref):
	try:
		droit="MODIFIER_VEHICULE_MODEL"
		modules, utilisateur,response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response


		ref = int(ref)
		model = dao_vehicule_model.toGetVehicule_model(ref)
		context ={'title' : 'Modifier Vehicule_model','model':model, 
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule_model/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER MODEL DE VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur modifier modèle de Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_vehicule_model"))

def post_modifier_vehicule_model(request):

	id = int(request.POST['ref'])
	try:
		nom = request.POST['nom']
		type = request.POST['type']
		logo = request.POST['logo']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		vehicule_model=dao_vehicule_model.toCreateVehicule_model(nom,type,logo,description)
		vehicule_model=dao_vehicule_model.toUpdateVehicule_model(id, vehicule_model)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_vehicule_model'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER MODEL DE VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post modifier modèle de Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_vehicule_model'))


def get_lister_vehicule(request):
	try:
		droit="LISTER_VEHICULE"
		modules, utilisateur,response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response


		model = dao_vehicule.toListVehicule()
		context = {
			'title' : 'Liste de véhicules',
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_vehicule(request):
	try:
		droit="CREER_VEHICULE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		
		documents = dao_document.toListDocuments()
		employes = dao_employe.toListEmployes()
		model = dao_vehicule_model.toListVehicule_model()

		context = {
			'title' : 'Nouveau véhicule',
			'model':model,'documents':documents,
			'employes':employes,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'actions':auth.toGetActions(modules,utilisateur),
			'menu' : 2
			}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur créer Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_vehicule"))

def post_creer_vehicule(request):

	try:
		designation = request.POST['designation']
		marque = request.POST['marque']
		vehicule_model_id = request.POST['vehicule_model_id']
		date_acquisition = request.POST['date_acquisition']
		image = request.POST['image']
		reference_licence = request.POST['reference_licence']
		document_id = request.POST['document_id']
		employe_id = request.POST['employe_id']
		couleur = request.POST['couleur']
		transmission = request.POST['transmission']
		type_carburant = request.POST['type_carburant']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		vehicule=dao_vehicule.toCreateVehicule(designation,marque,vehicule_model_id,date_acquisition,image,reference_licence,document_id,employe_id,couleur,transmission,type_carburant,description)
		vehicule=dao_vehicule.toSaveVehicule(auteur, vehicule)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_vehicule'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post créer Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_vehicule'))


def get_details_vehicule(request,ref):
	try:
		droit="LISTER_VEHICULE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		ref=int(ref)
		vehicule=dao_vehicule.toGetVehicule(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule/item.html')
		context = {
			'title' : 'Details d\'un véhicule',
			'vehicule' : vehicule,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4,
			'actions':auth.toGetActions(modules,utilisateur)
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_vehicule'))

def get_modifier_vehicule(request,ref):
	try:
		droit="MODIFIER_VEHICULE"
		modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		if response != None:
			return response

		ref = int(ref)
		documents = dao_document.toListDocuments()
		employes = dao_employe.toListEmployes()
		model = dao_vehicule_model.toListVehicule_model()

		model = dao_vehicule.toGetVehicule(ref)
		context ={
			'title' : 'Modifier Vehicule',
			'model':model,
			'documents':documents,
			'employes':employes,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'actions':auth.toGetActions(modules,utilisateur),
			'menu' : 2
			}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/vehicule/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur modifier Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_vehicule")) 

def post_modifier_vehicule(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		marque = request.POST['marque']
		vehicule_model_id = request.POST['vehicule_model_id']
		date_acquisition = request.POST['date_acquisition']
		image = request.POST['image']
		reference_licence = request.POST['reference_licence']
		document_id = request.POST['document_id']
		employe_id = request.POST['employe_id']
		couleur = request.POST['couleur']
		transmission = request.POST['transmission']
		type_carburant = request.POST['type_carburant']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		vehicule=dao_vehicule.toCreateVehicule(designation,marque,vehicule_model_id,date_acquisition,image,reference_licence,document_id,employe_id,couleur,transmission,type_carburant,description)
		vehicule=dao_vehicule.toUpdateVehicule(id, vehicule)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_vehicule'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER VEHICULE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post modifier Véhicule')
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_vehicule'))

class ModelVehiculeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Vehicule_model.objects.all()
	serializer_class = serializer.ModelVehiculeSerializer


class VehiculeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Vehicule.objects.all()
	serializer_class = serializer.VehiculeSerializer
