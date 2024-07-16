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
from datetime import time, timedelta, datetime
import json
from django.db import transaction
import os
import pandas as pd
import calendar
import base64

from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ErpBackOffice.models import Model_Facture, Model_Paiement, Model_Transaction
from ErpBackOffice.dao.dao_type_facture import dao_type_facture

from ErpBackOffice.dao.dao_model import dao_model

from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task

#Import ErpBackOffice
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_document import dao_document
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_devise import dao_devise
from ModuleVente.dao.dao_type_article import dao_type_article
from ErpBackOffice.dao.dao_taux import dao_taux
from ModuleComptabilite.dao.dao_type_journal import dao_type_journal
from ErpBackOffice.dao.dao_moyen_paiement import dao_moyen_paiement
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_civilite import dao_civilite
from ModuleAchat.dao.dao_condition_reglement import dao_condition_reglement
from ErpBackOffice.dao.dao_facture_client import dao_facture_client
from ErpBackOffice.dao.dao_facture import dao_facture
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique_facture import dao_wkf_historique_facture
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation
from ErpBackOffice.dao.dao_wkf_historique_etat_facturation import dao_wkf_historique_etat_facturation

from ModuleAchat.dao.dao_document_bon_reception import dao_document_bon_reception

#Import module achat
from ModuleAchat.dao.dao_unite_achat_article import dao_unite_achat_article
from ModuleAchat.dao.dao_stock_article import dao_stock_article
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception

#Import module vente
from ModuleVente.dao.dao_bon_commande import dao_bon_commande
from ModuleVente.dao.dao_client import dao_client
from ModuleVente.dao.dao_article import dao_article
from ModuleVente.dao.dao_unite import dao_unite
from ModuleVente.dao.dao_categorie_unite import dao_categorie_unite
from ModuleVente.dao.dao_ligne_commande import dao_ligne_commande
from ModuleVente.dao.dao_bon_livraison import dao_bon_livraison
from ModuleVente.dao.dao_transaction_client import dao_transaction_client
from ModuleVente.dao.dao_paiement_client import dao_paiement_client
from ModuleVente.dao.dao_categorie_article import dao_categorie_article
from ModuleVente.dao.dao_categorie import dao_categorie
from ModuleVente.dao.dao_fournisseur_article import dao_fournisseur_article
from ModuleVente.dao.dao_etat_facturation import dao_etat_facturation
from ModuleVente.dao.dao_document_etat_facturation import dao_document_etat_facturation
from ModuleVente.dao.dao_recouvrement import dao_recouvrement
from ModuleVente.dao.dao_recouvrement_ligne import dao_recouvrement_ligne
from ModuleVente.dao.dao_relance_recouvrement import dao_relance_recouvrement


#Import module inventaire
from ModuleInventaire.dao.dao_type_emplacement import dao_type_emplacement
#from ModuleInventaire.dao.dao_stock_article import dao_stock_article
from ModuleInventaire.dao.dao_emplacement import dao_emplacement


from ModuleConversation.dao.dao_temp_notification import dao_temp_notification

#Import module Comptabilite
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleComptabilite.dao.dao_ecriture_comptable import dao_ecriture_comptable
from ModuleComptabilite.dao.dao_compte import dao_compte
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleComptabilite.dao.dao_ligne_facture import dao_ligne_facture
from ModuleComptabilite.dao.dao_taux_change import dao_taux_change
from ModuleComptabilite.dao.dao_document_facture import dao_document_facture


from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation

# Import ErpBackOffice.models
from ErpBackOffice.models import Model_Unite_fonctionnelle, Model_Budget, Model_Employe, Model_Image

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile

#Pagination
from ErpBackOffice.utils.pagination import pagination


#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module= "ModuleVente"
var_module_id = 2

#DASHBOARD
def get_dashboard(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(2, request)
	if response != None:
		return response
	#droit = "LISTER"
	NumberCategorieArticle= dao_categorie_article.toListCategoriesArticle().count()
	NumberFactureClient = dao_facture_client.toListFacturesClient().count()
	NumberBonCommande = dao_bon_commande.toListBonCommande()
	ListeBonLivraison = dao_bon_livraison.toListBonLivraison()
	Liste_Client = dao_client.toListClientsActifs()
	Liste_Entreprise = dao_client.toListClientsParticuliers()
	Liste_Particulier = dao_client.toListClientsEntreprises()
	EtatFac = dao_etat_facturation.toListEtatFacturation()
	List_Client, Nombre_Article = dao_facture_client.toGetClient_Number_Article()
	count_article = dao_article.toListArticlesCommercialisables().count
	Somme_Total_paiement = dao_facture_client.toGetPaiementTotal()

	#print('la liste des clients %s' %List_Client)
	#print('Nombre des articles %s' %Nombre_Article)
	#print('la liste des fournisseurs %s' %ListeFour)
	if response != None:
		return response

	#WAY OF NOTIFCATION
	module_name = "MODULE_VENTE"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()
	#print("way")
	#print(temp_notif_count)
	#END WAY

	model = dao_bon_commande.toListBonCommande()[:1]
	context = {
		'modules':modules,
		'sous_modules':sous_modules,
		'title' : 'Tableau de Bord',
		'model' : model,
		'utilisateur' : identite.utilisateur(request),
		'modules' : modules,
		'module' : ErpModule.MODULE_VENTE,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'menu' : 2,
		'temp_notif_count':temp_notif_count,
		'temp_notif_list':temp_notif_list,
		'numberclient' : Liste_Client.count(),
		'NumberCategorieArticle' : NumberCategorieArticle,
		'NumberFactureClient' : NumberFactureClient,
		'NumberBonCommande' : NumberBonCommande.count(),
		'ListeBonComnande' : NumberBonCommande[:4],
		'ListeBonLivraison':ListeBonLivraison[:4],
		'NumberEntreprise':Liste_Entreprise.count(),
		'NumberParticulier': Liste_Particulier.count(),
		'count_article':count_article,
		'Liste_Entreprise' : Liste_Entreprise,
		'Liste_Particulier' : Liste_Particulier,
		'Liste_Client': Liste_Client[:4],
		'EtatFac':EtatFac,
		'List_Client': List_Client,
		'Nombre_Article': Nombre_Article,
		'Somme_Total_paiement': Somme_Total_paiement
		}

	template = loader.get_template('ErpProject/ModuleVente/index.html')
	return HttpResponse(template.render(context, request))


#BON DE COMMANDE
def get_lister_bon_commande(request):
	try:
		permission_number = -1
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_bon_commande.toListBonCommande()
		model = dao_model.toListModel(dao_bon_commande.toListBonCommande(), permission_number, groupe_permissions, identite.utilisateur(request))
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste de Bon Commande',
			'model' : model,
			'utilisateur' : identite.utilisateur(request),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 15
			}

		template = loader.get_template('ErpProject/ModuleVente/bon_commande/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		pass

def get_creer_bon_commande(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(2, request)
	if response != None:
		return response

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Nouveau Bon Commande',
		'utilisateur' : identite.utilisateur(request),
		'clients': dao_client.toListClients(),
		'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
		'devises': dao_devise.toListDevises(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'articles': dao_article.toListArticles(),
		'categories': dao_categorie_article.toListCategoriesArticle(),
	    'modules' : modules,
		'module' : ErpModule.MODULE_VENTE,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleVente/bon_commande/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_bon_commande(request):

	try:
		auteur = identite.utilisateur(request)
		date_prevue = request.POST["date_prevue"]
		#print("start")
		# LA DATE EST AU FORMAT : dd/mm/yyyy
		# ON PROCEDE A LA CONVERSION DU STRING EN DATETIME
		#date = timezone.datetime(int(date_prevue[6:10]), int(date_prevue[3:5]), int(date_prevue[0:2]))

		date_prevue = date_prevue[6:10] + '-' + date_prevue[3:5] + '-' + date_prevue[0:2]
		date_prevue = datetime.strptime(date_prevue, "%Y-%m-%d").date()


		client_id = request.POST["client_id"]
		devise_id = request.POST["devise_id"]
		condition_reglement_id = request.POST["condition_reglement_id"]
		etat_actuel_id = int(request.POST["etat_actuel_id"])

		numero = dao_bon_commande.toGenerateNumeroCommande()
		bon_commande = dao_bon_commande.t
		bon_commande = dao_bon_commande.toSaveBonReception(auteur, bon_commande)

		#print("bon saved")

		if bon_commande != None :
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					bon_commande.document = doc.doc
					bon_commande.save()
				Model_Image.objects.all().delete()

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
				#On stock l'article à l'emplacement d'entrée
				type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
				emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
				les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement.id)
				stock = les_stocks[0]
				unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_achat_id = unite_achat.id if unite_achat else None

				#print("BC ID %s" % bon_commande.id)
				ligne = dao_ligne_commande.toCreateLigneReception(bon_commande.id, article.id, quantite_demandee, prix_unitaire, unite_achat_id)
				ligne = dao_ligne_commande.toSaveLigneReception(ligne)

				#On rajoute le stock_article
				ligne.stock_article_id = stock.id
				ligne.save()

			#print('lignes fini')
			# WORKFLOWS INITIALS
			type_document = "Bon de commande"
			workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)

			if workflow != None:
				etape = dao_wkf_etape.toGetEtapeInitialWorkflow(workflow.id)
				bon_commande.statut_id = etape.id
				bon_commande.etat = etape.designation
				bon_commande.save()

				#print("AUTEUR %s" % auteur.id)

				historique = dao_wkf_historique_commande.toCreateHistoriqueWorkflow(auteur.id, etape.id, bon_commande.id)
				historique = dao_wkf_historique_commande.toSaveHistoriqueWorkflow(historique)

				#CHANGEMENT DE L'ETAT DE L'ETAT DE BESOIN
				if etat_actuel_id != 0:
					etape_id = request.POST["etape_wkf"]
					demande_id = request.POST["demande_wkf"]
					utilisateur_id = request.user.id

					#print("print 1 %s %s %s" % (utilisateur_id, etape_id, demande_id))

					employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
					etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
					demande_achat = dao_demande_achat.toGetDemande(demande_id)

					#print("print 2 %s %s %s " % (employe, etape, demande_achat))

					transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(demande_achat.statut_id)
					for item in transitions_etapes_suivantes:


						# Gestion des transitions dans le document
						demande_achat.statut_id = etape.id
						demande_achat.etat = etape.designation
						demande_achat.save()

					historique = dao_wkf_historique_demande.toCreateHistoriqueWorkflow(employe.id, etape.id, demande_achat.id)
					historique = dao_wkf_historique_demande.toSaveHistoriqueWorkflow(historique)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_vente_detail_bon_commande', args=(bon_commande.id,)))
	except Exception as e:
		module='ModuleVente'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_bon_commande'))

def get_lister_ligne_reception(request):
	data = {}
	try:
		lignes = []
		id = int(request.GET["ref"])
		fourniture = dao_bon_reception.toGetBonReception(id)
		lignes_fourniture = dao_ligne_reception.toListLigneOfReceptions(fourniture.id)
		devise_ref = dao_devise.toGetDeviseReference()
		symbole_devise = devise_ref.symbole_devise
		if fourniture.devise != None:
			symbole_devise : fourniture.devise.symbole_devise
		for item in lignes_fourniture :
			ligne = {
				"ligne_id" : item.id,
				"nom_article" : item.stock_article.article.designation,
				"quantite_fournie" : item.quantite_fournie,
				"prix_unitaire" : item.prix_unitaire,
				"prix_lot" : item.prix_lot,
				"symbole_unite" : item.unite_achat.unite.symbole_unite
			}
			lignes.append(ligne)
		data = {
			"prix_total" : fourniture.prix_total,
			"symbole_devise" : symbole_devise,
			"reference_document" : fourniture.reference_document,
			"lignes" : lignes
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("ERREUR")
		#print(e)
		return JsonResponse(data, safe=False)


#CIVILITE
def get_lister_civilite(request):
	try :
		permission_number = 33
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response


		# model = dao_civilite.toListCivilite()
		model = dao_model.toListModel(dao_civilite.toListCivilite(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)

		#print('id ezo ya %s'%(model))
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des civilités',
			'view':view,
			'model': model,
			'utilisateur': utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules': modules,
			'module': ErpModule.MODULE_VENTE,
			'menu': 8,
		}
		template = loader.get_template("ErpProject/ModuleVente/civilite/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER CiviliteS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Civilite')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_civilite'))

def get_creer_civilite(request):
	try:
		permission_number = 34
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title':'Nouvelle Civilité',
			'utilisateur': utilisateur,
			'isPopup': isPopup,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules': modules,
			'module': ErpModule.MODULE_VENTE,
			'menu': 8,
		}
		template = loader.get_template("ErpProject/ModuleVente/civilite/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER CiviliteS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Creer Civilite')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_civilite'))


def post_creer_civilite(request):

	try:
		designation = request.POST["designation"]
		designation_court = request.POST["designation_court"]

		civilite = dao_civilite.toCreateCivilite(designation, designation_court)
		civilite = dao_civilite.toSaveCivilite(civilite)

		if civilite != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_vente_details_civilite', args = (civilite.id)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur s'est produite lors de la création de la civilité.")
			return HttpResponseRedirect(reverse('module_vente_list_civilite'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER Post CiviliteS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Creer Civilite')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_civilite'))

def get_details_civilite(request, ref):
	try:
		permission_number = 33
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		civilite = dao_civilite.toGetCivilite(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,civilite)


		#print('civilite %s' % (civilite))

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' :civilite.designation,
			'model' : civilite,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleVente/civilite/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE GET MODIFIER CiviliteS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get details  Civilite')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_civilite'))

def get_modifier_civilite(request, ref):
	try:
		permission_number = 36
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		#print("errr",ref)
		id = int(ref)
		civilite = dao_civilite.toGetCivilite(id)
		#print('try civilite %s'%(civilite))
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title':'Nouvelle Civilité',
			'model':civilite,
			'utilisateur': utilisateur,
			'model': civilite,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules': modules,
			'module': ErpModule.MODULE_VENTE,
			'menu': 8,
		}
		template = loader.get_template("ErpProject/ModuleVente/civilite/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e :
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER Post CiviliteS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get modifier Civilite')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_civilite'))

def post_modifier_civilite(request):
	id = int(request.POST["ref"])
	try:
		civilite = dao_civilite.toGetCivilite(id)
		designation = request.POST["designation"]
		designation_court = request.POST["designation_court"]

		civilite.designation = designation
		civilite.designation_court = designation_court

		is_done = dao_civilite.toUpdateCivilite(designation, designation_court)

		if is_done == True : return HttpResponseRedirect(reverse('module_vente_details_civilite', args = (civilite.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur s'est produite lors de la modification de la civilité.")
			return HttpResponseRedirect(reverse('module_vente_update_civilite', args =(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER Post CiviliteS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post modifier Civilite')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_update_civilite'))

#CLIENT
def get_lister_clients(request):
	try:
		permission_number = 28
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		# model = dao_client.toListClientsActifs()
		model = dao_model.toListModel(dao_client.toListClientsActifs(), permission_number, groupe_permissions, identite.utilisateur(request))
		#Traitement des vues
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des clients',
			'model' : model,
			"utilisateur" : utilisateur,
			'view': view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_CLIENT',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CLIENT',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleVente/client/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA LISTE CLIENTS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Liste Client')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_clients'))

def get_creer_client(request):

	try:
		permission_number = 25
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Nouveau client',
			'pays' : dao_place.toListPlacesOfType(1),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'civilites': dao_civilite.toListCivilite(),
			'comptes': dao_compte.toListComptesDeClasse(4),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 3,
			'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
		}
		template = loader.get_template("ErpProject/ModuleVente/client/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER CLIENTS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Creer Client')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_clients'))

def post_creer_client(request):

	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		nom_complet = request.POST["nom_complet"]
		est_particulier = request.POST["est_particulier"]
		est_particulier = True if est_particulier == "1" else False
		email = request.POST["email"]
		phone = request.POST["phone"]
		adresse = request.POST["adresse"]
		commune_quartier_id = request.POST["commune_quartier_id"]
		civilite_id = request.POST["civilite_id"]
		if civilite_id == "" :
			civilite_id = None
		langue = request.POST["langue"]
		image = ""
		est_actif = True
		compte_id = request.POST["compte_id"]
		if est_particulier:
			lieu_de_naissance = request.POST["lieu_naissance"]
			date_de_naissance = request.POST["date_naissance"]
		else:
			lieu_de_naissance = request.POST["siege"]
			date_de_naissance = request.POST["date_creation"]
		if date_de_naissance == "":
			date_de_naissance = "2020-01-01"
		sexe = request.POST["sexe"]
		personne_contact = request.POST["personne_contact"]
		nui = request.POST["nui"]
		bp = request.POST["bp"]
		raison_soc = request.POST["raison_soc"]
		fax = request.POST["fax"]
		reglement = request.POST["reglement"]
		fiscal = request.POST["fiscal"]
		autre_info = request.POST["autre_info"]
		numero_compte_b = request.POST["compteB"]




		#compte = dao_compte.toGetCompteClient()

		client = dao_client.toCreateClient(nom_complet,None,None, nom_complet ,image,email,phone,adresse,commune_quartier_id, langue, est_actif,lieu_de_naissance,date_de_naissance,sexe, compte_id,est_particulier, civilite_id)
		client = dao_client.toSaveClient(auteur,client)
		client.numero_compte_b = numero_compte_b
		client.personne_contact = personne_contact
		client.nui = nui
		client.bp = bp
		client.raison_sociale = raison_soc
		client.fax = fax
		client.mode_reglement.id = reglement
		client.fiscale = fiscal
		client.autre_info = autre_info
		client.save()

		if client != None :
			image_string = request.POST["image_upload_string"]
			if image_string != "":
				_, b64data = image_string.split(',')
				#print(b64data)
				client_img_dir = 'personnes/'
				media_dir = media_dir + '/' + client_img_dir
				save_path = os.path.join(media_dir, str(client.id) + ".jpg")

				file = open(save_path, "wb")
				decoded = base64.decodestring(b64data)
				file.write(decoded)
				file.close()

				#On affecte le chemin de l'Image
				client.image = media_url + client_img_dir + str(client.id) + ".jpg"
				client.save()
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_vente_details_client", args=(client.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du client")
			return HttpResponseRedirect(reverse('module_vente_add_client'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER CLIENTS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Creer Client')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_clients'))

def get_modifier_client(request, ref):

	try:
		permission_number = 26
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		client = dao_client.toGetClient(id)
		pays = province = ville = commune = None
		#print("QUARTIER")
		#print(client.commune_quartier_id)
		if client.commune_quartier_id != None and client.commune_quartier_id != 0:
			#print("ICI")
			commune = dao_place.toGetPlace(client.commune_quartier_id)
			ville = dao_place.toGetPlace(commune.parent_id)
			province = dao_place.toGetPlace(ville.parent_id)
			pays = dao_place.toGetPlace(province.parent_id)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % client.nom_complet,
			'pays' : dao_place.toListPlacesOfType(1),
			'le_pays' : pays,
			'civilites': dao_civilite.toListCivilite(),
			'provinces':dao_place.toListPlacesOfType(2),
			'la_province' : province,
			'la_ville' : ville,
			'villes':dao_place.toListPlacesOfType(3),
			'la_commune' : commune,
			'comptes': dao_compte.toListComptesDeClasse(4),
			'communes': dao_place.toListPlacesOfType(4),
			'model' : client,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 3,
			'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),

		}
		template = loader.get_template("ErpProject/ModuleVente/client/update.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU MODIFIER CLIENTS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Client')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_clients'))

def post_modifier_client(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		identifiant = int(request.POST["ref"])
		nom_complet = request.POST["nom_complet"]

		est_particulier = request.POST["est_particulier"]
		est_particulier = True if est_particulier == "1" else False
		#if est_particulier == 1 : est_particulier = True
		#print("est parti", est_particulier)
		email = request.POST["email"]
		phone = request.POST["phone"]
		adresse = request.POST["adresse"]
		#print('etape 1')

		commune_quartier_id = int(request.POST["commune_quartier_id"])
		#print('commune_quartier_id %s'%(commune_quartier_id))

		#categorie_id = int(request.POST["categorie_id"])
		#print('etape 2 %s'%(categorie_id))

		civilite_id = request.POST["civilite_id"]
		if civilite_id == "" :
			civilite_id = None
		compte_id = request.POST["compte_id"]
		if est_particulier:
			lieu_de_naissance = request.POST["lieu_naissance"]
			date_de_naissance = request.POST["date_naissance"]
		else:
			lieu_de_naissance = request.POST["siege"]
			date_de_naissance = request.POST["date_creation"]
		if date_de_naissance == "":
			date_de_naissance = "2020-01-01"
		sexe = request.POST["sexe"]


		langue = request.POST["langue"]
		#print("la langue**********", langue)
		personne_contact = request.POST["personne_contact"]
		nui = request.POST["nui"]
		bp = request.POST["bp"]
		raison_soc = request.POST["raison_soc"]
		fax = request.POST["fax"]
		reglement = request.POST["reglement"]
		fiscal = request.POST["fiscal"]
		autre_info = request.POST["autre_info"]
		numero_compte_b = request.POST["compteB"]

		image_string = request.POST["image_upload_string"]
		#print('etape 3')
		if image_string != "":
			_, b64data = image_string.split(',')
			#print(b64data)
			client_img_dir = 'personnes/'
			media_dir = media_dir + '/' + client_img_dir
			save_path = os.path.join(media_dir, str(id) + ".jpg")

			file = open(save_path, "wb")
			decoded = base64.decodestring(b64data)
			file.write(decoded)
			file.close()
			#On affecte le chemin de l'Image
			image = media_url + client_img_dir + str(id) + ".jpg"

		else : image = ""
		#print('etape 4')
		#personne = dao_personne.toCreatePersonne(auteur, nom_complet, image, est_particulier, adresse, commune_quartier_id, categorie_id, civilite_id, phone, email, langue_id)
		client = dao_client.toCreateClient(nom_complet,None,None, nom_complet ,image,email,phone,adresse,commune_quartier_id, langue, True,lieu_de_naissance,date_de_naissance,sexe, compte_id,est_particulier, civilite_id)
		compte = dao_compte.toGetCompteClient()
		if client.compte_id == None and compte != None:
			client.compte_id = compte.id

		is_done = dao_client.toUpdateClient(identifiant, client)
		monclient = dao_client.toGetClient(identifiant)
		client.numero_compte_b = numero_compte_b
		monclient.personne_contact = personne_contact
		monclient.nui = nui
		monclient.bp = bp
		monclient.raison_sociale = raison_soc
		monclient.fax = fax
		monclient.mode_reglement.id = reglement
		monclient.fiscale = fiscal
		monclient.autre_info = autre_info
		monclient.save()
		if is_done != False : return HttpResponseRedirect(reverse('module_vente_details_client', args=(id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la modification des informations du client")
			return HttpResponseRedirect(reverse('module_vente_update_client', args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS POST DU MODIFIER CLIENTS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier Client')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_clients'))

def get_details_client(request, ref):

	try:
		permission_number = 28
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		client = dao_client.toGetClient(ref)

		factures = dao_facture_client.toListFacturesClientOfClient(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,client)



		context = {
			'title' : client.nom_complet,
			'model' : client,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			"sous_modules": sous_modules,
			"modules" : modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"factures" : factures,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleVente/client/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS POST DU DETAIL CLIENTS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detail Client')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_clients'))

def get_details_bon_commande(request,ref):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		bon_commande=dao_bon_commande.toGetBonCommande(ref)
		template = loader.get_template('ErpProject/ModuleVente/bon_commande/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_commande)


		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details d une bon_commande','bon_commande' : bon_commande,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_bon_commande'))

#LIGNE DE COMMANDE
def get_lister_ligne_commande(request):
	try:
		permission_number = -1
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_ligne_commande.toListLigneCommande()
		model = dao_model.toListModel(dao_ligne_commande.toListLigneCommande(), permission_number, groupe_permissions, identite.utilisateur(request))
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste de ligne_commande',
			'model' : model,
			'utilisateur' : identite.utilisateur(request),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'menu' : 2
			}
		template = loader.get_template('ErpProject/ModuleVente/ligne_commande/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		pass
		# auteur = identite.utilisateur(request)
		# module='ModuleVente'
		# monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES LISTES LIGNES\n {}".format(auteur.nom_complet, module, e))
		# monLog.debug("Info")
		# #print('Erreut Get Detail')
		# #print(e)
		# return HttpResponseRedirect(reverse('module_vente_list_condition_reglement'))


def get_creer_ligne_commande(request):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Nouvelle ligne_commande','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleVente/ligne_commande/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_ligne_commande(request):

	try:
		quantite_demandee = request.POST['quantite_demandee']
		quantite_fournie = request.POST['quantite_fournie']
		prix_unitaire = request.POST['prix_unitaire']
		prix_lot = request.POST['prix_lot']
		type = request.POST['type']
		bon_commande_id = request.POST['bon_commande_id']
		stock_article_id = request.POST['stock_article_id']

		auteur = identite.utilisateur(request)

		ligne_commande=dao_ligne_commande.toCreateLigneCommande(quantite_demandee,quantite_fournie,prix_unitaire,prix_lot,type,bon_commande_id,stock_article_id)
		ligne_commande=dao_ligne_commande.toSaveLigneCommande(auteur,ligne_commande)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# HttpResponseRedirect(reverse('module_vente_list_ligne_commande'))
		return HttpResponseRedirect(reverse('module_vente_detail_ligne_commande', args=(ligne_commande.id,)))
	except Exception as e:
		module='ModuleVente'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_ligne_commande'))


def get_details_ligne_commande(request,ref):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		ligne_commande=dao_ligne_commande.toGetLigneCommande(ref)
		template = loader.get_template('ErpProject/ModuleVente/ligne_commande/item.html')
		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details d\'une ligne_commande','ligne_commande' : ligne_commande,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_ligne_commande'))

'''def get_details_condition_reglement(request, ref):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))
	try:
		ref=int(ref)
		condition_reglement=dao_condition_reglement.toGetConditionReglement(ref)
		template = loader.get_template('ErpProject/ModuleVente/condition_reglement/item.html')
		context ={'title' : 'Details d une condition_reglement','condition_reglement' : condition_reglement,'utilisateur' : identite.utilisateur(request),'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_VENTE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_condition_reglement'))'''


# FACTURE CLIENT CONTROLLER
def get_lister_factures_client(request):

	permission_number = 297
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response


	# model = dao_facture_client.toListFacturesClient()
	model = dao_model.toListModel(dao_facture_client.toListFacturesClient(), permission_number, groupe_permissions, identite.utilisateur(request))
	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des factures clients',
		'model' : model,
		"utilisateur" : utilisateur,
		#"can_create" : dao_droit.toGetDroitRole('CREER_FACTURE_CLIENT',nom_role,utilisateur.nom_complet),
		#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_FACTURE_CLIENT',nom_role,utilisateur.nom_complet),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		"module" : ErpModule.MODULE_VENTE,
		'menu' : 21
	}
	template = loader.get_template("ErpProject/ModuleVente/facture/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_facture_client(request, ref):
	try:
		permission_number = 298
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		devises = dao_devise.toListDevisesActives()
		articles = dao_article.toListArticlesVendables()
		categories = dao_categorie_article.toListCategoriesArticle()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Nouvelle facture',
			'client' : dao_client.toGetClient(ref),
			'commandes' : dao_bon_commande.toListCommandes(),
			'devises' : devises,
			'articles' : articles,
			'categories' : categories,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleVente/facture/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST CREER TAUX")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_list_factures_client"))

def post_valider_facture_client(request):
	try:

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		numero_facture = request.POST["numero_facture"]
		if None == numero_facture or "" == numero_facture: numero_facture = dao_facture.toGenerateNumeroFacture()

		date_facturation = request.POST["date_facturation"]

		order_id = int(request.POST["order_id"])
		order = None
		type_facture = 0

		if order_id != 0:
			#print("BON DE COMMANDE")
			order = dao_bon_commande.toGetBonCommande(order_id)
			montant = order.prix_total

			comptes = dao_compte.toListComptes()
			devise = dao_devise.toGetDevise(order.devise_id)
			client = dao_client.toGetClient(order.client_id)
			compte_client = dao_compte.toGetCompteClient()
			if client.compte != None: compte_client = dao_compte.toGetCompte(client.compte_id)
			#print(compte_client)
			#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

			#Format ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
			ecritures_debit = []
			ecriture = {
				"id" : compte_client.id,
				"libelle" : client.nom_complet,
				"compte" : "%s %s" % (compte_client.numero, compte_client.designation),
				"montant" : montant
			}
			ecritures_debit.append(ecriture)

			#Format Facture
			facture = {
				"date_facturation" : date_facturation,
				"numero_facture" : numero_facture,
				"montant" : montant,
				"order_id" : order_id
			}

			#Format lignes facture et ecriture débit (dans le constat d'achat, les ecritures de debit dependent des lignes de facture)
			ecritures_credit = []
			lignes_facture = []
			lignes_commande = dao_ligne_commande.toListLigneOfCommandes(order.id)
			for item in lignes_commande :
				prix_unitaire = item.prix_unitaire
				total = item.prix_unitaire * item.quantite_fournie
				if 0 != item.prix_lot:
					total = item.prix_lot
					prix_unitaire = "-"

				#format lignes facture
				ligne = {
					"nom_article" : item.stock_article.article.designation,
					"quantite" : item.quantite_fournie,
					"prix_unitaire" : prix_unitaire,
					"prix_total" : total,
					"symbole_unite" : item.unite_achat.unite.symbole_unite
				}
				lignes_facture.append(ligne)


				article = dao_article.toGetArticle(item.stock_article.article.id)

				compte_article = dao_compte.toGetCompteMarchandise()
				if article.compte != None: compte_article = dao_compte.toGetCompte(article.compte_id)

				#format ecriture debit
				ecriture = {
					"id" : compte_article.id,
					"libelle" : article.designation,
					"compte" : "%s %s" % (compte_article.numero, compte_article.designation),
					"montant" : item.total
				}
				ecritures_credit.append(ecriture)

		else :
			#print("LIGNE FACTURE")
			type_facture = 1
			#Format lignes facture et ecriture débit en cas de ligne facture (dans le constat d'achat, les ecritures de debit dependent des lignes de facture)
			ecritures_credit = []
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
				#unite_achat_id = unite_achat.id if unite_achat else None

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

				compte_article = dao_compte.toGetCompteMarchandise()
				if article.compte != None: compte_article = dao_compte.toGetCompte(article.compte_id)

				#format ecriture debit
				ecriture = {
					"id" : compte_article.id,
					"libelle" : article.designation,
					"compte" : "%s %s" % (compte_article.numero, compte_article.designation),
					"montant" : total
				}
				ecritures_credit.append(ecriture)

			montant = total_fact

			comptes = dao_compte.toListComptes()
			devise_id = request.POST["devise_id"]
			devise = dao_devise.toGetDevise(devise_id)
			client_id = request.POST["client_id"]
			client = dao_client.toGetClient(client_id)
			#print("FIN 0")
			compte_client = dao_compte.toGetCompteClient()
			#print("COMPTE CLI")
			if client.compte != None: compte_client = dao_compte.toGetCompte(client.compte_id)
			#print(compte_client)
			#print("FIN 1")
			#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

			#Format ecriture crédit (dans le constat d'achat, c'est le compte du fournisseur qu'on crédite)
			ecritures_debit = []
			ecriture = {
				"id" : compte_client.id,
				"libelle" : client.nom_complet,
				"compte" : "%s %s" % (compte_client.numero, compte_client.designation),
				"montant" : montant
			}
			ecritures_debit.append(ecriture)
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
			'devise' : devise,
			'client' : client,
			'comptes'   : comptes,
			'bon_achat' : order,
			'lignes_facture' : lignes_facture,
			'ecritures_credit': ecritures_credit,
			'ecritures_debit' : ecritures_debit,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleVente/facture/validate.html")
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

		auteur = identite.utilisateur(request)
		numero_facture = request.POST["numero_facture"]
		date_facturation = request.POST["date_facturation"]
		date_facturation = timezone.datetime(int(date_facturation[6:10]), int(date_facturation[3:5]), int(date_facturation[0:2]))
		order_id = request.POST["order_id"]
		client_id = int(request.POST["client_id"])
		type_facture = int(request.POST["type_facture"])
		dev_id = request.POST["devise_id"]


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
		type_journal = dao_type_journal.toGetTypeVente()
		#print(type_journal)
		journal_vente = dao_journal.toGetJournalDefautOf(type_journal["id"])
		journal_id = None
		if journal_vente != None: journal_id = journal_vente.id
		#print("Journal recuperee")

		if type_facture == 0:
			order = dao_bon_commande.toGetBonCommande(order_id)
			montant = order.prix_total
			facture = dao_facture_client.toCreateFactureClient(date_facturation, numero_facture, montant, order_id, None,"","", client_id)
			facture = dao_facture_client.toSaveFactureClient(auteur, facture)

			if devise_ref.id != order.devise_id:
				#print("Les taux sont différents ...")
				taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(order.devise_id)
				if taux != None: taux_id = taux.id

			#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables
			piece_comptable = dao_piece_comptable.toCreatePieceComptable(order.numero_commande, order.reference_document, montant, journal_id, date_piece, client.id, order.id, None , facture.id, "CONSTAT DE VENTE", order.devise_id, taux_id)
			piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
			#print("piece cree")

			#On commmence la création de la facture, en formant les écritures qui seront générées et les lignes de facture à partir des lignes de commande

			#Creation ecriture crédit (dans le constat de vente, c'est le compte du client qu'on débite)
			#On cree l'ecriture de débit
			ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(client.nom_complet, montant , 0 , compte_client.id, piece_comptable.id)
			ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
			ecriture_debit.save()
			#print("ecriture_debit {} cree".format(ecriture_debit.id))

			lignes = dao_ligne_reception.toListLigneOfReceptions(order.id)

		elif type_facture == 1:
			#print("FACT 1")
			montant = 0.0

			facture = dao_facture_client.toCreateFactureClient(date_facturation, numero_facture, 0, None, None,"","", client_id)
			facture = dao_facture_client.toSaveFactureClient(auteur, facture)

			#print("FACT SAVED")
			list_article_id = request.POST.getlist('article_id', None)
			list_quantite_demandee = request.POST.getlist("qte", None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
			#print("DEBUT LIGNES")
			#print(len(list_article_id))
			#print(len(list_quantite_demandee))
			#print(len(list_prix_unitaire))
			for i in range(0, len(list_article_id)) :
				#print("ART ID %s" % list_article_id[i])
				#print("QTE %s" % list_quantite_demandee)
				#print("PRIX %s" % list_prix_unitaire)

				article_id = list_article_id[i]
				quantite_demandee = makeFloat(list_quantite_demandee[i].replace(',','.'))
				prix_unitaire = makeFloat(list_prix_unitaire[i].replace(',','.'))

				article = dao_article.toGetArticle(article_id)
				unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_achat_id = unite_achat.id if unite_achat else None

				prix_unitaire = prix_unitaire
				total = prix_unitaire * quantite_demandee
				montant = makeFloat(montant) + makeFloat(total)

				type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
				emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
				les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement.id)
				stock = les_stocks[0]

				ligne = dao_ligne_facture.toCreateLigneFacture(facture.id, article.id, quantite_demandee, prix_unitaire, unite_achat_id)
				ligne = dao_ligne_facture.toSaveLigneFacture(ligne)

				#On rajoute le stock_article
				ligne.stock_article_id = stock.id
				ligne.save()

			#print("Fin LIGNES")

			facture.montant = montant
			facture.save()

			#print("FACT UPDATED")
			if devise_ref.id != dev_id:
				#print("Les taux sont différents ...")
				taux = dao_taux_change.toGetTauxCourantDeLaDeviseArrive(dev_id)
				if taux != None: taux_id = taux.id

			#On crée la pièce comptable liée à cette facture et qui contiendra les écritures comptables

			piece_comptable = dao_piece_comptable.toCreatePieceComptable(facture.numero_facture, None, montant, journal_id, date_piece, client_id, None, None, facture.id, "CONSTAT DE VENTE", dev_id , taux_id)
			piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
			#print("piece cree")

			#Creation ecriture crédit (dans le constat de vente, c'est le compte du client qu'on débite)
			#On cree l'ecriture de débit


			ecriture_debit = dao_ecriture_comptable.toCreateEcritureComptable(client.nom_complet, montant , 0, compte_client.id, piece_comptable.id)
			ecriture_debit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
			ecriture_debit.save()
			#print("ecriture_debit {} cree".format(ecriture_debit.id))

			lignes = dao_ligne_facture.toListLigneOfFacture(facture.id)

		if facture != None :
			#print("Facture {} creee".format(facture.id))
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					facture.document = doc.doc
					facture.save()
				Model_Image.objects.all().delete()


			#Creation les ecriture Crédit (dans le constat de vente, ce sont les comptes des éléments des lignes de facture, ici les articles, qui sont crédité)

			for item in lignes:
				#print("ok")
				stock_article = dao_stock_article.toGetStockArticle(item.stock_article_id)
				article = dao_article.toGetArticle(stock_article.article_id)

				compte_article = dao_compte.toGetCompteMarchandise()
				if article.compte != None: compte_article = dao_compte.toGetCompte(article.compte_id)
				#print("compte_article recupere")
				#print(compte_article)

				#On cree l'ecriture de crédit
				ecriture_credit = dao_ecriture_comptable.toCreateEcritureComptable(article.designation, 0 ,item.total, compte_article.id, piece_comptable.id)
				ecriture_credit = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
				ecriture_credit.save()
				#print("ecriture_credit {} cree".format(ecriture_credit.id))


			# WORKFLOWS INITIALS
			#print("Debut workflow")
			type_document = "Facture client"
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
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse('module_vente_details_facture_client', args=(facture.id,)))
		else :
			transaction.savepoint_rollback(sid)
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la facture")
			return HttpResponseRedirect(reverse('module_vente_list_facture_client'))
	except Exception as e:
		#print("ERREUR POST CREER FACTURE FOURNISSEUR!")
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_facture_client'))

def get_modifier_facture_client(request, ref):
	permission_number = 299
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
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % title,
			'model' : facture,
			'menu' : 21,
			'lignes' : lignes,
			'bon'   : bon_reception,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
		}
		template = loader.get_template("ErpProject/ModuleVente/facture/update.html")
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

		if is_done != False : return HttpResponseRedirect(reverse('module_comptabilite_details_facture', args=(facture.id,)))
		else : return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(facture.id,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_update_facture_fournisseur', args=(id,)))

def get_details_facture_client(request, ref):
	try:
		permission_number = 297
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response


		ref = int(ref)
		facture = dao_facture_client.toGetFactureClient(ref)
		bon_reception = dao_bon_reception.toGetBonReception(facture.bon_reception_id)
		montant_paye = facture.montant_paye
		montant_restant = facture.montant_restant

		#historique = dao_wkf_historique_facture.toListHistoriqueOfFacture(facture.id)
		#transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(facture.statut_id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,facture)

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

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'model' : facture,
			'type_facture' : type_facture,
			'bon'   : bon_reception,
			'historique' : historique,
			'lignes' : lignes,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
    		"roles": groupe_permissions,
			'menu' : 21,
			"utilisateur" : utilisateur,
			#"can_create" : dao_droit.toGetDroitRole('CREER_FACTURE_FOURNISSEUR',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_FACTURE_FOURNISSEUR',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_FACTURE_FOURNISSEUR',nom_role,utilisateur.nom_complet),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'montant_paye' : montant_paye,
			'montant_restant' : montant_restant
		}
		template = loader.get_template("ErpProject/ModuleVente/facture/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

@transaction.atomic
def post_workflow_facture(request):
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
					doc = dao_document.toUploadDocument(auteur,nom_fichier,facture)

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
			return HttpResponseRedirect(reverse('module_vente_details_facture_client', args=(facture_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_vente_details_facture_client', args=(facture_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_facture_client'))


# ETAT DE FACTURATION

def get_lister_etat_facturation(request):
	permission_number = 310
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_etat_facturation.toListEtatFacturation()
	model = dao_model.toListModel(dao_etat_facturation.toListEtatFacturation(), permission_number, groupe_permissions, identite.utilisateur(request))
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des états de facturation',
		'model' : model,
		'view':view,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		"module" : ErpModule.MODULE_VENTE,
		'menu' : 21
	}
	template = loader.get_template("ErpProject/ModuleVente/etat_facturation/list.html")
	return HttpResponse(template.render(context, request))

def get_creer_etat_facturation(request):
	permission_number = 309
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response


	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Créer un état de facturation',
		#'model' : model,
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		"module" : ErpModule.MODULE_VENTE,
		'menu' : 21
	}
	template = loader.get_template("ErpProject/ModuleVente/etat_facturation/add.html")
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_etat_facturation(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		date_prevue = request.POST["date"]

		#print("start")

		# LA DATE EST AU FORMAT : dd/mm/yyyy
		# ON PROCEDE A LA CONVERSION DU STRING EN DATETIME
		#date = timezone.datetime(int(date_prevue[6:10]), int(date_prevue[3:5]), int(date_prevue[0:2]))

		date_prevue = date_prevue[6:10] + '-' + date_prevue[3:5] + '-' + date_prevue[0:2]
		date_prevue = datetime.strptime(date_prevue, "%Y-%m-%d").date()

		description = request.POST["description"]

		numero = dao_etat_facturation.toGenerateNumeroEtatFacturation()
		etat_facturation = dao_etat_facturation.toCreateEtatFacturation(numero,description,date_prevue,None)
		etat_facturation = dao_etat_facturation.toSaveEtatFacturation(auteur, etat_facturation)

		#print(etat_facturation)
		if etat_facturation != None :
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					etat_facturation.document = doc.doc
					etat_facturation.save()
				Model_Image.objects.all().delete()
		#print("Debut WKF")
		#Initialisation du workflow expression
		wkf_task.initializeWorkflow(auteur,etat_facturation)
		#print("FIN WKF")

		if etat_facturation != None:
			if 'file_upload' in request.FILES:
				files = request.FILES.getlist("file_upload",None)
				#print("here we are")
				document = dao_document.toUploadDocument(auteur,files,etat_facturation)
				#print("we are out")
				etat_facturation.document_id = document.id
				etat_facturation.save()

			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(expression.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_vente_details_etat_facturation', args=(etat_facturation.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de l'article")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_vente_add_etat_facturation'))

	except Exception as e:

		messages.error(request,e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_vente_add_etat_facturation'))

def get_details_etat_facturation(request, ref):
	try:
		permission_number = 311
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		etat_facturation = dao_etat_facturation.toGetEtatFacturation(ref)
		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,etat_facturation)

		#documents = dao_document_etat_facturation.toListDocumentbyEtat(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Etat de facturation N° %s" % etat_facturation.numero_etat_facturation,
			'model' : etat_facturation,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'content_type_id':content_type_id,
			'menu' : 21,
			"signee":signee,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"documents" : documents,
			'roles':groupe_permissions,
			"organisation":dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
		}
		template = loader.get_template("ErpProject/ModuleVente/etat_facturation/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_comptabilite_list_factures_fournisseur'))

@transaction.atomic
def post_workflow_etat_facturation(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		etat_facturation_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, etat_facturation_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		etat_facturation = dao_etat_facturation.toGetEtatFacturation(etat_facturation_id)

		#print("print 2 %s %s %s " % (employe, etape, etat_facturation))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(etat_facturation.statut_id)
		for item in transitions_etapes_suivantes:

			#print("Autres")
			# Gestion des transitions dans le document
			etat_facturation.statut_id = etape.id
			etat_facturation.etat = etape.designation
			etat_facturation.save()

		historique = dao_wkf_historique_etat_facturation.toCreateHistoriqueWorkflow(employe.id, etape.id, etat_facturation.id)
		historique = dao_wkf_historique_etat_facturation.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_vente_details_etat_facturation', args=(etat_facturation_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_vente_details_etat_facturation', args=(etat_facturation_id,)))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_etat_facturation'))

#BON DE LIVRAISON
def get_lister_bon_livraison(request):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_bon_livraison.toListBonLivraison()
	model = dao_model.toListModel(dao_bon_livraison.toListBonLivraison(), permission_number, groupe_permissions, identite.utilisateur(request))

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste de Bon Livraison','model' : model,'utilisateur' : identite.utilisateur(request),'modules' : modules, 'module' : ErpModule.MODULE_VENTE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleVente/bon_livraison/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_bon_livraison(request):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Nouveau Bon Commande',
		'utilisateur' : identite.utilisateur(request),
		'clients': dao_client.toListClients(),
		'conditions_reglement' : dao_condition_reglement.toListConditionsReglement(),
		'devises': dao_devise.toListDevises(),
		'articles': dao_article.toListArticles(),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'categories': dao_categorie_article.toListCategoriesArticle(),
	    'modules' : modules,
		'module' : ErpModule.MODULE_VENTE,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleVente/bon_livraison/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_bon_livraison(request):

	try:
		numero_livraison = request.POST['numero_livraison']
		date_livraison = request.POST['date_livraison']
		quantite_demandee = request.POST['quantite_demandee']
		quantite_recue = request.POST['quantite_recue']
		bon_commande_id = request.POST['bon_commande_id']
		document_id = request.POST['document_id']

		bon_livraison=dao_bon_livraison.toCreateBonLivraison(numero_livraison,date_livraison,quantite_demandee,quantite_recue,bon_commande_id,document_id)
		bon_livraison=dao_bon_livraison.toSaveBonLivraison(identite.utilisateur(request),bon_livraison)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# return HttpResponseRedirect(reverse('module_vente_list_bon_livraison'))
		return HttpResponseRedirect(reverse('module_vente_detail_bon_livraison', args=(bon_livraison.id,)))
	except Exception as e:
		module='ModuleVente'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_bon_livraison'))

def get_details_bon_livraison(request,ref):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		bon_livraison=dao_bon_livraison.toGetBonLivraison(ref)
		template = loader.get_template('ErpProject/ModuleVente/bon_livraison/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_livraison)

		context ={'modules':modules,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'sous_modules':sous_modules,'title' : 'Details d une bon_livraison','bon_livraison' : bon_livraison,'utilisateur' : identite.utilisateur(request),'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_bon_livraison'))

#TRANSACTION CLIENT
def get_lister_transaction_client(request):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_transaction_client.toListTransactionClient()
	model = dao_model.toListModel(dao_transaction_client.toListTransactionClient(), permission_number, groupe_permissions, identite.utilisateur(request))
	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste de Transaction Client',
		'model' : model,
		'utilisateur' : identite.utilisateur(request),
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_VENTE,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleVente/transaction_client/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_transaction_client(request):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Nouvelle Transaction Client','utilisateur' : identite.utilisateur(request),'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleVente/transaction_client/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_transaction_client(request):

	try:
		status = request.POST['status']
		type_paiement = request.POST['type_paiement']
		est_validee = request.POST['est_validee']
		sequence = request.POST['sequence']
		facture_id = request.POST['facture_id']
		auteur = identite.utilisateur(request)



		transaction_client=dao_transaction_client.toCreateTransactionClient(status,type_paiement,est_validee,sequence,facture_id)
		transaction_client=dao_transaction_client.toSaveTransactionClient(auteur,transaction_client)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# return HttpResponseRedirect(reverse('module_vente_list_transaction_client'))
		return HttpResponseRedirect(reverse('module_vente_detail_transaction_client', args=(transaction_client.id,)))
	except Exception as e:
		module='ModuleVente'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_transaction_client'))


def get_details_transaction_client(request,ref):
	permission_number = -1
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		transaction_client=dao_transaction_client.toGetTransactionClient(ref)
		template = loader.get_template('ErpProject/ModuleVente/transaction_client/item.html')
		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details d une transaction_client','transaction_client' : transaction_client,'utilisateur' : identite.utilisateur(request),'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_transaction_client'))

#PAIEMENT CLIENT
def get_lister_paiement_client(request):
	permission_number = 301
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_paiement_client.toListPaiementClient()
	model = dao_model.toListModel(dao_paiement_client.toListPaiementClient(), permission_number, groupe_permissions, identite.utilisateur(request))
	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste de Paiement Client',
	    'model' : model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_VENTE,
		'menu' : 13
		}
	template = loader.get_template('ErpProject/ModuleVente/paiement/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_paiement_client(request):
	permission_number = 302
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Nouvelle Paiement Client',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'moyen_paiement': dao_moyen_paiement.toListMoyenPaiement(),
		'devises': dao_devise.toListDevises(),
		'module' : ErpModule.MODULE_VENTE,
		'menu' : 13
		}
	template = loader.get_template('ErpProject/ModuleVente/paiement/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_paiement_client(request):
	pass
	'''
	try:
		montant = request.POST['montant']
		date_paiement = request.POST['date_paiement']
		is_complete = request.POST['is_complete']

		facture_id = request.POST['facture_id']
		document_id =request.POST['document_id']
		devise_id = request.POST['devise_id']
		taux_id  = request.POST['taux_id']
		#transaction_client_id = request.POST['transaction_client_id']

		auteur = identite.utilisateur(request)


		paiement_client=dao_paiement_client.toCreatePaiementClient(montant,date_paiement,is_complete,facture_id,document_id,devise_id,taux_id,transaction_client_id)
		paiement_client=dao_paiement_client.toSavePaiementClient(auteur,paiement_client)
		return HttpResponseRedirect(reverse('module_vente_list_paiement_client'))
	except Exception as e:
		module='ModuleVente'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
		return HttpResponseRedirect(reverse('module_vente_add_paiement_client'))'''


def get_details_paiement_client(request,ref):
	permission_number = 301
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		paiement_client=dao_paiement_client.toGetPaiementClient(ref)
		template = loader.get_template('ErpProject/ModuleVente/paiement_client/item.html')
		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Details d une paiement_client',
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),

		'paiement_client' : paiement_client,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 4}


		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_paiement_client'))


# ARTICLES VENDABLES CONTROLLER
def get_lister_article(request):

	try:
		permission_number = 29
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_article.toListArticlesAchetables()
		model = dao_model.toListModel(dao_article.toListArticlesVendables(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : "Liste des articles vendables",
			'model' : model,
			'view' : view,
			'types_article' : dao_type_article.toListTypesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'modules':modules,'sous_modules':sous_modules,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleVente/articles/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur List Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_articles'))

def get_creer_article(request):

	try:
		permission_number = 30
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Nouvel article',
			'unites' : dao_unite.toListUnite(),
			'clients' : dao_client.toListClientsActifs(),
			'types_article' : dao_type_article.toGetTypeService(),
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'categories' : dao_categorie_article.toListCategoriesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleVente/articles/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Creer Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_articles'))



@transaction.atomic
def post_creer_article(request):
    sid = transaction.savepoint()
    try:
	    auteur = identite.utilisateur(request)
	    base_dir = settings.BASE_DIR
	    media_dir = settings.MEDIA_ROOT
	    media_url = settings.MEDIA_URL
	    designation = request.POST["designation"]
	    unite_id = request.POST["unite_id"]
	    if ((unite_id == "0") or (unite_id == "")):
		    unite_id = None

	    est_commercialisable = False
	    if "est_commercialisable" in request.POST : est_commercialisable = True

	    est_achetable = False
	    if "est_achetable" in  request.POST : est_achetable = True

	    est_manufacturable = False
	    if "est_manufacturable" in request.POST : est_manufacturable = True

	    est_fabriquable = False
	    if "est_fabriquable" in request.POST : est_fabriquable = True

	    est_amortissable = False
	    if "est_amortissable" in request.POST : est_amortissable = True

	    '''est_commercialisable = True
	    est_achetable = False
	    est_manufacturable = False
	    est_fabriquable = False
	    est_amortissable = False'''

	    designation_court = ""
	    code_article = request.POST["code_article"]
	    code_barre = ""
	    type_article = int(request.POST["type_article"])
	    categorie_id = int(request.POST["categorie_id"])
	    prix_unitaire = makeFloat(request.POST["prix_unitaire_article"])
	    image = ""

	    article = dao_article.toCreateArticle(image, designation, unite_id, est_commercialisable, est_achetable, est_manufacturable, est_fabriquable, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire, None, est_amortissable)
	    article = dao_article.toSaveArticle(auteur, article)


	    if article != None :

			# CREATION DE L'UNITE D'ACHAT
		    if unite_id:
			    unite_achat = dao_unite_achat_article.toCreateUniteAchat(article.id, article.unite_id)
			    unite_achat = dao_unite_achat_article.toSaveUniteAchat(auteur, unite_achat)

		    if 'image_upload' in request.FILES:
			    file = request.FILES["image_upload"]
			    article_img_dir = 'articles/'
			    media_dir = media_dir + '/' + article_img_dir
			    save_path = os.path.join(media_dir, str(article.id) + ".jpg")
			    path = default_storage.save(save_path, file)
				#On affecte le chemin de l'Image
			    article.image = media_url + article_img_dir + str(article.id) + ".jpg"
			    article.save()
		    messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		    transaction.savepoint_commit(sid)
		    return HttpResponseRedirect(reverse("module_vente_details_article", args=(article.id,)))
	    else:
		    messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de l'article")
		    transaction.savepoint_rollback(sid)
		    return HttpResponseRedirect(reverse('module_vente_add_article'))
    except Exception as e:
	    auteur = identite.utilisateur(request)
	    module='ModuleVente'
	    monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
	    monLog.debug("Info")
	    #print('Erreut Post Creer Article')
	    #print(e)
	    transaction.savepoint_rollback(sid)
	    messages.error(request,e)
	    return HttpResponseRedirect(reverse('module_vente_list_articles'))

def get_modifier_article(request, ref):

	try:
		permission_number = 31
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		article = dao_article.toGetArticle(id)
		fournisseur_article = dao_fournisseur_article.toListFournisseursOf(article.id)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % article.designation,
			'model' : article,
			'unites' : dao_unite.toListUnite(),
			'clients' : dao_client.toListClientsActifs(),
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'fournisseur_article': fournisseur_article,
			'types_article' : dao_type_article.toGetTypeService(),
			'categories' : dao_categorie_article.toListCategoriesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleVente/articles/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Modifier Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_articles'))

@transaction.atomic
def post_modifier_article(request):
	sid = transaction.savepoint()
	id = int(request.POST["ref"])
	try:

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		designation = request.POST["designation"]
		unite_id = request.POST["unite_id"]
		if ((unite_id == "0") or (unite_id == "")):
		    unite_id = None

		est_commercialisable = False
		if "est_commercialisable" in request.POST : est_commercialisable = True

		est_achetable = False
		if "est_achetable" in  request.POST : est_achetable = True

		est_manufacturable = False
		if "est_manufacturable" in request.POST : est_manufacturable = True

		est_fabriquable = False
		if "est_fabriquable" in request.POST : est_fabriquable = True
		#print(est_fabriquable)
		#print(est_manufacturable)
		#print(est_achetable)
		#print(est_commercialisable)

		designation_court = ""
		code_article = request.POST["code_article"]
		code_barre = ""
		type_article = int(request.POST["type_article"])
		categorie_id = int(request.POST["categorie_id"])
		prix_unitaire = makeFloat(request.POST["prix_unitaire_article"])

		if 'image_upload' in request.FILES:
			file = request.FILES["image_upload"]
			article_img_dir = 'articles/'
			media_dir = media_dir + '/' + article_img_dir
			save_path = os.path.join(media_dir, str(id) + ".jpg")
			if default_storage.exists(save_path):
				default_storage.delete(save_path)
			path = default_storage.save(save_path, file)
			#default_storage.delete(path)
			#On affecte le chemin de l'Image
			image = media_url + article_img_dir + str(id) + ".jpg"
		else : image = ""

		article = dao_article.toCreateArticle(image, designation, unite_id, est_commercialisable, est_achetable, est_manufacturable, est_fabriquable, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire,None)
		#article = dao_article.toCreateUpdateArticle(image, designation, unite_id, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire)
		compte = dao_compte.toGetCompteClient()
		if article.compte_id == None and compte != None:
			article.compte_id = compte.id

		is_done = dao_article.toUpdateArticle(id, article)

		if is_done == True :
			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse("module_vente_details_article", args=(id,)))
		else :
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse("module_vente_update_article", args=(article.id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFICATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier Article')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_update_article', args=(id,)))

def get_details_article(request, ref):

	try:
		permission_number = 29
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		#print(dao_type_article.toListTypesArticles())

		ref = int(ref)
		article = dao_article.toGetArticle(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,article)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : article.designation,
			'model' : article,
			'types_article' : dao_type_article.toListTypesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleVente/articles/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detail Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_update_article', args=(article.id,)))

def get_json_get_prix_article(request):
	try:
		article_id = int(request.GET["ref"])
		article = dao_article.toGetArticle(article_id)
		#print("Article %s" % article)

		data = {
			"id" : article.id,
			"prix_unitaire" : article.prix_unitaire,
			"symbole_unite" : article.unite.symbole_unite,
		}

		#print("fin %s " % data)
		return JsonResponse(data, safe=False)

	except Exception as e:
		#print('ERREUR')
		#print(e)
		return JsonResponse([], safe=False)

def get_details_article_fourni(request):
	data = {}
	try:
		article_id = int(request.GET["ref"])
		article = dao_article.toGetArticle(article_id)
		type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
		emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
		les_stocks = dao_stock_article.toListStocksOfArticleInEmplacement(article_id, emplacement.id)

		if les_stocks == None or les_stocks.count() == 0 : stock_id = 0
		else:
			stock = les_stocks.first()
			stock_id = stock.id

		unite = dao_unite.toGetUnite(article.unite_id)

		data = {
			"designation" : article.designation,
			"stock_article_id" : stock_id,
			"prix_unitaire" : article.prix_unitaire,
			"symbole_unite" : unite.symbole_unite
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print(e)
		return JsonResponse(data, safe=False)


# CATEGORIER ARTICLE
def get_lister_categorie_articles(request):
	permission_number = 29
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		# categories = dao_categorie_article.toListCategoriesArticle()
		model = dao_model.toListModel(dao_categorie_article.toListCategoriesArticle(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'sous_modules':sous_modules,
			'title' : 'Liste des catégorie d\'articles',
			'view':view,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'model' : model,
			'menu' : 4
			}
		template = loader.get_template('ErpProject/ModuleVente/categorie/article/list.html')

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_articles'))

def get_creer_categorie_articles(request):

	try:
		permission_number = 30
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Nouvelle catégorie d'article",
			"utilisateur" : utilisateur,
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/categorie/article/add.html")

		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_articles'))

def post_creer_categorie_articles(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		categorie = dao_categorie_article.toSaveCategorieArticle(auteur, categorie)

		if categorie != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_vente_details_categorie_articles", args=(categorie.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la categorie article")
			return HttpResponseRedirect(reverse('module_vente_add_categorie_articles'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_articles'))

def get_details_categorie_articles(request, ref):

	permission_number = 29
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	try:
		ref = int(ref)
		categorie = dao_categorie_article.toGetCagorieArticle(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categorie)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_CATEGORIE_ARTICLE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_CATEGORIE_ARTICLE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CATEGORIE_ARTICLE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/categorie/article/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL CREATION CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_articles'))

def get_modifier_catagorie_articles(request, ref):

	permission_number = 31
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		id = int(ref)
		categorie = dao_categorie_article.toGetCagorieArticle(id)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Modifier la catégorie %s" % categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/categorie/article/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MISE A JOUR CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_articles'))

def post_modifier_categorie_articles(request):

	try:
		id = int(request.POST["ref"])
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		is_done = dao_categorie_article.toUpdateCategorieArticle(id, categorie)

		if is_done == True : return HttpResponseRedirect(reverse("module_vente_details_categorie_articles", args=(id,)))
		else : return HttpResponseRedirect(reverse('module_vente_update_categorie_articles', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST DE LA MISE A JOUR CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_articles'))


#UNITE DE MESURE
def get_lister_unites(request):

	try:
		permission_number = 322
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_unite.toListUnite()
		model = dao_model.toListModel(dao_unite.toListUnite(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Liste des unités de mesure",
			'model' : model,
			'view':view,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_UNITE_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_UNITE_DE_MESURE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleVente/unite/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_unite'))

def get_creer_unite(request):
	try:
		permission_number = 321
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Nouvelle unité de mésure',
			'categories' : dao_categorie_unite.toListCategoriesUnite(),
			"utilisateur" : utilisateur,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleVente/unite/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CREER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_unite'))

def post_creer_unite(request) :
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		symbole_unite = request.POST["symbole_unite"]
		est_systeme = False

		categorie_unite_id = int(request.POST["categorie_unite_id"])

		unite = dao_unite.toCreateUnite(designation, symbole_unite, est_systeme, categorie_unite_id)
		unite = dao_unite.toSaveUnite(auteur, unite)
		if unite != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_vente_details_unite', args=(unite.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de l'unité de mésure")
			return HttpResponseRedirect(reverse('module_vente_add_unite'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_unite'))

def get_modifier_unite(request, ref):
	try:
		permission_number = 323
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		id = int(ref)
		unite = dao_unite.toGetUnite(id)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % unite.designation,
			'categories' : dao_categorie_unite.toListCategoriesUnite(),
			'model' : unite,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleVente/unite/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU MODIFIER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Modifier')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_unite'))

def post_modifier_unite(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		symbole_unite = request.POST["symbole_unite"]
		categorie_unite_id = int(request.POST["categorie_unite_id"])

		unite = dao_unite.toGetUnite(id)
		unite.designation = designation
		unite.symbole_unite = symbole_unite
		unite.categorie_unite_id = categorie_unite_id
		is_done = dao_unite.toUpdateUnite(id, unite)

		if is_done == True : return HttpResponseRedirect(reverse('module_vente_details_unite', args=(id,)))
		else : return HttpResponseRedirect(reverse('module_vente_update_unite', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFIER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_update_unite', args=(id,)))

def get_details_unite(request, ref):

	try:
		permission_number = 322
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		unite = dao_unite.toGetUnite(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,unite)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : unite.designation,
			'model' : unite,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			#"utilisateur" : utilisateur,
			#"can_create" : dao_droit.toGetDroitRole('CREER_UNITE_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_UNITE_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_UNITE_DE_MESURE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleVente/unite/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_unite'))


#CONDITION DE REGLEMENT
def get_lister_condition_reglement(request):
	try:
		permission_number = 24
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_condition_reglement.toListConditionsReglement()
		model = dao_model.toListModel(dao_condition_reglement.toListConditionsReglement(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Liste des conditions de réglement",
			'model' : model,
			'view':view,
			#"utilisateur" : utilisateur,
			#"can_create" : dao_droit.toGetDroitRole('CREER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleVente/reglement/list.html")
		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE REGELEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_reglement'))

def get_creer_condition_reglement(request):

	try:
		permission_number = 21
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Nouvelle condition de Reglement",
			"utilisateur" : utilisateur,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleVente/reglement/add.html")
		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_reglement'))

def post_creer_condition_reglement(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		nombre_jours = request.POST["nombre_jours"]

		reglement = dao_condition_reglement.toCreateConditionReglement(designation,nombre_jours)
		reglement = dao_condition_reglement.toSaveConditionReglement(auteur,reglement)

		if reglement != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_vente_details_reglement", args=(reglement.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de cpnfition de reglement")
			return HttpResponseRedirect(reverse('module_vente_add_reglement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Reglement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_reglement'))

def get_details_condition_reglement(request, ref):

	try:
		permission_number = 24
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		condition_reglement = dao_condition_reglement.toGetConditionReglement(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,condition_reglement)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : condition_reglement.designation,
			'model' : condition_reglement,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			#"can_create" : dao_droit.toGetDroitRole('CREER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleVente/reglement/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_reglement'))

def get_modifier_condition_reglement(request, ref):

	try:
		permission_number = 22
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		condition_reglement = dao_condition_reglement.toGetConditionReglement(ref)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier la condition de réglement %s' % condition_reglement.designation,
			'model' : condition_reglement,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleVente/reglement/update.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Modifier')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_reglement'))

def post_modifier_condition_reglement(request):
	id = int(request.POST["ref"])
	#print("id ",id)
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		nombre_jours = int(request.POST["nombre_jours"])
		#print(designation," post_modifier_condition_reglement ",nombre_jours)

		reglement = dao_condition_reglement.toCreateConditionReglement(designation,nombre_jours)
		#print("objet",reglement.designation)
		is_done = dao_condition_reglement.toUpdateConditionReglement(id, reglement)
		#print("boolean ",is_done)
		if is_done == True : return HttpResponseRedirect(reverse("module_vente_list_reglement"))
		else : return HttpResponseRedirect(reverse('module_vente_update_reglement', args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFIER REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Regelement ',e)
		#return HttpResponseRedirect(reverse('module_vente_list_reglement'))
		return HttpResponseRedirect(reverse('module_vente_update_reglement', args=(id,)))



#CATEGORIE UNITE DE MESURE
def get_lister_categorie_unites(request):
	permission_number = 326
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		# categories = dao_categorie_unite.toListCategoriesUnite()
		model = dao_model.toListModel(dao_categorie_unite.toListCategoriesUnite(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Catégorie Unites',
			'view':view,
			'utilisateur' : identite.utilisateur(request),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'model' : model,
			'menu' : 4
			}
		template = loader.get_template('ErpProject/ModuleVente/categorie/unite/list.html')

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_unite'))

def get_creer_categorie_unites(request):

	try:
		permission_number = 325
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Nouvelle catégorie d'unite",
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/categorie/unite/add.html")

		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_unite'))

def post_creer_categorie_unites(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		categorie = dao_categorie_unite.toSaveCategorieUnite(auteur, categorie)

		if categorie != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_vente_details_categorie_unites", args=(categorie.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la categorie d'unite")
			return HttpResponseRedirect(reverse('module_vente_add_categorie_unites'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_unite'))

def get_details_categorie_unites(request, ref):

	permission_number = 326
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	try:
		ref = int(ref)
		categorie = dao_categorie_unite.toGetCagorieUnite(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categorie)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			#"can_create" : dao_droit.toGetDroitRole('CREER_CATEGORIE_UNITE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_CATEGORIE_UNITE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CATEGORIE_UNITE',nom_role,utilisateur.nom_complet),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/categorie/unite/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL CREATION CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_unite'))

def get_modifier_catagorie_unites(request, ref):

	permission_number = 327
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	try:
		id = int(ref)
		categorie = dao_categorie_unite.toGetCagorieUnite(id)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Modifier la catégorie %s" % categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/categorie/unite/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MISE A JOUR CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_unite'))

def post_modifier_categorie_unites(request):

	try:
		id = int(request.POST["ref"])
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		is_done = dao_categorie_unite.toUpdateCategorieUnite(id, categorie)

		if is_done == True : return HttpResponseRedirect(reverse("module_vente_details_categorie_unites", args=(id,)))
		else : return HttpResponseRedirect(reverse('module_vente_update_categorie_unites', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleVente'
		monLog.error("{} :: {}::\nERREUR LORS DU POST DE LA MISE A JOUR CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_categorie_unite'))

# RECOUVREMENT CONTROLLERS
def get_lister_recouvrement(request):
	try:
		permission_number = 386
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_recouvrement.toList()
		model = dao_model.toListModel(dao_recouvrement.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)

		title = "Liste des recouvrements"
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'view':view,
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleVente/recouvrement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des recouvrements \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des recouvrements')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_recouvrement'))

def get_details_recouvrement(request, ref):
	try:
		permission_number = 386
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_recouvrement.toGet(ref)
		ligne_recouvrements = dao_recouvrement_ligne.toListLigneDuRecouvrement(model.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Recouvrement {}'.format(model.designation),
			'model' : model,
			'ligne_recouvrements': ligne_recouvrements,
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
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		#print(' module %s' % (ErpModule.MODULE_VENTE))
		template = loader.get_template('ErpProject/ModuleVente/recouvrement/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_recouvrement'))

def get_creer_recouvrement(request):
	try:
		permission_number = 385
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		statut_recouvrements = dao_recouvrement.toListStatutRecouvrements()
		clients = dao_client.toListClientsActifs()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Créer un recouvrement',
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'clients': clients,
			'statut_recouvrements': statut_recouvrements,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleVente/recouvrement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer Recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer Recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_recouvrement'))

def post_creer_recouvrement(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		client_id = int(request.POST["client_id"])
		statut_recouvrement = int(request.POST['statut_recouvrement'])

		recouvrement = dao_recouvrement.toCreate(auteur.id, designation, statut_recouvrement, client_id, description)
		recouvrement = dao_recouvrement.toSave(recouvrement)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_vente_detail_recouvrement', args=(recouvrement.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_recouvrement'))

def get_modifier_recouvrement(request, ref):
	try:
		permission_number = 387
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_recouvrement.toGet(ref)
		statut_recouvrements = dao_recouvrement.toListStatutRecouvrements()
		ligne_recouvrements = dao_recouvrement_ligne.toListLigneDuRecouvrement(model.id)
		clients = dao_client.toListClientsActifs()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'clients': clients,
			'statut_recouvrements': statut_recouvrements,
			'ligne_recouvrements' : ligne_recouvrements,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleVente/recouvrement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_recouvrement'))

def post_modifier_recouvrement(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		client_id = int(request.POST["client_id"])
		statut_recouvrement = int(request.POST['statut_recouvrement'])

		recouvrement = dao_recouvrement.toCreate(auteur.id, designation, statut_recouvrement, client_id, description)
		recouvrement = dao_recouvrement.toUpdate(ref, recouvrement)

		if recouvrement == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_vente_detail_recouvrement', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_recouvrement'))


# RELANCE RECOUVREMENT CONTROLLERS
def get_lister_relance_recouvrement(request):
	try:
		permission_number = 382
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_relance_recouvrement.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_relance_recouvrement.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		title = "Liste des relances"
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'model' : model,
			'view':view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleVente/relance_recouvrement/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des relances \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des relances')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_relance_recouvrement'))

def get_creer_relance_recouvrement(request):
	try:
		permission_number = 381
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_relances = dao_relance_recouvrement.toListTypeRelance()
		clients = dao_client.toListClientsActifs()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Créer un recouvrement',
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'clients': clients,
			'type_relances': type_relances,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleVente/relance_recouvrement/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer relance Recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer relance Recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_relance_recouvrement'))


def get_details_relance_recouvrement(request, ref):
	try:
		permission_number = 382
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_relance_recouvrement.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Relance {}'.format(model.designation),
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
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		#print(' module %s' % (ErpModule.MODULE_VENTE))
		template = loader.get_template('ErpProject/ModuleVente/relance_recouvrement/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details relance recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail relance recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_relance_recouvrement'))


def post_creer_relance_recouvrement(request):
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_relance"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		client_id = int(request.POST["client_id"])
		type_relance = int(request.POST['type_relance'])
		date_relance = request.POST["date_relance"]
		date_relance = date_relance[6:10] + '-' + date_relance[3:5] + '-' + date_relance[0:2]
		date_relance = datetime.strptime(date_relance, "%Y-%m-%d").date()

		relance_recouvrement = dao_relance_recouvrement.toCreate(auteur.id, designation, date_relance, type_relance, client_id, description)
		relance_recouvrement = dao_relance_recouvrement.toSave(relance_recouvrement)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_vente_detail_relance__recouvrement', args=(relance_recouvrement.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer relance recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer relance recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_add_relance_recouvrement'))

def get_modifier_relance_recouvrement(request, ref):
	try:
		permission_number = 383
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		ref = int(ref)
		model = dao_relance_recouvrement.toGet(ref)
		type_relances = dao_relance_recouvrement.toListTypeRelance()
		clients = dao_client.toListClientsActifs()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'clients': clients,
			'type_relances': type_relances,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_VENTE,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleVente/relance_recouvrement/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier relance recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier relance recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_relance_recouvrement'))

def post_modifier_relance_recouvrement(request):
	ref = int(request.POST["ref"])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_relance"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		client_id = int(request.POST["client_id"])
		type_relance = int(request.POST['type_relance'])

		date_relance = request.POST["date_relance"]
		date_relance = date_relance[6:10] + '-' + date_relance[3:5] + '-' + date_relance[0:2]
		date_relance = datetime.strptime(date_relance, "%Y-%m-%d").date()

		relance_recouvrement = dao_relance_recouvrement.toCreate(auteur.id, designation, date_relance, type_relance, client_id, description)
		relance_recouvrement = dao_relance_recouvrement.toUpdate(ref, relance_recouvrement)

		if relance_recouvrement == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_vente_detail_relance_recouvrement', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier relance recouvrement\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier relance recouvrement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_vente_list_relance_recouvrement'))

# BALANCE CLIENTS
def get_generer_balance_client(request):

	permission_number = 375
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Générer la balance clients',
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"module" : ErpModule.MODULE_VENTE,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModuleVente/balance_client/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_balance_client(request):
	try:
		permission_number = 375
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

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
		equilibre_credit_mouvement = 0
		equilibre_debit_mouvement = 0
		equilibre_credit_solde = 0
		equilibre_debit_solde = 0

		#On récupère tous les comptes clients
		comptes = dao_compte.toListComptesClient()

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
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Balance clients",
			"model" : donnees_balance,
			'equilibre_credit_mouvement' : "%.2f" % equilibre_credit_mouvement,
			'equilibre_debit_mouvement' : "%.2f" % equilibre_debit_mouvement,
			'equilibre_credit_solde' : "%.2f" % equilibre_credit_solde,
			'equilibre_debit_solde' : "%.2f" % equilibre_debit_solde,
			"date_debut" : request.POST["date_debut"],
			"date_fin" : request.POST["date_fin"],
			"devise" : devise,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
			"modules" : dao_module.toListModulesInstalles() ,
			"module" : ErpModule.MODULE_VENTE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/balance_client/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_generer_balance_client"))

# EXTRAIT DES COMPTES CLEINTS
def get_generer_extrait_compte(request):

	permission_number = 389
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	clients = dao_client.toListClientsActifs()

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : "Générer l'extrait de compte client",
		"devises" : dao_devise.toListDevisesActives(),
		"utilisateur" : utilisateur,
		'clients' : clients,
		'actions': auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		"module" : ErpModule.MODULE_VENTE,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModuleVente/extrait_compte/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_extrait_compte(request):
	try:
		permission_number = 389
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)
		devise = dao_devise.toGetDeviseReference()
		client_id = int(request.POST["client_id"])

		#On declare les tableaux et variable qui seront renvoyés en output
		factures = []
		paiements = []

		client = dao_client.toGetClient(client_id)
		factures = Model_Facture.objects.filter(type = "CLIENT", client_id = client.id, date_facturation__lte = date_fin).order_by("-date_facturation")
		nbr_fac = factures.count()
		#print("nbr_fac: {}".format(nbr_fac))
		#Pour chaque facture, on récupère les paiements
		for facture in factures:
			#Pour les paiements
			list_paiements = Model_Paiement.objects.filter(facture_id = facture.id, est_valide = True)
			for paiement in list_paiements:
				payment = {}
				payment['date'] = paiement.date_paiement
				payment['libelle'] = paiement.designation
				payment['id'] = paiement.id
				payment['facture_id'] = facture.id
				payment['url'] = "module_comptabilite_details_paiement_client"
				#payment['url'] = "/comptabilite/paiements/client/item/{}/".format(paiement.id)
				if int(paiement.transaction.moyen_paiement) == 1:
					payment['montant'] = paiement.montant
					payment['type'] = "Espèce"
				elif int(paiement.transaction.moyen_paiement) == 2 :
					transaction = Model_Transaction.objects.get(paiement_id = paiement.id)
					payloads = json.loads(transaction.payloads.replace("'",'"'))
					pay_currency = int(payloads["devise"])

					payment['montant'] = float(payloads["montant"])
					payment['type'] = "Virement"

				paiements.append(payment)
		#On trie les paiments
		paiements = sorted(paiements, key=lambda paiement: paiement['date'], reverse=True)

		#On initialise les totaux de la balance agée
		total_montant = 0.0
		total_montant_paye = 0.0
		total_montant_solde = 0.0
		total_solde = 0.0

		# On récupere les soldes initiaux à partir des écritures d'avant période
		for facture in factures:
			total_montant = total_montant + float(facture.montant)
			total_montant_paye = total_montant_paye + float(facture.montant_paye)
			total_montant_solde = total_montant_solde + float(facture.montant_restant)

		total_solde = total_montant - total_montant_paye

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Extrait de compte {}".format(client.nom_complet),
			"factures" : factures,
			"paiements" : paiements,
			"client" : client,
			'total_montant' : "%.2f" % total_montant,
			'total_montant_paye' : "%.2f" % total_montant_paye,
			'total_montant_solde' : "%.2f" % total_montant_solde,
			'total_solde' : "%.2f" % total_solde,
			"date_fin" : request.POST["date_fin"],
			"devise" : devise,
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : dao_module.toListModulesInstalles() ,
			"module" : ErpModule.MODULE_VENTE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/extrait_compte/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_generer_extrait_compte"))

def post_imprimer_extrait_compte(request):
	try:
		permission_number = 389
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)
		devise = dao_devise.toGetDeviseReference()
		client_id = int(request.POST["client_id"])

		#On declare les tableaux et variable qui seront renvoyés en output
		factures = []
		paiements = []

		client = dao_client.toGetClient(client_id)
		factures = Model_Facture.objects.filter(type = "CLIENT", client_id = client.id, date_facturation__lte = date_fin).order_by("-date_facturation")
		nbr_fac = factures.count()
		#print("nbr_fac: {}".format(nbr_fac))
		#Pour chaque facture, on récupère les paiements
		for facture in factures:
			#Pour les paiements
			list_paiements = Model_Paiement.objects.filter(facture_id = facture.id, est_valide = True)
			for paiement in list_paiements:
				payment = {}
				payment['date'] = paiement.date_paiement
				payment['libelle'] = paiement.designation
				payment['id'] = paiement.id
				payment['facture_id'] = facture.id
				payment['url'] = "module_comptabilite_details_paiement_client"
				#payment['url'] = "/comptabilite/paiements/client/item/{}/".format(paiement.id)
				if int(paiement.transaction.moyen_paiement) == 1:
					payment['montant'] = paiement.montant
					payment['type'] = "Espèce"
				elif int(paiement.transaction.moyen_paiement) == 2 :
					transaction = Model_Transaction.objects.get(paiement_id = paiement.id)
					payloads = json.loads(transaction.payloads.replace("'",'"'))
					pay_currency = int(payloads["devise"])

					payment['montant'] = float(payloads["montant"])
					payment['type'] = "Virement"

				paiements.append(payment)
		#On trie les paiments
		paiements = sorted(paiements, key=lambda paiement: paiement['date'], reverse=True)

		#On initialise les totaux de la balance agée
		total_montant = 0.0
		total_montant_paye = 0.0
		total_montant_solde = 0.0
		total_solde = 0.0

		# On récupere les soldes initiaux à partir des écritures d'avant période
		for facture in factures:
			total_montant = total_montant + float(facture.montant)
			total_montant_paye = total_montant_paye + float(facture.montant_paye)
			total_montant_solde = total_montant_solde + float(facture.montant_restant)

		total_solde = total_montant - total_montant_paye

		context = {
			'title' : "Extrait de compte {}".format(client.nom_complet),
			"factures" : factures,
			"paiements" : paiements,
			"client" : client,
			'total_montant' : "%.2f" % total_montant,
			'total_montant_paye' : "%.2f" % total_montant_paye,
			'total_montant_solde' : "%.2f" % total_montant_solde,
			'total_solde' : "%.2f" % total_solde,
			"date_fin" : request.POST["date_fin"],
			"devise" : devise,
   			'organisation': dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			"utilisateur" : identite.utilisateur(request)
		}
		html_string = render_to_string('ErpProject/ModuleVente/reporting/extrait_compte.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'extrait_compte.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('extrait_compte.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="Extrait compte client.pdf"'
			return response

		return response
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_generer_extrait_compte"))

# BALANCE AGEE CLIENT
def get_generer_balance_agee_client(request):
	try:
		permission_number = 376
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
			'modules':modules,'sous_modules':sous_modules,
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
			"utilisateur" : identite.utilisateur(request),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : dao_module.toListModulesInstalles() ,
			"module" : ErpModule.MODULE_VENTE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/balance_agee/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GENERATE BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_tableau_de_bord"))

def post_generer_balance_agee_client(request):
	try:
		permission_number = 376
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

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
			'modules':modules,'sous_modules':sous_modules,
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
			"utilisateur" : identite.utilisateur(request),
   			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : dao_module.toListModulesInstalles() ,
			"module" : ErpModule.MODULE_VENTE,
			'format' : 'landscape',
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleVente/balance_agee/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR POST GENERATE BALANCE AGEE")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_generer_balance_agee_client"))


def get_upload_client(request):
	try:
		permission_number = 25
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des clients",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_VENTE,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleVente/client/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD PIECE COMPTABLE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_list_clients"))


@transaction.atomic
def post_upload_client(request):
	sid = transaction.savepoint()
	try:
		#print("upload_piece_comptable")
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
			nom_complet = str(df['Nom'][i])
			phone = str(df['Telephone'][i])
			type = str(df['Type'][i])
			adresse = str(df['Adresse'][i])
			email = str(df['Email'][i])
			est_particulier = False
			if "particul" in type.lower():
				est_particulier = True

			client = dao_client.toCreateClient(nom_complet,None,None, nom_complet ,None,email,phone,adresse,None, None, True,None,None,None, None,est_particulier, None)
			client = dao_client.toSaveClient(auteur,client)

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_vente_list_clients"))

	except Exception as e:
		#print("ERREUR POST UPLOAD CLIENT")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_vente_add_client"))
		pass


def get_lister_typefactureclient(request):
	permission_number = 524
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response

	model = dao_type_facture.toListTypefactureClient()
	context ={'title' : 'Liste des types factures clients','model' : model,'utilisateur' : utilisateur,'modules' : modules,
	 'sous_modules':sous_modules, 'organisation': dao_organisation.toGetMainOrganisation(), 'module' : ErpModule.MODULE_VENTE,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleVente/typefactureclient/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_typefactureclient(request):
	permission_number = 523
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response

	context ={'title' : 'Ajouter un type de facture client','utilisateur' : utilisateur,  'sous_modules':sous_modules, 'organisation': dao_organisation.toGetMainOrganisation(),  'modules' : modules,'module' : ErpModule.MODULE_VENTE, 'menu' : 2}
	template = loader.get_template('ErpProject/ModuleVente/typefactureclient/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_typefactureclient(request):

	try:
		designation = request.POST['designation']
		observation = request.POST['observation']
		type_facture = 2
		auteur = identite.utilisateur(request)

		typefactureclient=dao_type_facture.toCreateTypefacture(designation,observation, type_facture)
		typefactureclient=dao_type_facture.toSaveTypefacture(auteur, typefactureclient)
		return HttpResponseRedirect(reverse('module_vente_list_typefactureclient'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER TYPEFACTURECLIENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_vente_add_typefactureclient'))


def get_details_typefactureclient(request,ref):
	permission_number = 524
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response
	try:
		ref=int(ref)
		typefactureclient=dao_type_facture.toGetTypefacture(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,typefactureclient)

		template = loader.get_template('ErpProject/ModuleVente/typefactureclient/item.html')
		context ={'title' : 'Details sur un type de facture client',
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'typefactureclient' : typefactureclient, 'sous_modules':sous_modules, 'organisation': dao_organisation.toGetMainOrganisation(),  'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_VENTE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS TYPEFACTURECLIENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_vente_list_typefactureclient'))
def get_modifier_typefactureclient(request,ref):
	permission_number = 525
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		 return response

	ref = int(ref)
	model = dao_type_facture.toGetTypefacture(ref)
	context ={'title' : 'Modifier un type de facture client','model':model, 'utilisateur': utilisateur,'modules' : modules, 'sous_modules':sous_modules, 'organisation': dao_organisation.toGetMainOrganisation(), 'module' : ErpModule.MODULE_VENTE,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleVente/typefactureclient/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_typefactureclient(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		observation = request.POST['observation']
		type_facture = 2
		auteur = identite.utilisateur(request)

		typefactureclient=dao_type_facture.toCreateTypefacture(designation,observation, type_facture)
		typefactureclient=dao_type_facture.toUpdateTypefacture(id, typefactureclient)
		return HttpResponseRedirect(reverse('module_vente_list_typefactureclient'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER TYPEFACTURECLIENT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_vente_add_typefactureclient'))