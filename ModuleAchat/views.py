from __future__ import unicode_literals

import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect , JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy, reverse
from django.contrib import messages
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
from datetime import datetime, timedelta
import json
import array
import base64
from django.db import transaction
from django.utils import timezone
from ModuleBudget.dao.dao_transactionbudgetaire import dao_transactionbudgetaire
from datetime import date, timedelta
from ErpBackOffice.dao.dao_document import dao_document
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ModuleContrat.dao.dao_contrat import dao_contrat

from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.print import weasy_print
from ErpBackOffice.models import Model_Image, Model_Categorie, Model_Unite, Model_Bon_reception, Model_Fournisseur, Model_Demande_achat
from ErpBackOffice import models
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_historique import dao_wkf_historique
from ErpBackOffice.dao.dao_wkf_historique_demande import dao_wkf_historique_demande
from ErpBackOffice.dao.dao_wkf_historique_expression import dao_wkf_historique_expression
from ErpBackOffice.dao.dao_wkf_historique_reception import dao_wkf_historique_reception
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation
from ErpBackOffice.dao.dao_regle import dao_regle
from ErpBackOffice.dao.dao_civilite import dao_civilite
from ModuleBudget.dao.dao_dashbord import dao_dashbord


from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ErpBackOffice.dao.dao_facture_fournisseur import dao_facture_fournisseur
from ModuleAchat.dao.dao_categorie import dao_categorie
from ModuleAchat.dao.dao_expression_besoin import dao_expression_besoin
from ModuleAchat.dao.dao_ligne_expression import dao_ligne_expression
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ModuleAchat.dao.dao_categorie_unite import dao_categorie_unite
from ModuleAchat.dao.dao_unite import dao_unite
from ModuleAchat.dao.dao_condition_reglement import dao_condition_reglement
from ModuleAchat.dao.dao_article import dao_article
from ModuleAchat.dao.dao_stock_article import dao_stock_article
from ModuleAchat.dao.dao_type_article import dao_type_article
from ModuleAchat.dao.dao_fournisseur_article import dao_fournisseur_article
from ModuleAchat.dao.dao_unite_achat_article import dao_unite_achat_article
from ModuleAchat.dao.dao_emplacement import dao_emplacement
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ModuleAchat.dao.dao_type_emplacement import dao_type_emplacement
from ModuleAchat.dao.dao_taux_change import dao_taux_change
from ModuleAchat.dao.dao_demande_achat import dao_demande_achat
from ModuleAchat.dao.dao_ligne_demande_achat import dao_ligne_demande_achat
from ModuleBudget.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleAchat.dao.dao_civilite import dao_civilite

from ModuleAchat.dao.dao_document_bon_reception import dao_document_bon_reception
from ModuleAchat.dao.dao_document_demande import dao_document_demande
from ModuleConversation.dao.dao_notification import dao_notification
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification

from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleConversation.dao.dao_notification import dao_notification


from ErpBackOffice.utils.endpoint import endpoint

from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task

from ModuleAchat.dao.dao_avis_appel_offre import dao_avis_appel_offre
from ModuleBudget.dao.dao_centre_cout import dao_centre_cout
from ErpBackOffice.views import get_wizard_report, post_wizard_report

#For Data Table server side

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializer import CategorieArticleSerializer, UniteSerializer, BonReceptionSerializer, FournisseurSerializer
from ModuleAchat import serializer

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile
from dateutil.relativedelta import relativedelta
from ModuleBudget.dao.dao_dashbord import dao_dashbord
from ModuleBudget.dao.dao_localite import dao_localite
from ErpBackOffice.dao.dao_groupe_permission import dao_groupe_permission
#POUR LOGGING
import logging, inspect
from ModuleInventaire.dao.dao_asset import dao_asset
monLog = logging.getLogger('logger')
module= "ModuleAchat"
var_module_id = 1

def error_500(request):
		data = {}
		return render(request,'Page_500.html', data)

def error_404_view(request, exception):
	data = {"name": "ThePythonDjango.com"}
	return render(request,'ErpProject/error_404.html', data)

def get_json_article(request):
	try:
		#print("ima")
		data = []
		ident = int(request.GET["ref"])
		#print(ident)
		if 'bool' in request.GET:
			print("inside")
			articles = dao_article.toListArticlesOfEmplacementService(ident)
			#print(articles)
		else:
			print("dazom")
			articles = dao_article.toListArticlesOfServiceReferent(ident)
		print(articles)
		for article in articles:
				item = {"id": article.id,"code_article" : article.code_article,'designation' : article.designation}
				data.append(item)
		#print(data)

		return JsonResponse(data, safe=False)

	except Exception as e:
		return JsonResponse([], safe=False)

def get_json_articles_stock_emplacement(request):
	try:
		data = []
		ident = int(request.GET["ref"])
		if 'bool' in request.GET:
			# print('Inside')
			model = dao_stock_article.toListStocksInEmplacement(ident)
			# print(model)
		# else:
		# 	articles = dao_article.toListArticlesOfServiceReferent(ident)
		for x in model:
			item = {"id": x.article.id,"code_article" : x.article.code_article,'designation' : x.article.designation}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)

def get_json_ligne_expression(request):
	try:
		#print("ligne expression ajax")
		data = []
		ident = int(request.GET["ref"])
		#print(ident)

		#print("dazom")
		lignes_expression = dao_ligne_expression.toListLigneOfExpressions(ident)
		#print(lignes_expression)
		#print("before the bb")

		expression = dao_expression_besoin.toGetExpression(ident)

		for ligne in lignes_expression:
			article = dao_article.toGetArticle(ligne.article_id)
			item = {"id": ligne.id,"article_id" : article.id,'designation_article' : article.designation, 'quantite_demandee':ligne.quantite_demande, 'quantite_restante':ligne.quantite_restante, 'prix_unitaire':ligne.prix_unitaire, 'description':ligne.description, 'emplacement_id':expression.services_ref.emplacement.id, 'service_referent_libelle':expression.services_ref.libelle, 'demandeur_id': expression.demandeur_id, 'demandeur_nom':expression.demandeur.nom_complet, "service_ref_id":expression.services_ref.id}
			#print(item)
			data.append(item)
		#print("masolo",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("erreur",e)
		return JsonResponse([], safe=False)


def get_json_ligne_demande(request):
	try:
		#print("ligne demande ajax")
		data = []
		ident = int(request.GET["ref"])
		#print(ident)

		#print("dazom")
		lignes_demande = dao_ligne_demande_achat.toListLigneOfDemandes(ident)
		demande = dao_demande_achat.toGetDemande(ident)
		#print(lignes_demande)
		#print("before the bb")

		for ligne in lignes_demande:
			article = dao_article.toGetArticle(ligne.article_id)
			item = {"id": ligne.id,"article_id" : article.id,'designation_article' : article.designation, 'quantite_demandee':ligne.quantite_demande, 'prix_unitaire':ligne.prix_unitaire, 'description':ligne.description, 'emplacement_id':demande.services_ref.emplacement.id, 'service_referent_libelle':demande.services_ref.libelle}
			#print(item)
			data.append(item)
		#print("masolo",data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print("erreur",e)
		return JsonResponse([], safe=False)


def get_json_lignes_bon_commande_non_facture(request):
	try:
		data = []
		bons =  dao_bon_reception.toListFournituresFacturablesByWorkflow()
		devise = dao_devise.toGetDeviseReference()

		for bon in bons:
			lignes  = dao_ligne_reception.toListLigneOfReceptions(bon.id)
			for ligne in lignes:
				montant_total = ligne.prix_unitaire * ligne.quantite_demande
				item = {"id": ligne.id, "numero_bon" : ligne.bon_reception.numero_reception, 'article':ligne.article.designation, 'ligne_budgetaire' : ligne.ligne_budgetaire.code, 'montant_total':montant_total, 'devise': devise.symbole_devise, 'date':str(ligne.bon_reception.date_reception)}
				data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)



# Tableau de board
def get_dashboard(request):

	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(1, request)
	if response != None:
		return response

	#expressions = dao_expression_besoin.toListExpressions() if auth.toCheckAdmin(modules, utilisateur) else dao_expression_besoin.toListExpressionsByAuteur(utilisateur.id)

	demandes_recentes = None
	bon_reception_recentes = None
	total_frs = 0
	total_dem = 0
	total_art = 0
	total_cmd = 0
	lesExpressiondebesion = None
	Lesarticleslivre = None
	LesArticleApproue = None
	NombreExpressionArticleLivre = 0
	NombreExpressionDemandeAchatGenere = 0
	NombreExpressionLivrePartiellement = 0
	NombreExpressionEnvoyeDFC = 0
	NombreExpressnionApprouve = 0
	ExpressionByMonth = None
	model = None
	NombreExpressionCreeUser = None
	NombreExpressionAdmin = None

	if auth.toCheckAdmin("Achat", utilisateur):
		demandes_recentes = dao_demande_achat.toListDemandesRecentes()
		bon_reception_recentes = dao_bon_reception.toListBonReceptionRecentes()
		total_frs = dao_fournisseur.toListFournisseursActifs().count()
		total_dem = dao_demande_achat.toListDemandes().count()
		total_art = dao_article.toListArticles().count()
		total_cmd = dao_bon_reception.toListBonReception().count()
		lesExpressiondebesion,Lesarticleslivre,LesArticleApproue,NombreExpressionArticleLivre, NombreExpressionDemandeAchatGenere, NombreExpressionLivrePartiellement, NombreExpressionEnvoyeDFC, NombreExpressnionApprouve, NombreExpressionCreeUser = dao_expression_besoin.toCountExpression_SpecByAuteur(utilisateur.id)
		countExpressionB = dao_expression_besoin.toListExpressions().count()
		Listeencours = None

		#END WAY

		model = dao_bon_reception.toListBonReception()
	else:
		demandes_recentes = dao_demande_achat.toListDemandesRecentesByAuteur(utilisateur.id)
		bon_reception_recentes = dao_bon_reception.toListBonReceptionRecentesByAuteur(utilisateur.id)
		total_frs = dao_fournisseur.toListFournisseursActifs().count()
		total_dem = dao_demande_achat.toListDemandesByAuteur(utilisateur.id).count()
		total_art = dao_article.toListArticles().count()
		total_cmd = dao_bon_reception.toListBonReceptionByAuteur(utilisateur.id).count()
		lesExpressiondebesion,Lesarticleslivre,LesArticleApproue,NombreExpressionArticleLivre, NombreExpressionDemandeAchatGenere, NombreExpressionLivrePartiellement, NombreExpressionEnvoyeDFC, NombreExpressnionApprouve, NombreExpressionCreeUser = dao_expression_besoin.toCountExpression_SpecByAuteur(utilisateur.id)

		#END WAY
		countExpressionB = dao_expression_besoin.toListExpressionsByAuteur(utilisateur.id).count()
		Listeencours = NombreExpressionCreeUser[:4]
		#print('##LES EXPRESSION DE BESOIN#',countExpressionB)
		model = dao_bon_reception.toListBonReceptionByAuteur(utilisateur.id)

	lesExpressiondebesion,Lesarticleslivre,LesArticleApproue,NombreExpressionArticleLivre, NombreExpressionDemandeAchatGenere, NombreExpressionLivrePartiellement, NombreExpressionEnvoyeDFC, NombreExpressnionApprouve, NombreExpressionAdmin = dao_expression_besoin.toCountExpression_Spec()
	#WAY OF NOTIFCATION
	module_name = "MODULE_ACHAT"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()
	#print("way")
	#print(temp_notif_count)
	all_doc_year = dao_expression_besoin.toListExpressions()
	year=[]
	for item in all_doc_year:
		year.append(item.creation_date.year)

	year=set(year)

	ExpressionByMonths = dao_expression_besoin.toListNumberExpressionbyMonth()
	ExpressionAuteurByM = dao_expression_besoin.toListNumberExpressionbyMonthByAuteur(utilisateur.id)
	bccommende = dao_bon_reception.toListBonReception()

	bcvalide,lesjours,lesvaleurs = dao_dashbord.toGetCBValide()
	bcall= dao_dashbord.CountBC()
	bcwork = int(bcall) - int(bcvalide)
	mois,values, nbrebc = dao_dashbord.toGetLastBCMonth()
	periode, bcvalidecount, bnv= dao_dashbord.toGetLastpassebyMonth()
	groupe_permission = dao_groupe_permission.toGetGroupePermissionDeLaPersonne(utilisateur.id)
	if groupe_permission != None:
		if groupe_permission.designation == 'Chef de service SBA' or groupe_permission.designation == 'Chef de bureau Achat':
			template = loader.get_template('ErpProject/ModuleAchat/dashboardAss.html')
		else:
			template = loader.get_template('ErpProject/ModuleAchat/index.html')
	else:
		template = loader.get_template('ErpProject/ModuleAchat/dashboardAss.html')

	context = {
		'title' : 'Tableau de Bord',
		'model' : model,
		'sous_modules':sous_modules,
		'temp_notif_count':temp_notif_count,
		'temp_notif_list':temp_notif_list,
		'demandes' : demandes_recentes[:4],
		'bons' : bon_reception_recentes[:4],
		'tot_frs' : total_frs,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'total_dem' : total_dem,
		'total_art' : total_art,
		'total_cmd' : total_cmd,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'deggrade': 'module_achat',
		'NombreExpressionArticleLivre' : NombreExpressionArticleLivre,
  		'NombreExpressionDemandeAchatGenere' : NombreExpressionDemandeAchatGenere,
		'serviceRef' : lesExpressiondebesion.count(),
    	'NombreExpressionLivrePartiellement' : NombreExpressionLivrePartiellement,
       	'NombreExpressionEnvoyeDFC' : NombreExpressionEnvoyeDFC,
        'NombreExpressnionApprouve' : dao_expression_besoin.toListExpBesoinApprouve(utilisateur.id).count(),
		'ListExpBenCours': dao_expression_besoin.toListExpBesoinEnCours(utilisateur.id),
		'TotalExpression': countExpressionB,
		'Listeencours':Listeencours,
        'Lesarticleslivre': Lesarticleslivre[:4],
		'CountArticleLivre': Lesarticleslivre.count(),
        'LesArticleApproue': LesArticleApproue[:4],
		'lesExpressiondebesionAdmin': NombreExpressionAdmin[:4],
        'ExpressionByMonth' : ExpressionByMonths,
		'ExpressionAuteurByM': ExpressionAuteurByM,
		"year": year,'bccommandes':bccommende[:10],
		'CountBC':dao_dashbord.CountBC(),'bcwork': bcwork,'nbrebc':nbrebc,'bcvalide':bcvalide,
		'bcR':dao_dashbord.totalBCRapproche(), 'ListBCencours':dao_bon_reception.toListBCencours()[:5],
		'periode':periode,'bcvalidecount':bcvalidecount,'bnv':bnv,
	}

	# template = loader.get_template('ErpProject/ModuleAchat/index.html')
	# template = loader.get_template('ErpProject/ModuleAchat/dashboardAss.html')
	return HttpResponse(template.render(context, request))

# Ajax envois des expression des besois
def get_expression_de_besoin_to_dashbord(request):
    #print('Touched ajax Quantite')
    modules, utilisateur,response = auth.toGetAuth(request)

    try:
        mYear = request.GET['year']
        data=[]
        ExpressionByMonth = dao_expression_besoin.toListNumberExpressionbyMonth(mYear)
        data = [ExpressionByMonth]

        #print('les doc et dos %s' % (data))

        return JsonResponse(data, safe=False)
    except Exception as e:
        #print("probleme get_inventer_to_dashbord %s"%(e))
        return JsonResponse([], safe=False)
# Tableau de board
def get_update_notification(request,ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	return get_dashboard(request)



# Bon de reception
def get_lister_bon_reception(request):

	# droit = "LISTER_BON_COMMANDE_ACHAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 125
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_bon_reception.toListBonReception(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#


	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	context = {
		'title' : 'Liste de Bon de commande',
		'model' : model,'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'view' : view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	template = loader.get_template('ErpProject/ModuleAchat/bon_reception/list.html')
	return HttpResponse(template.render(context, request))

def get_lister_bon_reception_month(request, ref):
	permission_number = 125
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	model = dao_model.toListModel(dao_dashbord.toGetBCbynumber(ref), permission_number, groupe_permissions, identite.utilisateur(request))
	mois = ''
	for item in model:
		mois = item.date_prevue

	mois = mois.strftime("%B")
	# print('Le mois BC',mois)

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context = {
		'title' : 'Liste de Bon de Commande du Mois de'+ ' '+ mois,
		'model' : model,'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules': sous_modules,
		'view' : view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	template = loader.get_template('ErpProject/ModuleAchat/bon_reception/list_mont.html')
	return HttpResponse(template.render(context, request))

def get_creer_bon_reception(request):

	# droit = "CREER_BON_COMMANDE_ACHAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 125
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response



	etat_actuel_id = 0
	etat = ""
	lignes = []
	etape_id = 0
	demande_wkf_id = 0
	etape_wkf_id = 0

	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		lignes = dao_ligne_demande_achat.toListLigneOfDemandes(etat.id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		#print("Aucun etat de besoin trouvé")
		pass

	#print("ETAAAAAAAAATTTTTTTTTTTTT %s" % etat_actuel_id)

	devises = dao_devise.toListDevisesActives()
	reglement = dao_condition_reglement.toListConditionsReglement()
	articles = dao_article.toListArticlesAchetables()
	categories = dao_categorie_article.toListCategoriesArticle()
	ligne_budgetaires = dao_ligne_budgetaire.toListLigneBudgetaires()
	contrats = dao_contrat.toListContrats()

	fournisseur = dao_fournisseur.toListFournisseursActifs()

	demandes = dao_demande_achat.toListDemandesPourBonCommande()


	auteur = identite.utilisateur(request)

	#print("AUTEURRRRRRR")
	#print(auteur)
	#print("ETATTTTTT %s" % etat_actuel_id)

	context =	{
		'title' : 'Nouveau Bon de commande',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'fournisseurs' : fournisseur,
		'demandes' : demandes,
		'etat' : etat,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'demande_wkf' : demande_wkf_id,
		'lignes_etat'  : lignes,
		'devises' : devises,
		'articles' : articles,
		'categories' : categories,
		'conditions_reglement' : reglement,
		'ligne_budgetaires' : ligne_budgetaires,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'localites': dao_localite.toListLocalites(),
		'contrats':contrats
		}

	template = loader.get_template('ErpProject/ModuleAchat/bon_reception/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_bon_reception(request):
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_prevue"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		date_prevue = request.POST["date_prevue"]

		# date_prevue = date_prevue[6:10] + '-' + date_prevue[3:5] + '-' + date_prevue[0:2]
		# date_prevue = datetime.datetime.strptime(date_prevue, "%Y-%m-%d").date()
		date_prevue = timezone.datetime(int(date_prevue[6:10]), int(date_prevue[3:5]), int(date_prevue[0:2]))

		#demande_id = request.POST["demande_id"]
		fournisseur_id = request.POST["fournisseur_id"]
		devise_id = request.POST["devise_id"]
		condition_reglement_id = request.POST["condition_reglement_id"]
		codes_budgetaires = ''
		ligne_budgetaire = request.POST["ligne_budgetaire"]
		etat_actuel_id = int(request.POST["etat_actuel_id"])
		description_commande = request.POST["description_commande"]
		duree_vie =int(request.POST["duree_vie"])

		contrat_id = None
		if 'contrat' in request.POST:
			contrat = int(request.POST["contrat"])
			contrat = dao_contrat.toGetContrat(contrat)
			if contrat:
				contrat_id = contrat.id




		ligne_budgetaire_id = 0
		ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaireByCombinaison(ligne_budgetaire)
		#print(ligne_budgetaire)


		if ligne_budgetaire.is_bloqued:
			messages.error(request,'La ligne budgétaire saisie est bloquante')
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse("module_achat_add_bon_reception"))

		if ligne_budgetaire == None:
			messages.error(request,'La ligne budgétaire saisie est incorrecte')
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse("module_achat_add_bon_reception"))
		else:
			ligne_budgetaire_id = ligne_budgetaire.id


		est_groupe = False

		numero = dao_bon_reception.toGenerateNumeroReception()
		demande_id = request.POST['demande_id']

		if 'est_groupe' in request.POST:
			est_groupe = True
			#print(request.POST.getlist("demande_list_id",None))
			list_demande_id = request.POST.getlist("demande_list_id",None)
			#Enlève les dupliqués
			tableSet = set(list_demande_id)
			list_demande_id = list(tableSet)
			bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,"Créé",fournisseur_id,None,condition_reglement_id,None,ligne_budgetaire_id,False,description_commande,devise_id)
			bon_reception = dao_bon_reception.toSaveBonReception(auteur, bon_reception)
			for i in range(0, len(list_demande_id)) :
				demande_pk = list_demande_id[i]
				bon_reception.demandes_achat.add(demande_pk)

			bon_reception.est_groupe = True
			bon_reception.duree = duree_vie
			bon_reception.contrat_id = contrat_id
			bon_reception.save()
		else:
			demande_id = None
			if 'demande_id' in request.POST:
				demande_id = request.POST['demande_id']
				bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,"Créé",fournisseur_id,None,condition_reglement_id,demande_id,ligne_budgetaire_id,False,description_commande,devise_id)
				bon_reception = dao_bon_reception.toSaveBonReception(auteur, bon_reception)
				bon_reception.duree = duree_vie
				bon_reception.contrat_id = contrat_id
				bon_reception.save()


		#url = '<a class="lien chargement-au-click" href="/achat/bon_reception/item/'+ str(bon_reception.id) +'/">'+ bon_reception.numero + '</a>'
		#bon_reception.url = url

		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, bon_reception)
		### Fin traitement document

		#print("bon saved")

		if bon_reception != None :
			docs = Model_Image.objects.all()
			#print("bon 1")
			if docs != None:
				#print("bon 2")
				for doc in docs:
					#print ("DOCCCCCCCCC %s" % doc.doc)
					bon_reception.document = doc.doc
					bon_reception.save()
				Model_Image.objects.all().delete()

			#Affectation des codes budgetaires
			if codes_budgetaires != '':
				#print("bon 3")
				codes = codes_budgetaires.split("|")
				#print("CODES   %s" % codes)
				for code in codes:
					ligne_budgetaire = dao_ligne_budgetaire.toGetLigneOfCode(code)
					#print("LIGNEEEEE BUDGET %s" % ligne_budgetaire)
					bon_reception.codes_budgetaires.add(ligne_budgetaire)

			list_article_id = request.POST.getlist('article_id', None)
			#print("bon 4")
			list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
			list_ligne_budgetaire = request.POST.getlist("ligne_of_ligne_budgetaire", None)
			print(len(list_article_id))
			print(len(list_quantite_demandee))
			print(len(list_prix_unitaire))
			for i in range(0, len(list_article_id)) :
				#print("bon 5")
				article_id = int(list_article_id[i])
				quantite_demandee = makeFloat(list_quantite_demandee[i])
				prix_unitaire = makeFloat(list_prix_unitaire[i])
				ligne_of_ligne_budgetaire = list_ligne_budgetaire[i]

				article = dao_article.toGetArticle(article_id)
				#On stock l'article à l'emplacement d'entrée
				#1. On recupere le type d'emplacement d'entree
				type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
				#2. On recupere l'emplacement d'entree proprement dite à partir de son type
				emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
				#print("article id", article_id)
				#on recupere le stock de cet article présent dans cet emplacement
				les_stocks = dao_stock_article.toListStocksArticleInEmplacement(article_id,emplacement.id)

				#Traitement ligne budgetaire
				ligne_budget_id = 0
				if ligne_of_ligne_budgetaire == "":
					ligne_of_ligne_budgetaire = ligne_budgetaire #Ligne budgetaire par defaut du bon receptionù
				else:
					ligne_of_ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaireByCombinaison(ligne_of_ligne_budgetaire)
					if ligne_of_ligne_budgetaire == None:
						messages.error(request,'La ligne budgétaire saisie à la ligne '+ str(i+1) +' est incorrecte')
						transaction.savepoint_rollback(sid)
						return HttpResponseRedirect(reverse("module_achat_add_bon_reception"))
				ligne_budget_id = ligne_of_ligne_budgetaire.id
				###Fin traitement ligne budgetaire par ligne

				if not les_stocks:
					les_stocks = dao_stock_article.toCreateStockArticle(article_id,0,emplacement.id)
					les_stocks = dao_stock_article.toSaveStockArticle(les_stocks)
					stock = les_stocks
				else:
					stock = les_stocks[0]
				#print("le stock", stock)

				article = dao_article.toGetArticle(article_id)
				print("BC ID %s" % bon_reception.id)
				unite_article = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_article_id = unite_article.id if unite_article else None
				ligne = dao_ligne_reception.toCreateLigneReception(bon_reception.id, article.id, quantite_demandee, prix_unitaire, unite_article_id, ligne_budget_id)
				ligne = dao_ligne_reception.toSaveLigneReception(ligne)

				print('**LA LIGNE', ligne)

				#On rajoute le stock_article
				ligne.stock_article_id = stock.id
				ligne.save()

			#print('lignes fini')
			# WORKFLOWS INITIALS
			#type_document = "Bon de commande"
			wkf_task.initializeWorkflow(auteur,bon_reception)

			if demande_id != "" or est_groupe == True:
				if etat_actuel_id != 0:
					#print("Kkk")
					etape_id = request.POST["etape_wkf"]
					demande_id = request.POST["demande_wkf"]
					utilisateur_id = request.user.id

					employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
					demande_achat = dao_demande_achat.toGetDemande(demande_id)

					wkf_task.passingStepWorkflow(employe,demande_achat,etape_id)
				else:
					#print('ffff')
					employe = dao_employe.toGetEmployeFromUser(request.user.id)
					if not est_groupe:
						demande_achat = dao_demande_achat.toGetDemande(demande_id)
						wkf_task.passingStepWorkflow(auteur,demande_achat)
					else:
						#print('we are the zhest')
						for i in range(0, len(list_demande_id)) :
							demande_id = list_demande_id[i]
							demande_achat = dao_demande_achat.toGetDemande(demande_id)
							wkf_task.passingStepWorkflow(auteur,demande_achat)


			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			print("OKAY %s" % bon_reception.id)
			print("OKAY %s" % bon_reception.id)
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(bon_reception.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du bon de recception")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_add_bon_reception'))

	except Exception as e:
		print("ERREUR")
		print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_add_bon_reception'))

def get_print_reception(request):
	try:
		permission_number = 121
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		id = request.POST["id"]
		#print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK " + str(id))

		end = endpoint.reportingEndPoint()

		context = {
			'title' : 'Impression',
			'id' : id,
			'endpoint' : end,
			'utilisateur' : utilisateur,
			'roles':groupe_permissions,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleAchat/bon_reception/print.html')
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

def get_update_bon_reception(request, ref):

	# droit = "CREER_BON_COMMANDE_ACHAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 125
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	ref=int(ref)
	bon_reception = dao_bon_reception.toGetBonReception(ref)
	ligne_commande = dao_ligne_reception.toListLigneOfReceptions(ref)

	etat_actuel_id = 0
	etat = ""
	lignes = []
	etape_id = 0
	demande_wkf_id = 0
	etape_wkf_id = 0

	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		lignes = dao_ligne_demande_achat.toListLigneOfDemandes(etat.id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		#print("Aucun etat de besoin trouvé")
		pass

	#print("ETAAAAAAAAATTTTTTTTTTTTT %s" % etat_actuel_id)

	devises = dao_devise.toListDevisesActives()
	reglement = dao_condition_reglement.toListConditionsReglement()
	articles = dao_article.toListArticlesAchetables()
	categories = dao_categorie_article.toListCategoriesArticle()
	ligne_budgetaires = dao_ligne_budgetaire.toListLigneBudgetaires()

	fournisseur = dao_fournisseur.toListFournisseursActifs()

	demandes = dao_demande_achat.toListDemandesPourBonCommande()


	auteur = identite.utilisateur(request)

	#print("AUTEURRRRRRR")
	#print(auteur)
	#print("ETATTTTTT %s" % etat_actuel_id)

	context =	{
		'title' : 'Modification Bon de commande',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'fournisseurs' : fournisseur,
		'demandes' : demandes,
		'etat' : etat,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'demande_wkf' : demande_wkf_id,
		'lignes_etat'  : lignes,
		'devises' : devises,
		'articles' : articles,
		'categories' : categories,
		'conditions_reglement' : reglement,
		'ligne_budgetaires' : ligne_budgetaires,
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'localites': dao_localite.toListLocalites(),
		'model': bon_reception,
		'lignes':ligne_commande
		}

	template = loader.get_template('ErpProject/ModuleAchat/bon_reception/update.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_update_bon_reception(request):
	sid = transaction.savepoint()
	identifiant = int(request.POST["ref"])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_prevue"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)

		date_prevue = request.POST["date_prevue"]

		date_prevue = date_prevue[6:10] + '-' + date_prevue[3:5] + '-' + date_prevue[0:2]
		# date_prevue = datetime.datetime.strptime(date_prevue, "%Y-%m-%d").date()
		# print('Date Prevue', date_prevue)

		#demande_id = request.POST["demande_id"]
		fournisseur_id = request.POST["fournisseur_id"]
		devise_id = request.POST["devise_id"]
		condition_reglement_id = request.POST["condition_reglement_id"]
		codes_budgetaires = ''
		ligne_budgetaire = request.POST["ligne_budgetaire"]
		etat_actuel_id = int(request.POST["etat_actuel_id"])
		description_commande = request.POST["description_commande"]
		duree_vie =int(request.POST["duree_vie"])


		ligne_budgetaire_id = 0
		ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaireByCombinaison(ligne_budgetaire)
		# print(ligne_budgetaire)


		if ligne_budgetaire.is_bloqued:
			messages.error(request,'La ligne budgétaire saisie est bloquante')
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse("module_achat_add_bon_reception"))

		if ligne_budgetaire == None:
			messages.error(request,'La ligne budgétaire saisie est incorrecte')
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse("module_achat_add_bon_reception"))
		else:
			ligne_budgetaire_id = ligne_budgetaire.id


		est_groupe = False

		# numero = dao_bon_reception.toGenerateNumeroReception()
		bon_reception_last = dao_bon_reception.toGetBonReception(identifiant)
		numero = bon_reception_last.numero_reception
		# demande_id = request.POST['demande_id']
		statut_id = bon_reception_last.etat

		if 'est_groupe' in request.POST:
			est_groupe = True
			# print(request.POST.getlist("demande_list_id",None))
			list_demande_id = request.POST.getlist("demande_list_id",None)
			#Enlève les dupliqués
			tableSet = set(list_demande_id)
			list_demande_id = list(tableSet)
			bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,statut_id,fournisseur_id,None,condition_reglement_id,None,ligne_budgetaire_id,False,description_commande,devise_id)
			bon_reception = dao_bon_reception.toUpdateBonReception(bon_reception_last.id, bon_reception)
			for i in range(0, len(list_demande_id)) :
				demande_pk = list_demande_id[i]
				bon_reception.demandes_achat.add(demande_pk)

			bon_reception.est_groupe = True
			bon_reception.duree = duree_vie
			bon_reception.save()
		else:
			demande_id = None
			if 'demande_id' in request.POST:
				demande_id = request.POST['demande_id']
				if demande_id != None:
					bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,statut_id,fournisseur_id,None,condition_reglement_id,demande_id,ligne_budgetaire_id,False,description_commande,devise_id)
					bon_reception = dao_bon_reception.toUpdateBonReception(bon_reception_last.id, bon_reception)
					bon_reception.duree = duree_vie
					bon_reception.save()
				else:
					demande_id==None
					bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,statut_id,fournisseur_id,None,condition_reglement_id,demande_id,ligne_budgetaire_id,False,description_commande,devise_id)
					bon_reception = dao_bon_reception.toUpdateBonReception(bon_reception_last.id, bon_reception)
					bon_reception.duree = duree_vie
					bon_reception.save()
			else:
				bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,statut_id,fournisseur_id,None,condition_reglement_id,demande_id,ligne_budgetaire_id,False,description_commande,devise_id)
				bon_reception = dao_bon_reception.toUpdateBonReception(bon_reception_last.id, bon_reception)
				bon_reception.duree = duree_vie
				bon_reception.save()
			# else:
			# demande_id==None
			# bon_reception = dao_bon_reception.toCreateBonReception(numero,date_prevue,None,statut_id,fournisseur_id,None,condition_reglement_id,demande_id,ligne_budgetaire_id,False,description_commande,devise_id)
			# bon_reception = dao_bon_reception.toUpdateBonReception(bon_reception_last.id, bon_reception)
			# bon_reception.duree = duree_vie
			# bon_reception.save()

		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, bon_reception)
		### Fin traitement document

		# print("bon saved")

		if bon_reception != None :

			list_article_id = request.POST.getlist('article_id', None)
			# print("bon 4")
			list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
			list_ligne_budgetaire = request.POST.getlist("ligne_of_ligne_budgetaire", None)
			list_ligne_id = request.POST.getlist('ligne_id',None)
			list_all_ligne_id = request.POST.getlist('all_ligne_id', None)
			# print('Taille', len(list_ligne_id))
			# print(len(list_quantite_demandee))
			# print(len(list_prix_unitaire))
			i=0
			for i in range(0, len(list_all_ligne_id)):
				is_find = False
				the_item = list_all_ligne_id[i]
				for j in range(0, len(list_ligne_id)):
					if the_item == list_ligne_id[j]:
						is_find = True
				if is_find == False:
					dao_ligne_reception.toDeleteLigneReception(the_item)



			for i in range(0, len(list_ligne_id)) :
				# print("***Occurence", i)
				article_id = int(list_article_id[i])
				quantite_demandee = makeFloat(list_quantite_demandee[i])
				prix_unitaire = makeFloat(list_prix_unitaire[i])
				ligne_of_ligne_budgetaire = list_ligne_budgetaire[i]

				article = dao_article.toGetArticle(article_id)
				# print('L\'Article', article)
				#On stock l'article à l'emplacement d'entrée
				#1. On recupere le type d'emplacement d'entree
				# type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
				#2. On recupere l'emplacement d'entree proprement dite à partir de son type
				# emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
				#print("article id", article_id)
				#on recupere le stock de cet article présent dans cet emplacement
				# les_stocks = dao_stock_article.toListStocksArticleInEmplacement(article_id,emplacement.id)

				#Traitement ligne budgetaire
				ligne_budget_id = 0
				if ligne_of_ligne_budgetaire == "":
					ligne_of_ligne_budgetaire = ligne_budgetaire #Ligne budgetaire par defaut du bon receptionù
				else:
					ligne_of_ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaireByCombinaison(ligne_of_ligne_budgetaire)
					if ligne_of_ligne_budgetaire == None:
						messages.error(request,'La ligne budgétaire saisie à la ligne '+ str(i+1) +' est incorrecte')
						transaction.savepoint_rollback(sid)
						return HttpResponseRedirect(reverse("module_achat_add_bon_reception"))
				ligne_budget_id = ligne_of_ligne_budgetaire.id
				###Fin traitement ligne budgetaire par ligne

				# if not les_stocks:
					# les_stocks = dao_stock_article.toCreateStockArticle(article_id,0,emplacement.id)
				# 	les_stocks = dao_stock_article.toSaveStockArticle(les_stocks)
				# 	stock = les_stocks
				# else:
				# 	stock = les_stocks[0]
				# print("le stock", stock)
				# print('Check Article')

				article = dao_article.toGetArticle(article_id)
				# print("BC ID %s" % bon_reception.id)
				unite_article = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_article_id = unite_article.id if unite_article else None
				ligne_id = int(list_ligne_id[i])

				if ligne_id != 0:
					ligne = dao_ligne_reception.toCreateLigneReception(bon_reception.id, article.id, quantite_demandee, prix_unitaire, unite_article_id, ligne_budget_id)
					ligne = dao_ligne_reception.toUpdateLigneReception(ligne_id, ligne)
				else:
					ligne = dao_ligne_reception.toCreateLigneReception(bon_reception.id, article.id, quantite_demandee, prix_unitaire, unite_article_id, ligne_budget_id)
					ligne = dao_ligne_reception.toSaveLigneReception(ligne)

				#On rajoute le stock_article
				# ligne.stock_article_id = stock.id
				# ligne.save()

			# print('lignes fini' ligne)
			# WORKFLOWS INITIALS
			#type_document = "Bon de commande"
			# wkf_task.initializeWorkflow(auteur,bon_reception)

			# if demande_id != "" or est_groupe == True:
			# 	if etat_actuel_id != 0:
			# 		#print("Kkk")
			# 		etape_id = request.POST["etape_wkf"]
			# 		demande_id = request.POST["demande_wkf"]
			# 		utilisateur_id = request.user.id

			# 		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
			# 		demande_achat = dao_demande_achat.toGetDemande(demande_id)

			# 		wkf_task.passingStepWorkflow(employe,demande_achat,etape_id)
			# 	else:
			# 		#print('ffff')
			# 		employe = dao_employe.toGetEmployeFromUser(request.user.id)
			# 		if not est_groupe:
			# 			demande_achat = dao_demande_achat.toGetDemande(demande_id)
			# 			wkf_task.passingStepWorkflow(auteur,demande_achat)
			# 		else:
			# 			#print('we are the zhest')
			# 			for i in range(0, len(list_demande_id)) :
			# 				demande_id = list_demande_id[i]
			# 				demande_achat = dao_demande_achat.toGetDemande(demande_id)
			# 				wkf_task.passingStepWorkflow(auteur,demande_achat)


			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY %s" % bon_reception.id)
			#print("OKAY %s" % bon_reception.id)
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(bon_reception.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du bon de recception")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(identifiant,)))

	except Exception as e:
		# print("ERREUR")
		# print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(identifiant,)))


def get_details_bon_reception(request,ref):
	try:
		# droit = "LISTER_BON_COMMANDE_ACHAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 125
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref=int(ref)
		bon_reception = dao_bon_reception.toGetBonReception(ref)
		ligne_commande = dao_ligne_reception.toListLigneOfReceptions(ref)



		total = 0
		for ligne in ligne_commande:
			t = ligne.prix_unitaire * ligne.quantite_demande
			total = total + t

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_reception)


		# print("transition_etape_suivant %s" % transition_etape_suivant)
		#print("LIGNEEEE %s" % ligne_commande)
		#TRAITEMENT DUREE DE VIE
		showbutton = False
		time_add = 0
		formatcurrencedate = datetime.now()
		currentdate = formatcurrencedate.strftime('%Y-%m-%d')
		duree = bon_reception.duree
		if duree == 1:
			time_add = 6
		else: time_add = 12
		datecreation = bon_reception.creation_date
		dateAdds = datecreation + relativedelta(months=time_add)
		dateAdds = dateAdds.strftime('%Y-%m-%d')

		# print('**la date durée', dateAdds)
		# print('**La date en cours', currentdate)

		if dateAdds <= currentdate:
			showbutton = True

		# print('**Condition showbutton', showbutton)

		template = loader.get_template('ErpProject/ModuleAchat/bon_reception/item.html')
		context ={
			'title' : "Details d'un bon de commande",
			'model' : bon_reception,
			'lignes' : ligne_commande,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'total' : total,
			'roles':groupe_permissions,
			'documents' : documents,
			'utilisateur' : utilisateur,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4,
			'showbutton':showbutton,
			}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_bon_reception'))

def get_printing_bon_commande(request):
	try:
		permission_number = 125
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
		bon_reception = dao_bon_reception.toGetBonReception(ref)
		ligne_commande = dao_ligne_reception.toListLigneOfReceptions(ref)
		total = 0
		for ligne in ligne_commande:
			t = ligne.prix_unitaire * ligne.quantite_demande
			total = total + t
		context ={
			'title' : "Bon de Commande",
			'model' : bon_reception,
			'lignes' : ligne_commande,
			'total' : total,
			'roles':groupe_permissions,
			'utilisateur' : utilisateur,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			# 'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4
			}
		return weasy_print("ErpProject/ModuleAchat/rapport/bon_reception.html", "bon_reception.pdf", context)
	except Exception as e:
		# print('***ERREUR*****')
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_bon_reception'))

#SET LIVE CYCLE BC
def get_detail_traitement(request):
	try:
		# droit = "LISTER_BON_COMMANDE_ACHAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 125
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'ref' in request.GET:
			ref =int(request.GET['ref'])

		bon_reception = dao_bon_reception.toGetBonReception(ref)
		ligne_commande = dao_ligne_reception.toListLigneOfReceptions(ref)



		total = 0
		for ligne in ligne_commande:
			t = ligne.prix_unitaire * ligne.quantite_demande
			total = total + t

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bon_reception)


		# print("transition_etape_suivant %s" % transition_etape_suivant)
		#print("LIGNEEEE %s" % ligne_commande)

		template = loader.get_template('ErpProject/ModuleAchat/bon_reception/life_cycle.html')
		context ={
			'title' : "Traitement d'un bon de commande",
			'model' : bon_reception,
			'lignes' : ligne_commande,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'content_type_id':content_type_id,
			'total' : total,
			'roles':groupe_permissions,
			'documents' : documents,
			'utilisateur' : utilisateur,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4
			}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(ref,)))


@transaction.atomic
def get_traitement_duree_bc(request):
	sid = transaction.savepoint()
	identifiant = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		duree_vie =int(request.POST["duree_vie"])

		est_prolonger = False
		not_prolonger = False

		#On recupere le bon à traiter
		bon_reception = dao_bon_reception.toGetBonReception(identifiant)
		today = date.today()

		if 'est_prolonger' in request.POST:
			bon_reception.duree  = duree_vie
			bon_reception.creation_date = today
			bon_reception.is_actif = True
			bon_reception.save()
		else:
			bon_reception.is_actif = False
			bon_reception.save()

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(bon_reception.id,)))
	except Exception as e:
		# print("ERREUR")
		# print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(identifiant,)))


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
			compte_id = None
			compte_name = None
			try:
				#print("Inside")
				compte_id = item.article.compte_id
				compte_name = item.article.compte.numero + ' ' + item.article.compte.designation
			except Exception as e:
				pass

			#unite
			if item.unite_achat:
				symbole_unite = item.unite_achat.unite.symbole_unite
			elif item.article.unite:
				symbole_unite = item.article.unite.symbole_unite
			else:
				symbole_unite = ""
			#end unite
			ligne = {
				"ligne_id" : item.id,
				"nom_article" : item.article.designation,
				"article_id":item.article.id,
				"compte_id":compte_id,
				"compte_designation": compte_name,
				"quantite_fournie" : item.quantite_fournie,
				"prix_unitaire" : item.prix_unitaire,
				"prix_lot" : item.prix_lot,
				"symbole_unite" : symbole_unite
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

def get_details_ligne_reception(request,ref):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))
	try:
		ref=int(ref)
		ligne_reception=dao_ligne_reception.toGetLigneReception(ref)
		template = loader.get_template('ErpProject/ModuleAchat/ligne_reception/item.html')
		context ={'title' : 'Details d une ligne_reception','ligne_reception' : ligne_reception,'utilisateur' : identite.utilisateur(request),'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_ACHAT,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_ligne_reception'))

@transaction.atomic
def post_workflow_reception(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		reception_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, reception_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		bon_reception = dao_bon_reception.toGetBonReception(reception_id)

		#print("print 2 %s %s %s " % (employe, etape, bon_reception))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bon_reception.statut_id)
		for item in transitions_etapes_suivantes:


			if item.condition.designation == "CodeBudget":

				#print("Budget")
				nombre_a_signer = bon_reception.codes_budgetaires.all().count()
				nombre_deja_signer = dao_wkf_historique_demande.getCountSignatures( etape.id, bon_reception.id)
				#print("nombre_a_signer %i " % nombre_a_signer)
				#print("nombre_deja_signer %i " % nombre_deja_signer)
				#On verifie si tous les utilisateurs hormis la personne, ont signé, si oui
				if int(nombre_a_signer) - int(nombre_deja_signer) == 1:
					# Gestion des transitions dans le document
					bon_reception.statut_id = etape.id
					bon_reception.etat = etape.designation
					bon_reception.save()

			elif item.condition.designation == "Upload":

				#print("Upload")
				if 'file_upload' in request.FILES:
					nom_fichier = request.FILES['file_upload']

					#print(nom_fichier)
					#print("Debut file ")
					file = request.FILES["file_upload"]
					docs_dir = 'documents/'
					media_dir = media_dir + '/' + docs_dir
					save_path = os.path.join(media_dir, str(nom_fichier))
					path = default_storage.save(save_path, file)
					url = media_url + docs_dir + str(nom_fichier)

					#print("Saved url %s" % url)

					#On affecte le chemin de l'Image

					bon_reception.statut_id = etape.id
					bon_reception.etat = etape.designation
					bon_reception.save()

					document = dao_document_bon_reception.toCreateDocument("Bon de reception",url, bon_reception.etat,reception_id)
					document = dao_document_bon_reception.toSaveDocument(auteur, document)

					#print("docu saved")

			else:

				#print("Autres")
				# Gestion des transitions dans le document
				bon_reception.statut_id = etape.id
				bon_reception.etat = etape.designation
				bon_reception.save()

			#lotus
			if bon_reception.etat=="Accusé de reception téléchargé":
				montant_total = dao_ligne_reception.toGetMontantTotalOfBon(bon_reception.id)
				devise = dao_devise.toGetDeviseReference()
				compte = dao_compte.toGetCompte(bon_reception.ligne_budgetaire.compte_id)
				transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire("Paiement bon de commande "+bon_reception.numero_reception,montant_total,"",devise.id,compte.id, None,auteur.id,bon_reception.ligne_budgetaire_id,1)
				transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionBudgetaire)


		historique = dao_wkf_historique_reception.toCreateHistoriqueWorkflow(employe.id, etape.id, bon_reception.id)
		historique = dao_wkf_historique_reception.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(reception_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_detail_bon_reception', args=(reception_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_add_bon_reception'))


#Demande d'achat
def get_lister_demande(request):
	try:
		# droit = "LISTER_DEMANDE_ACHAT"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 121
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_demande_achat.toListDemandes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#


		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		#demandes = dao_demande_achat.toListDemandes()
		#print(demandes)
		context = {
			'title' : 'Liste des demandes d\'achat',
			'model' : model,
			'view' : view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleAchat/demande_achat/list.html')
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

#Zico
def get_creer_demande(request):
	# droit = "CREER_DEMANDE_ACHAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 120
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	centre_cout = dao_centre_cout.toListCentre_cout()

	#expressions = dao_expression_besoin.toListExpressionsNeedDemandeAchat()

	etat_actuel_id = 0
	etat = ""
	lignes = []
	etape_id = 0
	expression_wkf_id = 0
	etape_wkf_id = 0
	#print("amande")
	try:
		etat_actuel_id = request.POST["doc_id"]
		#print("etat_actuel", etat_actuel_id)
		etat = dao_expression_besoin.toGetExpression(etat_actuel_id)
		lignes = dao_ligne_expression.toListLigneOfExpressions(etat.id)
		etape_wkf_id = request.POST["etape_id"]
		expression_wkf_id = request.POST["doc_id"]
		#etat_besoins = dao_expression_besoin.toListExpressionsServiceReferent()
	except Exception as e:
		pass
		#print("Aucun etat de besoin trouvé")

	#print("ETAAAAAAAAATTTTTTTTTTTTT %s" % etat_actuel_id)

	auteur = identite.utilisateur(request)
	#print("amande 2")



	demandeurs = dao_employe.toListEmployesActifs()
	#print("Demand %s" % demandeurs)
	fournisseurs = dao_fournisseur.toListFournisseursActifs()
	articles = dao_article.toListArticlesAchetables()
	categories = dao_categorie_article.toListCategoriesArticle()
	dep_entrepots = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()

	if utilisateur.unite_fonctionnelle != None:
		#print("amande 3")
		expressions = dao_expression_besoin.toListExpressionsNeedDemandeAchat(utilisateur.unite_fonctionnelle.id)
		dep_entrepots = dao_unite_fonctionnelle.toListOfOneUniteFonctionnelle(utilisateur.unite_fonctionnelle.id)
	else:
		expressions = dao_expression_besoin.toListExpressions()

	#print("OKKKKKKKKKKKKKKKKKKKKKKKKK")


	context = {
		'title' : 'Créer une demande d\'achat',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 4,
		'etat' : etat,
		'centre_cout':centre_cout,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'expression_wkf' : expression_wkf_id,
		'expressions':expressions,
		'lignes_etat'  : lignes,
		'demandeurs' : demandeurs,
		'fournisseurs' : fournisseurs,
		'articles' : articles,
		'warehouses' : dep_entrepots,
		'categories' : categories,
			}

	template = loader.get_template('ErpProject/ModuleAchat/demande_achat/add.html')
	return HttpResponse(template.render(context, request))


@transaction.atomic
def post_creer_demande(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		date_prevue = request.POST["date"]
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		est_groupe = False
		date_prevue = timezone.datetime(int(date_prevue[6:10]), int(date_prevue[3:5]), int(date_prevue[0:2]))
		# date_prevue = date_prevue[6:10] + '-' + date_prevue[3:5] + '-' + date_prevue[0:2]
		# date_prevue = datetime.datetime.strptime(date_prevue, "%Y-%m-%d").date()

		demandeur_id = request.POST["demandeur_id"]
		description_demande = request.POST["description_demande"]
		service_ref_id = request.POST["service_ref_id"]
		centre_cout_id = None

		if centre_cout_id == 0:
			centre_cout_id = None
		numero = dao_demande_achat.toGenerateNumeroDemande()
		demande = dao_demande_achat.toIntializeDemandeAchat()
		expression_id = request.POST["expression_id"]
		#print("start2")
		if 'est_groupe' in request.POST:
			est_groupe = True
			#print(request.POST.getlist("expression_list_id",None))
			list_expression_id = request.POST.getlist("expression_list_id",None)
			#Enlève les dupliqués
			tableSet = set(list_expression_id)
			list_expression_id = list(tableSet)
			demande = dao_demande_achat.toCreateDemande(numero, date_prevue, description_demande, None , demandeur_id, "", "",True, None,"",service_ref_id,centre_cout_id)
			demande = dao_demande_achat.toSaveDemande(auteur, demande)
			for i in range(0, len(list_expression_id)) :
				expression_pk = list_expression_id[i]
				demande.expressions.add(expression_pk)

			demande.save()
		else:
			expression_id = None
			#print("moma")
			if 'expression_id' in request.POST:
				expression_id = request.POST['expression_id']
				if expression_id == "":
					expression_id = None
			demande = dao_demande_achat.toCreateDemande(numero, date_prevue, description_demande, None , demandeur_id, "", "", False,expression_id,"",service_ref_id)
			demande = dao_demande_achat.toSaveDemande(auteur, demande)
			if expression_id != None:
				demande.expressions.add(expression_id)
				demande.save()
			#print("hola")
			#print(expression_id)




		#print("start3")
		#print(est_groupe)
		#print(demande)

		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, demande)
		### Fin traitement document




		if demande != None :
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					demande.document = doc.doc
					demande.save()
				Model_Image.objects.all().delete()


			list_article_id = request.POST.getlist('article_id', None)
			list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
			list_description = request.POST.getlist("description", None)
			#print(len(list_article_id))
			#print(list_article_id)
			#print(len(list_quantite_demandee))
			#print(list_quantite_demandee)
			#print(len(list_prix_unitaire))
			#print(len(list_description))

			for i in range(0, len(list_article_id)) :
				article_id = int(list_article_id[i])
				quantite_demandee = makeFloat(list_quantite_demandee[i])
				#prix_unitaire = makeFloat(list_prix_unitaire[i])
				description = list_description[i]
				#print(demande)



				article = dao_article.toGetArticle(article_id)
				#print(article)

				unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_achat_id = unite_achat.id if unite_achat else None
				#print(unite_achat)

				ligne = dao_ligne_demande_achat.toCreateLigneDemande(demande.id, article.id, quantite_demandee, 0, unite_achat_id, description)
				ligne = dao_ligne_demande_achat.toSaveLigneDemande(ligne)

			# WORKFLOWS INITIALS
			#print("pass here")

			wkf_task.initializeWorkflow(auteur,demande)

			if est_groupe:
				for i in range(0, len(list_expression_id)) :
					expression_id = list_expression_id[i]
					expression = dao_expression_besoin.toGetExpression(expression_id)
					wkf_task.passingStepWorkflow(auteur,expression)

			'''if (expression_id != "" and expression_id != None) or (est_groupe == True):
				if not est_groupe :
					#print("inside the box")
					expression = dao_expression_besoin.toGetExpression(expression_id)
					wkf_task.passingStepWorkflow(auteur,expression)

				else:

					#MyWay MaTransition
					for i in range(0, len(list_expression_id)) :
						expression_id = list_expression_id[i]
						expression = dao_expression_besoin.toGetExpression(expression_id)
						wkf_task.passingStepWorkflow(auteur,expression)'''


			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			#print("OKAY")
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la demande")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_add_demande_achat'))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_add_demande_achat'))

def get_print_demande(request):
	try:
		id = request.POST["id"]
		end = endpoint.reportingEndPoint()

		permission_number = 125
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'title' : 'Impression demande achat',
			'id' : id,
			'endpoint' : end,
			'roles':groupe_permissions,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleAchat/demande_achat/print.html')
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

def get_details_demande(request, ref):

	try:
		# droit = "LISTER_DEMANDE_ACHAT"
		# modules, utilisateur,roles,response = auth.toGetAuthDroit(droit, request)
		permission_number = 121
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		demande = dao_demande_achat.toGetDemande(ref)
		lignes = dao_ligne_demande_achat.toListLigneOfDemandes(demande.id)
		'''historique = dao_wkf_historique_demande.toListHistoriqueOfDemande(demande.id)

		if demande.statut.designation == "Créée":
			transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(demande.statut_id, demande.services_ref.id)
		else:
			transition_etape_suivant = dao_wkf_etape.toListEtapeSuivante(demande.statut_id)

		documents = dao_document_demande.toListDocumentbyDemande(demande.id)'''


		total = 0
		for ligne in lignes:
			t = ligne.prix_unitaire * ligne.quantite_demande
			total = total + t

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,demande)

		#print("demande statut", demande.statut.est_decisive)

		context = {
			'title' : "Demande d'achat N°%s" % demande.numero_demande,
			'model' : demande,
			'lignes' : lignes,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'total' : total,
			'content_type_id':content_type_id,
			'documents':documents,
			'roles':groupe_permissions,
			#'can_validate' : dao_droit.toGetDroitRole('VALIDER_BONACHAT',nom_role,utilisateur.nom_complet),
			#'can_reject' : dao_droit.toGetDroitRole('REJETER_BONACHAT',nom_role,utilisateur.nom_complet),
			#'can_cancel' : dao_droit.toGetDroitRole('ANNULER_BONACHAT',nom_role,utilisateur.nom_complet),
			"utilisateur" : utilisateur,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 2
		}
		template = loader.get_template("ErpProject/ModuleAchat/demande_achat/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_demande_achat'))

def get_printing_demande(request):
	try:
		permission_number = 121
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
		demande = dao_demande_achat.toGetDemande(ref)
		lignes = dao_ligne_demande_achat.toListLigneOfDemandes(demande.id)
		total = 0
		context = {
			'title' : "Demande d'achat N°%s" % demande.numero_demande,
			'model' : demande,
			'lignes' : lignes,
			'total' : total,
			'roles':groupe_permissions,
			"utilisateur" : utilisateur,
			'organisation' : dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 2
		}
		return weasy_print("ErpProject/ModuleAchat/rapport/demande_achat.html", "demande_achat.pdf", context)
	except Exception as e:
		# print('***ERREUR*****')
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_demande_achat'))


def get_treat_demande(request):
	# droit = "CREER_DEMANDE_ACHAT"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 120
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		etat_actuel_id = request.POST["doc_id"]
		#print("etat_actuel", etat_actuel_id)
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		lignes = dao_ligne_demande_achat.toListLigneOfDemandes(etat.id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
		#etat_besoins = dao_expression_besoin.toListExpressionsServiceReferent()
	except Exception as e:
		#print("Aucun etat de besoin trouvé")
		pass

	#print("ETAAAAAAAAATTTTTTTTTTTTT %s" % etat_actuel_id)



	context = {
		'title' : 'Traiter la demande d\'achat N° ' +etat.numero_demande,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 4,
		'etat' : etat,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'demande_wkf' : demande_wkf_id,
		'lignes_etat'  : lignes,
		}

	template = loader.get_template('ErpProject/ModuleAchat/demande_achat/treatment.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_treat_demande(request):
	#print("begin here")
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		fournisseur_id = request.POST["fournisseur_id"]
		demande_id = request.POST["etat_actuel_id"]
		demande = dao_demande_achat.toGetDemande(demande_id)
		#print("Lala")

		demande.fournisseur_id = fournisseur_id
		demande.save()


		#print("Loulou")
		if demande != None:
			list_ligne_id = request.POST.getlist("ligne_id",None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)

			for i in range(0, len(list_ligne_id)) :
				ligne_id = int(list_ligne_id[i])
				prix_unitaire = makeFloat(list_prix_unitaire[i])
				ligne = dao_ligne_demande_achat.toTreatLigneDemande(ligne_id,prix_unitaire)

			#Faire passer d'Etat
			wkf_task.passingStepWorkflow(auteur,demande)
			#Integre le dossiers Uploader here
			if 'file_upload' in request.FILES:
				nom_fichier = request.FILES['file_upload'].name

				#print(nom_fichier)
				#print("Debut file ")
				files = request.FILES.getlist("file_upload",None)
				dao_document.toUploadDocument(auteur, files, demande)

				'''for fichier in files:

					#print("fichier", fichier)
					nom_fichier = fichier.name
					nom_fichier = nom_fichier[:75]
					#print(nom_fichier)
					docs_dir = 'documents/'
					media_dir = media_dir + '/' + docs_dir
					save_path = os.path.join(media_dir, str(nom_fichier))
					path = default_storage.save(save_path, fichier)
					url = media_url + docs_dir + str(nom_fichier)
					#print(url)
					#print(bzb)

					document = dao_document.toCreateDocument("Demande d'achat",url, demande.etat,demande)
					document = dao_document.toSaveDocument(auteur, document)'''
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande.id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_treat_demande_achat'))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_treat_demande_achat'))

@transaction.atomic
def post_workflow_demande(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		demande_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, demande_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		demande_achat = dao_demande_achat.toGetDemande(demande_id)

		#print("print 2 %s %s %s " % (employe, etape, demande_achat))

		if demande_achat.statut.designation == "Créée":
			transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(demande_achat.statut_id, demande_achat.services_ref.id)
		else:
			transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(demande_achat.statut_id)

		for item in transitions_etapes_suivantes:
			if item.condition.designation == "Upload":

				#print("Upload")
				if 'file_upload' in request.FILES:
					nom_fichier = request.FILES['file_upload'].name

					#print(nom_fichier)
					#print("Debut file ")
					files = request.FILES.getlist("file_upload",None)
					dao_document.toUploadDocument(auteur, files, demande_achat)

					#On affecte le chemin de l'Image

					demande_achat.statut_id = etape.id
					demande_achat.etat = etape.designation
					demande_achat.save()

					# for fichier in files:

					# 	#print("fichier", fichier)
					# 	nom_fichier = fichier.name
					# 	nom_fichier = nom_fichier[:75]
					# 	#print(nom_fichier)
					# 	docs_dir = 'documents/'
					# 	media_dir = media_dir + '/' + docs_dir
					# 	save_path = os.path.join(media_dir, str(nom_fichier))
					# 	path = default_storage.save(save_path, fichier)
					# 	url = media_url + docs_dir + str(nom_fichier)
					# 	#print(url)
					# 	#print(bzb)


					# 	document = dao_document_demande.toCreateDocument("Demande d'achat",url, demande_achat.etat,demande_achat.id)
					# 	document = dao_document_demande.toSaveDocument(auteur, document)

					#print("docu saved")
			else:
				#print("mama")
				# Gestion des transitions dans le document
				demande_achat.statut_id = etape.id
				demande_achat.etat = etape.designation
				demande_achat.save()

		historique = dao_wkf_historique_demande.toCreateHistoriqueWorkflow(employe.id, etape.id, demande_achat.id)
		historique = dao_wkf_historique_demande.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_add_demande_achat'))


@transaction.atomic
def post_cancel_workflow_demande(request,ref):
	sid = transaction.savepoint()
	try:
		employe = identite.utilisateur(request)
		#print(employe)
		ref = int(ref)
		# WORKFLOWS INITIALS
		#print("pass here")
		demande = dao_demande_achat.toGetDemande(ref)

		type_document = "Demande achat"
		workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)
		etape = dao_wkf_etape.toGetEtapeFinalWorkflow(workflow.id)
		#print("etape")
		demande.statut_id = etape.id
		demande.etat = etape.designation
		demande.save()
		#print("we are here")

		historique = dao_wkf_historique_demande.toCreateHistoriqueWorkflow(employe.id, etape.id, demande.id)
		historique = dao_wkf_historique_demande.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande.id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_detail_demande_achat', args=(demande.id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_achat_achat_demande_achat'))


def get_expression_rapports(request):
	modules, utilisateur,response = auth.toGetAuth(request)

	if response != None:
		return response

	date_debut = request.POST["date_debut"]
	date_fin = request.POST["date_fin"]
	end = endpoint.reportingEndPoint()

	context = {
		'title' : 'Business intelligence',
		'endpoint' : end,
		'date_debut' : date_debut,
		'date_fin' : date_fin,
		'utilisateur' : identite.utilisateur(request),
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : dao_module.toListModulesInstalles(),
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	template = loader.get_template('ErpProject/ModuleAchat/rapport/rapport_expression.html')
	return HttpResponse(template.render(context, request))


#Expression de besoin
def get_lister_expression(request):
	try:
		permission_number = 118
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		model = dao_model.toListModel(dao_expression_besoin.toListExpressions(), permission_number, groupe_permissions, identite.utilisateur(request))

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des expressions des besoins',
			'model' : model,
			'utilisateur' : utilisateur,
			'view' : view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleAchat/expression/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE DES EXPRESSIONS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste ezeze')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_tableau_de_bord'))

def get_creer_expression(request):
	try:
		# droit = "CREER_EXPRESSION_BESOIN"
		# modules, utilisateur,roles,response = auth.toGetAuthDroit(droit,request)
		permission_number = 116
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		demandeurs = dao_employe.toListEmployesActifs()
		#print("Demand %s" % demandeurs)
		fournisseurs = dao_fournisseur.toListFournisseursActifs()
		articles = dao_article.toListArticlesAchetables()
		categories = dao_categorie_article.toListCategoriesArticle()
		dep_entrepots = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()

		centre_cout = dao_centre_cout.toListCentre_cout()

		#print("OKKKKKKKKKKKKKKKKKKKKKKKKK")


		context = {
			'title' : 'Créer une expression de besoin',
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4,
			'demandeurs' : demandeurs,
			'centre_cout':centre_cout,
			'fournisseurs' : fournisseurs,
			'articles' : articles,
			'warehouses' : dep_entrepots,
			'categories' : categories,
				}

		template = loader.get_template('ErpProject/ModuleAchat/expression/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		#print('erre ',e)
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES DETAILS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_expression'))

@transaction.atomic
def post_creer_expression(request):
	#print("Date probleme ____ 0")
	sid = transaction.savepoint()
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")
		#print("Date probleme ____ I")
		auteur = identite.utilisateur(request)
		date_prevue = request.POST["date"]
		#print("Date probleme ____ II")

		#print("start")
		# LA DATE EST AU FORMAT : dd/mm/yyyy
		# ON PROCEDE A LA CONVERSION DU STRING EN DATETIME
		date_prevue = timezone.datetime(int(date_prevue[6:10]), int(date_prevue[3:5]), int(date_prevue[0:2]))

		# date_prevue = date_prevue[6:10] + '-' + date_prevue[3:5] + '-' + date_prevue[0:2]
		# date_prevue = datetime.datetime.strptime(date_prevue, "%Y-%m-%d").date()


		demandeur_id = request.POST["demandeur_id"]
		justification = request.POST["justification"]
		service_ref_id = request.POST["service_ref_id"]
		centre_cout_id = None

		if centre_cout_id == 0:
			centre_cout_id = None

		numero = dao_expression_besoin.toGenerateNumeroExpression()
		expression = dao_expression_besoin.toCreateExpression(numero, date_prevue, justification, None , demandeur_id, "", "", "", service_ref_id,centre_cout_id)
		expression = dao_expression_besoin.toSaveExpression(auteur, expression)

		#Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)
			dao_document.toUploadDocument(auteur, files, expression)

		#print(expression)
		if expression != None :
			docs = Model_Image.objects.all()
			if docs != None:
				for doc in docs:
					print ("DOCCCCCCCCC %s" % doc.doc)
					expression.document = doc.doc
					expression.save()
				Model_Image.objects.all().delete()


			list_article_id = request.POST.getlist('article_id', None)
			list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
			list_description = request.POST.getlist("description",None)

			#print(len(list_prix_unitaire))
			#print(len(list_description))
			for i in range(0, len(list_article_id)) :
				#print("argh")
				article_id = int(list_article_id[i])
				quantite_demandee = makeFloat(list_quantite_demandee[i])
				#prix_unitaire = makeFloat(list_prix_unitaire[i])
				description = list_description[i]
				#print(article_id)

				#print(description)


				article = dao_article.toGetArticle(article_id)
				#unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				#print(article.id)
				#print(article.unite_id)
				unite_article = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_article_id = unite_article.id if unite_article else None
				ligne = dao_ligne_expression.toCreateLigneExpression(expression.id, article.id, quantite_demandee, 0, unite_article_id, description)
				ligne = dao_ligne_expression.toSaveLigneExpression(ligne)

			#Initialisation du workflow expression
			wkf_task.initializeWorkflow(auteur,expression)


			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(expression.id,)))
			#print("OKAY")
			#print("OKAY")
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_achat_detail_expression', args=(expression.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de l'expression")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_add_expression'))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_achat_add_expression'))


def get_print_expression(request):
	try:
		id = request.POST["id"]
		#print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK " + str(id))

		end = endpoint.reportingEndPoint()

		permission_number = 118
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'title' : 'Impression état de besoin',
			'id' : id,
			'endpoint' : end,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 4,

			'roles':groupe_permissions,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
		}
		template = loader.get_template('ErpProject/ModuleAchat/expression/print.html')
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

def get_details_expression(request, ref):
	#print("get_details_expression touché")

	try:
		# droit = "LISTER_EXPRESSION_BESOIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 118
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		expression = dao_expression_besoin.toGetExpression(ref)
		lignes = dao_ligne_expression.toListLigneOfExpressions(expression.id)

		total = 0
		for ligne in lignes:
			t = ligne.prix_unitaire * ligne.quantite_demande
			total = total + t

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,expression)



		#print("Fin de tout")
		context = {
			'title' : "Expression des besoins N°%s" % expression.numero_expression,
			'model' : expression,
			'lignes' : lignes,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'signee' : signee,
			'total' : total,
			'content_type_id':content_type_id,
			"documents":documents,
			'roles':groupe_permissions,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 2
		}
		template = loader.get_template("ErpProject/ModuleAchat/expression/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		# print("ERREUR")
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_expression'))

def get_printing_expression(request):
	# print('*************PRINT************')
	try:
		# print('*************PRINT************')
		permission_number = 118
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# ref = int(ref)
		if 'ref' in request.GET:
			ref = int(request.GET['ref'])
		expression = dao_expression_besoin.toGetExpression(ref)
		lignes = dao_ligne_expression.toListLigneOfExpressions(expression.id)
		title = "Expression des besoins N°%s" % expression.numero_expression
		context = {
			'title' : title,
			'model' : expression,
			'lignes' : lignes,
			# 'total' : total,
			'roles':groupe_permissions,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 2
		}
		# template = loader.get_template("ErpProject/ModuleAchat/rapport/expression.html")
		# return weasy_print("ErpProject/ModuleAchat/rapport/expression.html", "detail_expression.pdf", context)
		# return HttpResponse(template.render(context, request))
		html_string = render_to_string('ErpProject/ModuleAchat/rapport/expression.html', context)

		download_dir = settings.DOWNLOAD_DIR
		css_dir = settings.CSS_DIR

		font_config = FontConfiguration()
		html = HTML(string=html_string)
		css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
		pdf_file = html.write_pdf(target=os.path.join(download_dir, 'expression_besoin.pdf'), stylesheets=[css_print], font_config=font_config)

		fs = FileSystemStorage(download_dir)
		with fs.open('expression_besoin.pdf') as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(title)
			return response

		return response
	except Exception as e:
		# print('***ERREUR*****')
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_expression'))


def get_modifier_expression(request, ref):

	try:

		# droit = "MODIFIER_EXPRESSION_BESOIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 117
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		id = int(ref)
		expression = dao_expression_besoin.toGetExpression(id)
		lignes_expression = dao_ligne_expression.toListLigneOfExpressions(id)
		articles = dao_article.toListArticlesOfServiceReferent(expression.services_ref)
		centre_cout = dao_centre_cout.toListCentre_cout()
		context = {
			'title' : "Modifier l'expréssion %s" % expression.numero_expression,
			'model' : expression,
			'lignes':lignes_expression,
			'articles':articles,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'centre_cout':centre_cout,
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/expression/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_expression'))


@transaction.atomic
def post_modifier_expression(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		identifiant = int(request.POST["ref"])
		#print("start")

		demandeur_id = request.POST["demandeur_id"]
		justification = request.POST["justification"]
		service_ref_id = request.POST["service_ref_id"]

		expression_last = dao_expression_besoin.toGetExpression(identifiant)
		date_prevue = expression_last.date_expression
		statut_id = expression_last.statut_id

		numero = dao_expression_besoin.toGenerateNumeroExpression()
		expression = dao_expression_besoin.toCreateExpression(numero, date_prevue, justification, statut_id , demandeur_id, "", "", "", service_ref_id, None)
		is_done = dao_expression_besoin.toUpdateExpression(identifiant, expression)

		#print(expression)
		if is_done :

			list_ligne_id = request.POST.getlist('ligne_id',None)

			list_article_id = request.POST.getlist('article', None)
			list_quantite_demandee = request.POST.getlist("quantite_demandee", None)
			list_prix_unitaire = request.POST.getlist("prix_unitaire", None)
			list_description = request.POST.getlist("description",None)

			list_all_ligne_id = request.POST.getlist('all_ligne_id', None)


			#print(len(list_article_id))
			#print(len(list_quantite_demandee))
			#print(len(list_prix_unitaire))
			#print(len(list_description))
			i=0
			for i in range(0, len(list_all_ligne_id)):
				is_find = False
				the_item = list_all_ligne_id[i]
				for j in range(0, len(list_ligne_id)):
					if the_item == list_ligne_id[j]:
						is_find = True
				if is_find == False:
					dao_ligne_expression.toDeleteLigneExpression(the_item)


			#print('taille liste id %s'%(len(list_ligne_id)))
			for i in range(0, len(list_article_id)):

				article_id = int(list_article_id[i])
				#print("you've win id article %s dans la position %s"%(article_id,i))

				quantite_demandee = makeFloat(list_quantite_demandee[i])
				#prix_unitaire = makeFloat(list_prix_unitaire[i])
				description = list_description[i]
				#print("you've win description %s"%(description))

				article = dao_article.toGetArticle(article_id)

				#print("you've win article %s"%(article))
				#print("you've win article unite %s"%(article.unite_id))
				unite_article = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
				unite_article_id = unite_article.id if unite_article else None
				#print('uinté %s'%(unite_article))
				#/******************************
				#print('list_ligne_id[i] %s'%(list_ligne_id[i]))
				ligne_id = int(list_ligne_id[i])
				#print('################# ligne id %s'%(ligne_id))
				if ligne_id != 0:

					ligne_expression = dao_ligne_expression.toCreateLigneExpression(identifiant, article.id, quantite_demandee, 0,unite_article_id, description)
					ligne_expression=dao_ligne_expression.toUpdateLigneExpression(ligne_id,ligne_expression)
				else:

					ligne_expression = dao_ligne_expression.toCreateLigneExpression(identifiant, article.id, quantite_demandee, 0,unite_article_id, description)
					ligne_expression = dao_ligne_expression.toSaveLigneExpression(ligne_expression)



			#//**************old version*************
				"""for i in range(0, len(list_ligne_id)):
					ligne_id = int(list_ligne_id[i])
					dao_ligne_expression.toDeleteLigneExpression(ligne_id)

				for i in range(0, len(list_article_id)):
					#print("argh")
					article_id = int(list_article_id[i])
					quantite_demandee = makeFloat(list_quantite_demandee[i])
					#prix_unitaire = makeFloat(list_prix_unitaire[i])
					description = list_description[i]
					#print(article_id)

					#print(description)


					article = dao_article.toGetArticle(article_id)
					#print(article)
					#unite_achat = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
					#print(article.id)
					#print(expression.id)
					unite_article = dao_unite_achat_article.toGetUniteAchatOfArticle(article.id, article.unite_id)
					if quantite_demandee != 0:
						#ligne = dao_ligne_expression.toCreateLigneExpression(identifiant, article.id, quantite_demandee, 0, unite_article.id, description)
						#ligne = dao_ligne_expression.toSaveLigneExpression(ligne)
				"""
				# NOTIFICATION POUR MODIFICATION PERCU DANS SON TRUC
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(expression.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_expression', args=(identifiant,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_add_expression'))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_achat_add_expression'))

@transaction.atomic
def post_workflow_expression(request):
	sid = transaction.savepoint()
	try:
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		expression_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, expression_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		expression = dao_expression_besoin.toGetExpression(expression_id)

		#print("print 2 %s %s %s " % (employe, etape, expression))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(expression.statut_id, expression.services_ref.id)
		for item in transitions_etapes_suivantes:

			# Gestion des transitions dans le document
			expression.statut_id = etape.id
			expression.etat = etape.designation
			expression.save()

		historique = dao_wkf_historique_expression.toCreateHistoriqueWorkflow(employe.id, etape.id, expression.id)
		historique = dao_wkf_historique_expression.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_expression', args=(expression_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_detail_expression', args=(expression_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_achat_add_expression'))



@transaction.atomic
def post_cancel_workflow_expression(request,ref):
	sid = transaction.savepoint()
	try:
		employe = identite.utilisateur(request)
		#print(employe)
		# WORKFLOWS FINAL
		type_document = "Etat de besoin"
		#print("ici")
		workflow = dao_wkf_workflow.toGetWorkflowFromTypeDoc(type_document)
		#print("ici1")
		etape = dao_wkf_etape.toGetEtapeFinalWorkflow(workflow.id)
		#print(etape)
		#print("ici2")
		ref = int(ref)
		#print("ici3")
		expression = dao_expression_besoin.toGetExpression(ref)
		expression.statut_id = etape.id
		#print("ici4")
		expression.etat = etape.designation
		expression.save()

		historique = dao_wkf_historique_expression.toCreateHistoriqueWorkflow(employe.id, etape.id, expression.id)
		#print("ici5")
		historique = dao_wkf_historique_expression.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#return HttpResponseRedirect(reverse('module_achat_details_bon_achat', args=(demande.id,)))
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_achat_detail_expression', args=(expression.id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_detail_expression', args=(expression.id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_achat_add_expression'))



#Catégorie Articles
def get_lister_categorie_articles(request):
	try:
		# droit = "LISTER_CATEGORIE_ARTICLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 12
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		model = dao_model.toListModel(dao_categorie_article.toListCategoriesArticle(), permission_number, groupe_permissions, identite.utilisateur(request))




		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : 'Catégorie Articles',
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'view' : view,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'model' : model,
			'menu' : 4
			}
		template = loader.get_template('ErpProject/ModuleAchat/categorie/article/list.html')

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_article'))

def get_creer_categorie_articles(request):
	try:
		# droit = "CREER_CATEGORIE_ARTICLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 12
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		context = {
			'title' : "Nouvelle catégorie d'article",
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/categorie/article/add.html")

		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_article'))

def post_creer_categorie_articles(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		categorie = dao_categorie_article.toSaveCategorieArticle(auteur, categorie)

		url = '<a class="lien chargement-au-click" href="/achat/categories/article/item/'+ str(categorie.id) +'/">'+ categorie.designation+ '</a>'
		categorie.url = url
		categorie.save()

		if categorie != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_achat_details_categorie_articles", args=(categorie.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de le categorie d'article")
			return HttpResponseRedirect(reverse('module_achat_add_categorie_articles'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_article'))

def get_details_categorie_articles(request, ref):

	# droit = "LISTER_CATEGORIE_ARTICLE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 12
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	if utilisateur.nom_complet != "SYSTEM":
		role = dao_role.toGetRoleDeLaPersonne(utilisateur.id)
		if role == None: return HttpResponseRedirect(reverse("backoffice_erreur_role"))
		else :
			modules = dao_module.toListModulesAttachesAuRole(role.id)

	try:
		ref = int(ref)
		categorie = dao_categorie_article.toGetCagorieArticle(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categorie)

		context = {
			'title' : categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'sous_modules':sous_modules,
			#"can_create" : dao_droit.toGetDroitRole('CREER_CATEGORIE_ARTICLE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_CATEGORIE_ARTICLE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CATEGORIE_ARTICLE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/categorie/article/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL CREATION CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_article'))

def get_modifier_catagorie_articles(request, ref):

	# modules, utilisateur,response = auth.toGetAuth(request)
	permission_number = 10
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		id = int(ref)
		categorie = dao_categorie_article.toGetCagorieArticle(id)
		context = {
			'title' : "Modifier la catégorie %s" % categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/categorie/article/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MISE A JOUR CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_article'))

def post_modifier_categorie_articles(request):

	try:
		id = int(request.POST["ref"])
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		is_done = dao_categorie_article.toUpdateCategorieArticle(id, categorie)

		if is_done == True :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_achat_details_categorie_articles", args=(id,)))
		else : return HttpResponseRedirect(reverse('module_achat_update_categorie_articles', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST DE LA MISE A JOUR CATEGORIE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_article'))


#Catégorie unité de mésure
def get_lister_categorie_unites(request):
	try:
		permission_number = 20
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		model = dao_model.toListModel(dao_categorie_unite.toListCategoriesUnite(), permission_number, groupe_permissions, identite.utilisateur(request))

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : 'Catégorie Unites',
			'utilisateur' : identite.utilisateur(request),
			'actions':auth.toGetActions(modules,utilisateur),
			'view' : view,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_ACHAT,
			'sous_modules': sous_modules,
			'model' : model,
			'menu' : 4
			}
		template = loader.get_template('ErpProject/ModuleAchat/categorie/unite/list.html')

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT LISTE CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_unite'))

def get_creer_categorie_unites(request):

	try:
		# droit = "CREER_CATEGORIE_UNITE_DE_MESURE"
		# # modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 17
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'title' : "Nouvelle catégorie d'unite",
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/categorie/unite/add.html")

		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_unite'))

def post_creer_categorie_unites(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		categorie = dao_categorie_unite.toSaveCategorieUnite(auteur, categorie)

		if categorie != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_achat_details_categorie_unites", args=(categorie.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de la categorie d'unite")
			return HttpResponseRedirect(reverse('module_achat_add_categorie_unites'))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_unite'))

def get_details_categorie_unites(request, ref):

	# droit = "LISTER_CATEGORIE_UNITE_DE_MESURE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 20
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		ref = int(ref)
		categorie = dao_categorie_unite.toGetCagorieUnite(ref)

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categorie)
		context = {
			'title' : categorie.designation,
			'model' : categorie,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'sous_modules':sous_modules,
			#"can_create" : dao_droit.toGetDroitRole('CREER_CATEGORIE_UNITE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_CATEGORIE_UNITE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CATEGORIE_UNITE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/categorie/unite/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL CREATION CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_unite'))

def get_modifier_catagorie_unites(request, ref):

	# droit = "MODIFIER_CATEGORIE_UNITE_DE_MESURE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 18
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		id = int(ref)
		categorie = dao_categorie_unite.toGetCagorieUnite(id)
		context = {
			'title' : "Modifier la catégorie %s" % categorie.designation,
			'model' : categorie,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"utilisateur" : utilisateur,
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModuleAchat/categorie/unite/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MISE A JOUR CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_unite'))

def post_modifier_categorie_unites(request):

	try:
		id = int(request.POST["ref"])
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]

		categorie = dao_categorie.toCreateCategorie(designation)
		is_done = dao_categorie_unite.toUpdateCategorieUnite(id, categorie)

		if is_done == True : return HttpResponseRedirect(reverse("module_achat_details_categorie_unites", args=(id,)))
		else : return HttpResponseRedirect(reverse('module_achat_update_categorie_unites', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST DE LA MISE A JOUR CATEGORIE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_categorie_unite'))


#Unité de mésure
def get_lister_unites(request):

	try:
		permission_number = 482
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		model = dao_model.toListModel(dao_unite.toListUnite(), permission_number, groupe_permissions, identite.utilisateur(request))


		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : "Liste des unités de mésure",
			'model' : model,
			'view' : view,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'sous_modules': sous_modules,
			'modules':modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleAchat/unite/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_unite'))

def get_creer_unite(request):
	try:
		permission_number = 483
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'title' : 'Nouvelle unité de mésure',
			'categories' : dao_categorie_unite.toListCategoriesUnite(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleAchat/unite/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU CREER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_unite'))

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
			return HttpResponseRedirect(reverse('module_achat_details_unite', args=(unite.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de l'unité de mésure")
			return HttpResponseRedirect(reverse('module_achat_add_unite'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_add_unite'))

def get_modifier_unite(request, ref):
	try:
		# droit="MODIFIER_UNITE_DE_MESURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 484
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		id = int(ref)
		unite = dao_unite.toGetUnite(id)
		context = {
			'title' : 'Modifier %s' % unite.designation,
			'categories' : dao_categorie_unite.toListCategoriesUnite(),
			'model' : unite,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleAchat/unite/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU MODIFIER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Modifier')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_unite'))

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

		if is_done == True : return HttpResponseRedirect(reverse('module_achat_details_unite', args=(id,)))
		else : return HttpResponseRedirect(reverse('module_achat_update_unite', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFIER UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_update_unite', args=(id,)))

def get_details_unite(request, ref):

	try:
		permission_number = 482
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		unite = dao_unite.toGetUnite(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,unite)

		context = {
			'title' : unite.designation,
			'model' : unite,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'sous_modules':sous_modules,
			"utilisateur" : utilisateur,
			"modules" : modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleAchat/unite/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL UNITE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_unite'))


#Condition de reglement
def get_lister_reglement(request):
	try:

		permission_number = 317
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		model = dao_model.toListModel(dao_condition_reglement.toListConditionsReglement(), permission_number, groupe_permissions, identite.utilisateur(request))

		context = {
			'title' : "Liste des conditions de réglement",
			'model' : model,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_CONDITION_REGLEMENT',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleAchat/reglement/list.html")
		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE REGELEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request, e)
		return HttpResponseRedirect(reverse('module_achat_list_reglement'))

def get_creer_reglement(request):

	try:
		permission_number = 318
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'title' : "Nouvelle condition de Reglement",
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleAchat/reglement/add.html")
		return HttpResponse(template.render(context,request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_reglement'))

def post_creer_reglement(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		nombre_jours = request.POST["nombre_jours"]

		reglement = dao_condition_reglement.toCreateConditionReglement(designation,nombre_jours)
		reglement = dao_condition_reglement.toSaveConditionReglement(auteur,reglement)

		if reglement != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_achat_details_reglement", args=(reglement.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du reglement")
			return HttpResponseRedirect(reverse('module_achat_add_reglement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Reglement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_reglement'))

def get_details_reglement(request, ref):

	try:
		permission_number = 317
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		condition_reglement = dao_condition_reglement.toGetConditionReglement(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,expression)

		context = {
			'title' : condition_reglement.designation,
			'model' : condition_reglement,
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
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleAchat/reglement/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_reglement'))

def get_modifier_reglement(request, ref):

	try:
		permission_number = 319
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		condition_reglement = dao_condition_reglement.toGetConditionReglement(ref)
		context = {
			'title' : 'Modifier la condition de réglement %s' % condition_reglement.designation,
			'model' : condition_reglement,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModuleAchat/reglement/update.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Modifier')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_reglement'))

def post_modifier_reglement(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		nombre_jours = request.POST["nombre_jours"]

		reglement = dao_condition_reglement.toCreateConditionReglement(designation,nombre_jours)
		is_done = dao_condition_reglement.toUpdateConditionReglement(id, reglement)

		if is_done == True : return HttpResponseRedirect(reverse("module_achat_details_reglement", args=(id,)))
		else : return HttpResponseRedirect(reverse('module_achat_update_reglement', args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFIER REGLEMENT\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Regelement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_update_reglement', args=(id,)))


# ARTICLES ACHETABLES CONTROLLER
def get_lister_article(request):

	try:
		permission_number = 7
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#model = dao_article.toListArticlesAchetables()
		if utilisateur.unite_fonctionnelle != None:
			model = dao_model.toListModel(dao_article.toListArticlesOfServiceReferent(utilisateur.unite_fonctionnelle.id), permission_number, groupe_permissions, identite.utilisateur(request))
		else:
			model = dao_model.toListModel(dao_article.toListArticlesAchetables(), permission_number, groupe_permissions, identite.utilisateur(request))

		#print("model", model)
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : "Liste des articles achetables",
			'model' : model,
			'view' : view,
			'types_article' : dao_type_article.toListTypesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleAchat/article/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut List Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_articles'))

def get_creer_article(request):

	try:
		permission_number = 5
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		dep_entrepots = None

		if utilisateur.unite_fonctionnelle != None:
			dep_entrepots = dao_unite_fonctionnelle.toListOfOneUniteFonctionnelle(utilisateur.unite_fonctionnelle.id)
		else:
			dep_entrepots = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()


		context = {
			'title' : 'Nouvel article',
			'unites' : dao_unite.toListUnite(),
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'types_article' : dao_type_article.toListTypesArticle(),
			'categories' : dao_categorie_article.toListCategoriesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'warehouses':dep_entrepots,
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleAchat/article/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA CREATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Creer Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_articles'))

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

		designation_court = request.POST["designation_court"]
		code_article = request.POST["code_article"]
		code_barre = request.POST["code_barre"]
		type_article = int(request.POST["type_article"])
		categorie_id = int(request.POST["categorie_id"])
		prix_unitaire = makeFloat(request.POST["prix_unitaire_article"])
		service_ref_id = int(request.POST['service_ref_id'])
		image = ""

		#print("TYPE ARTICLE %s" % type_article)
		#print("CATEGORIE ARTICLE %s" % categorie_id)


		article = dao_article.toCreateArticle(image, designation, unite_id, est_commercialisable, est_achetable, est_manufacturable, est_fabriquable, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire, None, est_amortissable,service_ref_id)
		article = dao_article.toSaveArticle(auteur, article)

		#print("ARTICLES SAVED %s" % article)


		if article != None :

			# CREATION DES STOCKS POUR L'ARTICLE
			# SCTOCK EMPLACEMENT D'ENTREE
			'''if article.est_achetable == True :
				type_emplacement = dao_type_emplacement.toGetTypeEmplacementEntree()
				#print("type empl %s" % type_emplacement)
				emplacement = dao_emplacement.toGetEmplacementEntree(type_emplacement)
				#print("emplace %s" % emplacement)
				stock_entrant = dao_stock_article.toCreateStockArticle(article.id, 0, emplacement.id, 0)
				#print("stock %s" % stock_entrant)
				dao_stock_article.toSaveStockArticle(stock_entrant)
				#print("EMPLE ENTREE ")

			# SCTOCK EMPLACEMENT DE RESERVE
			if article.est_manufacturable == True :
				type_emplacement = dao_type_emplacement.toGetTypeEmplacementReserve()
				emplacement = dao_emplacement.toGetEmplacementReserve(type_emplacement)
				stock_reserve = dao_stock_article.toCreateStockArticle(article.id, 0, emplacement.id, 0)
				dao_stock_article.toSaveStockArticle(stock_reserve)
				#print("RESERVE")

			#print("STOCK EMPLACEMENT")
			# SCTOCK EMPLACEMENT DE STOCKAGE
			type_emplacement = dao_type_emplacement.toGetTypeEmplacementStock()
			#print("type empla %s" % type_emplacement)
			emplacements = dao_emplacement.toGetEmplacementStock(type_emplacement).filter(designation = "Stockage")
			for item in emplacements:
				#print("empla %s" % item)
				stock_stockage = dao_stock_article.toCreateStockArticle(article.id, 0, item.id, 0)
				dao_stock_article.toSaveStockArticle(stock_stockage)
				break'''

			if type_article != "2":
				emplacement_sba = dao_emplacement.toGetEmplacementBySBA()
				#print("emplace", emplacement_sba)
				#print(emplacement_sba.id)
				stock_article = dao_stock_article.toCreateStockArticle(article.id,0,emplacement_sba.id)
				stock_article = dao_stock_article.toSaveStockArticle(stock_article)

				unite_fonctionnelle = dao_unite_fonctionnelle.toGetUniteFonctionnelle(service_ref_id)
				#print("unit",unite_fonctionnelle)
				stock_article = dao_stock_article.toCreateStockArticle(article.id,0,unite_fonctionnelle.emplacement_id)
				stock_article = dao_stock_article.toSaveStockArticle(stock_article)
				#print(buzoba)








			#print("CREATION UNITE")

			# CREATION DE L'UNITE D'ACHAT
			unite_achat = dao_unite_achat_article.toCreateUniteAchat(article.id, article.unite_id)
			unite_achat = dao_unite_achat_article.toSaveUniteAchat(auteur, unite_achat)

			#print("FIN CREATION UNITE")


			# CREATION DES FOURNISSEUR_ARTICLE S'IL Y A
			list_fournisseur_id = request.POST.getlist("fournisseur_id", None)
			list_prix_unitaire_fournisseur = request.POST.getlist("prix_unitaire_fournisseur", None)
			list_quantite_minimale = request.POST.getlist("quantite_minimale", None)

			for i in range(0 , len(list_fournisseur_id)):
				fournisseur_id = int(list_fournisseur_id[i])
				if fournisseur_id != 0 :
					prix_unitaire_fournisseur = 0
					try:
						prix_unitaire_fournisseur = makeFloat(list_prix_unitaire_fournisseur[i])
					except Exception as e:
						pass

					quantite_minimale = 0
					try:
						quantite_minimale = makeFloat(list_quantite_minimale[i])
					except Exception as e:
						pass

					fournisseur_article = dao_fournisseur_article.toCreateFournisseurArticle(article.id, fournisseur_id, prix_unitaire_fournisseur, quantite_minimale)
					fournisseur_article = dao_fournisseur_article.toSaveFournisseurArticle(auteur, fournisseur_article)

			if 'image_upload' in request.FILES:
				file = request.FILES["image_upload"]
				article_img_dir = 'articles/'
				media_dir = media_dir + '/' + article_img_dir
				save_path = os.path.join(media_dir, str(article.id) + ".jpg")
				path = default_storage.save(save_path, file)
				#On affecte le chemin de l'Image
				article.image = media_url + article_img_dir + str(article.id) + ".jpg"
				article.save()
			transaction.savepoint_commit(sid)
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_achat_details_article", args=(article.id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création de l'article")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_achat_add_article'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer Article')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_articles'))

def get_modifier_article(request, ref):

	try:
		permission_number = 6
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		unite_fonctionnelle = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()
		id = int(ref)
		article = dao_article.toGetArticle(id)
		context = {
			'title' : 'Modifier %s' % article.designation,
			'model' : article,
			'unites' : dao_unite.toListUnite(),
			'fournisseurs' : dao_fournisseur.toListFournisseursActifs(),
			'types_article' : dao_type_article.toListTypesArticle(),
			'categories' : dao_categorie_article.toListCategoriesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"unite_fonctionnelle":unite_fonctionnelle,
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleAchat/article/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA MODIFICATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Modifier Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_articles'))

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

		est_commercialisable = False
		if "est_commercialisable" in request.POST : est_commercialisable = True

		est_achetable = False
		if "est_achetable" in  request.POST : est_achetable = True

		est_manufacturable = False
		if "est_manufacturable" in request.POST : est_manufacturable = True

		est_fabriquable = False
		if "est_fabriquable" in request.POST : est_fabriquable = True

		designation_court = request.POST["designation_court"]
		code_article = request.POST["code_article"]
		code_barre = request.POST["code_barre"]
		type_article = int(request.POST["type_article"])
		categorie_id = int(request.POST["categorie_id"])
		prix_unitaire = makeFloat(request.POST["prix_unitaire_article"])
		service_ref_id = int(request.POST['service_ref_id'])

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

		article = dao_article.toCreateArticle(image, designation, unite_id, est_commercialisable, est_achetable, est_manufacturable, est_fabriquable, designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire,service_ref_id)
		compte = dao_compte.toGetCompteFournisseur()
		if article.compte_id == None and compte != None:
			article.compte_id = compte.id

		is_done = dao_article.toUpdateArticle(id, article)



		if is_done == True :
			# CREATION DES FOURNISSEUR_ARTICLE S'IL Y A
			list_ligne_id = request.POST.getlist('ligne_id',None)
			list_all_ligne_id = request.POST.getlist('all_ligne_id', None)

			list_fournisseur_id = request.POST.getlist("fournisseur_id", None)
			list_prix_unitaire_fournisseur = request.POST.getlist("prix_unitaire_fournisseur", None)
			list_quantite_minimale = request.POST.getlist("quantite_minimale", None)

			#print("ligne", list_ligne_id)
			#print("all ligne", list_all_ligne_id)
			#print(list_fournisseur_id)
			#print(list_prix_unitaire_fournisseur)
			#print(list_quantite_minimale)
			i = 0
			for i in range(0, len(list_all_ligne_id)):
				is_find = False
				the_item = list_all_ligne_id[i]
				for j in range(0, len(list_ligne_id)):
					if the_item == list_ligne_id[j]:
						is_find = True
				if is_find == False:
					dao_fournisseur_article.toDeleteFournisseurArticle(the_item)

			try:
				for i in range(0 , len(list_fournisseur_id)):
					fournisseur_id = int(list_fournisseur_id[i])
					#print("************", fournisseur_id)
					ligne_id = int(list_ligne_id[i])
					prix_unitaire_fournisseur = makeFloat(list_prix_unitaire_fournisseur[i])
					quantite_minimale = makeFloat(list_quantite_minimale[i])

					if ligne_id !=0:
						fournisseur_article = dao_fournisseur_article.toCreateFournisseurArticle(id, fournisseur_id, prix_unitaire_fournisseur, quantite_minimale)
						fournisseur_article = dao_fournisseur_article.toUpdateFournisseurArticle(ligne_id, fournisseur_article)
					else:
						fournisseur_article = dao_fournisseur_article.toCreateFournisseurArticle(id, fournisseur_id, prix_unitaire_fournisseur, quantite_minimale)
						fournisseur_article = dao_fournisseur_article.toSaveFournisseurArticle(auteur, fournisseur_article)
			except Exception as em:
				#print("on updating fournisseur article", em)
				pass

			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse("module_achat_details_article", args=(id,)))
		else :
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse("module_achat_update_article", args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFICATION ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier Article')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_update_article', args=(id,)))

def get_details_article(request, ref):

	try:
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
			'types_article' : dao_type_article.toListTypesArticle(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'fournisseurs_article' : dao_fournisseur_article.toListFournisseursOf(article.id),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			#"can_create" : dao_droit.toGetDroitRole('CREER_ARTICLE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_ARTICLE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_ARTICLE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 5
		}
		template = loader.get_template("ErpProject/ModuleAchat/article/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL ARTICLE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detail Article')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_update_article', args=(id,)))

def get_json_get_prix_article(request):
	try:
		article_id = int(request.GET["ref"])
		article = dao_article.toGetArticle(article_id)
		#print("Article %s" % article)

		compte_id = None
		compte_name = None
		symbole_unite = None
		try:
			#print("Inside")
			compte_id = article.compte_id
			compte_name = article.compte.numero + ' ' + article.compte.designation
		except Exception as e:
			pass

		if article.unite:
			symbole_unite = article.unite.symbole_unite
		else:
			symbole_unite = "Elt"
		data = {
			"id" : article.id,
			"designation":article.designation,
			"compte_id":compte_id,
			"compte_designation":compte_name,
			"prix_unitaire" : article.prix_unitaire,
			"symbole_unite" : symbole_unite,
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
		# assets = dao_asset.toGetAssetByArticle(article_id)


		data = {
			"designation" : article.designation,
			"stock_article_id" : stock_id,
			"prix_unitaire" : article.prix_unitaire,
			"symbole_unite" : unite.symbole_unite,
			'united_id':unite.id,
		}
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print(e)
		return JsonResponse(data, safe=False)

def get_details_list_asset_of_article(request):
	data = []
	try:
		article_id = int(request.GET["ref"])
		service = request.GET["service"]
		# assets = dao_asset.toGetAssetByArticle(article_id)
		assets = dao_asset.toGetAssetByArticleOfEmplacement(article_id,service)
		# print("ASSET", assets)
		for el in assets:
			item = {"id" : el.id,"code" :el.numero_identification}
			data.append(item)
		# print('BEFORE PASS CONTENT', data)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse(data, safe=False)

# FOURNISSEUR CONTROLLER
def get_lister_fournisseurs(request):

	try:
		permission_number = 4
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		model = dao_model.toListModel(dao_fournisseur.toListFournisseursActifs(), permission_number, groupe_permissions, identite.utilisateur(request))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des fournisseurs',
			'model' : model,
			"utilisateur" : utilisateur,
			'view' : view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleAchat/fournisseur/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA LISTE FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Liste Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_fournisseurs'))

def get_creer_fournisseur(request):

	try:
		permission_number = 1
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		civilite=dao_civilite.listeCivilite()
		context = {
			'title' : 'Nouveau fournisseur',
			'pays' : dao_place.toListPlacesOfType(1),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'isPopup': True if 'isPopup' in request.GET else False,
			"modules" : modules,
			"civilite":civilite,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 3,
		}
		template = loader.get_template("ErpProject/ModuleAchat/fournisseur/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE CREER FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Creer Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_fournisseurs'))

def post_creer_fournisseur(request):
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		nom_complet = request.POST["nom_complet"]
		est_particulier = request.POST["est_particulier"]
		if est_particulier != "0":
			est_particulier = True
		else:
			est_particulier = False
		email = request.POST["email"]
		phone = request.POST["phone"]
		adresse = request.POST["adresse"]
		commune_quartier_id = request.POST["commune_quartier_id"]
		categorie_id = None #request.POST["categorie_id"]
		civilite_id = None #request.POST["civilite_id"]
		langue = request.POST["langue"]
		image = ""
		isPopup = request.POST["isPopup"]
		# print('**FOURNISSEUR INFO**')

		#compte = dao_compte.toGetCompteFournisseur()

		fournisseur = dao_fournisseur.toCreateFournisseur(nom_complet,None,None, nom_complet ,image,email,phone,adresse,commune_quartier_id, langue, True,"","2000-01-01","","",categorie_id,"2000-01-01",None, est_particulier)
		fournisseur = dao_fournisseur.toSaveFournisseur(auteur,fournisseur)
		# print('FOURNISSEUR CREER', fournisseur)

		url = '<a class="lien chargement-au-click" href="/achat/fournisseur/item/'+ str(fournisseur.id) +'/">'+ fournisseur.nom_complet + '</a>'

		fournisseur.url = url
		fournisseur.save()

		if fournisseur != None :
			if 'image_upload' in request.FILES:
				file = request.FILES["image_upload"]
				fournisseur_img_dir = 'personnes/'
				media_dir = media_dir + '/' + fournisseur_img_dir
				save_path = os.path.join(media_dir, str(fournisseur.id) + ".jpg")
				path = default_storage.save(save_path, file)
				fournisseur.image = media_url + fournisseur_img_dir + str(fournisseur.id) + ".jpg"
				fournisseur.save()
				# print('**FOURNISSEUR SAVE IMAGE**')

			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse("module_achat_details_fournisseur", args=(fournisseur.id,))) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du fournisseur")

		return HttpResponseRedirect(reverse('module_achat_add_fournisseur')) if isPopup =='False' else HttpResponse('<script type="text/javascript">window.close();</script>')

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		# print('Erreur Post Creer Fournisseur')
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_fournisseurs'))

def get_modifier_fournisseur(request, ref):

	try:
		permission_number = 425
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		id = int(ref)
		fournisseur = dao_fournisseur.toGetFournisseur(id)
		pays = province = ville = commune = None
		#print(fournisseur.commune_quartier_id)

		if fournisseur.commune_quartier_id != None and fournisseur.commune_quartier_id != 0:
			#print("ICI")
			commune = dao_place.toGetPlace(fournisseur.commune_quartier_id)
			ville = dao_place.toGetPlace(commune.parent_id)
			province = dao_place.toGetPlace(ville.parent_id)
			pays = dao_place.toGetPlace(province.parent_id)

		civilite=dao_civilite.listeCivilite()
		context = {
			'title' : 'Modifier %s' % fournisseur.nom_complet,
			'pays' : dao_place.toListPlacesOfType(1),
			'le_pays' : pays,
			"civilite":civilite,
			'la_province' : province,
			'la_ville' : ville,
			'la_commune' : commune,
			'model' : fournisseur,
			"utilisateur" : utilisateur,
			'comptes': dao_compte.toListComptesDeClasse(4),
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleAchat/fournisseur/update.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DU MODIFIER FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_fournisseurs'))

def post_modifier_fournisseur(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		nom_complet = request.POST["nom_complet"]
		est_particulier = request.POST["est_particulier"]
		if est_particulier != "0":
			est_particulier = True
		else:
			est_particulier = False
		email = request.POST["email"]
		phone = request.POST["phone"]
		adresse = request.POST["adresse"]
		compte_id = int(request.POST["compte_id"])
		commune_quartier_id = int(request.POST["commune_quartier_id"])
		categorie_id = None #int(request.POST["categorie_id"])
		civilite_id = None #int(request.POST["civilite_id"])
		langue = request.POST["langue"]
		#image_string = request.POST["image_upload_string"]



		#personne = dao_personne.toCreatePersonne(auteur, nom_complet, image, est_particulier, adresse, commune_quartier_id, categorie_id, civilite_id, phone, email, langue)
		personne = dao_personne.toGetPersonne(id)
		personne = dao_personne.toCreatePersonne(personne.prenom,personne.nom,personne.postnom,nom_complet,personne.image,email,phone,adresse,commune_quartier_id,langue,True, personne.lieu_de_naissance, personne.date_de_naissance, compte_id, est_particulier)
		compte = dao_compte.toGetCompteFournisseur()
		if personne.compte_id == None and compte != None:
			personne.compte_id = compte.id

		is_done = dao_fournisseur.toUpdateFournisseur(id,personne)

		if is_done != False :
			fournisseur = dao_fournisseur.toGetFournisseur(id)
			if 'image_upload' in request.FILES:
				file = request.FILES["image_upload"]
				fournisseur_img_dir = 'personnes/'
				media_dir = media_dir + '/' + fournisseur_img_dir
				save_path = os.path.join(media_dir, str(fournisseur.id) + ".jpg")
				path = default_storage.save(save_path, file)
				fournisseur.image = media_url + fournisseur_img_dir + str(fournisseur.id) + ".jpg"
				fournisseur.save()

			return HttpResponseRedirect(reverse('module_achat_details_fournisseur', args=(id,)))
		else:
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la modification des informations du fournisseur")
			return HttpResponseRedirect(reverse('module_achat_update_fournisseur', args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS POST DU MODIFIER FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Modifier Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_fournisseurs'))

def get_details_fournisseur(request, ref):
	try:
		permission_number = 4
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
			"modules" : modules,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 3
		}
		template = loader.get_template("ErpProject/ModuleAchat/fournisseur/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS POST DU DETAIL FOURNISSEURS\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Detail Fournisseur')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_fournisseurs'))

## DataTables Server Side

class CategorieViewSet(viewsets.ModelViewSet):
	queryset = Model_Categorie.objects.filter(type = 'ARTICLE').order_by('designation')
	serializer_class = CategorieArticleSerializer

class UniteViewSet(viewsets.ModelViewSet):
	queryset = Model_Unite.objects.all().order_by('designation')
	serializer_class = UniteSerializer

class CategorieUniteViewSet(viewsets.ModelViewSet):
	queryset = Model_Categorie.objects.filter(type = 'UNITE').order_by('designation')
	serializer_class = CategorieArticleSerializer

class BonReceptionViewSet(viewsets.ModelViewSet):
	queryset = Model_Bon_reception.objects.all().order_by('numero_reception')
	serializer_class = BonReceptionSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
	queryset = Model_Fournisseur.objects.all().order_by("nom_complet")
	serializer_class = FournisseurSerializer

class DemandeAchatViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Demande_achat.objects.all()
	serializer_class = serializer.DemandeDAchatSerializer

class ConditionReglementViewSet(viewsets.ModelViewSet):
	queryset = models.Model_ConditionReglement.objects.all()
	serializer_class = serializer.ConditionReglementSerializer

# BUSINESS INTELLIGENCE CONTROLLERS

def get_generate_report(request):
	permission_number = 481
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response


	context = {
		'title' : 'Business intelligence',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	#Calling the wizard Report
	return None #get_wizard_report(request, context, module = "ModuleAchat")


def post_generate_report(request):
	permission_number = 481
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response


	context = {
		'title' : 'Business intelligence',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	#Calling the wizard Report
	return None #post_wizard_report(request, context, module = "ModuleAchat")




def get_demande_rapports(request):
	modules, utilisateur,response = auth.toGetAuth(request)

	if response != None:
		return response

	date_debut = request.POST["date_debut"]
	date_fin = request.POST["date_fin"]
	end = endpoint.reportingEndPoint()

	context = {
		'title' : 'Business intelligence',
		'endpoint' : end,
		'date_debut' : date_debut,
		'date_fin' : date_fin,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	template = loader.get_template('ErpProject/ModuleAchat/rapport/rapport_demande.html')
	return HttpResponse(template.render(context, request))


def get_reception_rapports(request):
	modules, utilisateur,response = auth.toGetAuth(request)

	if response != None:
		return response

	date_debut = request.POST["date_debut"]
	date_fin = request.POST["date_fin"]
	end = endpoint.reportingEndPoint()

	context = {
		'title' : 'Business intelligence',
		'endpoint' : end,
		'date_debut' : date_debut,
		'date_fin' : date_fin,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2,
		'degrade': 'module_achat'
	}
	template = loader.get_template('ErpProject/ModuleAchat/rapport/rapport_bon_reception.html')
	return HttpResponse(template.render(context, request))


####### Avis appel offre
'''
def get_lister_avis_appel_offre(request):

	try:
		permission_number = 157
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		model = dao_model.toListModel(dao_avis_appel_offre.toListAvis_appel_offre(), permission_number, groupe_permissions, identite.utilisateur(request))

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : "Liste des avis d'appel d'offre",
			'model' : model,
			'utilisateur' : utilisateur,
			'view' : view,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#'roles' : roles,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_ACHAT,
			'menu' : 1
		}
		template = loader.get_template('ErpProject/ModuleAchat/avis_appel_offre/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleAchat'
		monLog.error("{} :: {}::\nERREUR LORS DE LA LISTE AViS FOURNISSEUR\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Liste Avis Appel offre')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_tableau_de_bord'))

def get_creer_avis_appel_offre(request):
	permission_number = 156
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	etat_actuel_id = 0
	etape_wkf_id = 0
	demande_wkf_id = 0
	etat = ""
	try:
		etat_actuel_id = request.POST["doc_id"]
		etat = dao_demande_achat.toGetDemande(etat_actuel_id)
		etape_wkf_id = request.POST["etape_id"]
		demande_wkf_id = request.POST["doc_id"]
	except Exception as e:
		#print("Aucune demande d'achat trouvée")
		pass

	demandes = dao_demande_achat.toListDemandesPourAvisAppelOffre()

	context ={'title' : "Ajouter un avis d'appel d'offre",
				'etat_actuel_id' : int(etat_actuel_id),
				'etape_wkf' : etape_wkf_id,
				'etat':etat,
				'demande_wkf' : demande_wkf_id,
				'demandes':demandes,
				'utilisateur' : utilisateur,
				'actions':auth.toGetActions(modules,utilisateur),
				'organisation': dao_organisation.toGetMainOrganisation(),
				'modules' : modules,'sous_modules': sous_modules,'module' : ErpModule.MODULE_ACHAT,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleAchat/avis_appel_offre/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_avis_appel_offre(request):

	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_signature"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		numero_reference = request.POST['numero_reference']
		numero_dossier = request.POST['numero_dossier']
		designation_commission = request.POST['designation_commission']
		objet_appel = request.POST['objet_appel']
		financement = request.POST['financement']
		type_appel_offre = request.POST['type_appel_offre']
		lieu_consultation = request.POST['lieu_consultation']
		qualification = request.POST['qualification']
		conditions = request.POST['conditions']
		date_signature = request.POST['date_signature']
		lieu_depot = request.POST['lieu_depot']
		date_depot = request.POST['date_depot']
		delai_engagement = request.POST['delai_engagement']
		montant_commission = request.POST['montant_commission']
		demande_id = request.POST["demande_id"]
		desc = request.POST['desc']



		auteur = identite.utilisateur(request)

		if (demande_id == "") or (demande_id == 0) :
			demande_id = None

		date_signature = date_signature[6:10] + '-' + date_signature[3:5] + '-' + date_signature[0:2]
		date_signature = datetime.datetime.strptime(date_signature, "%Y-%m-%d").date()

		date_depot = date_depot[6:10] + '-' + date_depot[3:5] + '-' + date_depot[0:2]
		date_depot = datetime.datetime.strptime(date_depot, "%Y-%m-%d").date()

		avis_appel_offre=dao_avis_appel_offre.toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,objet_appel,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc,demande_id)
		avis_appel_offre=dao_avis_appel_offre.toSaveAvis_appel_offre(auteur, avis_appel_offre)


		#Initialisation du workflow avis appel offre
		wkf_task.initializeWorkflow(auteur,avis_appel_offre)

		etat_actuel_id = int(request.POST["etat_actuel_id"])

		if etat_actuel_id != 0:
			etape_id = request.POST["etape_wkf"]
			demande_id = request.POST["demande_wkf"]
			utilisateur_id = request.user.id

			employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
			demande_achat = dao_demande_achat.toGetDemande(demande_id)

			wkf_task.passingStepWorkflow(employe,demande_achat,etape_id)
		else:
			if demande_id != None:
				employe = dao_employe.toGetEmployeFromUser(request.user.id)
				demande_achat = dao_demande_achat.toGetDemande(demande_id)
				wkf_task.passingStepWorkflow(auteur,demande_achat)

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		# return HttpResponseRedirect(reverse('module_achat_list_avis_appel_offre'))
		return HttpResponseRedirect(reverse("module_achat_detail_avis_appel_offre", args=(avis_appel_offre.id,)))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER AVIS_APPEL_OFFRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_add_avis_appel_offre'))


def get_details_avis_appel_offre(request,ref):
	try:
		permission_number = 157
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref=int(ref)
		avis_appel_offre=dao_avis_appel_offre.toGetAvis_appel_offre(ref)
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,avis_appel_offre)

		template = loader.get_template('ErpProject/ModuleAchat/avis_appel_offre/item.html')
		context ={
					'title' : "Détails sur l'appel d'offre N° " + avis_appel_offre.numero_reference,
					'model' : avis_appel_offre,
					'utilisateur' : utilisateur,
					'actions':auth.toGetActions(modules,utilisateur),
					'organisation': dao_organisation.toGetMainOrganisation(),
					'modules' : modules,
					'sous_modules': sous_modules,
					'module' : ErpModule.MODULE_ACHAT,
					'historique' : historique,
					'roles':groupe_permissions,
					'etapes_suivantes' : transition_etape_suivant,
					'signee' : signee,
					'content_type_id':content_type_id,
					'documents':documents,
					'organisation':dao_organisation.toGetMainOrganisation(),
					'menu' : 4
					}


		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS AVIS_APPEL_OFFRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_achat_list_avis_appel_offre'))

def get_modifier_avis_appel_offre(request,ref):
	permission_number = 158
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "Modifier un avis d'appel d'offre",
		'model':model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleAchat/avis_appel_offre/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_avis_appel_offre(request):

	id = int(request.POST['ref'])
	try:
		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		if not auth.toPostValidityDate(var_module_id, request.POST["date_signature"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		numero_reference = request.POST['numero_reference']
		numero_dossier = request.POST['numero_dossier']
		designation_commission = request.POST['designation_commission']
		objet_appel = request.POST['objet_appel']
		financement = request.POST['financement']
		type_appel_offre = request.POST['type_appel_offre']
		lieu_consultation = request.POST['lieu_consultation']
		qualification = request.POST['qualification']
		conditions = request.POST['conditions']
		date_signature = request.POST['date_signature']
		lieu_depot = request.POST['lieu_depot']
		date_depot = request.POST['date_depot']
		delai_engagement = request.POST['delai_engagement']
		montant_commission = request.POST['montant_commission']
		desc = request.POST['desc']
		auteur = identite.utilisateur(request)

		date_signature = date_signature[6:10] + '-' + date_signature[3:5] + '-' + date_signature[0:2]
		date_signature = datetime.datetime.strptime(date_signature, "%Y-%m-%d").date()

		date_depot = date_depot[6:10] + '-' + date_depot[3:5] + '-' + date_depot[0:2]
		date_depot = datetime.datetime.strptime(date_depot, "%Y-%m-%d").date()

		avis_appel_offre=dao_avis_appel_offre.toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,objet_appel,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc)
		avis_appel_offre=dao_avis_appel_offre.toUpdateAvis_appel_offre(id, avis_appel_offre)
		return HttpResponseRedirect(reverse('module_achat_list_avis_appel_offre'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER AVIS_APPEL_OFFRE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_achat_add_avis_appel_offre'))

'''
def get_modelprint(request):
	permission_number = 158
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_avis_appel_offre.toGetAvis_appel_offre(ref)
	context = {
		'title' : "Modèle du PV de réception",
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_ACHAT,
		'menu' : 2
	}
	return weasy_print("ErpProject/ModuleAchat/reporting/lettrecomande.html", "commande.pdf", context)
	# return weasy_print("ErpProject/ModuleAchat/reporting/demande_cotation.html", "cotation.pdf", context) #COTATION
	# return weasy_print("ErpProject/ModuleAchat/reporting/model_pv.html", "modelepv.pdf", context)   #MODELE PV
	# return weasy_print("ErpProject/ModuleAchat/reporting/model_appel_offre.html", "appel_offre.pdf", context) #AVIS D'APPEL D'OFFRE



# EXTRATION ACHAT
def get_generer_analyse_achat(request):
	try:
		permission_number = 481
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		context = {
			'title' : 'Générer une analyse Achat',
			"devises" : dao_devise.toListDevisesActives(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_ACHAT,
			'menu' : 6
		}
		template = loader.get_template("ErpProject/ModuleAchat/rapport/generate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e, reverse("module_budget_tableau_de_bord"))


def post_traiter_analyse_achat(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_ACHAT):
	'''fonction de traitement de calcul pour extraction d'un diplôme'''
	#On recupère et format les inputs reçus
	date_debut = request.POST["date_debut"]
	date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))

	date_fin = request.POST["date_fin"]
	date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]), 23, 59, 59)
	# ExerciceB = int(request.POST["exercice_bgt"])
	typeExtraction = int(request.POST["type_extraction"])
	Combine = []
	LignesBudgetaire = []
	if typeExtraction == 1:
		Expression = models.Model_Expression.objects.filter(creation_date__range = [date_debut, date_fin]).order_by("-creation_date")
		model = Expression
		titre = 'Analyse Etat de Suivi Expression Besoin'
	elif typeExtraction == 2:
		Demande_Achat = models.Model_Demande_achat.objects.filter(creation_date__range = [date_debut, date_fin]).order_by("-creation_date")
		model = Demande_Achat
		titre = 'Analyse Etat de Suivi Demande d\'Achat'
	elif typeExtraction == 3:
		bon_commande = models.Model_Bon_reception.objects.filter(creation_date__range = [date_debut, date_fin]).order_by("-creation_date")
		model = bon_commande
		titre = 'Analyse Etat de Suivi Bons de Commande'

	context = {
		'title' : titre,
		"model" : model,
		"date_debut" : request.POST["date_debut"],
		"date_fin" : request.POST["date_fin"],
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : enum_module,
		'format' : 'landscape',
		'menu' : 7,
		'typeExtraction': typeExtraction,
	}
	return context



def post_generer_analyse_achat(request):
	try:
		permission_number = 481
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_analyse_achat(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModuleAchat/rapport/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def post_imprimer_analyse_achat(request):
	try:
		permission_number = 481
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = post_traiter_analyse_achat(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModuleAchat/rapport/print_analyse_achat.html", "analyse_achat.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)
