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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
#-----------------------------------------------
from ErpBackOffice.utils.separateur import AfficheEntier
from ErpBackOffice.utils.trad import trad
#-----------------------------------------------
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ErpBackOffice.utils.wkf_task import wkf_task
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from datetime import time, timedelta, datetime
import json
from django.db import transaction
import pandas as pd
import requests
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import time
from requests.auth import HTTPBasicAuth,HTTPDigestAuth
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ErpBackOffice.utils.print import render_to_pdf
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire

from ErpBackOffice.utils.endpoint import endpoint
from ErpBackOffice.utils.pagination import pagination

from ErpBackOffice.dao.dao_document import dao_document

from ModuleComptabilite.dao.dao_annee_fiscale import dao_annee_fiscale
from ModuleComptabilite.dao.dao_local import dao_local
from ModuleComptabilite.dao.dao_lettrage import dao_lettrage
from ModuleComptabilite.dao.dao_banque import dao_banque
from ModuleComptabilite.dao.dao_compte_banque import dao_compte_banque
from ModuleComptabilite.dao.dao_caisse import dao_caisse
from ModuleComptabilite.dao.dao_operationtresorerie import dao_operationtresorerie
from ModuleComptabilite.dao.dao_ligne_operation_tresorerie import dao_ligne_operation_tresorerie
from ModuleComptabilite.dao.dao_billeterie import dao_billeterie
from ModuleComptabilite.dao.dao_ligne_billeterie import dao_ligne_billeterie
from ErpBackOffice.utils.print import weasy_print
from ErpBackOffice.dao.dao_type_facture import dao_type_facture

from ModuleComptabilite.dao.dao_taxe import dao_taxe
from ModuleBudget.dao.dao_transactionbudgetaire import dao_transactionbudgetaire

# Import ErpBackOffice.models
from ErpBackOffice.models import Model_Unite_fonctionnelle, Model_Budget, Model_Employe, Model_Image, Model_Type_service

# Import ErpBackOffice.dao
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_facture_fournisseur import dao_facture_fournisseur
from ErpBackOffice.dao.dao_facture_client import dao_facture_client
from ErpBackOffice.dao.dao_facture import dao_facture
from ErpBackOffice.dao.dao_paiement import dao_paiement
from ErpBackOffice.dao.dao_transaction import dao_transaction
from ErpBackOffice.dao.dao_payloads import dao_payloads
from ErpBackOffice.dao.dao_statut_transaction import dao_statut_transaction
from ErpBackOffice.dao.dao_moyen_paiement import dao_moyen_paiement
from ErpBackOffice.dao.dao_type_paiement import dao_type_paiement
from ErpBackOffice.dao.dao_article import dao_article
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique_demande import dao_wkf_historique_demande
from ErpBackOffice.dao.dao_wkf_historique_facture import dao_wkf_historique_facture
from ErpBackOffice.dao.dao_wkf_historique_paiement import dao_wkf_historique_paiement
from ModuleBudget.dao.dao_transactionbudgetaire import dao_transactionbudgetaire
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation
from ErpBackOffice.dao.dao_model import dao_model

# Import from ModuleAchat et ModuleVente

from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleAchat.dao.dao_condition_reglement import dao_condition_reglement
from ModuleVente.dao.dao_client import dao_client
from ModuleVente.dao.dao_bon_commande import dao_bon_commande
from ModuleVente.dao.dao_ligne_commande import dao_ligne_commande
from ModuleInventaire.dao.dao_stock_article import dao_stock_article
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ModuleAchat.dao.dao_unite_achat_article import dao_unite_achat_article
from ModuleAchat.dao.dao_type_emplacement import dao_type_emplacement
from ModuleAchat.dao.dao_emplacement import dao_emplacement

from ModuleVente.dao.dao_bon_commande import dao_bon_commande
from ModuleVente.dao.dao_etat_facturation import dao_etat_facturation
from ModuleVente.dao.dao_recouvrement import dao_recouvrement
from ModuleVente.dao.dao_recouvrement_ligne import dao_recouvrement_ligne
from ModuleVente.dao.dao_relance_recouvrement import dao_relance_recouvrement


# Import from ModuleRessourcesHumaines
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
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
from ModuleComptabilite.dao.dao_budget import dao_budget
from ModuleComptabilite.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleComptabilite.dao.dao_taux_change import dao_taux_change
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleComptabilite.dao.dao_ligne_facture import dao_ligne_facture
from ModuleComptabilite.dao.dao_document_paiement import dao_document_paiement
from ModuleComptabilite.dao.dao_document_facture import dao_document_facture
from ModuleComptabilite.dao.dao_config_comptabilite import dao_config_comptabilite
from ErpBackOffice.utils.wkf_task import wkf_task
from ErpBackOffice.models import Model_Facture
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ModuleComptabilite.utils.balance import balanceArray
#from ModuleComptabilite.utils.bilan import bilan
from ModuleComptabilite.utils.compte_resultat import compteResultatArray
from ModuleComptabilite.utils.bilan import bilanArray


from ModuleInventaire.dao.dao_asset import dao_asset
from rest_framework.decorators import api_view

from ModuleInventaire.dao.dao_traitement_immobilisation import dao_traitement_immobilisation
from ModuleInventaire.dao.dao_ligne_traitementimmobilisation import dao_ligne_traitementimmobilisation

from ModuleBudget.dao.dao_centre_cout import dao_centre_cout
from ModuleBudget.dao.dao_groupeanalytique import dao_groupeanalytique

from ModuleComptabilite.dao.dao_ordre_paiement import dao_ordre_paiement
from ModuleComptabilite.dao.dao_ligne_ordre_paiement import dao_ligne_ordre_paiement

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile

#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module = "ModuleComptabilité"
var_module_id = 8

# Tableau de board
def get_tableau_de_bord(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(8, request)
	if response != None:
		return response

	facrecu = dao_bon_reception.toListBonReception()
	facFour = dao_facture_fournisseur.toListFacturesFournisseur()
	facCLient = dao_facture_client.toListFacturesClient()
	piece =dao_piece_comptable.toListPieceComptable()
	MontantFacNonsol =dao_facture_fournisseur.toListFacturesFournisseurNonSoldees()
	MontantFaCNonsol = dao_facture_client.toListFacturesClientNonSoldees()
	Taux = dao_taux_change.toListTauxCourant().count()
	ListeTauxRef = dao_devise.toGetDeviseReference()
	devises = dao_devise.toListDevisesActives()
	taux_ref = dao_devise.toGetTauxByDeviseReference()
	ListeDevise = devises.count()
	pays = dao_place.toListPlacesOfType(1)
	journaux = dao_journal.toListJournauxDuDashboard()
	CompteB = dao_compte_banque.toListCompteBanque().count()
	config = dao_config_comptabilite.toGetConfigComptabiliteActive()
	# #print("config {}".format(config))
	config_ajour = dao_config_comptabilite.estAjour()
	config_societe_ajour = dao_config_comptabilite.societeEstAjour()
	config_tresorerie_ajour = dao_config_comptabilite.tresorerieEstAjour()
	config_periode_ajour = dao_config_comptabilite.periodeEstAjour()
	config_compte_ajour = dao_config_comptabilite.compteEstAjour()
	#for journal in journaux:
	#	#print("Journal: {}".format(journal.designation))
	#	#print("Journal: {}".format(journal.kanban_dashboard_graph_datas))

	if response != None:
		return response
	# #print(ListeTauxRef)
	# #print("Installe Capture Compte")
	# INSTALLATION
	# dao_capture_compte.toInstallComptabilite()
	################################

	#WAY OF NOTIFCATION
	module_name = "MODULE_COMPTABILITE"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()


	context = {
		'title' : 'Tableau de Bord',
		'journaux' : journaux,
		'sous_modules':sous_modules,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'config' : config,
		'config_ajour' : config_ajour,
		'config_societe_ajour' : config_societe_ajour,
		'config_tresorerie_ajour' : config_tresorerie_ajour,
		'config_periode_ajour' : config_periode_ajour,
		'temp_notif_count':temp_notif_count,
		'temp_notif_list': temp_notif_list,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2,
		'pays' : pays,
		'devises' : devises,
		'facrecu' : facrecu.count(),
		'facFour' :facFour.count(),
		'ListFacFour':facFour[:4],
		'facCLient':facCLient.count(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'piece' : piece.count(),
		'ListeFacure' : facrecu[:4],
		'ListePiece' : piece[:4],
		'MontantFacNonsol': len(MontantFacNonsol),
		'MontantFaCNonsol' : len(MontantFaCNonsol),
		'Taux':Taux,
		'ListeTauxRef':ListeTauxRef,
		'ListeDevise' : ListeDevise,
		'taux_ref' : taux_ref,
		'CompteB':CompteB
	}
	template = loader.get_template('ErpProject/ModuleComptabilite/index.html')
	# template = loader.get_template('ErpProject/ModuleComptabilite/view_Dashboard/index_compta_client.html')
	# template = loader.get_template('ErpProject/ModuleComptabilite/view_Dashboard/index_compta_fss.html')
	# template = loader.get_template('ErpProject/ModuleComptabilite/view_Dashboard/index_treso.html')
	return HttpResponse(template.render(context, request))


def get_update_notification(request,ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	return get_tableau_de_bord(request)


# ECRITURES COMPTABLES VIEWS
def get_lister_ecritures(request):
	try:
		# droit="LISTER_ECRITURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 84
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_ecriture_comptable.toListEcrituresComptables()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_ecriture_comptable.toListEcrituresComptables(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		#Traitement des vues
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des écritures comptables',
			'model' : model,
			"utilisateur" : utilisateur,
			'view': view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/ecriture/list.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))

# PIECES COMPTABLES VIEWS
def get_lister_pieces_comptables(request):
	try:
		# droit="LISTER_PIECE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 85
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		# model = dao_piece_comptable.toListPiecesComptables()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_piece_comptable.toListPiecesComptables(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		#Traitement des vues
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des pièces comptables',
			'model' : model,
			'view': view,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/piece/list.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_home"))

def get_creer_piece_comptable(request):

	# droit="CREER_PIECE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 86
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# #print('nos devices %s' % (dao_devise.toListDevises()))
	context = {
		"partenaires" : dao_personne.toListPersonnes(),
		"comptes" : dao_compte.toListComptes(),
		#"devises" : dao_devise.toListDevisesActives(),
		"devise": dao_devise.toGetDeviseReference(),
		"journaux" : dao_journal.toListJournaux(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"title" : "Nouvelle pièce comptable",
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 4
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/piece/add.html")
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_piece_comptable(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_piece"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		erreur_survenue = False
		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		taux = None

		designation = request.POST["designation"]
		reference = request.POST["reference"]
		devise_id = int(request.POST["devise_id"])
		if devise_id != devise.id :
			devise = dao_devise.toGetDevise(devise_id)
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)
		partenaire_id = int(request.POST["partenaire_id"])
		montant = 0
		description = request.POST["description"]
		journal_id = int(request.POST["journal_id"])

		date_piece = request.POST["date_piece"]
		date_piece = timezone.datetime(int(date_piece[6:10]), int(date_piece[3:5]), int(date_piece[0:2]))

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation, reference, montant, journal_id, date_piece, partenaire_id, None, None, None, "", devise.id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		# #print(piece_comptable)

		list_compte_id = request.POST.getlist("compte_id", None)
		list_libelles = request.POST.getlist("libelle", None)
		list_montants_debit = request.POST.getlist("montant_debit", None)
		list_montants_credit = request.POST.getlist("montant_credit", None)

		montant_test_debit = 0
		montant_test_credit = 0

		for i in range(0, len(list_compte_id)):
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		if montant_test_credit != montant_test_debit:
			messages.error(request,'Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_comptabilite_creer_piece"))




		for i in range(0, len(list_compte_id)):
			compte_id = int(list_compte_id[i])
			libelle = list_libelles[i]
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])

			# #print("COMPTE %s" % compte_id)
			# #print("PIECE COMPTABLE %s" % piece_comptable)

			compte = dao_compte.toGetCompte(compte_id)

			ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte.id, piece_comptable.id)
			ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
			if ecriture_comptable == None:
				erreur_survenue = True
				break

		if erreur_survenue == True:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la pièce comptable")
			return HttpResponseRedirect(reverse("module_comptabilite_creer_piece_comptable"))
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_details_piece", args=(piece_comptable.id,)))
	except Exception as e:
		# #print("ERREUR POST CREER PIECE COMPTABLE")
		# #print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_piece"))

def get_modifier_piece_comptable(request, ref):

	try:

		# droit="MODIFIER_PIECE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 86
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		piece_comptable = dao_piece_comptable.toGetPieceComptable(ref)
		ecritures_comptables = dao_ecriture_comptable.toListEcrituresComptablesOfPieceComptable(piece_comptable.id)

		context = {
			"model" : piece_comptable,
			"ecritures_comptables" : ecritures_comptables,
			"partenaires" : dao_personne.toListPersonnes(),
			"comptes" : dao_compte.toListComptes(),
			"devises" : dao_devise.toListDevisesActives(),
			"journaux" : dao_journal.toListJournaux(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Modifier la pièce comptable %s" % piece_comptable.designation,
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/piece/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_pieces"))

@transaction.atomic
def post_modifier_piece_comptable(request):

	ref = int(request.POST["ref"])
	sid = transaction.savepoint()
	try:
		erreur_survenue = False
		piece_comptable = dao_piece_comptable.toGetPieceComptable(ref)

		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		taux = None

		reference = request.POST["reference"]
		piece_comptable.reference = reference

		partenaire_id = int(request.POST["partenaire_id"])
		piece_comptable.partenaire_id = partenaire_id

		description = request.POST["description"]
		piece_comptable.description = description

		journal_id = int(request.POST["journal_id"])
		if journal_id != 0: piece_comptable.journal_comptable_id = journal_id
		else: piece_comptable.journal_comptable_id = None

		is_done = dao_piece_comptable.toUpdatePieceComptable(ref, piece_comptable)
		if is_done == False:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la mise à jour de la pièce comptable")
			return HttpResponseRedirect(reverse("module_comptabilite_modifier_piece_comptable", args=(ref,)))

		list_ecriture_id = request.POST.getlist("ecriture_id", None)
		list_compte_id = request.POST.getlist("compte_id", None)
		list_libelles = request.POST.getlist("libelle", None)
		list_montants_debit = request.POST.getlist("montant_debit", None)
		list_montants_credit = request.POST.getlist("montant_credit", None)

		for i in range(0, len(list_compte_id)):
			ecriture_id = int(list_ecriture_id[i])
			compte_id = int(list_compte_id[i])
			libelle = list_libelles[i]
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])

			ecriture_comptable = dao_ecriture_comptable.toGetEcritureComptable(ecriture_id)
			compte = dao_compte.toGetCompte(compte_id)
			ecriture_comptable.compte_id = compte.id
			ecriture_comptable.montant_debit = montant_debit
			ecriture_comptable.montant_credit = montant_credit
			ecriture_comptable.designation = libelle

			is_done = dao_ecriture_comptable.toUpdateEcritureComptable(ecriture_id, ecriture_comptable)
			if is_done == False:
				erreur_survenue = True
				break
		if erreur_survenue == True:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la mise à jour de la pièce comptable")
			return HttpResponseRedirect(reverse("module_comptabilite_modifier_piece", args=(ref,)))
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_comptabilite_details_piece", args=(ref,)))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_modifier_piece", args=(ref,)))

def get_details_piece(request, ref):
	try:

		# droit="LISTER_PIECE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 85
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		piece_comptable = dao_piece_comptable.toGetPieceComptable(ref)
		ecritures_comptables = dao_ecriture_comptable.toListEcrituresComptablesOfPieceComptable(piece_comptable.id)
		partenaire = dao_personne.toGetPersonne(piece_comptable.partenaire_id)
		devise = dao_devise.toGetDevise(piece_comptable.devise_id)
		journal = dao_journal.toGetJournal(piece_comptable.journal_comptable_id)

		montant_credit = 0
		montant_debit = 0

		for item in ecritures_comptables:
			montant_credit = montant_credit + item.montant_credit
			montant_debit += item.montant_debit

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,piece_comptable)


		context = {
			"model" : piece_comptable,
			"ecritures_comptables" : ecritures_comptables,
			"partenaire" : partenaire,
			"devise" : devise,
			"journal" : journal,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			"title" : "Pièce comptable %s" % piece_comptable.designation,
			"utilisateur" : utilisateur,
			"montant_credit":AfficheEntier(makeFloat(montant_credit)),
			"montant_debit":AfficheEntier(makeFloat(montant_debit)),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/piece/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_pieces"))

def get_upload_piece_comptable(request):
	try:
		# droit="CREER_PIECE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 86
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		designation = request.POST["designation"]
		reference = request.POST["reference"]
		devise_id = request.POST.get("devise_id", 0)
		# #print("devise_id {}".format(devise_id))
		partenaire_id = request.POST.get('partenaire_id', 0)
		# #print("partenaire_id {}".format(partenaire_id))
		description = request.POST["description"]
		journal_id = request.POST.get("journal_id", 0)
		# #print("journal_id {}".format(journal_id))
		date_piece = request.POST["date_piece"]

		context = {
			"designation" : designation,
			"reference" : reference,
			"devise_id" : devise_id,
			"partenaire_id" : partenaire_id,
			"journal_id" : journal_id,
			"date_piece" : date_piece,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import des écritures comptables",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/piece/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR GET UPLOAD PIECE COMPTABLE")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_piece"))

@transaction.atomic
def post_upload_piece_comptable(request):
	sid = transaction.savepoint()
	try:
		# #print("upload_piece_comptable")
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

		# #print("Sheet : {} file: {}".format(sheet, file_name))
		df = pd.read_excel(io=file_name, sheet_name=sheet)

		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		taux = None

		designation_piece = request.POST["designation"]
		reference = request.POST["reference"]
		devise_id = int(request.POST.get("devise_id", 0))
		if devise_id != devise.id :
			devise = dao_devise.toGetDevise(devise_id)
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)

		partenaire_id = request.POST.get('partenaire_id', 0)
		if partenaire_id == 0 or partenaire_id == '': partenaire_id = None
		else: partenaire_id = int(partenaire_id)

		montant = 0
		description = request.POST["description"]

		journal_id = request.POST.get("journal_id", 0)
		if journal_id == 0 or journal_id == '': journal_id = None
		else: journal_id = int(journal_id)

		date_piece = request.POST["date_piece"]
		date_piece = timezone.datetime(int(date_piece[6:10]), int(date_piece[3:5]), int(date_piece[0:2]))

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation_piece, reference, montant, journal_id, date_piece, partenaire_id, None, None, None, "", devise.id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		# #print(piece_comptable)

		montant_test_debit = 0
		montant_test_credit = 0

		for i in df.index:
			# #print("montant_debit: {}".format(df['montant_debit'][i]))
			# #print("montant_credit: {}".format(df['montant_credit'][i]))
			montant_debit = makeFloat(df['montant_debit'][i])
			montant_credit = makeFloat(df['montant_credit'][i])
			# #print("montant_debit: {}".format(montant_debit))
			# #print("montant_credit: {}".format(montant_credit))
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		# #print("montant_test_debit: {}".format(montant_test_debit))
		# #print("montant_test_credit: {}".format(montant_test_credit))

		if montant_test_credit != montant_test_debit:
			messages.error(request,'Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_comptabilite_add_ouverture_compte"))

		for i in df.index:
			compte_id = int(i)
			numero = str(df['numero'][i])
			numero = dao_compte.toGetNumeroCompteArrondi(numero)
			designation = str(df['designation'][i])
			compte = dao_compte.toGetCompteDuNumero(numero)
			if compte == None:
				#On crée un nouveau compte comme le compte n'existe pas
				type_compte = dao_type_compte.toGetTypeCompteRecevable()
				permet_reconciliation = False

				compte = dao_compte.toCreateCompte(numero, designation, type_compte.id, permet_reconciliation)
				compte = dao_compte.toSaveCompte(auteur, compte)
			compte_id = compte.id

			libelle = designation_piece
			montant_debit = makeFloat(df['montant_debit'][i])
			montant_credit = makeFloat(df['montant_credit'][i])
			solde = montant_debit - montant_credit

			# #print("Compte Numero {}".format(numero))
			# #print("Compte ID {}".format(compte_id))
			# #print("Piece pcomptable {}".format(piece_comptable))
			if montant_debit == 0 and montant_credit == 0: pass#print("pas la peine d'enregistrer")
			else:
				ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte_id, piece_comptable.id)
				ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
				#print("Ecriture comptable {} cree".format(ecriture_comptable.id))
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_comptabilite_details_piece", args=(piece_comptable.id,)))
	except Exception as e:
		# #print("ERREUR POST UPLOAD ECRITURE COMPTABLE")
		# #print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_piece"))


# JOURNAUX VIEWS
def get_lister_journaux(request):

	# droit="LISTER_JOURNAL"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 89
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	# model = dao_journal.toListJournaux()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_journal.toListJournaux(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste des journaux',
		'model' : model,
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 20
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/journal/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_journal(request):

	# droit="CREER_JOURNAL"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 90
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		"types_journal" : dao_type_journal.toListTypesJournal(),
		"comptes" : dao_compte.toListComptes(),
		"devises" : dao_devise.toListDevisesActives(),
		"title" : "Nouveau journal",
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 20
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/journal/add.html")
	return HttpResponse(template.render(context, request))

def post_creer_journal(request):
	try:
		erreur_survenue = False
		auteur = identite.utilisateur(request)

		designation = request.POST["designation"]
		code = request.POST["code"]
		type_journal = int(request.POST["type_journal"])
		devise_id = int(request.POST["devise_id"])
		compte_credit_id = int(request.POST["compte_credit_id"])
		compte_debit_id = int(request.POST["compte_debit_id"])
		est_affiche = False
		if "est_affiche" in request.POST: est_affiche = True

		journal = dao_journal.toCreateJournal(code, designation, type_journal, est_affiche, compte_debit_id, compte_credit_id, devise_id)
		journal = dao_journal.toSaveJournal(auteur, journal)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_details_journal", args=(journal.id,)))

	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_journal"))

def get_modifier_journal(request, ref):
	try:

		# droit="MODIFIER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 91
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		journal = dao_journal.toGetJournal(ref)

		context = {
			"model" : journal,
			"types_journal" : dao_type_journal.toListTypesJournal(),
			"comptes" : dao_compte.toListComptes(),
			"devises" : dao_devise.toListDevisesActives(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Modifier le journal %s" % journal.designation,
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 20
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/journal/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_journaux"))

def post_modifier_journal(request):
	ref = int(request.POST["ref"])
	try:
		journal = dao_journal.toGetJournal(ref)
		auteur = identite.utilisateur(request)

		designation = request.POST["designation"]
		journal.designation = designation

		code = request.POST["code"]
		journal.code = code

		type_journal = int(request.POST["type_journal"])
		journal.type_journal = type_journal

		devise_id = int(request.POST["devise_id"])
		if devise_id != 0 : journal.devise_id = devise_id
		else: journal.devise_id = None

		compte_credit_id = int(request.POST["compte_credit_id"])
		if compte_credit_id != 0: journal.compte_credit_id = compte_credit_id
		else: journal.compte_credit_id = None

		compte_debit_id = int(request.POST["compte_debit_id"])
		if compte_debit_id != 0: journal.compte_debit_id = compte_debit_id
		else: journal.compte_debit_id = None

		est_affiche = False
		if "est_affiche" in request.POST: est_affiche = True
		journal.est_affiche = est_affiche

		is_done = dao_journal.toUpdateJournal(ref, journal)
		if is_done == False:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la mise à jour du journal")
			return HttpResponseRedirect(reverse("module_comptabilite_modifier_journal", args=(ref,)))
		else:
			return HttpResponseRedirect(reverse("module_comptabilite_details_journal", args=(ref,)))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_modifier_journal", args=(ref,)))

def get_set_journal_defaut(request, ref):
	try:
		ref = int(ref)
		journal = dao_journal.toGetJournal(ref)

		is_done = dao_journal.toSetJournalDefaut(journal.id, journal.type_journal)
		if is_done == True: return HttpResponseRedirect(reverse("module_comptabilite_details_journal", args=(ref,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'assignation du journal par défaut.")
			return HttpResponseRedirect(reverse("module_comptabilite_details_journal", args=(ref,)))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_journaux"))

def get_details_journal(request, ref):
	try:

		# droit="LISTER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 89
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		journal = dao_journal.toGetJournal(ref)
		type_journal = dao_type_journal.toGetTypeJournal(journal.type_journal)
		devise = None
		if journal.devise != None: devise = dao_devise.toGetDevise(journal.devise_id)
		compte_credit = None
		if journal.compte_credit != None: compte_credit = dao_compte.toGetCompte(journal.compte_credit_id)
		compte_debit = None
		if journal.compte_debit != None: compte_debit = dao_compte.toGetCompte(journal.compte_debit_id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,journal)


		context = {
			"model" : journal,
			"devise" : devise,
			"compte_credit" : compte_credit,
			"compte_debit" : compte_debit,
			"type_journal" : type_journal,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Journal %s" % journal.designation,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 20
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/journal/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_journaux"))

# COMPTES VIEWS
def get_lister_comptes(request):

	# droit="LISTER_COMPTE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 93
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_compte.toListComptes()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_compte.toListComptes(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Plan comptable',
		'model' : model,
		'view': view,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/compte/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_compte(request):

	# droit="CREER_COMPTE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 94
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Nouveau compte',
		"types_compte" : dao_type_compte.toListTypesCompte(),
		"utilisateur" : utilisateur,
		'isPopup': True if 'isPopup' in request.GET else False,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/compte/add.html")
	return HttpResponse(template.render(context, request))

def post_creer_compte(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		numero = request.POST["numero"]
		type_compte_id = int(request.POST["type_compte_id"])
		isPopup = request.POST["isPopup"]
		permet_reconciliation = False
		if "permet_reconciliation" in request.POST: permet_reconciliation = True

		compte = dao_compte.toCreateCompte(numero, designation, type_compte_id, permet_reconciliation)
		compte = dao_compte.toSaveCompte(auteur, compte)

		if compte == None:
			return HttpResponseRedirect(reverse("module_comptabilite_creer_compte")) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
		else:
			return HttpResponseRedirect(reverse('module_comptabilite_details_compte', args=(compte.id,))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_compte"))

def get_modifier_compte(request, ref):

	try:

		# droit="MODIFIER_COMPTE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 95
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_compte.toGetCompte(ref)
		context = {
			'title' : 'Compte %s' % model.designation,
			"model" : model,
			"types_compte" : dao_type_compte.toListTypesCompte(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 2
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/compte/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_comptes"))

def post_modifier_compte(request):
	ref = int(request.POST["ref"])
	# #print('touché')
	try:
		designation = request.POST["designation"]
		numero =int( request.POST["numero"])
		type_compte_id = int(request.POST["type_compte_id"])
		permet_reconciliation = False

		# #print(' designaion %s'%(designation))
		# #print(' numero %s'%(numero))
		# #print(' type_compte_id %s' % (type_compte_id))
		if "permet_reconciliation" in request.POST: permet_reconciliation = True

		compte = dao_compte.toCreateCompte(numero, designation, type_compte_id, permet_reconciliation)

		is_done = dao_compte.toUpdateCompte(ref, compte)

		if is_done == True:
			return HttpResponseRedirect(reverse("module_comptabilite_details_compte", args=(ref,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la mise à jour du compte")
			return HttpResponseRedirect(reverse("module_comptabilite_modifier_compte", args=(ref,)))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_modifier_compte", args=(ref,)))

def get_details_compte(request, ref):

	try:
		# droit="LISTER_COMPTE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 93
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		model = dao_compte.toGetCompte(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context = {
			'title' : 'Compte %s' % model.designation,
			"model" : model,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 2
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/compte/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_comptes"))

def get_lister_comptes_correspondants(request):

	if('term' in request.GET):
		term = request.GET["term"].lower()
		data = []
		comptes = dao_compte.toListComptes()

		for compte in comptes:
			designation = ("%s %s" % (compte.numero, compte.designation)).lower()
			if designation.find(term) != -1 :
				element = {
					'label':"%s %s" % (compte.numero, compte.designation),
					'value':"%s %s" % (compte.numero, compte.designation),
					'id':compte.id
				}
				data.append(element)
		return JsonResponse(data, safe=False)
	else: return JsonResponse([], safe=True)

# ENV PDF OUTPUT
def link_callback(uri, rel):
	"""
	Convert HTML URIs to absolute system paths so xhtml2pdf can access those
	resources
	"""

	sUrl = settings.STATIC_URL
	sRoot = settings.STATIC_ROOT
	mUrl = settings.MEDIA_URL
	mRoot = settings.MEDIA_ROOT

	# convert URIs to absolute system paths
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))
	else:
		return uri  # handle absolute uri (ie: http://some.tld/foo.png)

	# make sure that file exists
	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
		)
	return path

# JOURNAUX OUTPUT PDF VIEWS
def get_generer_journal(request):

	# droit="GENERER_JOURNAL"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 97
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
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 5
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/journal/generate.html")
	return HttpResponse(template.render(context, request))

def post_traiter_journal(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction du journal'''
	#On recupère et format les inputs reçus
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise_ref = dao_devise.toGetDeviseReference()

	groupe = int(request.POST["groupe"])

	#On declare les tableaux et variable qui seront renvoyés en output
	ecritures_comptables = []
	pieces_comptables = []
	journaux = []
	title = ""

	#Début traitement par Option choisie (Groupe)
	if groupe == 0:
		title = "Journal de toutes les écritures"
		list_journaux = dao_journal.toListJournaux()
		for item in list_journaux:
			pieces = dao_piece_comptable.toListPiecesComptablesDuJournal(item.id)
			pieces_comptables.extend(pieces)
			if len(pieces) != 0: journaux.append(item)
	elif groupe == -1:
		title = "Journal des écritures de certaines pièces"
		list_journal_id = request.POST.getlist('journal_id', None)

		if len(list_journal_id) == 0:
			messages.add_message(request, messages.ERROR, "Veillez sélectionner au moins un journal comme vous voulez avoir un rapport incluant certains journaux.")
			return HttpResponseRedirect(reverse("module_comptabilite_generer_journal"))

		for i in range(0, len(list_journal_id)) :
			journal_id = int(list_journal_id[i])
			item = dao_journal.toGetJournal(journal_id)
			journaux.append(item)
	else:
		type_journal = dao_type_journal.toGetTypeJournal(groupe)
		journaux = dao_journal.toListJournauxOf(type_journal["id"])
		title = "Journal de %s" % type_journal["designation"]
		for item in journaux:
			pieces_comptables.extend(dao_piece_comptable.toListPiecesComptablesDuJournal(item.id))

	#Une fois les journaux et les pièces récupérés, il reste plus que les écritures
	for item in pieces_comptables:
		ecritures_comptables.extend(dao_ecriture_comptable.toListEcrituresComptablesOfPieceComptableInPeriode(item.id, date_debut, date_fin))
	ecritures_comptables = sorted(ecritures_comptables, key=lambda ecriture: ecriture.date_creation, reverse=True)

	equilibre_credit = 0
	equilibre_debit = 0
	for item in ecritures_comptables:
		equilibre_credit = equilibre_credit + float(item.credit)
		equilibre_debit = equilibre_debit + float(item.debit)

	total_equilibre_credit = 0
	total_equilibre_debit = 0
	for item in journaux:
		total_equilibre_credit = total_equilibre_credit + float(item.valeur_credit)
		total_equilibre_debit = total_equilibre_debit + float(item.valeur_debit)

	context = {
		'title' : title,
		"model" : ecritures_comptables,
		"journaux" : journaux,
		"pieces_comptables" : pieces_comptables,
		"equilibre_credit" : "%.2f" % equilibre_credit,
		"equilibre_debit" : "%.2f" % equilibre_debit,
		"total_equilibre_credit" : "%.2f" % total_equilibre_credit,
		"total_equilibre_debit" : "%.2f" % total_equilibre_debit,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		"groupe" : groupe,
		"types_journal" : dao_type_journal.toListTypesJournal(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : "portrait",
		'menu' : 5
	}
	return context

def post_generer_journal(request):
	try:
		#Authentification
		# droit="GENERER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 97
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_journal(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModuleComptabilite/journal/generated.html")
		docHtml = template.render(context)
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_journal"))

def post_imprimer_journal(request):
	try:
		#Authentification
		# droit="IMPRIMER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 97
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_journal(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/journal.html", "journal.pdf", context)

	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_journal"))

#DDP ORDRE DE PAIEMENT
def post_imprimer_ordre_paiement(request, ref):
		permission_number = 361
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		try:
			ref=int(ref)
			ordre_paiement=dao_ordre_paiement.toGetOrdre_paiement(ref)

			#Traitement et recuperation des informations importantes à afficher dans l'item.html
			historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,ordre_paiement)

			# template = loader.get_template('ErpProject/ModuleComptabilite/ordre_paiement/item.html')
			Ligne = dao_ligne_ordre_paiement.toListLigneOfOrdrePaiement(ref)

			context ={'title' : 'DEMANDE DE PAIEMENT N° ' + ordre_paiement.reference,
			'lignes': dao_ligne_ordre_paiement.toListLigneOfOrdrePaiement(ref),
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'roles':groupe_permissions,
			'modules' : modules,'sous_modules': sous_modules,
			'documents':documents,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'model' : ordre_paiement,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

			if len(Ligne) > 1:
				return weasy_print("ErpProject/ModuleComptabilite/reporting/ordre_paiement.html", "DDP.pdf", context)
			else:
				return weasy_print("ErpProject/ModuleComptabilite/reporting/ordre_paiement_alone.html", "DDP.pdf", context)
		except Exception as e:
			#print('Erreut Get Detail')
			messages.error(request,e)
			auteur = identite.utilisateur(request)
			monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS ORDRE_PAIEMENT \n {}'.format(auteur.nom_complet, module,e))
			#print(e)
			return HttpResponseRedirect(reverse('module_comptabilite_list_ordre_paiement'))

# GRANDS LIVRES OUTPUT PDF
def get_generer_grand_livre(request):

	# droit="GENERER_GRANDLIVRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 98
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
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 6
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/livre/generate.html")
	return HttpResponse(template.render(context, request))

def post_traiter_grand_livre(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction du grand livre'''
	#On recupère et format les inputs reçus
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise = dao_devise.toGetDeviseReference()

	groupe = int(request.POST["groupe"])
	title = ""

	#On declare les tableaux et variable qui seront renvoyés en output
	comptes = []
	ecritures_comptables = []

	#Pour l'option tous les comptes
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
	#Pour l'option où on choisie que quelques les comptes
	elif groupe == -1:
		title = "Grand-Livre de certains comptes"
		list_compte_id = request.POST.getlist('compte_id', None)
		#Quand on a sélectionné aucun compte --- Erreur
		if len(list_compte_id) == 0:
			messages.add_message(request, messages.ERROR, "Veillez sélectionner au moins un compte comme vous voulez avoir le grand-livre de certains comptes.")
			return HttpResponseRedirect(reverse("module_comptabilite_generer_grand_livre"))

		for i in range(0, len(list_compte_id)) :
			compte_id = int(list_compte_id[i])
			compte = dao_compte.toGetCompte(compte_id)
			comptes.append(compte)
			ecritures_comptables.extend(dao_ecriture_comptable.toListEcrituresComptablesDuCompteInPeriode(compte.id, date_debut, date_fin))
	#Sinon la dernière option c'est par type de compte
	else:
		type_compte = dao_type_compte.toGetTypeCompte(groupe)
		comptes = dao_compte.toListComptesOf(type_compte.id)
		title = "Grand-Livre des comptes %s" % type_compte.designation
		for compte in comptes:
			ecritures_comptables.extend(dao_ecriture_comptable.toListEcrituresComptablesDuCompteInPeriode(compte.id, date_debut, date_fin))
	#On trie les comptes et écritures générées
	comptes = sorted(comptes, key=lambda compte: compte.designation, reverse=False)
	ecritures_comptables = sorted(ecritures_comptables, key=lambda ecriture: ecriture.date_creation, reverse=True)

	#Calcule des totaux
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
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 6
	}
	return context


def post_generer_grand_livre(request):
	try:
		# droit="GENERER_GRANDLIVRE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_grand_livre(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/livre/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_grand_livre"))

def post_imprimer_grand_livre(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_grand_livre(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/grand_livre.html", "grand_livre.pdf", context)


	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_grand_livre"))

# BALANCE GENERALE OUTPUT PDF
def get_generer_balance_generale(request):

	# droit="GENERER_BALANCE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 99
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
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/balance/generate.html")
	return HttpResponse(template.render(context, request))

def post_traiter_balance_generale(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction d'une balance générale'''
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()

	#On declare les tableaux et variable qui seront renvoyés en output
	donnees_balance = []
	equilibre_credit_ouverture = 0
	equilibre_debit_ouverture = 0
	equilibre_credit_mouvement = 0
	equilibre_debit_mouvement = 0
	equilibre_credit_solde = 0
	equilibre_debit_solde = 0

	#On récupère tous les comptes dans un premier temps
	comptes = dao_compte.toListComptes()

	for compte in comptes:
		#Ici Pour chaque compte, on recupère toutes les ecritures de la periode choisie
		ecrituresDansPeriode = dao_ecriture_comptable.toListEcrituresDuCompteInPeriode(compte, date_debut, date_fin)
		#Ici Pour chaque compte, on recupère toutes les ecritures avant la periode choisie dans l'année fiscal en cours
		ecrituresAvantPeriode = dao_ecriture_comptable.toListEcrituresDuCompteBeforePeriode(compte, date_debut)
		if len(ecrituresDansPeriode) > 0 or len(ecrituresAvantPeriode) > 0: #Si le compte a au moins une ecriture, on le rajoute dans la liste de compte à afficher dans la balance
			#On initialise les montant de la balance pour ce compte
			solde_initial_debit = 0
			solde_initial_credit = 0
			mouvement_credit = 0
			mouvement_debit = 0
			solde_final_debit = 0
			solde_final_credit = 0

			# On récupere les soldes initiaux à partir des écritures d'avant période
			for ecriture in ecrituresAvantPeriode:
				solde_initial_debit = solde_initial_debit + float(ecriture.montant_debit)
				solde_initial_credit = solde_initial_credit + float(ecriture.montant_credit)

			# On récupere le solde des mouvement à partir des écritures de la période
			for ecriture in ecrituresDansPeriode:
				mouvement_debit = mouvement_debit + float(ecriture.montant_debit)
				mouvement_credit = mouvement_credit + float(ecriture.montant_credit)

			# Pour les soldes finaux, on additionne d'abord les soldes initiaux et mouvement
			solde_debit = solde_initial_debit + mouvement_debit
			solde_credit = solde_initial_credit + mouvement_credit
			#Puis par rapport au signe de la différence obtenue, on affecte soit sfd(si +) ou sfc(si -)
			solde = solde_debit - solde_credit
			if solde < 0: solde_final_credit = abs(solde)
			else: solde_final_debit = solde

			#On affecte les données de la ligne qui sera affiché la balance
			item = {
				"numero_compte" : compte.numero,
				"designation_compte" : compte.designation,
				"debit_ouverture" : "%.2f" % solde_initial_debit,
				"credit_ouverture" : "%.2f" % solde_initial_credit,
				"debit_mouvement" : "%.2f" % mouvement_debit,
				"credit_mouvement" : "%.2f" % mouvement_credit,
				"debit_solde" : "%.2f" % solde_final_debit,
				"credit_solde" : "%.2f" % solde_final_credit
			}
			donnees_balance.append(item)

			#On incrémente les totaux avec les données de cette ligne de la balance
			equilibre_credit_ouverture = equilibre_credit_ouverture + solde_initial_credit
			equilibre_debit_ouverture = equilibre_debit_ouverture + solde_initial_credit
			equilibre_credit_mouvement = equilibre_credit_mouvement + mouvement_credit
			equilibre_debit_mouvement = equilibre_debit_mouvement + mouvement_debit
			equilibre_credit_solde = equilibre_credit_solde + solde_final_credit
			equilibre_debit_solde = equilibre_debit_solde + solde_final_debit

	context = {
		'title' : "Balance générale des comptes",
		"model" : donnees_balance,
		'equilibre_credit_ouverture' : "%.2f" % equilibre_credit_ouverture,
		'equilibre_debit_ouverture' : "%.2f" % equilibre_debit_ouverture,
		'equilibre_credit_mouvement' : "%.2f" % equilibre_credit_mouvement,
		'equilibre_debit_mouvement' : "%.2f" % equilibre_debit_mouvement,
		'equilibre_credit_solde' : "%.2f" % equilibre_credit_solde,
		'equilibre_debit_solde' : "%.2f" % equilibre_debit_solde,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7
	}
	return context

def post_generer_balance_generale(request):
	try:
		# droit="GENERER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 99
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_generale(request, utilisateur, modules, sous_modules)


		template = loader.get_template("ErpProject/ModuleComptabilite/balance/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_generale"))

def post_imprimer_balance_generale(request):
	try:
		# droit="IMPRIMER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 99
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = post_traiter_balance_generale(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/balance.html", "balance.pdf", context)

	except Exception as e:
		# #print("ERREUR print BALANCE")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_generale"))

# BALANCE DES TIERS
def get_generer_balance_tiers(request):

	# droit="GENERER_BALANCE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 369
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer la balance des tiers',
		"devises" : dao_devise.toListDevisesActives(),
		"clients" : dao_client.toListClientsActifs(),
		"fournisseurs" : dao_fournisseur.toListFournisseursActifs(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/balance_tiers/generate.html")
	return HttpResponse(template.render(context, request))

def post_traiter_balance_tiers(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction de la balance tiers'''
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()
	tiers = int(request.POST["tiers"])

	#On declare les tableaux et variable qui seront renvoyés en output
	donnees_balance = []
	equilibre_credit_mouvement = 0
	equilibre_debit_mouvement = 0
	equilibre_credit_solde = 0
	equilibre_debit_solde = 0

	#On récupère tous les comptes clients ou fournisseurs selon la requête
	if tiers == 1:
		comptes = dao_compte.toListComptesClient()
		tiers_name = "clients"
	elif tiers == 2:
		comptes = dao_compte.toListComptesFournisseur()
		tiers_name = "fournisseurs"

	for compte in comptes:
		#Ici Pour chaque compte, on recupère toutes les ecritures de la periode choisie
		ecrituresDansPeriode = dao_ecriture_comptable.toListEcrituresDuCompteInPeriode(compte, date_debut, date_fin)
		if len(ecrituresDansPeriode) > 0: #Si le compte a au moins une ecriture, on le rajoute dans la liste de compte à afficher dans la balance
			#On initialise les montant de la balance pour ce compte
			mouvement_credit = 0
			mouvement_debit = 0
			solde_final_debit = 0
			solde_final_credit = 0

			# On récupere le solde des mouvement à partir des écritures de la période
			for ecriture in ecrituresDansPeriode:
				mouvement_debit = mouvement_debit + float(ecriture.montant_debit)
				mouvement_credit = mouvement_credit + float(ecriture.montant_credit)

			# Pour les soldes finaux, on additionne d'abord les soldes initiaux et mouvement
			solde_debit = mouvement_debit
			solde_credit = mouvement_credit
			#Puis par rapport au signe de la différence obtenue, on affecte soit sfd(si +) ou sfc(si -)
			solde = solde_debit - solde_credit
			if solde < 0: solde_final_credit = abs(solde)
			else: solde_final_debit = solde

			#On affecte les données de la ligne qui sera affiché la balance
			item = {
				"numero_compte" : compte.numero,
				"designation_compte" : compte.designation,
				"debit_mouvement" : "%.2f" % mouvement_debit,
				"credit_mouvement" : "%.2f" % mouvement_credit,
				"debit_solde" : "%.2f" % solde_final_debit,
				"credit_solde" : "%.2f" % solde_final_credit
			}
			donnees_balance.append(item)

			#On incrémente les totaux avec les données de cette ligne de la balance
			equilibre_credit_mouvement = equilibre_credit_mouvement + mouvement_credit
			equilibre_debit_mouvement = equilibre_debit_mouvement + mouvement_debit
			equilibre_credit_solde = equilibre_credit_solde + solde_final_credit
			equilibre_debit_solde = equilibre_debit_solde + solde_final_debit

	context = {
		'title' : "Balance {}".format(tiers_name),
		"model" : donnees_balance,
		'equilibre_credit_mouvement' : "%.2f" % equilibre_credit_mouvement,
		'equilibre_debit_mouvement' : "%.2f" % equilibre_debit_mouvement,
		'equilibre_credit_solde' : "%.2f" % equilibre_credit_solde,
		'equilibre_debit_solde' : "%.2f" % equilibre_debit_solde,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		"tiers" : tiers,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7
	}
	return context


def post_generer_balance_tiers(request):
	try:
		# droit="GENERER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 369
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_tiers(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/balance_tiers/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_tiers"))

def post_imprimer_balance_tiers(request):
	try:
		# droit="IMPRIMER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 369
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_tiers(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/balance_tiers.html", "balance_tiers.pdf", context)

	except Exception as e:
		# #print("ERREUR")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_tiers"))


# BALANCE AGEE
def get_generer_balance_agee_client(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 370
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
			"module" : ErpModule.MODULE_COMPTABILITE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/balance_agee/client/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))

def post_traiter_balance_agee_client(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction de la balance agée'''
	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)
	devise = dao_devise.toGetDeviseReference()
	type_date = "5"

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
		"type_date": type_date,
		'total_montant_au_jour' : "%.2f" % total_montant_au_jour,
		'total_montant_1_30' : "%.2f" % total_montant_1_30,
		'total_montant_31_60' : "%.2f" % total_montant_31_60,
		'total_montant_61_90' : "%.2f" % total_montant_61_90,
		'total_montant_91_plus' : "%.2f" % total_montant_91_plus,
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7
	}
	return context


def post_generer_balance_agee_client(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 370
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_balance_agee_client(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/balance_agee/client/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST GENERATE BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_agee_client"))


def post_imprimer_balance_agee_client(request):
	try:
		# droit="IMPRIMER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 370
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_agee_client(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/balance_agee_client.html", "balance_agee_client.pdf", context)

	except Exception as e:
		# #print("ERREUR print BALANCE AGEE")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_agee_client"))

# BALANCE AGEE FOURNISSEUR
def get_generer_balance_agee_fournisseur(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 371
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
			"module" : ErpModule.MODULE_COMPTABILITE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/balance_agee/fournisseur/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))

def post_traiter_balance_agee_fournisseur(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction du journal'''
	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)
	devise = dao_devise.toGetDeviseReference()
	type_date = "5"

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
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7
	}
	return context



def post_generer_balance_agee_fournisseur(request):
	try:
		# droit="GENERER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 371
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_agee_fournisseur(request, utilisateur, modules, sous_modules)


		template = loader.get_template("ErpProject/ModuleComptabilite/balance_agee/fournisseur/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST GENERATE BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_agee_fournisseur"))


def post_imprimer_balance_agee_fournisseur(request):
	try:
		# droit="IMPRIMER_BALANCE_AGEE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 371
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_balance_agee_fournisseur(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/balance_agee_fournisseur.html", "balance_agee_fournisseur.pdf", context)

	except Exception as e:
		# #print("ERREUR POST print BALANCE AGEE")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_balance_agee_fournisseur"))


# BILAN OUTPUT PDF
def get_generer_bilan(request):

	# droit="GENERER_BILAN"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 100
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
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 8
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/bilan/generate.html")
	return HttpResponse(template.render(context, request))


def post_traiter_bilan(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction du bilan'''
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()

	#On declare les tableaux et variable qui seront renvoyés en output
	donnees_bilan_actif = []
	donnees_bilan_passif = []
	comptes = []

	#On récupère les données de la balance de la periode
	donnees_balance = balanceArray.toGetInPeriode(date_debut, date_fin, devise)
	#TODO Garder que les comptes du bilan (classe 1 à 5) pour optimisation

	#On récupère le resultat de la periode
	donnees_compte_resultat = compteResultatArray.toGetOfBalance(donnees_balance)

	# -----------------------------------
	# TRAITEMENT BILAN ACTIF
	# -----------------------------------

	total_immo_incorporelle_brut = 0
	total_immo_incorporelle_amort = 0
	total_immo_incorporelle = 0

	total_immo_corporelle_brut = 0
	total_immo_corporelle_amort = 0
	total_immo_corporelle = 0

	total_immo_financiere_brut = 0
	total_immo_financiere_amort = 0
	total_immo_financiere = 0

	total_actif_immobilise_brut = 0
	total_actif_immobilise_amort = 0
	total_actif_immobilise = 0

	creances_emplois_brut = 0
	creances_emplois_amort = 0
	creances_emplois = 0

	total_actif_circulant_brut = 0
	total_actif_circulant_amort = 0
	total_actif_circulant = 0

	total_tresorerie_actif_brut = 0
	total_tresorerie_actif_amort = 0
	total_tresorerie_actif = 0

	total_general_actif_brut = 0
	total_general_actif_amort = 0
	total_general_actif = 0

	# -----------------------------------
	# TOTAL IMMOBILISATIONS INCORPORELLES
	item = {
		"reference" : "AD",
		"libelle" : "IMMOBILISATIONS INCORPORELLES",
		"note" : "3",
		"est_total" : True,
		"brut" : "%.2f" % total_immo_incorporelle_brut,
		"amort" : "%.2f" % total_immo_incorporelle_amort,
		"balance_n" : "%.2f" % total_immo_incorporelle,
		"balance_n1" : "%.2f" % total_immo_incorporelle
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	# Frais de développement et de prospection 211, 2191, 2181    2811, 2911, 2918, 2919
	#
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] == "211" or item_balance["numero_compte"][0:4] in ("2191", "2181"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AE",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:4] in ("2811", "2911", "2918", "2919"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AE",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AE",
		"libelle" : "Frais de développement et de prospection",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_incorporelle_brut = total_immo_incorporelle_brut + brut
	total_immo_incorporelle_amort = total_immo_incorporelle_amort + amort
	total_immo_incorporelle = total_immo_incorporelle + balance

	# -----------------------------------
	# Brevets, licences, logiciels, et  droits similaires	212, 213, 214, 2193   2812, 2813, 2814, 2912, 2913, 2914, 2919
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:4] == "2193" or item_balance["numero_compte"][0:3] in ("212", "213", "214"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AF",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:4] in ("2812", "2813", "2814", "2912", "2913", "2914", "2919"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AF",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AF",
		"libelle" : "Brevets, licences, logiciels, et  droits similaires",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_incorporelle_brut = total_immo_incorporelle_brut + brut
	total_immo_incorporelle_amort = total_immo_incorporelle_amort + amort
	total_immo_incorporelle = total_immo_incorporelle + balance

	# -----------------------------------
	# Fonds commercial et droit au bail 215, 216     2815, 2816, 2915, 2916
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] in ("215", "216"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AG",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:4] in ("2815", "2816", "2915", "2916"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AG",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AG",
		"libelle" : "Fonds commercial et droit au bail",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_incorporelle_brut = total_immo_incorporelle_brut + brut
	total_immo_incorporelle_amort = total_immo_incorporelle_amort + amort
	total_immo_incorporelle = total_immo_incorporelle + balance

	# -----------------------------------
	# Autres immobilisations incorporelles 217, 218(sauf 2181), 2198   			2817, 2818, 2917, 2918,
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] in ("217", "218") and item_balance["numero_compte"][0:4] != "2181" or item_balance["numero_compte"][0:4] == "2198":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:4] in ("2817", "2818", "2917", "2918"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AH",
		"libelle" : "Autres immobilisations incorporelles",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_incorporelle_brut = total_immo_incorporelle_brut + brut
	total_immo_incorporelle_amort = total_immo_incorporelle_amort + amort
	total_immo_incorporelle = total_immo_incorporelle + balance

	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AD":
			item_bilan["brut"] = total_immo_incorporelle_brut
			item_bilan["amort"] = total_immo_incorporelle_amort
			item_bilan["balance_n"] = total_immo_incorporelle
			item_bilan["balance_n"] = total_immo_incorporelle

	# -----------------------------------
	# TOTAL IMMOBILISATIONS CORPORELLES
	item = {
		"reference" : "AI",
		"libelle" : "IMMOBILISATIONS CORPORELLES",
		"note" : "3",
		"est_total" : True,
		"brut" : "%.2f" % total_immo_corporelle_brut,
		"amort" : "%.2f" % total_immo_corporelle_amort,
		"balance_n" : "%.2f" % total_immo_corporelle,
		"balance_n1" : "%.2f" % total_immo_corporelle
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	# "Terrains (1)
	# dont Placement Net:" 22        282, 292
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "22":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] in ("282", "292"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AJ",
		"libelle" : "Terrains (1) dont Placement Net:",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_corporelle_brut = total_immo_corporelle_brut + brut
	total_immo_corporelle_amort = total_immo_corporelle_amort + amort
	total_immo_corporelle = total_immo_corporelle + balance

	# -----------------------------------
	# "Bâtiments (1)
	#	dont Placement Net:" 231, 232, 233, 237, 2391, 2392, 2393            2831, 2832, 2833, 2837, 2931, 2932, 2933, 2937, 2939
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] in ("231", "232", "233", "237") or item_balance["numero_compte"][0:4] in ("2391", "2392", "2393"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AK",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:4] in ("2831", "2832", "2833", "2837", "2931", "2932", "2933", "2937", "2939"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AK",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AK",
		"libelle" : "Bâtiments (1) dont Placement Net:",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_corporelle_brut = total_immo_corporelle_brut + brut
	total_immo_corporelle_amort = total_immo_corporelle_amort + amort
	total_immo_corporelle = total_immo_corporelle + balance

	# -----------------------------------
	# Aménagements, agencements et installations 234, 235, 238, 239(sauf 2391, 2392, 2393)      283 (sauf 2831, 2832, 2833, 2837) 2939
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] in ("234", "235", "238", "239") and item_balance["numero_compte"][0:4] in ("2391", "2392", "2393"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AL",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "283" and item_balance["numero_compte"][0:4] not in ("2831", "2832", "2833", "2837") or item_balance["numero_compte"][0:4] == "2939" :
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AL",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AL",
		"libelle" : "Aménagements, agencements et installations",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_corporelle_brut = total_immo_corporelle_brut + brut
	total_immo_corporelle_amort = total_immo_corporelle_amort + amort
	total_immo_corporelle = total_immo_corporelle + balance

	# -----------------------------------
	# Matériel, mobilier et actifs biologiques 24 (sauf 245 et 2495)    284 (sauf 2845), 294 (sauf 2945 et 2949)
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "24" and item_balance["numero_compte"][0:3] != "245" and item_balance["numero_compte"][0:4] != "2495":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AM",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] in ("284", "294") and item_balance["numero_compte"][0:4] not in ("2845", "2945", "2949"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AM",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AM",
		"libelle" : "Matériel, mobilier et actifs biologiques",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_corporelle_brut = total_immo_corporelle_brut + brut
	total_immo_corporelle_amort = total_immo_corporelle_amort + amort
	total_immo_corporelle = total_immo_corporelle + balance

	# -----------------------------------
	# Matériel de transport 245, 2495   2845, 2945, 2949
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] == "245" or item_balance["numero_compte"][0:4] == "2495":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AN",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:4] in ("2845", "2945", "2949"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AN",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AN",
		"libelle" : "Matériel de transport",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_corporelle_brut = total_immo_corporelle_brut + brut
	total_immo_corporelle_amort = total_immo_corporelle_amort + amort
	total_immo_corporelle = total_immo_corporelle + balance

	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AI":
			item_bilan["brut"] = total_immo_corporelle_brut
			item_bilan["amort"] = total_immo_corporelle_amort
			item_bilan["balance_n"] = total_immo_corporelle
			item_bilan["balance_n"] = total_immo_corporelle

	# -----------------------------------
	# AVANCES ET ACOMPTES VERSES SUR IMMOBILISATIONS 25  295
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "25":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AP",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "295":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AP",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AP",
		"libelle" : "AVANCES ET ACOMPTES VERSES SUR IMMOBILISATIONS",
		"note" : "3",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_actif_immobilise_brut = total_actif_immobilise_brut + brut
	total_actif_immobilise_amort = total_actif_immobilise_amort + amort
	total_actif_immobilise = total_actif_immobilise + balance

	# -----------------------------------
	# TOTAL IMMOBILISATIONS FINANCIERES
	item = {
		"reference" : "AQ",
		"libelle" : "IMMOBILISATIONS FINANCIERES",
		"note" : "4",
		"est_total" : True,
		"brut" : "%.2f" % total_immo_financiere_brut,
		"amort" : "%.2f" % total_immo_financiere_amort,
		"balance_n" : "%.2f" % total_immo_financiere,
		"balance_n1" : "%.2f" % total_immo_financiere
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	# Titres de participation 26  296
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "26":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AR",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "296":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AR",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AR",
		"libelle" : "Titres de participation",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_financiere_brut = total_immo_financiere_brut + brut
	total_immo_financiere_amort = total_immo_financiere_amort + amort
	total_immo_financiere = total_immo_financiere + balance

	# -----------------------------------
	# Autres immobilisations financières 27  297
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "27":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AS",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "297":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "AS",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "AS",
		"libelle" : "Autres immobilisations financières",
		"note" : "",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_immo_financiere_brut = total_immo_financiere_brut + brut
	total_immo_financiere_amort = total_immo_financiere_amort + amort
	total_immo_financiere = total_immo_financiere + balance

	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AQ":
			item_bilan["brut"] = total_immo_financiere_brut
			item_bilan["amort"] = total_immo_financiere_amort
			item_bilan["balance_n"] = total_immo_financiere
			item_bilan["balance_n"] = total_immo_financiere

	# -----------------------------------
	# TOTAL ACTIF IMMOBILISE 	SOMME NOTE 1, 2, 3 et 4

	total_actif_immobilise_brut = total_actif_immobilise_brut + total_immo_financiere_brut + total_immo_incorporelle_brut + total_immo_corporelle_brut
	total_actif_immobilise_amort = total_actif_immobilise_amort + total_immo_financiere_amort + total_immo_incorporelle_amort + total_immo_corporelle_amort
	total_actif_immobilise = total_actif_immobilise + total_immo_financiere + total_immo_incorporelle + total_immo_corporelle

	item = {
		"reference" : "AZ",
		"libelle" : "TOTAL ACTIF IMMOBILISE",
		"note" : "",
		"est_total" : True,
		"brut" : "%.2f" % total_actif_immobilise_brut,
		"amort" : "%.2f" % total_actif_immobilise_amort,
		"balance_n" : "%.2f" % total_actif_immobilise,
		"balance_n1" : "%.2f" % total_actif_immobilise
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	# ACTIF CIRCULANT HAO 485, 486, 488    498
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] in ("485", "486", "488"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BA",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "498":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BA",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BA",
		"libelle" : "ACTIF CIRCULANT HAO",
		"note" : "5",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_actif_circulant_brut = total_actif_circulant_brut + brut
	total_actif_circulant_amort = total_actif_circulant_amort + amort
	total_actif_circulant = total_actif_circulant + balance

	# -----------------------------------
	# STOCKS ET ENCOURS 31, 32, 33, 34, 36, 37, 38     39
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] in ("31", "32", "33", "34", "36", "37", "38"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BB",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:2] == "39":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BB",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BB",
		"libelle" : "STOCKS ET ENCOURS",
		"note" : "6",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_actif_circulant_brut = total_actif_circulant_brut + brut
	total_actif_circulant_amort = total_actif_circulant_amort + amort
	total_actif_circulant = total_actif_circulant + balance

	# -----------------------------------
	# CREANCES ET EMPLOIS ASSIMILES
	item = {
		"reference" : "BG",
		"libelle" : "CREANCES ET EMPLOIS ASSIMILES",
		"note" : "",
		"est_total" : True,
		"brut" : "%.2f" % creances_emplois_brut,
		"amort" : "%.2f" % creances_emplois_amort,
		"balance_n" : "%.2f" % creances_emplois,
		"balance_n1" : "%.2f" % creances_emplois
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	#  Fournisseurs avances versées	40 	490
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "40":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "490":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BH",
		"libelle" : "Fournisseurs avances versées",
		"note" : "17",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	creances_emplois_brut = creances_emplois_brut + brut
	creances_emplois_amort = creances_emplois_amort + amort
	creances_emplois = creances_emplois + balance

	# -----------------------------------
	#  Clients	41 (sauf 419)	491
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "41" and item_balance["numero_compte"][0:3] != "419":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BI",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "491":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BI",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BI",
		"libelle" : "Clients",
		"note" : "7",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	creances_emplois_brut = creances_emplois_brut + brut
	creances_emplois_amort = creances_emplois_amort + amort
	creances_emplois = creances_emplois + balance

	# -----------------------------------
	#  Autres créances	Soldes débiteurs : (185, 186, 187, 188), 42, 43, 44, 45, 46, 47 (sauf 478)	492, 493, (494) 495, 496, 497
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] in ("42", "43", "44", "45", "46", "47") and item_balance["numero_compte"][0:3] != "478":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] in ("492", "493", "495", "496", "497"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BJ",
		"libelle" : "Autres créances",
		"note" : "8",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	creances_emplois_brut = creances_emplois_brut + brut
	creances_emplois_amort = creances_emplois_amort + amort
	creances_emplois = creances_emplois + balance

	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BG":
			item_bilan["brut"] = creances_emplois_brut
			item_bilan["amort"] = total_immo_financiere_amort
			item_bilan["balance_n"] = creances_emplois
			item_bilan["balance_n"] = creances_emplois

	# -----------------------------------
	# TOTAL ACTIF CIRCULANT

	total_actif_circulant_brut = total_actif_circulant_brut + creances_emplois_brut
	total_actif_circulant_amort = total_actif_circulant_amort + creances_emplois_amort
	total_actif_circulant = total_actif_circulant + creances_emplois

	item = {
		"reference" : "BK",
		"libelle" : "TOTAL ACTIF CIRCULANT",
		"note" : "",
		"est_total" : True,
		"brut" : "%.2f" % total_actif_circulant_brut,
		"amort" : "%.2f" % total_actif_circulant_amort,
		"balance_n" : "%.2f" % total_actif_circulant,
		"balance_n1" : "%.2f" % total_actif_circulant
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	# Titres de placement 	50	590
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "50":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BQ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "590":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BQ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BQ",
		"libelle" : "Titres de placement",
		"note" : "9",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_tresorerie_actif_brut = total_tresorerie_actif_brut + brut
	total_tresorerie_actif_amort = total_tresorerie_actif_amort + amort
	total_tresorerie_actif = total_tresorerie_actif + balance

	# -----------------------------------
	# Valeurs à encaisser 	51	591
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2] == "51":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BR",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] == "591":
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BR",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BR",
		"libelle" : "Valeurs à encaisser",
		"note" : "10",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_tresorerie_actif_brut = total_tresorerie_actif_brut + brut
	total_tresorerie_actif_amort = total_tresorerie_actif_amort + amort
	total_tresorerie_actif = total_tresorerie_actif + balance

	# -----------------------------------
	# Banques, chèques postaux, caisse et assimilés Soldes débiteurs : 52, 53, 54, (55) 57, 581, 582	592, 593, 594
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:2]  in ("52", "53", "54","55", "57") or item_balance["numero_compte"][0:3] in ("581", "582"):
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BS",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		elif item_balance["numero_compte"][0:3] in ("592", "592", "594"):
			solde = float(item_balance["credit_solde"])
			amort = amort + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BS",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": True,
				"balance" : solde,
			}
			comptes.append(compte)
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BS",
		"libelle" : "Banques, chèques postaux, caisse et assimilés",
		"note" : "11",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_tresorerie_actif_brut = total_tresorerie_actif_brut + brut
	total_tresorerie_actif_amort = total_tresorerie_actif_amort + amort
	total_tresorerie_actif = total_tresorerie_actif + balance

	# -----------------------------------
	# TOTAL TRESORERIE-ACTIF
	item = {
		"reference" : "BT",
		"libelle" : "TOTAL TRESORERIE-ACTIF",
		"note" : "",
		"est_total" : True,
		"brut" : "%.2f" % total_tresorerie_actif_brut,
		"amort" : "%.2f" % total_tresorerie_actif_amort,
		"balance_n" : "%.2f" % total_tresorerie_actif,
		"balance_n1" : "%.2f" % total_tresorerie_actif
	}
	donnees_bilan_actif.append(item)

	# ---------------------------------------------------
	# Ecart de conversion-Actif 478
	brut = 0
	amort = 0
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le brut
		if item_balance["numero_compte"][0:3] == "478":
			solde = float(item_balance["debit_solde"])
			brut = brut + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "BU",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"est_amort": False,
				"balance" : solde,
			}
			comptes.append(compte)
		#Pour l' amortissement et dépreciation
		amort = 0.0
	balance = float(brut) - float(amort)
	item = {
		"reference" : "BU",
		"libelle" : "Ecart de conversion-Actif",
		"note" : "12",
		"est_total" : False,
		"brut" : "%.2f" % brut,
		"amort" : "%.2f" % amort,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_actif.append(item)

	total_general_actif_brut = total_general_actif_brut + brut
	total_general_actif_amort = total_general_actif_amort + amort
	total_general_actif = total_general_actif + balance

	# -----------------------------------
	# TOTAL GENERAL

	total_general_actif_brut = total_general_actif_brut + total_tresorerie_actif_brut + total_actif_circulant_brut + total_actif_immobilise_brut
	total_general_actif_amort = total_general_actif_amort + total_tresorerie_actif_amort + total_actif_circulant_amort + total_actif_immobilise_amort
	total_general_actif = total_general_actif + total_tresorerie_actif + total_actif_circulant + total_actif_immobilise

	item = {
		"reference" : "BZ",
		"libelle" : "TOTAL GENERAL",
		"note" : "",
		"est_total" : True,
		"brut" : "%.2f" % total_general_actif_brut,
		"amort" : "%.2f" % total_general_actif_amort,
		"balance_n" : "%.2f" % total_general_actif,
		"balance_n1" : "%.2f" % total_general_actif
	}
	donnees_bilan_actif.append(item)

	# -----------------------------------
	#	FIN TRAITEMENT BILAN ACTIF
	# -----------------------------------

	# -----------------------------------
	#	TRAITEMENT BILAN PASSIF
	# -----------------------------------

	total_capitaux = 0
	total_dettes = 0
	total_ressources_stables = 0
	total_passif_circulant = 0
	total_tresorerie_passif = 0
	total_general_passif = 0

	# -----------------------------------
	# Capital 101, 102, 103, 104
	#
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] in ("101", "102", "103", "104"):
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CA",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CA",
		"libelle" : "Capital",
		"note" : "13",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Apporteurs capital non appelé (-) 	109
	#
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "109":
			solde = float(item_balance["credit_solde"]) - float(item_balance["debit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CB",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CB",
		"libelle" : "Apporteurs capital non appelé (-)",
		"note" : "13",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Primes liées au capital social	105
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "105":
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CD",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CD",
		"libelle" : "Primes liées au capital social",
		"note" : "14",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Ecarts de réévaluation 106
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "106":
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CE",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CE",
		"libelle" : "Ecarts de réévaluation",
		"note" : "3E",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Réserves indisponibles 111, 112, 113
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] in ("111", "112", "113") :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CF",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CF",
		"libelle" : "Réserves indisponibles",
		"note" : "14",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Réserves libres 118
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "118" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CG",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CG",
		"libelle" : "Réserves libres",
		"note" : "14",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Report à nouveau (+ ou -) 121 129
	balance = 0
	balance_n1 = 0
	debit = 0
	credit = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "121" :
			solde = float(item_balance["credit_solde"])
			credit = credit + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
		elif item_balance["numero_compte"][0:3] == "129" :
			solde = float(item_balance["debit_solde"])
			debit = debit + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = credit - debit
	item = {
		"reference" : "CH",
		"libelle" : "Report à nouveau (+ ou -)",
		"note" : "14",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Résultat net de l'exercice (bénéfice + ou perte -) 139
	balance = 0
	balance_n1 = 0
	resultat = 0
	for cr in donnees_compte_resultat:
		if cr["reference"] == "XI": resultat = makeFloat(cr["balance_n"])
	#print("RESUTAT {}".format(resultat))
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "139" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	#balance = resultat
	item = {
		"reference" : "CJ",
		"libelle" : "Résultat net de l'exercice (bénéfice + ou perte -)",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % resultat,
		"balance_n1" : "%.2f" % resultat
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + resultat

	# -----------------------------------
	# Subventions  d'investissement 14
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] == "14" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CL",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CL",
		"libelle" : "Subventions  d'investissement",
		"note" : "15",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# Provisions  réglementées 15
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] == "15" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "CM",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "CM",
		"libelle" : "Provisions  réglementées",
		"note" : "15",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_capitaux = total_capitaux + balance

	# -----------------------------------
	# TOTAL CAPITAUX PROPRES ET RESSOURCES ASSIMILEES
	item = {
		"reference" : "CP",
		"libelle" : "TOTAL CAPITAUX PROPRES ET RESSOURCES ASSIMILEES",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % total_capitaux,
		"balance_n1" : "%.2f" % total_capitaux
	}
	donnees_bilan_passif.append(item)

	# -----------------------------------
	# Emprunts et dettes financières diverses 161, 162, 163, 164, 165, 166, 167, 168, 181, 182, 183, 184
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] in ("161", "162", "163", "164", "165", "166", "167", "168", "181", "182", "183", "184") :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DA",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DA",
		"libelle" : "Emprunts et dettes financières diverses",
		"note" : "16",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_dettes = total_dettes + balance

	# -----------------------------------
	# Dettes de location-acquisition 17
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] == "17" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DB",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DB",
		"libelle" : "Dettes de location-acquisition",
		"note" : "16",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_dettes = total_dettes + balance

	# -----------------------------------
	# Provisions pour risques et charges 19
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] == "19" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DC",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DC",
		"libelle" : "Provisions  réglementées",
		"note" : "16",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_dettes = total_dettes + balance

	# -----------------------------------
	# TOTAL  DETTES FINANCIERES ET  RESSOURCES ASSIMILEES
	item = {
		"reference" : "DD",
		"libelle" : "TOTAL  DETTES FINANCIERES ET  RESSOURCES ASSIMILEES",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % total_dettes,
		"balance_n1" : "%.2f" % total_dettes
	}
	donnees_bilan_passif.append(item)

	# -----------------------------------
	# TOTAL  RESSOURCES STABLES
	total_ressources_stables = total_capitaux + total_dettes
	item = {
		"reference" : "DF",
		"libelle" : "TOTAL  RESSOURCES STABLES",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % total_ressources_stables,
		"balance_n1" : "%.2f" % total_ressources_stables
	}
	donnees_bilan_passif.append(item)

	# -----------------------------------
	# Dettes circulantes HAO 481, 482, 484, 488, 4998
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] in ("481", "482", "484") or item_balance["numero_compte"][0:4] == "4998":
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#print("DH {}".format(balance))
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DH",
		"libelle" : "Dettes circulantes HAO",
		"note" : "5",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	#print("DH {}".format(balance))
	donnees_bilan_passif.append(item)
	total_passif_circulant = total_passif_circulant + balance

	# -----------------------------------
	# Clients, avances reçues 41
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] == "41" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DI",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DI",
		"libelle" : "Clients, avances reçues",
		"note" : "7",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_passif_circulant = total_passif_circulant + balance

	# -----------------------------------
	# Fournisseurs d'exploitation 40
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] == "40" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DJ",
		"libelle" : "Fournisseurs d'exploitation",
		"note" : "17",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_passif_circulant = total_passif_circulant + balance

	# -----------------------------------
	# Dettes fiscales et sociales 	Soldes créditeurs : 42, 43, 44
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] in ("42", "43", "44") :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DK",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DK",
		"libelle" : "Dettes fiscales et sociales",
		"note" : "18",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_passif_circulant = total_passif_circulant + balance

	# -----------------------------------
	# Autres dettes   Soldes créditeurs : 185 (186, 187, 188) 45, 46, 47 (sauf 479)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:2] in ("45", "46", "47") and item_balance["numero_compte"][0:3] != "479" or item_balance["numero_compte"][0:3] == "185" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DM",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DM",
		"libelle" : "Autres dettes",
		"note" : "19",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_passif_circulant = total_passif_circulant + balance

	# -----------------------------------
	# Provisions pour risques et charges à court terme   499 (sauf 4998), 599
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "499" and item_balance["numero_compte"][0:4] != "4998" or item_balance["numero_compte"][0:3] == "599":
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DN",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DN",
		"libelle" : "Provisions pour risques et charges à court terme",
		"note" : "19",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_passif_circulant = total_passif_circulant + balance

	# -----------------------------------
	# TOTAL PASSIF CIRCULANT
	item = {
		"reference" : "DP",
		"libelle" : "TOTAL PASSIF CIRCULANT",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % total_passif_circulant,
		"balance_n1" : "%.2f" % total_passif_circulant
	}
	donnees_bilan_passif.append(item)

	# -----------------------------------
	# Banques,  crédits d'escompte  564, 565
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] in ("564", "565") :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DQ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DQ",
		"libelle" : "Banques,  crédits d'escompte",
		"note" : "20",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_tresorerie_passif = total_tresorerie_passif + balance

	# -----------------------------------
	# 	Banques, établissements financiers et crédits de trésorerie	   Soldes créditeurs : 52, 53, 561, 566
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] in ("52", "53") or item_balance["numero_compte"][0:3] in ("561", "566"):
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DR",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DR",
		"libelle" : "Banques, établissements financiers et crédits de trésorerie",
		"note" : "20",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_tresorerie_passif = total_tresorerie_passif + balance

	# -----------------------------------
	# TOTAL TRESORERIE-PASSIF
	item = {
		"reference" : "DT",
		"libelle" : "TOTAL TRESORERIE-PASSIF",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % total_tresorerie_passif,
		"balance_n1" : "%.2f" % total_tresorerie_passif
	}
	donnees_bilan_passif.append(item)

	# -----------------------------------
	# 	Ecart de conversion-Passif	   479
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		#Pour le net
		if item_balance["numero_compte"][0:3] == "479" :
			solde = float(item_balance["credit_solde"])
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le bilan
			compte = {
				"reference" : "DV",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "DV",
		"libelle" : "Ecart de conversion-Passif",
		"note" : "12",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_bilan_passif.append(item)
	total_general_passif = total_tresorerie_passif + total_passif_circulant + total_ressources_stables + balance

	# -----------------------------------
	# TOTAL GENERAL
	item = {
		"reference" : "DZ",
		"libelle" : "TOTAL GENERAL",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % total_general_passif,
		"balance_n1" : "%.2f" % total_general_passif
	}
	donnees_bilan_passif.append(item)


	# -----------------------------------
	#	FIN TRAITEMENT BILAN PASSIF
	# -----------------------------------


	#print("donnees_bilan_actif {}".format(donnees_bilan_actif))
	#print("donnees_bilan_passif {}".format(donnees_bilan_passif))

	context = {
		'title' : "Bilan",
		"donnees_bilan_actif" : donnees_bilan_actif,
		"donnees_bilan_passif" : donnees_bilan_passif,
		"comptes": comptes,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules ,
		"module" : enum_module,
		'format' : 'portrait',
		'modules' : modules,
		'sous_modules': sous_modules,
		'menu' : 9
	}
	return context


@transaction.atomic
def post_generer_bilan(request):
	sid = transaction.savepoint()
	try:
		# droit="GENERER_BILAN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 100
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_bilan(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/bilan/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_bilan"))

def post_imprimer_bilan(request):
	try:
		# droit="IMPRIMER_BILAN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 100
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_bilan(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/bilan.html", "bilan.pdf", context)

	except Exception as e:
		# #print("ERREUR print BILAN")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_bilan"))


# RESULTAT OUTPUT PDF
def get_generer_resultat(request):

	# droit="GENERER_COMPTE_RESULTAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 101
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
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/resultat/generate.html")
	return HttpResponse(template.render(context, request))

def post_traiter_resultat(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction du journal'''
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()

	#On declare les tableaux et variable qui seront renvoyés en output
	donnees_compte_resultat = []
	comptes = []

	marge_commerciale = 0
	chiffre_affaire = 0
	valeur_ajoutee = 0
	excedent_brut = 0
	resultat_exploitation = 0
	resultat_financier = 0
	resultat_ao = 0
	resultat_hao = 0
	resultat_net = 0

	#On récupère les données de la balance de la periode
	donnees_balance = balanceArray.toGetInPeriode(date_debut, date_fin, devise)
	#TODO Garder que les comptes des charges et produits pour optimisation

	# -----------------------------------
	# Calcul Ventes de marchandises (701)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "701":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TA",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TA",
		"libelle" : "Ventes de marchandises",
		"lettre" : "A",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	marge_commerciale = marge_commerciale + balance
	chiffre_affaire = chiffre_affaire + balance
	#print("Ligne 1")
	# -----------------------------------
	# Calcul Achats de marchandises (601)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "601":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RA",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RA",
		"libelle" : "Achats de marchandises",
		"lettre" : "",
		"signe" : "-",
		"note" : "22",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	marge_commerciale = marge_commerciale + balance
	valeur_ajoutee = valeur_ajoutee + balance
	#print("Ligne 2")
	# -----------------------------------
	# Calcul Variation  de stocks de marchandises (6031)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6031":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RB",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RB",
		"libelle" : "Variation  de stocks de marchandises",
		"lettre" : "",
		"signe" : "+/-",
		"note" : "6",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	marge_commerciale = marge_commerciale + balance
	valeur_ajoutee = valeur_ajoutee + balance
	#print("Ligne 3")
	# -----------------------------------
	# Calcul MARGE COMMERCIALE (Somme TA à RB)
	item = {
		"reference" : "XA",
		"libelle" : "MARGE COMMERCIALE (Somme TA à RB)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % marge_commerciale,
		"balance_n1" : "%.2f" % marge_commerciale
	}
	donnees_compte_resultat.append(item)

	# -----------------------------------
	# Ventes de produits fabriqués (702, 703, 704)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "702" or item_balance["numero_compte"][0:3] == "703" or item_balance["numero_compte"][0:3] == "704":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TB",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TB",
		"libelle" : "Ventes de produits fabriqués",
		"lettre" : "B",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	chiffre_affaire = chiffre_affaire + balance

	# -----------------------------------
	# Travaux, services vendus (705, 706)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "705" or item_balance["numero_compte"][0:3] == "706":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TC",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TC",
		"libelle" : "Travaux, services vendus",
		"lettre" : "C",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	chiffre_affaire = chiffre_affaire + balance

	# -----------------------------------
	# Produits accessoires (707)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "707":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TD",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TD",
		"libelle" : "Produits accessoires",
		"lettre" : "D",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	chiffre_affaire = chiffre_affaire + balance

	# -----------------------------------
	# CHIFFRES D’AFFAIRES (A + B + C+ D)
	item = {
		"reference" : "XB",
		"libelle" : "CHIFFRES D’AFFAIRES (A + B + C+ D)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % chiffre_affaire,
		"balance_n1" : "%.2f" % chiffre_affaire
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + chiffre_affaire

	# -----------------------------------
	# Production stockée (ou déstockage) (73)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "73":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TE",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TE",
		"libelle" : "Production stockée (ou déstockage)	",
		"lettre" : "",
		"signe" : "+/-",
		"note" : "6",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Production immobilisée (72)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "72":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TF",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TF",
		"libelle" : "Production immobilisée",
		"lettre" : "",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Subventions d’exploitation (71)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "71":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TG",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TG",
		"libelle" : "Subventions d’exploitation",
		"lettre" : "",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Autres produits	 (75)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "75":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TH",
		"libelle" : "Autres produits",
		"lettre" : "",
		"signe" : "+",
		"note" : "21",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Transferts de charges d'exploitation (781)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "781":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TI",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TI",
		"libelle" : "Transferts de charges d'exploitation",
		"lettre" : "",
		"signe" : "+",
		"note" : "12",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Achats de matières premières et fournitures liées (602)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "602":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RC",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RC",
		"libelle" : "Achats de matières premières et fournitures liées",
		"lettre" : "",
		"signe" : "-",
		"note" : "22",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Variation de stocks de matières premières et fournitures liées (6032)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6032":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RD",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RD",
		"libelle" : "Variation de stocks de matières premières et fournitures liées",
		"lettre" : "",
		"signe" : "+/-",
		"note" : "6",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	marge_commerciale = marge_commerciale + balance
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Autres achats (604, 605, 608)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "604" or item_balance["numero_compte"][0:3] == "605" or item_balance["numero_compte"][0:3] == "608":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RE",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RE",
		"libelle" : "Autres achats",
		"lettre" : "",
		"signe" : "-",
		"note" : "22",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Variation de stocks d’autres approvisionnements (6033)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6033":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RF",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RF",
		"libelle" : "Variation de stocks d’autres approvisionnements",
		"lettre" : "",
		"signe" : "+/-",
		"note" : "6",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Transports (61)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "61":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RG",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RG",
		"libelle" : "Transports",
		"lettre" : "",
		"signe" : "-",
		"note" : "23",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Services extérieurs (62, 63)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "62" or item_balance["numero_compte"][0:2] == "63":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RH",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RH",
		"libelle" : "Achats de marchandises",
		"lettre" : "",
		"signe" : "-",
		"note" : "24",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Impôts et taxes (64)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "64":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RI",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RI",
		"libelle" : "Impôts et taxes",
		"lettre" : "",
		"signe" : "-",
		"note" : "25",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance

	# -----------------------------------
	# Autres charges (65)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "65":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RJ",
		"libelle" : "Autres charges",
		"lettre" : "",
		"signe" : "-",
		"note" : "26",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	valeur_ajoutee = valeur_ajoutee + balance


	# -----------------------------------
	# VALEUR AJOUTEE (XB +RA+RB) + (somme TE à RJ)
	item = {
		"reference" : "XC",
		"libelle" : "VALEUR AJOUTEE (XB +RA+RB) + (somme TE à RJ)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % valeur_ajoutee,
		"balance_n1" : "%.2f" % valeur_ajoutee
	}
	donnees_compte_resultat.append(item)
	excedent_brut = excedent_brut + valeur_ajoutee

	# -----------------------------------
	# Charges de personnel (66)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "66":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RK",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RK",
		"libelle" : "Charges de personnel",
		"lettre" : "",
		"signe" : "-",
		"note" : "27",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	excedent_brut = excedent_brut + balance

	# -----------------------------------
	# EXCEDENT BRUT D'EXPLOITATION (XC+RK)
	item = {
		"reference" : "XD",
		"libelle" : "EXCEDENT BRUT D'EXPLOITATION (XC+RK)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % excedent_brut,
		"balance_n1" : "%.2f" % excedent_brut
	}
	donnees_compte_resultat.append(item)
	resultat_exploitation = resultat_exploitation + excedent_brut

	# -----------------------------------
	# Reprises d’amortissements, provisions et dépréciations (794, 798)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "791" or item_balance["numero_compte"][0:3] == "798" or item_balance["numero_compte"][0:3] == "799":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TJ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TJ",
		"libelle" : "Reprises d’amortissements, provisions et dépréciations",
		"lettre" : "",
		"signe" : "+",
		"note" : "28",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_exploitation = resultat_exploitation + balance

	# -----------------------------------
	# Dotations aux amortissements, aux provisions et dépréciations (681, 691)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "681" or item_balance["numero_compte"][0:3] == "691":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RL",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RL",
		"libelle" : "Dotations aux amortissements, aux provisions et dépréciations",
		"lettre" : "",
		"signe" : "-",
		"note" : "3C&28",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_exploitation = resultat_exploitation + balance

	# -----------------------------------
	# RESULTAT D'EXPLOITATION (XD + TJ + RL)
	item = {
		"reference" : "XE",
		"libelle" : "RESULTAT D'EXPLOITATION (XD + TJ + RL)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % resultat_exploitation,
		"balance_n1" : "%.2f" % resultat_exploitation
	}
	donnees_compte_resultat.append(item)

	# -----------------------------------
	# Revenus financiers et assimilés (77)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "77":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TK",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TK",
		"libelle" : "Revenus financiers et assimilés",
		"lettre" : "",
		"signe" : "+",
		"note" : "29",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_financier = resultat_financier + balance

	# -----------------------------------
	# Reprises de provisions et dépréciations financières (797)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "797":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TL",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TL",
		"libelle" : "Reprises de provisions et dépréciations financières",
		"lettre" : "",
		"signe" : "+",
		"note" : "28",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_financier = resultat_financier + balance

	# -----------------------------------
	# Transferts de charges financières (787)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "787":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TM",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TM",
		"libelle" : "Transferts de charges financières",
		"lettre" : "",
		"signe" : "+",
		"note" : "12",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_financier = resultat_financier + balance

	# -----------------------------------
	# Frais financiers et charges assimilées (67)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "67":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RM",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RM",
		"libelle" : "Frais financiers et charges assimilées",
		"lettre" : "",
		"signe" : "-",
		"note" : "29",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_financier = resultat_financier + balance

	# -----------------------------------
	# Dotations aux provisions et aux dépréciations financières (687, 697)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "687" or item_balance["numero_compte"][0:3] == "697":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RN",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RN",
		"libelle" : "Dotations aux provisions et aux dépréciations financières",
		"lettre" : "",
		"signe" : "-",
		"note" : "3C&28",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_financier = resultat_financier + balance

	# -----------------------------------
	# RESULTAT FINANCIER (Somme TK à RN)
	item = {
		"reference" : "XF",
		"libelle" : "RESULTAT FINANCIER (Somme TK à RN)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % resultat_financier,
		"balance_n1" : "%.2f" % resultat_financier
	}
	donnees_compte_resultat.append(item)

	# -----------------------------------
	# RESULTAT  DES ACTIVITES ORDINAIRES (XE+XF)
	resultat_ao = resultat_exploitation + resultat_financier
	item = {
		"reference" : "XG",
		"libelle" : "RESULTAT  DES ACTIVITES ORDINAIRES (XE+XF)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % resultat_ao,
		"balance_n1" : "%.2f" % resultat_ao
	}
	donnees_compte_resultat.append(item)
	resultat_net = resultat_net + resultat_ao

	# -----------------------------------
	# Produits des cessions d'immobilisations (82)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "82":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TN",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TN",
		"libelle" : "Produits des cessions d'immobilisations",
		"lettre" : "",
		"signe" : "+",
		"note" : "3D",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_hao = resultat_hao + balance

	# -----------------------------------
	# Autres Produits HAO (84, 86)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "84" or item_balance["numero_compte"][0:2] == "86":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "TO",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "TO",
		"libelle" : "Autres Produits HAO",
		"lettre" : "",
		"signe" : "+",
		"note" : "30",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_hao = resultat_hao + balance

	# -----------------------------------
	# Valeurs comptables des cessions d'immobilisations (81)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "81":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RO",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RO",
		"libelle" : "Valeurs comptables des cessions d'immobilisations",
		"lettre" : "",
		"signe" : "-",
		"note" : "3D",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_hao = resultat_hao + balance

	# -----------------------------------
	# Autres Charges HAO (83, 85)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "83" or item_balance["numero_compte"][0:2] == "85":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RP",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RP",
		"libelle" : "Autres Charges HAO",
		"lettre" : "",
		"signe" : "-",
		"note" : "30",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_hao = resultat_hao + balance

	# -----------------------------------
	# RESULTAT HORS ACTIVITES ORDINAIRES (somme TN à RP)
	item = {
		"reference" : "XH",
		"libelle" : "RESULTAT HORS ACTIVITES ORDINAIRES (somme TN à RP)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % resultat_hao,
		"balance_n1" : "%.2f" % resultat_hao
	}
	donnees_compte_resultat.append(item)
	resultat_net = resultat_net + resultat_hao

	# -----------------------------------
	# Participations des travailleurs (87)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "87":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RQ",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RQ",
		"libelle" : "Participations des travailleurs",
		"lettre" : "",
		"signe" : "-",
		"note" : "30",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_net = resultat_net + balance

	# -----------------------------------
	# Impôts sur le résultat (89)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "89":
			solde = - (float(item_balance["debit_solde"]) - float(item_balance["credit_solde"]))
			balance = balance + solde
			#On enregistre aussi les comptes qui entrent en jeu dans le compte de resultat
			compte = {
				"reference" : "RS",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "RS",
		"libelle" : "Impôts sur le résultat",
		"lettre" : "",
		"signe" : "-",
		"note" : "37",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_compte_resultat.append(item)
	resultat_net = resultat_net + balance

	# -----------------------------------
	# RESULTAT NET (XG + XH +RQ + RS)
	item = {
		"reference" : "XI",
		"libelle" : "RESULTAT NET (XG + XH +RQ + RS)",
		"lettre" : "",
		"signe" : "",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % resultat_net,
		"balance_n1" : "%.2f" % resultat_net
	}
	donnees_compte_resultat.append(item)
	#print("donnees compte resultat: {}".format(donnees_compte_resultat))

	context = {
		'title' : "Compte de résultat",
		"model" : donnees_compte_resultat,
		"comptes" : comptes,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules ,
		"module" : enum_module,
		'format' : 'portrait',
		'modules' : modules,
		'sous_modules': sous_modules,
		'menu' : 9
	}
	return context


def post_generer_resultat(request):
	try:
		# droit="GENERER_COMPTE_RESULTAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 101
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		#print("post_generer_resultat")
		context = post_traiter_resultat(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/resultat/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_resultat"))

def post_imprimer_resultat(request):
	try:
		# droit="IMPRIMER_COMPTE_RESULTAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 101
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_resultat(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/compte_resultat.html", "compte_resultat.pdf", context)

	except Exception as e:
		# #print("ERREUR print COMPTE RESULTAT")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_resultat"))

#  TABLEAU DE BORD DE FLUX DE TRESORERIE
def get_generer_tb_tresorerie(request):

	# droit="GENERER_FLUX_TRESORERIE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 372
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le tableau de bord des flux de trésorerie',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		"modules" : modules ,
		'sous_modules': sous_modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/tb_tresorerie/generate.html")
	return HttpResponse(template.render(context, request))


def post_traiter_tb_tresorerie(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	'''fonction de traitement de calcul pour extraction d'un tableau de tresorerie'''
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()

	#On declare les tableaux et variable qui seront renvoyés en output
	donnees_tb_initial = []
	donnees_tb_operationnel = []
	donnees_tb_investissement = []
	donnees_tb_financement = []
	donnees_tb_final = []
	comptes = []

	tresorerie_initiale = 0

	cafg = 0
	montant_fb_tft = 0
	montant_fd_tft = 0
	montant_fe_tft = 0
	variation_fb_activite_operationnelle = 0
	tresorerie_activite_operationnelle = 0

	decaissement_immo_incorporelle = 0
	decaissement_immo_corporelle = 0
	decaissement_immo_financiere = 0
	encaissement_immobilisation = 0
	encaissement_immo_financiere = 0
	tresorerie_activite_investissement = 0

	augmentation_capital = 0
	subventions_recues = 0
	prelevement_capital = 0
	dividentes_versees = 0
	financement_capitaux_propres = 0
	financement_capitaux_etrangers = 0
	tresorerie_capitaux_propres = 0

	variation_tresorerie_nette = 0
	tresorerie_nette_periode = 0

	tresorerie_finale = 0

	montant_a_equilibre_tft = 0

	#On récupère les données de la balance de la periode
	donnees_balance = balanceArray.toGetInPeriode(date_debut, date_fin, devise)
	#On récupère les données de la balance de la periode
	donnees_compte_resultat = compteResultatArray.toGetOfBalance(donnees_balance)
	#On récupère les données de la balance de la periode
	donnees_bilan_actif, donnees_bilan_passif = bilanArray.toGetOfBalance(donnees_balance, donnees_compte_resultat)

	#TODO Garder que les comptes des charges et produits pour optimisation

	# -----------------------------------
	# Trésorerie-actif de N-1   sid: 50, 51, 52, 53, 54, 57, 581, 582
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("50", "51", "52", "53", "54", "57") or item_balance["numero_compte"][0:3] in ("581", "582"):
			solde = float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "1",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "1",
		"libelle" : "Trésorerie-actif de N-1",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_initial.append(item)
	tresorerie_initiale = tresorerie_initiale + balance

	#print(" etape 1")
	# -----------------------------------
	# Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N-1
	# sid 472 - sic 472
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "472":
			solde = float(item_balance["debit_ouverture"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "2",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "2",
		"libelle" : "Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N-1",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_initial.append(item)
	tresorerie_initiale = tresorerie_initiale + balance

	# -----------------------------------
	# Trésorerie-passif de N-1 sic 52, 53, 564, 565, 561, 566
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("52", "53") or item_balance["numero_compte"][0:3] in ("564", "565", "561", "566"):
			solde = float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "3",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "3",
		"libelle" : "Trésorerie-passif de N-1",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_initial.append(item)
	tresorerie_initiale = tresorerie_initiale + balance

	# -----------------------------------
	# Trésorerie au 1er janvier (A)
	item = {
		"libelle" : "Trésorerie au 1er janvier (A)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_initiale,
		"balance_n1" : "%.2f" % tresorerie_initiale
	}
	donnees_tb_initial.append(item)
	# -----------------------------------
	# Excédent brut d’exploitation (poste XD compte de résultat) Excédent brut d'exploitation dans CR
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "XD":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "4",
		"libelle" : "Excédent brut d’exploitation (poste XD compte de résultat)",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Compte 654 solde débiteur balance N   sfd 654
	#print(" etape 2")
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "654":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "5",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "5",
		"libelle" : "Compte 654 solde débiteur balance N",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Compte 754 solde créditeur balance N 		sfc 754

	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "754":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "6",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "6",
		"libelle" : "Compte 754 solde créditeur balance N",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Résultat financier (poste XF compte de résultat)

	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "XF":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "7",
		"libelle" : "Résultat financier (poste XF compte de résultat)",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Autres produits HAO (poste TO compte de résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "TO":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "8",
		"libelle" : "Autres produits HAO (poste TO compte de résultat)",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance
	#print(" etape 3")
	# -----------------------------------
	# autres charges HAO (poste RP compte de résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "RP":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "9",
		"libelle" : "autres charges HAO (poste RP compte de résultat)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance
	#print(" etape 33")
	# -----------------------------------
	# Participation des travailleurs (poste RQ du compte résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "RQ":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "10",
		"libelle" : "Participation des travailleurs (poste RQ du compte résultat)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance
	#print(" etape 333")
	# -----------------------------------
	# Impôts sur le résultat (poste RS du compte de résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "RS":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "11",
		"libelle" : "Impôts sur le résultat (poste RS du compte de résultat)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance
	#print(" etape 33333")
	# -----------------------------------
	# Capacité d’Autofinancement Globale (CAFG)
	item = {
		"libelle" : "Capacité d’Autofinancement Globale (CAFG)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % cafg,
		"balance_n1" : "%.2f" % cafg
	}
	donnees_tb_operationnel.append(item)
	tresorerie_activite_operationnelle = tresorerie_activite_operationnelle + cafg
	#print("Flux {}".format(tresorerie_activite_operationnelle))

	# -----------------------------------
	# Actif circulant HAO (Poste BA des bilans )
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BA":
			balance = float(item_bilan["balance_n"])
	item = {
		"reference" : "12",
		"libelle" : "Actif circulant HAO (Poste BA des bilans )",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fb_tft = montant_fb_tft + balance

	# -----------------------------------
	# Compte 485 (exlure)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "485":
			solde = item_balance["debit_solde"]
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "13",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "13",
		"libelle" : "Compte 485 (exlure)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_operationnel.append(item)
	montant_fb_tft = montant_fb_tft + balance

	# -----------------------------------
	# Montant affecté au poste FB du TFT
	item = {
		"reference" : "FB",
		"libelle" : "Montant affecté au poste FB du TFT",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_fb_tft,
		"balance_n1" : "%.2f" % montant_fb_tft
	}
	donnees_tb_operationnel.append(item)


	# -----------------------------------
	# Variation des stocks (Poste BB des bilans) Poste FC du TFT
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BB":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "14",
		"libelle" : "Variation des stocks (Poste BB des bilans) Poste FC du TFT",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	variation_fb_activite_operationnelle = - float(montant_fb_tft) + (- float(balance))


	# -----------------------------------
	# Variation des créances  et emplois assimilé (Poste BG des bilans)
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BG":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "15",
		"libelle" : "Variation des créances  et emplois assimilé (Poste BG des bilans)",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance

	# -----------------------------------
	# Variation du compte 478
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "478":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "16",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "16",
		"libelle" : "Variation du compte 478",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 419
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "419":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "17",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "17",
		"libelle" : "Variation du compte 419",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 414
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "414":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "17",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "17",
		"libelle" : "Variation du compte 414",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "19",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "19",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance

	# -----------------------------------
	# Variation du compte 458
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "458":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "20",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "20",
		"libelle" : "Variation du compte 458",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 4494
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4494":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "21",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "21",
		"libelle" : "Variation du compte 4494",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 4751
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4751":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "22",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "22",
		"libelle" : "Variation du compte 4751",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance

	# -----------------------------------
	# Montant affecté au poste FD du TFT
	item = {
		"reference" : "FD",
		"libelle" : "Montant affecté au poste FD du TFT",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_fd_tft,
		"balance_n1" : "%.2f" % montant_fd_tft
	}
	donnees_tb_operationnel.append(item)
	variation_fb_activite_operationnelle = variation_fb_activite_operationnelle + (- float(montant_fd_tft))


	# -----------------------------------
	# Variation du passif circulant (Poste DP des bilans)
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_passif:
		if item_bilan["reference"] == "DP":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "23",
		"libelle" : "Variation du passif circulant (Poste DP des bilans)",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 409
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "409":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "24",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "24",
		"libelle" : "Variation du compte 409",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 404
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "404":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "25",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "25",
		"libelle" : "Variation du compte 404",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance

	# -----------------------------------
	# Variation du compte 481
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "481":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "26",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "26",
		"libelle" : "Variation du compte 481",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 482
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "482":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "27",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "27",
		"libelle" : "Variation du compte 482",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "28",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "28",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 4752
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4752":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "29",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "29",
		"libelle" : "Variation du compte 4752",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 472
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "472":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "30",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "30",
		"libelle" : "Variation du compte 472",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance

	# -----------------------------------
	# Montant affecté au poste FE du TFT
	item = {
		"reference" : "FE",
		"libelle" : "Montant affecté au poste FE du TFT",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_fe_tft,
		"balance_n1" : "%.2f" % montant_fe_tft
	}
	donnees_tb_operationnel.append(item)
	variation_fb_activite_operationnelle = variation_fb_activite_operationnelle + montant_fe_tft


	# -----------------------------------
	# Variation du BF lié aux activités opérationnelles
	item = {
		"libelle" : "Variation du BF lié aux activités opérationnelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % variation_fb_activite_operationnelle,
		"balance_n1" : "%.2f" % variation_fb_activite_operationnelle
	}
	donnees_tb_operationnel.append(item)
	tresorerie_activite_operationnelle = tresorerie_activite_operationnelle + variation_fb_activite_operationnelle
	#print("Flux {}".format(tresorerie_activite_operationnelle))
	# -----------------------------------
	# LES FLUX DE  TRESORERIE PROVENANT DES ACTIVITES OPERATIONNELLES (B)
	item = {
		"libelle" : "LES FLUX DE TRESORERIE PROVENANT DES ACTIVITES OPERATIONNELLES (B)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_activite_operationnelle,
		"balance_n1" : "%.2f" % tresorerie_activite_operationnelle
	}
	donnees_tb_operationnel.append(item)

	# -----------------------------------
	# Variation des immobilisations  incorporelles nettes (poste AD)
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AD":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "31",
		"libelle" : "Variation des immobilisations  incorporelles nettes (poste AD)",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 6812
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6812":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "32",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "32",
		"libelle" : "Compte 6812",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 6913
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6913":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "33",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "33",
		"libelle" : "Compte 6913",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 6541
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6541":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "34",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "34",
		"libelle" : "Compte 6541",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance
	#print(" etape 10")
	# -----------------------------------
	# Compte 811
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "811":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "35",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "35",
		"libelle" : "Compte 811",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 251
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "251":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "36",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "36",
		"libelle" : "Compte 251",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 4811,4821, 4041, 4046
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4811","4821", "4041", "4046"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "37",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "37",
		"libelle" : "Compte 4811,4821, 4041, 4046",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 4811,4821, 4041, 4046
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4811","4821", "4041", "4046"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "38",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "38",
		"libelle" : "Compte 4811,4821, 4041, 4046",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 48161, 48171, 48181
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("48161", "48171", "48181"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "39",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "39",
		"libelle" : "Compte 48161, 48171, 48181",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 48161, 48171, 48181
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("48161", "48171", "48181"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "40",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "40",
		"libelle" : "Compte 48161, 48171, 48181",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Décaissements liés aux acquisitions d’immobilisations incorporelles
	item = {
		"reference" : "FF",
		"libelle" : "Décaissements liés aux acquisitions d’immobilisations incorporelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % decaissement_immo_incorporelle,
		"balance_n1" : "%.2f" % decaissement_immo_incorporelle
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Variation des immobilisations  corporelles nettes ( poste AI )
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AD":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "41",
		"libelle" : "Variation des immobilisations  corporelles nettes ( poste AI )",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 6813
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6813":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "42",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "42",
		"libelle" : "Compte 6813",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance
	#print(" etape 11")
	# -----------------------------------
	# Compte 6914
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6914":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "43",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "43",
		"libelle" : "Compte 6914",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 6542
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6542":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "44",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "44",
		"libelle" : "Compte 6542",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 812
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "812":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "45",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "45",
		"libelle" : "Compte 812",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 1061
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1061":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "46",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "46",
		"libelle" : "Compte 1061",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 1062
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1062":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "47",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "47",
		"libelle" : "Compte 1062",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 154
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "154":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "48",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "48",
		"libelle" : "Compte 154",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance
	#print(" etape 12")
	# -----------------------------------
	# Compte 1984
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1984":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "49",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "49",
		"libelle" : "Compte 1984",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 2286, 2316, 2326, 2416, 2426, 2446, 2456
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("2286", "2316", "2326", "2416", "2426", "2446", "2456"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "50",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "50",
		"libelle" : "Compte 2286, 2316, 2326, 2416, 2426, 2446, 2456",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 2714
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "2714":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "51",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "51",
		"libelle" : "Compte 2714",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 252
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "252":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "52",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "52",
		"libelle" : "Compte 252",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 4812, 4822, 4042, 4047
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4812", "4822", "4042", "4047"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "53",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "53",
		"libelle" : "Compte 4812, 4822, 4042, 4047",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 4812, 4822, 4042, 4047
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4812", "4822", "4042", "4047"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "54",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "54",
		"libelle" : "Compte 4812, 4822, 4042, 4047",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 48162, 48172, 48182
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] in ("48162", "48172", "48182"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "55",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "55",
		"libelle" : "Compte 48162, 48172, 48182",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance
	#print(" etape 13")
	# -----------------------------------
	# Compte 48162, 48172, 48182
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] in ("48162", "48172", "48182"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "56",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "56",
		"libelle" : "Compte 48162, 48172, 48182",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Décaissements liés aux acquisitions d’immobilisations corporelles
	item = {
		"reference" : "FG",
		"libelle" : "Décaissements liés aux acquisitions d’immobilisations corporelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % decaissement_immo_corporelle,
		"balance_n1" : "%.2f" % decaissement_immo_corporelle
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Compte 26, 27
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("26", "27"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "57",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "57",
		"libelle" : "Compte 26, 27",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_financiere = decaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4813
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4813":
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "58",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "58",
		"libelle" : "Compte 4813",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_financiere = decaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4813
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4813":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "59",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "59",
		"libelle" : "Compte 4813",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_financiere = decaissement_immo_financiere + balance

	# -----------------------------------
	# Décaissements liés aux acquisitions d’immobilisations financières
	item = {
		"reference" : "FH",
		"libelle" : "Décaissements liés aux acquisitions d’immobilisations financières",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % decaissement_immo_financiere,
		"balance_n1" : "%.2f" % decaissement_immo_financiere
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Compte 821, 822 ou 7541, 7542
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] in ("821", "822") or item_balance["numero_compte"][0:4] in ("7541", "7542"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "60",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "60",
		"libelle" : "Compte 821, 822 ou 7541, 7542",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immobilisation = encaissement_immobilisation + balance

	# -----------------------------------
	# Compte 4851, 4852 ou 4141,4142
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4851", "4852", "4141", "4142"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "61",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "61",
		"libelle" : "Compte 4851, 4852 ou 4141,4142",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	encaissement_immobilisation = encaissement_immobilisation + balance

	# -----------------------------------
	# Compte 4851, 4852 ou 4141,4142
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4851", "4852", "4141", "4142"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "62",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "62",
		"libelle" : "Compte 4851, 4852 ou 4141,4142",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immobilisation = encaissement_immobilisation + balance

	# -----------------------------------
	# Encaissements liés aux cessions d’immobilisations incorporelles et corporelles
	item = {
		"reference" : "FI",
		"libelle" : "Encaissements liés aux cessions d’immobilisations incorporelles et corporelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % encaissement_immobilisation,
		"balance_n1" : "%.2f" % encaissement_immobilisation
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Compte 826
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "826":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "63",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "63",
		"libelle" : "Compte 826",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance
	#print(" etape 14")
	# -----------------------------------
	# Compte 4856 ou 4143
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4856", "4143"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "64",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "64",
		"libelle" : "Compte 4856 ou 4143",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4856 ou 4143
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4856", "4143"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "65",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "65",
		"libelle" : "Compte 4856 ou 4143",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 27
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "27":
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "66",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "66",
		"libelle" : "Compte 27",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Encaissements liés aux cessions d’immobilisations financières
	item = {
		"reference" : "FJ",
		"libelle" : "Encaissements liés aux cessions d’immobilisations financières",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % encaissement_immo_financiere,
		"balance_n1" : "%.2f" % encaissement_immo_financiere
	}
	donnees_tb_investissement.append(item)

	tresorerie_activite_investissement = - (decaissement_immo_incorporelle + decaissement_immo_corporelle + decaissement_immo_financiere) + (encaissement_immobilisation + encaissement_immo_financiere)
	# -----------------------------------
	# LES FLUX  DE TRESORERIE PROVENANT DES ACTIVITES  D’INVESTISSEMENT ( C )
	item = {
		"libelle" : "LES FLUX  DE TRESORERIE PROVENANT DES ACTIVITES  D’INVESTISSEMENT ( C )",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_activite_investissement,
		"balance_n1" : "%.2f" % tresorerie_activite_investissement
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Variation du compte 10 ----------- IMPORTANT solde final N-1 = ouverture N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "10":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "67",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "67",
		"libelle" : "Variation du compte 10",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 106
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "106":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "69",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "69",
		"libelle" : "Variation du compte 106",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 109
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "109":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "70",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "70",
		"libelle" : "Variation du compte 109",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "71",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "71",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 4581
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4581":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "72",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "72",
		"libelle" : "Variation du compte 4581",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance


	# -----------------------------------
	# l’Augmentation de capital par apports à nouveaux
	item = {
		"libelle" : "l’Augmentation de capital par apports à nouveaux",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % augmentation_capital,
		"balance_n1" : "%.2f" % augmentation_capital
	}
	donnees_tb_financement.append(item)
	#print(" etape 16")
	# -----------------------------------
	# Variation du compte 14
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "14":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "73",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "73",
		"libelle" : "Variation du compte 14",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 799
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "799":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "74",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "74",
		"libelle" : "Variation du compte 799",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 4582
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4582":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "75",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "75",
		"libelle" : "Variation du compte 4582",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 4494
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4494":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "76",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "76",
		"libelle" : "Variation du compte 4494",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance
	#print(" etape 17")
	# -----------------------------------
	# Variation du compte 4497
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4497":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "77",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "77",
		"libelle" : "Variation du compte 4497",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Subventions d’investissements reçues
	item = {
		"libelle" : "Subventions d’investissements reçues",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % subventions_recues,
		"balance_n1" : "%.2f" % subventions_recues
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Subventions d’investissements reçues
	item = {
		"libelle" : "Subventions d’investissements reçues",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % subventions_recues,
		"balance_n1" : "%.2f" % subventions_recues
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 10
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "10":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "78",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "78",
		"libelle" : "Variation du compte 10",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	prelevement_capital = prelevement_capital + balance

	# -----------------------------------
	# Variation du compte 106
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "106":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "79",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "79",
		"libelle" : "Variation du compte 106",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	prelevement_capital = prelevement_capital + balance

	# -----------------------------------
	# Variation du compte 109
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "109":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "80",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "80",
		"libelle" : "Variation du compte 109",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	prelevement_capital = prelevement_capital + balance

	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "81",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "81",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 4581
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4581":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "82",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "82",
		"libelle" : "Variation du compte 4581",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	#print(" etape 18")
	# -----------------------------------
	# Prélèvements sur le capital
	item = {
		"libelle" : "Prélèvements sur le capital",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % prelevement_capital,
		"balance_n1" : "%.2f" % prelevement_capital
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Compte 465
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "465":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "83",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "83",
		"libelle" : "Compte 465",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	dividentes_versees = - float(balance)
	# -----------------------------------
	# Dividendes versés
	item = {
		"libelle" : "Dividendes versés",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % dividentes_versees,
		"balance_n1" : "%.2f" % dividentes_versees
	}
	donnees_tb_financement.append(item)

	financement_capitaux_propres = augmentation_capital + subventions_recues + prelevement_capital + dividentes_versees
	# -----------------------------------
	# Flux de financement provenant des capitaux  propres
	item = {
		"libelle" : "Flux de financement provenant des capitaux  propres",
		"signe" : "D",
		"est_total" : True,
		"balance_n" : "%.2f" % financement_capitaux_propres,
		"balance_n1" : "%.2f" % financement_capitaux_propres
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 16
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "16":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "84",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "84",
		"libelle" : "Variation du compte 16",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Variation du compte 18
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "18":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "85",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "85",
		"libelle" : "Variation du compte 18",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Variation du compte 183
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "183":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "86",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "86",
		"libelle" : "Variation du compte 183",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance
	#print(" etape 20")
	# -----------------------------------
	# Compte 17
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "17":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "87",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "87",
		"libelle" : "Compte 17",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Flux de financement provenant des capitaux  étrangers
	item = {
		"libelle" : "Flux de financement provenant des capitaux  étrangers",
		"signe" : "E",
		"est_total" : True,
		"balance_n" : "%.2f" % financement_capitaux_etrangers,
		"balance_n1" : "%.2f" % financement_capitaux_etrangers
	}
	donnees_tb_financement.append(item)

	tresorerie_capitaux_propres = financement_capitaux_propres + financement_capitaux_etrangers
	# -----------------------------------
	# LES FLUX  DE TRESORERIE PROVENANT DES CAPITAUX PROPRES (F)
	item = {
		"libelle" : "LES FLUX  DE TRESORERIE PROVENANT DES CAPITAUX PROPRES (F)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_capitaux_propres,
		"balance_n1" : "%.2f" % tresorerie_capitaux_propres
	}
	donnees_tb_financement.append(item)

	variation_tresorerie_nette = tresorerie_activite_operationnelle + tresorerie_activite_investissement + tresorerie_capitaux_propres
	# -----------------------------------
	# VARIATION DE LA TRESORERIE NETTE DE LA PERIODE (B+C+F)
	item = {
		"libelle" : "VARIATION DE LA TRESORERIE NETTE DE LA PERIODE (B+C+F)",
		"signe" : "G",
		"est_total" : True,
		"balance_n" : "%.2f" % variation_tresorerie_nette,
		"balance_n1" : "%.2f" % variation_tresorerie_nette
	}
	donnees_tb_financement.append(item)
	#print(" etape 21")
	tresorerie_nette_periode = tresorerie_initiale + variation_tresorerie_nette
	# -----------------------------------
	# TRESORERIE NETTE DE LA PERIODE (G+A)
	item = {
		"libelle" : "TRESORERIE NETTE DE LA PERIODE (G+A)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_nette_periode,
		"balance_n1" : "%.2f" % tresorerie_nette_periode
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Trésorerie-actif de N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("50", "51", "52", "53", "54", "57") or item_balance["numero_compte"][0:3] in ("581", "582"):
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "88",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "88",
		"libelle" : "Trésorerie-actif de N",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_final.append(item)
	tresorerie_finale = tresorerie_finale + balance
	#print(" etape 22")
	# -----------------------------------
	# Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "472":
			solde = float(item_balance["debit_solde"]) - float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "89",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "89",
		"libelle" : "Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_final.append(item)
	tresorerie_finale = tresorerie_finale + balance

	# -----------------------------------
	# Trésorerie-passif de N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("52", "53") or item_balance["numero_compte"][0:3] in ("564", "565", "561", "566"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "90",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "90",
		"libelle" : "Trésorerie-passif de N",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_final.append(item)
	tresorerie_finale = tresorerie_finale + balance

	# -----------------------------------
	# Contrôle Trésorerie au 31 décembre : Trésorerie-actif N -  Trésorerie-passif N
	item = {
		"libelle" : "Contrôle Trésorerie au 31 décembre : Trésorerie-actif N -  Trésorerie-passif N",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_finale,
		"balance_n1" : "%.2f" % tresorerie_finale
	}
	donnees_tb_final.append(item)

	montant_a_equilibre_tft = tresorerie_nette_periode - tresorerie_finale
	# -----------------------------------
	# En cas de déséquilibre, le montant à équilibrer au TFT est de :
	item = {
		"libelle" : "En cas de déséquilibre, le montant à équilibrer au TFT est de :",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_a_equilibre_tft,
		"balance_n1" : "%.2f" % montant_a_equilibre_tft
	}
	donnees_tb_final.append(item)

	context = {
		'title' : "Tableau de bord des flux de trésorerie",
		"donnees_tb_initial" : donnees_tb_initial ,
		"donnees_tb_operationnel" : donnees_tb_operationnel ,
		"donnees_tb_investissement" : donnees_tb_investissement ,
		"donnees_tb_financement" : donnees_tb_financement ,
		"donnees_tb_final" : donnees_tb_final ,
		"comptes" : comptes ,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'portrait',
		'menu' : 9
	}


def post_generer_tb_tresorerie(request):
	try:
		# droit="GENERER_FLUX_TRESORERIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 372
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_tb_tresorerie(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/tb_tresorerie/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GENERATE TB TRESORERIE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_tb_tresorerie"))


#  TABLEAU DE FLUX DE TRESORERIE
def get_generer_tresorerie(request):

	# droit="GENERER_FLUX_TRESORERIE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 373
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
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/flux_tresorerie/generate.html")
	return HttpResponse(template.render(context, request))

def post_traiter_tresorerie(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()

	#On declare les tableaux et variable qui seront renvoyés en output
	donnees_tb_initial = []
	donnees_tb_operationnel = []
	donnees_tb_investissement = []
	donnees_tb_financement = []
	donnees_tb_final = []
	comptes = []

	tresorerie_initiale = 0

	cafg = 0
	montant_fb_tft = 0
	montant_fd_tft = 0
	montant_fe_tft = 0
	variation_fb_activite_operationnelle = 0
	tresorerie_activite_operationnelle = 0

	decaissement_immo_incorporelle = 0
	decaissement_immo_corporelle = 0
	decaissement_immo_financiere = 0
	encaissement_immobilisation = 0
	encaissement_immo_financiere = 0
	tresorerie_activite_investissement = 0

	augmentation_capital = 0
	subventions_recues = 0
	prelevement_capital = 0
	dividentes_versees = 0
	financement_capitaux_propres = 0
	financement_capitaux_etrangers = 0
	tresorerie_capitaux_propres = 0

	variation_tresorerie_nette = 0
	tresorerie_nette_periode = 0

	tresorerie_finale = 0

	montant_a_equilibre_tft = 0

	#On récupère les données de la balance de la periode
	donnees_balance = balanceArray.toGetInPeriode(date_debut, date_fin, devise)
	#On récupère les données de la balance de la periode
	donnees_compte_resultat = compteResultatArray.toGetOfBalance(donnees_balance)
	#On récupère les données de la balance de la periode
	donnees_bilan_actif, donnees_bilan_passif = bilanArray.toGetOfBalance(donnees_balance, donnees_compte_resultat)

	#TODO Garder que les comptes des charges et produits pour optimisation

	# -----------------------------------
	# Trésorerie-actif de N-1   sid: 50, 51, 52, 53, 54, 57, 581, 582
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("50", "51", "52", "53", "54", "57") or item_balance["numero_compte"][0:3] in ("581", "582"):
			solde = float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "1",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "1",
		"libelle" : "Trésorerie-actif de N-1",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_initial.append(item)
	tresorerie_initiale = tresorerie_initiale + balance

	# -----------------------------------
	# Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N-1
	# sid 472 - sic 472
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "472":
			solde = float(item_balance["debit_ouverture"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "2",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "2",
		"libelle" : "Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N-1",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_initial.append(item)
	tresorerie_initiale = tresorerie_initiale + balance

	# -----------------------------------
	# Trésorerie-passif de N-1 sic 52, 53, 564, 565, 561, 566
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("52", "53") or item_balance["numero_compte"][0:3] in ("564", "565", "561", "566"):
			solde = float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "3",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "3",
		"libelle" : "Trésorerie-passif de N-1",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_initial.append(item)
	tresorerie_initiale = tresorerie_initiale + balance

	# -----------------------------------
	# Trésorerie au 1er janvier (A)
	item = {
		"reference" : "ZA",
		"libelle" : "Trésorerie au 1er janvier (A)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_initiale,
		"balance_n1" : "%.2f" % tresorerie_initiale
	}
	donnees_tb_initial.append(item)
	# -----------------------------------
	# Excédent brut d’exploitation (poste XD compte de résultat) Excédent brut d'exploitation dans CR
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "XD":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "4",
		"libelle" : "Excédent brut d’exploitation (poste XD compte de résultat)",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Compte 654 solde débiteur balance N   sfd 654

	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "654":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "5",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "5",
		"libelle" : "Compte 654 solde débiteur balance N",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Compte 754 solde créditeur balance N 		sfc 754

	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "754":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "6",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "6",
		"libelle" : "Compte 754 solde créditeur balance N",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Résultat financier (poste XF compte de résultat)

	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "XF":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "7",
		"libelle" : "Résultat financier (poste XF compte de résultat)",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Autres produits HAO (poste TO compte de résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "TO":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "8",
		"libelle" : "Autres produits HAO (poste TO compte de résultat)",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance
	#print(" etape 3")
	# -----------------------------------
	# autres charges HAO (poste RP compte de résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "RP":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "9",
		"libelle" : "autres charges HAO (poste RP compte de résultat)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Participation des travailleurs (poste RQ du compte résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "RQ":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "10",
		"libelle" : "Participation des travailleurs (poste RQ du compte résultat)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance

	# -----------------------------------
	# Impôts sur le résultat (poste RS du compte de résultat)
	balance = 0
	balance_n1 = 0
	for item_resultat in donnees_compte_resultat:
		if item_resultat["reference"] == "RS":
			balance = float(item_resultat["balance_n"])
			balance_n1 = float(item_resultat["balance_n1"])
	item = {
		"reference" : "11",
		"libelle" : "Impôts sur le résultat (poste RS du compte de résultat)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	cafg = cafg + balance
	#print(" etape 33333")
	# -----------------------------------
	# Capacité d’Autofinancement Globale (CAFG)
	item = {
		"reference" : "FA",
		"libelle" : "Capacité d’Autofinancement Globale (CAFG)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % cafg,
		"balance_n1" : "%.2f" % cafg
	}
	donnees_tb_operationnel.append(item)
	tresorerie_activite_operationnelle = tresorerie_activite_operationnelle + cafg
	#print("Flux {}".format(tresorerie_activite_operationnelle))

	# -----------------------------------
	# Actif circulant HAO (Poste BA des bilans )
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BA":
			balance = float(item_bilan["balance_n"])
	item = {
		"reference" : "12",
		"libelle" : "Actif circulant HAO (Poste BA des bilans )",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fb_tft = montant_fb_tft + balance

	# -----------------------------------
	# Compte 485 (exlure)
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "485":
			solde = item_balance["debit_solde"]
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "13",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "13",
		"libelle" : "Compte 485 (exlure)",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_operationnel.append(item)
	montant_fb_tft = montant_fb_tft + balance

	# -----------------------------------
	# Montant affecté au poste FB du TFT
	item = {
		"reference" : "FB",
		"libelle" : "Montant affecté au poste FB du TFT",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_fb_tft,
		"balance_n1" : "%.2f" % montant_fb_tft
	}
	donnees_tb_operationnel.append(item)


	# -----------------------------------
	# Variation des stocks (Poste BB des bilans) Poste FC du TFT
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BB":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "14",
		"libelle" : "Variation des stocks (Poste BB des bilans) Poste FC du TFT",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	variation_fb_activite_operationnelle = - float(montant_fb_tft) + (- float(balance))


	# -----------------------------------
	# Variation des créances  et emplois assimilé (Poste BG des bilans)
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "BG":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "15",
		"libelle" : "Variation des créances  et emplois assimilé (Poste BG des bilans)",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance

	# -----------------------------------
	# Variation du compte 478
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "478":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "16",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "16",
		"libelle" : "Variation du compte 478",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 419
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "419":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "17",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "17",
		"libelle" : "Variation du compte 419",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 414
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "414":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "17",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "17",
		"libelle" : "Variation du compte 414",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "19",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "19",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance

	# -----------------------------------
	# Variation du compte 458
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "458":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "20",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "20",
		"libelle" : "Variation du compte 458",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 4494
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4494":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "21",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "21",
		"libelle" : "Variation du compte 4494",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance


	# -----------------------------------
	# Variation du compte 4751
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4751":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "22",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "22",
		"libelle" : "Variation du compte 4751",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fd_tft = montant_fd_tft + balance

	# -----------------------------------
	# Montant affecté au poste FD du TFT
	item = {
		"reference" : "FD",
		"libelle" : "Montant affecté au poste FD du TFT",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_fd_tft,
		"balance_n1" : "%.2f" % montant_fd_tft
	}
	donnees_tb_operationnel.append(item)
	variation_fb_activite_operationnelle = variation_fb_activite_operationnelle + (- float(montant_fd_tft))


	# -----------------------------------
	# Variation du passif circulant (Poste DP des bilans)
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_passif:
		if item_bilan["reference"] == "DP":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "23",
		"libelle" : "Variation du passif circulant (Poste DP des bilans)",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 409
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "409":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "24",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "24",
		"libelle" : "Variation du compte 409",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 404
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "404":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "25",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "25",
		"libelle" : "Variation du compte 404",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance

	# -----------------------------------
	# Variation du compte 481
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "481":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "26",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "26",
		"libelle" : "Variation du compte 481",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 482
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "482":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "27",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "27",
		"libelle" : "Variation du compte 482",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "28",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "28",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 4752
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4752":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "29",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "29",
		"libelle" : "Variation du compte 4752",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance


	# -----------------------------------
	# Variation du compte 472
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "472":
			solde = - float(item_balance["credit_solde"]) - float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "30",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "30",
		"libelle" : "Variation du compte 472",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_operationnel.append(item)
	montant_fe_tft = montant_fe_tft + balance

	# -----------------------------------
	# Montant affecté au poste FE du TFT
	item = {
		"reference" : "FE",
		"libelle" : "Montant affecté au poste FE du TFT",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_fe_tft,
		"balance_n1" : "%.2f" % montant_fe_tft
	}
	donnees_tb_operationnel.append(item)
	variation_fb_activite_operationnelle = variation_fb_activite_operationnelle + montant_fe_tft


	# -----------------------------------
	# Variation du BF lié aux activités opérationnelles
	item = {
		"reference" : "BF",
		"libelle" : "Variation du BF lié aux activités opérationnelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % variation_fb_activite_operationnelle,
		"balance_n1" : "%.2f" % variation_fb_activite_operationnelle
	}
	donnees_tb_operationnel.append(item)
	tresorerie_activite_operationnelle = tresorerie_activite_operationnelle + variation_fb_activite_operationnelle
	#print("Flux {}".format(tresorerie_activite_operationnelle))
	# -----------------------------------
	# LES FLUX DE  TRESORERIE PROVENANT DES ACTIVITES OPERATIONNELLES (B)
	item = {
		"reference" : "B",
		"libelle" : "LES FLUX DE TRESORERIE PROVENANT DES ACTIVITES OPERATIONNELLES (B)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_activite_operationnelle,
		"balance_n1" : "%.2f" % tresorerie_activite_operationnelle
	}
	donnees_tb_operationnel.append(item)

	# -----------------------------------
	# Variation des immobilisations  incorporelles nettes (poste AD)
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AD":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "31",
		"libelle" : "Variation des immobilisations  incorporelles nettes (poste AD)",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 6812
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6812":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "32",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "32",
		"libelle" : "Compte 6812",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 6913
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6913":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "33",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "33",
		"libelle" : "Compte 6913",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 6541
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6541":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "34",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "34",
		"libelle" : "Compte 6541",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 811
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "811":
			solde = + float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "35",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "35",
		"libelle" : "Compte 811",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 251
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "251":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "36",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "36",
		"libelle" : "Compte 251",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 4811,4821, 4041, 4046
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4811","4821", "4041", "4046"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "37",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "37",
		"libelle" : "Compte 4811,4821, 4041, 4046",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 4811,4821, 4041, 4046
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4811","4821", "4041", "4046"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "38",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "38",
		"libelle" : "Compte 4811,4821, 4041, 4046",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 48161, 48171, 48181
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("48161", "48171", "48181"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "39",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "39",
		"libelle" : "Compte 48161, 48171, 48181",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Compte 48161, 48171, 48181
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("48161", "48171", "48181"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "40",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "40",
		"libelle" : "Compte 48161, 48171, 48181",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_incorporelle = decaissement_immo_incorporelle + balance

	# -----------------------------------
	# Décaissements liés aux acquisitions d’immobilisations incorporelles
	item = {
		"reference" : "FF",
		"libelle" : "Décaissements liés aux acquisitions d’immobilisations incorporelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % decaissement_immo_incorporelle,
		"balance_n1" : "%.2f" % decaissement_immo_incorporelle
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Variation des immobilisations  corporelles nettes ( poste AI )
	balance = 0
	balance_n1 = 0
	for item_bilan in donnees_bilan_actif:
		if item_bilan["reference"] == "AD":
			balance = float(item_bilan["balance_n"]) - float(item_bilan["balance_n1"])
	item = {
		"reference" : "41",
		"libelle" : "Variation des immobilisations  corporelles nettes ( poste AI )",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 6813
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6813":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "42",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "42",
		"libelle" : "Compte 6813",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 6914
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6914":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "43",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "43",
		"libelle" : "Compte 6914",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 6542
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "6542":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "44",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "44",
		"libelle" : "Compte 6542",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 812
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "812":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "45",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "45",
		"libelle" : "Compte 812",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 1061
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1061":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "46",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "46",
		"libelle" : "Compte 1061",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 1062
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1062":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "47",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "47",
		"libelle" : "Compte 1062",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 154
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "154":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "48",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "48",
		"libelle" : "Compte 154",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 1984
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1984":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "49",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "49",
		"libelle" : "Compte 1984",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 2286, 2316, 2326, 2416, 2426, 2446, 2456
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("2286", "2316", "2326", "2416", "2426", "2446", "2456"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "50",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "50",
		"libelle" : "Compte 2286, 2316, 2326, 2416, 2426, 2446, 2456",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 2714
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "2714":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "51",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "51",
		"libelle" : "Compte 2714",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 252
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "252":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "52",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "52",
		"libelle" : "Compte 252",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 4812, 4822, 4042, 4047
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4812", "4822", "4042", "4047"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "53",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "53",
		"libelle" : "Compte 4812, 4822, 4042, 4047",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 4812, 4822, 4042, 4047
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4812", "4822", "4042", "4047"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "54",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "54",
		"libelle" : "Compte 4812, 4822, 4042, 4047",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 48162, 48172, 48182
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] in ("48162", "48172", "48182"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "55",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "55",
		"libelle" : "Compte 48162, 48172, 48182",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Compte 48162, 48172, 48182
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] in ("48162", "48172", "48182"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "56",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "56",
		"libelle" : "Compte 48162, 48172, 48182",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_corporelle = decaissement_immo_corporelle + balance

	# -----------------------------------
	# Décaissements liés aux acquisitions d’immobilisations corporelles
	item = {
		"reference" : "FG",
		"libelle" : "Décaissements liés aux acquisitions d’immobilisations corporelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % decaissement_immo_corporelle,
		"balance_n1" : "%.2f" % decaissement_immo_corporelle
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Compte 26, 27
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("26", "27"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "57",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "57",
		"libelle" : "Compte 26, 27",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_financiere = decaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4813
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4813":
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "58",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "58",
		"libelle" : "Compte 4813",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_financiere = decaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4813
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4813":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "59",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "59",
		"libelle" : "Compte 4813",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	decaissement_immo_financiere = decaissement_immo_financiere + balance

	# -----------------------------------
	# Décaissements liés aux acquisitions d’immobilisations financières
	item = {
		"reference" : "FH",
		"libelle" : "Décaissements liés aux acquisitions d’immobilisations financières",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % decaissement_immo_financiere,
		"balance_n1" : "%.2f" % decaissement_immo_financiere
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Compte 821, 822 ou 7541, 7542
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] in ("821", "822") or item_balance["numero_compte"][0:4] in ("7541", "7542"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "60",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "60",
		"libelle" : "Compte 821, 822 ou 7541, 7542",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immobilisation = encaissement_immobilisation + balance

	# -----------------------------------
	# Compte 4851, 4852 ou 4141,4142
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4851", "4852", "4141", "4142"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "61",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "61",
		"libelle" : "Compte 4851, 4852 ou 4141,4142",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	encaissement_immobilisation = encaissement_immobilisation + balance

	# -----------------------------------
	# Compte 4851, 4852 ou 4141,4142
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4851", "4852", "4141", "4142"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "62",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "62",
		"libelle" : "Compte 4851, 4852 ou 4141,4142",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immobilisation = encaissement_immobilisation + balance

	# -----------------------------------
	# Encaissements liés aux cessions d’immobilisations incorporelles et corporelles
	item = {
		"reference" : "FI",
		"libelle" : "Encaissements liés aux cessions d’immobilisations incorporelles et corporelles",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % encaissement_immobilisation,
		"balance_n1" : "%.2f" % encaissement_immobilisation
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Compte 826
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "826":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "63",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "63",
		"libelle" : "Compte 826",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4856 ou 4143
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4856", "4143"):
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "64",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "64",
		"libelle" : "Compte 4856 ou 4143",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 4856 ou 4143
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("4856", "4143"):
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "65",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "65",
		"libelle" : "Compte 4856 ou 4143",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Compte 27
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "27":
			solde = float(item_balance["credit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "66",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "66",
		"libelle" : "Compte 27",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_investissement.append(item)
	encaissement_immo_financiere = encaissement_immo_financiere + balance

	# -----------------------------------
	# Encaissements liés aux cessions d’immobilisations financières
	item = {
		"reference" : "FJ",
		"libelle" : "Encaissements liés aux cessions d’immobilisations financières",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % encaissement_immo_financiere,
		"balance_n1" : "%.2f" % encaissement_immo_financiere
	}
	donnees_tb_investissement.append(item)

	tresorerie_activite_investissement = - (decaissement_immo_incorporelle + decaissement_immo_corporelle + decaissement_immo_financiere) + (encaissement_immobilisation + encaissement_immo_financiere)
	# -----------------------------------
	# LES FLUX  DE TRESORERIE PROVENANT DES ACTIVITES  D’INVESTISSEMENT ( C )
	item = {
		"reference" : "C",
		"libelle" : "LES FLUX  DE TRESORERIE PROVENANT DES ACTIVITES  D’INVESTISSEMENT ( C )",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_activite_investissement,
		"balance_n1" : "%.2f" % tresorerie_activite_investissement
	}
	donnees_tb_investissement.append(item)

	# -----------------------------------
	# Variation du compte 10 ----------- IMPORTANT solde final N-1 = ouverture N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "10":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "67",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "67",
		"libelle" : "Variation du compte 10",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 106
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "106":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "69",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "69",
		"libelle" : "Variation du compte 106",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 109
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "109":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "70",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "70",
		"libelle" : "Variation du compte 109",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "71",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "71",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance

	# -----------------------------------
	# Variation du compte 4581
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4581":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "72",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "72",
		"libelle" : "Variation du compte 4581",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	augmentation_capital = augmentation_capital + balance


	# -----------------------------------
	# l’Augmentation de capital par apports à nouveaux
	item = {
		"reference" : "FK",
		"libelle" : "l’Augmentation de capital par apports à nouveaux",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % augmentation_capital,
		"balance_n1" : "%.2f" % augmentation_capital
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 14
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "14":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "73",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "73",
		"libelle" : "Variation du compte 14",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 799
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "799":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "74",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "74",
		"libelle" : "Variation du compte 799",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 4582
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4582":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "75",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "75",
		"libelle" : "Variation du compte 4582",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 4494
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4494":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "76",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "76",
		"libelle" : "Variation du compte 4494",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Variation du compte 4497
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4497":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "77",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "77",
		"libelle" : "Variation du compte 4497",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	subventions_recues = subventions_recues + balance

	# -----------------------------------
	# Subventions d’investissements reçues
	item = {
		"reference" : "FL",
		"libelle" : "Subventions d’investissements reçues",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % subventions_recues,
		"balance_n1" : "%.2f" % subventions_recues
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 10
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "10":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "78",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "78",
		"libelle" : "Variation du compte 10",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	prelevement_capital = prelevement_capital + balance

	# -----------------------------------
	# Variation du compte 106
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "106":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "79",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "79",
		"libelle" : "Variation du compte 106",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	prelevement_capital = prelevement_capital + balance

	# -----------------------------------
	# Variation du compte 109
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "109":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "80",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "80",
		"libelle" : "Variation du compte 109",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	prelevement_capital = prelevement_capital + balance

	# -----------------------------------
	# Variation du compte 467
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "467":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "81",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "81",
		"libelle" : "Variation du compte 467",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 4581
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "4581":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "82",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "82",
		"libelle" : "Variation du compte 4581",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Prélèvements sur le capital
	item = {
		"reference" : "FM",
		"libelle" : "Prélèvements sur le capital",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % prelevement_capital,
		"balance_n1" : "%.2f" % prelevement_capital
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Compte 465
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "465":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "83",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "83",
		"libelle" : "Compte 465",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	dividentes_versees = - float(balance)
	# -----------------------------------
	# Dividendes versés
	item = {
		"reference" : "FN",
		"libelle" : "Dividendes versés",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % dividentes_versees,
		"balance_n1" : "%.2f" % dividentes_versees
	}
	donnees_tb_financement.append(item)

	financement_capitaux_propres = augmentation_capital + subventions_recues + prelevement_capital + dividentes_versees
	# -----------------------------------
	# Flux de financement provenant des capitaux  propres
	item = {
		"reference": "D",
		"libelle" : "Flux de financement provenant des capitaux  propres",
		"signe" : "D",
		"est_total" : True,
		"balance_n" : "%.2f" % financement_capitaux_propres,
		"balance_n1" : "%.2f" % financement_capitaux_propres
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Variation du compte 16
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "16":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "84",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "84",
		"libelle" : "Variation du compte 16",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Variation du compte 18
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "18":
			solde = float(item_balance["credit_solde"]) - float(item_balance["credit_solde"])#float(item_balance["credit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "85",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "85",
		"libelle" : "Variation du compte 18",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Variation du compte 183
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "183":
			solde = float(item_balance["debit_solde"]) - float(item_balance["debit_solde"]) #float(item_balance["debit_ouverture"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "86",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "86",
		"libelle" : "Variation du compte 183",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Compte 17
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "17":
			solde = float(item_balance["debit_mouvement"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "87",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "87",
		"libelle" : "Compte 17",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % float(balance),
		"balance_n1" : "%.2f" % float(balance)
	}
	donnees_tb_financement.append(item)
	financement_capitaux_etrangers = financement_capitaux_etrangers + balance

	# -----------------------------------
	# Flux de financement provenant des capitaux  étrangers
	item = {
		"reference" : "E",
		"libelle" : "Flux de financement provenant des capitaux  étrangers",
		"signe" : "E",
		"est_total" : True,
		"balance_n" : "%.2f" % financement_capitaux_etrangers,
		"balance_n1" : "%.2f" % financement_capitaux_etrangers
	}
	donnees_tb_financement.append(item)

	tresorerie_capitaux_propres = financement_capitaux_propres + financement_capitaux_etrangers
	# -----------------------------------
	# LES FLUX  DE TRESORERIE PROVENANT DES CAPITAUX PROPRES (F)
	item = {
		"reference" : "F",
		"libelle" : "LES FLUX  DE TRESORERIE PROVENANT DES CAPITAUX PROPRES (F)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_capitaux_propres,
		"balance_n1" : "%.2f" % tresorerie_capitaux_propres
	}
	donnees_tb_financement.append(item)

	variation_tresorerie_nette = tresorerie_activite_operationnelle + tresorerie_activite_investissement + tresorerie_capitaux_propres
	# -----------------------------------
	# VARIATION DE LA TRESORERIE NETTE DE LA PERIODE (B+C+F)
	item = {
		"reference" : "G",
		"libelle" : "VARIATION DE LA TRESORERIE NETTE DE LA PERIODE (B+C+F)",
		"signe" : "G",
		"est_total" : True,
		"balance_n" : "%.2f" % variation_tresorerie_nette,
		"balance_n1" : "%.2f" % variation_tresorerie_nette
	}
	donnees_tb_financement.append(item)

	tresorerie_nette_periode = tresorerie_initiale + variation_tresorerie_nette
	# -----------------------------------
	# TRESORERIE NETTE DE LA PERIODE (G+A)
	item = {
		"reference" : "GA",
		"libelle" : "TRESORERIE NETTE DE LA PERIODE (G+A)",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_nette_periode,
		"balance_n1" : "%.2f" % tresorerie_nette_periode
	}
	donnees_tb_financement.append(item)

	# -----------------------------------
	# Trésorerie-actif de N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("50", "51", "52", "53", "54", "57") or item_balance["numero_compte"][0:3] in ("581", "582"):
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "88",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "88",
		"libelle" : "Trésorerie-actif de N",
		"signe" : "+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_final.append(item)
	tresorerie_finale = tresorerie_finale + balance
	# -----------------------------------
	# Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "472":
			solde = float(item_balance["debit_solde"]) - float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "89",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	item = {
		"reference" : "89",
		"libelle" : "Compte 472 versements restant à effectuer sur titres de placement non libérés de l’année N",
		"signe" : "-/+",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_final.append(item)
	tresorerie_finale = tresorerie_finale + balance

	# -----------------------------------
	# Trésorerie-passif de N
	balance = 0
	balance_n1 = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] in ("52", "53") or item_balance["numero_compte"][0:3] in ("564", "565", "561", "566"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu dans le tableau de bord
			compte = {
				"reference" : "90",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"balance" : solde,
			}
			comptes.append(compte)
	balance = - balance
	item = {
		"reference" : "90",
		"libelle" : "Trésorerie-passif de N",
		"signe" : "-",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance
	}
	donnees_tb_final.append(item)
	tresorerie_finale = tresorerie_finale + balance

	# -----------------------------------
	# Contrôle Trésorerie au 31 décembre : Trésorerie-actif N -  Trésorerie-passif N
	item = {
		"libelle" : "Contrôle Trésorerie au 31 décembre : Trésorerie-actif N -  Trésorerie-passif N",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % tresorerie_finale,
		"balance_n1" : "%.2f" % tresorerie_finale
	}
	donnees_tb_final.append(item)

	montant_a_equilibre_tft = tresorerie_nette_periode - tresorerie_finale
	# -----------------------------------
	# En cas de déséquilibre, le montant à équilibrer au TFT est de :
	item = {
		"libelle" : "En cas de déséquilibre, le montant à équilibrer au TFT est de :",
		"signe" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % montant_a_equilibre_tft,
		"balance_n1" : "%.2f" % montant_a_equilibre_tft
	}
	donnees_tb_final.append(item)


	# --------------------------------------------------------------------------------------
	# TABLEAU DES FLUX DE TRESORERIE
	#--------------------------------------------------------------------------------------
	#print("Debut Flux de tresorerie")
	donnees_flux_tresorerie = []

	variation_bf = 0
	variation_bf_n1 = 0

	flux_activite_operationnelle = 0
	flux_activite_operationnelle_n1 = 0

	flux_activite_invetissement = 0
	flux_activite_invetissement_n1 = 0

	flux_activite_capitaux_propres_1 = 0
	flux_activite_capitaux_propres_1_n1 = 0

	flux_activite_capitaux_propres_2 = 0
	flux_activite_capitaux_propres_2_n1 = 0

	flux_activite_financement = 0
	flux_activite_financement_n1 = 0

	variation_tresorerie_nette = 0
	variation_tresorerie_nette_n1 = 0

	controle_tresorerie_nette_periode = 0
	controle_tresorerie_nette_periode_n1 = 0

	# -----------------------------------
	# Trésorerie nette au 1er Janvier
	# Trésorerie actif N-1 – Trésorerie-passif N-1
	balance = tresorerie_initiale
	balance_n1 = tresorerie_initiale
	item = {
		"reference" : "ZA",
		"libelle" : "Trésorerie nette au 1er Janvier     Trésorerie actif N-1 – Trésorerie-passif N-1",
		"lettre" : "A",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	controle_tresorerie_nette_periode = controle_tresorerie_nette_periode + balance
	controle_tresorerie_nette_periode_n1 = controle_tresorerie_nette_periode_n1 + balance_n1

	# -----------------------------------
	# Flux de trésorerie provenant des activités opérationnelles
	item = {
		"reference" : "",
		"libelle" : "Flux de trésorerie provenant des activités opérationnelles",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "",
		"balance_n1" : ""
	}
	donnees_flux_tresorerie.append(item)

	# -----------------------------------
	# Capacité d’Autofinancement Globale (CAFG)

	balance = cafg
	balance_n1 = cafg
	item = {
		"reference" : "FA",
		"libelle" : "Capacité d’Autofinancement Globale (CAFG)",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)

	# -----------------------------------
	# - Actif circulant HAO(1)

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_operationnel:
		if item_tb["reference"] == "14":
			balance = - float(item_tb["balance_n"])
			balance_n1 = - float(item_tb["balance_n1"])
	item = {
		"reference" : "FB",
		"libelle" : "- Actif circulant HAO(1)",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_bf = variation_bf + balance
	variation_bf_n1 = variation_bf_n1 + balance_n1

	# -----------------------------------
	# - Variation des stocks
	#print("apres")
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_operationnel:
		if item_tb["reference"] == "14":
			balance = - float(item_tb["balance_n"])
			balance_n1 = - float(item_tb["balance_n1"])
	item = {
		"reference" : "FC",
		"libelle" : "- Variation des stocks",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_bf = variation_bf + balance
	variation_bf_n1 = variation_bf_n1 + balance_n1

	# -----------------------------------
	# Variation des créances et emplois assimilés

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_operationnel:
		if item_tb["reference"] == "FD":
			balance = - float(item_tb["balance_n"])
			balance_n1 = - float(item_tb["balance_n1"])
	item = {
		"reference" : "FD",
		"libelle" : "Variation des créances et emplois assimilés",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_bf = variation_bf + balance
	variation_bf_n1 = variation_bf_n1 + balance_n1

	# -----------------------------------
	# + Variation du passif circulant(1)

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_operationnel:
		if item_tb["reference"] == "FE":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FE",
		"libelle" : "+ Variation du passif circulant(1)",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_bf = variation_bf + balance
	variation_bf_n1 = variation_bf_n1 + balance_n1

	# -----------------------------------
	# Variation du BF lié aux activités opérationnelles (FB+FC+FD+FE) :

	balance = variation_bf
	balance_n1 = variation_bf_n1
	item = {
		"reference" : "",
		"libelle" : "Variation du BF lié aux activités opérationnelles (FB+FC+FD+FE) :",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)

	# -----------------------------------
	# Flux de  trésorerie provenant des activités opérationnelles (somme FA à FE)
	balance = variation_bf + cafg
	balance_n1 = variation_bf_n1 + cafg
	item = {
		"reference" : "ZB",
		"libelle" : "Flux de  trésorerie provenant des activités opérationnelles (somme FA à FE)",
		"lettre" : "B",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_tresorerie_nette = variation_tresorerie_nette + balance
	variation_tresorerie_nette_n1 = variation_tresorerie_nette + balance_n1

	# -----------------------------------
	# Flux de  trésorerie provenant des activités d'investissements
	balance = 0
	balance_n1 = 0
	item = {
		"reference" : "",
		"libelle" : "Flux de  trésorerie provenant des activités d'investissements",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "",
		"balance_n1" : ""
	}
	donnees_flux_tresorerie.append(item)

	# -----------------------------------
	# - Décaissements liés aux acquisitions d’immobilisations incorporelles

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_investissement:
		if item_tb["reference"] == "FF":
			balance = - float(item_tb["balance_n"])
			balance_n1 = - float(item_tb["balance_n1"])
	item = {
		"reference" : "FF",
		"libelle" : "- Décaissements liés aux acquisitions d’immobilisations incorporelles",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_invetissement = flux_activite_invetissement + balance
	flux_activite_invetissement_n1 = flux_activite_invetissement_n1 + balance_n1

	# -----------------------------------
	# - Décaissements liés aux acquisitions d’immobilisations corporelles

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_investissement:
		if item_tb["reference"] == "FG":
			balance = - float(item_tb["balance_n"])
			balance_n1 = - float(item_tb["balance_n1"])
	item = {
		"reference" : "FG",
		"libelle" : "- Décaissements liés aux acquisitions d’immobilisations corporelles",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_invetissement = flux_activite_invetissement + balance
	flux_activite_invetissement_n1 = flux_activite_invetissement_n1 + balance_n1

	# -----------------------------------
	# - Décaissements liés aux acquisitions d’immobilisations financières

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_investissement:
		if item_tb["reference"] == "FH":
			balance = - float(item_tb["balance_n"])
			balance_n1 = - float(item_tb["balance_n1"])
	item = {
		"reference" : "FH",
		"libelle" : "- Décaissements liés aux acquisitions d’immobilisations financières",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_invetissement = flux_activite_invetissement + balance
	flux_activite_invetissement_n1 = flux_activite_invetissement_n1 + balance_n1

	# -----------------------------------
	# + Encaissements liés aux cessions d’immobilisations incorporelles et corporelles

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_investissement:
		if item_tb["reference"] == "FI":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FI",
		"libelle" : "+ Encaissements liés aux cessions d’immobilisations incorporelles et corporelles",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_invetissement = flux_activite_invetissement + balance
	flux_activite_invetissement_n1 = flux_activite_invetissement_n1 + balance_n1

	# -----------------------------------
	# + Encaissements liés aux cessions d’immobilisations financières

	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_investissement:
		if item_tb["reference"] == "FJ":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FJ",
		"libelle" : "+ Encaissements liés aux cessions d’immobilisations financières",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_invetissement = flux_activite_invetissement + balance
	flux_activite_invetissement_n1 = flux_activite_invetissement_n1 + balance_n1

	# -----------------------------------
	# Flux de  trésorerie provenant des activités d'investissement (somme FF à FJ)
	balance = flux_activite_invetissement
	balance_n1 = flux_activite_invetissement_n1
	item = {
		"reference" : "ZC",
		"libelle" : "Flux de  trésorerie provenant des activités d'investissement (somme FF à FJ)",
		"lettre" : "C",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_tresorerie_nette = variation_tresorerie_nette + balance
	variation_tresorerie_nette_n1 = variation_tresorerie_nette + balance_n1


	# -----------------------------------
	# Flux de trésorerie provenant du financement des capitaux propres
	item = {
		"reference" : "",
		"libelle" : "Flux de trésorerie provenant du financement des capitaux propres",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "",
		"balance_n1" : ""
	}
	donnees_flux_tresorerie.append(item)

	# -----------------------------------
	# + Augmentation de capital par apports à nouveaux
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] == "FK":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FK",
		"libelle" : "+ Augmentation de capital par apports à nouveaux",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_1 = flux_activite_capitaux_propres_1 + balance
	flux_activite_capitaux_propres_1_n1 = flux_activite_capitaux_propres_1_n1 + balance_n1

	# -----------------------------------
	# + Subventions d’investissements reçues
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] == "FL":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FL",
		"libelle" : "+ Subventions d’investissements reçues",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_1 = flux_activite_capitaux_propres_1 + balance
	flux_activite_capitaux_propres_1_n1 = flux_activite_capitaux_propres_1_n1 + balance_n1

	# -----------------------------------
	# - Prélèvements sur le capital
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] == "FM":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FM",
		"libelle" : "- Prélèvements sur le capital",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_1 = flux_activite_capitaux_propres_1 + balance
	flux_activite_capitaux_propres_1_n1 = flux_activite_capitaux_propres_1_n1 + balance_n1

	# -----------------------------------
	# - Dividendes versés
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] == "FN":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FN",
		"libelle" : "- Dividendes versés",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_1 = flux_activite_capitaux_propres_1 + balance
	flux_activite_capitaux_propres_1_n1 = flux_activite_capitaux_propres_1_n1 + balance_n1

	# -----------------------------------
	# Flux de trésorerie provenant des capitaux propres (Somme FK à FN)
	balance = flux_activite_capitaux_propres_1
	balance_n1 = flux_activite_capitaux_propres_1_n1
	item = {
		"reference" : "ZD",
		"libelle" : "Flux de trésorerie provenant des capitaux propres (Somme FK à FN)",
		"lettre" : "D",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_financement = flux_activite_financement + balance
	flux_activite_financement_n1 = flux_activite_financement_n1 + balance_n1

	# -----------------------------------
	# Trésorerie provenant des capitaux étrangers
	item = {
		"reference" : "",
		"libelle" : "Trésorerie provenant des capitaux étrangers",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "",
		"balance_n1" : ""
	}
	donnees_flux_tresorerie.append(item)

	# -----------------------------------
	# + Emprunts
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] == "84":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FO",
		"libelle" : "+ Emprunts",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_2 = flux_activite_capitaux_propres_2 + balance
	flux_activite_capitaux_propres_2_n1 = flux_activite_capitaux_propres_2_n1 + balance_n1

	# -----------------------------------
	# + Autres dettes financières
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] in ("85", "86"):
			balance = balance + float(item_tb["balance_n"])
			balance_n1 = balance_n1 + float(item_tb["balance_n1"])
	item = {
		"reference" : "FP",
		"libelle" : "+ Autres dettes financières",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_2 = flux_activite_capitaux_propres_2 + balance
	flux_activite_capitaux_propres_2_n1 = flux_activite_capitaux_propres_2_n1 + balance_n1

	# -----------------------------------
	# - Remboursements des emprunts et autres dettes financières
	balance = 0
	balance_n1 = 0
	for item_tb in donnees_tb_financement:
		if item_tb["reference"] == "87":
			balance = float(item_tb["balance_n"])
			balance_n1 = float(item_tb["balance_n1"])
	item = {
		"reference" : "FQ",
		"libelle" : "- Remboursements des emprunts et autres dettes financières ",
		"lettre" : "",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_capitaux_propres_2 = flux_activite_capitaux_propres_2 + balance
	flux_activite_capitaux_propres_2_n1 = flux_activite_capitaux_propres_2_n1 + balance_n1

	# -----------------------------------
	# Flux de trésorerie provenant des capitaux propres (Somme FO à FQ)
	balance = flux_activite_capitaux_propres_2
	balance_n1 = flux_activite_capitaux_propres_2_n1
	item = {
		"reference" : "ZE",
		"libelle" : "Flux de trésorerie provenant des capitaux propres (Somme FO à FQ)",
		"lettre" : "E",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	flux_activite_financement = flux_activite_financement + balance
	flux_activite_financement_n1 = flux_activite_financement_n1 + balance_n1

	# -----------------------------------
	# Flux de  trésorerie provenant des activités de financement (D + E)
	balance = flux_activite_financement
	balance_n1 = flux_activite_financement_n1
	item = {
		"reference" : "ZF",
		"libelle" : "Flux de  trésorerie provenant des activités de financement (D + E)",
		"lettre" : "F",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	variation_tresorerie_nette = variation_tresorerie_nette + balance
	variation_tresorerie_nette_n1 = variation_tresorerie_nette + balance_n1

	# -----------------------------------
	# VARIATION DE LA TRESORERIE NETTE DE LA PERIODE (B+C+F)
	balance = variation_tresorerie_nette
	balance_n1 = variation_tresorerie_nette_n1
	item = {
		"reference" : "ZG",
		"libelle" : "VARIATION DE LA TRESORERIE NETTE DE LA PERIODE (B+C+F)",
		"lettre" : "G",
		"note" : "",
		"est_total" : False,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)
	controle_tresorerie_nette_periode = controle_tresorerie_nette_periode + balance
	controle_tresorerie_nette_periode_n1 = controle_tresorerie_nette_periode_n1 + balance_n1

	# -----------------------------------
	# Trésorerie nette au 31 décembre (G + A)
	# Contrôle : Trésorerie-actif N -  Trésorerie-passif N
	balance = controle_tresorerie_nette_periode
	balance_n1 = controle_tresorerie_nette_periode_n1
	item = {
		"reference" : "ZH",
		"libelle" : "Trésorerie nette au 31 décembre (G + A)    Contrôle : Trésorerie-actif N -  Trésorerie-passif N",
		"lettre" : "H",
		"note" : "",
		"est_total" : True,
		"balance_n" : "%.2f" % balance,
		"balance_n1" : "%.2f" % balance_n1
	}
	donnees_flux_tresorerie.append(item)


	context = {
		'title' : "Tableau des flux de trésorerie",
		"donnees_flux_tresorerie" : donnees_flux_tresorerie,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7
	}
	return context

def post_generer_tresorerie(request):
	try:
		# droit="GENERER_FLUX_TRESORERIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 373
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		context = post_traiter_tresorerie(request, utilisateur, modules, sous_modules)


		template = loader.get_template("ErpProject/ModuleComptabilite/flux_tresorerie/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_tresorerie"))


def post_imprimer_tresorerie(request):
	try:
		# droit="IMPRIMER_FLUX_TRESORERIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 373
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_tresorerie(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleComptabilite/reporting/flux_tresorerie.html", "flux_tresorerie.pdf", context)
	except Exception as e:
		# #print("ERREUR print FLUX TRESORERIE")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_tresorerie"))


#  NOTES ANNEXES
def get_generer_annexe(request):

	# droit="GENERER_FLUX_TRESORERIE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 374
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer les notes annexes',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'actions':auth.toGetActions(modules,utilisateur),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 9
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/annexe/generate.html")
	return HttpResponse(template.render(context, request))


def post_traiter_annexe(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_COMPTABILITE):
	#On recupère et format les inputs reçus
	#TODO Donner la possibilité de choisir l'année fiscale, puis mettre une restriction par rapport à l'interval de date choisie
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#TODO Filtrer par rapport à la devise choisie
	devise_id = int(request.POST["devise_id"])
	devise = dao_devise.toGetDevise(devise_id)
	devise = dao_devise.toGetDeviseReference()

	comptes = []
	donnees_annexe = []

	#On récupère les données de la balance de la periode
	donnees_balance = balanceArray.toGetInPeriode(date_debut, date_fin, devise)

	# ------------------------------------------------
	# NOTE 1: DETTES GARANTIES PAR DES SURETES REELLES
	# ------------------------------------------------
	item = {"reference" : "NOTE-1"}
	sous_total1 = 0
	sous_total2 = 0
	sous_total3 = 0


	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1612":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_1",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_1"] = "%.2f" % balance

	sous_total1 = sous_total1 + balance

	balance1 = 0
	balance2 = balance
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "161":
			solde = float(item_balance["credit_solde"])
			balance1 = float(balance1) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_2",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	balance = balance1 - balance2
	item["note1_montant_2"] = "%.2f" % balance

	sous_total1 = sous_total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "162":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_3",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_3"] = "%.2f" % balance

	sous_total1 = sous_total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] in ("163","164","165","166","167","168","181","182","183","184"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_4",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_4"] = "%.2f" % balance

	sous_total1 = sous_total1 + balance

	balance = sous_total1
	item["note1_st_1"] = "%.2f" % balance


	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "172" or item_balance["numero_compte"][0:4] == "1762":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_5",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_5"] = "%.2f" % balance

	sous_total2 = sous_total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "173" or item_balance["numero_compte"][0:4] == "1763":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_6",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_6"] = "%.2f" % balance

	sous_total2 = sous_total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1741" or item_balance["numero_compte"][0:5] == "17641":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_7",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_7"] = "%.2f" % balance

	sous_total2 = sous_total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "1742" or item_balance["numero_compte"][0:5] == "17642":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_8",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_8"] = "%.2f" % balance

	sous_total2 = sous_total2 + balance

	balance = sous_total2
	item["note1_st_2"] = "%.2f" % balance


	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "40":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_9",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_9"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "41":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_10",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_10"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "42":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_11",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_11"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "43":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_12",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_12"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "44":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_13",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_13"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "45":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_14",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_14"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "46":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_15",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_15"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:2] == "47":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_16",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_16"] = "%.2f" % balance

	sous_total3 = sous_total3 + balance

	balance = sous_total3
	item["note1_st_3"] = "%.2f" % balance


	balance = sous_total1 + sous_total2 + sous_total3
	item["note1_total_123"] = "%.2f" % balance


	# Engagements financiers
	total1 = 0
	total2 = 0

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] == "90581":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_17",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_17"] = "%.2f" % balance

	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] == "90181":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_18",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_18"] = "%.2f" % balance

	total2 = total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] == "90582":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_19",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_19"] = "%.2f" % balance

	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] == "90582":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_20",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_20"] = "%.2f" % balance

	total2 = total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] in ("9061", "9062"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_21",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_21"] = "%.2f" % balance

	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] in ("9021", "9022"):
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_22",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_22"] = "%.2f" % balance

	total2 = total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "9063" or item_balance["numero_compte"][0:5] in ("90583", "90584", "90585"):
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_23",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_23"] = "%.2f" % balance

	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "9023" or item_balance["numero_compte"][0:5] in ("90281", "90282", "90283"):
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_24",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_24"] = "%.2f" % balance

	total2 = total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "415":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_25",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_25"] = "%.2f" % balance
	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:3] == "415":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_26",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_26"] = "%.2f" % balance
	total2 = total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] == "41112":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_27",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_27"] = "%.2f" % balance
	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:5] == "41112":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_28",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_28"] = "%.2f" % balance
	total2 = total2 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "9041":
			solde = float(item_balance["credit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_29",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde crédit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_29"] = "%.2f" % balance
	total1 = total1 + balance

	balance = 0
	for item_balance in donnees_balance:
		if item_balance["numero_compte"][0:4] == "9084":
			solde = float(item_balance["debit_solde"])
			balance = float(balance) + float(solde)
			#On enregistre aussi les comptes qui entrent en jeu
			compte = {
				"reference" : "note1_montant_30",
				"numero_compte" : item_balance["numero_compte"],
				"designation_compte" : item_balance["designation_compte"],
				"libelle_montant": "Solde débit",
				"balance" : solde,
			}
			comptes.append(compte)
	item["note1_montant_30"] = "%.2f" % balance
	total2 = total2 + balance

	balance = total1
	item["note1_total_1"] = "%.2f" % balance


	balance = total2
	item["note1_total_2"] = "%.2f" % balance

	donnees_annexe.append(item)

	context = {
		'title' : "Notes annexes du Système Normal",
		"donnees_annexe" : donnees_annexe,
		"comptes" : comptes,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		"devise" : devise,
		'actions':auth.toGetActions(modules,utilisateur),
		"utilisateur" : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7
	}
	return context

def post_generer_annexe(request):
	try:
		# droit="GENERER_BALANCE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 374
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_annexe(request, utilisateur, modules, sous_modules)

		template = loader.get_template("ErpProject/ModuleComptabilite/annexe/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_annexe(request):
	try:
		# droit="IMPRIMER_FLUX_TRESORERIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 374
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_annexe(request, utilisateur, modules, sous_modules)

		name = "notes_annexes.pdf"
		download_dir = settings.DOWNLOAD_DIR
		target=os.path.join(download_dir, name)

		fs = FileSystemStorage(download_dir)
		with fs.open(name) as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format("Notes Annexes")
			return response
	except Exception as e:
		# #print("ERREUR print FLUX TRESORERIE")
		# #print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

# DEVISES VIEWS
def get_lister_devises(request):

	# droit="LISTER_DEVISE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 103
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	# model = dao_devise.toListDevises()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_devise.toListDevises(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste des dévises',
		'model' : model,
		'view': view,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 17
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/devise/list.html")
	return HttpResponse(template.render(context, request))


def get_creer_devise(request):

	# droit="CREER_DEVISE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 102
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response


	context = {
		'title' : 'Nouvelle devise',
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 17
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/devise/add.html")
	return HttpResponse(template.render(context, request))

def post_creer_devise(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		code_iso = request.POST["code_iso"]
		symbole_devise = request.POST["symbole_devise"]

		devise = dao_devise.toCreateDevise(symbole_devise, code_iso, designation)
		devise = dao_devise.toSaveDevise(auteur, devise)

		if devise == None:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la devise")
			return HttpResponseRedirect(reverse("module_comptabilite_creer_devise"))
		else:
			messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_comptabilite_details_devise', args=(devise.id,)))
	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_devise"))

def get_modifier_devise(request, ref):

	try:

		# droit="MODIFIER_DEVISE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 104
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_devise.toGetDevise(ref)
		context = {
			'title' : 'Modifier %s' % model.designation,
			"model" : model,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 17
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/devise/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_devises"))

def post_modifier_devise(request):
	ref = int(request.POST["ref"])

	try:
		designation = request.POST["designation"]
		code_iso = request.POST["code_iso"]
		symbole_devise = request.POST["symbole_devise"]

		devise = dao_devise.toCreateDevise(symbole_devise, code_iso, designation)
		devise = dao_devise.toUpdateDevise(ref, devise)

		if devise != None:
			messages.add_message(request,messages.SUCCESS,"Opération effectuée avec succès !")
			return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la mise à jour de la devise")
			return HttpResponseRedirect(reverse("module_comptabilite_modifier_devise", args=(ref,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_modifier_devise", args=(ref,)))

def get_details_devise(request, ref):

	try:

		# droit="LISTER_DEVISE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 103
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_devise.toGetDevise(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context = {
			'title' : 'Devise %s' % model.designation,
			"model" : model,
			"taux_change" : dao_taux_change.toGetTauxCourantDeLaDeviseArrive(model.id),
			"devise_ref" : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 17
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/devise/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR DETAIL DEVISE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_devises"))

def get_activer_devise(request, ref):

	try:

		# droit="ACTIVER_DEVISE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 104
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_devise.toGetDevise(ref)
		is_done = dao_devise.toActiveDevise(model.id, True)
		if is_done == True: return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'activation de la devise")
			return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
	except Exception as e:
		#print("ERREUR ACTIVER DEVISE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_devises"))

def get_desactiver_devise(request, ref):

	try:

		# droit="DESACTIVER_DEVISE"

		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 104
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_devise.toGetDevise(ref)
		is_done = dao_devise.toActiveDevise(model.id, False)
		if is_done == True: return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la desactivation de la devise")
			return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
	except Exception as e:
		#print("ERREUR DESACTIVER DEVISE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_devises"))

def get_referencer_devise(request, ref):
	try:
		# droit="REFERENCER_DEVISE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 104
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_devise.toGetDevise(ref)
		is_done = dao_devise.toReferenceDevise(model.id)
		if is_done == True: return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération'")
			return HttpResponseRedirect(reverse("module_comptabilite_details_devise", args=(ref,)))
	except Exception as e:
		#print("ERREUR REFERENCER DEVISE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_devises"))

# TAUX DE CHANGE VIEWS
def get_lister_taux_change(request):

	# droit="LISTER_TAUX_DE_CHANGE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 103
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response


	# model = dao_taux_change.toListTauxCourant()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_taux_change.toListTauxCourant(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context = {
		'title' : 'Liste des taux de change',
		'model' : model,
		"devise_ref" : dao_devise.toGetDeviseReference(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 10
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/taux/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_taux_change(request, ref):
	try:
		# droit="CREER_TAUX_DE_CHANGE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 102
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_devise.toGetDevise(ref)

		context = {
			'title' : 'Taux de change',
			'model' : model,
			"devise_ref" : dao_devise.toGetDeviseReference(),
			"taux_courant" : dao_taux_change.toGetTauxCourantDeLaDeviseArrive(model.id),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/taux/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR CREER TAUX")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_devises"))

def post_creer_taux_change(request):
	devise_arrivee_id = int(request.POST["devise_arrivee_id"])
	try:
		auteur = identite.utilisateur(request)
		devise_ref = dao_devise.toGetDeviseReference()
		montant = makeFloat(request.POST["montant"])

		taux_courant = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise_arrivee_id)
		if taux_courant != None:
			taux_courant.est_courant = False
			dao_taux_change.toUpdateTaux(taux_courant.id, taux_courant)

		taux_change = dao_taux_change.toCreateTaux(devise_ref.id, devise_arrivee_id, montant, True)
		taux_change = dao_taux_change.toSaveTaux(auteur, taux_change)

		if taux_change == None:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
			return HttpResponseRedirect(reverse("module_comptabilite_creer_taux_change", args=(devise_arrivee_id,)))
		else:
			messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_comptabilite_details_devise', args=(devise_arrivee_id,)))
	except Exception as e:
		#print("ERREUR POST CREER TAUX")
		#print(e)
		messages.error(request,e)
		messages.add_message(request, messages.SERROR,e)
		return HttpResponseRedirect(reverse("module_comptabilite_creer_taux_change", args=(devise_arrivee_id,)))

# CONFIGURATION CONTROLLER
def get_modifier_parametre(request):
	try:
		permission_number = 464
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#print("DEBUT")

		vente_par_defaut				=	dao_compte.toGetCompteVente()
		achat_par_defaut				=	dao_compte.toGetCompteAchat()
		fournisseur_par_defaut			=	dao_compte.toGetCompteFournisseur()
		client_par_defaut				=	dao_compte.toGetCompteClient()
		taxe_par_defaut					=	dao_compte.toGetCompteTaxe()
		caisse_par_defaut				=	dao_compte.toGetCompteCaisse()
		banque_par_defaut				=	dao_compte.toGetCompteBanque()
		marchandise_par_defaut			=	dao_compte.toGetCompteMarchandise()
		personnel_par_defaut			=	dao_compte.toGetComptePersonnel()
		salaire_par_defaut				=	dao_compte.toGetCompteSalaire()
		liaison_par_defaut				=	dao_compte.toGetCompteLiaison()

		devise_ref = dao_devise.toGetDeviseReference()
		comptes = dao_compte.toListComptes()

		#print("FIN AFFETACTION")

		context = {
			'title' : 'Paramètrage de la comptabilité',
			"devise_ref" : devise_ref,
			"comptes" : comptes,
			"exercice": dao_annee_fiscale.toGetAnneeFiscaleActive(),
			"taux_courant" : dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise_ref.id),
			"vente_par_defaut" : vente_par_defaut,
			"achat_par_defaut"	: achat_par_defaut,
			"fournisseur_par_defaut" : fournisseur_par_defaut,
			"client_par_defaut" : client_par_defaut,
			"taxe_par_defaut" : taxe_par_defaut,
			"caisse_par_defaut" : caisse_par_defaut,
			"banque_par_defaut" : banque_par_defaut,
			"marchandise_par_defaut" : marchandise_par_defaut,
			"personnel_par_defaut" : personnel_par_defaut,
			"salaire_par_defaut" : salaire_par_defaut,
			"liaison_par_defaut" : liaison_par_defaut,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/configuration/index.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR CONFIGURATION")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))

@transaction.atomic
def post_modifier_configuration(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		devise_ref = dao_devise.toGetDeviseReference()
		configured = True

		## MaJ Seuil d'immobilisation
		seuil_immobilisation = float(request.POST["seuil_immobilisation"])
		if seuil_immobilisation > 1:
			dao_annee_fiscale.toUpdateSeuilImmobilisationOfAnneeFiscaleActive(seuil_immobilisation)


		compte_vente_par_defaut_id			=	int(request.POST["vente_par_defaut"])
		compte_achat_par_defaut_id			=	int(request.POST["achat_par_defaut"])
		compte_fournisseur_par_defaut_id	=	int(request.POST["fournisseur_par_defaut"])
		compte_client_par_defaut_id			=	int(request.POST["client_par_defaut"])
		compte_taxe_par_defaut_id			=	int(request.POST["taxe_par_defaut"])
		compte_caisse_par_defaut_id			=	int(request.POST["caisse_par_defaut"])
		compte_banque_par_defaut_id			=	int(request.POST["banque_par_defaut"])
		compte_marchandise_par_defaut_id	=	int(request.POST["marchandise_par_defaut"])
		compte_personnel_par_defaut_id		=	int(request.POST["personnel_par_defaut"])
		compte_salaire_par_defaut_id		=	int(request.POST["salaire_par_defaut"])
		compte_liaison_par_defaut_id		=	int(request.POST["liaison_par_defaut"])

		configured	=	dao_compte.toSetCompteVente(compte_vente_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteAchat(compte_achat_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteFournisseur(compte_fournisseur_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteClient(compte_client_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteTaxe(compte_taxe_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteCaisse(compte_caisse_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteBanque(compte_banque_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteMarchandise(compte_marchandise_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetComptePersonnel(compte_personnel_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteSalaire(compte_salaire_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')
		configured	=	dao_compte.toSetCompteLiaison(compte_liaison_par_defaut_id)
		if configured == False : raise Exception('vente_par_defaut non modifie')


		messages.add_message(request, messages.SUCCESS, "Configuration mise à jour avec succès")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_comptabilite_modifier_configuration"))
	except Exception as e:
		#print("ERREUR POST CONFIGURATION")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la configuration")
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_modifier_configuration"))

# FACTURE FOURNISSEUR CONTROLLER
def get_lister_factures_fournisseur(request):

	# droit="LISTER_FACTURE_FOURNISSEUR"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 106
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_facture_fournisseur.toListFacturesFournisseurMere()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_facture_fournisseur.toListFacturesFournisseurMere(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	#Traitement des vues
	# vue_profil = dao_groupe_permission.toGetGroupePermissionDeLaPersonne(utilisateur.id)

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste des factures fournisseur',
		'model' : model,
		"utilisateur" : utilisateur,
		'view':view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 21,
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_facture(request):
	try:
		# droit="CREER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 107
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
				response

		devises = dao_devise.toListDevisesActives()
		articles = dao_article.toListArticlesAchetables()
		categories = dao_categorie_article.toListCategoriesArticle()
		comptes = dao_compte.toListComptes()
		taxes = dao_taxe.toListTaxeOfTypeAchat()

		fournitures = dao_bon_reception.toListFournituresFacturablesByWorkflow()

		try:
			fournitures = []
			doc_id = request.POST["doc_id"]
			#print("doc id", doc_id)
			bon_reception = dao_bon_reception.toGetBonReception(doc_id)
			fournitures.append(bon_reception)
		except Exception as e:
			fournitures = dao_bon_reception.toListFournituresFacturablesByWorkflow()
			#print("Aucun bon de command trouvé")

		compte_default = dao_compte.toGetCompteAchat()
		centres = dao_centre_cout.toListCentreCoutOfTypeAccount()

		context = {
			'title' : 'Nouvelle facture',
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'fournitures' : fournitures,
			'devises' : devises,
			'articles' : articles,
			'centres':centres,
			'comptes':comptes,
			'taxes':taxes,
			'compte_default':compte_default,
			'categories' : categories,
			"utilisateur" : utilisateur,
			"devises" : dao_devise.toListDevisesActives(),
			'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST CREER TAUX")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_factures_fournisseur"))

def post_valider_facture(request):
	try:
		# droit="CREER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 107
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		numero_facture = dao_facture.toGenerateNumeroFacture()

		date_facturation = request.POST["date_facturation"]
		reference_facture = request.POST["reference_facture"]
		order_id = int(request.POST["order_id"])
		condition_reglement_id = request.POST["condition_reglement_id"]
		#Traitement cas facture partielle ou intgrale
		est_integral = request.POST["est_integral"]#(s'il vaut 2, c'est une facture partielle d'un bon de commande; si'il vaut 1, c'est total, s'il vaut 0, facture ne dependant pas d'un bon de commande)

		order = None

		#print("order id", order_id)

		type_facture = 0

		if order_id == 0 or order_id == None or order_id == "":
			order_id = ""
			type_facture = 1
		#print("LIGNE FACTURE")

		#Format lignes facture et ecriture débit en cas de ligne facture (dans le constat d'achat, les ecritures de debit dependent des lignes de facture)
		ecritures_debit = []
		lignes_facture = []
		lignes_analytiques = [] #Format lignes analytiques
		total_fact = 0.0

		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		list_libelle = request.POST.getlist("libelle", None)
		list_ligne_bon_commande_id = request.POST.getlist('ligne_bon_commande_id', None)
		list_compte = request.POST.getlist("compte", None)
		#traitement des taxex dans count select
		list_taxe_id = request.POST.getlist("taxe",None)
		list_remise_id = request.POST.getlist("remise",None)
		list_count_select = request.POST.getlist("count_select",None)

		#Centres des couts / comptes analytiques:
		list_centre_cout = request.POST.getlist("centre_cout",None)

		#Traitement de la liste des taxes recues
		list_taxe = dao_taxe.toDesignListTaxe(list_taxe_id, list_count_select)
		#print("liste de taxe",list_taxe)
		#print(len(list_article_id))
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		montant_total_taxe = 0
		montant_total_remise = 0
		#Preparation des ecritures de taxes
		ecritures_taxes = []

		#Traitement
		for i in range(0, len(list_article_id)) :
			article_id = int(list_article_id[i])
			quantite_demandee = makeFloat(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])
			libelle = list_libelle[i]
			#Test de l'équivalence d'une ligne de commande à une ligne de facture pr retrouver la ligne budgetaire
			try:
				ligne_bon_commande_id = list_ligne_bon_commande_id[i]
			except Exception as e:
				ligne_bon_commande_id = 0



			remise = list_remise_id[i]
			if remise == "":
				remise = 0
			else:
				remise = makeFloat(remise)
			compte_id = int(list_compte[i])

			centre_cout_id = list_centre_cout[i]
			if centre_cout_id == "" or centre_cout_id == '0':
				centre_cout_id = None
			else:
				centre_cout_id = int(centre_cout_id)

			taxe_tab = list_taxe[i]
			#print("taxe tab", taxe_tab)

			article = dao_article.toGetArticle(article_id)
			unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)

			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			#Application de la remise
			total = total - (total*remise/100)
			total_fact = makeFloat(total_fact) + makeFloat(total)
			#print("compute")
			#Calcul du montant par ligne de la taxe et préparation des ecritures de taxe
			montant_taxe,ecritures_taxes = dao_taxe.toComputeMontantAndEcritureTaxe(taxe_tab,total, ecritures_taxes, centre_cout_id)
			montant_total_taxe += montant_taxe



			symbole_unite = "Elt"
			if article.unite:
				#print("***********************", article.unite)
				symbole_unite = article.unite.symbole_unite




			#format lignes facture
			ligne = {
				"article_id" : article_id,
				"nom_article" : article.designation,
				"quantite" : quantite_demandee,
				"prix_unitaire" : prix_unitaire,
				"prix_total" : total,
				"symbole_unite" : symbole_unite,
				"montant_taxe": montant_taxe,
				"remise":remise,
				'ligne_bon_commande_id': ligne_bon_commande_id,
				'compte_id': compte_id,

			}
			lignes_facture.append(ligne)

			#Affectation du compte comptable de l'article
			compte_article = dao_compte.toGetCompte(compte_id)



			#format ecriture debit
			ecriture = {
				"id" : compte_article.id,
				"libelle" : libelle,
				"compte" : "%s %s" % (compte_article.numero, compte_article.designation),
				"montant" : total,
				"centre_cout_id": centre_cout_id,
			}
			ecritures_debit.append(ecriture)


		#Ajout des ecritures comptables de la taxe à liste des ecritures de debit définis
		ecritures_debit.extend(ecritures_taxes)

		#Agregation des ecritures de même comptes
		ecritures_debit = dao_ecriture_comptable.toAgregateEcritureComptable(ecritures_debit)


		montant = total_fact

		#Traitement sur la TVA
		'''compte_taxe = dao_compte.toGetCompteTaxe()
		ecriture = {
			"id" : compte_taxe.id,
			"libelle" : compte_taxe.designation,
			"compte" : "%s %s" % (compte_taxe.numero, compte_taxe.designation),
			"montant" : montant_total_taxe
		}
		ecritures_debit.append(ecriture)'''


		comptes = dao_compte.toListComptes()
		devise_id = request.POST["devise_id"]
		devise = dao_devise.toGetDevise(devise_id)
		fournisseur_id = request.POST["fournisseur_id"]
		fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)
		#print("FIN 0")
		compte_fournisseur = dao_compte.toGetCompteFournisseur()
		#print("COMPTE FRS")
		if fournisseur.compte != None: compte_fournisseur = dao_compte.toGetCompte(fournisseur.compte_id)
		#print(compte_fournisseur)
		#print("FIN 1")
		#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

		#Format ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
		montant_total = montant + montant_total_taxe - montant_total_remise

		ecritures_credit = []
		ecriture = {
			"id" : compte_fournisseur.id,
			"libelle" : fournisseur.nom_complet,
			"compte" : "%s %s" % (compte_fournisseur.numero, compte_fournisseur.designation),
			"montant" : montant_total
		}
		ecritures_credit.append(ecriture)
		#print("FIN 2")
		#Format Facture

		facture = {
			"date_facturation" : date_facturation,
			"numero_facture" : numero_facture,
			"montant_ht" : montant,
			"montant_taxe_total":montant_total_taxe,
			"montant_total_remise":montant_total_remise,
			'montant_total':montant_total,
			"order_id" : order_id,
			"reference_facture": reference_facture,
			"est_integral": est_integral,
			"condition_reglement_id" : condition_reglement_id
		}
		#print('lignes fini')


		#ON VERIFIE L'ATTACHEMENT DU DOCUMENT
		if 'document_upload' in request.FILES:
			#print("OKKKKKKKKKKKKK")
			file = request.FILES["document_upload"]

			facture_doc_dir = 'documents/facture/fournisseur/'
			media_dir = media_dir + '/' + facture_doc_dir
			id = dao_facture_fournisseur.toGetNextId()
			#print(id)
			save_path = os.path.join(media_dir, str(id) + '.JPG')
			path = default_storage.save(save_path, file)
			document = Model_Image(doc = media_url + facture_doc_dir + str(id)+'.JPG')
			document.save()

		context = {
			'title' : 'Validation facture',
			'facture' : facture,
			'type_facture' : type_facture,
			'devise' : devise,
			'fournisseur' : fournisseur,
			'comptes'   : comptes,
			'bon_achat' : order,
			'lignes_facture' : lignes_facture,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'ecritures_credit': ecritures_credit,
			'ecritures_debit' : ecritures_debit,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/validate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,"Veuillez selectionner une taxe applicable")
		return HttpResponseRedirect(reverse("module_comptabilite_add_facture_fournisseur"))

@transaction.atomic
def post_creer_facture(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		numero_facture = request.POST["numero_facture"]
		est_integral = request.POST["est_integral"] #Test sur le caractere partiel ou integrale d'un bon de commande rattaché à une facture
		date_facturation = request.POST["date_facturation"]
		reference_facture = request.POST["reference_facture"]
		if date_facturation != None and date_facturation != "":
			date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))
		fournisseur_id = int(request.POST["fournisseur_id"])
		type_facture = int(request.POST["type_facture"])
		if type_facture == 0:
			order_id = request.POST["order_id"]
		else:
			order_id = None

		dev_id = request.POST["devise_id"]
		condition_reglement_id = request.POST["condition_reglement_id"]
		if condition_reglement_id == 0: condition_reglement_id = None

		montant_taxe = request.POST["montant_taxe"]

		#Traitement cas facture partielle ou intgrale
		est_integral = request.POST["est_integral"]#(s'il vaut 2, c'est une facture partielle d'un bon de commande; si'il vaut 1, c'est total, s'il vaut 0, facture ne dependant pas d'un bon de commande)

		#On recupère le fournisseur et le compte fournisseur à créditer
		fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)
		compte_fournisseur = dao_compte.toGetCompteFournisseur()
		#print("compte_fournisseur %s" % compte_fournisseur)
		if fournisseur.compte != None: compte_fournisseur = dao_compte.toGetCompte(fournisseur.compte_id)
		#print("compte_fournisseur recupere")
		#print("compte_fournisseur")

		devise_ref = dao_devise.toGetDeviseReference()
		taux_id = None

		lignes = []

		# ECRITURES COMPTABLES DUES AU CONSTAT DE L'ACHAT
		date_piece = timezone.now()
		if date_facturation != None and date_facturation != "":
			date_piece = date_facturation
		type_journal = dao_type_journal.toGetTypeAchat()
		#print(type_journal)
		journal_achat = dao_journal.toGetJournalDefautOf(type_journal["id"])
		journal_id = None
		if journal_achat != None: journal_id = journal_achat.id
		#print("Journal recuperee")
		piece_comptable_id = None

		#Creation du lettrage referençant la facture
		lettrage = dao_lettrage.toCreateLettrage(dao_lettrage.toGenerateDesignationLettrage(), numero_facture)
		lettrage = dao_lettrage.toSaveLettrage(auteur,lettrage)
		#print("Journal 1111")

		montant = 0.0

		facture = dao_facture_fournisseur.toCreateFactureFournisseur(date_facturation, numero_facture, 0, order_id, journal_id,"",reference_facture, fournisseur_id, None, lettrage.id, condition_reglement_id)
		facture = dao_facture_fournisseur.toSaveFactureFournisseur(auteur, facture)

		#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables
		piece_comptable = dao_piece_comptable.toCreatePieceComptable("Pièce FF %s" % facture.numero_facture , facture.numero_facture, montant, journal_id, date_piece, fournisseur_id, None, order_id, facture.id, "CONSTAT D'ACHAT", dev_id , taux_id)
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print("PIECE CREEEEEEE ID %s" % piece_comptable.id)
		#piece_comptable_id = piece_comptable.id


		#print("FACT SAVED")

		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, facture)
		### Fin traitement document

		#Enregistrements des lignes factures
		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("qte", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		list_montant_taxe = request.POST.getlist("ligne_montant_taxe", None)
		list_remise = request.POST.getlist("remise", None)
		list_compte_id = request.POST.getlist("compte_id", None)
		#print("DEBUT LIGNES")
		#print(len(list_article_id))
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		#print(len(list_remise))
		montant_taxe_total = 0
		montant = 0




		for i in range(0, len(list_article_id)) :
			#print("ART ID %s" % list_article_id[i])
			#print("QTE %s" % list_quantite_demandee)
			#print("PRIX %s" % list_prix_unitaire)

			article_id = list_article_id[i]
			montant_taxe = list_montant_taxe[i]
			compte_id = list_compte_id[i]
			montant_taxe_total += makeFloat(montant_taxe)
			quantite_demandee = makeFloat(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])

			remise = makeFloat(list_remise[i]) if list_remise[i] != "" else 0

			#print("L1")


			article = dao_article.toGetArticle(article_id)
			unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
			unite_achat_id = unite_achat.id if unite_achat else None


			#print("L2")
			#print("le montant est là, avant assignation", montant)
			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			total = total - (total * remise / 100)
			montant = makeFloat(montant) + makeFloat(total)
			#print("**********************",montant)

			#print("FACT ID ")
			#print("FACT ID %s" % facture.id)
			# #print("ARTICLE %s" % article.id)
			# #print("UNITE %s" % unite_achat)

			ligne = dao_ligne_facture.toCreateLigneFacture(article.designation,facture.id, article.id, quantite_demandee, prix_unitaire, unite_achat_id, montant_taxe, remise, compte_id)
			ligne = dao_ligne_facture.toSaveLigneFacture(ligne)


		#print("FACT UPDATED")
		facture.montant_ht = montant
		facture.devise_id = dev_id
		facture.montant_taxe = makeFloat(montant_taxe_total)
		facture.montant = montant + makeFloat(montant_taxe_total)
		facture.montant_en_lettre = trad.trad(facture.montant)
		facture.save()

		#print("FACT UPDATED")
		if devise_ref.id != dev_id:
			#print("Les taux sont différents ...")
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(dev_id)
			if taux != None: taux_id = taux.id





		#Creation ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
		#On cree l'ecriture de crédit
		list_compte_credit_id = request.POST.getlist("compte_credit_id", None)
		list_montant_credit = request.POST.getlist("montant_credit", None)
		list_devise_credit = request.POST.getlist("devise_credit", None)
		list_libelle_credit = request.POST.getlist("libelle_credit", None)


		for i in range(0, len(list_compte_credit_id)):
			compte_credit = list_compte_credit_id[i]
			montant_credit = makeFloat(list_montant_credit[i])
			devise_credit = list_devise_credit[i]
			libelle_credit = list_libelle_credit[i]

			ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(libelle_credit, 0, montant_credit, compte_credit, piece_comptable.id, facture.lettrage_id, facture.date_echeance)
			ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
			ecriture_credit.save()
			#print("ecriture_credit {} cree".format(ecriture_credit.id))

		if facture != None :
			#print("Facture {} creee".format(facture.id))
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					facture.document = doc.doc
					facture.save()
				Model_Image.objects.all().delete()


			#Creation les ecriture débit (dans le constat d'achat, ce sont les comptes des éléments des lignes de facture, ici les articles, qui sont débités)
			list_compte_debit_id = request.POST.getlist("compte_debit_id", None)
			list_montant_debit = request.POST.getlist("montant_debit", None)
			list_devise_debit = request.POST.getlist("devise_debit", None)
			list_libelle_debit = request.POST.getlist("libelle_debit", None)

			list_centre_cout_id = request.POST.getlist("centre_cout_id", None)


			for i in range(0, len(list_compte_debit_id)):
				#print("on entre")
				compte_debit = list_compte_debit_id[i]
				montant_debit = makeFloat(list_montant_debit[i])
				devise_debit = list_devise_debit[i]
				libelle_debit = list_libelle_debit[i]
				centre_cout_id = list_centre_cout_id[i]
				#print("centre de cout", centre_cout_id)

				ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(libelle_debit, montant_debit, 0, compte_debit, piece_comptable.id, facture.lettrage_id)
				ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
				ecriture_debit.save()
				#print("ecriture_debit {} cree".format(ecriture_debit.id))

				#Ecritures pour analytique
				if (centre_cout_id != "") and (centre_cout_id != "0") and (centre_cout_id != None) and (centre_cout_id != "None"):
					#print("je suis enrrééééééééééé")
					montant_debit = -1 * montant_debit
					ecriture_analytique = dao_ecriture_analytique.toCreateEcriture_analytique(libelle_debit,compte_debit,centre_cout_id,facture.id,montant_debit,dev_id,2,ecriture_debit.id)
					ecriture_analytique = dao_ecriture_analytique.toSaveEcriture_analytique(auteur,ecriture_analytique)
				#print("end of line")

			# WORKFLOWS INITIALS
			#print("Debut workflow")
			type_document = "Facture fournisseur"
			wkf_task.initializeWorkflow(auteur,facture,type_document)


			#Bon reception if existe
			if order_id != "" and order_id != None:
				#Cas facture complet (est_integral = 2, partiel)
				if est_integral == "1":
					bon_reception = dao_bon_reception.toGetBonReception(order_id)
					wkf_task.passingStepWorkflow(auteur,bon_reception)

			#On passe les transactions budgetaires REEEL
			if facture.bon_reception != None:
				list_ligne_bon_commande_id = request.POST.getlist('ligne_bon_commande_id', None)
				is_done = dao_transactionbudgetaire.toCreateTransactionReelBudgetaire(auteur, facture, list_ligne_bon_commande_id )
			else:
				is_done = dao_transactionbudgetaire.toCreateTransactionReelBCNull(auteur, facture)


			#TODO Créer les lignes de facture
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_fournisseur', args=(facture.id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la facture")
			return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))
	except Exception as e:
		#print("ERREUR POST CREER FACTURE FOURNISSEUR!")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

def get_modifier_facture(request, ref):
	# droit="MODIFIER_FACTURE_FOURNISSEUR"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 108
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		id = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)

		title = "la facture"
		if facture.numero_facture != None and facture.numero_facture != "" : title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"

		context = {
			'title' : 'Modifier %s' % title,
			'model' : facture,
			'menu' : 21,
			'lignes' : lignes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'bon'   : bon_reception,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

def post_modifier_facture(request):
	id = int(request.POST["ref"])
	try:
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))

		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		facture.numero_facture = numero_facture
		facture.date_facturation = date_facturation
		is_done = dao_facture_fournisseur.toUpdateFactureFournisseur(facture.id,facture)

		if is_done != False :
			messages.add_message(request, messages.SUCCESS, "Configuration mise à jour avec succès")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture', args=(facture.id,)))
		else :
			return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(facture.id,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(id,)))

# PAIEMENT FACTURE FOURNISSEUR CONTROLLER

def get_lister_paiements_fournisseur(request):
	try:
		# droit="LISTER_PAIEMENT_FOURNISSEUR_COMPTA"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 305
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_paiement.toListPaiementsFournisseur()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_paiement.toListPaiementsFournisseur(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		types_paiement = dao_type_paiement.toListTypePaiement()
		context = {
			'title' : 'Liste des paiements fournisseur',
			'model' : model,
			"utilisateur" : utilisateur,
			"types_paiement" : types_paiement,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_COMPTABILITE,
			'modules' : modules,
			'sous_modules': sous_modules,
			'menu' : 28
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/fournisseur/list.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_tableau_de_bord'))

def get_creer_paiement_fournisseur(request):
	try:
		# droit="CREER_PAIEMENT_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 306
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		moyen_paiement = dao_moyen_paiement.toListMoyenPaiement()
		types_paiement = dao_type_paiement.toListTypePaiement()
		fournisseurs = dao_fournisseur.toListFournisseursActifs()
		journaux = dao_journal.toListJournaux()

		#print("on est ma")

		context = {
			'title' : "Nouveau réglement",
			'devises' : devises,
			'devise_ref' : devise_ref,
			'menu': 28,
			'moyen_paiement' : moyen_paiement,
			'types_paiement' : types_paiement,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'journaux' : journaux,
			'fournisseurs' : fournisseurs,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/fournisseur/add.html")
		return HttpResponse(template.render(context,request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_fournisseur'))

def get_creer_paiement_facture_fournisseur(request, ref):
	try:
		# droit="CREER_PAIEMENT_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 306
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		id = int(ref)
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		journaux = dao_journal.toListJournaux()
		moyen_paiement = dao_moyen_paiement.toListMoyenPaiement()
		types_paiement = dao_type_paiement.toListTypePaiement()

		operations = dao_operationtresorerie.toListOperationtresorerieNonCloture()

		context = {
			'title' : "Nouveau réglement de facture",
			'devises' : devises,
			'operations':operations,
			'devise_ref' : devise_ref,
			'menu' : 28,
			'facture' : facture,
			'journaux' : journaux,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'moyen_paiement' : moyen_paiement,
			'types_paiement' : types_paiement,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/fournisseur/facture/add.html")
		return HttpResponse(template.render(context,request))
	except Exception as e:
		#print("ERREUR !")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_fournisseur'))

#SECUNDO
@transaction.atomic
def post_creer_paiement_fournisseur(request):
	sid = transaction.savepoint()
	ref = int(request.POST["ref"])
	try:
		#print("debut post avec ref {}".format(ref))
		devise_ref = dao_devise.toGetDeviseReference()
		auteur = identite.utilisateur(request)
		date_paiement = request.POST["date_paiement"]
		date_paiement = timezone.datetime(int(date_paiement[6:10]), int(date_paiement[3:5]), int(date_paiement[0:2]))

		montant = makeFloat(request.POST["montant"])
		designation = str(request.POST["designation"])
		description = str(request.POST["description"])
		type_paiement = int(request.POST["type_paiement"])
		#journal_id = int(request.POST["journal_id"])
		operation_tresorerie_id = int(request.POST["operation_tresorerie_id"])

		devise_id = int(request.POST["devise_id"])
		partenaire_id = int(request.POST["partenaire_id"])

		operation_tresorerie = dao_operationtresorerie.toGetOperationtresorerie(operation_tresorerie_id)
		journal_id = operation_tresorerie.journal_id

		devise = dao_devise.toGetDevise(devise_id)
		journal = dao_journal.toGetJournal(journal_id)
		fournisseur = dao_fournisseur.toGetFournisseur(partenaire_id)
		transaction_paiement_id = None
		facture_id = None
		taux_id = None
		lettrage_id = None

		if ref != 0:
			facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)
			myfacturebgt = dao_facture_fournisseur.toGetFactureFournisseur(ref) #Variable dediée au traitement budget
			lettrage_id = facture.lettrage_id
			# On verifie si la facture est mere ou fille
			if facture.est_mere == True:
				facture_id = facture.id
			else:

				if makeFloat(facture.montant_restant) != makeFloat(montant):
					messages.add_message(request, messages.ERROR , "Le montant de paiement de la facture d'avance doit être égal au montant payé")
					return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_facture_fournisseur', args=(facture.id,)))
				else:
					# On charge la facture mere pour y passer les écritires comptables
					facture = dao_facture_fournisseur.toGetFactureFournisseur(facture.facture_mere_id)
					facture_id = facture.id


			montant_facture = facture.montant_restant

			if devise.id == facture.devise_id:
				#print("devise existe")
				if makeFloat(montant_facture) <= makeFloat(montant) :
					facture.est_soldee = True
					facture.save()
					#dao_facture_fournisseur.toUpdateFactureFournisseur(facture.id, facture)


		#Un paiement effectué annule la possibilité de constituer une facture d'avoir
		#print("nullable ???")
		facture.est_nullable = False
		facture.save()
		#print("annulé ")

		#On enregistre la transaction
		statut_transaction = dao_statut_transaction.toGetStatutSuccess()
		transaction_paiement = dao_transaction.toCreateTransaction(facture_id, statut_transaction["id"], 1)
		transaction_paiement = dao_transaction.toSaveTransaction(auteur, transaction_paiement)
		transaction_paiement_id = transaction_paiement.id
		#print('transaction cree avec id {}'.format(transaction_paiement_id))

		#On définit le taux
		if devise.id != devise_ref.id:
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)
			if taux != None: taux_id = taux.id

		# On enregistre le paiement
		paiement = dao_paiement.toCreatePaiement(transaction_paiement_id, date_paiement, facture_id, devise.id, montant, type_paiement, journal.id , partenaire_id , auteur.id, designation, description)
		#print(paiement)
		paiement = dao_paiement.toSavePaiement(paiement)
		#print('paiement cree avec id {}'.format(paiement.id))
		if ref != 0:
			paiement.est_lettre = True
			paiement.est_valide = True
			paiement.save()

		#On enregistre le payloads (Informations supplémentaires et utile pour le paiement)
		logs = "{'journal':'%s', 'montant':'%s', 'devise':'%s' }" % (journal.designation, montant, devise.designation)
		payloads = dao_payloads.toCreatePayloads(paiement.id, logs)
		dao_payloads.toSavePayloads(payloads)
		#print('payloads cree avec id {}'.format(dao_payloads.id))

		# ECRITURES COMPTABLES DUES AU PAIEMENT DU FOURNISSEUR
		#Ici On débite le compte de trésorerie
		date_piece = timezone.now()
		compte_tresorerie = journal.compte_debit

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(paiement.designation, "", montant, journal_id, date_piece, partenaire_id, None, None, facture_id, "PAIEMENT FOURNISSEUR", devise.id, taux_id)
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print('piece cree avec id {}'.format(piece_comptable.id))


		#print('dev ',devise.id)
		ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, montant, 0, compte_tresorerie.id, piece_comptable.id, lettrage_id)
		ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
		#print('here we are')
		#print('ecriture credit cree avec id {}'.format(ecriture_credit.id))

		#On crédite le compte du fournisseur
		compte_fournisseur = dao_compte.toGetCompteFournisseur()
		if fournisseur.compte != None: compte_fournisseur = dao_compte.toGetCompte(fournisseur.compte_id)

		ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(fournisseur.nom_complet, 0, montant, compte_fournisseur.id, piece_comptable.id, lettrage_id)
		ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
		#print('ecriture debit cree avec id {}'.format(ecriture_debit.id))


		# On solde la facture fille par default après le paiement
		facture2 = dao_facture_fournisseur.toGetFactureFournisseur(ref)
		if facture2.est_mere == False:
			facture2.est_soldee = True
			facture2.save()

		#print('Check Etat Fcture')
		if makeFloat(facture.montant_restant) <= 0:
			#print('FACT SOLDEE')
			facture.est_soldee = True
			facture.save()

		## On crée la reference au ligne de paiement
		type_operation = 2 #Retrait
		ligne_operation = dao_ligne_operation_tresorerie.toCreateLigne_operation_tresorerie(designation,"Paiement facture"+facture.numero_facture,partenaire_id,montant,devise_id,taux_id,type_operation, description,operation_tresorerie.id,date_paiement)
		ligne_operation = dao_ligne_operation_tresorerie.toSaveLigne_operation_tresorerie(auteur,ligne_operation)
		ligne_operation.est_lettre = True
		ligne_operation.paiement_id = paiement.id
		ligne_operation.save()

		#Enregistrement du lien entre paiement et operation tresorerie
		paiement.ligne_operation_tresorerie_id = ligne_operation.id
		paiement.save()

		transaction.savepoint_commit(sid)
		if ref != 0:
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_fournisseur', args=(facture_id,)))
		else : return HttpResponseRedirect(reverse('module_comptabilite_details_paiement_fournisseur', args=(paiement.id,)))
	except Exception as e:
		#print("ERREUR POST")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		if ref != 0:
			return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_facture_fournisseur', args=(ref,)))
		else: return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_fournisseur'))

def get_details_paiement_fournisseur(request, ref):
	try:
		# droit="LISTER_PAIEMENT_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 305
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		paiement = dao_paiement.toGetPaiement(ref)
		#print("PAIEMENT")
		#print(ref)
		types_paiement = dao_type_paiement.toListTypePaiement()
		#print(types_paiement)

		title = "Paiement"
		title = title + " %s" % paiement.designation
		#print(paiement.designation)

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,paiement)


		context = {
			'title' : title,
			'model' : paiement,
			'types_paiement' : types_paiement,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'menu' : 28,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/fournisseur/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_fournisseur'))


# FACTURE FOURNISSEUR AVANCE CONTROLLER
def get_lister_facture_avance(request):

	# droit="LISTER_FACTURE_FOURNISSEUR"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 5558
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_facture_fournisseur.toListFacturesFournisseurMere()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_facture_fournisseur.toListFacturesFournisseurAcompte(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	#Traitement des vues
	# vue_profil = dao_groupe_permission.toGetGroupePermissionDeLaPersonne(utilisateur.id)

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste des factures d\'acompte fournisseur',
		'model' : model,
		"utilisateur" : utilisateur,
		'view':view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 21,
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/avance/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_facture_avance(request, ref):
	try:
		# droit="CREER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 107
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		devises = dao_devise.toListDevisesActives()
		articles = dao_article.toListArticlesAchetables()
		categories = dao_categorie_article.toListCategoriesArticle()
		facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)


		#print("FRS  %s" % facture.fournisseur.nom_complet)

		context = {
			'title' : 'Nouvelle facture avance',
			'facture_principale' : facture,
			'fournitures' : dao_bon_reception.toListFournituresFacturables(),
			'devises' : devises,
			'articles' : articles,
			'categories' : categories,
			'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"utilisateur" : utilisateur,
			"devises" : dao_devise.toListDevisesActives(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/avance/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST CREER TAUX")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_factures_fournisseur"))

def post_valider_facture_avance(request):
	try:

		permission_number = 107
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")


		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		numero_facture = request.POST["numero_facture"]
		facture_mere_id = request.POST["facture_mere_id"]

		if None == numero_facture or "" == numero_facture: numero_facture = dao_facture.toGenerateNumeroFacture()

		date_facturation = request.POST["date_facturation"]

		order_id = "0"
		order = None
		type_facture = 0

		#print("LIGNE FACTURE")
		type_facture = 1
		#Format lignes facture et ecriture débit en cas de ligne facture (dans le constat d'achat, les ecritures de debit dependent des lignes de facture)
		ecritures_debit = []
		lignes_facture = []
		total_fact = 0.0

		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		#print(len(list_article_id))
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		for i in range(0, len(list_article_id)) :
			article_id = int(list_article_id[i])
			quantite_demandee = makeFloat(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])

			article = dao_article.toGetArticle(article_id)
			unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)

			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			total_fact = makeFloat(total_fact) + makeFloat(total)

			#format lignes facture
			ligne = {
				"article_id" : article_id,
				"nom_article" : article.designation,
				"quantite" : quantite_demandee,
				"prix_unitaire" : prix_unitaire,
				"prix_total" : total,
				"symbole_unite" : ""
			}
			lignes_facture.append(ligne)

			"""
			compte_article = dao_compte.toGetCompteMarchandise()
			if article.compte != None: compte_article = dao_compte.toGetCompte(article.compte_id)

			#format ecriture debit
			ecriture = {
				"id" : compte_article.id,
				"libelle" : article.designation,
				"compte" : "%s %s" % (compte_article.numero, compte_article.designation),
				"montant" : total
			}
			ecritures_debit.append(ecriture)
			"""
		montant = total_fact

		comptes = dao_compte.toListComptes()
		devise_id = request.POST["devise_id"]
		devise = dao_devise.toGetDevise(devise_id)
		fournisseur_id = request.POST["fournisseur_id"]
		fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)
		#print("FIN 0")
		compte_fournisseur = dao_compte.toGetCompteFournisseur()
		#print("COMPTE FRS")
		if fournisseur.compte != None: compte_fournisseur = dao_compte.toGetCompte(fournisseur.compte_id)
		#print(compte_fournisseur)
		#print("FIN 1")
		#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

		#Format ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
		"""
		ecritures_credit = []
		ecriture = {
			"id" : compte_fournisseur.id,
			"libelle" : fournisseur.nom_complet,
			"compte" : "%s %s" % (compte_fournisseur.numero, compte_fournisseur.designation),
			"montant" : montant
		}
		ecritures_credit.append(ecriture)
		"""
		#print("FIN 2")

		#Format Facture
		facture = {
			"date_facturation" : date_facturation,
			"numero_facture" : numero_facture,
			"montant" : montant,
			"order_id" : ""
		}
		#print('lignes fini')


		#ON VERIFIE L'ATTACHEMENT DU DOCUMENT
		if 'document_upload' in request.FILES:
			#print("OKKKKKKKKKKKKK")
			file = request.FILES["document_upload"]
			facture_doc_dir = 'documents/facture/fournisseur/'
			media_dir = media_dir + '/' + facture_doc_dir
			id = dao_facture_fournisseur.toGetNextId()
			#print(id)
			save_path = os.path.join(media_dir, str(id) + '.JPG')
			path = default_storage.save(save_path, file)
			document = Model_Image(doc = media_url + facture_doc_dir + str(id)+'.JPG')
			document.save()

		context = {
			'title' : 'Validation facture',
			'facture' : facture,
			'type_facture' : type_facture,
			'devise' : devise,
			'fournisseur' : fournisseur,
			'facture_mere_id' : facture_mere_id,
			#'comptes'   : comptes,
			#'bon_achat' : order,
			'lignes_facture' : lignes_facture,
			#'ecritures_credit': ecritures_credit,
			#'ecritures_debit' : ecritures_debit,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/avance/validate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_bons_achat"))

@transaction.atomic
def post_creer_facture_avance(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))
		order_id = request.POST["order_id"]
		fournisseur_id = int(request.POST["fournisseur_id"])
		type_facture = int(request.POST["type_facture"])
		dev_id = request.POST["devise_id"]
		facture_mere_id = request.POST["facture_mere_id"]

		#On recupère le fournisseur et le compte fournisseur à créditer
		fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)
		compte_fournisseur = dao_compte.toGetCompteFournisseur()
		#print("compte_fournisseur %s" % compte_fournisseur)
		if fournisseur.compte != None: compte_fournisseur = dao_compte.toGetCompte(fournisseur.compte_id)
		#print("compte_fournisseur recupere")
		#print(compte_fournisseur)

		devise_ref = dao_devise.toGetDeviseReference()
		taux_id = None

		lignes = []

		# ECRITURES COMPTABLES DUES AU CONSTAT DE L'ACHAT
		date_piece = timezone.now()

		type_journal = dao_type_journal.toGetTypeAchat()
		#print(type_journal)
		journal_achat = dao_journal.toGetJournalDefautOf(type_journal["id"])
		journal_id = None
		if journal_achat != None: journal_id = journal_achat.id
		#print("Journal recuperee")


		#print("FACT 1")
		montant = 0.0

		#print("FACT MERE ID %s" % facture_mere_id)
		facture_mere = dao_facture_fournisseur.toGetFacture(facture_mere_id)
		facture = dao_facture_fournisseur.toCreateFactureFournisseur(date_facturation, numero_facture, 0, None, journal_id,"","", fournisseur_id, facture_mere_id, facture_mere.lettrage_id)
		facture = dao_facture_fournisseur.toSaveFactureFournisseur(auteur, facture)
		#print("FACTURE %s" % facture)

		#print("FACT SAVED")
		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("qte", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		#print("DEBUT LIGNES")
		#print(len(list_article_id))
		#print(list_article_id)
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		for i in range(0, len(list_article_id)) :
			#print("ART ID %s" % list_article_id[i])
			#print("QTE %s" % list_quantite_demandee)
			#print("PRIX %s" % list_prix_unitaire)

			article_id = list_article_id[i]
			quantite_demandee = makeFloat(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])

			#print("L1")

			article = dao_article.toGetArticle(article_id)
			unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
			unite_achat_id = unite_achat.id if unite_achat else None


			#print("L2")
			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			montant = makeFloat(montant) + makeFloat(total)

			#print("FACT ID ")
			#print("FACT ID %s" % facture.id)
			#print("ARTICLE %s" % article.id)
			#print("UNITE %s" % unite_achat)

			ligne = dao_ligne_facture.toCreateLigneFacture(article.designation,facture.id, article.id, quantite_demandee, prix_unitaire, unite_achat_id)
			ligne = dao_ligne_facture.toSaveLigneFacture(ligne)
			#print("Ligne %s" % ligne)

			#print("L5")
			#On rajoute le stock_article
			ligne.save()
			#print("Ligne %s" % ligne)

		#print("Fin LIGNES")

		facture.montant = montant
		facture.devise_id = facture_mere.devise_id
		facture.save()
		#print("FACT UPDATED")

		if facture != None :
			#print("Facture creee")
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					facture.document = doc.doc
					facture.save()
				Model_Image.objects.all().delete()


		#print("FIN DOCUMENT")
		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, facture)


		# WORKFLOWS INITIALS
		#print("Debut workflow")
		type_document = "Facture fournisseur"
		workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)
		#print(workflow)

		if workflow != None:
			#print("NON NULL")
			etape = dao_wkf_etape.toGetEtapeInitialWorkflow(workflow.id)
			facture.statut_id = etape.id
			facture.etat = etape.designation
			facture.save()

			#print("AUTEUR %s" % auteur.id)

			historique = dao_wkf_historique_facture.toCreateHistoriqueWorkflow(auteur.id, etape.id, facture.id)
			historique = dao_wkf_historique_facture.toSaveHistoriqueWorkflow(historique)

			#TODO Créer les lignes de facture
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_fournisseur', args=(facture.id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
			return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

	except Exception as e:
		#print("ERREUR POST CREER FACTURE FOURNISSEUR!")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

def get_modifier_facture(request, ref):
	# droit="MODIFIER_FACTURE_FOURNISSEUR"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 108
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		id = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)

		title = "la facture"
		if facture.numero_facture != None and facture.numero_facture != "" : title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"

		context = {
			'title' : 'Modifier %s' % title,
			'model' : facture,
			'menu' : 21,
			'lignes' : lignes,
			'bon'   : bon_reception,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

def post_modifier_facture(request):
	id = int(request.POST["ref"])
	try:
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))

		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		facture.numero_facture = numero_facture
		facture.date_facturation = date_facturation
		is_done = dao_facture_fournisseur.toUpdateFactureFournisseur(facture.id,facture)

		if is_done != False :
			messages.add_message(request, messages.SUCCESS, "Configuration mise à jour avec succès")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture', args=(facture.id,)))
		else :
			messages.add_message(request, messages.ERROR,"Une erruer est survenue lors de l'opération")
			return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(facture.id,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(id,)))


def get_details_facture(request, ref):
	try:
		# droit="LISTER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 106
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		montant_paye = facture.montant_paye
		montant_restant = facture.montant_restant

		#print("Il faut ozela")

		'''historique = dao_wkf_historique_facture.toListHistoriqueOfFacture(facture.id)
		transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(facture.statut_id)'''

		title = "Facture"
		if facture.numero_facture != None and facture.numero_facture != "" :
			title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"

		if bon_reception != None :
			type_facture = "Bon"
		else :
			type_facture = "Ligne"

		lignes = dao_ligne_facture.toListLigneOfFacture(ref)
		factures_filles = dao_facture.toListFacturesFilles(facture.id)

		#Test si la facture possède une facture d'avoir déjà enregistrée afin de bloquer les boutons permettant certaines opérations

		hasFactureAvoir = dao_facture.toCheckIfHasGotFactureAvoir(facture.id)
		#print("has facture avoir ?", hasFactureAvoir)
		paiements = dao_paiement.toListPaiementOfFacture(facture.id)
		is_solded = dao_paiement.toCheckPaiementSoldeOfFacture(facture.id, facture.montant)

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,facture)




		context = {
			'title' : title,
			'model' : facture,
			'type_facture' : type_facture,
			#'bon'   : bon_reception,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'roles':groupe_permissions,
			'content_type_id':content_type_id,
			'documents':documents,
			'lignes' : lignes,
			'paiements':paiements,
			'is_solded':is_solded,
			'hasFactureAvoir':hasFactureAvoir,
			'menu' : 21,
			'factures_filles':factures_filles,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'montant_paye' : montant_paye,
			'montant_restant' : montant_restant
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET DETAILS FACTURE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

def get_imprimer_facture_fournisseur(request):
	try:
		# droit="IMPRIMER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

		permission_number = 106
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
		#print("ref", ref)

		ref = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		montant_paye = facture.montant_paye
		montant_restant = facture.montant_restant



		'''historique = dao_wkf_historique_facture.toListHistoriqueOfFacture(facture.id)
		transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(facture.statut_id)'''

		title = "Facture"
		if facture.numero_facture != None and facture.numero_facture != "" :
			title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"



		if bon_reception != None :
			type_facture = "Bon"
		else :
			type_facture = "Ligne"

		lignes = dao_ligne_facture.toListLigneOfFacture(ref)

		factures_filles = dao_facture.toListFacturesFilles(facture.id)

		#Test si la facture possède une facture d'avoir déjà enregistrée afin de bloquer les boutons permettant certaines opérations

		hasFactureAvoir = dao_facture.toCheckIfHasGotFactureAvoir(facture.id)
		#print("has facture avoir ?", hasFactureAvoir)
		paiements = dao_paiement.toListPaiementOfFacture(facture.id)
		is_solded = dao_paiement.toCheckPaiementSoldeOfFacture(facture.id, facture.montant)

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,facture)

		context = {
			'title' : title,
			'model' : facture,
			'type_facture' : type_facture,
			'bon'   : bon_reception,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'roles':groupe_permissions,
			'content_type_id':content_type_id,
			'documents':documents,
			'lignes' : lignes,
			'paiements':paiements,
			'is_solded':is_solded,
			'hasFactureAvoir':hasFactureAvoir,
			'menu' : 21,
			'factures_filles':factures_filles,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'montant_paye' : montant_paye,
			'montant_restant' : montant_restant
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/facture_fournisseur.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'facture_fournisseur.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('facture_fournisseur.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response

		return response
	except Exception as e:
		# print("ERREUR print FACTURE FOURNISSEUR")
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))




# FACTURE D'AVOIR CONTROLLER


# FACTURE CLIENT CONTROLLER



def get_creer_facture_avoir(request, ref):
	try:
		# droit="CREER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 449
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)

		'''if bon_reception != None :
			type_facture = "Bon"
			#print("Bon ID %s" % (bon_reception.id))
			lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)
		else :'''
		type_facture = "Ligne"
		#print("LIGNE ID %s" % (ref))
		lignes = dao_ligne_facture.toListLigneOfFacture(ref)

		context = {
			'title' : "Nouvelle facture d'avoir",
			'facture' : facture,
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'fournitures' : dao_bon_reception.toListFournituresFacturables(),
			'lignes' : lignes,
			'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"devises" : dao_devise.toListDevisesActives(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/avoir/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST CREER TAUX")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_factures_fournisseur"))

def post_valider_facture_avoir(request):
	try:
		permission_number = 449
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")


		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		numero_facture = request.POST["numero_facture"]
		facture_mere_id = request.POST["facture_mere_id"]

		if 'numero_facture' in request.POST:
			numero_facture = request.POST["numero_facture"]
		else:
			numero_facture = dao_facture.toGenerateNumeroFacture()

		date_facturation = request.POST["date_facturation"]

		order_id = int(request.POST["order_id"])
		order = None
		type_facture = 0

		#print("mamouchk")

		if order_id == 0:
			order_id = ""
			type_facture = 1
			devise_id = request.POST["devise_id"]
			devise = dao_devise.toGetDevise(devise_id)
			fournisseur_id = request.POST["fournisseur_id"]
			fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)
		else:
			order = dao_bon_reception.toGetBonReception(order_id)
			devise = dao_devise.toGetDevise(order.devise_id)
			fournisseur = dao_fournisseur.toGetFournisseur(order.fournisseur_id)

		facture_mere = dao_facture.toGetFacture(facture_mere_id)


		facture = {
			"date_facturation" : date_facturation,
			"numero_facture" : numero_facture,
			"montant" : facture_mere.montant,
			"order_id" : order_id
		}
		#print('lignes fini')


		#ON VERIFIE L'ATTACHEMENT DU DOCUMENT
		if 'document_upload' in request.FILES:
			#print("OKKKKKKKKKKKKK")
			file = request.FILES["document_upload"]
			facture_doc_dir = 'documents/facture/fournisseur/'
			media_dir = media_dir + '/' + facture_doc_dir
			id = dao_facture_fournisseur.toGetNextId()
			#print(id)
			save_path = os.path.join(media_dir, str(id) + '.JPG')
			path = default_storage.save(save_path, file)
			document = Model_Image(doc = media_url + facture_doc_dir + str(id)+'.JPG')
			document.save()

		#MyTreatment
		#print("before t")
		lignes_facture = dao_ligne_facture.toListLigneOfFacture(facture_mere_id)
		comptes = dao_compte.toListComptes()
		ecritures_debit = []
		ecritures_credit = []
		piece_comptable = dao_piece_comptable.toGetPieceComptableFromFacture(facture_mere_id)
		ecritures_comptables = dao_ecriture_comptable.toListEcrituresComptablesOfPieceComptable(piece_comptable.id)
		for ecriture_comptable in ecritures_comptables:
			if ecriture_comptable.montant_credit == 0:
				ecriture = {
				"id" : ecriture_comptable.compte_id,
				"libelle" : ecriture_comptable.designation,
				"compte" : "%s %s" % (ecriture_comptable.compte.numero, ecriture_comptable.compte.designation),
				"montant" : ecriture_comptable.montant_debit
				}
				ecritures_credit.append(ecriture)
			elif ecriture_comptable.montant_debit == 0:
				ecriture = {
				"id" : ecriture_comptable.compte_id,
				"libelle" : ecriture_comptable.designation,
				"compte" : "%s %s" % (ecriture_comptable.compte.numero, ecriture_comptable.compte.designation),
				"montant" : ecriture_comptable.montant_credit
				}
				ecritures_debit.append(ecriture)


		context = {
			'title' : 'Validation facture',
			'facture' : facture,
			'facture_mere_id' : facture_mere_id,
			'type_facture' : type_facture,
			'devise' : devise,
			'comptes':comptes,
			'fournisseur' : fournisseur,
			'bon_achat' : order,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'lignes_facture' : lignes_facture,
			'ecritures_credit': ecritures_credit,
			'ecritures_debit' : ecritures_debit,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/avoir/validate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_bons_achat"))

@transaction.atomic
def post_creer_facture_avoir(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))
		order_id = request.POST["order_id"]
		fournisseur_id = int(request.POST["fournisseur_id"])
		type_facture = int(request.POST["type_facture"])
		dev_id = request.POST["devise_id"]
		facture_mere_id = request.POST["facture_mere_id"]

		facture_mere = dao_facture.toGetFacture(facture_mere_id)

		#On recupère le fournisseur et le compte fournisseur à créditer
		fournisseur = dao_fournisseur.toGetFournisseur(fournisseur_id)
		compte_fournisseur = dao_compte.toGetCompteFournisseur()
		#print("compte_fournisseur %s" % compte_fournisseur)
		if fournisseur.compte != None: compte_fournisseur = dao_compte.toGetCompte(fournisseur.compte_id)
		#print("compte_fournisseur recupere")
		#print(compte_fournisseur)

		devise_ref = dao_devise.toGetDeviseReference()
		taux_id = None

		lignes = []

		# ECRITURES COMPTABLES DUES AU CONSTAT DE L'ACHAT
		date_piece = timezone.now()
		type_journal = dao_type_journal.toGetTypeAchat()
		#print(type_journal)
		journal_achat = dao_journal.toGetJournalDefautOf(type_journal["id"])
		journal_id = None
		if journal_achat != None: journal_id = journal_achat.id
		#print("Journal recuperee")

		if type_facture == 0:
			order = dao_bon_reception.toGetBonReception(order_id)
			montant = order.prix_total
			facture = dao_facture_fournisseur.toCreateFactureFournisseur(date_facturation, numero_facture, montant, order_id, journal_id,"","", fournisseur_id)
			facture = dao_facture_fournisseur.toSaveFactureFournisseur(auteur, facture)
			facture.facture_mere_id = facture_mere_id
			facture.est_facture_avoir = True
			facture.save()

			if devise_ref.id != order.devise_id:
				#print("Les taux sont différents ...")
				taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(order.devise_id)
				if taux != None: taux_id = taux.id

			#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables
			piece_comptable = dao_piece_comptable.toCreatePieceComptable(order.numero_reception, order.reference_document, montant, journal_id, date_piece, fournisseur.id, None, order.id, facture.id, "CONSTAT D'ACHAT", order.devise_id, taux_id)
			piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
			#print("piece cree")

			lignes = dao_ligne_reception.toListLigneOfReceptions(order.id)

		elif type_facture == 1:
			#print("FACT 1")
			montant = 0.0

			facture = dao_facture_fournisseur.toCreateFactureFournisseur(date_facturation, numero_facture, 0, None, None,"","", fournisseur_id)
			facture = dao_facture_fournisseur.toSaveFactureFournisseur(auteur, facture)
			facture.facture_mere_id = facture_mere_id
			facture.est_facture_avoir = True
			facture.save()

			#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables
			piece_comptable = dao_piece_comptable.toCreatePieceComptable(facture.numero_facture, None, montant, journal_id, date_piece, fournisseur_id, None, None, facture.id, "CONSTAT D'ACHAT", dev_id , taux_id)
			piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
			#print("piece cree")

			#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

			lignes = dao_ligne_facture.toListLigneOfFacture(facture.id)

			#print("FACT SAVED")
		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("qte", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		list_montant_taxe = request.POST.getlist("ligne_montant_taxe", None)
		#print("DEBUT LIGNES")
		#print(list_article_id)
		#print(len(list_article_id))
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		for i in range(0, len(list_article_id)) :
			#print("ART ID %s" % list_article_id[i])
			#print("QTE %s" % list_quantite_demandee)
			#print("PRIX %s" % list_prix_unitaire)

			article_id = int(list_article_id[i])
			#print("article", article_id)
			quantite_demandee = int(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])
			montant_taxe = list_montant_taxe[i]
			#print("renvoy",montant_taxe)

			#print("L1")

			article = dao_article.toGetArticle(article_id)

			#print("article", article)
			unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
			unite_achat_id = unite_achat.id if unite_achat else None


			#print("L2")
			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			montant = makeFloat(montant) + makeFloat(total)

			#print(muzomba)

			#print("FACT ID ")
			#print("FACT ID %s" % facture.id)
			#print("ARTICLE %s" % article.id)
			#print("UNITE %s" % unite_achat)

			ligne = dao_ligne_facture.toCreateLigneFacture(article.designation,facture.id, article.id, quantite_demandee, prix_unitaire, unite_achat_id, montant_taxe)
			ligne = dao_ligne_facture.toSaveLigneFacture(ligne)
			#print("Ligne %s" % ligne)

			#print("L5")
			#On rajoute le stock_article
			#ligne.save()
		#print("Fin LIGNES")

		facture.montant = montant
		facture.save()

		#print("FACT UPDATED")
		if devise_ref.id != dev_id:
			#print("Les taux sont différents ...")
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(dev_id)
			if taux != None: taux_id = taux.id



		#Creation ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
		#On cree l'ecriture de crédit
		#print("*********************************")
		list_compte_credit_id = request.POST.getlist("compte_credit_id", None)
		#print(list_compte_credit_id)
		list_montant_credit = request.POST.getlist("montant_credit", None)
		#print(list_montant_credit)
		list_devise_credit = request.POST.getlist("devise_credit", None)
		list_libelle_credit = request.POST.getlist("libelle_credit", None)

		for i in range(0, len(list_compte_credit_id)):
			compte_credit = list_compte_credit_id[i]
			montant_credit = list_montant_credit[i]
			devise_credit = list_devise_credit[i]
			libelle_credit = list_libelle_credit[i]

			ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(libelle_credit, 0, montant_credit, compte_credit, piece_comptable.id, facture_mere.lettrage_id)
			ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
			ecriture_credit.save()
			#print("ecriture_credit {} cree".format(ecriture_credit.id))

		if facture != None :
			#print("Facture {} creee".format(facture.id))
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					facture.document = doc.doc
					facture.save()
				Model_Image.objects.all().delete()


			#Creation les ecriture débit (dans le constat d'achat, ce sont les comptes des éléments des lignes de facture, ici les articles, qui sont débités)
			list_compte_debit_id = request.POST.getlist("compte_debit_id", None)
			list_montant_debit = request.POST.getlist("montant_debit", None)
			list_devise_debit = request.POST.getlist("devise_debit", None)
			list_libelle_debit = request.POST.getlist("libelle_debit", None)

			for i in range(0, len(list_compte_debit_id)):
				compte_debit = list_compte_debit_id[i]
				montant_debit = list_montant_debit[i]
				devise_debit = list_devise_debit[i]
				libelle_debit = list_libelle_debit[i]

				ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(libelle_debit, montant_debit, 0, compte_debit, piece_comptable.id, facture_mere.lettrage_id)
				ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
				ecriture_debit.save()
				#print("ecriture_debit {} cree".format(ecriture_debit.id))

			#Transactions budgetaires
			transactions = dao_transactionbudgetaire.toListTransactionBudgetaireOfFacture(facture_mere_id)

			for une_transaction in transactions:
				montant_total = (-1)*float(une_transaction.montant)
				transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire("Annulation Paiement Réel du bon de commande {0} via la facture {1}".format(facture.bon_reception.numero_reception, facture.numero_facture),montant_total,"",une_transaction.devise_id,une_transaction.poste_budgetaire_id,auteur.id,une_transaction.ligne_budgetaire_id,1,2)
				transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur,transactionBudgetaire)
				transactionBudgetaire.bon_reception = une_transaction.bon_reception
				transactionBudgetaire.facture = facture


			# WORKFLOWS INITIALS
			#print("Debut workflow")
			type_document = "Facture fournisseur"
			workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)
			#print(workflow)

			if workflow != None:
				#print("NON NULL")
				etape = dao_wkf_etape.toGetEtapeInitialWorkflow(workflow.id)
				facture.statut_id = etape.id
				facture.etat = etape.designation
				facture.save()

				#print("AUTEUR %s" % auteur.id)

				historique = dao_wkf_historique_facture.toCreateHistoriqueWorkflow(auteur.id, etape.id, facture.id)
				historique = dao_wkf_historique_facture.toSaveHistoriqueWorkflow(historique)

			#TODO Créer les lignes de facture
			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_fournisseur', args=(facture.id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la facture")
			return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))
	except Exception as e:
		#print("ERREUR POST CREER FACTURE FOURNISSEUR!")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))



# FACTURE CLIENT CONTROLLER
def get_lister_factures_client(request):

	# droit="LISTER_FACTURE_CLIENT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 110
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_facture_client.toListFacturesClient()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_facture_client.toListFacturesClient(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste des factures clients',
		'model' : model,
		"utilisateur" : utilisateur,
		'view':view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 21
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/facture/client/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_facture_client(request):
	try:
		# droit="CREER_FACTURE_CLIENT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 109
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		devises = dao_devise.toListDevisesActives()
		articles = dao_article.toListArticlesVendables()
		categories = dao_categorie_article.toListCategoriesArticle()
		type_facture = dao_type_facture.toListTypefactureClient()
		comptes = dao_compte.toListComptes()
		taxes = dao_taxe.toListTaxeOfTypeVente()
		etat_facturations = dao_etat_facturation.toListEtatFacturationValides()
		etat_facturations = dao_etat_facturation.toListEtatFacturation()
		#print("Etat facturation**************", etat_facturations)

		compte_default = dao_compte.toGetCompteVente()
		centres = dao_centre_cout.toListCentreCoutOfTypeAccount()

		context = {
			'title' : 'Nouvelle facture',
			'clients' : dao_client.toListClientsActifs(),
			'commandes' : dao_bon_commande.toListCommandes(),
			'etat_facturations' : etat_facturations,
			'type_facture':type_facture,
			'type_services': Model_Type_service.objects.all(),
			'devises' : devises,
			'articles' : articles,
			'comptes':comptes,
			'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
			'compte_default':compte_default,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'taxes':taxes,
			'centres':centres,
			'categories' : categories,
			"utilisateur" : utilisateur,
			"devises" : dao_devise.toListDevisesActives(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/client/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST CREER TAUX")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_factures_fournisseur"))

def post_valider_facture_client(request):
	try:
		# droit="CREER_FACTURE_CLIENT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 109
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		numero_facture = ""#request.POST["numero_facture"]
		etat_facturation_id = request.POST["etat_facturation_id"]
		type_facture_client = request.POST["type_facture_client"]
		type_service = request.POST["type_service"]
		autres_infos = request.POST["autres_infos"]
		numero_facture = dao_facture.toGenerateNumeroFacture()

		#if None == numero_facture or "" == numero_facture: numero_facture = dao_facture.toGenerateNumeroFacture()

		date_facturation = request.POST["date_facturation"]

		order_id = int(request.POST["order_id"])
		order = None
		type_facture = 0

		#print("Etat FACTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT %s" % etat_facturation_id)
		etat_facturation = dao_etat_facturation.toGetEtatFacturation(etat_facturation_id)
		#print("Etat FACTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT %s" % etat_facturation)
		if order_id == 0 or order_id == None or order_id == "":
			order_id = ""
			order = dao_bon_reception.toGetBonReception(order_id)
			type_facture = 1
		#print("LIGNE FACTURE")

		#Format lignes facture et ecriture débit en cas de ligne facture (dans le constat d'achat, les ecritures de debit dependent des lignes de facture)
		ecritures_credit = []
		lignes_facture = []
		lignes_analytiques = [] #Format lignes analytiques
		total_fact = 0.0

		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		list_libelle = request.POST.getlist("libelle", None)
		list_compte = request.POST.getlist("compte", None)
		#traitement des taxex dans count select
		list_taxe_id = request.POST.getlist("taxe",None)
		list_remise_id = request.POST.getlist("remise",None)
		list_count_select = request.POST.getlist("count_select",None)

		#Centres des couts / comptes analytiques:
		list_centre_cout = request.POST.getlist("centre_cout",None)

		#Traitement de la liste des taxes recues
		list_taxe = dao_taxe.toDesignListTaxe(list_taxe_id, list_count_select)
		#print("liste de taxe",list_taxe)
		#print(len(list_article_id))
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		montant_total_taxe = 0
		montant_total_remise = 0
		#Preparation des ecritures de taxes
		ecritures_taxes = []

		#Traitement
		for i in range(0, len(list_article_id)) :
			article_id = int(list_article_id[i])
			quantite_demandee = makeFloat(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])
			libelle = list_libelle[i]
			compte_id = int(list_compte[i])

			remise = list_remise_id[i]
			if remise == "":
				remise = 0
			else:
				remise = makeFloat(remise)

			centre_cout_id = list_centre_cout[i]
			if centre_cout_id == "" or centre_cout_id == '0':
				centre_cout_id = None
			else:
				centre_cout_id = int(centre_cout_id)

			taxe_tab = list_taxe[i]
			#print("taxe tab", taxe_tab)

			article = dao_article.toGetArticle(article_id)
			symbole_unite = "Elt"
			if article.unite:
				#print("***********************", article.unite)
				symbole_unite = article.unite.symbole_unite



			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			#Application de la remise
			total = total - (total*remise/100)
			total_fact = makeFloat(total_fact) + makeFloat(total)
			#print("compute")
			#Calcul du montant par ligne de la taxe et préparation des ecritures de taxe
			montant_taxe,ecritures_taxes = dao_taxe.toComputeMontantAndEcritureTaxe(taxe_tab,total, ecritures_taxes, centre_cout_id)
			montant_total_taxe += montant_taxe

			#format lignes facture
			ligne = {
				"article_id" : article_id,
				"nom_article" : article.designation,
				"quantite" : quantite_demandee,
				"prix_unitaire" : prix_unitaire,
				"prix_total" : total,
				"symbole_unite" : symbole_unite,
				"montant_taxe": montant_taxe,
				"remise":remise,
				"compte_id": compte_id
			}
			lignes_facture.append(ligne)

			#Affectation du compte comptable de l'article
			compte_article = dao_compte.toGetCompte(compte_id)


			#format ecriture debit
			ecriture = {
				"id" : compte_article.id,
				"libelle" : libelle,
				"compte" : "%s %s" % (compte_article.numero, compte_article.designation),
				"montant" : total,
				"centre_cout_id": centre_cout_id,
			}
			ecritures_credit.append(ecriture)


		#Ajout des ecritures comptables de la taxe à liste des ecritures de debit définis
		ecritures_credit.extend(ecritures_taxes)

		#Agregation des ecritures de même comptes
		ecritures_credit = dao_ecriture_comptable.toAgregateEcritureComptable(ecritures_credit)


		montant = total_fact

		#Traitement sur la TVA
		'''compte_taxe = dao_compte.toGetCompteTaxe()
		ecriture = {
			"id" : compte_taxe.id,
			"libelle" : compte_taxe.designation,
			"compte" : "%s %s" % (compte_taxe.numero, compte_taxe.designation),
			"montant" : montant_total_taxe
		}
		ecritures_debit.append(ecriture)'''


		comptes = dao_compte.toListComptes()
		devise_id = request.POST["devise_id"]
		devise = dao_devise.toGetDevise(devise_id)
		client_id = request.POST["client_id"]
		client = dao_client.toGetClient(client_id)
		condition_reglement_id = request.POST["condition_reglement_id"]
		#print("FIN 0")
		compte_client = dao_compte.toGetCompteClient()
		#print("COMPTE CLI")
		if client.compte != None: compte_client = dao_compte.toGetCompte(client.compte_id)
		#print(compte_client)
		#print("FIN 1")
		#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

		#Format ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
		montant_total = montant + montant_total_taxe

		ecritures_debit = []
		ecriture = {
			"id" : compte_client.id,
			"libelle" : client.nom_complet,
			"compte" : "%s %s" % (compte_client.numero, compte_client.designation),
			"montant" : montant_total
		}
		ecritures_debit.append(ecriture)
		#print("FIN 2")

		#Format Facture

		facture = {
			"date_facturation" : date_facturation,
			"numero_facture" : numero_facture,
			"montant_ht" : montant,
			"montant_taxe_total":montant_total_taxe,
			'montant_total':montant_total,
			"autres_infos":autres_infos,
			'type_service':type_service,
			"order_id" : order_id,
			"condition_reglement_id" : condition_reglement_id
		}
		#print('lignes fini')


		#ON VERIFIE L'ATTACHEMENT DU DOCUMENT
		if 'document_upload' in request.FILES:
			#print("OKKKKKKKKKKKKK")
			file = request.FILES["document_upload"]
			facture_doc_dir = 'documents/facture/client/'
			media_dir = media_dir + '/' + facture_doc_dir
			id = dao_facture_client.toGetNextId()
			#print(id)
			save_path = os.path.join(media_dir, str(id) + '.JPG')
			path = default_storage.save(save_path, file)
			document = Model_Image(doc = media_url + facture_doc_dir + str(id)+'.JPG')
			document.save()

		context = {
			'title' : 'Validation facture',
			'facture' : facture,
			'type_facture' : type_facture,
			'type_facture_client' : type_facture_client,
			'type_service' : type_service,
			'devise' : devise,
			'client' : client,
			'etat_facturation_id' : etat_facturation_id,
			'etat_facturation' : etat_facturation,
			'comptes'   : comptes,
			'bon_achat' : order,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'lignes_facture' : lignes_facture,
			'ecritures_credit': ecritures_credit,
			'ecritures_debit' : ecritures_debit,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/client/validate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_bons_achat"))

@transaction.atomic
def post_creer_facture_client(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		if date_facturation != None and date_facturation != "":
			date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))
		order_id = None #request.POST["order_id"]
		client_id = int(request.POST["client_id"])
		type_facture = int(request.POST["type_facture"])
		dev_id = request.POST["devise_id"]
		etat_facturation_id = request.POST["etat_facturation_id"]
		type_facture_client = request.POST["type_facture_client"]
		if (type_facture_client == "" or type_facture_client == "0"):
			type_facture_client = None

		type_service = request.POST["type_service"]
		autres_infos = request.POST["autres_infos"]

		montant_taxe = request.POST["montant_taxe"]
		condition_reglement_id = request.POST["condition_reglement_id"]
		if condition_reglement_id == 0: condition_reglement_id = None

		#print("condition de ",condition_reglement_id)


		#On recupère le client et le compte client à débiter
		client = dao_client.toGetClient(client_id)
		compte_client = dao_compte.toGetCompteClient()
		#print("compte_client %s" % compte_client)
		if client.compte != None: compte_client = dao_compte.toGetCompte(client.compte_id)
		#print("compte_client recupere")
		#print(compte_client)

		devise_ref = dao_devise.toGetDeviseReference()
		taux_id = None

		lignes = []

		# ECRITURES COMPTABLES DUES AU CONSTAT DE LA VENTE
		date_piece = timezone.now()
		if date_facturation != None and date_facturation != "":
			date_piece = date_facturation
		type_journal = dao_type_journal.toGetTypeVente()
		#print(type_journal)
		journal_vente = dao_journal.toGetJournalDefautOf(type_journal["id"])
		journal_id = None
		if journal_vente != None: journal_id = journal_vente.id
		#print("Journal recuperee")

		#Creation du lettrage referençant la facture
		lettrage = dao_lettrage.toCreateLettrage(dao_lettrage.toGenerateDesignationLettrage(), numero_facture)
		lettrage = dao_lettrage.toSaveLettrage(auteur,lettrage)




		if type_facture == 0:
			order = dao_bon_commande.toGetBonCommande(order_id)
			montant = order.prix_total
			facture = dao_facture_client.toCreateFactureClient(date_facturation, numero_facture, montant, order_id, journal_id,"","", client_id,lettrage.id, condition_reglement_id)
			facture = dao_facture_client.toSaveFactureClient(auteur, facture)


			if devise_ref.id != order.devise_id:
				#print("Les taux sont différents ...")
				taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(order.devise_id)
				if taux != None: taux_id = taux.id

			#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables
			piece_comptable = dao_piece_comptable.toCreatePieceComptable(order.numero_commande, order.reference_document, montant, journal_id, date_piece, client.id, order.id, None , facture.id, "CONSTAT DE VENTE", order.devise_id, taux_id)
			piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
			piece_comptable_id = piece_comptable.id
			#print("piece cree")

			lignes = dao_ligne_reception.toListLigneOfReceptions(order.id)

		elif type_facture == 1:
			#print("FACT 1")
			#print("i,nsidididi")
			montant = 0.0

			facture = dao_facture_client.toCreateFactureClient(date_facturation, numero_facture, 0, None, journal_id,"","", client_id, lettrage.id, condition_reglement_id)
			#print("muisolo 1", facture)
			facture = dao_facture_client.toSaveFactureClient(auteur, facture)

			#print("muisolo")


			#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables

			piece_comptable = dao_piece_comptable.toCreatePieceComptable(facture.numero_facture, None, montant, journal_id, date_piece, client_id, None, None, facture.id, "CONSTAT DE VENTE", dev_id , taux_id)
			piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
			#print("piece cree")
			piece_comptable_id = piece_comptable.id

			lignes = dao_ligne_facture.toListLigneOfFacture(facture.id)
			#print("FACT SAVED")


		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, facture)
		### Fin traitement document

		#Enregistrements des lignes factures
		list_article_id = request.POST.getlist('article_id', None)
		list_quantite_demandee = request.POST.getlist("qte", None)
		list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
		list_montant_taxe = request.POST.getlist("ligne_montant_taxe", None)
		list_remise = request.POST.getlist("remise", None)
		list_compte_id = request.POST.getlist("compte_id", None)
		#print("DEBUT LIGNES")
		#print(len(list_article_id))
		#print(len(list_quantite_demandee))
		#print(len(list_prix_unitaire))
		montant_taxe_total = 0
		for i in range(0, len(list_article_id)) :
			#print("ART ID %s" % list_article_id[i])
			#print("QTE %s" % list_quantite_demandee)
			#print("PRIX %s" % list_prix_unitaire)

			article_id = list_article_id[i]
			montant_taxe = list_montant_taxe[i]
			compte_id = list_compte_id[i]
			montant_taxe_total += makeFloat(montant_taxe)
			quantite_demandee = makeFloat(list_quantite_demandee[i])
			prix_unitaire = makeFloat(list_prix_unitaire[i])
			remise = makeFloat(list_remise[i]) if list_remise[i] != "" else 0

			#print("L1")

			article = dao_article.toGetArticle(article_id)
			symbole_unite = "Elt"
			unite_achat_id = None
			if article.unite:
				unite_achat_id = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id).id
				symbole_unite = article.unite.symbole_unite

			#print("L2")
			prix_unitaire = prix_unitaire
			total = prix_unitaire * quantite_demandee
			total = total - (total * remise / 100)
			montant = makeFloat(montant) + makeFloat(total)

			#print("FACT ID ")
			#print("FACT ID %s" % facture.id)
			#print("ARTICLE %s" % article.id)
			#print("UNITE %s" % unite_achat)


			ligne = dao_ligne_facture.toCreateLigneFacture(article.designation, facture.id, article.id, quantite_demandee, prix_unitaire, unite_achat_id, 0, remise, compte_id)
			ligne = dao_ligne_facture.toSaveLigneFacture(ligne)
			#print("Ligne %s" % ligne)

			#print("L5")
			#On rajoute le stock_article
			#ligne.stock_article_id = stock.id
			ligne.save()

			#print("Fin LIGNES")

		facture.montant_ht = montant
		facture.devise_id = dev_id
		facture.montant_taxe = makeFloat(montant_taxe_total)
		facture.montant = montant + makeFloat(montant_taxe)
		facture.montant_en_lettre = trad.trad(facture.montant)
		facture.etat_facturation_id = etat_facturation_id
		facture.type_facture_id = type_facture_client
		facture.type_service_id = type_service
		facture.autres_infos = autres_infos
		facture.save()

		etat_fact = dao_etat_facturation.toSetUpBilledEtatFacturation(etat_facturation_id)

		#print("FACT UPDATED")
		if devise_ref.id != dev_id:
			#print("Les taux sont différents ...")
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(dev_id)
			if taux != None: taux_id = taux.id

		#Creation ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
		#On cree l'ecriture de crédit
		list_compte_debit_id = request.POST.getlist("compte_debit_id", None)
		list_montant_debit = request.POST.getlist("montant_debit", None)
		list_devise_debit = request.POST.getlist("devise_debit", None)
		list_libelle_debit = request.POST.getlist("libelle_debit", None)

		for i in range(0, len(list_compte_debit_id)):
			compte_debit = list_compte_debit_id[i]
			montant_debit = makeFloat(list_montant_debit[i])
			devise_debit = list_devise_debit[i]
			libelle_debit = list_libelle_debit[i]

			ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(libelle_debit, montant_debit, 0, compte_debit, piece_comptable.id, facture.lettrage_id, facture.date_echeance)
			ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
			ecriture_debit.save()
			#print("ecriture_debit {} cree".format(ecriture_debit.id))

		if facture != None :
			#print("Facture {} creee".format(facture.id))
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					facture.document = doc.doc
					facture.save()
				Model_Image.objects.all().delete()

			#Creation les ecriture débit (dans le constat d'achat, ce sont les comptes des éléments des lignes de facture, ici les articles, qui sont débités)
			list_compte_credit_id = request.POST.getlist("compte_credit_id", None)
			list_montant_credit = request.POST.getlist("montant_credit", None)
			list_devise_credit = request.POST.getlist("devise_credit", None)
			list_libelle_credit = request.POST.getlist("libelle_credit", None)

			list_centre_cout_id = request.POST.getlist("centre_cout_id", None)
			#print("jsuis la", list_centre_cout_id)

			for i in range(0, len(list_compte_credit_id)):
				compte_credit = list_compte_credit_id[i]
				montant_credit = makeFloat(list_montant_credit[i])
				devise_credit = list_devise_credit[i]
				libelle_credit = list_libelle_credit[i]
				centre_cout_id = list_centre_cout_id[i]

				ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(libelle_credit, 0, montant_credit, compte_credit, piece_comptable_id, facture.lettrage_id)
				ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
				ecriture_credit.save()
				#print("ecriture_credit {} cree".format(ecriture_credit.id))
				#Ecritures pour analytique
				if (centre_cout_id != "") and (centre_cout_id != "0") and (centre_cout_id != None) and (centre_cout_id != "None"):
					ecriture_analytique = dao_ecriture_analytique.toCreateEcriture_analytique(libelle_credit,compte_credit,centre_cout_id,facture.id,montant_credit,dev_id,2,ecriture_credit.id)
					ecriture_analytique = dao_ecriture_analytique.toSaveEcriture_analytique(auteur,ecriture_analytique)




			# WORKFLOWS INITIALS
			#print("Debut workflow")
			type_document = "Facture client"
			wkf_task.initializeWorkflow(auteur,facture,type_document)

			#TODO Créer les lignes de facture
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_client', args=(facture.id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la facture")
			return HttpResponseRedirect(reverse('module_comptabilite_list_factures_client'))
	except Exception as e:
		#print("ERREUR POST CREER FACTURE CLIENT!")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_client'))

def get_modifier_facture_client(request, ref):
	# droit="MODIFIER_FACTURE_FOURNISSEUR"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 108
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response


	try:
		id = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)

		title = "la facture"
		if facture.numero_facture != None and facture.numero_facture != "" : title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"

		context = {
			'title' : 'Modifier %s' % title,
			'model' : facture,
			'menu' : 21,
			'lignes' : lignes,
			'bon'   : bon_reception,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/fournisseur/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

def post_modifier_facture_client(request):
	id = int(request.POST["ref"])
	try:
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))

		facture = dao_facture_fournisseur.toGetFactureFournisseur(id)
		facture.numero_facture = numero_facture
		facture.date_facturation = date_facturation
		is_done = dao_facture_fournisseur.toUpdateFactureFournisseur(facture.id,facture)

		if is_done != False :
			messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture', args=(facture.id,)))
		else :
			messages.add_message(request, messages.ERROR,"Une erreur est survenue lors de l'opération")
			return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(facture.id,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(id,)))

def get_details_facture_client(request, ref):
	try:
		# droit="LISTER_FACTURE_CLIENT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 110
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		montant_paye = facture.montant_paye
		montant_restant = facture.montant_restant

		title = "Facture"
		if facture.numero_facture != None and facture.numero_facture != "" :
			title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"

		if bon_reception != None :
			type_facture = "Bon"
			lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)
		else :
			type_facture = "Ligne"
			lignes = dao_ligne_facture.toListLigneOfFacture(ref)

		paiements = dao_paiement.toListPaiementOfFacture(facture.id)
		is_solded = dao_paiement.toCheckPaiementSoldeOfFacture(facture.id, facture.montant)

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,facture)

		# #print("historique",historique)
		# #print("transition_etape_suivant",transition_etape_suivant)
		# #print("roles", roles)

		context = {
			'title' : title,
			'model' : facture,
			'type_facture' : type_facture,
			'paiements':paiements,
			'is_solded':is_solded,
			'bon'   : bon_reception,
			'historique' : historique,
			'actions':auth.toGetActions(modules,utilisateur),
			'etapes_suivantes' : transition_etape_suivant,
			'content_type_id':content_type_id,
			'documents':documents,
			'lignes' : lignes,
			'roles':groupe_permissions,
			'menu' : 21,
			"utilisateur" : utilisateur,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'montant_paye' : montant_paye,
			'montant_restant' : montant_restant
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/client/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_client'))

@transaction.atomic
def post_workflow_facture_client(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		facture_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, facture_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		facture = dao_facture.toGetFacture(facture_id)

		#print("print 2 %s %s %s " % (employe, etape, facture))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(facture.statut_id)
		for item in transitions_etapes_suivantes:

			if item.condition.designation == "Upload":

				#print("Upload")
				if 'file_upload' in request.FILES:
					nom_fichier = request.FILES['file_upload']
					doc=dao_document.toUploadDocument(auteur, nom_fichier, facture)

					#On affecte le chemin de l'Image

					facture.statut_id = etape.id
					facture.etat = etape.designation
					facture.save()

					document = dao_document_facture.toCreateDocument("Facture",doc.url_document, facture.etat,facture_id)
					document = dao_document_facture.toSaveDocument(auteur, document)

					#print("docu saved")

			else:

				#print("Autres")
				# Gestion des transitions dans le document
				facture.statut_id = etape.id
				facture.etat = etape.designation
				facture.save()

		historique = dao_wkf_historique_facture.toCreateHistoriqueWorkflow(employe.id, etape.id, facture.id)
		historique = dao_wkf_historique_facture.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_client', args=(facture_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_client', args=(facture_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_facture_client Methode:"post_workflow_facture_client"'))

def get_print_facture_client(request):
	try:
		modules, utilisateur, response = auth.toGetAuth(request)
		if response != None:
			return response

		id = request.POST["id"]
		#print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK " + str(id))

		end = endpoint.reportingEndPoint()

		context = {
			'title' : 'Liste des états de besoin',
			'id' : id,
			'endpoint' : end,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleComptabilite/facture/client/print.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE DES DEMANDES ACHAT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_tableau_de_bord'))

def get_imprimer_facture_client(request):
	try:
		# droit="IMPRIMER_FACTURE_CLIENT"
		permission_number = 110
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
		#print("ref", ref)


		if response != None:
			return response

		facture = dao_facture_fournisseur.toGetFactureFournisseur(ref)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		montant_paye = facture.montant_paye
		montant_restant = facture.montant_restant

		title = "Facture"
		if facture.numero_facture != None and facture.numero_facture != "" :
			title = title + " N°%s" % facture.numero_facture
		else: title = title + " sans numéro"

		if bon_reception != None :
			type_facture = "Bon"
			lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)
		else :
			type_facture = "Ligne"
			lignes = dao_ligne_facture.toListLigneOfFacture(ref)

		paiements = dao_paiement.toListPaiementOfFacture(facture.id)
		is_solded = dao_paiement.toCheckPaiementSoldeOfFacture(facture.id, facture.montant)

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,facture)

		#print("historique",historique)
		#print("transition_etape_suivant",transition_etape_suivant)
		#print("roles", roles)

		context = {
			'title' : title,
			'model' : facture,
			'type_facture' : type_facture,
			'paiements':paiements,
			'is_solded':is_solded,
			'bon'   : bon_reception,
			'historique' : historique,
			'actions':auth.toGetActions(modules,utilisateur),
			'etapes_suivantes' : transition_etape_suivant,
			'content_type_id':content_type_id,
			'documents':documents,
			'lignes' : lignes,
			"utilisateur" : utilisateur,
			'montant_paye' : montant_paye,
			'montant_restant' : montant_restant,
			'modules' : modules,
			'sous_modules': sous_modules,
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/facture_client.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'facture_client.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('facture_client.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response

		return response
	except Exception as e:
		#print("ERREUR print FACTURE CLIENT")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_client'))

def get_json_type_fact_client(request):
	try:
		data = []
		etat_facturation_id = request.GET["ref"]
		#print("etat_facturation_id", etat_facturation_id)

		types = dao_facture.toListTypeFactClientNotCreated(etat_facturation_id)

		for type in types:
			item = {"designation": type}
			data.append(item)

		#print(data)
		return JsonResponse(data, safe=False)

	except Exception as e:
		return JsonResponse([], safe=False)



@transaction.atomic
def post_workflow_facture_fournisseur(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		facture_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, facture_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		facture = dao_facture.toGetFacture(facture_id)

		#print("print 2 %s %s %s " % (employe, etape, facture))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(facture.statut_id)
		for item in transitions_etapes_suivantes:

			if item.condition.designation == "Upload":

				#print("Upload")
				if 'file_upload' in request.FILES:
					nom_fichier = request.FILES['file_upload']
					doc=dao_document.toUploadDocument(auteur, nom_fichier, facture)

					#On affecte le chemin de l'Image

					facture.statut_id = etape.id
					facture.etat = etape.designation
					facture.save()

					document = dao_document_facture.toCreateDocument("Facture",doc.url_document, facture.etat,facture_id)
					document = dao_document_facture.toSaveDocument(auteur, document)

					#print("docu saved")

			else:

				#print("Autres")
				# Gestion des transitions dans le document
				facture.statut_id = etape.id
				facture.etat = etape.designation
				facture.save()

		historique = dao_wkf_historique_facture.toCreateHistoriqueWorkflow(employe.id, etape.id, facture.id)
		historique = dao_wkf_historique_facture.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_fournisseur', args=(facture_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_fournisseur', args=(facture_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_facture_fournisseur'))


# PAIEMENT FACTURE CLIENT CONTROLLER

def get_lister_paiements_client(request):
	try:
		# droit="LISTER_PAIEMENT_CLIENT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 301
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_paiement.toListPaiementsClient()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_paiement.toListPaiementsClient(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		types_paiement = dao_type_paiement.toListTypePaiement()
		context = {
			'title' : 'Liste des paiements client',
			'model' : model,
			"utilisateur" : utilisateur,
			"types_paiement" : types_paiement,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 29,
			'modules' : modules,
			'sous_modules': sous_modules,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/client/list.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_tableau_de_bord'))

def get_creer_paiement_client(request):
	try:
		# droit="CREER_PAIEMENT_CLIENT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 302
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		moyen_paiement = dao_moyen_paiement.toListMoyenPaiement()
		types_paiement = dao_type_paiement.toListTypePaiement()
		clients = dao_client.toListClientsActifs()
		journaux = dao_journal.toListJournauxPaie()

		context = {
			'title' : "Nouveau paiement client",
			'devises' : devises,
			'devise_ref' : devise_ref,
			'menu': 29,
			'moyen_paiement' : moyen_paiement,
			'types_paiement' : types_paiement,
			'journaux' : journaux,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'clients' : clients,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/client/add.html")
		return HttpResponse(template.render(context,request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_client'))

def get_creer_paiement_facture_client(request, ref):
	try:
		permission_number = 302
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		id = int(ref)
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		facture = dao_facture_client.toGetFactureClient(id)
		journaux = dao_journal.toListJournauxPaie()
		moyen_paiement = dao_moyen_paiement.toListMoyenPaiement()
		types_paiement = dao_type_paiement.toListTypePaiement()

		operations = dao_operationtresorerie.toListOperationtresorerieNonCloture()


		context = {
			'title' : "Nouveau réglement de facture",
			'operations':operations,
			'devises' : devises,
			'devise_ref' : devise_ref,
			'menu' : 29,
			'facture' : facture,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'journaux' : journaux,
			'moyen_paiement' : moyen_paiement,
			'types_paiement' : types_paiement,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/client/facture/add.html")
		return HttpResponse(template.render(context,request))
	except Exception as e:
		#print("ERREUR !")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_client'))

@transaction.atomic
def post_creer_paiement_client(request):
	sid = transaction.savepoint()
	ref = int(request.POST["ref"])
	try:
		devise_ref = dao_devise.toGetDeviseReference()
		auteur = identite.utilisateur(request)
		date_paiement = request.POST["date_paiement"]
		date_paiement = timezone.datetime(int(date_paiement[6:10]), int(date_paiement[3:5]), int(date_paiement[0:2]))

		montant = makeFloat(request.POST["montant"])
		designation = str(request.POST["designation"])
		description = str(request.POST["description"])
		type_paiement = int(request.POST["type_paiement"])
		#journal_id = int(request.POST["journal_id"])
		operation_tresorerie_id = int(request.POST["operation_tresorerie_id"])
		devise_id = int(request.POST["devise_id"])
		partenaire_id = int(request.POST["partenaire_id"])
		#print("MANDEKE")
		#print("PARTE %s" % partenaire_id)

		operation_tresorerie = dao_operationtresorerie.toGetOperationtresorerie(operation_tresorerie_id)
		journal_id = operation_tresorerie.journal_id

		devise = dao_devise.toGetDevise(devise_id)
		journal = dao_journal.toGetJournal(journal_id)
		client = dao_client.toGetClient(partenaire_id)
		transaction_paiement_id = None
		facture_id = None
		taux_id = None
		lettrage_id = None

		#print("Avant fac")
		if ref != 0:
			#print("Dans fac")
			facture = dao_facture_client.toGetFactureClient(ref)
			facture_id = facture.id
			montant_facture = facture.montant_restant
			lettrage_id = facture.lettrage_id

			if devise.id == facture.devise_id:
				if makeFloat(montant_facture) == makeFloat(montant) :
					facture.est_soldee = True
					dao_facture_client.toUpdateFactureClient(facture.id, facture)
				elif makeFloat(montant_facture) < makeFloat(montant):
					messages.error(request,'Le montant saisi est supérieur au montant attendu : ' + str(montant_facture) + ' ' + devise.symbole_devise)
					return HttpResponseRedirect(reverse("module_comptabilite_add_paiement_facture_client", args=(ref,)))
		#print("Apres fac")

		statut_transaction = dao_statut_transaction.toGetStatutSuccess()
		transaction_paiement = dao_transaction.toCreateTransaction(facture_id, statut_transaction["id"], 1)
		transaction_paiement = dao_transaction.toSaveTransaction(auteur, transaction_paiement)
		transaction_paiement_id = transaction_paiement.id
		#print("Trans cree")
		#On définit le taux
		if devise.id != devise_ref.id:
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)
			if taux != None: taux_id = taux.id
			#print("Taux recupere")

		#print("CLIENT %s" % client.id)
		# On enregistre le paiement
		paiement = dao_paiement.toCreatePaiement(transaction_paiement_id, date_paiement, facture_id, devise.id, montant, type_paiement, journal.id , client.id , auteur.id, designation, description, True)
		paiement = dao_paiement.toSavePaiement(paiement)
		#paiement.type = "Paiement client"

		#print("Paiement cree")

		#On enregistre le payloads (Informations supplémentaires et utile pour le paiement)
		logs = "{'journal':'%s', 'montant':'%s', 'devise':'%s' }" % (journal.designation, montant, devise.designation)
		payloads = dao_payloads.toCreatePayloads(paiement.id, logs)
		dao_payloads.toSavePayloads(payloads)
		#print("Payload cree")

		#print("Fin fac")

		# WORKFLOWS INITIALS
		#print("Debut workflow")
		type_document = "Paiement client"
		#Initialisation du workflow avis appel offre
		wkf_task.initializeWorkflow(auteur,paiement,type_document)

		## On crée la reference au ligne de paiement
		type_operation = 1 #Retrait
		ligne_operation = dao_ligne_operation_tresorerie.toCreateLigne_operation_tresorerie(designation,"Paiement facture"+facture.numero_facture,partenaire_id,montant,devise_id,taux_id,type_operation, description,operation_tresorerie.id,date_paiement)
		ligne_operation = dao_ligne_operation_tresorerie.toSaveLigne_operation_tresorerie(auteur,ligne_operation)
		ligne_operation.est_lettre = True
		ligne_operation.paiement_id = paiement.id
		ligne_operation.save()

		#Enregistrement du lien entre paiement et operation tresorerie
		paiement.ligne_operation_tresorerie_id = ligne_operation.id
		paiement.save()



		transaction.savepoint_commit(sid)
		if ref != 0:
			return HttpResponseRedirect(reverse('module_comptabilite_details_paiement_client', args=(paiement.id,)))
		else : return HttpResponseRedirect(reverse('module_comptabilite_details_facture_client', args=(facture_id,)))
	except Exception as e:
		#print("ERREUR POST")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		if ref != 0:
			return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_facture_client', args=(facture_id,)))
		else : return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_client'))

def post_valider_paiement_client(request):
	sid = transaction.savepoint()
	ref = int(request.POST["doc_id"])
	try:
		auteur = identite.utilisateur(request)
		paiement = dao_paiement.toGetPaiement(ref)
		journal = dao_journal.toGetJournal(paiement.journal_id)
		client = dao_client.toGetClient(paiement.partenaire_id)

		#print("Fin des gets")

		# ECRITURES COMPTABLES DUES AU PAIEMENT DU CLIENT
		#Ici On débite le compte de trésorerie
		date_piece = timezone.now()
		compte_tresorerie = journal.compte_debit

		#print("fin date piece")

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(paiement.designation, "", paiement.montant, journal.id, date_piece, paiement.partenaire_id, None, None, paiement.facture_id, "PAIEMENT CLIENT", paiement.devise_id, paiement.taux_id)
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)

		#print("piece prise")
		ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, paiement.montant, 0, compte_tresorerie.id, piece_comptable.id, paiement.facture.lettrage_id)
		ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)

		#print("fin debit")

		#On crédite le compte du client
		compte_client = dao_compte.toGetCompteClient()
		if client.compte != None: compte_client = dao_compte.toGetCompte(client.compte_id)

		#print("fin compte client")
		ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(client.nom_complet, 0, paiement.montant, compte_client.id, piece_comptable.id, paiement.facture.lettrage_id)
		ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
		#print("Fin fac")
		paiement.est_valide = True
		paiement.save()

		############################ WORKFLOW #############################
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		paiement_id = request.POST["doc_id"]

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		paiement = dao_paiement.toGetPaiement(paiement_id)

		#Passage de transition
		wkf_task.passingStepWorkflow(employe,paiement,etape.id)

		transaction.savepoint_commit(sid)
		if ref != 0:
			return HttpResponseRedirect(reverse('module_comptabilite_details_facture_client', args=(paiement.facture_id,)))
		else : return HttpResponseRedirect(reverse('module_comptabilite_details_paiement_client', args=(paiement.id,)))
	except Exception as e:
		#print("ERREUR POST")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		if ref != 0:
			return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_facture_client', args=(ref,)))
		else : return HttpResponseRedirect(reverse('module_comptabilite_add_paiement_client'))

def get_details_paiement_client(request, ref):
	try:
		# droit="LISTER_PAIEMENT_CLIENT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 301
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		paiement = dao_paiement.toGetPaiement(ref)
		moyens_paiement = dao_moyen_paiement.toListMoyenPaiement()
		types_paiement = dao_type_paiement.toListTypePaiement()

		#print("Paiement %s" % paiement)

		title = "Paiement"
		if paiement.designation != None and paiement.designation != "" :
			title = title + " %s" % paiement.designation

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,paiement)

		context = {
			'title' : title,
			'model' : paiement,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'content_type_id':content_type_id,
			'documents':documents,
			'roles':groupe_permissions,
			'moyens_paiement' : moyens_paiement,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'types_paiement' : types_paiement,
			'menu' : 29,
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/paiement/client/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_client'))

@transaction.atomic
def post_workflow_paiement_client(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		paiement_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, paiement_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		paiement = dao_paiement.toGetPaiement(paiement_id)

		#print("print 2 %s %s %s " % (employe, etape, paiement))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(paiement.statut_id)
		for item in transitions_etapes_suivantes:

			if item.condition.designation == "Upload":

				#print("Upload")
				if 'file_upload' in request.FILES:
					nom_fichier = request.FILES['file_upload']
					doc=dao_document.toUploadDocument(auteur, nom_fichier, paiement)

					#On affecte le chemin de l'Image

					paiement.statut_id = etape.id
					paiement.etat = etape.designation
					paiement.save()

					document = dao_document_paiement.toCreateDocument("Paiement",doc.url_document, paiement.etat,paiement_id)
					document = dao_document_paiement.toSaveDocument(auteur, document)

					#print("docu saved")

			else:

				#print("Autres")
				# Gestion des transitions dans le document
				paiement.statut_id = etape.id
				paiement.etat = etape.designation
				paiement.save()

		historique = dao_wkf_historique_paiement.toCreateHistoriqueWorkflow(employe.id, etape.id, paiement.id)
		historique = dao_wkf_historique_paiement.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_comptabilite_details_paiement_client', args=(paiement_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_comptabilite_details_paiement_client', args=(paiement_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_paiements_client'))

# RECEPTION FACTURE CONTROLLER
def get_lister_bons_achat(request):

	# droit="LISTER_RECEPTION_FACTURE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 111
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	# model = dao_bon_reception.toListFournituresFacturables()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_bon_reception.toListFournituresFacturables(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)
	context = {
		'title' : "Reception facture",
		'model' : model,
		"utilisateur" : utilisateur,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 23,
		'modules' : modules,
		'sous_modules': sous_modules,
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/bons/list.html")
	return HttpResponse(template.render(context, request))

def get_details_bon_achat(request, ref):
	try:
		# droit="LISTER_RECEPTION_FACTURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 111
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		bon_reception = dao_bon_reception.toGetBonReception(ref)
		lignes = dao_ligne_reception.toListLigneOfReceptions(bon_reception.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_reception)


		context = {
			'title' : "Bon de commande N°%s" % bon_reception.numero_reception,
			'model' : bon_reception,
			'lignes' : lignes,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 23,
			'modules' : modules,
			'sous_modules': sous_modules,
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/bons/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_bons_achat'))

def get_creer_facture_bon_achat(request, ref):
	pass


# IMMOBILISATIONS CONTROLLER
def get_lister_immobilisations(request):
	# droit="LISTER_IMMOBILISATION"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 460
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	# model = dao_immobilisation.toList()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_immobilisation.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : "Liste des immobilisations",
		'model' : model,
		'devise_ref' : dao_devise.toGetDeviseReference(),
		"utilisateur" : utilisateur,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 25,
		'modules' : modules,
		'sous_modules': sous_modules,
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/list.html")
	return HttpResponse(template.render(context, request))



def get_creer_immobilisation(request):
	# droit="CREER_IMMOBILISATION"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 461
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	asset = None
	if 'ref' in request.GET:
		ref = request.GET["ref"]
		#print("ref", ref)
		asset = dao_asset.toGetAsset(ref)
		#print("asset done", asset)
		if asset.est_immobilise :
			messages.add_message(request, messages.ERROR, "L'élément est déjà immobilisé")
			return HttpResponseRedirect(reverse('module_comptabilite_add_immobilisation'))


	assets = dao_asset.toListAssetNonImmobilise()
	#print("liste assets", assets)
	comptes = dao_compte.toListComptes()


	context = {
		'title' : 'Nouvelle immobilisation',
		'immobiliers' : assets,
		'asset':asset,
		'devise_ref' : dao_devise.toGetDeviseReference(),
		"utilisateur" : utilisateur,
		'comptes':comptes,
		'locaux':dao_local.toListLocal(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 25,
		'modules' : modules,
		'sous_modules': sous_modules,
		'numeroref': dao_immobilisation.toGenerateNumeroImmo(),
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/add.html")
	return HttpResponse(template.render(context, request))


def get_creer_tableau_immobilisation(request):
	permission_number = 463
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	#print("immo", dao_immobilisation.toListImmobilisationAvailableAndComptabilise())

	context = {
		'title' : 'Tableau d\'immobilisation',
		"immobilisations": dao_immobilisation.toListImmobilisationAvailableAndComptabilise(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 25
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/tableau.html")
	return HttpResponse(template.render(context, request))



@transaction.atomic
def post_creer_immobilisation(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		code = request.POST["code"]
		immobilier_id = int(request.POST["immobilier_id"])
		valeur_immobilier = makeFloat(request.POST["valeur_acquisition"])
		date_acquisition = request.POST["date_acquisition"]
		date_acquisition = timezone.datetime(int(date_acquisition[6:10]), int(date_acquisition[3:5]), int(date_acquisition[0:2]))
		duree_amortissement	= int(request.POST["duree_amortissement"])
		taux_amortissement = 100 / duree_amortissement

		compte_dotation_id	= int(request.POST["compte_dotation"])
		compte_depreciation_id	= int(request.POST["compte_depreciation"])
		compte_immobilier_id	= int(request.POST["compte_immobilier"])
		type_amortissement	= int(request.POST["type_amortissement"])
		local_id = int(request.POST["local_id"])
		if local_id == 0:
			local_id = None
		coefficient = 0.0
		#print("dadju")

		#Si type = degressif, gestion d
		if type_amortissement == 2:
			if duree_amortissement < 3:
				transaction.savepoint_rollback(sid)
				messages.add_message(request, messages.ERROR, "Pour le type d'amortissement dégressif, la durée de vie doit être au minimum de 3 ans")
				return HttpResponseRedirect(reverse('module_comptabilite_add_immobilisation'))
			elif duree_amortissement == 3 or duree_amortissement == 4 :
				coefficient = 1.25
			elif duree_amortissement == 5 or duree_amortissement == 6:
				coefficient = 1.75
			else:
				coefficient = 2.25
			taux_amortissement = 100 * coefficient / duree_amortissement




		#print("dadju 2")
		#enregitrement de l'asset en tant qu'immobilier immobilisé
		immobilier = dao_asset.toGetAsset(immobilier_id)
		immobilier.est_immobilise = True
		immobilier.save()
		#Enregistrement de l'immobilisation
		immobilisation = dao_immobilisation.toCreate(code, immobilier.id, date_acquisition, taux_amortissement, valeur_immobilier, duree_amortissement,coefficient,type_amortissement,compte_dotation_id, compte_depreciation_id, compte_immobilier_id,local_id)
		immobilisation = dao_immobilisation.toSave(auteur, immobilisation)


		#print("dadju 3")
		if immobilisation == None:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
			return HttpResponseRedirect(reverse('module_comptabilite_add_immobilisation'))


		#print("dadju 4")
		#Initialisation wkflow
		wkf_task.initializeWorkflow(auteur,immobilisation)

		#print("dadju 5")
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_details_immobilisation", args=(immobilisation.id,)))
	except Exception as e:
		# print("ERREUR !")
		# print(e)
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_immobilisation'))

def get_modifier_immobilisation(request, ref):
	# droit="MODIFIER_IMMOBILISATION"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 462
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		id = int(ref)
		immobilisation = dao_immobilisation.toGet(id)

		context = {
			'title' : "Modifier l'immobilisation %s" % immobilisation.code,
			'model' : immobilisation,
			'immobiliers' : dao_asset.toListAsset(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_immobilisations'))

def post_modifier_immobilisation(request):
	id = int(request.POST["ref"])

	try:
		auteur = identite.utilisateur(request)
		code = request.POST["code"]
		immobilier_id = int(request.POST["immobilier_id"])
		valeur_immobilier = makeFloat(request.POST["valeur_acquisition"])
		date_acquisition = request.POST["date_acquisition"]
		date_acquisition = timezone.datetime(int(date_acquisition[6:10]), int(date_acquisition[3:5]), int(date_acquisition[0:2]))
		duree_amortissement	= int(request.POST["duree_amortissement"])
		taux_amortissement = 100 / duree_amortissement

		immobilier = dao_asset.toGetAsset(immobilier_id)
		immobilisation = dao_immobilisation.toCreate(code, immobilier.id, date_acquisition, taux_amortissement, valeur_immobilier,duree_amortissement)
		is_done = dao_immobilisation.toUpdate(id, immobilisation)
		if is_done == True:
			messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
			return HttpResponseRedirect(reverse("module_comptabilite_details_immobilisation", args=(id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
			return HttpResponseRedirect(reverse("module_comptabilite_update_immobilisation", args=(id,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_immobilisation', args=(id,)))

def get_details_immobilisation(request, ref):
	try:
		# droit="LISTER_IMMOBILISATION"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 460
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		immobilisation = dao_immobilisation.toGet(ref)
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,immobilisation)
		#print("trans", transition_etape_suivant)

		lignes_amortissements = dao_immobilisation.toListLigneAmortissement(immobilisation.id)
		context = {
			'title' : "Immobilisation %s" % immobilisation.code,
			'model' : immobilisation,
			'immobilier' : dao_asset.toGetAsset(immobilisation.immobilier_id),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'historique':historique,
			'roles':groupe_permissions,
			'lignes_amortissements':lignes_amortissements,
			'etapes_suivantes':transition_etape_suivant,
			'content_type_id':content_type_id,
			'documents':documents,
			"organisation":dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_immobilisations'))




def get_lister_article(request):

	try:
		permission_number = 469
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response
		# model = dao_article.toListArticlesNonService()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_article.toListArticlesNonService(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		#Traitement des vues
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)


		context = {
			'title' : "Liste des articles achetables",
			'model' : model,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'view': view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/article/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilité'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE COMPTABILITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut List Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_article'))

def get_details_article(request, ref):

	try:
		# droit = "LISTER_ARTICLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 7
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		article = dao_article.toGetArticle(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,article)

		context = {
			'title' : article.designation,
			'model' : article,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/article/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detail Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_article'))


def get_modifier_article(request, ref):

	try:
		# droit = "LISTER_ARTICLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 7
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		id = int(ref)

		if response != None:
			return response

		article = dao_article.toGetArticle(id)
		context = {
			'title' : 'Assigner un compte comptable',
			'model' : article,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/article/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Modifier Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_article'))

@transaction.atomic
def post_modifier_article(request):
	sid = transaction.savepoint()

	try:
		if "ref" in request.POST:
			id = int(request.POST["ref"])
		else:
			id = int(request.GET["ref"])
		auteur = identite.utilisateur(request)
		compte_id = None
		if "compte_id" in request.POST:
			compte_id = request.POST["compte_id"]


		is_done = dao_article.toUpdateCompteofArticle(id, compte_id)

		if is_done == True :
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
			return HttpResponseRedirect(reverse("module_comptabilite_detail_article", args=(id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR,"Une erreur est survenue lors de l'opération !")
			return HttpResponseRedirect(reverse("module_comptabilite_update_article", args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilité'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFICATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier Article')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_article'))


# FOURNISSEUR CONTROLLER
def get_lister_fournisseurs(request):

	try:
		permission_number = 475
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		# model = dao_fournisseur.toListFournisseurs()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_fournisseur.toListFournisseurs(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		#Traitement des vues
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)


		context = {
			'title' : 'Liste des fournisseurs',
			'model' : model,
			'view': view,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/fournisseur/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DE LA LISTE FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Liste Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_fournisseur'))

def get_details_fournisseur(request, ref):
	try:
		# droit = "LISTER_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 475
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		fournisseur = dao_fournisseur.toGetFournisseur(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,fournisseur)

		context = {
			'title' : fournisseur.nom_complet,
			'model' : fournisseur,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/fournisseur/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS POST DU DETAIL FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detail Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_fournisseur'))


def get_modifier_fournisseur(request, ref):

	try:
		#print("LOZEA")
		# droit = "LISTER_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 475
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		id = int(ref)

		if response != None:
			return response

		fournisseur = dao_fournisseur.toGetFournisseur(id)
		comptes = dao_compte.toListComptes()
		context = {
			'title' : 'Assigner un compte comptable',
			'model' : fournisseur,
			"utilisateur" : utilisateur,
			'comptes': comptes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/fournisseur/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION fournisseur\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Modifier fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_fournisseur'))

@transaction.atomic
def post_modifier_fournisseur(request):
	sid = transaction.savepoint()
	try:
		if "ref" in request.POST:
			id = int(request.POST["ref"])
		else:
			id = int(request.GET["ref"])
		auteur = identite.utilisateur(request)
		compte_id = None
		if "compte_id" in request.POST:
			compte_id = request.POST["compte_id"]

		#print("wel inside")

		is_done = dao_fournisseur.toUpdateCompteofFournisseur(id, compte_id)


		if is_done == True :
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
			return HttpResponseRedirect(reverse("module_comptabilite_detail_fournisseur", args=(id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR,"Une erreur est survenue lors de l'opération")
			return HttpResponseRedirect(reverse("module_comptabilite_update_fournisseur", args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilité'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFICATION fournisseur\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier fournisseur')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_fournisseur'))


def get_lister_taxe(request):
	# droit = "LISTER_TAXE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 251
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	# model = dao_taxe.toListTaxe()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_taxe.toListTaxe(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des taxes',
		'model' : model,
		'utilisateur' : utilisateur,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/taxe/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_taxe(request):
	# droit = "CREER_TAXE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 250
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	devises = dao_devise.toListDevises()
	comptes = dao_compte.toListComptes()
	context ={'title' : 'Ajouter une taxe',
	'devises':devises,
	'comptes':comptes,
	'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	"modules" : modules,
	'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/taxe/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_taxe(request):

	try:
		designation = request.POST['designation']
		categorie_taxe = request.POST['categorie_taxe']
		portee_taxe = request.POST['portee_taxe']
		type_montant_taxe = request.POST['type_montant_taxe']
		montant = request.POST['montant']
		compte_taxe_id = request.POST['compte_taxe_id']
		description = request.POST['description']
		devise_id = request.POST['devise_id']
		if devise_id == "":
			devise_id = None
		if compte_taxe_id == "":
			compte_taxe_id = None

		est_active = False
		if "est_active" in request.POST : est_active = True

		auteur = identite.utilisateur(request)

		taxe=dao_taxe.toCreateTaxe(designation,categorie_taxe,portee_taxe,type_montant_taxe,montant,compte_taxe_id,est_active,description,devise_id)
		taxe=dao_taxe.toSaveTaxe(auteur, taxe)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_taxe', args=(taxe.id),))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TAXE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_taxe'))


def get_details_taxe(request,ref):
	# droit = "LISTER_TAXE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 251
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		taxe=dao_taxe.toGetTaxe(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/taxe/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,taxe)

		context ={
		'title' : 'Details sur taxe',
		'taxe' : taxe,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'utilisateur' : utilisateur,"modules" : modules,
		'sous_modules': sous_modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TAXE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_taxe'))
def get_modifier_taxe(request,ref):
	# droit = "MODIFIER_TAXE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 252
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ref = int(ref)
	model = dao_taxe.toGetTaxe(ref)
	comptes = dao_compte.toListComptes()
	devises = dao_devise.toListDevises()
	context ={'title' : 'Modifier une taxe','model':model,
	'comptes':comptes,
	'devises':devises,
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/taxe/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_taxe(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		categorie_taxe = request.POST['categorie_taxe']
		portee_taxe = request.POST['portee_taxe']
		type_montant_taxe = request.POST['type_montant_taxe']
		montant = request.POST['montant']
		compte_taxe_id = request.POST['compte_taxe_id']
		description = request.POST['description']
		devise_id = request.POST['devise_id']
		if devise_id == "":
			devise_id = None

		auteur = identite.utilisateur(request)

		est_active = False
		if "est_active" in request.POST : est_active = True

		taxe=dao_taxe.toCreateTaxe(designation,categorie_taxe,portee_taxe,type_montant_taxe,montant,compte_taxe_id,est_active,description, devise_id)
		taxe=dao_taxe.toUpdateTaxe(id, taxe)
		messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_taxe', args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER TAXE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_taxe', args=(id,)))


def get_lister_annee_fiscale(request):
	# droit='LISTER_ANNEE_FISCALE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 255
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	# model = dao_annee_fiscale.toListAnnee_fiscale()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_annee_fiscale.toListAnnee_fiscale(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des années fiscales',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : model,
		'view': view,
		'utilisateur' : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/annee_fiscale/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_annee_fiscale(request):
	# droit='CREER_ANNEE_FISCALE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 254
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
			return response

	context ={'title' : 'Ajouter une année fiscale',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/annee_fiscale/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_annee_fiscale(request):

	try:
		designation = request.POST['designation']
		observation = request.POST['observation']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		est_active = False
		if "est_active" in request.POST : est_active = True

		auteur = identite.utilisateur(request)

		annee_fiscale=dao_annee_fiscale.toCreateAnnee_fiscale(designation,observation,date_debut,date_fin,est_active)
		annee_fiscale=dao_annee_fiscale.toSaveAnnee_fiscale(auteur, annee_fiscale)
		id =int(annee_fiscale.id)
		# print('Annee Crée', id)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_annee_fiscale',args=(id,)))
	except Exception as e:
		# print('Erreur lors de l enregistrement')
		# print(e)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER ANNEE_FISCALE \n {}'.format(auteur.nom_complet, module,e))
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_annee_fiscale'))


def get_details_annee_fiscale(request,ref):
	# droit='LISTER_ANNEE_FISCALE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 255
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
			return response
	try:
		ref=int(ref)
		annee_fiscale=dao_annee_fiscale.toGetAnnee_fiscale(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/annee_fiscale/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,annee_fiscale)

		context ={'title' : 'Details sur une année fiscale',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'annee_fiscale' : annee_fiscale,'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS ANNEE_FISCALE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_annee_fiscale'))

def get_modifier_annee_fiscale(request,ref):
	# droit='MODIFIER_ANNEE_FISCALE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 256
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_annee_fiscale.toGetAnnee_fiscale(ref)
	context ={'title' : 'Modifier une année fiscale','model':model,
	'actions':auth.toGetActions(modules,utilisateur),'sous_modules': sous_modules,'modules' : modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/annee_fiscale/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_annee_fiscale(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		observation = request.POST['observation']
		date_debut = request.POST['date_debut']
		date_fin = request.POST['date_fin']
		est_active = False
		if "est_active" in request.POST : est_active = True
		auteur = identite.utilisateur(request)

		annee_fiscale=dao_annee_fiscale.toCreateAnnee_fiscale(designation,observation,date_debut,date_fin,est_active)
		annee_fiscale=dao_annee_fiscale.toUpdateAnnee_fiscale(id, annee_fiscale)
		messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_annee_fiscale',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER ANNEE_FISCALE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_annee_fiscale'))


def get_lister_local(request):
	# droit='LISTER_LOCAL'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 258
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	# model = dao_local.toListLocal()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_local.toListLocal(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des locaux',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : model,
		'view': view,
		'utilisateur' : utilisateur,
		'sous_modules': sous_modules,'modules' : modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/local/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_local(request):
	# droit='CREER_LOCAL'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 259
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context ={'title' : 'Ajouter un local',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'locals':dao_local.toListLocal(),
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/local/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_local(request):

	try:
		designation = request.POST['designation']
		description = request.POST['description']
		type_local = request.POST["type_local"]
		parent_id = request.POST["parent_local"]
		auteur = identite.utilisateur(request)

		if parent_id: parent_id = int(parent_id)

		local=dao_local.toCreateLocal(designation,description, type_local,parent_id)
		local=dao_local.toSaveLocal(auteur, local)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_local',args=(local.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER LOCAL \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_local'))


def get_details_local(request,ref):
	# droit='LISTER_LOCAL'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 258
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		local=dao_local.toGetLocal(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/local/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,local)

		context ={'title' : 'Détails sur un local',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'local' : local,'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS LOCAL \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_local'))

def get_modifier_local(request,ref):
	# droit='MODIFIER_LOCAL'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 260
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_local.toGetLocal(ref)
	context ={'title' : 'Modifier un local',
	'actions':auth.toGetActions(modules,utilisateur),'sous_modules': sous_modules,'modules' : modules,
		'organisation': dao_organisation.toGetMainOrganisation(),'locals':dao_local.toListLocal(),
	'model':model, 'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/local/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_local(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		type_local = request.POST["type_local"]
		auteur = identite.utilisateur(request)
		parent_id = request.POST["parent_local"]
		if parent_id: parent_id = int(parent_id)

		local=dao_local.toCreateLocal(designation,description, type_local,parent_id)
		local=dao_local.toUpdateLocal(id, local)
		messages.add_message(request, messages.SUCCESS,"Opération effectuée avec succès !")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_local',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER LOCAL \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_local'))


def get_lister_lettrage(request):
	# droit='LISTER_LETTRAGE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 262
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_lettrage.toListLettrage()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_lettrage.toListLettrage(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context ={'title' : 'Liste des lettrages',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model' : model,'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleComptabilite/lettrage/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_lettrage(request):
	# droit='CREER_LETTRAGE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 263
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context ={'title' : 'Ajouter un lettrage',
	'actions':auth.toGetActions(modules,utilisateur),'sous_modules': sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/lettrage/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_lettrage(request):

	try:
		designation = request.POST['designation']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		lettrage=dao_lettrage.toCreateLettrage(designation,description)
		lettrage=dao_lettrage.toSaveLettrage(auteur, lettrage)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_lettrage',args=(lettrage.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER LETTRAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_lettrage'))


def get_details_lettrage(request,ref):
	# droit='LISTER_LETTRAGE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 262
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		lettrage=dao_lettrage.toGetLettrage(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/lettrage/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,lettrage)


		context ={'title' : 'Details sur lettrage',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'lettrage' : lettrage,'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS LETTRAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_lettrage'))

def get_modifier_lettrage(request,ref):
	# droit='MODIFIER_LETTRAGE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 264
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_lettrage.toGetLettrage(ref)
	context ={'title' : 'Modifier un lettrage',
	'actions':auth.toGetActions(modules,utilisateur),'sous_modules': sous_modules,'modules' : modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/lettrage/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_lettrage(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		lettrage=dao_lettrage.toCreateLettrage(designation,description)
		lettrage=dao_lettrage.toUpdateLettrage(id, lettrage)
		messages.add_message(request, messages.ERROR,"Opération effectuée avec succès !")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_lettrage',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER LETTRAGE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_lettrage'))



def get_lister_compte_banque(request):
	# droit='LISTER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 266
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	# model = dao_compte_banque.toListCompteBanque()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_compte_banque.toListCompteBanque(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)
	context ={
		'title' : 'Liste des comptes bancaires',
		'model' : model,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'sous_modules': sous_modules,'modules' : modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/compte_banque/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_compte_banque(request):
	# droit='CREER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 267
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	employes = dao_employe.toListEmployes()
	comptes = dao_compte.toListComptes()
	devises = dao_devise.toListDevises()

	context ={'title' : 'Ajouter un compte bancaire','utilisateur' : utilisateur,
	'employes':employes,
	'comptes':comptes,
	'devises':devises,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'sous_modules': sous_modules,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/compte_banque/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_compte_banque(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		description = request.POST['description']

		numero_compte = request.POST['numero_compte']
		type_compte = request.POST['type_compte']
		banque_id = request.POST['banque_id']

		code_journal = request.POST['code_journal']
		compte_debit_id = request.POST['compte_debit_id']
		compte_id = request.POST['compte_id']
		compte_credit_id = request.POST['compte_credit_id']
		devise_id = request.POST['devise_id']

		if compte_credit_id == "":
			compte_credit_id = None
		if compte_debit_id == "":
			compte_debit_id = None
		if devise_id == "":
			devise_id = None
		if compte_id == "":
			compte_id = dao_compte.toGetCompteCaisse()

		auteur = identite.utilisateur(request)

		#creation du journal
		journal = dao_journal.toCreateJournal(code_journal,designation,3,True,compte_debit_id,compte_credit_id,devise_id)
		journal = dao_journal.toSaveJournal(auteur,journal)

		banque=dao_compte_banque.toCreateCompteBanque(designation,description,numero_compte,type_compte,banque_id,journal.id, compte_debit_id)
		banque=dao_compte_banque.toSaveCompteBanque(auteur, banque)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_compte_banque',args=(banque.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER BANQUE \n {}'.format(auteur.nom_complet, module,e))
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_compte_banque'))


def get_details_compte_banque(request,ref):
	# droit='LISTER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 266
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		banque=dao_compte_banque.toGetCompteBanque(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/compte_banque/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,banque)

		context ={'title' : 'Details sur un compte bancaire','banque' : banque,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'actions':auth.toGetActions(modules,utilisateur),'sous_modules': sous_modules,'modules' : modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS BANQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_compte_banque'))
def get_modifier_compte_banque(request,ref):
	# droit='MODIFIER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 268
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_compte_banque.toGetCompteBanque(ref)
	comptes = dao_compte.toListComptes()
	context ={'title' : 'Modifier un compte bancaire','model':model,
	'comptes':comptes,'sous_modules': sous_modules,'modules' : modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/compte_banque/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_compte_banque(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		journal_id = request.POST['journal_id']

		numero_compte = request.POST['numero_compte']
		type_compte = request.POST['type_compte']
		banque_id = request.POST['banque_id']
		compte_id = request.POST["compte_id"]

		if journal_id == "":
			journal_id = None
		if compte_id == "":
			compte_id = None
			compte_id = dao_compte.toGetCompteCaisse()
		auteur = identite.utilisateur(request)

		banque=dao_compte_banque.toCreateCompteBanque(designation,description,numero_compte,type_compte,banque_id,journal_id, compte_id)
		banque=dao_compte_banque.toUpdateCompteBanque(id, banque)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_compte_banque',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER BANQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_compte_banque'))


def get_lister_caisse(request):
	# droit='LISTER_CAISSE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 270
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	# model = dao_caisse.toListCaisse()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_caisse.toListCaisse(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des caisses',
		'model' : model,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1}
	template = loader.get_template('ErpProject/ModuleComptabilite/caisse/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_caisse(request):
	# droit='CREER_CAISSE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 271
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	employes = dao_employe.toListEmployes()
	comptes = dao_compte.toListComptes()
	devises = dao_devise.toListDevises()
	context ={'title' : 'Ajouter une caisse',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'employes':employes,
	'devises':devises,
	'comptes':comptes,
	'utilisateur' : utilisateur,'modules' : modules,
	'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/caisse/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_caisse(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		responsable_id = request.POST['responsable_id']
		code_journal = request.POST['code_journal']
		compte_id = request.POST['compte_id']
		compte_debit_id = request.POST['compte_debit_id']
		compte_credit_id = request.POST['compte_credit_id']
		devise_id = request.POST['devise_id']

		if compte_credit_id == "":
			compte_credit_id = None
		if compte_debit_id == "":
			compte_debit_id = None
		if compte_id == "":
			compte_id = dao_compte.toGetCompteCaisse()
		if responsable_id == "":
			responsable_id = None
		if devise_id == "":
			devise_id = None
		auteur = identite.utilisateur(request)

		#creation du journal
		journal = dao_journal.toCreateJournal(code_journal,designation,4,True,compte_debit_id,compte_credit_id,devise_id)
		journal = dao_journal.toSaveJournal(auteur,journal)
		#print(journal)
		#print(journal.id)


		#Creation de la caisse
		caisse=dao_caisse.toCreateCaisse(designation,description,responsable_id,journal.id, compte_id)
		caisse=dao_caisse.toSaveCaisse(auteur, caisse)
		#print(caisse)
		#print(caisse.journal)
		#print(caisse.journal_id)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_caisse',args=(caisse.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CAISSE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_caisse'))


def get_details_caisse(request,ref):
	# droit='LISTER_CAISSE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 270
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		caisse=dao_caisse.toGetCaisse(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/caisse/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,caisse)

		context ={'title' : 'Details sur une caisse',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'caisse' : caisse,'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CAISSE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_caisse'))
def get_modifier_caisse(request,ref):
	# droit='MODIFIER_CAISSE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 272
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_caisse.toGetCaisse(ref)
	employes = dao_employe.toListEmployes()
	comptes = dao_compte.toListComptes()


	context ={'title' : 'Modifier une caisse',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'comptes':comptes,
	'employes':employes,'modules' : modules,
		'sous_modules': sous_modules,
	'model':model, 'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/caisse/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_caisse(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		responsable_id = request.POST['responsable_id']
		journal_id = request.POST['journal_id']
		compte_id = request.POST['compte_id']

		if journal_id == "":
			journal_id = None
		if compte_id == "":
			compte_id = None
			compte_id = dao_compte.toGetCompteCaisse()
		auteur = identite.utilisateur(request)

		caisse=dao_caisse.toCreateCaisse(designation,description,responsable_id,journal_id, compte_id)
		caisse=dao_caisse.toUpdateCaisse(id, caisse)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_caisse'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CAISSE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_caisse'))


def get_lister_operationtresorerie(request,ref,filter):
	# droit='LISTER_OPERATION_TRESORERIE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 274
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	id = int(ref)
	if response != None:
		return response

	if filter == "caisse":
		# model = dao_operationtresorerie.toListOperationtresorerieOfCaisse(id)
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_operationtresorerie.toListOperationtresorerieOfCaisse(id), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		objet = dao_caisse.toGetCaisse(id)
		title = objet.designation + " : Liste des opérations de caisse"
	elif filter == "banque":
		# model = dao_operationtresorerie.toListOperationtresorerieOfBanque(id)
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_operationtresorerie.toListOperationtresorerieOfBanque(id), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		objet = dao_compte_banque.toGetCompteBanque(id)
		title = objet.designation + " : Liste des relevés bancaires"

	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : title,
		'objet':objet,
		'filter':filter,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : model,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1}
	template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_operationtresorerie(request,ref,filter):
	# droit='CREER_OPERATION_TRESORERIE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 275
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	id = int(ref)
	if filter == "caisse":
		model = dao_operationtresorerie.toGetLastOperationtresorerie(id, filter)
		title = "Ajouter une opération de caisse"
		objet = dao_caisse.toGetCaisse(id)
	elif filter == "banque":
		model = dao_operationtresorerie.toGetLastOperationtresorerie(id, filter)
		title = "Ajouter un relevé bancaire"
		objet = dao_compte_banque.toGetCompteBanque(id)



	devise = objet.journal.devise
	partenaires = dao_personne.toListPersonnes()
	factures = dao_facture.toListFacturesNonSoldees()
	context ={'title' : title,
	'objet':objet,
	'filter':filter,
	'last_operation':model,
	'factures':factures,
	'devise':devise,
	'partenaires':partenaires,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,
	'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_operationtresorerie(request):
	sid = transaction.savepoint()
	type_operation = request.POST['type_operation']
	objet_id = request.POST["objet_id"]
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_operation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		#Manipulation de généralisation du cas Caisse / Banque
		if type_operation == "caisse":
			caisse_id = objet_id
			compte_banque_id = None
			objet_caisse_banque = dao_caisse.toGetCaisse(objet_id)
			compte_local_id = objet_caisse_banque.compte_comptable_id if objet_caisse_banque.compte_comptable_id != None else dao_compte.toGetCompteCaisse().id
		elif type_operation == "banque":
			compte_banque_id = objet_id
			caisse_id = None
			objet_caisse_banque = dao_compte_banque.toGetCompteBanque(objet_id)
			compte_local_id = objet_caisse_banque.compte_comptable_id if objet_caisse_banque.compte_comptable_id != None else dao_compte.toGetCompteBanque().id

		#Test sur l'existence d'un compte local
		if compte_local_id == None:
			messages.error(request,'Aucun compte comptable configuré, veuillez en définir' )
			return HttpResponseRedirect(reverse('module_comptabilite_add_operationtresorerie', args=(objet_id,type_operation,)))

		journal_id = request.POST['journal_id']
		reference = request.POST['reference']




		balance_initiale = request.POST['balance_initiale']
		solde = request.POST['solde']
		date_operation = request.POST['date_operation']
		date_operation = timezone.datetime(int(date_operation[6:10]), int(date_operation[3:5]), int(date_operation[0:2]))
		date_comptable = request.POST['date_comptable']
		date_comptable = timezone.datetime(int(date_comptable[6:10]), int(date_comptable[3:5]), int(date_comptable[0:2]))
		devise_id = request.POST['devise_id']
		taux_id = None
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		journal = dao_journal.toGetJournal(journal_id)
		devise = dao_devise.toGetDevise(devise_id)

		#Enregistrement de l'operation
		operationtresorerie=dao_operationtresorerie.toCreateOperationtresorerie(reference,journal_id,caisse_id,compte_banque_id,type_operation,balance_initiale,solde,date_operation,date_comptable,devise_id,taux_id,description)
		operationtresorerie=dao_operationtresorerie.toSaveOperationtresorerie(auteur, operationtresorerie)

		#Enregistrement des lignes

		list_date_ligne_operation = request.POST.getlist('date_ligne_operation', None)
		list_libelle = request.POST.getlist('libelle', None)
		list_partenaire = request.POST.getlist('partenaire', None)
		list_facture = request.POST.getlist('facture', None)
		list_type_operation_ligne = request.POST.getlist('type_operation_ligne', None)
		list_montant = request.POST.getlist('montant', None)
		list_motif = request.POST.getlist('motif', None)

		for i in range (0, len(list_date_ligne_operation)):
			date_ligne_operation = list_date_ligne_operation[i]
			date_ligne_operation = timezone.datetime(int(date_ligne_operation[6:10]), int(date_ligne_operation[3:5]), int(date_ligne_operation[0:2]))
			libelle = list_libelle[i]
			partenaire_id = list_partenaire[i]
			if partenaire_id == "":
				partenaire_id = None
			facture_id = list_facture[i]
			if facture_id == "":
				facture_id = None
			type_operation_ligne = list_type_operation_ligne[i]
			montant = list_montant[i]
			motif = list_motif[i]

			ligne_operation = dao_ligne_operation_tresorerie.toCreateLigne_operation_tresorerie(reference,libelle,partenaire_id,montant,devise_id,taux_id,type_operation_ligne, motif,operationtresorerie.id,date_ligne_operation)
			ligne_operation = dao_ligne_operation_tresorerie.toSaveLigne_operation_tresorerie(auteur,ligne_operation)
			ligne_operation.save()


			##################################################ENREGISTREMENT PAIEMENT###################

			if facture_id:
				facture = dao_facture.toGetFacture(facture_id)
				#print("nakatii oooooh")
				if type_operation_ligne == '2':
					#print("apa ",type_operation_ligne)
					partenaire = dao_fournisseur.toGetFournisseur(partenaire_id)
					compte_partenaire = dao_compte.toGetCompteFournisseur()
				elif type_operation_ligne == '1' :
					#print('lidia',type_operation_ligne)
					partenaire = dao_client.toGetClient(partenaire_id)
					compte_partenaire = dao_compte.toGetCompteClient()
				#On enregistre la transaction
				statut_transaction = dao_statut_transaction.toGetStatutSuccess()
				transaction_paiement = dao_transaction.toCreateTransaction(facture_id, statut_transaction["id"], 1)
				transaction_paiement = dao_transaction.toSaveTransaction(auteur, transaction_paiement)
				transaction_paiement_id = transaction_paiement.id
				#print('transaction cree avec id {}'.format(transaction_paiement_id))

				# On enregistre le paiement
				paiement = dao_paiement.toCreatePaiement(transaction_paiement_id, date_ligne_operation, facture_id, devise_id, montant, 1, journal_id , partenaire_id , auteur.id, libelle, motif)
				#print(paiement)
				paiement = dao_paiement.toSavePaiement(paiement)
				#print('paiement cree avec id {}'.format(paiement.id))
				if paiement :
					paiement.est_lettre = True
					paiement.est_valide = True
					paiement.ligne_operation_tresorerie_id = ligne_operation.id
					paiement.save()
					ligne_operation.paiement_id = paiement.id
					ligne_operation.facture_id = facture_id
					ligne_operation.est_lettre = True
					ligne_operation.save()


				#print("montant", montant)
				#print("montant restat", facture.separateur_montant_restant)
				#print("montant", facture.montant)
				montant_restant = dao_facture.toGetMontantRestantOfPaymentFacture(facture_id)
				#print("montant_restant t", montant_restant)


				if makeFloat(montant) > makeFloat(montant_restant):
					transaction.savepoint_rollback(sid)
					messages.error(request,'La ligne sur laquelle la facture est renseignée fait l\'objet d\'un montant supérieur à ce qui reste !' )
					return HttpResponseRedirect(reverse('module_comptabilite_add_operationtresorerie', args=(objet_id,type_operation,)))
				elif makeFloat(montant) == makeFloat(montant_restant):
					#print("moses ", montant_restant)
					facture.est_soldee = True
					facture.save()
					#print("************ fzcture payee")

				#print("2222 ", montant_restant)


				#On enregistre le payloads (Informations supplémentaires et utile pour le paiement)

				logs = "{'journal':'%s', 'montant':'%s', 'devise':'%s' }" % (journal.designation, montant, devise.designation)
				payloads = dao_payloads.toCreatePayloads(paiement.id, logs)
				dao_payloads.toSavePayloads(payloads)
				#print('payloads cree avec id {}'.format(dao_payloads.id))

				# ECRITURES COMPTABLES DUES AU PAIEMENT DU FOURNISSEUR
				#Ici On débite le compte de trésorerie
				date_piece = timezone.now()
				compte_tresorerie = journal.compte_debit

				piece_comptable = dao_piece_comptable.toCreatePieceComptable(paiement.designation, "", montant, journal_id, date_ligne_operation, partenaire_id, None, None, facture_id, "PAIEMENT FOURNISSEUR", devise.id, taux_id)
				piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
				#print('piece cree avec id {}'.format(piece_comptable.id))


				#print('dev ',devise.id)
				#print('dev ',partenaire)

				if partenaire.compte != None: compte_partenaire_id = partenaire.compte_id




				#print('dev ',partenaire)

				if type_operation_ligne == '2':

					ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, montant, 0, compte_local_id, piece_comptable.id, facture.lettrage_id)
					ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
					#print('here we are')
					#print('ecriture credit cree avec id {}'.format(ecriture_credit.id))

					ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(partenaire.nom_complet, 0, montant, compte_partenaire.id, piece_comptable.id, facture.lettrage_id)
					ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
					#print('ecriture debit cree avec id {}'.format(ecriture_debit.id))

				elif type_operation_ligne == '1' :

					ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, 0, montant, compte_partenaire.id, piece_comptable.id, facture.lettrage_id)
					ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
					#print('here we are')
					#print('ecriture credit cree avec id {}'.format(ecriture_debit.id))


					ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(partenaire.nom_complet, montant, 0, compte_local_id, piece_comptable.id, facture.lettrage_id)
					ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
					#print('ecriture debit cree avec id {}'.format(ecriture_credit.id))

			##################################################ENREGISTREMENT PAIEMENT###################



		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_list_operationtresorerie', args=(objet_id,type_operation,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER OPERATIONTRESORERIE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_operationtresorerie', args=(objet_id,type_operation,)))


def get_details_operationtresorerie(request,ref):
	# droit='LISTER_OPERATION_TRESORERIE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 274
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		operationtresorerie=dao_operationtresorerie.toGetOperationtresorerie(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,operationtresorerie)

		context ={'title' : 'Details sur une opération de trésorerie',
		'actions':auth.toGetActions(modules,utilisateur),'modules' : modules,'sous_modules': sous_modules,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'operationtresorerie' : operationtresorerie,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS OPERATIONTRESORERIE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_operationtresorerie'))
def get_modifier_operationtresorerie(request,ref):
	# droit='MODIFIER_OPERATION_TRESORERIE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 276
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_operationtresorerie.toGetOperationtresorerie(ref)
	#print(model)
	#print(model.id)
	ligne_operation = dao_ligne_operation_tresorerie.toListLigneTresorerieofOperation(ref)
	#print("lihn",ligne_operation)


	if model.caisse != None:
		objet = model.caisse
		title = "Modifier une opération de caisse"
		filter = "caisse"
	elif model.compte_banque != None:
		objet = model.compte_banque
		title = "Modifier un relevé bancaire"
		filter = "banque"

	partenaires = dao_personne.toListPersonnes()
	lignes_billeterie = dao_ligne_billeterie.toGetLigneFromBilleterie(model.billeterie_id)
	factures = dao_facture.toListFacturesNonSoldees()

	#Teste si tous les lignes de l'objet sont lettré
	est_lettre = True
	for ligne in ligne_operation:
		if ligne.est_lettre == False:
			est_lettre = False


	context ={'title' : title,
	'ligne_operation':ligne_operation,
	'objet':objet,
	'factures':factures,
	'est_lettre':est_lettre,
	'filter':filter,
	'lignes_billeterie':lignes_billeterie,
	'partenaires':partenaires,'modules' : modules,'sous_modules': sous_modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/update.html')
	return HttpResponse(template.render(context, request))


def get_closed_operationtresorerie(request,ref):

	ref = int(ref)
	operationtresorerie = dao_operationtresorerie.toGetOperationtresorerie(ref)

	#Test de la conformité de l'extrait
	solde_final = operationtresorerie.balance_initiale
	ligne_operaton = dao_ligne_operation_tresorerie.toListLigneTresorerieofOperation(ref)
	for item in ligne_operaton:
		if item.type_operation == 2:
			solde_final -= item.montant
		else:
			solde_final += item.montant

	#print("solde ", solde_final)
	#print("op", operationtresorerie.solde)
	if makeFloat(solde_final) != makeFloat(operationtresorerie.solde):
		messages.error(request,'Les montants ne correspondent pas' )
		return get_modifier_operationtresorerie(request,ref)

	#print("ca passe")
	is_done = dao_operationtresorerie.toClosedOperationtresorerie(ref)


	if is_done:
		messages.add_message(request, messages.SUCCESS,'Opération de cloture réussie!' )
		return get_modifier_operationtresorerie(request,ref)


@transaction.atomic
def post_modifier_operationtresorerie(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	#print("ident", id)
	type_operation = request.POST['type_operation']
	objet_id = request.POST["objet_id"]
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_operation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		#Manipulation de généralisation du cas Caisse / Banque
		if type_operation == "caisse":
			caisse_id = objet_id
			compte_banque_id = None
			objet_caisse_banque = dao_caisse.toGetCaisse(objet_id)
			compte_local_id = objet_caisse_banque.compte_comptable_id if objet_caisse_banque.compte_comptable_id != None else dao_compte.toGetCompteCaisse().id
		elif type_operation == "banque":
			compte_banque_id = objet_id
			caisse_id = None
			objet_caisse_banque = dao_compte_banque.toGetCompteBanque(objet_id)
			compte_local_id = objet_caisse_banque.compte_comptable_id if objet_caisse_banque.compte_comptable_id != None else dao_compte.toGetCompteBanque().id

		#Test sur l'existence d'un compte local
		if compte_local_id == None:
			messages.error(request,'Aucun compte comptable configuré, veuillez en définir' )
			return HttpResponseRedirect(reverse('module_comptabilite_add_operationtresorerie', args=(objet_id,type_operation,)))

		reference = request.POST['reference']
		journal_id = request.POST['journal_id']
		journal = dao_journal.toGetJournal(journal_id)
		balance_initiale = request.POST['balance_initiale']
		solde = request.POST['solde']
		date_operation = request.POST['date_operation']
		date_operation = timezone.datetime(int(date_operation[6:10]), int(date_operation[3:5]), int(date_operation[0:2]))
		date_comptable = request.POST['date_comptable']
		date_comptable = timezone.datetime(int(date_comptable[6:10]), int(date_comptable[3:5]), int(date_comptable[0:2]))
		devise_id = request.POST['devise_id']
		devise = dao_devise.toGetDevise(devise_id)
		taux_id = None
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		#Enregistrement modification opération
		operationtresorerie=dao_operationtresorerie.toCreateOperationtresorerie(reference,journal_id,caisse_id,compte_banque_id,type_operation,balance_initiale,solde,date_operation,date_comptable,devise_id,taux_id,description)
		dao_operationtresorerie.toUpdateOperationtresorerie(id, operationtresorerie)

		list_date_ligne_operation = request.POST.getlist('date_ligne_operation', None)
		list_libelle = request.POST.getlist('libelle', None)
		list_partenaire = request.POST.getlist('partenaire', None)
		list_type_operation_ligne = request.POST.getlist('type_operation_ligne', None)
		list_montant = request.POST.getlist('montant', None)
		list_facture = request.POST.getlist('facture', None)
		list_motif = request.POST.getlist('motif', None)
		list_all_ligne_id = request.POST.getlist('all_ligne_id', None)
		list_ligne_id = request.POST.getlist('ligne_id', None)

		for i in range(0, len(list_all_ligne_id)):
			is_find = False
			the_item = list_all_ligne_id[i]
			for j in range(0, len(list_ligne_id)):
				if the_item == list_ligne_id[j]:
					is_find = True
			if is_find == False:
				dao_ligne_operation_tresorerie.toDeleteLigne_operation_tresorerie(the_item)

		for i in range(0, len(list_date_ligne_operation)):
			#print("you ve win")
			date_ligne_operation = list_date_ligne_operation[i]
			date_ligne_operation = timezone.datetime(int(date_ligne_operation[6:10]), int(date_ligne_operation[3:5]), int(date_ligne_operation[0:2]))
			libelle = list_libelle[i]
			partenaire_id = list_partenaire[i]
			if partenaire_id == "":
				partenaire_id = None
			facture_id = list_facture[i]
			if facture_id == "":
				facture_id = None
			type_operation_ligne = list_type_operation_ligne[i]
			montant = list_montant[i]
			motif = list_motif[i]
			ligne_id = int(list_ligne_id[i])
			#print("you ve win1", facture_id)

			if ligne_id != 0:
				#print("you ve win")
				ligne_operation = dao_ligne_operation_tresorerie.toCreateLigne_operation_tresorerie(reference,libelle,partenaire_id,montant,devise_id,taux_id,type_operation_ligne, motif,id,date_ligne_operation)
				dao_ligne_operation_tresorerie.toUpdateLigne_operation_tresorerie(ligne_id,ligne_operation)

			else:
				#print("you've win2")
				ligne_operation = dao_ligne_operation_tresorerie.toCreateLigne_operation_tresorerie(reference,libelle,partenaire_id,montant,devise_id,taux_id,type_operation_ligne, motif,id,date_ligne_operation)
				ligne_operation = dao_ligne_operation_tresorerie.toSaveLigne_operation_tresorerie(auteur,ligne_operation)
				#ligne_id = ligne_operation.id
			#print("you ve win3")

			##################################################ENREGISTREMENT PAIEMENT###################

			ligne_operation = dao_ligne_operation_tresorerie.toGetLigne_operation_tresorerie(ligne_id)
			#print("ligne op",ligne_operation)
			if facture_id and not ligne_operation.est_lettre:
				#print("you've win4")
				facture = dao_facture.toGetFacture(facture_id)
				#print("nakatii oooooh")
				if type_operation_ligne == '2':
					#print("apa ",type_operation_ligne)
					partenaire = dao_fournisseur.toGetFournisseur(partenaire_id)
					compte_partenaire = dao_compte.toGetCompteFournisseur()
				elif type_operation_ligne == '1' :
					#print('lidia',type_operation_ligne)
					partenaire = dao_client.toGetClient(partenaire_id)
					compte_partenaire = dao_compte.toGetCompteClient()
				#On enregistre la transaction
				statut_transaction = dao_statut_transaction.toGetStatutSuccess()
				transaction_paiement = dao_transaction.toCreateTransaction(facture_id, statut_transaction["id"], 1)
				transaction_paiement = dao_transaction.toSaveTransaction(auteur, transaction_paiement)
				transaction_paiement_id = transaction_paiement.id
				#print('transaction cree avec id {}'.format(transaction_paiement_id))

				# On enregistre le paiement
				paiement = dao_paiement.toCreatePaiement(transaction_paiement_id, date_ligne_operation, facture_id, devise_id, montant, 1, journal_id , partenaire_id , auteur.id, libelle, motif)
				#print(paiement)
				paiement = dao_paiement.toSavePaiement(paiement)
				#print('paiement cree avec id {}'.format(paiement.id))
				if paiement :
					#print("paiement exist")
					paiement.est_lettre = True
					#print("paiement exist")
					paiement.est_valide = True
					#print("paiement exist")
					paiement.ligne_operation_tresorerie_id = ligne_operation.id
					#print("paiement exist")
					paiement.save()
					#print("paiement exist")
					ligne_operation.paiement_id = paiement.id
					#print("paiement exist")
					ligne_operation.facture_id = facture_id
					ligne_operation.est_lettre = True
					ligne_operation.save()
					#print("paiement exist")


				#print("montant", montant)
				#print("montant restat", facture.separateur_montant_restant)
				#print("montant", facture.montant)
				montant_restant = dao_facture.toGetMontantRestantOfPaymentFacture(facture_id)
				#print("montant_restant t", montant_restant)


				if makeFloat(montant) > makeFloat(montant_restant):
					transaction.savepoint_rollback(sid)
					messages.error(request,'La ligne sur laquelle la facture est renseignée fait l\'objet d\'un montant supérieur à ce qui reste !' )
					return HttpResponseRedirect(reverse('module_comptabilite_add_operationtresorerie', args=(objet_id,type_operation,)))
				elif makeFloat(montant) == makeFloat(montant_restant):
					#print("moses ", montant_restant)
					facture.est_soldee = True
					facture.save()
					#print("************ fzcture payee")

				#print("2222 ", montant_restant)


				#On enregistre le payloads (Informations supplémentaires et utile pour le paiement)

				logs = "{'journal':'%s', 'montant':'%s', 'devise':'%s' }" % (journal.designation, montant, devise.designation)
				payloads = dao_payloads.toCreatePayloads(paiement.id, logs)
				dao_payloads.toSavePayloads(payloads)
				#print('payloads cree avec id {}'.format(dao_payloads.id))

				# ECRITURES COMPTABLES DUES AU PAIEMENT DU FOURNISSEUR
				#Ici On débite le compte de trésorerie
				date_piece = timezone.now()
				compte_tresorerie = journal.compte_debit

				piece_comptable = dao_piece_comptable.toCreatePieceComptable(paiement.designation, "", montant, journal_id, date_ligne_operation, partenaire_id, None, None, facture_id, "PAIEMENT FOURNISSEUR", devise.id, taux_id)
				piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
				#print('piece cree avec id {}'.format(piece_comptable.id))


				#print('dev ',devise.id)
				#print('dev ',partenaire)

				if partenaire.compte != None: compte_partenaire = dao_compte.toGetCompte(partenaire.compte_id)


				#print('dev ',partenaire)

				if type_operation_ligne == '2':

					ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, montant, 0, compte_local_id, piece_comptable.id, facture.lettrage_id)
					ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
					#print('here we are')
					#print('ecriture credit cree avec id {}'.format(ecriture_credit.id))

					ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(partenaire.nom_complet, 0, montant, compte_partenaire.id, piece_comptable.id, facture.lettrage_id)
					ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
					#print('ecriture debit cree avec id {}'.format(ecriture_debit.id))

				elif type_operation_ligne == '1' :

					ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, 0, montant, compte_partenaire.id, piece_comptable.id, facture.lettrage_id)
					ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
					#print('here we are')
					#print('ecriture credit cree avec id {}'.format(ecriture_debit.id))


					ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(partenaire.nom_complet, montant, 0, compte_local_id, piece_comptable.id, facture.lettrage_id)
					ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
					#print('ecriture debit cree avec id {}'.format(ecriture_credit.id))

			##################################################ENREGISTREMENT PAIEMENT###################



		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès")
		#return get_modifier_operationtresorerie(request,id)
		return HttpResponseRedirect(reverse('module_comptabilite_list_operationtresorerie',args=(objet_id,type_operation,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER OPERATIONTRESORERIE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_operationtresorerie', args=(id,)))




def get_lister_bank(request):
	# droit='LISTER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 266
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	model = dao_banque.toListBank()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_banque.toListBank(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des banques',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : model,
		'view': view,
		'utilisateur' : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/bank/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_bank(request):
	# droit='CREER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 267
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	context ={'title' : 'Ajouter une banque',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'isPopup': True if 'isPopup' in request.GET else False,
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/bank/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_bank(request):

	try:
		designation = request.POST['designation']
		adresse = request.POST['adresse']
		codebank = request.POST['code']
		observation = request.POST['observation']
		isPopup = request.POST["isPopup"]
		auteur = identite.utilisateur(request)

		bank=dao_banque.toCreateBank(designation,adresse,observation)
		bank=dao_banque.toSaveBank(auteur, bank)
		bank.code = codebank
		bank.save()
		return HttpResponseRedirect(reverse('module_comptabilite_detail_bank',args=(bank.id,))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER BANK \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_bank'))


def get_details_bank(request,ref):
	# droit='LISTER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 266
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		bank=dao_banque.toGetBank(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/bank/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bank)

		context ={'title' : 'Détails sur une banque',
		'actions':auth.toGetActions(modules,utilisateur),'modules' : modules,'sous_modules': sous_modules,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'bank' : bank,'utilisateur' : utilisateur,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS BANK \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_bank'))
def get_modifier_bank(request,ref):
	# droit='MODIFIER_BANQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 268
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_banque.toGetBank(ref)
	context ={'title' : 'Modifier les informations sur une banque',
	'actions':auth.toGetActions(modules,utilisateur),'modules' : modules,'sous_modules': sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/bank/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_bank(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		adresse = request.POST['adresse']
		observation = request.POST['observation']
		auteur = identite.utilisateur(request)

		bank=dao_banque.toCreateBank(designation,adresse,observation)
		bank=dao_banque.toUpdateBank(id, bank)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_bank',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER BANK \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_bank'))



def get_creer_lettrage_operationtresorerie(request,ref):
	# droit='CREER_LETTRAGE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 262
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	operationtresorerie = dao_operationtresorerie.toGetOperationtresorerie(ref)
	ligne_operation = dao_ligne_operation_tresorerie.toListLigneTresorerieofOperationNonLettre(ref)
	comptes = dao_compte.toListComptes()
	personnes = dao_personne.toListPersonnes()


	if operationtresorerie.caisse != None:
		filter = "caisse"
		objet = operationtresorerie.caisse
	elif operationtresorerie.compte_banque != None:
		filter = "banque"
		objet = operationtresorerie.compte_banque


	context ={'title' : 'Journal ' + operationtresorerie.journal.designation + ' : Lettrer les opérations',
	'ligne_operation':ligne_operation,
	'comptes':comptes,
	'filter':filter,
	'objet':objet,
	'partenaires':personnes,
	'model':operationtresorerie,
	'modules' : modules,
	'sous_modules': sous_modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur': utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/lettrage/add.html')
	return HttpResponse(template.render(context, request))


@transaction.atomic
def post_creer_lettrage_operationtresorerie(request):
	sid = transaction.savepoint()
	operation_id = request.POST["operation_id"]
	try:
		erreur_survenue = False
		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		taux = None

		partenaire_id = request.POST["partenaire_id"]
		ligne_operation_id = request.POST["ligne_operation_id"]
		facture_id = request.POST["facture_id"]
		est_facture = False

		filter = request.POST["filter"]

		if filter == "caisse":
			designation = "Opération de caisse"
		elif filter == "banque":
			designation = "Relevé bancaire"

		operation_tresorerie = dao_operationtresorerie.toGetOperationtresorerie(operation_id)

		if facture_id == "" or facture_id == 0:
			#print("est pas facture")
			facture_id = None
			lettrage = dao_lettrage.toCreateLettrage(designation,operation_tresorerie.description)
			lettrage = dao_lettrage.toSaveLettrage(auteur,lettrage)
		else:
			#print("est facture")
			est_facture = True
			facture = dao_facture.toGetFacture(facture_id)
			lettrage = facture.lettrage



		#Creation du lettrage



		#Creation de la piece comptable

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation, operation_tresorerie.reference, 0, operation_tresorerie.journal_id, operation_tresorerie.date_comptable, partenaire_id,None,None,facture_id,operation_tresorerie.devise_id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print(piece_comptable)

		list_compte_id = request.POST.getlist("compte_id", None)
		list_libelles = request.POST.getlist("libelle", None)
		list_montants_debit = request.POST.getlist("montant_debit", None)
		list_montants_credit = request.POST.getlist("montant_credit", None)

		montant_test_debit = 0
		montant_test_credit = 0

		for i in range(0, len(list_compte_id)):
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])
			#print("montant credit", montant_credit)
			#print("montant debit", montant_debit)
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		if montant_test_credit != montant_test_debit:
			transaction.savepoint_rollback(sid)
			messages.error(request,'Echec : Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_comptabilite_add_lettrage_operationtresorerie", args=(operation_id,)))


		'''if est_facture:
			#Enregistrement des paiements
			statut_transaction = dao_statut_transaction.toGetStatutSuccess()
			transaction_paiement = dao_transaction.toCreateTransaction(facture.id, statut_transaction["id"], 1)
			transaction_paiement = dao_transaction.toSaveTransaction(auteur, transaction_paiement)

			paiement = dao_paiement.toCreatePaiement(transaction_paiement_id, operation_tresorerie.date_operation, facture.id, operation_tresorerie.devise_id, montant_test_credit, "Règlement", operation_tresorerie.journal_id , facture.fournisseur_id , auteur.id, "Paiement", "", True)
			paiement = dao_paiement.toSavePaiement(paiement)'''




		for i in range(0, len(list_compte_id)):
			compte_id = int(list_compte_id[i])
			libelle = list_libelles[i]
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])

			#print("COMPTE %s" % compte_id)
			#print("PIECE COMPTABLE %s" % piece_comptable)

			compte = dao_compte.toGetCompte(compte_id)

			ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte.id, piece_comptable.id, lettrage.id)
			ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
			if ecriture_comptable == None:
				erreur_survenue = True
				break

		#Mis à jour ligne est lettré true

		is_update = dao_ligne_operation_tresorerie.toSetLigneLettrage(ligne_operation_id, lettrage.id, facture_id)
		#print("ligne oper est mis a jour lettrage", is_update)



		if erreur_survenue == True:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR,"Echec : Une erreur est survenue lors de l'opératio")
			return HttpResponseRedirect(reverse("module_comptabilite_add_lettrage_operationtresorerie",args=(operation_id,)))
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_add_lettrage_operationtresorerie", args=(operation_id,)))
	except Exception as e:
		#print("ERREUR POST CREER LETTRAGE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse("module_comptabilite_add_lettrage_operationtresorerie", args=(operation_id,)))


def get_json_facture(request):
	try:
		#print("ima")
		data = []
		type_facture = request.GET["ref"]
		fournisseur_id = request.GET["fournisseur_id"]
		#print("type_facture", type_facture)

		if type_facture =="fournisseur":
			factures = dao_facture_fournisseur.toListFacturesFournisseurNonSoldeesOfFournisseur(fournisseur_id)
		else:
			factures = dao_facture_client.toListFacturesClientNonSoldees(fournisseur_id)

		#print("factures", factures)
		for facture in factures:
				item = {"id": facture.id,"numero_facture" : facture.numero_facture, "date_facturation":facture.date_facturation}
				data.append(item)
		#print(data)
		return JsonResponse(data, safe=False)

	except Exception as e:
		return JsonResponse([], safe=False)

from ModuleComptabilite.dao.dao_ecriture_analytique import dao_ecriture_analytique
from ModuleBudget.dao.dao_centre_cout import dao_centre_cout

def get_lister_ecriture_analytique(request):
	# droit='LISTER_ECRITURE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 341
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	# model = dao_ecriture_analytique.toListEcriture_analytique()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_ecriture_analytique.toListEcriture_analytique(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des écritures analytiques',
		'model' : model,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/ecriture_analytique/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_ecriture_analytique(request):
	# droit='CREER_ECRITURE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 342
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response


	comptes = dao_compte.toListComptes()
	centres = dao_centre_cout.toListCentreCoutOfTypeAccount()
	devises = dao_devise.toListDevisesActives()
	factures = dao_facture.toListFactures()

	context ={'title' : 'Ajouter une écriture analytique',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'centres':centres,
	'comptes':comptes,
	'factures':factures,
	'devises':devises,
	'modules' : modules,'sous_modules': sous_modules,
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/ecriture_analytique/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_ecriture_analytique(request):

	try:
		libelle = request.POST['libelle']
		compte_id = request.POST['compte_id']
		centre_cout_id = request.POST['centre_cout_id']
		facture_id = request.POST['facture_id']
		devise_id = request.POST['devise_id']
		montant = request.POST['montant']
		if devise_id == "" or devise_id == '0':
			devise_id = None
		auteur = identite.utilisateur(request)

		ecriture_analytique=dao_ecriture_analytique.toCreateEcriture_analytique(libelle,compte_id,centre_cout_id,facture_id, montant, devise_id)
		ecriture_analytique=dao_ecriture_analytique.toSaveEcriture_analytique(auteur, ecriture_analytique)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_ecriture_analytique',args=(ecriture_analytique.id)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER ECRITURE_ANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_ecriture_analytique'))


def get_details_ecriture_analytique(request,ref):
	# droit='LISTER_ECRITURE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 341
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		ecriture_analytique=dao_ecriture_analytique.toGetEcriture_analytique(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/ecriture_analytique/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,ecriture_analytique)

		context ={'title' : 'Details sur une écriture analytique','modules' : modules,'sous_modules': sous_modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'ecriture_analytique' : ecriture_analytique,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS ECRITURE_ANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_ecriture_analytique'))
def get_modifier_ecriture_analytique(request,ref):
	# droit='MODIFIER_ECRITURE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 343
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_ecriture_analytique.toGetEcriture_analytique(ref)
	context ={'title' : 'Modifier Ecriture_analytique',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'modules' : modules,'sous_modules': sous_modules,
	'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/ecriture_analytique/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_ecriture_analytique(request):

	id = int(request.POST['ref'])
	try:
		libelle = request.POST['libelle']
		compte_id = request.POST['compte_id']
		centre_cout_id = request.POST['centre_cout_id']
		facture_id = request.POST['facture_id']
		devise_id = request.POST['devise_id']
		montant = request.POST['montant']
		if devise_id == "" or devise_id == '0':
			devise_id = None
		auteur = identite.utilisateur(request)

		ecriture_analytique=dao_ecriture_analytique.toCreateEcriture_analytique(libelle,compte_id,centre_cout_id,facture_id, montant, devise_id)
		ecriture_analytique=dao_ecriture_analytique.toUpdateEcriture_analytique(id, ecriture_analytique)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_ecriture_analytique',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER ECRITURE_ANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_ecriture_analytique'))


def get_creer_piece_immobilisation(request):

	# droit="CREER_IMMOBILISATION"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 460
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	etat_actuel_id = request.POST["doc_id"]
	immobilisation = dao_immobilisation.toGet(etat_actuel_id)

	context = {
		"partenaire" : dao_personne.toListPersonnes(),
		"immobilisation":immobilisation,
		"comptes" : dao_compte.toListComptes(),
		#"devises" : dao_devise.toListDevisesActives(),
		"devises": dao_devise.toListDevises(),
		"journaux" : dao_journal.toListJournaux(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"title" : "Nouvelle pièce d'immobilisation",
		"utilisateur" : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 4
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/piece/add.html")
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_piece_immobilisation(request):
	sid = transaction.savepoint()
	ref = request.POST["ref"]
	try:
		erreur_survenue = False
		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		taux = None

		designation = request.POST["designation"]
		reference = request.POST["reference"]
		devise_id = int(request.POST["devise_id"])
		if devise_id != devise.id :
			devise = dao_devise.toGetDevise(devise_id)
			taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)
		partenaire_id = request.POST["partenaire_id"]
		if partenaire_id == "0" or partenaire_id == "":
			partenaire_id = None
		montant = 0
		description = request.POST["description"]
		journal_id = int(request.POST["journal_id"])

		date_piece = request.POST["date_piece"]
		date_piece = timezone.datetime(int(date_piece[6:10]), int(date_piece[3:5]), int(date_piece[0:2]))

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation, reference, montant, journal_id, date_piece, partenaire_id, None, None, None, "", devise.id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print(piece_comptable)

		list_compte_id = request.POST.getlist("compte_id", None)
		list_libelles = request.POST.getlist("libelle", None)
		list_montants_debit = request.POST.getlist("montant_debit", None)
		list_montants_credit = request.POST.getlist("montant_credit", None)

		montant_test_debit = 0
		montant_test_credit = 0

		for i in range(0, len(list_compte_id)):
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		if montant_test_credit != montant_test_debit:
			messages.error(request,'Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_comptabilite_creer_piece"))


		for i in range(0, len(list_compte_id)):
			compte_id = int(list_compte_id[i])
			libelle = list_libelles[i]
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])

			#print("COMPTE %s" % compte_id)
			#print("PIECE COMPTABLE %s" % piece_comptable)

			compte = dao_compte.toGetCompte(compte_id)

			ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte.id, piece_comptable.id)
			ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
			if ecriture_comptable == None:
				erreur_survenue = True
				break

		if erreur_survenue == True:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la pièce comptable")
			return HttpResponseRedirect(reverse("module_comptabilite_details_immobilisation", args=(ref,)))

		#Passage du workflow
		immobilisation = dao_immobilisation.toGet(ref)
		immobilisation.est_comptabilise = True
		immobilisation.journal_id = journal_id
		immobilisation.devise_id = devise_id
		immobilisation.save()
		wkf_task.passingStepWorkflow(auteur,immobilisation)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_details_immobilisation", args=(ref,)))
	except Exception as e:
		#print("ERREUR POST CREER PIECE COMPTABLE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_comptabilite_details_immobilisation", args=(ref,)))


def get_creer_piece_traitement(request):

	# droit="CREER_IMMOBILISATION"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 460
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	etat_actuel_id = request.POST["doc_id"]
	traitement_immobilisation = dao_traitement_immobilisation.toGetTraitement_immobilisation(etat_actuel_id)
	lignes = dao_ligne_traitementimmobilisation.toListLigneOfTraitementNonTraite(etat_actuel_id)

	texte = ""
	if traitement_immobilisation.type_traitement == 1:
		texte = "Cession"
	elif traitement_immobilisation.type_traitement == 2:
		texte = "Mis au rebut"


	context = {
		"partenaire" : dao_personne.toListPersonnes(),
		'lignes_traitements':lignes,
		'traitement_immobilisation':traitement_immobilisation,
		"comptes" : dao_compte.toListComptes(),
		#"devises" : dao_devise.toListDevisesActives(),
		"devises": dao_devise.toListDevises(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"title" : "Passage d'écritures d'immobilisation de " + texte,
		"utilisateur" : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 4
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/immobilisation/traitement/add.html")
	return HttpResponse(template.render(context, request))


@transaction.atomic
def post_creer_piece_traitement(request):
	sid = transaction.savepoint()
	ref = request.POST["ref"]#traitement_immobilisation
	try:
		erreur_survenue = False
		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		taux = None

		ligne_traitement_id = request.POST["ligne_traitement_id"]
		immobilisation_id = request.POST["immobilisation_id"]

		traitement_immobilisation = dao_traitement_immobilisation.toGetTraitement_immobilisation(ref)
		immobilisation = dao_immobilisation.toGet(immobilisation_id)

		#print("#######")

		texte = ""
		if traitement_immobilisation.type_traitement == 1:
			texte = "Cession d'immobilisation"
		elif traitement_immobilisation == 2 :
			texte = "Mise au rebut d'immobilisation"


		piece_comptable = dao_piece_comptable.toCreatePieceComptable(texte, traitement_immobilisation.numero_traitement, 0, immobilisation.journal_id, timezone.now(), None,None,None,None,immobilisation.devise_id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print(piece_comptable)

		list_compte_id = request.POST.getlist("compte_id", None)
		list_libelles = request.POST.getlist("libelle", None)
		list_montants_debit = request.POST.getlist("montant_debit", None)
		list_montants_credit = request.POST.getlist("montant_credit", None)

		montant_test_debit = 0
		montant_test_credit = 0

		for i in range(0, len(list_compte_id)):
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		if montant_test_credit != montant_test_debit:
			transaction.savepoint_rollback(sid)
			messages.error(request,'Echec : Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_inventaire_detail_traitement_immobilisation", args=(ref,)))



		for i in range(0, len(list_compte_id)):
			compte_id = int(list_compte_id[i])
			libelle = list_libelles[i]
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])

			#print("COMPTE %s" % compte_id)
			#print("PIECE COMPTABLE %s" % piece_comptable)

			compte = dao_compte.toGetCompte(compte_id)

			ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte.id, piece_comptable.id, None)
			ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
			if ecriture_comptable == None:
				erreur_survenue = True
				break

		#Mis à jour ligne est lettré true

		is_update = dao_ligne_traitementimmobilisation.toSetLigneTraitement(ligne_traitement_id)
		is_so_update = dao_immobilisation.toSetImmobilisationNonAvailable(immobilisation_id)
		#print("ligne traitement est mis a jour", is_update)
		#print("immobilisation est mis a jour", is_update)

		#Passage d'état du workflow si toutes les lignes sont immobilisées
		lignes = dao_ligne_traitementimmobilisation.toListLigneOfTraitementNonTraite(ref)

		if not lignes:
			#print("it was last lignes")
			wkf_task.passingStepWorkflow(auteur,traitement_immobilisation)




		if erreur_survenue == True:
			transaction.savepoint_rollback(sid)
			messages.error(request,'Une erreur est survenue lors de l\'opération')
			return HttpResponseRedirect(reverse("module_inventaire_detail_traitement_immobilisation",args=(ref,)))
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_inventaire_detail_traitement_immobilisation", args=(ref,)))
	except Exception as e:
		#print("ERREUR POST CREER FILTRE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse("module_inventaire_detail_traitement_immobilisation", args=(ref,)))

		################################################ RAPPORT ########################################################
def get_lister_factures_avoir(request):

	# droit="LISTER_FACTURE_FOURNISSEUR"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 106
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	# model = dao_facture_client.toListFacturesAvoir()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_facture_client.toListFacturesAvoir(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste des factures d\'avoir',
		'model' : model,
		"utilisateur" : utilisateur,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 21
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/facture/avoir/list.html")
	return HttpResponse(template.render(context, request))


def generer_facture_avoir(request):
	# droit = 'CREER_RAPPORT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 486
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	clients = dao_client.toListClients()
	factures = dao_facture_client.toListFacturesAvoir()

	context =	{
		'title' : 'Générer une facture d\'avoir',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'clients':clients,
		'factures':factures,
		'utilisateur': utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2
	}
	template = loader.get_template('ErpProject/ModuleComptabilite/facture/avoir/add.html')
	return HttpResponse(template.render(context, request))


def get_facture_client_extend(request):
	if('ref' in request.GET):
		#fact = int(request.GET["facture_avant"])
		fact = int(request.GET["ref"])
		f = dao_facture_client.toGetFacture(fact)
		cli = f.client.id
		#print("Facture : ", fact)
		data = []
		factures = Model_Facture.objects.filter(type = "CLIENT").filter(client_id = cli).exclude(id = fact).order_by("-date_facturation")

		for facture in factures:
			element = {
				'id': facture.id,
				'designation' : facture.numero_facture
			}
			data.append(element)
		return JsonResponse(data, safe=False)
	else: return JsonResponse([], safe=False)

def post_generer_facture_avoir(request):
	try:
		# droit = 'CREER_RAPPORT'
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 486
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		client_id = int(request.POST['client_id'])
		facture_avant = int(request.POST['facture_avant'])
		facture_apres = int(request.POST['facture_apres'])
		destinataire = request.POST['destinataire']
		objet = request.POST['objet']
		type_facture = int(request.POST['type_facture'])
		sujet = request.POST['type']

		client = dao_client.toGetClient(client_id)
		facture_ap = dao_facture_client.toGetFacture(facture_apres)
		facture_av = dao_facture_client.toGetFacture(facture_avant)

	except Exception as e:
		#print(e)
		pass


	context =	{
		'title' : 'Lettre de Facture d\'avoir',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'client':client,
		'facture_ap':facture_ap,
		'facture_av':facture_av,
		'type_facture' : type_facture,
		'objet': objet,
		'destinataire' : destinataire,
		'utilisateur': utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2
	}

	template = loader.get_template('ErpProject/ModuleComptabilite/facture/avoir/item.html')
	return HttpResponse(template.render(context, request))

# OUVERTURE URLS
def get_creer_ouverture_organisation(request):
	modules, utilisateur,response = auth.toGetAuth(request)
	if response != None:
		return response
	try:
		organisation = dao_organisation.toGetMainOrganisation()
		devise = dao_devise.toGetDeviseReference()
		devises = dao_devise.toListDevisesActives()
		#types_organisations = dao_type_organisation.toListTypesOrganisation()

		nom = email = image = phone = fax = numero_fiscal = site_web = adresse = ""

		devise_id = devise.id
		devise = devise.designation
		pays_id = province_id = ville_id = commune_quartier_id = organisation_id = 0


		if organisation != None:
			organisation_id = organisation.id
			nom = organisation.nom
			email = organisation.email
			image = organisation.image
			phone = organisation.phone
			fax = organisation.fax
			numero_fiscal = organisation.numero_fiscal
			site_web = organisation.site_web
			adresse = organisation.adresse
			if organisation.devise_id != None:
				devise = organisation.devise.designation
				devise_id = organisation.devise_id
			if organisation.commune_quartier_id != None:
				commune_quartier_id = organisation.commune_quartier_id
				commune = dao_place.toGetPlace(commune_quartier_id)
				ville = dao_place.toGetPlace(commune.parent_id)
				ville_id = ville.id
				province = dao_place.toGetPlace(ville.parent_id)
				province_id = province.id
				pays = dao_place.toGetPlace(province.parent_id)
				pays_id = pays.id


		data = {
			"success" : True,
			"message" : "la recuperation des données de la société effectuée avec succès",
			"nom" : nom,
			"email" : email,
			"image" : image,
			"phone" : phone,
			"fax" : fax,
			"numero_fiscal" : numero_fiscal,
			"site_web" : site_web,
			"adresse" : adresse,
			"devise" : devise,
			"devise_id" : devise_id,
			"commune_quartier_id" : commune_quartier_id,
			"pays_id" : pays_id,
			"province_id" : province_id,
			"ville_id" : ville_id,
			"organisation_id" : organisation_id
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("ERREUR get_creer_ouverture_organisation()")
		#print(e)
		data = {
			"success" : False,
			"message" : "Erreur survenue lors de la recuperation des données de la société"
		}
		return JsonResponse(data, safe=False)


@api_view(['POST'])
@transaction.atomic
def post_creer_ouverture_organisation(request):
	sid = transaction.savepoint()
	try:
		#print("post_creer_ouverture_organisation")

		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		auteur = identite.utilisateur(request)
		organisation_id = int(request.POST.get('organisation_id', 0))
		#print("organisation_id {}".format(organisation_id))
		devise_id = int(request.POST.get('devise_id', 0))
		#print("devise_id {}".format(devise_id))
		nom = request.POST.get('nom', None)
		#print("nom {}".format(nom))
		site_web = request.POST.get('site_web', None)
		#print("site_web {}".format(site_web))
		numero_fiscal = request.POST.get('numero_fiscal', None)
		#print("numero_fiscal {}".format(numero_fiscal))
		phone = request.POST.get('phone', None)
		#print("phone {}".format(phone))
		fax = request.POST.get('fax', None)
		#print("fax {}".format(fax))
		email = request.POST.get('email', None)
		#print("email {}".format(email))
		phone = request.POST.get('phone', None)
		#print("phone {}".format(phone))
		adresse = request.POST.get('adresse', None)
		#print("adresse {}".format(adresse))
		commune_quartier_id = int(request.POST.get('commune_quartier_id', 0))
		#print("commune_quartier_id {}".format(commune_quartier_id))
		image = ""
		randomId = randint(111, 999)
		if 'image_upload' in request.FILES:
			file = request.FILES["image_upload"]
			organisation_img_dir = 'organisation/'
			media_dir = media_dir + '/' + organisation_img_dir
			save_path = os.path.join(media_dir, str(randomId) + ".jpg")
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			path = default_storage.save(save_path, file)
			#default_storage.delete(path)
			#On affecte le chemin de l'Image
			image = media_url + organisation_img_dir + str(randomId) + ".jpg"
		else: image = ""
		#print("image {}".format(image))
		organisation = dao_organisation.toCreateOrganisation(image, None, nom, None, None, None, devise_id, commune_quartier_id, adresse, email, phone, site_web, fax, numero_fiscal)
		if organisation_id == 0:
			organisation = dao_organisation.toSaveOrganisation(auteur, organisation)
			dao_organisation.toSetMainOrganisation(organisation.id)
		else: organisation = dao_organisation.toUpdateOrganisation(organisation_id, organisation)
		if organisation == False : raise Exception('organisation non modifie')
		# On met à jour la configuration initiale
		config = dao_config_comptabilite.toCreateConfigComptabilite()
		config = dao_config_comptabilite.toSaveConfigComptabilite(auteur, config)
		dao_config_comptabilite.toSetConfigSocieteConfigure(config.id)
		data = {
			"success" : True,
			"message" : "Mise à jour effectuée avec succès"
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("ERREUR post_creer_ouverture_organisation()")
		#print(e)
		data = {
			"success" : False,
			"message" : "Erreur survenue lors de la mise à jour"
		}
		return JsonResponse(data, safe=False)

def get_creer_ouverture_compte(request):
	# droit="LISTER_COMPTE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 93
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	model = dao_compte.toListComptes()
	context = {
		'title' : 'Ouverture année fiscale',
		'model' : model,
		'isPopup': True,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/ouverture/add.html")
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_ouverture_compte(request):
	sid = transaction.savepoint()
	try:
		#print("post_creer_ouverture_compte")

		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		annee_fiscale = dao_annee_fiscale.toGetAnneeFiscaleActive()
		taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)

		designation = "Ouverture année fiscale"
		reference = 'OUV00' + annee_fiscale.date_debut.strftime('%Y')


		partenaire_id = None
		montant = 0
		description = ""
		journal_id = None
		date_piece = annee_fiscale.date_debut

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation, reference, montant, journal_id, date_piece, partenaire_id, None, None, None, "", devise.id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print(piece_comptable)

		list_compte_id = request.POST.getlist('compte_id', None)
		list_numeros = request.POST.getlist("numero", None)
		list_designations = request.POST.getlist("designation", None)
		list_montants_debit = request.POST.getlist("montant_debit",None)
		list_montants_credit = request.POST.getlist("montant_credit",None)

		#print(len(list_compte_id))
		#print(len(list_numeros))
		#print(len(list_designations))
		#print(len(list_montants_debit))
		#print(len(list_montants_credit))

		montant_test_debit = 0
		montant_test_credit = 0

		for i in range(0, len(list_compte_id)):
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		if montant_test_credit != montant_test_debit:
			messages.error(request,'Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_comptabilite_add_ouverture_compte"))

		for i in range(0, len(list_compte_id)):
			compte_id = int(list_compte_id[i])
			numero = list_numeros[i]
			numero = dao_compte.toGetNumeroCompteArrondi(numero)
			designation = list_designations[i]
			if compte_id == 0:
				compte = dao_compte.toGetCompteDuNumero(numero)
				if compte == None:
					#On crée un nouveau compte comme le compte n'existe pas
					type_compte = dao_type_compte.toGetTypeCompteRecevable()
					permet_reconciliation = False

					compte = dao_compte.toCreateCompte(numero, designation, type_compte.id, permet_reconciliation)
					compte = dao_compte.toSaveCompte(auteur, compte)
				compte_id = compte.id

			libelle = "Solde initial"
			montant_debit = makeFloat(list_montants_debit[i])
			montant_credit = makeFloat(list_montants_credit[i])

			#print("Compte {}".format(compte_id))
			#print("Piece pcomptable {}".format(piece_comptable))

			ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte_id, piece_comptable.id)
			ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
			#print("Ecriture comptable {} cree".format(ecriture_comptable.id))
		# On met à jour la configuration initiale
		config = dao_config_comptabilite.toGetConfigComptabiliteActive()
		dao_config_comptabilite.toSetConfigPeriodeConfigure(config.id)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_details_piece", args=(piece_comptable.id,)))
	except Exception as e:
		#print("ERREUR POST OUVERTURE COMPTABLE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse("module_comptabilite_add_ouverture_compte"))

def get_upload_ouverture_compte(request):
	# droit="LISTER_COMPTE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 93
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Importer un fichier Excel',
		'isPopup': True,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/ouverture/upload.html")
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_upload_ouverture_compte(request):
	sid = transaction.savepoint()
	try:
		#print("upload_ouverture_compte")
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
		devise = dao_devise.toGetDeviseReference()
		annee_fiscale = dao_annee_fiscale.toGetAnneeFiscaleActive()
		taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(devise.id)

		designation = "Ouverture année fiscale"
		reference = 'OUV00' + annee_fiscale.date_debut.strftime('%Y')

		partenaire_id = None
		montant = 0
		description = ""
		journal_id = None
		date_piece = annee_fiscale.date_debut

		piece_comptable = dao_piece_comptable.toCreatePieceComptable(designation, reference, montant, journal_id, date_piece, partenaire_id, None, None, None, "", devise.id)
		if taux != None: piece_comptable.taux_id = taux.id
		piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		#print(piece_comptable)



		montant_test_debit = 0
		montant_test_credit = 0

		for i in df.index:
			#print("montant_debit: {}".format(df['montant_debit'][i]))
			#print("montant_credit: {}".format(df['montant_credit'][i]))
			montant_debit = makeFloat(df['montant_debit'][i])
			montant_credit = makeFloat(df['montant_credit'][i])
			#print("montant_debit: {}".format(montant_debit))
			#print("montant_credit: {}".format(montant_credit))
			montant_test_debit += montant_debit
			montant_test_credit += montant_credit

		#print("montant_test_debit: {}".format(montant_test_debit))
		#print("montant_test_credit: {}".format(montant_test_credit))

		if montant_test_credit != montant_test_debit:
			messages.error(request,'Les écritures saisies ne sont pas équilibrées!')
			return HttpResponseRedirect(reverse("module_comptabilite_add_ouverture_compte"))

		for i in df.index:
			compte_id = int(i)
			numero = str(df['numero'][i])
			numero = dao_compte.toGetNumeroCompteArrondi(numero)
			designation = str(df['designation'][i])
			compte = dao_compte.toGetCompteDuNumero(numero)
			if compte == None:
				#On crée un nouveau compte comme le compte n'existe pas
				type_compte = dao_type_compte.toGetTypeCompteRecevable()
				permet_reconciliation = False

				compte = dao_compte.toCreateCompte(numero, designation, type_compte.id, permet_reconciliation)
				compte = dao_compte.toSaveCompte(auteur, compte)
			compte_id = compte.id

			libelle = "Solde initial"
			montant_debit = makeFloat(df['montant_debit'][i])
			montant_credit = makeFloat(df['montant_credit'][i])
			solde = montant_debit - montant_credit

			#print("Compte Numero {}".format(numero))
			#print("Compte ID {}".format(compte_id))
			#print("Piece pcomptable {}".format(piece_comptable))

			if solde != 0:
				ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(libelle, montant_debit, montant_credit, compte_id, piece_comptable.id)
				ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)
				#print("Ecriture comptable {} cree".format(ecriture_comptable.id))
		# On met à jour la configuration initiale
		config = dao_config_comptabilite.toGetConfigComptabiliteActive()
		dao_config_comptabilite.toSetConfigCompteConfigure(config.id)
		dao_config_comptabilite.toSetConfigComptabiliteAjour(config.id)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_comptabilite_details_piece", args=(piece_comptable.id,)))
	except Exception as e:
		#print("ERREUR POST OUVERTURE COMPTABLE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse("module_comptabilite_upload_ouverture_compte"))

@api_view(['POST'])
@transaction.atomic
def post_creer_ouverture_caisse(request):
	sid = transaction.savepoint()
	try:
		#print("post_creer_ouverture_caisse")
		designation = request.POST.get('designation', None)
		devise_id = request.POST.get('devise_id', None)
		if devise_id == 0:
			devise = dao_devise.toGetDeviseReference()
			devise_id = devise.id
		code_journal = request.POST.get('code_journal', None)
		compte = dao_compte.toGetCompteCaisse()
		compte_id = compte.id
		auteur = identite.utilisateur(request)
		description = None
		responsable_id = None
		compte_debit_id = None
		compte_credit_id = None

		#print("designation : {}".format(designation))
		#print("devise_id : {}".format(devise_id))
		#print("code_journal : {}".format(code_journal))

		#creation du journal
		journal = dao_journal.toCreateJournal(code_journal,designation,4,True,compte_debit_id,compte_credit_id,devise_id)
		journal = dao_journal.toSaveJournal(auteur,journal)
		#print(journal)
		#print(journal.id)

		#Creation de la caisse
		caisse=dao_caisse.toCreateCaisse(designation,description,responsable_id,journal.id, compte_id)
		caisse=dao_caisse.toSaveCaisse(auteur, caisse)
		#print(caisse)
		#print(caisse.journal)
		#print(caisse.journal_id)
		# On met à jour la configuration initiale
		config = dao_config_comptabilite.toGetConfigComptabiliteActive()
		dao_config_comptabilite.toSetConfigTresorerieConfigure(config.id)
		transaction.savepoint_commit(sid)
		data = {
			"success" : True,
			"message" : "Mise à jour effectuée avec succès"
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("ERREUR post_creer_ouverture_caisse()")
		#print(e)
		transaction.savepoint_rollback(sid)
		data = {
			"success" : False,
			"message" : "Erreur survenue lors de la mise à jour"
		}
		return JsonResponse(data, safe=False)

@api_view(['POST'])
@transaction.atomic
def post_creer_ouverture_banque(request):
	sid = transaction.savepoint()
	try:
		#print("post_creer_ouverture_caisse")
		designation = request.POST.get('designation', None)
		banque = request.POST.get('banque', None)
		description = None

		numero_compte = request.POST.get('numero_compte', None)
		type_compte = None

		code_journal = request.POST.get('code_journal', None)
		compte_debit_id = None
		compte_credit_id = None
		devise_id = request.POST.get('devise_id', None)
		if devise_id == 0:
			devise = dao_devise.toGetDeviseReference()
			devise_id = devise.id
		compte_id = dao_compte.toGetCompteBanque()
		auteur = identite.utilisateur(request)

		#creation banque
		banque = dao_banque.toCreateBank(banque)
		banque = dao_banque.toSaveBank(auteur, banque)
		#print(banque)
		#print(banque.id)
		banque_id = banque.id

		#creation du journal
		journal = dao_journal.toCreateJournal(code_journal,designation,3,True,compte_debit_id,compte_credit_id,devise_id)
		journal = dao_journal.toSaveJournal(auteur,journal)
		#print(journal)
		#print(journal.id)

		#creation du compte bancaire
		compte_banque=dao_compte_banque.toCreateCompteBanque(designation,description,numero_compte,type_compte,banque_id,journal.id, compte_debit_id)
		compte_banque=dao_compte_banque.toSaveCompteBanque(auteur, compte_banque)
		#print(compte_banque)
		#print(compte_banque.id)

		# On met à jour la configuration initiale
		config = dao_config_comptabilite.toGetConfigComptabiliteActive()
		dao_config_comptabilite.toSetConfigTresorerieConfigure(config.id)
		transaction.savepoint_commit(sid)
		data = {
			"success" : True,
			"message" : "Mise à jour effectuée avec succès"
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("ERREUR post_creer_ouverture_banque()")
		#print(e)
		transaction.savepoint_rollback(sid)
		data = {
			"success" : False,
			"message" : "Erreur survenue lors de la mise à jour"
		}
		return JsonResponse(data, safe=False)


@api_view(['POST'])
def post_creer_ouverture_annee_fiscale(request):
	try:
		#print("post_creer_ouverture_annee_fiscale")

		observation = request.POST.get('observation', None)
		date_debut = request.POST.get('date_debut', None)
		date_fin_jour = request.POST['date_fin_jour']
		date_fin_mois = request.POST['date_fin_mois']
		date_fin_annee = date_debut[6:10]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = timezone.datetime(int(date_fin_annee), int(date_fin_mois), int(date_fin_jour))
		designation = "Année fiscale " + date_fin_annee
		est_active = False

		auteur = identite.utilisateur(request)

		annee_fiscale = dao_annee_fiscale.toCreateAnnee_fiscale(designation,observation,date_debut,date_fin,est_active)
		annee_fiscale = dao_annee_fiscale.toSaveAnnee_fiscale(auteur, annee_fiscale)
		#print(annee_fiscale)
		#print(annee_fiscale.id)
		dao_annee_fiscale.toSetAnneeFiscaleActive(annee_fiscale.id)

		# On met à jour la configuration initiale
		config = dao_config_comptabilite.toGetConfigComptabiliteActive()
		dao_config_comptabilite.toSetConfigPeriodeConfigure(config.id)
		data = {
			"success" : True,
			"message" : "Mise à jour effectuée avec succès"
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("ERREUR post_creer_ouverture_annee_fiscale()")
		#print(e)
		data = {
			"success" : False,
			"message" : "Erreur survenue lors de la mise à jour"
		}
		return JsonResponse(data, safe=False)

def get_json_list_devises_actives(request):
	try:
		data = []
		devises = dao_devise.toListDevisesActives()
		for devise in devises:
			item = {
				"id" : devise.id,
				"designation" : devise.designation,
				"symbole_devise" : devise.symbole_devise,
				"code_iso" : devise.code_iso
			}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)

def get_analyse_factures(request, ref):
	try:

		# droit="LISTER_JOURNAL"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 89
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		journal = dao_journal.toGetJournal(ref)
		type_journal = dao_type_journal.toGetTypeJournal(journal.type_journal)
		devise = None
		if journal.devise != None: devise = dao_devise.toGetDevise(journal.devise_id)
		compte_credit = None
		if journal.compte_credit != None: compte_credit = dao_compte.toGetCompte(journal.compte_credit_id)
		compte_debit = None
		if journal.compte_debit != None: compte_debit = dao_compte.toGetCompte(journal.compte_debit_id)

		context = {
			"model" : journal,
			"devise" : devise,
			"compte_credit" : compte_credit,
			"compte_debit" : compte_debit,
			"type_journal" : type_journal,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Journal %s" % journal.designation,
			"utilisateur" : utilisateur,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 20
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/facture/analyse.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_lister_journaux"))

def get_cloture_periode(request):
	permission_number = 473
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	Taux = dao_taux_change.toListTauxCourant().count()
	ListeTauxRef = dao_devise.toGetDeviseReference()
	devises = dao_devise.toListDevisesActives()
	ListeDevise = devises.count()
	pays = dao_place.toListPlacesOfType(1)
	journaux = dao_journal.toListJournauxDuDashboard()

	if response != None:
		return response


	context = {
		'title' : 'Clôture période comptable',
		'journaux' : journaux,
		'utilisateur' : utilisateur,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 2,
		'pays' : pays,
		'devises' : devises,
		'actions':auth.toGetActions(modules,utilisateur),
		'Taux':Taux,
		'ListeTauxRef':ListeTauxRef,
		'ListeDevise' : ListeDevise
	}
	template = loader.get_template('ErpProject/ModuleComptabilite/cloture/index.html')
	return HttpResponse(template.render(context, request))


@transaction.atomic
def post_creer_billeterie_operation_budgetaire(request):
	sid = transaction.savepoint()
	try:
		#print("post_creer_billeterie_operation_budgetaire")
		auteur = identite.utilisateur(request)

		operation_tresorerie_id = request.POST["operation_tresorerie_id"]
		operation_tresorerie = dao_operationtresorerie.toGetOperationtresorerie(operation_tresorerie_id)



		list_billet = request.POST.getlist('billet', None)
		list_all_ligne_bille_id = request.POST.getlist('all_ligne_billet_id', None)
		#print('list all', list_all_ligne_bille_id)

		list_ligne_billet_id = request.POST.getlist('ligne_billet_id', None)
		list_valeur = request.POST.getlist('valeur', None)
		list_sous_total = request.POST.getlist('sous_total', None)

		#print('list ligne', list_ligne_billet_id)



		#Test sur le montant global
		somme1 = 0
		somme2 = 0
		for i in range(0, len(list_billet)):
			billet = makeFloat(list_billet[i])
			valeur = makeFloat(list_valeur[i])
			sous_total = makeFloat(list_sous_total[i])
			somme1 += billet * valeur
			somme2 += sous_total

		if somme1 != somme2:
			messages.add_message(request, messages.ERROR, "Les montants ne correspondent pas, veuillez recompter!")
			return HttpResponseRedirect(reverse("module_comptabilite_update_operationtresorerie", args=(operation_tresorerie_id,)))

		if operation_tresorerie.billeterie:
			billeterie = operation_tresorerie.billeterie
		else:
			billeterie = dao_billeterie.toCreateBilleterie(operation_tresorerie.reference, somme1 )
			billeterie = dao_billeterie.toSaveBilleterie(auteur, billeterie)

		#Checking of Update Deletee On ligne if Exist
		for i in range(0, len(list_all_ligne_bille_id)):
			is_find = False
			the_item = list_all_ligne_bille_id[i]
			for j in range(0, len(list_ligne_billet_id)):
				if the_item == list_ligne_billet_id[j]:
					is_find = True
			if is_find == False:
				dao_ligne_billeterie.toDeleteLigneBilleterie(the_item)



		for i in range(0, len(list_billet)):
			billet = makeFloat(list_billet[i])
			valeur = makeFloat(list_valeur[i])
			sous_total = makeFloat(list_sous_total[i])

			ligne_billet_id = int(list_ligne_billet_id[i])

			if ligne_billet_id !=0:
				ligne_billeterie = dao_ligne_billeterie.toCreateLigneBilleterie(billet,valeur,sous_total, billeterie.id)
				dao_ligne_billeterie.toUpdateLigneBilleterie(ligne_billet_id, ligne_billeterie)

			else:
				ligne_billeterie = dao_ligne_billeterie.toCreateLigneBilleterie(billet,valeur,sous_total, billeterie.id)
				ligne_billeterie = dao_ligne_billeterie.toSaveLigneBilleterie(auteur, ligne_billeterie)


		is_update = dao_operationtresorerie.toUpdateSoldeOperationtresorerie(operation_tresorerie_id, somme1, billeterie.id)




		if is_update:
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_comptabilite_update_operationtresorerie", args=(operation_tresorerie_id,)))
			#return HttpResponseRedirect(reverse("module_comptabilite_detail_operationtresorerie", args=(operation_tresorerie_id,)))
		else:
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération, veuillez recommencer!")
			return HttpResponseRedirect(reverse("module_comptabilite_update_operationtresorerie", args=(operation_tresorerie_id,)))


	except Exception as e:
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_caisse"))


def get_json_select_facture(request):
	try:
		facture_id = int(request.GET["ref"])
		facture = dao_facture.toGetFacture(facture_id)

		#print("facture %s" % facture)
		type_facture = ""
		partenaire_id = 0
		partenaire_name = ""
		type_name = ""
		montant_restant = 0

		if facture.client:
			type_facture = 1
			type_name = "Dépôt"
			partenaire_id = facture.client_id
			partenaire_name = facture.client.nom_complet

		elif facture.fournisseur:
			type_facture = 2
			type_name = "Retrait"
			partenaire_id = facture.fournisseur_id
			partenaire_name = facture.fournisseur.nom_complet

		montant_restant = facture.montant_restant

		data = {
			"id" : facture.id,
			"type_id": type_facture,
			"type_name":type_name,
			"partenaire_id":partenaire_id,
			"partenaire_name": partenaire_name,
			"montant_restant": montant_restant,
		}

		#print("fin %s " % data)
		return JsonResponse(data, safe=False)

	except Exception as e:
		#print('ERREUR')
		#print(e)
		return JsonResponse([], safe=False)


def get_rapport_sur_ligne_operation_tresorerie(request):
	try:
		auteur = identite.utilisateur(request)
		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
			#print(' REF %s'%(ref))

			ligne_operation = dao_ligne_operation_tresorerie.toGetLigne_operation_tresorerie(ref)

			if ligne_operation.operation_tresorerie.caisse != None:
				title = "PIECE DE CAISSE"
			elif ligne_operation.operation_tresorerie.compte_banque != None:
				title = "PIECE DE BANQUE"

		context = {
			'title' : title,
			'isPopup':True,
			'ligne_operation':ligne_operation,
			'auteur':auteur,
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/piece_caisse.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'piece_caisse.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('piece_caisse.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response
	except Exception as e:
		#print("ERREUR print PIECE DE CAISSE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_caisse"))

def get_rapport_operationtresorerie(request):
	try:
		# droit='IMPRIMER_OPERATION_TRESORERIE'
		permission_number = 274
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
		#print("ref", ref)

		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		if response != None:
				return response

		model = dao_operationtresorerie.toGetOperationtresorerie(ref)

		ligne_operation = dao_ligne_operation_tresorerie.toListLigneTresorerieofOperation(ref)
		tot_mont=0
		for i in ligne_operation:
			tot_mont += i.montant

		if model.caisse != None:
			objet = model.caisse
			title = "Brouillard de caisse"
			designation = model.caisse.designation
			filter = "caisse"
		elif model.compte_banque != None:
			objet = model.compte_banque
			designation = model.compte_banque.designation
			title = "Relevé bancaire"
			filter = "banque"

		partenaires = dao_personne.toListPersonnes()

		#Teste si tous les lignes de l'objet sont lettré
		est_lettre = True
		for ligne in ligne_operation:
			if ligne.est_lettre == False:
				est_lettre = False

		context = {
			'title' : title,
			'ligne_operation':ligne_operation,
			'objet':objet,
			'est_lettre':est_lettre,
			'designation':designation,
			'filter':filter,
			'isPopup': True,
			'partenaires':partenaires,
			'tot_mont':tot_mont,
			'model':model, 'utilisateur': utilisateur,
			'modules' : modules,'sous_modules': sous_modules,
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/brouillardCaisse.html', context)
		# html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/brouillardDepense.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'brouillard.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('brouillard.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response

		return response
	except Exception as e:
		#print("ERREUR print BROUILLARD")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_caisse"))



def check_json_active_operation_in_poste(request):
	try:
		#print("set_json_cloturecheck_json_active_operation_in_poste_exercice_budgetaire")
		data = []
		poste_id = int(request.GET["poste_id"])
		filter = request.GET["filter"]

		hasGotActiveOne, reference = dao_operationtresorerie.toCheckOperationtresorerieOfPoste(poste_id, filter)

		item = { "hasGotActiveOne":hasGotActiveOne, "reference": reference}
		data.append(item)
		#print("cloture check",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("erreur",e)
		return JsonResponse([], safe=False)



# GRANDS LIVRES OUTPUT PDF
def get_generer_rapport_synthese(request):
	try:
		permission_number = 455
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'title' : 'Générer une synthèse de trésorerie',
			"comptes" : dao_compte.toListComptes(),
			"devises" : dao_devise.toListDevisesActives(),
			"types_compte" : dao_type_compte.toListTypesCompte(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/operationtresorerie/rapport/generate_synthese.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DE GENERER rapport de trésorerie \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur générer rapport de trésorerie ')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))


def post_rapport_pre_synthese(request):
	try:
		permission_number = 455
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		date_debut = request.POST["date_debut"]
		#date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		#date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))

		factures = dao_facture_fournisseur.toListFacturesFournisseurNonSoldees()
		factures_clients = dao_facture_client.toListFacturesClientNonSoldees()
		#print("factu", factures)
		#print("fac client", factures_clients)
		context = {
			'title' : "Dépenses à prevoir",
			'date_debut' : date_debut,
			'date_fin' : date_fin,
			#'type_extraction' : type_extraction,
			'utilisateur' : utilisateur,
			'factures': factures,
			'factures_clients':factures_clients,
			'isPopup': True,
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/rapport/pre_synthese.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE RAPPORT TRESORERIE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_generate_rapport_synthese'))



def post_rapport_synthese(request):
	try:
		permission_number = 455
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#print("**************************************")
		date_debut = request.POST["date_debut"]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		#type_extraction = request.POST["type_extraction"]
		#file_name = "synthese.html"

		depenses = []


		list_libelle = request.POST.getlist('libelle', None)
		list_dette = request.POST.getlist('dette', None)
		list_proposition = request.POST.getlist('proposition', None)

		total_depense_prevue = 0

		for i in range(0, len(list_libelle)) :
			unedepense = {
			'libelle':'',
			'dette':0,
			'proposition':0,
			'solde':0
			}
			unedepense['libelle'] = list_libelle[i]
			unedepense['dette'] = list_dette [i]
			unedepense['proposition'] = list_proposition[i]
			total_depense_prevue += makeFloat(list_proposition[i])
			unedepense['solde'] = makeFloat(list_dette[i]) - makeFloat(list_proposition[i])

			depenses.append(unedepense)


		recettes = []


		list_libelle_client = request.POST.getlist('client_libelle', None)
		list_creance = request.POST.getlist('creance', None)
		list_proposition_client = request.POST.getlist('client_proposition', None)

		total_recette_prevue = 0

		for i in range(0, len(list_libelle_client)) :
			unerecette = {
			'libelle':'',
			'creance':0,
			'proposition':0,
			'solde':0
			}
			unerecette['libelle'] = list_libelle_client[i]
			unerecette['creance'] = list_creance [i]
			unerecette['proposition'] = list_proposition_client[i]
			total_recette_prevue += makeFloat(list_proposition_client[i])
			unerecette['solde'] = makeFloat(list_creance[i]) - makeFloat(list_proposition_client[i])

			recettes.append(unerecette)

		total_avoir = 0

		banques = dao_banque.toListBankSoldeOfPeriode(date_debut, date_fin)
		#print("banques",banques)


		caisses = dao_caisse.toListCaisseSoldeOfPeriode(date_debut, date_fin)
		#print("caisse", caisses)
		#print("depenses", depenses)

		for banque in banques:
			total_avoir += banque['solde']
		for caisse in caisses:
			total_avoir += caisse['solde']

		total_avoir_apres_depense = total_avoir - total_depense_prevue
		total_avoir_apres_recette_et_depense = total_avoir_apres_depense + total_recette_prevue



		#end = endpoint.reportingEndPoint()

		context = {
			'title' : "Synthèse de trésorerie",
			'date_debut' : date_debut,
			'date_fin' : date_fin,
			'banques':banques,
			'caisses':caisses,
			'depenses':depenses,
			'recettes':recettes,
			'total_avoir':total_avoir,
			'total_depense_prevue':total_depense_prevue,
			'total_recette_prevue': total_recette_prevue,
			'total_avoir_apres_depense':total_avoir_apres_depense,
			'total_avoir_apres_recette_et_depense':total_avoir_apres_recette_et_depense,
			#'type_extraction' : type_extraction,
			'utilisateur' : utilisateur,
			'isPopup': True,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4,'modules' : modules,'sous_modules': sous_modules,
		}
		template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/rapport/synthese.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE RAPPORT TRESORERIE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_generate_rapport_synthese'))


# GRANDS LIVRES OUTPUT PDF
def get_generer_rapport_rapprochement(request):
	try:
		permission_number = 453
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'title' : 'Générer un rapprochement bancaire',
			"comptes" : dao_compte_banque.toListCompteBanque(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/operationtresorerie/rapport/generate_rapprochement.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DE GENERER rapport de trésorerie \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur générer rapport de trésorerie ')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))


def post_rapport_rapprochement(request):
	try:
		# droit="CREER_RAPPORT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 453
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#print("back again ***********************")

		date_debut = request.POST["date_debut"]
		#print("date debut", date_debut)
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		compte_banque_id = request.POST["compte_banque_id"]
		compte_banque = dao_compte_banque.toGetCompteBanque(compte_banque_id)

		tableauLignes, tableauLettres = dao_ligne_operation_tresorerie.toListLignesRapprochementBancaire(compte_banque_id, date_debut, date_fin)
		#print("tab lig", tableauLignes)
		#print("tab letr", tableauLettres)

		est_printable = False
		if 'is_printable' in request.POST:
			est_printable = True

		sommeCreditLigne = 0
		sommedebitLigne = 0
		for item in tableauLignes:
			# print('****Ligne Credit', item['credit'])
			# print('****Ligne Debit', item['debit'])
			sommeCreditLigne += item['credit']
			sommedebitLigne += item['debit']

		soldeLigne = int(sommeCreditLigne) - int(sommedebitLigne)

		sommeCreditEcriture = 0
		sommeDeditEcriture = 0
		for item in tableauLettres:
			# print('****Ecriture Credit', item['credit'])
			# print('****Ecriture Debit', item['debit'])
			sommeCreditEcriture += item['credit']
			sommeDeditEcriture += item['debit']

		soldeEcriture = int(sommeCreditEcriture) - int(sommeDeditEcriture)

		# print('Date Debut', request.POST["date_debut"])
		# print('Date Fin', request.POST["date_fin"])



		context = {
			'title' : 'RAPPROCHEMENT BANCAIRE',
			'compte_banque':compte_banque,
			'tableauLignes':tableauLignes,
			'tableauLettres':tableauLettres,
			'isPopup': True,
			# 'date_debut' : date_debut,
			# 'date_fin' : date_fin,

			'date_debut' :request.POST["date_debut"],
			'date_fin' : request.POST["date_fin"],
			'compte_banque_id' : request.POST["compte_banque_id"],

			#'type_extraction' : type_extraction,
			'utilisateur' : utilisateur,
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4,
			'soldeEcriture':soldeEcriture,
			'sommeCreditEcriture':sommeCreditEcriture,
			'sommeDeditEcriture':sommeDeditEcriture,

			'soldeLigne':soldeLigne,
			'sommeCreditLigne':sommeCreditLigne,
			'sommedebitLigne':sommedebitLigne,
		}
		template = loader.get_template('ErpProject/ModuleComptabilite/operationtresorerie/rapport/rapprochement.html')
		if not est_printable:
			return HttpResponse(template.render(context, request))
		else:
			# pdf = render_to_pdf('ErpProject/ModuleComptabilite/operationtresorerie/rapport/rapprochement_print.html', context, request)
			return weasy_print("ErpProject/ModuleComptabilite/operationtresorerie/rapport/rapprochement_print.html", "Rapprochement.pdf", context)
			# return HttpResponse(pdf, content_type='application/pdf')
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE RAPPORT TRESORERIE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_generate_rapport_rapprochement'))

def print_rapport_rapprochement_bancaire(request):
	try:
		# droit="CREER_RAPPORT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 453
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#print("back again ***********************")

		date_debut = request.POST["date_debut"]
		#print("date debut", date_debut)
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		compte_banque_id = request.POST["compte_banque_id"]
		compte_banque = dao_compte_banque.toGetCompteBanque(compte_banque_id)

		tableauLignes, tableauLettres = dao_ligne_operation_tresorerie.toListLignesRapprochementBancaire(compte_banque_id, date_debut, date_fin)
		#print("tab lig", tableauLignes)
		#print("tab letr", tableauLettres)

		est_printable = False
		if 'is_printable' in request.POST:
			est_printable = True

		sommeCreditLigne = 0
		sommedebitLigne = 0
		for item in tableauLignes:
			# print('****Ligne Credit', item['credit'])
			# print('****Ligne Debit', item['debit'])
			sommeCreditLigne += item.credit
			sommedebitLigne += item.debit

		soldeLigne = int(sommeCreditLigne) - int(sommedebitLigne)

		sommeCreditEcriture = 0
		sommeDeditEcriture = 0
		for item in tableauLettres:
			# print('****Ecriture Credit', item['credit'])
			# print('****Ecriture Debit', item['debit'])
			sommeCreditEcriture += item.credit
			sommeDeditEcriture += item.debit

		soldeEcriture = int(sommeCreditEcriture) - int(sommeDeditEcriture)




		context = {
			'title' : 'RAPPROCHEMENT BANCAIRE',
			'compte_banque':compte_banque,
			'tableauLignes':tableauLignes,
			'tableauLettres':tableauLettres,
			'isPopup': True,
			'date_debut' : date_debut,
			'date_fin' : date_fin,

			'date_debut' :request.POST["date_debut"],
			'date_fin' : request.POST["date_fin"],
			'compte_banque_id' : request.POST["compte_banque_id"],

			#'type_extraction' : type_extraction,
			'utilisateur' : utilisateur,
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_COMPTABILITE,
			'menu' : 4,

			'soldeEcriture':soldeEcriture,
			'sommeCreditEcriture':sommeCreditEcriture,
			'sommeDeditEcriture':sommeDeditEcriture,

			'soldeLigne':soldeLigne,
			'sommeCreditLigne':sommeCreditLigne,
			'sommedebitLigne':sommedebitLigne,
		}
		return weasy_print("ErpProject/ModuleComptabilite/operationtresorerie/rapport/rapprochement_print.html", "Rapprochement.pdf", context)
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE RAPPORT TRESORERIE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_generate_rapport_rapprochement'))





#COMPTE ANALYTIQUE = CENTRE COUT
def get_lister_compte_analytique(request):
	# droit='LISTER_COMPTE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 357
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	# model = dao_centre_cout.toListCentre_cout()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_centre_cout.toListCentre_cout(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste de comptes analytiques',
		'model' : model,
		'view': view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/compte_analytique/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_compte_analytique(request):
	# droit='CREER_COMPTE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 356
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	centre_cout = dao_centre_cout.toListCentreCoutOfTypeView()
	groupes = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Ajouter un compte analytique','centre_cout':centre_cout, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'groupes':groupes,'modules' : modules,'sous_modules': sous_modules,
	'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/compte_analytique/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_compte_analytique(request):

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
			date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()

			date_fin = request.POST["date_fin"]
			date_fin = date_fin[6:10] + '-' + date_fin[3:5] + '-' + date_fin[0:2]
			date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()


		if centre_cout_id == "":
			centre_cout_id = None
		auteur = identite.utilisateur(request)

		centre_cout=dao_centre_cout.toCreateCentre_cout(designation,code,type_centre,abbreviation,centre_cout_id, groupe_analytique_id)
		centre_cout=dao_centre_cout.toSaveCentre_cout(auteur, centre_cout)
		centre_cout.date_debut = date_debut
		centre_cout.date_fin = date_fin
		centre_cout.save()
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_compte_analytique',args=(centre_cout.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_compte_analytique'))


def get_details_compte_analytique(request,ref):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 357
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

		template = loader.get_template('ErpProject/ModuleComptabilite/compte_analytique/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,centre_cout)


		context ={'title' : centre_cout.designation + ' : Détails','compte_analytique' : centre_cout,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'montant_alloue':montant_alloue,
		'montant_consomme':montant_consomme,
		'ligne_budgetaire':lignes,
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_compte_analytique'))
def get_modifier_compte_analytique(request,ref):
	# droit='MODIFIER_COMPTE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 358
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ref = int(ref)
	model = dao_centre_cout.toGetCentre_cout(ref)
	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	centre_cout = dao_centre_cout.toListCentre_cout()
	context ={'title' : 'Modifier le compte analytique','model':model, 'utilisateur': utilisateur,
	'groupe_analytique':groupe_analytique,
	'centre_cout':centre_cout,'modules' : modules,'sous_modules': sous_modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/compte_analytique/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_compte_analytique(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		code = request.POST['code']
		centre_cout_id = request.POST['centre_cout_id']
		abbreviation = request.POST['abbreviation']
		type_centre = request.POST['type_centre']
		groupe_analytique_id = request.POST['groupe_analytique_id']

		auteur = identite.utilisateur(request)

		centre_cout=dao_centre_cout.toCreateCentre_cout(designation,code,type_centre, abbreviation,centre_cout_id, groupe_analytique_id)
		centre_cout=dao_centre_cout.toUpdateCentre_cout(id, centre_cout)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_compte_analytique',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_centre_cout'))

def get_details_ecriture_analytique_of_compte_analytique(request, ref):
	try:
		# droit="LISTER_COMPTE_ANALYTIQUE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 274
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
			return HttpResponseRedirect(reverse('module_comptabilite_list_compte_analytique'))

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





		balance = montant_alloue + produit + charge
		if montant_alloue > 0:
			pourcentage = 100 * makeFloat(montant_consomme) / makeFloat(montant_alloue)
		else:
			pourcentage = 0

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,centre_cout)


		context ={
		'title' : 'Ecritures analytiques du compte analytique',
		'centre_cout':centre_cout,
		'utilisateur' : utilisateur,
		'charge': abs(charge),
		'produit': produit,
		'montant_alloue': montant_alloue,
		'pourcentage' : pourcentage,
		'balance': balance,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'devise': devise,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'ecritures_analytiques':ecritures_analytiques,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleComptabilite/compte_analytique/ecriture_analytique/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleComptabilite'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR DETAILLER Ecriture")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_compte_analytique'))


def get_lister_groupeanalytique(request):
	permission_number = 456
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	# model = dao_groupeanalytique.toListGroupeanalytique()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_groupeanalytique.toListGroupeanalytique(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des groupes analytiques',
		'model' : model,
		'view': view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/groupe_analytique/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_groupeanalytique(request):
	permission_number = 457
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Ajouter un groupe analytique','utilisateur' : utilisateur,
	'groupe_analytique':groupe_analytique,
	'isPopup': True if 'isPopup' in request.GET else False,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/groupe_analytique/add.html')
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

		return HttpResponseRedirect(reverse('module_comptabilite_detail_groupeanalytique',args=(groupeanalytique.id, ))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_groupeanalytique'))


def get_details_groupeanalytique(request,ref):
	permission_number = 456
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		groupeanalytique=dao_groupeanalytique.toGetGroupeanalytique(ref)
		template = loader.get_template('ErpProject/ModuleComptabilite/groupe_analytique/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,groupeanalytique)


		context ={'title' : 'Détails sur un groupe analytique','groupeanalytique' : groupeanalytique,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4,
		'modules' : modules,'sous_modules': sous_modules}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_groupeanalytique'))
def get_modifier_groupeanalytique(request,ref):
	permission_number = 457
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_groupeanalytique.toGetGroupeanalytique(ref)
	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Modifier un groupe analytique','model':model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'groupe_analytique':groupe_analytique,'modules' : modules,'sous_modules': sous_modules,
	'utilisateur': utilisateur,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/groupe_analytique/update.html')
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
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_groupeanalytique',args=(groupeanalytique.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_groupeanalytique'))



def get_lister_ordre_paiement(request):
	# droit='LISTER_ORDRE_PAIEMENT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 361
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	# model = dao_ordre_paiement.toListOrdre_paiement()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_ordre_paiement.toListOrdre_paiement(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	#Traitement des vues
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)

	context ={
		'title' : 'Liste des demandes de paiement',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : model,
		'view': view,
		'utilisateur' : utilisateur,
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_COMPTABILITE,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleComptabilite/ordre_paiement/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_ordre_paiement(request):
	# droit='CREER_ORDRE_PAIEMENT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 360
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	context ={'title' : 'Ajouter une demande de paiement',
	'factures': dao_facture_fournisseur.toListFacturesNonSoldees(),
	'partenaires':dao_personne.toListPersonnes(),
	'compte_banques':dao_compte_banque.toListCompteBanque(),
	'caisses': dao_caisse.toListCaisse(),
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/ordre_paiement/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_ordre_paiement(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_echeance"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		compte_banque_id = None
		caisse_id = None
		devise_id = None
		type_paiement = int(request.POST['type_paiement'])

		if type_paiement == 1:
			compte_banque_id = request.POST["compte_banque_id"]
			compte = dao_compte_banque.toGetCompteBanque(compte_banque_id)
			devise_id = compte.journal.devise_id

		elif type_paiement == 2:
			caisse_id = request.POST["caisse_id"]
			caisse = dao_caisse.toGetCaisse(caisse_id)
			devise_id = caisse.journal.devise_id
		reference = request.POST['reference']


		date_echeance = request.POST['date_echeance']
		date_echeance = timezone.datetime(int(date_echeance[6:10]), int(date_echeance[3:5]), int(date_echeance[0:2]))
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		ordre_paiement=dao_ordre_paiement.toCreateOrdre_paiement(reference,type_paiement,date_echeance,compte_banque_id,caisse_id,description)
		ordre_paiement=dao_ordre_paiement.toSaveOrdre_paiement(auteur, ordre_paiement)


		list_libelle = request.POST.getlist('libelle', None)
		list_partenaire = request.POST.getlist('partenaire', None)
		list_facture = request.POST.getlist('facture', None)
		list_montant = request.POST.getlist('montant', None)
		list_observation = request.POST.getlist('observation', None)

		for i in range (0, len(list_libelle)):
			libelle = list_libelle[i]
			partenaire_id = list_partenaire[i]
			if partenaire_id == "":
				partenaire_id = None
			facture_id = list_facture[i]
			if facture_id == "":
				facture_id = None
			montant = list_montant[i]
			observation = list_observation[i]

			ligne_ordre_paiement = dao_ligne_ordre_paiement.toCreateLigne_ordre_paiement(libelle,partenaire_id,facture_id,montant, devise_id,observation, ordre_paiement.id)
			ligne_ordre_paiement = dao_ligne_ordre_paiement.toSaveLigne_ordre_paiement(auteur, ligne_ordre_paiement)

			ligne_ordre_paiement.save()

		#Initialisation Wkf
		wkf_task.initializeWorkflow(auteur,ordre_paiement)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_ordre_paiement',args=(ordre_paiement.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER ORDRE_PAIEMENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_ordre_paiement'))


def get_details_ordre_paiement(request,ref):
	# droit='LISTER_ORDRE_PAIEMENT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 361
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		ordre_paiement=dao_ordre_paiement.toGetOrdre_paiement(ref)

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,ordre_paiement)

		template = loader.get_template('ErpProject/ModuleComptabilite/ordre_paiement/item.html')
		context ={'title' : 'Demande de paiement N° ' + ordre_paiement.reference,
		'lignes': dao_ligne_ordre_paiement.toListLigneOfOrdrePaiement(ref),
		'historique' : historique,
		'etapes_suivantes' : transition_etape_suivant,
		'signee' : signee,
		'content_type_id':content_type_id,
		'roles':groupe_permissions,
		'modules' : modules,'sous_modules': sous_modules,
		'documents':documents,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model' : ordre_paiement,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS ORDRE_PAIEMENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_ordre_paiement'))
def get_modifier_ordre_paiement(request,ref):
	# droit='MODIFIER_ORDRE_PAIEMENT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 362
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_ordre_paiement.toGetOrdre_paiement(ref)
	context ={'title' : 'Modifier une demande de paiement','modules' : modules,'sous_modules': sous_modules,
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'module' : ErpModule.MODULE_COMPTABILITE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleComptabilite/ordre_paiement/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_ordre_paiement(request):

	id = int(request.POST['ref'])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_echeance"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		reference = request.POST['reference']
		type_paiement = request.POST['type_paiement']
		date_echeance = request.POST['date_echeance']
		compte_banque_id = request.POST['compte_banque_id']
		caisse_id = request.POST['caisse_id']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		ordre_paiement=dao_ordre_paiement.toCreateOrdre_paiement(reference,type_paiement,date_echeance,compte_banque_id,caisse_id,description)
		ordre_paiement=dao_ordre_paiement.toUpdateOrdre_paiement(id, ordre_paiement)
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_list_ordre_paiement',args=(id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER ORDRE_PAIEMENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_comptabilite_add_ordre_paiement'))



def get_creer_paiement_of_ordre_paiement(request):
	# droit="CREER_OPERATION_TRESORERIE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 275
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ordre_paiement = None
	lignes = None
	etape_id = None
	reference = ""
	operations = None

	try:
		etat_actuel_id = request.POST["doc_id"]
		#print("etat_actuel", etat_actuel_id)
		ordre_paiement = dao_ordre_paiement.toGetOrdre_paiement(etat_actuel_id)
		#print("unos")
		if ordre_paiement.compte_banque:
			#print("tertio")
			operations = dao_operationtresorerie.toListOperationOfBanqueNonCloture(ordre_paiement.compte_banque_id)
		elif ordre_paiement.caisse:
			#print("quarto")
			operations = dao_operationtresorerie.toListOperationOfCaisseNonCloture(ordre_paiement.caisse_id)
		reference = ordre_paiement.reference
		lignes = dao_ligne_ordre_paiement.toListLigneOfOrdrePaiement(etat_actuel_id)
		etape_wkf_id = request.POST["etape_id"]
		#etat_besoins = dao_expression_besoin.toListExpressionsServiceReferent()
	except Exception as e:
		#print("Aucun etat de besoin trouvé")
		messages.error(request,'Aucune opération de tresorerie en cours disponible pour le compte/caisse choisi. Veuillez en ouvrir une!' )

	context = {
		'title' : 'Paiement de la demande N° ' + reference,
		'ordre_paiement':ordre_paiement,
		'lignes':lignes,
		'etape_id':etape_id,
		"utilisateur" : utilisateur,
		'operations':operations,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_COMPTABILITE,
		'menu' : 25
	}
	template = loader.get_template("ErpProject/ModuleComptabilite/ordre_paiement/paiement/add.html")
	return HttpResponse(template.render(context, request))


@transaction.atomic
def post_creer_paiement_of_ordre_paiement(request):
	sid = transaction.savepoint()
	ordre_paiement_id = request.POST['ordre_paiement_id']
	try:
		ordre_paiement = dao_ordre_paiement.toGetOrdre_paiement(ordre_paiement_id)
		date_operation = request.POST['date_operation']
		date_operation = timezone.datetime(int(date_operation[6:10]), int(date_operation[3:5]), int(date_operation[0:2]))

		operation_tresorerie_id = request.POST['operation_tresorerie_id']
		operationtresorerie = dao_operationtresorerie.toGetOperationtresorerie(operation_tresorerie_id)
		devise_id = operationtresorerie.devise_id
		devise = dao_devise.toGetDevise(devise_id)
		journal = dao_journal.toGetJournal(operationtresorerie.journal_id)
		journal_id = journal.id
		taux_id = None

		if ordre_paiement.compte_banque:
			objet_id = ordre_paiement.compte_banque_id
		elif ordre_paiement.caisse:
			objet_id = ordre_paiement.caisse_id


		auteur = identite.utilisateur(request)

		list_libelle = request.POST.getlist('libelle', None)
		list_partenaire = request.POST.getlist('partenaire', None)
		list_type_operation_ligne = request.POST.getlist('type_operation_ligne', None)
		list_montant = request.POST.getlist('montant', None)
		list_facture = request.POST.getlist('facture', None)
		list_motif = request.POST.getlist('motif', None)


		for i in range(0, len(list_libelle)):
			#print("you've win")
			date_ligne_operation = date_operation
			libelle = list_libelle[i]
			partenaire_id = list_partenaire[i]
			if partenaire_id == "":
				partenaire_id = None
			facture_id = list_facture[i]
			if facture_id == "":
				facture_id = None
			type_operation_ligne = list_type_operation_ligne[i]
			montant = list_montant[i]
			motif = list_motif[i]

			#print("youve win2")
			ligne_operation = dao_ligne_operation_tresorerie.toCreateLigne_operation_tresorerie(operationtresorerie.reference,libelle,partenaire_id,montant,devise_id,taux_id,type_operation_ligne, motif,operationtresorerie.id,date_ligne_operation)
			ligne_operation = dao_ligne_operation_tresorerie.toSaveLigne_operation_tresorerie(auteur,ligne_operation)
			ligne_id = ligne_operation.id
			#print("youve win3")

			##################################################ENREGISTREMENT PAIEMENT###################

			ligne_operation = dao_ligne_operation_tresorerie.toGetLigne_operation_tresorerie(ligne_id)
			#print("ligne op",ligne_operation)
			if facture_id and not ligne_operation.est_lettre:
				#print("you've win4")
				facture = dao_facture.toGetFacture(facture_id)
				#print("nakatii oooooh")
				if type_operation_ligne == '2':
					#print("apa ",type_operation_ligne)
					partenaire = dao_fournisseur.toGetFournisseur(partenaire_id)
					compte_partenaire = dao_compte.toGetCompteFournisseur()
				elif type_operation_ligne == '1' :
					#print('lidia',type_operation_ligne)
					partenaire = dao_client.toGetClient(partenaire_id)
					compte_partenaire = dao_compte.toGetCompteClient()
				#On enregistre la transaction
				statut_transaction = dao_statut_transaction.toGetStatutSuccess()
				transaction_paiement = dao_transaction.toCreateTransaction(facture_id, statut_transaction["id"], 1)
				transaction_paiement = dao_transaction.toSaveTransaction(auteur, transaction_paiement)
				transaction_paiement_id = transaction_paiement.id
				#print('transaction cree avec id {}'.format(transaction_paiement_id))

				# On enregistre le paiement
				paiement = dao_paiement.toCreatePaiement(transaction_paiement_id, date_ligne_operation, facture_id, devise_id, montant, 1, journal_id , partenaire_id , auteur.id, libelle, motif)
				#print(paiement)
				paiement = dao_paiement.toSavePaiement(paiement)
				#print('paiement cree avec id {}'.format(paiement.id))
				if paiement :
					#print("paiement exist")
					paiement.est_lettre = True
					#print("paiement exist")
					paiement.est_valide = True
					#print("paiement exist")
					paiement.ligne_operation_tresorerie_id = ligne_operation.id
					#print("paiement exist")
					paiement.save()
					#print("paiement exist")
					ligne_operation.paiement_id = paiement.id
					#print("paiement exist")
					ligne_operation.facture_id = facture_id
					ligne_operation.est_lettre = True
					ligne_operation.save()
					#print("paiement exist")


				#print("montant", montant)
				#print("montant restat", facture.separateur_montant_restant)
				#print("montant", facture.montant)
				montant_restant = dao_facture.toGetMontantRestantOfPaymentFacture(facture_id)
				#print("montant_restant t", montant_restant)


				if makeFloat(montant) > makeFloat(montant_restant):
					transaction.savepoint_rollback(sid)
					messages.error(request,'La ligne sur laquelle la facture est renseignée fait l\'objet d\'un montant supérieur à ce qui reste !' )
					return HttpResponseRedirect(reverse('module_comptabilite_add_operationtresorerie', args=(objet_id,type_operation_ligne,)))
				elif makeFloat(montant) == makeFloat(montant_restant):
					#print("moses ", montant_restant)
					facture.est_soldee = True
					facture.save()
					#print("************ fzcture payee")

				#print("2222 ", montant_restant)


				#On enregistre le payloads (Informations supplémentaires et utile pour le paiement)

				logs = "{'journal':'%s', 'montant':'%s', 'devise':'%s' }" % (journal.designation, montant, devise.designation)
				payloads = dao_payloads.toCreatePayloads(paiement.id, logs)
				dao_payloads.toSavePayloads(payloads)
				#print('payloads cree avec id {}'.format(dao_payloads.id))

				# ECRITURES COMPTABLES DUES AU PAIEMENT DU FOURNISSEUR
				#Ici On débite le compte de trésorerie
				date_piece = timezone.now()
				compte_tresorerie = journal.compte_debit

				piece_comptable = dao_piece_comptable.toCreatePieceComptable(paiement.designation, "", montant, journal_id, date_ligne_operation, partenaire_id, None, None, facture_id, "PAIEMENT FOURNISSEUR", devise.id, taux_id)
				piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
				#print('piece cree avec id {}'.format(piece_comptable.id))


				#print('dev ',devise.id)
				#print('dev ',partenaire)

				if partenaire.compte != None: compte_partenaire = dao_compte.toGetCompte(partenaire.compte_id)


				#print('dev ',partenaire)

				if type_operation_ligne == '2':

					ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, montant, 0, objet_id, piece_comptable.id, facture.lettrage_id)
					ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
					#print('here we are')
					#print('ecriture credit cree avec id {}'.format(ecriture_credit.id))

					ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(partenaire.nom_complet, 0, montant, compte_partenaire.id, piece_comptable.id, facture.lettrage_id)
					ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
					#print('ecriture debit cree avec id {}'.format(ecriture_debit.id))

				elif type_operation_ligne == '1' :

					ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(journal.designation, 0, montant, compte_partenaire.id, piece_comptable.id, facture.lettrage_id)
					ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
					#print('here we are')
					#print('ecriture credit cree avec id {}'.format(ecriture_debit.id))


					ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(partenaire.nom_complet, montant, 0, objet_id, piece_comptable.id, facture.lettrage_id)
					ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
					#print('ecriture debit cree avec id {}'.format(ecriture_credit.id))

			##################################################ENREGISTREMENT PAIEMENT###################

		#Passing step wkf
		wkf_task.passingStepWorkflow(auteur,ordre_paiement)
		#print("goood lastA")

		transaction.savepoint_commit(sid)
		#print("goood last2")
		#messages.SUCCESS(request,'Paiement enregistrées!' )
		#messages.add_message(request, messages.SUCCESS, 'Paiement enregistrées!')
		#print("goood last3")
		messages.add_message(request, messages.SUCCESS, "Opération effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_comptabilite_detail_ordre_paiement',args=(ordre_paiement_id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER PAIEMENT OF ORDRE DE PAIEMENT\n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR,e)
		return HttpResponseRedirect(reverse('module_comptabilite_detail_ordre_paiement', args=(ordre_paiement_id,)))


#GESTION DES NOTES ANNEXES
# def post_generer_note_annexe(request):
#     	try:
# 		# droit="GENERER_GRANDLIVRE"
# 		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
# 		permission_number = 98
# 		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

# 		if response != None:
# 			return response

# 		context = post_traiter_grand_livre(request, utilisateur, modules, sous_modules)

# 		template = loader.get_template("ErpProject/ModuleComptabilite/livre/generated.html")
# 		return HttpResponse(template.render(context, request))
# 	except Exception as e:
# 		messages.add_message(request, messages.ERROR, e)
# 		messages.error(request,e)
# 		return HttpResponseRedirect(reverse("module_comptabilite_generer_grand_livre"))

def get_details_note_annexe_1(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 1'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe1.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


def post_imprimer_cas_1(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 1'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote1.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote1.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe1.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe1.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 2
def get_details_note_annexe_2(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 2'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe2.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_grand_livre"))


def post_imprimer_cas_2(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 2'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote2.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote2.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe2.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe2.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 3
def get_details_note_annexe_3(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 3'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe3.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


def post_imprimer_cas_3(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 3'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote3A.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote3A.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe3.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe3.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 3B
def get_details_note_annexe_3B(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 3B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe3B.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_3B(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 3B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote3B.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote3B.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe3B.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe3B.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 3C
def get_details_note_annexe_3C(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 3C'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe3C.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_3C(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 3C'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote3C.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote3C.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe3C.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe3C.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 3D
def get_details_note_annexe_3D(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 3D'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe3D.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_3D(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 3D'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote3D.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote3D.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe3D.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe3D.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 3E
def get_details_note_annexe_3E(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 3E'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe3E.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_3E(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 3E'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote3E.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote3E.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe3E.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe3E.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 4
def get_details_note_annexe_4(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 4'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe4.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_4(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 4'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote4.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote4.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe4.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe4.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 5
def get_details_note_annexe_5(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 5'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe5.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_5(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 5'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote5.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote5.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe5.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe5.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 6
def get_details_note_annexe_6(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 6'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe6.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_6(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 6'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote6.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote6.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe6.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe6.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 7
def get_details_note_annexe_7(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 7'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe7.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_7(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 7'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote7.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote7.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe7.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe7.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 8
def get_details_note_annexe_8(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 8'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe8.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_8(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 8'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote8.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote8.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe8.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe8.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 9
def get_details_note_annexe_9(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 9'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe9.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_9(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 9'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote9.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote9.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe9.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe9.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 10
def get_details_note_annexe_10(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 10'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe10.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_10(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 10'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote10.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote10.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe10.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe10.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 11
def get_details_note_annexe_11(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 11'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe11.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_11(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 11'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote11.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote11.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe11.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe11.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 12
def get_details_note_annexe_12(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 12'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe12.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_12(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 12'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote12.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote12.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe12.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe12.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 13
def get_details_note_annexe_13(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 13'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe13.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_13(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 13'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote13.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote13.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe13.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe13.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 14
def get_details_note_annexe_14(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 14'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe14.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_14(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 14'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote14.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote14.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe14.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe14.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 15
def get_details_note_annexe_15(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 15'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe15A.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_15(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 15'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote15A.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote15A.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe15A.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe15a.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 15B
def get_details_note_annexe_15B(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 15B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe15B.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_15B(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 15B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote15B.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote15B.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe15B.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe15B.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 16A
def get_details_note_annexe_16A(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 16A'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe16A.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_16A(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 16A'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote16A.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote16A.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe16A.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe16A.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 16B
def get_details_note_annexe_16B(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 16B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe16B.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_16B(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 16B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote16B.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote16B.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe16B.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe16B.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 16C
def get_details_note_annexe_16C(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 16C'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe16C.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_16C(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 16C'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote16C.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote16C.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe16C.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe16C.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 17
def get_details_note_annexe_17(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 17'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe17.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_17(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 17'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote17.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote17.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe17.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe17.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 18
def get_details_note_annexe_18(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 18'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe18.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_18(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 18'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote18.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote18.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe18.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe18.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 19
def get_details_note_annexe_19(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 19'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe19.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_19(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 19'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote19.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote19.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe19.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe19.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 20
def get_details_note_annexe_20(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 20'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe20.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_20(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 20'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote20.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote20.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe20.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe20.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 21
def get_details_note_annexe_21(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 21'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe21.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_21(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 21'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote21.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote21.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe21.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe21.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 22
def get_details_note_annexe_22(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 22'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe22.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_22(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 22'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote22.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote22.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe22.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe22.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 23
def get_details_note_annexe_23(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 23'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe23.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_23(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 23'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote23.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote23.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe23.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe23.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 24
def get_details_note_annexe_24(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 24'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe24.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_24(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 24'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote24.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote24.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe24.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe24.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 25
def get_details_note_annexe_25(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 25'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe25.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_25(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 25'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote25.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote25.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe25.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe25.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 26
def get_details_note_annexe_26(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 26'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe26.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_26(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 26'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote26.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote26.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe26.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe26.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 27A
def get_details_note_annexe_27(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 27'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe27.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_27(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 27'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote27.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote27.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe27.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe27.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 27B
def get_details_note_annexe_27B(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 27B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe27B.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_27B(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 27B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote27B.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote27B.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe27B.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe27B.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 27B
def get_details_note_annexe_27B(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 27B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe27B.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_27B(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 27B'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote27B.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote27B.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe27B.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe27B.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 28
def get_details_note_annexe_28(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 28'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe28.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_28(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 28'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote28.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote28.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe28.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe28.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 29
def get_details_note_annexe_29(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 29'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe29.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_29(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 29'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote29.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote29.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe29.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe29.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 30
def get_details_note_annexe_30(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 30'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe30.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_30(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 30'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote30.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote30.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe30.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe30.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 31
def get_details_note_annexe_31(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 31'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe31.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_31(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 31'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote31.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote31.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe31.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe31.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 32
def get_details_note_annexe_32(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 32'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe32.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_32(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 32'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote32.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote32.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe32.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe32.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 33
def get_details_note_annexe_33(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 33'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe33.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_33(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 33'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote33.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote33.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe33.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe33.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 34
def get_details_note_annexe_34(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 34'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe34.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_34(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 34'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote34.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote34.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe34.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe34.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))


#NOTE 35
def get_details_note_annexe_35(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 35'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe35.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_35(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 35'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote35.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote35.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe35.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe35.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

#NOTE 36
def get_details_note_annexe_36(request):
	try:
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		title = 'Note Annexe 36'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		template = loader.get_template("ErpProject/ModuleComptabilite/note_annexe_resultat/noteannexe36.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))

def post_imprimer_cas_36(request):
	try:
		# droit="IMPRIMER_GRANDLIVRE"
		# print('-------A SAVOIR--------')
		permission_number = 98
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		title = 'Note Annexe 36'
		context = {
			'title' : title,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_COMPTABILITE,
			'menu' : 25
		}
		html_string = render_to_string('ErpProject/ModuleComptabilite/reporting/HTML/grand_livrenote36.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'printnote36.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'note_annexe36.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('note_annexe36.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response
		return response

	except Exception as e:
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_generer_annexe"))
