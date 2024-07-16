# Create your views here.
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
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
import os
from datetime import time, timedelta, datetime
import json
from django.db import transaction
from ErpBackOffice.utils.separateur import AfficheEntier
# Import ErpBackOffice.models
from ErpBackOffice.models import Model_Unite_fonctionnelle, Model_Employe, Model_Image, Model_Evenement, Model_Participant, Model_Alarme
from ModuleBudget.dao.dao_centre_cout import dao_centre_cout

from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId

# Import ErpBackOffice.dao
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_statut_transaction import dao_statut_transaction
from ErpBackOffice.dao.dao_moyen_paiement import dao_moyen_paiement
from ErpBackOffice.dao.dao_article import dao_article
from ErpBackOffice.dao.dao_document import dao_document
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique_demande import dao_wkf_historique_demande
from ErpBackOffice.dao.dao_wkf_historique_reception import dao_wkf_historique_reception
from ErpBackOffice.dao.dao_wkf_historique_reception import dao_wkf_historique_reception
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation
from ErpBackOffice.dao.dao_type_paiement import dao_type_paiement
from ErpBackOffice.dao.dao_wkf_historique_lotbulletin import dao_wkf_historique_lotbulletin
from ErpBackOffice.dao.dao_wkf_historique_bulletin import dao_wkf_historique_bulletin
from ErpBackOffice.utils.EmailThread import send_async_mail
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.endpoint import endpoint

# Import from ModuleAchat et ModuleVente
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleVente.dao.dao_client import dao_client
from ModuleVente.dao.dao_bon_commande import dao_bon_commande
from ModuleVente.dao.dao_ligne_commande import dao_ligne_commande
from ModuleInventaire.dao.dao_stock_article import dao_stock_article
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ModuleAchat.dao.dao_unite_achat_article import dao_unite_achat_article
from ModuleAchat.dao.dao_type_emplacement import dao_type_emplacement
from ModuleAchat.dao.dao_emplacement import dao_emplacement

from ModuleVente.dao.dao_bon_commande import dao_bon_commande

	# Import from ModuleRessourcesHumaines
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_pret import dao_pret
from ModuleRessourcesHumaines.dao.dao_conge import dao_conge
from ModuleRessourcesHumaines.dao.dao_type_unite_fonctionnelle import dao_type_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation

# Import from ModuleComptabilite
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModuleComptabilite.dao.dao_capture_compte import dao_capture_compte
from ModuleComptabilite.dao.dao_compte import dao_compte
from ModuleComptabilite.dao.dao_immobilisation import dao_immobilisation
from ModuleComptabilite.dao.dao_portee_taxe import dao_portee_taxe
from ModuleComptabilite.dao.dao_type_compte import dao_type_compte
from ModuleComptabilite.dao.dao_type_journal import dao_type_journal
from ModuleComptabilite.dao.dao_type_of_typecompte import dao_type_of_typecompte
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleComptabilite.dao.dao_ecriture_comptable import dao_ecriture_comptable
from ModuleComptabilite.dao.dao_taux_change import dao_taux_change
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleComptabilite.dao.dao_ligne_facture import dao_ligne_facture
from ModuleComptabilite.dao.dao_local import dao_local


#Import from ModuleConversation
from ModuleConversation.dao.dao_notif import dao_notif
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification

#Import From ModuleInventaire
from ModuleInventaire.dao.dao_asset import dao_asset

#Import From ModuleBudget
from ModuleBudget.dao.dao_budget import dao_budget
from ModuleBudget.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleBudget.dao.dao_projet import dao_projet
from ModuleBudget.dao.dao_activite import dao_activite
from ModuleBudget.dao.dao_nature_activite import dao_nature_activite


from ErpBackOffice import models
from ModuleBudget import serializer
from rest_framework import viewsets
from django.core.paginator import Paginator


from ModuleCalendrier.dao.dao_alarme import dao_alarme
from ModuleCalendrier.dao.dao_evenement import dao_evenement
from ModuleCalendrier.dao.dao_participant import dao_participant
from ModuleCalendrier.dao.dao_type_evenement import dao_type_evenement
from ErpBackOffice.dao.dao_model import dao_model

#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module = "ModuleCalendrier"
var_module_id = 18

# ALARME CONTROLLERS
def get_lister_alarme(request):
	try:
		permission_number = 423
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_alarme.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_alarme.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		dao_evenement.toListDeUtilisateur(utilisateur)
		title = "Liste des alarmes"
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/alarme/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des alarmes \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des alarmes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_alarme'))

def get_details_alarme(request, ref):
	try:
		permission_number = 423
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_alarme.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'alarme {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		#print(' module %s' % (ErpModule.MODULE_CALENDRIER))
		template = loader.get_template('ErpProject/ModuleCalendrier/alarme/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details alarme\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail alarme')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_alarme'))

def get_creer_alarme(request):
	try:
		permission_number = 420
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_intervalles = dao_alarme.toListTypeAlarme()
		type_alarmes = dao_alarme.toListTypeIntervalles()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Créer une alarme',
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'type_alarmes': type_alarmes,
			'type_intervalles': type_intervalles,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/alarme/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer alarme\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer alarme')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_alarme'))

def post_creer_alarme(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		type_alarme = int(request.POST["type_alarme"])
		type_intervalle = int(request.POST['type_intervalle'])
		temps = int(request.POST['temps'])

		alarme = dao_alarme.toCreate(auteur.id, designation, type_intervalle, type_alarme, temps, description)
		alarme = dao_alarme.toSave(alarme)
		return HttpResponseRedirect(reverse('module_calendrier_detail_alarme', args=(alarme.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer alarme\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer alarme')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_add_alarme'))

def get_modifier_alarme(request, ref):
	try:
		permission_number = 421
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_alarme.toGet(ref)
		type_intervalles = dao_alarme.toListTypeAlarme()
		type_alarmes = dao_alarme.toListTypeIntervalles()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'type_intervalles': type_intervalles,
			'type_alarmes': type_alarmes,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/alarme/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier alarme\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier alarme')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_alarme'))

def post_modifier_alarme(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		type_alarme = int(request.POST["type_alarme"])
		type_intervalle = int(request.POST['type_intervalle'])
		temps = int(request.POST['temps'])

		alarme = dao_alarme.toCreate(auteur.id, designation, type_intervalle, type_alarme, temps, description)
		alarme = dao_alarme.toUpdate(ref, alarme)

		if alarme == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_calendrier_detail_alarme', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier alarme\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier alarme')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_alarme'))

# EVENEMENT CONTROLLERS
def get_lister_evenement(request):
	try:
		permission_number = 412
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		est_admin = False
		actions = auth.toGetActions(modules,utilisateur)
		for action in actions:
			if action.droit == "CREER_RAPPORT": est_admin = True

		if response != None:
			return response

		if est_admin :
			# model = dao_evenement.toList()
			#*******Filtre sur les règles **********#
			model = dao_model.toListModel(dao_evenement.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
			#******* End Regle *******************#
			title = "Liste des évènements"
		else :
			# model = dao_evenement.toListDeUtilisateur(utilisateur)
			#*******Filtre sur les règles **********#
			model = dao_model.toListModel(dao_evenement.toListDeUtilisateur(utilisateur), permission_number, groupe_permissions, identite.utilisateur(request))
			#******* End Regle *******************#
			title = "Liste de mes évènements"

		try:
			view = str(request.GET.get("view","calendar"))
		except Exception as e:
			view = "calendar"

		if view != "calendar":
			#Pagination
			model = pagination.toGet(request, model)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'model' : model,
			'view' : view,
			'utilisateur' : utilisateur,
			'actions': actions,
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/evenement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des evenements \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des evenements')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_evenement'))

def get_details_evenement(request, ref):
	try:
		permission_number = 412
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_evenement.toGet(ref)
		proprietaires = model.proprietaires.all()
		rappels = model.rappels.all()
		participants = model.participants.all()
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : '{}'.format(model.designation),
			'model' : model,
			'proprietaires' : proprietaires,
			'rappels' : rappels,
			'participants' : participants,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		#print(' module %s' % (ErpModule.MODULE_CALENDRIER))
		template = loader.get_template('ErpProject/ModuleCalendrier/evenement/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_evenement'))

def get_creer_evenement(request):
	try:
		permission_number = 413
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		confidentialites = dao_evenement.toListConfidentialites()
		type_recurrents = dao_evenement.toListTypeRecurrents()
		type_fin_recurrents = dao_evenement.toListTypeFinRecurrent()
		jour_de_semaines = dao_evenement.toListJoursDelaSemaines()
		par_mois = dao_evenement.toListParMoiss()
		par_jours = dao_evenement.toListParJours()
		locales = dao_local.toListLocal()
		type_evenements = dao_type_evenement.toList()
		employes = dao_employe.toListEmployesActifs()
		rappels = dao_alarme.toList()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Créer un évènement',
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'employes': employes,
            'rappels' : rappels,
			'type_evenements': type_evenements,
			'locales' : locales,
			'par_jours': par_jours,
			'par_mois' : par_mois,
			'jour_de_semaines': jour_de_semaines,
			'type_fin_recurrents' : type_fin_recurrents,
			'type_recurrents': type_recurrents,
			'confidentialites' : confidentialites,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/evenement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_evenement'))

@transaction.atomic
def post_creer_evenement(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		journee = False
		if "journee" in request.POST : journee = True
		duree = request.POST["duree"]
		date_debut = request.POST["date_debut"]
		date_debut_heure = request.POST["date_debut_heure"]
		date_fin = request.POST["date_fin"]
		local_id = int(request.POST["local_id"])
		type_evenement_id = int(request.POST['type_evenement_id'])
		confidentialite = int(request.POST['confidentialite'])

		#print("Etape 1")
		# Gestion toute la journée
		if journee:
			date_debut_date = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
			date_fin_date = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
			date_debut_heure = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]), 8, 30)
			date_fin_heure = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 17, 30)
			if date_debut_date > date_fin_date:
				messages.error(request,'Les date et heure de fin ne peuvent pas être antérieure aux date et heure de début!')
				return HttpResponseRedirect(reverse("module_calendrier_add_evenement"))
			duree = get_duree(date_fin_heure, date_debut_heure)
			date_debut = date_debut_heure
			date_fin = date_fin_heure
			#print("Etape 2")
		else:
			date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]), int(date_debut_heure[0:2]), int(date_debut_heure[3:5]))
			duree_segondes = (int(duree[0:2]) * 3600) + (int(duree[3:5]) * 60)
			date_fin = date_debut + timedelta(seconds=duree_segondes)
			#print("Etape 3")
		# Gestion de la récurrence
		est_recurrent = False
		if "est_recurrent" in request.POST : est_recurrent = True
		if est_recurrent:
			interval_recurrent     =    int(request.POST['interval_recurrent'])
			type_recurrent         =    int(request.POST['type_recurrent'])
			compte_recurrent       =    int(request.POST['compte_recurrent'])
			type_fin_recurrent     =    int(request.POST['type_fin_recurrent'])
			date_fin_recurrent     =    request.POST["date_fin_recurrent"]
			date_fin_recurrent     =    timezone.datetime(int(date_fin_recurrent[6:10]), int(date_fin_recurrent[3:5]), int(date_fin_recurrent[0:2]))

			par_jour = int(request.POST['par_jour'])
			par_mois =  int(request.POST['par_mois'])
			date_du_mois =  int(request.POST['date_du_mois'])
			jour_de_semaine = str(request.POST['jour_de_semaine'])


			lundi = False
			if "lundi" in request.POST : lundi = True
			mardi = False
			if "mardi" in  request.POST : mardi = True
			mercredi = False
			if "mercredi" in request.POST : mercredi = True
			jeudi = False
			if "jeudi" in request.POST : jeudi = True
			vendredi = False
			if "vendredi" in request.POST : vendredi = True
			samedi = False
			if "samedi" in request.POST : samedi = True
			dimanche = False
			if "dimanche" in request.POST : dimanche = True
			#print("Etape 4")

		list_proprietaire_id = request.POST.getlist('proprietaire_id', None)
		list_rappel_id = request.POST.getlist("rappel_id", None)
		list_participant_employe_id = request.POST.getlist('participant_employe_id', None)
		list_participant_email = request.POST.getlist("participant_email", None)
		list_participant_nom = request.POST.getlist('participant_nom', None)

		dao_evenement_object = dao_evenement.toCreate(auteur.id, date_debut, date_fin, type_evenement_id, designation, description, local_id, confidentialite, duree, journee)
		#print("Etape 5")
		if est_recurrent:
			recurrent_id = dao_evenement.toGenerateRecurrentId()
			dao_evenement_object = dao_evenement.toCreateRecurrent(dao_evenement_object, True, interval_recurrent, type_recurrent, compte_recurrent, type_fin_recurrent, date_fin_recurrent, par_jour, par_mois, date_du_mois, jour_de_semaine, lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche, recurrent_id)
			duree_segondes = (int(duree[0:2]) * 3600) + (int(duree[3:5]) * 60)
			if type_recurrent == 1: # Répéter tous les jours
				interval = - interval_recurrent
				#Jusqu'à
				if type_fin_recurrent == 1:
					#On crée autant d'instance d'évènement telque défini dans compte_recurrent
					for i in range(0, compte_recurrent) :
						interval = interval + interval_recurrent
						dd = date_debut + timedelta(days=interval)
						df = date_fin + timedelta(days=interval)
						evenement = dao_evenement.toSaveEvent(dao_evenement_object, dd, df, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
						#print("Evenement {} bel et bien cree".format(evenement.id))
				elif type_fin_recurrent == 2:
					# supérieure, donc au moins un jour de plus que la date de fin
					if date_fin_recurrent < date_fin.replace(hour=0, minute=0, second=0, microsecond=0):
						messages.error(request,'Les date et heure de fin de récurrence ne peuvent pas être antérieure aux date et heure de fin du rendez-vous!')
						return HttpResponseRedirect(reverse("module_calendrier_add_evenement"))
					for i in range(0, 1000) :
						interval = interval + interval_recurrent
						dd = date_debut + timedelta(days=interval)
						df = date_fin + timedelta(days=interval)
						if date_fin_recurrent >= df.replace(hour=0, minute=0, second=0, microsecond=0):
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, dd, df, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						else: break
				#print("Etape 6")
			elif type_recurrent == 2: # Répéter toutes les semaines
				#On crée d'abord la prémière instance
				evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
				#print("Evenement {} bel et bien cree".format(evenement.id))
				interval = interval_recurrent * 7
				#Jusqu'à
				if type_fin_recurrent == 1 and compte_recurrent > 1:
					compte = 1
					the_day = date_debut.replace(hour=0, minute=0, second=0, microsecond=0)
					day_of_week = int(the_day.strftime('%w'))
					first_day_of_week = the_day + timedelta(days=-day_of_week+1)
					for i in range(1, 10000):
						start_next_week = first_day_of_week + timedelta(days=i*interval)
						next_day = start_next_week # On initialise à lundi
						if lundi == True :
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
						if mardi == True :
							next_day = start_next_week + timedelta(days=1)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
						if mercredi == True :
							next_day = start_next_week + timedelta(days=2)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
						if jeudi == True :
							next_day = start_next_week + timedelta(days=3)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
						if vendredi == True :
							next_day = start_next_week + timedelta(days=4)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
						if samedi == True :
							next_day = start_next_week + timedelta(days=5)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
						if dimanche == True :
							next_day = start_next_week + timedelta(days=6)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
					#print("Etape 7")
				elif type_fin_recurrent == 2:
					# supérieure, donc au moins un jour de plus que la date de fin
					if date_fin_recurrent < date_fin.replace(hour=0, minute=0, second=0, microsecond=0):
						messages.error(request,'Les date et heure de fin de récurrence ne peuvent pas être antérieure aux date et heure de fin du rendez-vous!')
						return HttpResponseRedirect(reverse("module_calendrier_add_evenement"))
					#On lance la boucle
					the_day = date_debut.replace(hour=0, minute=0, second=0, microsecond=0)
					day_of_week = int(the_day.strftime('%w'))
					first_day_of_week = the_day + timedelta(days=-day_of_week+1)
					for i in range(1, 10000):
						start_next_week = first_day_of_week + timedelta(days=i*interval)
						next_day = start_next_week # On initialise à lundi
						if lundi == True :
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						if mardi == True :
							next_day = start_next_week + timedelta(days=1)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						if mercredi == True :
							next_day = start_next_week + timedelta(days=2)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						if jeudi == True :
							next_day = start_next_week + timedelta(days=3)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						if vendredi == True :
							next_day = start_next_week + timedelta(days=4)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						if samedi == True :
							next_day = start_next_week + timedelta(days=5)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						if dimanche == True :
							next_day = start_next_week + timedelta(days=6)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
				#print("Etape 8")
			elif type_recurrent == 3: # Répéter tous les mois
				#On crée d'abord la prémière instance
				evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
				#print("Evenement {} bel et bien cree".format(evenement.id))
				if type_fin_recurrent == 1 and compte_recurrent > 1:
					compte = 1
					if par_mois == 1: # Date dans le mois
						for i in range(1, 10000):
							mois, annee = get_annee_mois_suivant(date_debut, interval_recurrent)
							# TODO régulariser date et mois
							date_debut = date_debut.replace(day=date_du_mois, month=mois, year=annee)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
					elif par_mois == 2: # Jour du mois
						for i in range(1, 10000):
							mois, annee = get_annee_mois_suivant(date_debut, interval_recurrent)
							next_day = dow_date_finder(par_jour, int(jour_de_semaine), mois, annee)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
							compte = compte + 1
							if compte == compte_recurrent: break
				elif type_fin_recurrent == 2:
					if par_mois == 1: # Date dans le mois
						for i in range(1, 10000):
							mois, annee = get_annee_mois_suivant(date_debut, interval_recurrent)
							# TODO régulariser date et mois
							date_debut = date_debut.replace(day=date_du_mois, month=mois, year=annee)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
					elif par_mois == 2: # Jour du mois
						for i in range(1, 10000):
							mois, annee = get_annee_mois_suivant(date_debut, interval_recurrent)
							next_day = dow_date_finder(par_jour, int(jour_de_semaine), mois, annee)
							date_debut = next_day.replace(hour=date_debut.hour, minute=date_debut.minute, second=date_debut.second, microsecond=date_debut.microsecond)
							date_fin = date_debut + timedelta(seconds=duree_segondes)
							if date_debut > date_fin_recurrent: break
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
				#print("Etape 9")
			elif type_recurrent == 4: # Répéter tous les ans
				interval = - interval_recurrent
				#Jusqu'à
				if type_fin_recurrent == 1:
					#On crée autant d'instance d'évènement telque défini dans compte_recurrent
					for i in range(0, compte_recurrent) :
						interval = interval + interval_recurrent
						dd = date_debut + timedelta(days=interval*365)
						df = date_fin + timedelta(days=interval*365)
						evenement = dao_evenement.toSaveEvent(dao_evenement_object, dd, df, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
						#print("Evenement {} bel et bien cree".format(evenement.id))
				elif type_fin_recurrent == 2:
					# supérieure, donc au moins un jour de plus que la date de fin
					if date_fin_recurrent < date_fin.replace(hour=0, minute=0, second=0, microsecond=0):
						messages.error(request,'Les date et heure de fin de récurrence ne peuvent pas être antérieure aux date et heure de fin du rendez-vous!')
						return HttpResponseRedirect(reverse("module_calendrier_add_evenement"))
					for i in range(0, 1000) :
						interval = interval + interval_recurrent
						dd = date_debut + timedelta(days=interval*365)
						df = date_fin + timedelta(days=interval*365)
						if date_fin_recurrent >= date_fin.replace(hour=0, minute=0, second=0, microsecond=0):
							evenement = dao_evenement.toSaveEvent(dao_evenement_object, dd, df, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
							#print("Evenement {} bel et bien cree".format(evenement.id))
						else: break
				#print("Etape 10")
		else:
			evenement = dao_evenement.toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom)
			#print("Evenement {} bel et bien cree".format(evenement.id))
			#print("Etape 11")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_calendrier_details_evenement', args=(evenement.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer evenement')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_add_evenement'))

def get_modifier_evenement(request, ref):
	try:
		permission_number = 414
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_evenement.toGet(ref)
		confidentialites = dao_evenement.toListConfidentialites()
		type_recurrents = dao_evenement.toListTypeRecurrents()
		type_fin_recurrents = dao_evenement.toListTypeFinRecurrent()
		jour_de_semaines = dao_evenement.toListJoursDelaSemaines()
		par_mois = dao_evenement.toListParMoiss()
		par_jours = dao_evenement.toListParJours()
		locales = dao_local.toListLocal()
		type_evenements = dao_type_evenement.toList()
		employes = dao_employe.toListEmployesActifs()
		rappels = dao_alarme.toList()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'employes': employes,
            'rappels' : rappels,
			'type_evenements': type_evenements,
			'locales' : locales,
			'par_jours': par_jours,
			'par_mois' : par_mois,
			'jour_de_semaines': jour_de_semaines,
			'type_fin_recurrents' : type_fin_recurrents,
			'type_recurrents': type_recurrents,
			'confidentialites' : confidentialites,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/evenement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_evenement'))

@transaction.atomic
def post_modifier_evenement(request):
	ref = int(request.POST["ref"])
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		journee = False
		if "journee" in request.POST : journee = True
		duree = request.POST["duree"]
		date_debut = request.POST["date_debut"]
		date_debut_heure = request.POST["date_debut_heure"]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]), int(date_debut_heure[0:2]), int(date_debut_heure[3:5]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		local_id = int(request.POST["local_id"])
		type_evenement_id = int(request.POST['type_evenement_id'])
		confidentialite = int(request.POST['confidentialite'])
		date_du_mois = int(request.POST['date_du_mois'])


		# Gestion de la récurrence
		est_recurrent = False
		if "est_recurrent" in request.POST : est_recurrent = True
		if est_recurrent:
			interval_recurrent     =    int(request.POST['interval_recurrent'])
			type_recurrent         =    int(request.POST['type_recurrent'])
			compte_recurrent       =    int(request.POST['compte_recurrent'])
			type_fin_recurrent     =    int(request.POST['type_fin_recurrent'])
			date_fin_recurrent = request.POST["date_fin_recurrent"]
			date_fin_recurrent = timezone.datetime(int(date_fin_recurrent[6:10]), int(date_fin_recurrent[3:5]), int(date_fin_recurrent[0:2]))

			par_jour = int(request.POST['par_jour'])
			par_mois =  int(request.POST['par_mois'])
			date_du_mois =  int(request.POST['date_du_mois'])
			jour_de_semaine = str(request.POST['jour_de_semaine'])

			lundi = False
			if "lundi" in request.POST : lundi = True
			mardi = False
			if "mardi" in  request.POST : mardi = True
			mercredi = False
			if "mercredi" in request.POST : mercredi = True
			jeudi = False
			if "jeudi" in request.POST : jeudi = True
			vendredi = False
			if "vendredi" in request.POST : vendredi = True
			samedi = False
			if "samedi" in request.POST : samedi = True

		list_proprietaire_id = request.POST.getlist('proprietaire_id', None)
		list_rappel_id = request.POST.getlist("rappel_id", None)
		list_participant_employe_id = request.POST.getlist('participant_employe_id', None)
		list_participant_email = request.POST.getlist("participant_email", None)
		list_participant_nom = request.POST.getlist('participant_nom', None)

		evenement = dao_evenement.toCreate(auteur.id, date_debut, date_fin, type_evenement_id, designation, description, local_id, confidentialite, duree, journee)
		if est_recurrent: evenement = dao_evenement.toCreateRecurrent(evenement, True, interval_recurrent, type_recurrent, compte_recurrent, type_fin_recurrent, date_fin_recurrent, par_jour, par_mois, date_du_mois, jour_de_semaine, lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche)
		evenement = dao_evenement.toUpdate(ref, evenement)
		if evenement == False:
			raise  Exception("Erreur modification")
		else: pass#print("Evenement {} modifie".format(ref))
		evenement = dao_evenement.toGet(ref)

		# Gestion participant (OneToMany - Modification)
		participantsOld = evenement.participants.all()
		participantsUpdated = []
		#print("confidentialite {}".format(confidentialite))
		if confidentialite == 1 or  confidentialite == 2:
			#print("Nbre de participant {}".format(len(list_participant_nom)))
			for i in range(0, len(list_participant_nom)) :
				existe = False
				ajouter = True
				nom = list_participant_nom[i]
				email = list_participant_email[i]
				employe_id = int(list_participant_employe_id[i])
				if confidentialite == 1 and employe_id == 0:
					employe_id = None
					#print("tout le monde")
				elif confidentialite == 2 and employe_id == 0:
					#print("Employe seulement")
					ajouter = False
				for participant in participantsOld:
					if participant.email == email:
						existe = True
				if ajouter == True: participantsUpdated.append(email)
				# Enregistrement nouvel éléments
				if ajouter == True and existe == False:
					participant = dao_participant.toCreate(auteur.id, evenement.id, nom, email, employe_id)
					participant = dao_participant.toSave(participant)
				#print("participant {} cree".format(participant.id))
			# Suppression éléments qui n'existent plus
			for participant in participantsOld:
				if participant.email not in participantsUpdated:
					#print("participant {} recupere".format(participant.id))
					participant.delete()
					#print("participant supprime")
		elif confidentialite == 3 and evenement.participants.count() > 0:
			#print("moi seulement")
			for participant in participantsOld:
				#print("participant {} recuperee".format(participant.id))
				participant.delete()
				#print("participant supprime")

		#Ajout des rappels (ManyToMany - Modification)
		rappelsOld = evenement.rappels.all()
		rappelsUpdated = []
		#print("Nbre de rappel {}".format(len(list_rappel_id)))
		for i in range(0, len(list_rappel_id)):
			existe = False
			alarme_id = int(list_rappel_id[i])
			alarme = Model_Alarme.objects.get(pk = alarme_id)
			for rappel in rappelsOld:
				if rappel.id == alarme.id:
					existe = True
			rappelsUpdated.append(alarme.id)
			# Enregistrement  nouvel élément
			if existe == False: evenement.rappels.add(alarme)
		# Suppression éléments qui n'existent plus
		for rappel in rappelsOld:
			if rappel.id not in rappelsUpdated:
				#print("rappel {} recupere".format(rappel.id))
				evenement.rappels.remove(rappel)
				#print("rappel supprime")

		#Ajout des propriétaires (ManyToMany - Modification)
		proprietairesOld = evenement.proprietaires.all()
		proprietairesUpdated = []
		for i in range(0, len(list_proprietaire_id)):
			proprietaire_id = int(list_proprietaire_id[i])
			proprietaire = Model_Employe.objects.get(pk = proprietaire_id)
			for item in proprietairesOld:
				if item.id == proprietaire.id:
					existe = True
					proprietairesUpdated.append(proprietaire.id)
			# Enregistrement  nouvel élément
			if existe == False: evenement.proprietaires.add(proprietaire)
		# Suppression éléments qui n'existent plus
		for proprietaire in proprietairesOld:
			if proprietaire.id not in proprietairesUpdated:
				#print("proprietaire {} recupere".format(proprietaire.id))
				evenement.proprietaires.remove(proprietaire)
				#print("proprietaire supprime")

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_calendrier_details_evenement', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier evenement')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_evenement'))

# TYPE EVENEMENT CONTROLLERS
def get_lister_type_evenement(request):
	try:
		permission_number = 416
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_type_evenement.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_type_evenement.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		title = "Liste des types d'évènement"
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/type_evenement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des type_evenements \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des type_evenements')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_type_evenement'))

def get_details_type_evenement(request, ref):
	try:
		permission_number = 416
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_type_evenement.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Type d'évènement {}".format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/type_evenement/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details type_evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail type_evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_type_evenement'))

def get_creer_type_evenement(request):
	try:
		permission_number = 417
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer un type d'évènement",
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/type_evenement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_type_evenement'))

def post_creer_type_evenement(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		type_evenement = dao_type_evenement.toCreate(auteur.id, designation, description)
		type_evenement = dao_type_evenement.toSave(type_evenement)
		return HttpResponseRedirect(reverse('module_calendrier_detail_type_evenement', args=(type_evenement.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer type_evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer type evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_add_type_evenement'))

def get_modifier_type_evenement(request, ref):
	try:
		permission_number = 418
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_type_evenement.toGet(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_CALENDRIER,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleCalendrier/type_evenement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier type_evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier type evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_type_evenement'))

def post_modifier_type_evenement(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		type_evenement = dao_type_evenement.toCreate(auteur.id, designation, description)
		type_evenement = dao_type_evenement.toUpdate(ref, type_evenement)

		if type_evenement == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_calendrier_detail_type_evenement', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier type evenement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type evenement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_calendrier_list_type_evenement'))

def get_duree(date_fin, date_debut):
	days = date_fin - date_debut
	duree_seconds = days.total_seconds()
	heures, seconds = divmod(duree_seconds, 3600)
	minutes = 0
	if seconds > 60: minutes = round(seconds/60)

	if heures < 10: heures = "0{}".format(int(heures))
	else: heures = "{}".format(int(heures))

	if minutes < 10: minutes = "0{}".format(int(minutes))
	else: minutes = "{}".format(int(minutes))

	duree = "{}:{}".format(heures, minutes)
	return duree

def dow_date_finder(which_weekday_in_month,day,month,year):
	# On soustrait le nième jour de la semaine de 1, pcq voici les valeurs prisent en compte:
	#FIRST = 0, SECOND = 1, THIRD = 2, FOURTH  = 3 ,FIFTH = 4, LAST = -1
	if which_weekday_in_month != -1: which_weekday_in_month = which_weekday_in_month - 1
	# On soustrait le jour de la semaine de 1, pcq voici les valeurs prisent en compte:
	#Lundi = 0, Mardi = 1, Mercredi = 2, Jeudi  = 3 ,Vendredi = 4, Samedi = 5, Dimanche = 6
	day = day - 1
	dt = datetime(year,month,1)
	dow_lst = []
	while dt.weekday() != day:
		dt = dt + timedelta(days=1)
	while dt.month == month:
		dow_lst.append(dt)
		dt = dt + timedelta(days=7)
	return dow_lst[which_weekday_in_month]

def get_annee_mois_suivant(date_debut, interval_recurrent):
	annee = date_debut.year
	mois = date_debut.month + interval_recurrent
	if mois > 12 and mois <= 24:
		mois = mois - 12
		annee = annee + 1
	elif mois > 24 and mois <= 36:
		mois = mois - 24
		annee = annee + 2
	elif mois > 36 and mois <= 48:
		mois = mois - 36
		annee = annee + 3
	elif mois > 48 and mois <= 60:
		mois = mois - 48
		annee = annee + 4
	return mois, annee