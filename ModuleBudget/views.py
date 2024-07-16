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
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.utils.wkf_task import wkf_task
import os
import datetime
import json
from django.db import transaction
from ErpBackOffice.utils.separateur import AfficheEntier
# Import ErpBackOffice.models
from ErpBackOffice.models import * #Model_Unite_fonctionnelle, Model_Budget, Model_Employe, Model_Image
from ModuleBudget.dao.dao_centre_cout import dao_centre_cout
from ModuleBudget.dao.dao_groupeanalytique import dao_groupeanalytique

from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ModuleBudget.dao.dao_categoriebudget import dao_categoriebudget
from ModuleComptabilite.dao.dao_ecriture_analytique import dao_ecriture_analytique
from ErpBackOffice.utils.pagination import pagination
from ModuleBudget.dao.dao_exercicebudgetaire import dao_exercicebudgetaire

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

from ModuleBudget.dao.dao_type_transaction_budgetaire import dao_type_transaction_budgetaire
from ErpBackOffice.utils.endpoint import endpoint
from ErpBackOffice.utils.print import weasy_print
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
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
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation


# Import from ModuleRessourcesHumaines
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleRessourcesHumaines.views import get_prets_a_recuperer
from ModuleRessourcesHumaines.views import get_allocations_a_payer
from ModuleRessourcesHumaines.dao.dao_pret import dao_pret
from ModuleRessourcesHumaines.dao.dao_conge import dao_conge
from ModuleRessourcesHumaines.dao.dao_lot_bulletin import dao_lot_bulletin
from ModuleRessourcesHumaines.dao.dao_bulletin import dao_bulletin
from ModuleRessourcesHumaines.dao.dao_item_bulletin import dao_item_bulletin
from ModuleRessourcesHumaines.dao.dao_type_unite_fonctionnelle import dao_type_unite_fonctionnelle

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
from ModuleBudget.dao.dao_nature_charge import dao_nature_charge
from ModuleBudget.dao.dao_nature_ligne import dao_nature_ligne
from ModuleBudget.dao.dao_localite import dao_localite
from ModuleBudget.dao.dao_type_budget import dao_type_budget
from ModuleBudget.dao.dao_type_entite import dao_type_entite
from ModuleBudget.dao.dao_type_ligne_budgetaire import dao_type_ligne_budgetaite

from ErpBackOffice import models
from ModuleBudget import serializer
from rest_framework import viewsets


from ModuleBudget.dao.dao_activite import dao_activite
from ModuleBudget.dao.dao_ligne_poste_budgetaire import dao_ligne_poste_budgetaire
from ModuleBudget.dao.dao_poste_budgetaire import dao_poste_budgetaire
from ModuleBudget.dao.dao_dashbord import dao_dashbord

#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module = "ModuleBudget"
var_module_id = 6

# Tableau de board
def get_tableau_de_bord(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(17, request)
	if response != None:
		return response

	#WAY OF NOTIFCATION
	module_name = "MODULE_BUDGET"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()
	#print("way")
	#print(temp_notif_count)
	# ListeTransaction = dao_transactionbudgetaire.toListTransactionbudgetaireOfAnneeActive()
	# nombre_transaction=dao_transactionbudgetaire.toListTransactionbudgetaireOfAnneeActive().count()
	# nombre_centre_cout = dao_centre_cout.toListCentre_cout().count()
	combinaison = dao_ligne_budgetaire.toListLigneBudgetaires()
	#print("way")
	Recette = dao_budget.toListBudgetRecettes().count()
	# Depenses=dao_budget.toListBudgetDepenses().count()
	#print("way")
	# ExerciceBudgtaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
	#print("way")
	#END WAY
	#SOLDE ALL PROJETS
	modelProjet = dao_projet.toListProjet()
	#print("way4")
	somme_total = 0
	ladevise = ""
	for item in modelProjet:
		somme_total = somme_total + item.montant
		ladevise = item.devise.symbole_devise
	somme_total = str(AfficheEntier(float(somme_total)))+ " "+ ladevise
	# categorie_budget = dao_categoriebudget.toListCategoriebudget()

	solde=dao_budget.toListBudget()
	soldeToT=0.0
	for item in solde:
		soldeToT +=item.solde
		ladevise = item.devise.symbole_devise


	#print('categorie budget bord %s' % (categorie_budget))
	mois,values, nbrebc = dao_dashbord.toGetLastBCMonth()
	bcvalide,lesjours,lesvaleurs = dao_dashbord.toGetCBValide()
	periode, bcvalidecount, bnv= dao_dashbord.toGetLastpassebyMonth()
	sommeExp, sommeRec, sommeIn, sommeGl, listbudget= dao_dashbord.toGetBudgetGlobal()
	# testfonct = dao_dashbord.toGetBudgetInfogeneral()
	transactlabel,transactvalue = dao_dashbord.toGetTransactionbymonth()
	# datatet = dao_dashbord.toGetCompareCBwithBR()
	#print("way5")

	#Calcul par type de budet
	# calcul_recette = dao_budget.toComputeBudget(1)
	# calcul_depense = dao_budget.toComputeBudget(2)
	# calcul_projet = dao_centre_cout.toComputeProjet()
	# list_categorie = dao_categoriebudget.toComputeBudgetByCategorie()

	#print("calcul projet", calcul_projet)
	# centre = dao_centre_cout.toListCentre_cout()
	bccommende = dao_bon_reception.toListBonReception()
	# print('bon commande', bccommende)
	groupe_permission = dao_groupe_permission.toGetGroupePermissionDeLaPersonne(utilisateur.id)
	if groupe_permission != None:
		if groupe_permission.designation == 'Chef de service SBA':
			template = loader.get_template('ErpProject/ModuleBudget/dashboardsba.html')
		else:
			template = loader.get_template('ErpProject/ModuleBudget/dashboard.html')
	else:
		# template = loader.get_template('ErpProject/ModuleBudget/dashboardAss.html')
		# template = loader.get_template('ErpProject/ModuleBudget/dashboard.html')
		template = loader.get_template('ErpProject/ModuleBudget/dashboardsba.html')



	#*****************Begin of Clean Object for Dashboard*************
	budget_recette = dao_type_budget.toGetTypeBudgetRecette() #All need of recette
	budget_depense = dao_type_budget.toGetTypeBudgetDepense() #All need of depense

	testMostLB = dao_dashbord.toGetMostUseLineBudgetaire()
	mostLingeused = dao_dashbord.toGetMostLigneUsed()
	lastcontrat = dao_dashbord.lastcontrat()
	lettreCommande = dao_dashbord.lastlettreCommande()
	bcall= dao_dashbord.CountBC()
	bcwork = int(bcall) - int(bcvalide)

	# print('****BC NON VALIDE', bnv)


	#send_mail_test()
	context ={
		'title' : 'Tableau de Bord',
		'budget_recette': budget_recette,
		'budget_depense': budget_depense,
		'sous_modules':sous_modules,
		'temp_notif_count':temp_notif_count,
		'temp_notif_list':temp_notif_list,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 2,
		'isAdmin': auth.toCheckAdmin("Budget", utilisateur),
		'Recette':Recette,
		'solde':AfficheEntier(soldeToT),
		'combinaison': combinaison[:10],
		'ladevise':ladevise,'bccommandes':bccommende[:10],
		'mois':mois,'values':values, 'nbrebc':nbrebc,'bcvalide':bcvalide,'lesjours':lesjours,'lesvaleurs':lesvaleurs,'periode':periode,'bcvalidecount':bcvalidecount,'bnv':bnv,
		'sommeExp':AfficheEntier(sommeExp), 'sommeRec':sommeRec, 'sommeIn':sommeIn, 'sommeGl':sommeGl,'listbudget':listbudget,'ligneused':dao_dashbord.toGetligneUsed()[:10],
		'transactlabel':transactlabel,'transactvalue':transactvalue,'testMostLB':testMostLB[:3],'mostLingeused':mostLingeused[:5],'lastcontrat':lastcontrat,'lettreCommande': lettreCommande,'GetlistProjets':dao_dashbord.GetlistProjets(),
		'Contrat':dao_dashbord.SoldeContrat(),'projets':dao_dashbord.SoldeProjet(),'CountBC':dao_dashbord.CountBC(),'bcwork': bcwork,'bcR':dao_dashbord.totalBCRapproche()
	}
	# template = loader.get_template('ErpProject/ModuleBudget/index.html')
	# template = loader.get_template('ErpProject/ModuleBudget/dashboardsba.html')
	return HttpResponse(template.render(context, request))


def get_update_notification(request,ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	return get_tableau_de_bord(request)

# BUDGET CONTROLLERS
def get_lister_budget(request):
	# droit = "LISTER_BUDGET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 142
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	model = None
	type = request.GET.get("list","")

	if type == "1":
		# model = dao_budget.toListBudgetRecettes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_budget.toListBudgetRecettes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		title = "Budget Recette: Liste des sous-catégories"
	elif type == "2":
		# model = dao_budget.toListBudgetDepenses()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_budget.toListBudgetDepenses(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		title = "Budget Dépense: Liste des sous-catégories"
	else:
		# model = dao_budget.toListBudget()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_budget.toListBudget(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		title = "Liste des budgets"

	somme_total = 0
	ladevise = ""
	for item in model:
		somme_total = somme_total + item.solde
		ladevise = item.devise.symbole_devise

	somme_total = str(somme_total)

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)


	context ={
		'title' : title,
		'model' : model,
		"somme_total":AfficheEntier(makeFloat(somme_total)),
		"ladevise":ladevise,
		'view' : view,
		"type": type,
		'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'responsable':dao_employe.toListEmployes(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26
	}
	template = loader.get_template('ErpProject/ModuleBudget/budget/list.html')
	return HttpResponse(template.render(context, request))

# Ce Modele se transformeà la creation du groupement budgetaire qui regroupement l'ensemble des combinaisons budgetaire.
def get_creer_budget(request):
	try:
		# droit="CREER_BUDGET"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 141
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		model = dao_budget.toListBudget()
		type = request.GET.get("type","")
		categorie_budget = dao_categoriebudget.toListCategoriebudget()
		if type == "1":
			title  = "Ajouter un regroupement budgetaire"
		else:
			title = "Ajouter un regroupement budgetaire"
		context = {
			'title' : title,
			'model' : model,
			'type_budget': type,
			'categorie_budget': categorie_budget,
			'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'responsable':dao_employe.toListEmployes(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_BUDGET,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleBudget/budget/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer Budget\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_budget'))


def get_details_budget(request, ref):
	try:
		# droit="LISTER_BUDGET"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 142
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		model = dao_budget.toGetBudget(ref)
		type = request.GET.get("type","")
		ligne_budgetaire = dao_ligne_budgetaire.toListLigneOfBudgets(model.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'title' : 'Budget {}'.format(model.designation),
			'model' : model,
			'ligne_budgetaire': ligne_budgetaire,
			'type_budget': type,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_BUDGET,
			'menu' : 26
		}
		#print(' module %s' % (ErpModule.MODULE_BUDGET))
		template = loader.get_template('ErpProject/ModuleBudget/budget/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details Budget\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_budget'))


def post_creer_budget(request):
	# type_budget = request.POST["type_budget"]
	try:
		"""Premièrement, on crée d'abord un budget. """

		#print("on cherche type_budget", request.POST)
		designation = request.POST["designation_budget"]
		categoriebudget_id = int(request.POST["categoriebudget_id"])
		devise_id = request.POST['devise_id']

		typebudget = dao_categoriebudget.toGetTypecategorieBudgetbyid(categoriebudget_id)
		# print('TYPE BUDGET', typebudget)
		# print('AUTEUR', identite.utilisateur(request))

		budget = dao_budget.toCreateBudget(designation, categoriebudget_id,devise_id )
		budget = dao_budget.toSaveBudget(identite.utilisateur(request), budget)
		# print('**BUDGET', budget)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_budget_detail_budget", args=(budget.id,)) + "?type=" + str(typebudget))
		# return HttpResponseRedirect(reverse("module_budget_list_regroupement_b"))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer Budget\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_budget') + "?type=" + typebudget)

def get_modifier_budget(request, ref):
	try:
		# droit="MODIFIER_BUDGET"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 143
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		#print('etp 1')
		if response != None:
			return response

		ref = int(ref)
		model = dao_budget.toGetBudget(ref)
		ligne_budgetaire = dao_ligne_budgetaire.toListLigneOfBudgets(model.id)

		#print('budget %s'%(model.designation))
		#print('budget model %s'%(model ))

		#print('unite_fonctionnelle %s'%( dao_unite_fonctionnelle.toListUniteFonctionnelle() ))

		#print('responsable %s'%(dao_employe.toListEmployes()))

		#print('ligne_budgetaire %s'%(ligne_budgetaire))

		#print('modules %s'%(modules))

		#print(' module %s' % (ErpModule.MODULE_BUDGET))

		context ={
		'title' : 'Budget {}'.format(model.designation),
		'model' : model,
		'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
		'responsable':dao_employe.toListEmployes(),
		'ligne_budgetaire' : ligne_budgetaire,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleBudget/budget/update.html')
		#print('Template %s'%(template))
		return HttpResponse(template.render(context, request))

	except Exception as e:
		#print('erreur specifique %s'%(e))
		monLog.error("{} :: {}::\nErreur lors de Get Modifier Budget\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_budget'))

#@transaction.atomic
def post_modifier_budget(request):
	#print('methode touché')
	#sid = transaction.savepoint()
	ref = int(request.POST["ref"])
	try:
		#transaction.savepoint_commit(sid)
		"""Premièrement, on crée d'abord un budget. """

		designation = request.POST["designation_budget"]
		devise_id  = request.POST['devise']

		categoriebudget_id = request.POST["categoriebudget_id"]
		#budget = dao_budget.toCreateBudget(designation, annee, date_debut, date_fin, solde, devise_id=devise_id)
		budget = dao_budget.toCreateBudget(designation,categoriebudget_id, devise_id)

		budget = dao_budget.toUpdateBudget(ref, budget)

		if budget == False:
			raise  Exception()
		return HttpResponseRedirect(reverse("module_budget_detail_budget", args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier Budget\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_budget'))


#REGROUPEMENT BUDGETAIRE
def get_lister_regroupement_lignebudgetaire(request):
	permission_number = 1010
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	
	if response != None:
		return response

	model = Model_GroupementCombinaisonB.objects.all()		
	model = dao_model.toListModel(model, permission_number, groupe_permissions, identite.utilisateur(request))
	# print('GROUPE', model)
	title = "Liste des regroupements Budgétaires"
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	#Pagination
	model = pagination.toGet(request, model)
	context ={
		'title' : title,
		'model' : model,
		'view' : view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'responsable':dao_employe.toListEmployes(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26
	}
	template = loader.get_template('ErpProject/ModuleBudget/regroupement_LigneB/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_regroupement_lignebudgetaire(request):
	try:
		permission_number = 1011
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		categorie_budget = dao_categoriebudget.toListCategoriebudget()
		lignes           = dao_ligne_budgetaire.toListLigneBudgetaires()

		title = "Ajouter un regroupement ligne budgetaire"
		context = {
			'title' : title,
			'categorie_budget': categorie_budget,
			'lignes': lignes,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'responsable':dao_employe.toListEmployes(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_BUDGET,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleBudget/regroupement_LigneB/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer Regroupement Ligne Budgetaire\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		print('Erreur lors de Get Creer Ligne Budgetaire')
		print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_lister_regroupement_lignebudgetaire'))

def get_list_combinaison_b(request):
	try:
		# print("*********")
		id = int(request.GET["ref"])
		exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		data = []
		lignes = Model_LigneBudgetaire.objects.filter(budget__categoriebudget__id = id, exericebudgetaires__id = exercice.id)
		print("lignes", lignes)
		for ligne in lignes:
			item = {
			"id": ligne.id,
			"code" : ligne.code,
			}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		# print('ERREUR GETTING DATA JSON')
		# print(e)
		return JsonResponse([], safe=False) 


@transaction.atomic
def post_creer_regroupement_ligne_budgetaire(request):
	sid = transaction.savepoint()
	try:
		transaction.savepoint_commit(sid)
		auteur = identite.utilisateur(request)
		code = request.POST["code"]
		designation = request.POST["designation"]
		lignebugetaire = request.POST["lignebugetaire"]
		categorie = int(request.POST["categorie"])

		regroupement = Model_GroupementCombinaisonB()
		regroupement.code = code
		regroupement.designation = designation
		regroupement.categoriebudget_id = categorie
		regroupement.save()
	
		lignebugetaire_id = request.POST.getlist("lignebugetaire", None)
		for i in range(0, len(lignebugetaire_id)):
			regroupement.lignebudgetaire.add(dao_ligne_budgetaire.toGetLigneBudgetaire(lignebugetaire_id[i]))

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_lister_regroupement_lignebudgetaire'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE POST REGROUPEMENT LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print("ERREUR POST CREER LIGNE BUDGETAIRE")
		print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_creer_regroupement_lignebudgetaire'))

def get_details_groupement_ligne_budget(request, ref):
	try:
		# droit="LISTER_BUDGET"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 1010
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		model = Model_GroupementCombinaisonB.objects.get(pk = ref)
		# type = request.GET.get("type","")
		# ligne_budgetaire = dao_ligne_budgetaire.toListLigneOfBudgets(model.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'title' : 'Budget {}'.format(model.designation),
			'model' : model,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_BUDGET,
			'menu' : 26
		}
		#print(' module %s' % (ErpModule.MODULE_BUDGET))
		template = loader.get_template('ErpProject/ModuleBudget/regroupement_LigneB/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details Budget\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_lister_regroupement_lignebudgetaire'))

def get_delete_groupement_ligne_budget(request, ref):
	try:
		# droit="LISTER_BUDGET"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 1010
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = Model_GroupementCombinaisonB.objects.get(pk = ref)
		model.delete()
		return HttpResponseRedirect(reverse('module_budget_lister_regroupement_lignebudgetaire'))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Delete Groupement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail Budget')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_lister_regroupement_lignebudgetaire'))

# LIGNE BUDGETAIRE CONTROLLERS

def get_lister_ligne_budgetaire(request):
	try:
		# droit="LISTER_COMBINAISON"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 146
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		# model = dao_ligne_budgetaire.toListLigneBudgetaires()
		#*******Filtre sur les règles **********#
		# model = dao_model.toListModel(dao_ligne_budgetaire.toListLigneBudgetaires(), permission_number, groupe_permissions, identite.utilisateur(request))
		model = dao_model.toListModel(dao_ligne_budgetaire.toListLigneBudgetairesofExeciceEncours(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		# normale = dao_ligne_budgetaire.toListLigneBudgetairesofExeciceEncours()

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context ={
		'title' : 'Liste des Combinaisons budgétaires',
		'model' : model,
		'view' : view,
		'responsable': dao_employe.toListEmployes(),
		'budget': dao_budget.toListBudget(),
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR LISTER LIGNE BUDGETAIRE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_budget_tableau_de_bord"))

def get_creer_ligne_budgetaire(request):
	try:
		# droit="CREER_COMBINAISON"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 145
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		model = dao_ligne_budgetaire.toListLigneBudgetaires()


		context = {
		'title' : 'Nouvelle Combinaison Budgétaire',
		'model' : model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'responsable':dao_employe.toListEmployes(),
		'budget': dao_budget.toListBudget(),
		'isPopup': True if 'isPopup' in request.GET else False,
		'comptes': dao_compte.toListComptes(),
		'activites': dao_activite.toListActivite(),
		'projets': dao_projet.toListProjet(),
		'natureactivites': dao_nature_activite.toListNatureActivites(),
		'naturecharges': dao_nature_charge.toListNatureCharges(),
		'naturelignes': dao_nature_ligne.toListNatureLigneBgts(),
		'localites': dao_localite.toListLocalites(),
		'typebudgets': dao_type_budget.toListTypeBudgets(),
		'typeentites': dao_type_entite.toListTypeEntites(),
		'centres': dao_centre_cout.toListCentreCoutOfTypeAccount(),
		'types' : dao_type_ligne_budgetaite.toListTypesLignesBudgetaire(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR CREER LIGNE BUDGETAIRE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))

def get_detail_ligne_budgetaire_without_bc(request):
	try:
		permission_number = 146
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return None
		# ref = int(ref)
		model = dao_transactionbudgetaire.toListTransactionSansBC()
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)
		context ={
			'title' : 'Transactions Budgetaire',
			'model' : model,
			'utilisateur' : utilisateur,
			'view' : view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_BUDGET,
			'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/transact_bc_null.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER TRANSACTION BC NULL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print("ERREUR DETAILLER TRANSACTION BC NULL")
		print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_tableau_de_bord'))


def get_details_ligne_budgetaire(request, ref):
	try:
	# droit="LISTER_COMBINAISON"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 146
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return None

		ref = int(ref)
		model = dao_ligne_budgetaire.toGetLigneBudgetaire(ref)
		# print('***model***', model)
		exercice_active = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		# valeur = dao_ligne_budgetaire.toComputeValeur(model.id)
		employes = dao_employe.toListEmployeOfClassificationByDepartementCode("SBA", "CHEFSER")
		# print("******** exercice_active", exercice_active)
		transactions = dao_transactionbudgetaire.toListOfCombinaisonOfAnneeActive(model.id)
		# print('transactions:', transactions)
		context ={
		'title' : 'Ligne Budgétaire {}'.format(model.designation),
		'model' : model,
		'utilisateur' : utilisateur,
		'employes': employes,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'exercice_budgetaire':exercice_active,
		'modules' : modules,'sous_modules': sous_modules,
		'transactions' : transactions,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print("ERREUR DETAILLER LIGNE BUDGETAIRE")
		print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))


@transaction.atomic
def post_creer_ligne_budgetaire(request):
	sid = transaction.savepoint()
	try:
		"Enregistrons une ligne budgétaire tout d'abord en sauvergardant l'état de la base de données"
		transaction.savepoint_commit(sid)

		#Enregistrons er creons le poste budgetaire associé



		auteur = identite.utilisateur(request)
		code = request.POST["code"]
		#print(code)
		entite = request.POST["entite"]
		nature_activite = int(request.POST["nature_activite"])

		entite_demanderesse = request.POST["entite_demanderesse"] #Centre de cout
		activite_id = int(request.POST["activite"])
		nature_charge = request.POST["nature_charge"]
		localite = int(request.POST["localite"])
		montant_dotation = request.POST["montant_dotation"]
		nom_projet = request.POST["nom_projet"]
		nom_active = request.POST["nom_activite"]
		type = int(request.POST["type"])
		compte_id = int(request.POST["compte"])
		# print(f"**DATA SEND {nom_projet} : ")
		# print('type', type)
		# print("{} {} ", format(nature_activite,entite_demanderesse))
		# print("{} ", format(activite_id))
		# print("{} {} ", format(montant_dotation))
		# print("{} {} ", format(nom_projet, nom_active))
		# print("{} {} ", format(type, compte_id))
		# print("{} {}",format(nature_charge,localite))

		if "compte_id" in request.POST :
			find = dao_ligne_budgetaire.toCheckCompteComptable(compte_id)
			if find:
				messages.error(request,'Le compte comptable saisi est déjà utilisé ')
				transaction.savepoint_rollback(sid)
				return HttpResponseRedirect(reverse("module_budget_add_ligne_budgetaire"))

		solde = 0

		budget_id = int(request.POST["budget"])
		pourcentage_alert = makeFloat(request.POST["pourcentage_alert"])
		message_alert = request.POST["message_alert"]
		isPopup = request.POST["isPopup"]


		is_bloqued = False
		if "is_bloqued" in request.POST : is_bloqued = True

		if type == 1:
			cpte = dao_compte.toGetCompte(compte_id)
			designation = cpte.designation
		elif type == 2:
			designation = nom_projet
			compte_id = None 
		elif type == 3:
			designation = nom_active
			compte_id = None 

		# print('DESIGNATION', designation)
		exercice_id = None
		exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		if exercice: exercice_id = exercice.id

		ligne_budgetaire = dao_ligne_budgetaire.toCreateLigneBudgetaire(code, designation, budget_id, None, entite, compte_id, nature_activite, entite_demanderesse, activite_id, nature_charge, localite, pourcentage_alert, message_alert, type, is_bloqued)
		ligne_budgetaire = dao_ligne_budgetaire.toSaveLigneBudgetaire(auteur, ligne_budgetaire)
		ligne_budgetaire.exericebudgetaires_id = exercice_id
		url = '<a class="lien chargement-au-click" href="/budget/ligne_budgetaire/item/'+ str(ligne_budgetaire.id) +'/">'+ ligne_budgetaire.designation + '</a>'
		ligne_budgetaire.url = url
		ligne_budgetaire.save()

		if "responsable_id" in request.POST :
			responsable_id = request.POST.getlist("responsable_id", None)
			for i in range(0, len(responsable_id)):
				ligne_budgetaire.correspondant.add(dao_personne.toGetPersonne(responsable_id[i]))

		#Creation de la transaction
		#On crée la transaction
		#Mais avant, test sur le montant est different de 0
		#print("dot", montant_dotation)
		if montant_dotation == "":
			montant_dotation = 0
		if makeFloat(montant_dotation) > 0:
			#test sur l'existence d'un exercice budgétaire en cours ou pas
			exercice_budgetaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
			if exercice_budgetaire:
				devise = dao_devise.toGetDeviseReference()
				type_transaction = 4
				statut_transaction = 2
				transactionbudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire("Dotation de la ligne ",makeFloat(montant_dotation),"",devise.id,ligne_budgetaire.compte_id,auteur.id, ligne_budgetaire.id, type_transaction, statut_transaction)
				transactionbudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionbudgetaire)
				#print('transaction creee avec id {}'.format(transactionbudgetaire.id))
			else:
				messages.error(request,"Echec: Aucun exercice en cours d'éxécution, le montant de la dotation ne pourra être affecté, indiquez 0 à la place")
				transaction.savepoint_rollback(sid)
				return HttpResponseRedirect(reverse('module_budget_add_ligne_budgetaire'))



		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_ligne_budgetaire', args=(ligne_budgetaire.id,))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print("ERREUR POST CREER LIGNE BUDGETAIRE")
		print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))


def get_modifier_ligne_budgetaire(request, ref):
	try:
		# droit="MODIFIER_COMBINAISON"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 147
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response !=None:
			return response

		ref = int(ref)
		model = dao_ligne_budgetaire.toGetLigneBudgetaire(ref)
		context ={
		'title' : 'Ligne Budgétaire {}'.format(model.designation),
		'model' : model,
		'responsable': dao_employe.toListEmployes(),
		'budget': dao_budget.toListBudget(),
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR MODIFIER LIGNE BUDGETAIRE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))

def post_modifier_ligne_budgetaire(request):
	sid = transaction.savepoint()
	ref = int(request.POST["ref"])
	try:
		"Enregistrons une ligne budgétaire tout d'abord en sauvergardant l'état de la base de données"

		code = request.POST["code"]
		responsable = request.POST["responsable"]
		designation = request.POST["designation"]
		solde = request.POST["solde"]
		budget = request.POST["budget"]

		ligne_budgetaire = dao_ligne_budgetaire.toCreateLigneBudgetaire(code, designation, budget, responsable, solde)
		ligne_budgetaire = dao_ligne_budgetaire.toUpdateLigneBudgetaire(ref, ligne_budgetaire)

		return HttpResponseRedirect(reverse('module_budget_details_ligne_budgetaire', args=(ref,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR POST MODIFIER LIGNE BUDGETAIRE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))

def get_upload_ligne_budgetaire(request):
	try:
		permission_number = 146
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des combinaisons budgétaires",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_BUDGET,
			'menu' : 27
		}
		template = loader.get_template("ErpProject/ModuleBudget/ligne_budgetaire/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD PIECE COMPTABLE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_budget_list_ligne_budgetaire"))


# def post_bloque_combinaison_b(request):
#     try:
# 		print("")
# 		# id = int(request.GET["ref"])
# 		# id = int(request.GET["ref"])
# 		# statut = request.GET["statut"]
# 		# model = dao_ligne_budgetaire.toGetLigneBudgetaire(id)
# 		# model.is_bloqued = statut
# 		# model.save()
# 		# data = {
# 		# 	"message" : "Success!",
# 		# }
# 		return JsonResponse(data, safe=False)
#     except Exception as e:
# 		print('ERREUR GETTING DATA JSON')
# 		print(e)
# 		return JsonResponse([], safe=False)


#Quelques fonctions spécifiques ramenant une double validation pour le deblocage
#d'une ligne budgetaire
def post_bloque_combinaison_b(request):
	id = int(request.GET["ref"])
	statut = request.GET["statut"]
	model = dao_ligne_budgetaire.toGetLigneBudgetaire(id)
	if statut == "1": model.is_bloqued = not model.is_bloqued
	elif statut == "0": model.is_bloqued = model.is_bloqued
	model.is_waiting_confirmation = False
	model.user_confirmation = None
	model.save()
	data = {
		"message" : "Success!"
	}
	return JsonResponse(data, safe=False)

def post_initiate_blocus_status_change(request):
	combinaison_id = request.POST["combinaison_id"]
	try:
		employe_id = request.POST["employe_id"]
		dao_ligne_budgetaire.toSetUserConfirmationOfBlocusLigneBudgetaire(combinaison_id, employe_id)
		return get_details_ligne_budgetaire(request, combinaison_id)
	except Exception as e:
		return get_details_ligne_budgetaire(request, combinaison_id)


# EXTRATION BUDGETAIRE
def get_generer_analyse_budgetaire(request):
	try:
		permission_number = 149
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
			"module" : ErpModule.MODULE_BUDGET,
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleBudget/rapport/generate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e, reverse("module_budget_tableau_de_bord"))

def post_traiter_analyse_budgetaire(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_BUDGET):
	'''fonction de traitement de calcul pour extraction d'un diplôme'''
	#On recupère et format les inputs reçus
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	ExerciceB = int(request.POST["exercice_bgt"])
	typeExtraction = int(request.POST["type_extraction"])
	Combine = []
	LignesBudgetaire = []
	transac = ''
	# print('**CONFIRMATION FUNCTION**')

	if typeExtraction == 1: #Budget type recette
		Ligne = models.Model_LigneBudgetaire.objects.filter(creation_date__range = [date_debut, date_fin]).filter(budget__categoriebudget__type = 1).order_by("-creation_date")
		# print('1****Extraction Recette', Ligne)
		for item in Ligne:
			transac = dao_ligne_budgetaire.toSendTransactionB(ExerciceB, item)
			for ele in transac:
				if ele.ligne_budgetaire.id not in Combine:
					Combine.append(ele.ligne_budgetaire.id)
		# print('2****Combinaison Extraire', Combine)
		for item in Combine:
			laligne = dao_ligne_budgetaire.toGetLigneBudgetaire(item)
			LignesBudgetaire.append(laligne)

		# model = LignesBudgetaire

	if typeExtraction == 2: #Budget type Depense
		Ligne = models.Model_LigneBudgetaire.objects.filter(creation_date__range = [date_debut, date_fin]).filter(budget__categoriebudget__type = 2).order_by("-creation_date")
		# print('3****Combinaison Extraire', Combine)
		for item in Ligne:
			transac = dao_ligne_budgetaire.toSendTransactionB(ExerciceB, item)
			for ele in transac:
				if ele.ligne_budgetaire.id not in Combine:
					Combine.append(ele.ligne_budgetaire.id)

		for item in Combine:
			laligne = dao_ligne_budgetaire.toGetLigneBudgetaire(item)
			LignesBudgetaire.append(laligne)

		# model = LignesBudgetaire

	if typeExtraction == 3:#Combinaison budgétaire(Projet)
		Ligne = models.Model_LigneBudgetaire.objects.filter(creation_date__range = [date_debut, date_fin]).filter(type = 2).order_by("-creation_date")
		# print('4****Combinaison Extraire', Combine)
		for item in Ligne:
			transac = dao_ligne_budgetaire.toSendTransactionB(ExerciceB, item)
			for ele in transac:
				if ele.ligne_budgetaire.id not in Combine:
					Combine.append(ele.ligne_budgetaire.id)

		for item in Combine:
			laligne = dao_ligne_budgetaire.toGetLigneBudgetaire(item)
			LignesBudgetaire.append(laligne)

		# model = LignesBudgetaire


	if typeExtraction == 4: #Transactions
		transactions = models.Model_Transactionbudgetaire.objects.filter(exercice_budgetaire__id=ExerciceB)
		model = LignesBudgetaire

	#On récupère les données suivant le filtre défini
	# model = dao_ligne_budgetaire.toListLigneBudgetaires()
	# model = models.Model_LigneBudgetaire.objects.filter(creation_date__range = [date_debut, date_fin]).order_by("-creation_date")

	context = {
		'title' : "Analyse budgétaire",
		"model" : LignesBudgetaire,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7,
		'transactions': transac,
		'typeExtraction':typeExtraction,
		'ExerciceB': ExerciceB
	}
	return context

def post_generer_analyse_budgetaire(request):
	try:
		permission_number = 149
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		print("Limite 0")

		if response != None:
			return response

		context = post_traiter_analyse_budgetaire(request, utilisateur, modules, sous_modules)
		print("Limite 1")
		template = loader.get_template("ErpProject/ModuleBudget/rapport/generated.html")
		print("Limite 1")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def post_imprimer_analyse_budgetaire(request):
	try:
		permission_number = 149
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_analyse_budgetaire(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleBudget/reporting/analyse_budgetaire.html", "analyse_budgetaire.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

# EXTRATION LIGNE BUDGETAIRE
def get_generer_analyse_ligne_budgetaire(request):
	try:
		permission_number = 149
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		context = {
			'title' : 'Générer une analyse de la ligne budgetaire',
			"comptes" : dao_compte.toListComptes(),
			"devises" : dao_devise.toListDevisesActives(),
			"types_compte" : dao_type_compte.toListTypesCompte(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'exercices': dao_exercicebudgetaire.toListExercicebudgetaire(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_BUDGET,
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleBudget/rapport/ligne_generate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e, reverse("module_budget_tableau_de_bord"))

def post_traiter_analyse_ligne_budgetaire(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_RESSOURCES_HUMAINES):
	'''fonction de traitement de calcul pour extraction d'un diplôme'''
	#On recupère et format les inputs reçus
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)

	#On récupère les données suivant le filtre défini
	model = dao_ligne_budgetaire.toListLigneBudgetaires()
	model = models.Model_LigneBudgetaire.objects.filter(creation_date__range = [date_debut, date_fin]).order_by("-creation_date")

	context = {
		'title' : "Analyse Ligne budgétaire",
		"model" : model,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
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

def post_generer_analyse_ligne_budgetaire(request):
	try:
		permission_number = 149
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_analyse_ligne_budgetaire(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModuleBudget/rapport/ligne_generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def post_imprimer_analyse_ligne_budgetaire(request):
	try:
		permission_number = 149
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_analyse_ligne_budgetaire(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleBudget/reporting/analyse_ligne_budgetaire.html", "analyse_ligne_budgetaire.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def post_generer_analyse(request):
	try:
		permission_number = -1
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
				return HttpResponseRedirect(reverse("module_budget_analyse_budgetaire"))

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
		template = loader.get_template("ErpProject/ModuleBudget/rapport/generated.html")
		docHtml = template.render(context)
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nErreur lors génération analyse budgetaire \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur generer analyse budgetaire ')
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_budget_analyse_budgetaire"))


def get_analyse_bgt(request):
	try:
		# droit="CREER_RAPPORT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 149
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
			'module' : ErpModule.MODULE_BUDGET,
			'menu' : 4,

			'sous_modules': sous_modules,

		}
		template = loader.get_template('ErpProject/ModuleBudget/rapport/print.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DU print ANALYSE BUDGETAIRE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_analyse_budgetaire'))




# VIEWSET CLASS
class BudgetViewSet(viewsets.ModelViewSet):

	queryset = models.Model_Budget.objects.all()
	serializer_class = serializer.BudgetSerializer

class LigneBudgetaireViewSet(viewsets.ModelViewSet):
	queryset = models.Model_LigneBudgetaire.objects.all()
	serializer_class = serializer.LigneBudgetaireSerializer




def get_lister_exercicebudgetaire(request):
	# droit="LISTER_EXERCICE_BUDGETAIRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 150
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	# model = dao_exercicebudgetaire.toListExercicebudgetaire()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_exercicebudgetaire.toListExercicebudgetaire(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)


	context ={'title' : 'Liste des exercices budgetaires','model' : model,'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/exercicebudgetaire/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_exercicebudgetaire(request):
	# droit="CREER_EXERCICE_BUDGETAIRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 128
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	context ={'title' : 'Ajouter un exercice budgetaire','utilisateur' : utilisateur,
				'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
				'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/exercicebudgetaire/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_exercicebudgetaire(request):

	try:
		# print("***************************************************")
		designation = request.POST['designation']
		# print("****2")
		montant = makeFloat(request.POST['montant'])
		annee = request.POST['annee']
		auteur = identite.utilisateur(request)
		date_debut = request.POST["date_debut"]
		date_debut = date_debut[6:10] + '-' + date_debut[3:5] + '-' + date_debut[0:2]
		# date_debut = datetime.datetime.strptime(date_debut, "%Y-%m-%d").date()

		date_fin = request.POST["date_fin"]
		date_fin = date_fin[6:10] + '-' + date_fin[3:5] + '-' + date_fin[0:2]
		# date_fin = datetime.datetime.strptime(date_fin, "%Y-%m-%d").date()

		exercicebudgetaire=dao_exercicebudgetaire.toCreateExercicebudgetaire(designation,montant,annee, date_debut, date_fin)
		exercicebudgetaire=dao_exercicebudgetaire.toSaveExercicebudgetaire(auteur, exercicebudgetaire)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_exercicebudgetaire', args=(exercicebudgetaire.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER EXERCICEBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_exercicebudgetaire'))


def get_details_exercicebudgetaire(request,ref):
	# droit="LISTER_EXERCICE_BUDGETAIRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 150
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		exercicebudgetaire=dao_exercicebudgetaire.toGetExercicebudgetaire(ref)
		#print("is acti", exercicebudgetaire.is_active)
		if exercicebudgetaire.is_active:
			type = 1
		else:
			type = 2
		if exercicebudgetaire.is_cloture:
			type = 3
		template = loader.get_template('ErpProject/ModuleBudget/exercicebudgetaire/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,exercicebudgetaire)

		context ={'title' : exercicebudgetaire.designation,'exercicebudgetaire' : exercicebudgetaire,
					'utilisateur' : utilisateur,
					'type':type,
					'actions':auth.toGetActions(modules,utilisateur),
					'organisation': dao_organisation.toGetMainOrganisation(),
					"historique": historique,
					"etapes_suivantes": etapes_suivantes,
					"signee": signee,
					"content_type_id": content_type_id,
					"documents": documents,
					"roles": groupe_permissions,
					'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS EXERCICEBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_exercicebudgetaire'))

def get_modifier_exercicebudgetaire(request,ref):
	# droit="MODIFIER_EXERCICE_BUDGETAIRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 129
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
			return response

	ref = int(ref)
	model = dao_exercicebudgetaire.toGetExercicebudgetaire(ref)
	context ={'title' : 'Modifier un exercice budgetaire','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/exercicebudgetaire/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_exercicebudgetaire(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		montant = makeFloat(request.POST['montant'])
		annee = request.POST['annee']
		auteur = identite.utilisateur(request)
		#print("d'acco")
		date_debut = request.POST["date_debut"]
		date_debut = date_debut[6:10] + '-' + date_debut[3:5] + '-' + date_debut[0:2]
		date_debut = datetime.datetime.strptime(date_debut, "%Y-%m-%d").date()
		#print("jjdkd")


		date_fin = request.POST["date_fin"]
		date_fin = date_fin[6:10] + '-' + date_fin[3:5] + '-' + date_fin[0:2]
		date_fin = datetime.datetime.strptime(date_fin, "%Y-%m-%d").date()

		exercicebudgetaire=dao_exercicebudgetaire.toCreateExercicebudgetaire(designation,montant,annee, date_debut, date_fin)
		exercicebudgetaire=dao_exercicebudgetaire.toUpdateExercicebudgetaire(id, exercicebudgetaire)
		return HttpResponseRedirect(reverse('module_budget_list_exercicebudgetaire'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER EXERCICEBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_exercicebudgetaire'))
from ModuleBudget.dao.dao_projet import dao_projet

def get_lister_projet(request):
	# droit="LISTER_PROJET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 132
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	# model = dao_projet.toListProjet()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_projet.toListProjet(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	somme_total = 0
	ladevise = ""
	for item in model:
		somme_total = somme_total + item.montant
		ladevise = item.devise.symbole_devise


	context ={'title' : 'Liste des projets',"ladevise":ladevise,'somme_total':AfficheEntier(makeFloat(somme_total)), 'model' : model,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/projet/list.html')
	return HttpResponse(template.render(context, request))


def get_creer_projet(request):
	# droit="CREER_PROJET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 131
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	categorie_budget = dao_categoriebudget.toListCategoriebudgetOfType(2)


	context ={'title' : 'Ajouter projet','categorie_budget':categorie_budget, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/projet/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_projet(request):

	try:
		codeprojet = request.POST['codeprojet']
		designation = request.POST['designation']
		description = request.POST['description']
		categoriebudget_id = int(request.POST["categoriebudget_id"])
		montant = request.POST['montant']
		devise_id = request.POST['devise_id']
		date_debut = request.POST['date_debut']
		date_fin = request.POST['date_fin']
		pourcentage_alert = makeFloat(request.POST["pourcentage_alert"])
		message_alert = request.POST["message_alert"]
		auteur = identite.utilisateur(request)

		if categoriebudget_id == 0:
			categoriebudget_id = None

		if devise_id == 0:
			devise_id = dao_devise.toGetDeviseReference().id

		projet=dao_projet.toCreateProjet(codeprojet,designation,description,montant,devise_id,date_debut,date_fin,categoriebudget_id,pourcentage_alert, message_alert)
		projet=dao_projet.toSaveProjet(auteur, projet)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_projet', args=(projet.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER PROJET \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_projet'))


def get_details_projet(request,ref):
	# droit="LISTER_PROJET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 132
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		projet=dao_projet.toGetProjet(ref)
		ligne_budgetaire = dao_ligne_budgetaire.toListLigneOfProjets(projet.id)

		template = loader.get_template('ErpProject/ModuleBudget/projet/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,projet)

		context ={'title' : 'Details sur projet',
		'projet' : projet,
		'ligne_budgetaire':ligne_budgetaire,
		'utilisateur' : utilisateur,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS PROJET \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_projet'))

def get_modifier_projet(request,ref):
	# droit="MODIFIER_PROJET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 133
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response
	ref = int(ref)
	model = dao_projet.toGetProjet(ref)
	context ={'title' : 'Modifier Projet','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/projet/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_projet(request):
	id = int(request.POST['ref'])
	try:
		codeprojet = request.POST['codeprojet']
		designation = request.POST['designation']
		description = request.POST['description']
		categoriebudget_id = int(request.POST["categoriebudget_id"])
		montant = request.POST["montant"]
		devise_id = request.POST['devise_id']
		date_debut = request.POST['date_debut']
		date_fin = request.POST['date_fin']
		pourcentage_alert = makeFloat(request.POST["pourcentage_alert"])
		message_alert = request.POST["message_alert"]

		auteur = identite.utilisateur(request)

		projet=dao_projet.toCreateProjet(codeprojet,designation,description,montant,devise_id,date_debut,date_fin, categoriebudget_id, pourcentage_alert, message_alert)
		projet=dao_projet.toUpdateProjet(id, projet)
		return HttpResponseRedirect(reverse('module_budget_list_projet'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER PROJET \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_projet'))
from ModuleBudget.dao.dao_transactionbudgetaire import dao_transactionbudgetaire

def get_lister_transactionbudgetaire(request):
	# droit="LISTER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 136
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response
	#Lister les employés

	# model = dao_transactionbudgetaire.toListTransactionbudgetaireOfAnneeActive()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_transactionbudgetaire.toListTransactionbudgetaireOfAnneeActive(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)


	context ={'title' : 'Liste des transactions budgétaires','model' : model,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/transactionbudgetaire/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_transactionbudgetaire(request):
	# droit="CREER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 135
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	context ={'title' : 'Ajouter une transaction budgetaire','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'comptes': dao_compte.toListComptes(),'employes':dao_employe.toListEmployes(),'lignes':dao_ligne_budgetaire.toListLigneBudgetairesofExeciceEncours(),'types':dao_type_transaction_budgetaire.toListTypesTransactionBudgetaire(), 'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/transactionbudgetaire/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_transactionbudgetaire(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		#if not auth.toPostValidityDate(var_module_id, datetime.datetime.now().strftime("%d/%m/%Y")): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		designation = request.POST['designation']
		montant = makeFloat(request.POST['montant'])
		description = request.POST['description']
		devise_id = int(request.POST['devise_id'])
		ligne_id = int(request.POST['ligne_id'])
		type_id = int(request.POST['type_id'])
		employe_id  = int(request.POST['employe_id'])
		statut = int(request.POST['statut'])
		auteur = identite.utilisateur(request)

		ligne = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_id)

		#On crée la transaction
		transactionbudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire(designation,montant,description,devise_id,ligne.compte_id,employe_id, ligne_id, type_id, statut)
		transactionbudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionbudgetaire)
		#print('transaction creee avec id {}'.format(transactionbudgetaire.id))

		print('TRANSACTION CREATED')

		#Gestion d'alerte
		ligne = models.Model_LigneBudgetaire.objects.get(pk = ligne_id)
		if ligne != None and makeFloat(ligne.valeur_pourcentage) > makeFloat(ligne.pourcentage_alert):
			#print("toza awa")
			subject = "Alerte depassement du budget de "+ str(ligne.pourcentage_alert)+" %"
			message = ligne.message_alert
			recipient_list = []
			#recipient_list.append(ligne.responsable.email)
			recipient_list.append("sion.israel.pro@gmail.com")
			send_async_mail(subject, message, recipient_list, False, 'Alerte seuil depassé')
			#print("Mail alert envoye")
			ligne.is_alerted = True
			ligne.save()
			#print("Is alerted modifie")
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_transactionbudgetaire', args=(transactionbudgetaire.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_transactionbudgetaire'))


def get_details_transactionbudgetaire(request,ref):
	# droit="LISTER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 136
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		transactionbudgetaire=dao_transactionbudgetaire.toGetTransactionbudgetaire(ref)
		template = loader.get_template('ErpProject/ModuleBudget/transactionbudgetaire/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,transactionbudgetaire)


		context ={'title' : 'Détails sur une transaction budgétaire',
		'transactionbudgetaire' : transactionbudgetaire,
		'model':transactionbudgetaire,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_transactionbudgetaire'))

def get_modifier_transactionbudgetaire(request,ref):
	# droit="CREER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 135
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	ref = int(ref)
	model = dao_transactionbudgetaire.toGetTransactionbudgetaire(ref)
	context ={'title' : 'Modifier une Transaction budgetaire','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/transactionbudgetaire/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_transactionbudgetaire(request):
	id = int(request.POST['ref'])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		# if not auth.toPostValidityDate(var_module_id, datetime.datetime.now().strftime("%d/%m/%Y")): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		designation = request.POST['designation']
		montant = makeFloat(request.POST['montant'])
		description = request.POST['description']
		devise_id = request.POST['devise_id']
		ligne_id = int(request.POST['ligne_id'])
		type_id = int(request.POST['type_id'])
		employe_id  = int(request.POST['employe_id'])
		statut = int(request.POST['statut'])
		auteur = identite.utilisateur(request)

		ligne = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_id)

		transactionbudgetaire=dao_transactionbudgetaire.toCreateTransactionbudgetaire(designation,montant,description,devise_id,ligne.compte_id,employe_id, ligne_id, type_id,statut)
		transactionbudgetaire=dao_transactionbudgetaire.toUpdateTransactionbudgetaire(id, transactionbudgetaire)
		return HttpResponseRedirect(reverse('module_budget_list_transactionbudgetaire'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_transactionbudgetaire'))




def get_lister_categoriebudget(request):
	# droit="LISTER_CATEGORIE_BUDGET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 138
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	# model = dao_categoriebudget.toListCategoriebudget()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_categoriebudget.toListCategoriebudget(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	context ={'title' : 'Liste des catégories de budget','model' : model,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/categoriebudget/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_categoriebudget(request):
	# droit="CREER_CATEGORIE_BUDGET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 137
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context ={'title' : 'Ajouter une catégorie de budget','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/categoriebudget/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_categoriebudget(request):

	try:
		designation = request.POST['designation']
		description = request.POST['description']
		type = request.POST['typebudget']
		auteur = identite.utilisateur(request)

		categoriebudget=dao_categoriebudget.toCreateCategoriebudget(designation,description,type)
		categoriebudget=dao_categoriebudget.toSaveCategoriebudget(auteur, categoriebudget)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_categoriebudget', args=(categoriebudget.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CATEGORIEBUDGET \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_categoriebudget'))


def get_details_categoriebudget(request,ref):
	# droit="LISTER_CATEGORIE_BUDGET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 138
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		categoriebudget=dao_categoriebudget.toGetCategoriebudget(ref)
		template = loader.get_template('ErpProject/ModuleBudget/categoriebudget/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categoriebudget)


		context ={'title' : 'Details sur la catégorie de budget',
		'categoriebudget' : categoriebudget,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CATEGORIEBUDGET \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_categoriebudget'))

def get_modifier_categoriebudget(request,ref):
	# droit="MODIFIER_CATEGORIE_BUDGET"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 139
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	ref = int(ref)
	model = dao_categoriebudget.toGetCategoriebudget(ref)
	context ={'title' : 'Modifier une Catégorie de budget','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/categoriebudget/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_categoriebudget(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		type =int( request.POST['typebudget'])
		auteur = identite.utilisateur(request)

		categoriebudget=dao_categoriebudget.toCreateCategoriebudget(designation,description,type)
		categoriebudget=dao_categoriebudget.toUpdateCategoriebudget(id, categoriebudget)
		return HttpResponseRedirect(reverse('module_budget_list_categoriebudget'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CATEGORIEBUDGET \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_categoriebudget'))


def get_creer_rallonge(request,ref):
	# droit="CREER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 135
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	ref=int(ref)
	ligne=dao_ligne_budgetaire.toGetLigneBudgetaire(ref)
	context ={'title' : 'Ajouter une rallonge budgétaire','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'comptes': dao_compte.toListComptes(), 'ligne_id':ligne.id, 'employes':dao_employe.toListEmployes(),'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/rallonge/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_rallonge(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		montant = makeFloat(request.POST['montant'])
		description = request.POST['description']
		devise_id = request.POST['devise_id']
		ligne_id = request.POST['ligne_id']
		type = dao_type_transaction_budgetaire.toGetTypeRallonge()
		statut = 2 #statut validée
		employe_id  = request.POST['employe_id']
		auteur = identite.utilisateur(request)

		ligne = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_id)

		#test du depassement de la valeur du budget
		exercice_budgetaire = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		montant_alloue_apres_operation = exercice_budgetaire.montant_alloue_exercice + float(montant)
		if exercice_budgetaire.montant < montant_alloue_apres_operation:
			messages.add_message(request, messages.ERROR, "Echec: La rallonge saisie entraine un depassement du montant total du budget prévu")
			return HttpResponseRedirect(reverse('module_budget_add_rallonge', args=(ligne_id,)))

		#On crée la rallonge
		transactionbudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire(designation,montant,description,devise_id,ligne.compte_id, employe_id, ligne_id, type['id'], statut)
		transactionbudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionbudgetaire)

		wkf_task.initializeWorkflow(auteur, transactionbudgetaire)
		#print('TRANSACTIONBUDGETAIRE CREE ID {}'.format(transactionbudgetaire.id))

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_transactionbudgetaire', args=(transactionbudgetaire.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		ligne_id = request.POST['ligne_id']
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_rallonge', args=(ligne_id,)))


def get_details_rallonge(request,ref):
	# droit="LISTER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 136
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		transactionbudgetaire=dao_transactionbudgetaire.toGetTransactionbudgetaire(ref)
		template = loader.get_template('ErpProject/ModuleBudget/rallonge/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,transactionbudgetaire)

		context ={'title' : 'Details sur la rallonge','transactionbudgetaire' : transactionbudgetaire,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_transactionbudgetaire'))

def get_creer_diminution(request,ref):
	# droit="CREER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 135
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	ref=int(ref)
	ligne=dao_ligne_budgetaire.toGetLigneBudgetaire(ref)
	context ={'title' : 'Ajouter une diminution budgétaire','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'comptes': dao_compte.toListComptes(), 'ligne_id':ligne.id, 'employes':dao_employe.toListEmployes(),'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/diminution/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_diminution(request):
	sid = transaction.savepoint()
	try:
		designation = request.POST['designation']
		montant = makeFloat(request.POST['montant'])
		description = request.POST['description']
		devise_id = request.POST['devise_id']
		ligne_id = request.POST['ligne_id']
		type = dao_type_transaction_budgetaire.toGetTypeDiminution()
		statut = 2 #statut validée
		employe_id  = request.POST['employe_id']
		auteur = identite.utilisateur(request)

		ligne = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_id)

		#Test si on va en dessous du seuil d'alerte
		montant_apres_operation = float(ligne.valeur_solde) - float(montant)
		montant_seuil_limite = (ligne.montant_alloue * ligne.pourcentage_alert) / 100
		if montant_apres_operation < montant_seuil_limite:
			messages.add_message(request, messages.ERROR, "Echec: Le budget ne peut aller en dessous de son seuil d'alerte")
			return HttpResponseRedirect(reverse('module_budget_add_diminution', args=(ligne_id,)))


		#On crée la diminution
		transactionbudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire(designation,montant,description,devise_id,ligne.compte_id, employe_id, ligne_id, type['id'], statut)
		transactionbudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionbudgetaire)
		#print('TRANSACTIONBUDGETAIRE CREE ID {}'.format(transactionbudgetaire.id))
		wkf_task.initializeWorkflow(auteur, transactionbudgetaire)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_transactionbudgetaire', args=(transactionbudgetaire.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		ligne_id = request.POST['ligne_id']
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_add_diminution', args=(ligne_id,)))


def get_details_diminution(request,ref):
	# droit="LISTER_TRANSACTION_BGT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 136
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		transactionbudgetaire=dao_transactionbudgetaire.toGetTransactionbudgetaire(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,transactionbudgetaire)

		template = loader.get_template('ErpProject/ModuleBudget/diminution/item.html')
		context ={'title' : 'Details sur la diminution','transactionbudgetaire' : transactionbudgetaire,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TRANSACTIONBUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_transactionbudgetaire'))


def get_json_list_categorie_budget(request):
	try:
		data = []
		type = int(request.GET["ref"])
		categories = dao_categoriebudget.toListCategoriebudgetOfType(type)
		for categorie in categories:
			item = {
				"id" : categorie.id,
				"designation" : categorie.designation,
				"description" : categorie.description
			}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)


#CENTRE DE COUT
def get_lister_centre_cout(request):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 175
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
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/centre_cout/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_centre_cout(request):
	# droit='CREER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 174
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	centre_cout = dao_centre_cout.toListCentreCoutOfTypeView()
	groupes = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Ajouter un centre de coût','centre_cout':centre_cout, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'groupes':groupes,
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/centre_cout/add.html')
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
		return HttpResponseRedirect(reverse('module_budget_detail_centre_cout', args=(centre_cout.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_centre_cout'))


def get_details_centre_cout(request,ref):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 175
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

		template = loader.get_template('ErpProject/ModuleBudget/centre_cout/item.html')

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,centre_cout)
		context ={'title' : centre_cout.designation + ' : Détails','centre_cout' : centre_cout,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'montant_alloue':montant_alloue,
		'montant_consomme':montant_consomme,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'ligne_budgetaire':lignes,
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_list_centre_cout'))
def get_modifier_centre_cout(request,ref):
	# droit='MODIFIER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 176
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
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/centre_cout/update.html')
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
		return HttpResponseRedirect(reverse('module_budget_list_centre_cout'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_centre_cout'))





def get_lister_activite(request):
	# droit='LISTER_ACTIVITE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 330
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_activite.toListActivite()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_activite.toListActivite(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	context ={'title' : 'Liste des activités','model' : model,
	'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/activite/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_activite(request):
	# droit='CREER_ACTIVITE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 329
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	context ={'title' : 'Ajouter une activité','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/activite/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_activite(request):

	try:
		code = request.POST['code']
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		activite=dao_activite.toCreateActivite(code,designation)
		activite=dao_activite.toSaveActivite(auteur, activite)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_activite', args=(activite.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER ACTIVITE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_activite'))


def get_details_activite(request,ref):
	# droit='LISTER_ACTIVITE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 330
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		activite=dao_activite.toGetActivite(ref)
		template = loader.get_template('ErpProject/ModuleBudget/activite/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,activite)

		context ={'title' : 'Détails sur une activité','activite' : activite,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS ACTIVITE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_list_activite'))
def get_modifier_activite(request,ref):
	# droit='MODIFIER_ACTIVITE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 331
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ref = int(ref)
	model = dao_activite.toGetActivite(ref)
	context ={'title' : 'Modifier une activité','model':model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur': utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/activite/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_activite(request):

	id = int(request.POST['ref'])
	try:
		code = request.POST['code']
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		activite=dao_activite.toCreateActivite(code,designation)
		activite=dao_activite.toUpdateActivite(id, activite)
		return HttpResponseRedirect(reverse('module_budget_list_activite'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER ACTIVITE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_activite'))

#TOOLS
def send_mail_alert(ligne):
	sujet = "Alerte depassement du budget de "+ ligne.pourcentage_alert+" %"
	message = ligne.message_alert
	from_email = 'noreply.nsandax@gmail.com'
	recipient_list = ['fabermandeke@gmail.com']

	html_message =  '<!doctype html><html><head><meta name="viewport" content="initial-scale=1.0, user-scalable=no"><meta charset="utf-8">'
	html_message = html_message + '<style>html, body, * {height: 100%;margin: 0;padding: 0; box-sizing: border-box; font-family: "Trebuchet MS", sans-serif;  font-size: 14px;}'
	html_message = html_message + ' head {display: none;} .grid {display: block; position: relative; margin: .625rem 0;}'
	html_message = html_message + ' .grid .row:last-child {margin-bottom: 0;}'
	html_message = html_message + ' .grid .row {width: 100%; display: block; margin: 0 0 2.12765% 0;}'
	html_message = html_message + ' .grid .row.cells3 > .cell.colspan2 {width: 65.95745%;} '
	html_message = html_message + ' .grid .row > .cell:first-child {margin-left: 0;} .grid .row > .cell {display: block; makeFloat: left; min-height: 10px;}'
	html_message = html_message + ' .padding40 {padding: 2.5rem;} p {display: block; -webkit-margin-before: 1em; -webkit-margin-after: 1em;}'
	html_message = html_message + ' .danger, .button.alert {background: #ce352c; color: #ffffff; border-color: #ce352c;}'
	html_message = html_message + ' a.button {padding-top: .53125rem;} a:visited {color: #2086bf;}'
	html_message = html_message + ' .button {padding: 0 1rem; height: 2.125rem; text-align: center; vertical-align: middle;'
	html_message = html_message + ' border: 1px #d9d9d9 solid; cursor: pointer; display: inline-block; outline: none; font-size: .875rem;'
	html_message = html_message + ' line-height: 100%; margin: .15625rem 0; position: relative; } a {text-decoration: none;}</style>'
	html_message = html_message + '</head><body>'
	html_message = html_message + '<div class="grid"><div class="row cells3"><div class="cell colspan2 padding40"><p style="font-size:13px">'
	html_message = html_message + "Bonjour,<br><br>"+ ligne.message_alert +".<br><br>"
	html_message = html_message + '<br><br>Nous vous prions de cliquer sur le bouton ci-dessous pour vous connecter à votre compte.'
	html_message = html_message + '<br><br><a href="http://127.0.0.1" class="button danger">Acceder à mon compte</a><br><br>'
	html_message = html_message + "<br><br><b>Nsandax ERP</b>.</p></div></div></div></body></html>"

	send_mail(sujet, message, from_email, recipient_list, fail_silently = False, html_message = html_message)

def send_mail_test():
	sujet = "Test envoie mail"
	message = "Test envoie mail avec style"
	from_email = 'noreply.nsandax@gmail.com'
	recipient_list = ['fabermandeke@gmail.com']

	html_message =  '<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"><meta charset="utf-8">'
	html_message = html_message + '<style type="text/css">'
	html_message = html_message + '* { margin: 0; padding: 0; font-size: 100%; font-family: "Avenir Next", "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif; line-height: 1.65; }img { max-width: 100%; margin: 0 auto; display: block; }body, .body-wrap { width: 100% !important; height: 100%; background: #f8f8f8; }a { color: #71bc37; text-decoration: none; }a:hover { text-decoration: underline; }.text-center { text-align: center; }.text-right { text-align: right; }.text-left { text-align: left; }.button { display: inline-block; color: white; background: #d2023b; border: solid #d2023b; border-width: 10px 20px 8px; font-weight: bold; border-radius: 4px; }'
	html_message = html_message + '.button:hover { text-decoration: none; }h1, h2, h3, h4, h5, h6 { margin-bottom: 20px; line-height: 1.25; }h1 { font-size: 16px; }h2 { font-size: 28px; }h3 { font-size: 24px; }h4 { font-size: 20px; }h5 { font-size: 16px; }p, ul, ol { font-size: 16px; font-weight: normal; margin-bottom: 20px; }.container { display: block !important; clear: both !important; margin: 0 auto !important; max-width: 580px !important; }.container table { width: 100% !important; border-collapse: collapse; }.container .masthead { padding: 25px 0; background: #d2023b; color: white; }.container .mastheadimg { width: 200px; padding: 10px 0; background:transparent;border-bottom:5px #00172d solid; }.container .masthead h1 { margin: 0 auto !important; max-width: 90%; text-transform: uppercase; }.container .content { background: white; padding: 30px 35px; }.container .content.footer { background: none; }.container .content.footer p { margin-bottom: 0; color: #888; text-align: center; font-size: 14px; }.container .content.footer a { color: #888; text-decoration: none; font-weight: bold; }.container .content.footer a:hover { text-decoration: underline; }.logo { width: 200px; }'
	html_message = html_message + '</style>'
	html_message = html_message + '</head><body>'
	html_message = html_message + '<table class="body-wrap">'
	html_message = html_message + '<tr><td class="container"><table>'
	html_message = html_message + '<tr><td align="center" class="mastheadimg"><img class="logo" src="http://www.influxapp.media/assets/images/logo_arpce_large.png"/></td></tr>'
	html_message = html_message + '<tr><td align="center" class="masthead"><h1>Nouvelle disponibilité sur Influx</h1></td></tr>'
	html_message = html_message + '<tr><td class="content"><img width=220 height=220 src="http://www.influxapp.media/assets/images/danger.png"/>'
	html_message = html_message + '<h4 style="margin-top:10px">Bonjour ,</h4><p>c est une nouvelle disponibilité sur Influx</p></td></tr>'
	html_message = html_message + '</table></td></tr>'
	html_message = html_message + '<tr><td class="container"><table><tr><td class="content footer" align="center"><p>Nsandax ERP</p><p><a href="mailto:">admin@arpce.cd</a> </p></td></tr></table></td></tr>'
	html_message = html_message + '</table></body></html>'

	send_mail(sujet, message, from_email, recipient_list, fail_silently = False, html_message = html_message)






def get_lister_groupeanalytique(request):
	# droit='LISTER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 334
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
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/groupeanalytique/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_groupeanalytique(request):
	# droit='CREER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 333
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	context ={'title' : 'Ajouter un groupe analytique','utilisateur' : utilisateur,
	'groupe_analytique':groupe_analytique,
	'isPopup': True if 'isPopup' in request.GET else False,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/groupeanalytique/add.html')
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
		return HttpResponseRedirect(reverse('module_budget_detail_groupeanalytique', args=(groupeanalytique.id,))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_groupeanalytique'))


def get_details_groupeanalytique(request,ref):
	# droit='LISTER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 334
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		groupeanalytique=dao_groupeanalytique.toGetGroupeanalytique(ref)
		template = loader.get_template('ErpProject/ModuleBudget/groupeanalytique/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,groupeanalytique)

		context ={'title' : 'Details sur un groupe analytique','groupeanalytique' : groupeanalytique,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_list_groupeanalytique'))
def get_modifier_groupeanalytique(request,ref):
	# droit='MODIFIER_GROUPE_ANALYTIQUE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 336
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
	'utilisateur': utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/groupeanalytique/update.html')
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
		return HttpResponseRedirect(reverse('module_budget_list_groupeanalytique'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER GROUPEANALYTIQUE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_groupeanalytique'))


def get_lister_poste_budgetaire(request):
	# droit='LISTER_POSTE_BUDGETAIRE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 338
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_poste_budgetaire.toListPoste_budgetaire()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_poste_budgetaire.toListPoste_budgetaire(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	context ={'title' : 'Liste des postes budgétaires',
	'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model' : model,'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/poste_budgetaire/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_poste_budgetaire(request):
	# droit='CREER_POSTE_BUDGETAIRE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 337
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context ={'title' : 'Ajouter un poste budgétaire',
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/poste_budgetaire/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_poste_budgetaire(request):

	try:
		code = request.POST['code']
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		poste_budgetaire=dao_poste_budgetaire.toCreatePoste_budgetaire(code,designation)
		poste_budgetaire=dao_poste_budgetaire.toSavePoste_budgetaire(auteur, poste_budgetaire)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_poste_budgetaire', args=(poste_budgetaire.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER POSTE_BUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_poste_budgetaire'))


def get_details_poste_budgetaire(request,ref):
	# droit='LISTER_POSTE_BUDGETAIRE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 338
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref=int(ref)
		poste_budgetaire=dao_poste_budgetaire.toGetPoste_budgetaire(ref)
		ligne_poste_budgetaire = dao_ligne_poste_budgetaire.toListLigneOfPosteBudgetaire(ref)

		template = loader.get_template('ErpProject/ModuleBudget/poste_budgetaire/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,poste_budgetaire)


		context ={'title' : 'Details sur un poste budgétaire',
		'ligne_poste_budgetaire':ligne_poste_budgetaire,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'poste_budgetaire' : poste_budgetaire,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS POSTE_BUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_list_poste_budgetaire'))
def get_modifier_poste_budgetaire(request,ref):
	# droit='MODIFIER_POSTE_BUDGETAIRE'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 339
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ref = int(ref)
	model = dao_poste_budgetaire.toGetPoste_budgetaire(ref)
	context ={'title' : 'Modifier un poste budgétaire',
	'actions':auth.toGetActions(modules,utilisateur),'modules' : modules,'sous_modules': sous_modules,
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/poste_budgetaire/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_poste_budgetaire(request):

	id = int(request.POST['ref'])
	try:
		code = request.POST['code']
		designation = request.POST['designation']
		auteur = identite.utilisateur(request)

		poste_budgetaire=dao_poste_budgetaire.toCreatePoste_budgetaire(code,designation)
		poste_budgetaire=dao_poste_budgetaire.toUpdatePoste_budgetaire(id, poste_budgetaire)
		return HttpResponseRedirect(reverse('module_budget_list_poste_budgetaire'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER POSTE_BUDGETAIRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_poste_budgetaire'))


#PROJET -- CENTRE DE COUT
def get_lister_centre_projet(request):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 175
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_centre_cout.toListCentreCoutOfProjet()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_centre_cout.toListCentreCoutOfProjet(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context ={'title' : 'Liste des projets','model' : model,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/centre_cout/projet/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_centre_projet(request):
	# droit='CREER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 174
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	centre_cout = dao_centre_cout.toListCentreCoutOfProjet()
	context ={'title' : 'Ajouter un projet','centre_cout':centre_cout, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/centre_cout/projet/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_centre_projet(request):

	try:
		designation = request.POST['designation']
		code = request.POST['code']
		centre_cout_id = request.POST['centre_cout_id']
		abbreviation = request.POST['abbreviation']
		type_centre = request.POST['type_centre']
		groupe_analytique_id = request.POST['groupe_analytique_id']

		if centre_cout_id == "":
			centre_cout_id = None
		auteur = identite.utilisateur(request)

		centre_cout=dao_centre_cout.toCreateCentre_cout(designation,code,type_centre,abbreviation,centre_cout_id, groupe_analytique_id)
		centre_cout=dao_centre_cout.toSaveCentre_cout(auteur, centre_cout)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_budget_detail_projet_centre_cout', args=(centre_cout.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_projet_centre_cout'))


def get_details_centre_projet(request,ref):
	# droit='LISTER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 175
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

		template = loader.get_template('ErpProject/ModuleBudget/centre_cout/projet/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,centre_cout)

		context ={'title' : centre_cout.designation + ' : Détails',
		'centre_cout' : centre_cout,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'montant_alloue':montant_alloue,
		'montant_consomme':montant_consomme,
		'ligne_budgetaire':lignes,
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_projet_list_centre_cout'))
def get_modifier_centre_projet(request,ref):
	# droit='MODIFIER_CENTRE_COUT'
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 176
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ref = int(ref)
	model = dao_centre_cout.toGetCentre_cout(ref)
	groupe_analytique = dao_groupeanalytique.toListGroupeanalytique()
	centre_cout = dao_centre_cout.toListCentreCoutOfProjet()
	context ={'title' : 'Modifier le projet','model':model, 'utilisateur': utilisateur,
	'groupe_analytique':groupe_analytique,
	'centre_cout':centre_cout,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleBudget/centre_cout/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_centre_projet(request):

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
		return HttpResponseRedirect(reverse('module_budget_list_projet_centre_cout'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CENTRE_COUT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_budget_add_projet_centre_cout'))



def get_details_ecriture_analytique_of_ligne_budgetaire(request, ref):
	try:
		# droit="LISTER_COMBINAISON"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 146
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return None

		ref = int(ref)
		ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaire(ref)
		exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		ecritures_analytiques = []
		balance = 0
		if exercice:
			ecritures_analytiques = dao_ecriture_analytique.toListEcritureAnalytiqueOfLigneBudgetaire(ref, exercice.date_debut, exercice.date_fin)
			balance = makeFloat(ligne_budgetaire.montant_alloue) - makeFloat(ligne_budgetaire.valeur_ecriture_reel)

		montant_consomme = 0
		charge = 0
		produit = 0
		for ecriture in ecritures_analytiques:
			#Montant consommé via les écritures
			montant_consomme += ecriture.montant
			if ecriture.montant >= 0:
				produit += ecriture.montant
			else:
				charge += ecriture.montant

		if ligne_budgetaire.montant_alloue > 0:
			pourcentage = 100 * makeFloat(montant_consomme) / makeFloat(ligne_budgetaire.montant_alloue)
		else:
			pourcentage = 0


		context ={
		'title' : 'Ecritures analytiques de la combinaison budgétaire',
		'ligne_budgetaire':ligne_budgetaire,
		'utilisateur' : utilisateur,
		'charge':charge,
		'produit':produit,
		'montant_alloue': ligne_budgetaire.montant_alloue,
		'devise': dao_devise.toGetDeviseReference(),
		'pourcentage' : pourcentage,
		'balance': balance,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'ecritures_analytiques':ecritures_analytiques,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/ecriture_analytique/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print("ERREUR DETAILLER Ecriture")
		print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))

def get_details_ecriture_analytique_of_centre_cout(request, ref):
	try:
		# droit="LISTER_CENTRE_COUT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 175
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
			return HttpResponseRedirect(reverse('module_budget_list_centre_cout'))


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
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'reel': montant_consomme,
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
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/centre_cout/ecriture_analytique/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR DETAILLER Ecriture")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_centre_cout'))

def get_details_ecriture_comptable_of_ligne_budgetaire(request, ref):
	try:
		# droit="LISTER_COMBINAISON"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 146
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return None

		ref = int(ref)
		ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaire(ref)
		exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		#print("lqksqls", exercice)
		if exercice:
			ecritures_comptables, montant_debit, montant_credit = dao_ecriture_comptable.toListEcrituresComptablesOfAccount(ligne_budgetaire.compte_id, exercice.date_debut, exercice.date_fin)
		else:
			ecritures_comptables, montant_debit, montant_credit = [], 0, 0


		#print("ecri", ecritures_comptables[0])
		context ={
		'title' : 'Ecritures comptables de la combinaison budgétaire',
		'ligne_budgetaire':ligne_budgetaire,
		'utilisateur' : utilisateur,
		'montant_debit': montant_debit,
		'montant_credit': montant_credit,
		'montant_alloue': ligne_budgetaire.montant_alloue,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		'ecritures_comptables':ecritures_comptables,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 27
		}
		template = loader.get_template('ErpProject/ModuleBudget/ligne_budgetaire/ecriture_comptable/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleBudget'
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIGNE BUDGETAIRE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("ERREUR DETAILLER Ecriture")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_budget_list_ligne_budgetaire'))


def get_json_groupement_analytique(request):
	try:
		#print("groupement analytique")
		data = []
		ident = int(request.GET["ref"])
		#print(ident)

		#print("dazom")
		groupement_analytique = dao_groupeanalytique.toGetGroupeanalytique(ident)
		item = {"est_projet": groupement_analytique.est_projet}
		data.append(item)
		#print("masolo",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("erreur",e)
		return JsonResponse([], safe=False)

def get_json_report_ligne_budgetaire(request):
	try:
			#print("active exercice budgetaire")
		data = []
		id = int(request.GET["ref"])

		ligne = dao_ligne_budgetaire.toGetReportLignebudgetaire(id)
		item = { "is_success":"ok"}
		data.append(item)
		# print("REPONSE",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		# print("erreur",e)
		return JsonResponse([], safe=False)

def get_json_desactive_ligne_budgetaire_report(request):
	try:
			#print("active exercice budgetaire")
		data = []
		id = int(request.GET["ref"])

		ligne = dao_ligne_budgetaire.toDesactiveReportLignebudgetaire(id)
		item = { "is_success":"ok"}
		data.append(item)
		# print("REPONSE",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		# print("erreur",e)
		return JsonResponse([], safe=False)


@transaction.atomic
def post_cloture_exercice_budgetaire(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		id = int(request.POST["exercicebudgetaire_id"])
		exercice_encours = dao_exercicebudgetaire.toGetExercicebudgetaire(id)
		year = exercice_encours.date_fin
		year = str(year.year)

		lignes = Model_LigneBudgetaire.objects.filter(exericebudgetaires__id = id, is_reportable = True)
		for item in lignes:
			item.lastyearrepart = year
			item.save()

		exercice = dao_exercicebudgetaire.toClotureExerciceBudgetaire(id)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		# print("ERREUR POST FERMETURE EXERCICE")
		# print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_budget_list_exercicebudgetaire"))



def get_json_active_exercice_budgetaire(request):
	try:
		#print("active exercice budgetaire")
		data = []

		exercice = dao_exercicebudgetaire.toGetActiveExercicebudgetaire()
		item = {"annee": exercice.annee, "designation":exercice.designation}
		data.append(item)
		#print("masolo",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("erreur",e)
		return JsonResponse([], safe=False)

def set_json_cloture_exercice_budgetaire(request):
	try:
		#print("set_json_cloture_exercice_budgetaire")
		data = []
		id = int(request.GET["ref"])

		exercice = dao_exercicebudgetaire.toClotureExerciceBudgetaire(id)
		item = { "is_success":exercice}
		data.append(item)
		#print("masolo",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("erreur",e)
		return JsonResponse([], safe=False)


def get_creer_ouverture_exercice(request):
	# droit="LISTER_COMBINAISON"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 146
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response
	#On recupere uniquement les lignes budgetaires dont le report est activé
	model = dao_ligne_budgetaire.toListLigneBudgetaireReport()
	# for item in model:
    # 	resultat = dao_ligne_budgetaire.toComputeValueOfLigneBudgetaireForExerciceBudgetaire(ligne.id,ref)

	ref = None
	if 'ref' in request.GET:
		ref = request.GET['ref']
		#print("ref", ref)
	context = {
		'title' : 'Ouverture exercice budgétaire',
		'model' : model,
		'isPopup': True,
		'exercicebudgetaire_id':ref,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_BUDGET,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleBudget/exercicebudgetaire/ouverture/add.html")
	return HttpResponse(template.render(context, request))

def to_get_cloture_exercice(request):
	permission_number = 146
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	lignes = dao_ligne_budgetaire.toListLigneBudgetairesExerciceON()
	model = []
	ref = None
	designation =  ""
	if 'ref' in request.GET:
		ref = request.GET['ref']
		exercice = dao_exercicebudgetaire.toGetExercicebudgetaire(ref)
		designation = exercice.designation

	resultat_global = {
		'montant_alloue':0,
		'dotation':0,
		'rallonge':0,
		'diminution':0,
		'normal':0,
		'solde':0
	}
	for ligne in lignes:
		resultat = dao_ligne_budgetaire.toComputeValueOfLigneBudgetaireForExerciceBudgetaire(ligne.id,ref)
		# print(resultat)
		model.append(resultat)
		resultat_global['dotation'] += resultat['dotation']
		resultat_global['rallonge'] += resultat['rallonge']
		resultat_global['diminution'] += resultat['diminution']
		resultat_global['normal'] += resultat['normal']

	resultat_global['solde'] = resultat_global['dotation'] + resultat_global['rallonge'] - resultat_global['diminution'] - resultat_global['normal']
	resultat_global['montant_alloue'] = resultat_global['solde'] + resultat_global['normal']

	devise = dao_devise.toGetDeviseReference()

	context = {
		'title' : 'Clôture :' + designation ,
		'model' : model,
		'resultat_global':resultat_global,
		'isPopup': True,
		'devise':devise,
		'exercicebudgetaire_id':ref,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_BUDGET,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleBudget/exercicebudgetaire/closed/closing.html")
	return HttpResponse(template.render(context, request))


def get_rapport_cloture_exercice(request):
	permission_number = 146
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	lignes = dao_ligne_budgetaire.toListLigneBudgetaires()
	model = []
	ref = None
	designation =  ""
	if 'ref' in request.GET:
		ref = request.GET['ref']
		#print("ref", ref)
		exercice = dao_exercicebudgetaire.toGetExercicebudgetaire(ref)
		designation = exercice.designation

	resultat_global = {
				'montant_alloue':0,
				'dotation':0,
				'rallonge':0,
				'diminution':0,
				'normal':0,
				'solde':0
				}

	for ligne in lignes:
		resultat = dao_ligne_budgetaire.toComputeValueOfLigneBudgetaireForExerciceBudgetaire(ligne.id,ref)
		model.append(resultat)
		resultat_global['dotation'] += resultat['dotation']
		resultat_global['rallonge'] += resultat['rallonge']
		resultat_global['diminution'] += resultat['diminution']
		resultat_global['normal'] += resultat['normal']

	resultat_global['solde'] = resultat_global['dotation'] + resultat_global['rallonge'] - resultat_global['diminution'] - resultat_global['normal']
	resultat_global['montant_alloue'] = resultat_global['solde'] + resultat_global['normal']

	devise = dao_devise.toGetDeviseReference()


	context = {
		'title' : 'Rapport de clôture :' + designation ,
		'model' : model,
		'resultat_global':resultat_global,
		'isPopup': True,
		'devise':devise,
		'exercicebudgetaire_id':ref,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_BUDGET,
		'menu' : 2
	}
	template = loader.get_template("ErpProject/ModuleBudget/exercicebudgetaire/ouverture/item.html")
	return HttpResponse(template.render(context, request))



def get_print_rapport_cloture_exercice(request):
	permission_number = 146
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	lignes = dao_ligne_budgetaire.toListLigneBudgetaires()
	model = []
	ref = None
	designation =  ""
	if 'ref' in request.GET:
		ref = request.GET['ref']
		#print("ref", ref)
		exercice = dao_exercicebudgetaire.toGetExercicebudgetaire(ref)
		designation = exercice.designation

	resultat_global = {
				'montant_alloue':0,
				'dotation':0,
				'rallonge':0,
				'diminution':0,
				'normal':0,
				'solde':0
				}

	for ligne in lignes:
		resultat = dao_ligne_budgetaire.toComputeValueOfLigneBudgetaireForExerciceBudgetaire(ligne.id,ref)
		model.append(resultat)
		resultat_global['dotation'] += resultat['dotation']
		resultat_global['rallonge'] += resultat['rallonge']
		resultat_global['diminution'] += resultat['diminution']
		resultat_global['normal'] += resultat['normal']

	resultat_global['solde'] = resultat_global['dotation'] + resultat_global['rallonge'] - resultat_global['diminution'] - resultat_global['normal']
	resultat_global['montant_alloue'] = resultat_global['solde'] + resultat_global['normal']

	devise = dao_devise.toGetDeviseReference()


	context = {
		'title' : 'Rapport de clôture :' + designation ,
		'model' : model,
		'resultat_global':resultat_global,
		'isPopup': True,
		'devise':devise,
		'exercicebudgetaire_id':ref,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_BUDGET,
		'menu' : 2
	}
	return weasy_print("ErpProject/ModuleBudget/reporting/cloture_budget.html", "cloture_budget.pdf", context)




@transaction.atomic
def post_creer_ouverture_exercice(request):
	sid = transaction.savepoint()
	exercice_budgetaire_id = request.POST["exercicebudgetaire_id"]
	try:
		#print("post_creer_ouverture_exercice")
		exercice_budgetaire = dao_exercicebudgetaire.toGetExercicebudgetaire(exercice_budgetaire_id)

		auteur = identite.utilisateur(request)
		devise = dao_devise.toGetDeviseReference()
		list_ligne_id = request.POST.getlist('ligne_id', None)
		list_montant_alloue = request.POST.getlist('montant_alloue', None)

		for i in range(0, len(list_ligne_id)):
			ident = int(list_ligne_id[i])
			ligne = Model_LigneBudgetaire.objects.get(pk = ident)
			ligne.exericebudgetaires_id = exercice_budgetaire.id
			ligne.save()

		#print(len(list_ligne_id))
		#print(len(list_montant_alloue))
		#Test if montant des lignes est superieur au montant d'exercice
		
		#print("exerice budgetaire ", exercice_budgetaire)
		montant_total = 0
		for i in range(0, len(list_ligne_id)):
			montant_total += makeFloat(list_montant_alloue[i])

		if montant_total > exercice_budgetaire.montant:
			messages.add_message(request, messages.ERROR, "Echec: Le montant entré depasse le montant total du budget prévu")
			return HttpResponseRedirect(reverse('module_budget_add_ouverture_exercice') + "?ref=" + exercice_budgetaire_id)
		#set exercice budgetaire selectionné as exercice budgetaire Active
		dao_exercicebudgetaire.toSetActiveExerciceBudgetaire(exercice_budgetaire_id)

		designation = "Ouverture exercice budgétaire"

		for i in range(0, len(list_ligne_id)):

			ligne_id = list_ligne_id[i]
			montant_alloue = makeFloat(list_montant_alloue[i])
			lignebudgetaire = dao_ligne_budgetaire.toGetLigneBudgetaire(ligne_id)
			dao_ligne_budgetaire.toDesactiveReportLignebudgetaire(ligne_id)
			#print("ligne", ligne_id)
			type_transaction = 4 #Type Dotation
			statut_transaction = 2 # statut traité
			#On crée la transaction
			transactionbudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire(designation,montant_alloue,"",devise.id,lignebudgetaire.compte_id,auteur.id, ligne_id, type_transaction, statut_transaction)
			transactionbudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionbudgetaire)
			#print('transaction creee avec id {}'.format(transactionbudgetaire.id))

		#On change le statut de est_report de chaque ligne B.
		# for item in list_ligne_id:
    	# 	ligne = dao_ligne_budgetaire.toDesactiveReportLignebudgetaire(item)



		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		#print("ERREUR POST OUVERTURE COMPTABLE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_budget_add_ouverture_exercice")+ "?ref=" + exercice_budgetaire_id)



# BUDGET DEPENSE A PART
def get_lister_budget_depense(request):
	permission_number = 142
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	model = None
	# model = dao_model.toListModel(dao_budget.toListBudgetDepenses(), permission_number, groupe_permissions, identite.utilisateur(request))
	model = dao_model.toListModel(dao_ligne_budgetaire.toGetLigneBudgetaireBudgetDepense(), permission_number, groupe_permissions, identite.utilisateur(request))

	budget_depense = dao_type_budget.toGetTypeBudgetDepense()

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)
	type_budget = dao_type_budget.toGetTypeBudget(2)

	context ={
		'title' : "Liste des budgets de dépense",
		'model' : model,
		'budget_depense': budget_depense,
		'view' : view,
		'type_budget': type_budget,
		'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26
	}
	template = loader.get_template('ErpProject/ModuleBudget/budget/depense/list.html')
	return HttpResponse(template.render(context, request))


# BUDGET DEPENSE A PART
def get_lister_budget_recette(request):
	permission_number = 142
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	model = None
	# model = dao_model.toListModel(dao_budget.toListBudgetRecettes(), permission_number, groupe_permissions, identite.utilisateur(request))
	model = dao_model.toListModel(dao_ligne_budgetaire.toGetLigneBudgetaireBudgetRecette(), permission_number, groupe_permissions, identite.utilisateur(request))

	budget_recette = dao_type_budget.toGetTypeBudgetRecette()
	calcul_recette = dao_budget.toComputeBudget(1)
	print('***LISTE BUDGET RECETTE', model)

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)
	type_budget = dao_type_budget.toGetTypeBudget(1)


	context ={
		'title' : "Liste des budgets de recette",
		'model' : model,
		'budget_recette': budget_recette,
		'view' : view,
		'unite_fonctionnelle': dao_unite_fonctionnelle.toListUniteFonctionnelle(),
		'type_budget': type_budget,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26,
		'calcul_recette':calcul_recette,
	}
	template = loader.get_template('ErpProject/ModuleBudget/budget/recette/list.html')
	return HttpResponse(template.render(context, request))

# BUDGET REGROUPEMENT
def get_lister_regroupement_b(request):
    permission_number = 625
    modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

    if response != None:
    	return response

    # model = None
    model = dao_model.toListModel(dao_budget.toListBudget(), permission_number, groupe_permissions, identite.utilisateur(request))

    somme_total = 0
    ladevise = ""
    for item in model:
    	somme_total = somme_total + item.solde
    	ladevise = item.devise.symbole_devise

    somme_total = str(somme_total)

    try:
    	view = str(request.GET.get("view","list"))
    except Exception as e:
    	view = "list"

	#Pagination
    model = pagination.toGet(request, model)

    context ={
		'title' : "Liste des Natures de budget",
		'model' : model,
		'view' : view,
		'utilisateur' : utilisateur,
		"somme_total":AfficheEntier(makeFloat(somme_total)),
		'ladevise': ladevise,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_BUDGET,
		'menu' : 26
	}

    template = loader.get_template('ErpProject/ModuleBudget/budget/regroupement_bgt/list.html')
    return HttpResponse(template.render(context, request))


def get_lister_rapprochement_transaction(request):
	permission_number = 136
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	#Lister les employés

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_transactionbudgetaire.toListTransactionbudgetaireOfAnneeActive(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = dao_transactionbudgetaire.toListTransactionSansBC()

	context ={
		'title' : 'Rapprochement budgetaire','model' : model,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_BUDGET,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleBudget/rapprochement/list.html')
	return HttpResponse(template.render(context, request))

def get_json_lignes_bon_commande_non_facture_for_transaction(request):
	try:
		data = []
		#On prend uniquement les bons en attente de facturation
		bons =  dao_bon_reception.toListFournituresFacturablesByWorkflow()
		devise = dao_devise.toGetDeviseReference()
		ref = int(request.GET["ref"])
		transaction_budgetaire = dao_transactionbudgetaire.toGetTransactionbudgetaire(ref)

		for bon in bons:
			lignes  = dao_ligne_reception.toListLigneOfReceptions(bon.id)
			for ligne in lignes:
				montant_total = ligne.prix_unitaire * ligne.quantite_demande
				if montant_total == transaction_budgetaire.montant:
					item = {"id": ligne.id, "numero_bon" : ligne.bon_reception.numero_reception, 'article':ligne.article.designation, 'ligne_budgetaire' : ligne.ligne_budgetaire.code, 'montant_total':montant_total, 'devise': devise.symbole_devise, 'date':str(ligne.bon_reception.date_reception)}
					data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		print('erreur', e)
		return JsonResponse([], safe=False)


def post_json_rapprocher_transaction(request):
	try:
		print("Des rapprochement", request)
		transaction_id = int(request.GET["transaction_id"])
		ligne_reception_id = int(request.GET["ligne_reception_id"])

		ligne_reception = dao_ligne_reception.toGetLigneReception(ligne_reception_id)

		#Problème du cancel engagement précédemment saisi !!! CECI EST UN CAS A TRAITER
		#Question ? Comment cancel les transactions engagés en ne connaissant que la ligne de reception
		#dao_transactionbudgetaire.toCancelEngagement(None, ligne_reception.bon_reception)

		is_done = dao_transactionbudgetaire.toSetRapprochementTransaction(transaction_id, ligne_reception.bon_reception, ligne_reception.ligne_budgetaire_id)
		data = {"is_success": True} if is_done else {"is_success": False}

		return JsonResponse(data, safe=False)

	except Exception as e:
		print(e)
		return JsonResponse([], safe=False)