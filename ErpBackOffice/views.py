# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cgitb import small
import imp
from django.contrib.contenttypes import fields

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
import datetime
import json
import os
from ErpBackOffice.dao.dao_query import dao_query
from ErpBackOffice.models import Model_Contrat, Model_Lettre_commande
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.print import render_to_pdf, my_exec, the_import_exec
from ErpBackOffice.dao.dao_print import *
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_place import dao_place
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice.utils.auth import auth
import importlib
import inspect
from django.db import transaction
from ErpBackOffice.utils.wkf_task import wkf_task
from ErpBackOffice.dao.dao_document import dao_document

from ErpBackOffice.dao.dao_session import dao_session
from ErpBackOffice.dao.dao_query_builder import dao_query_builder


from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_stakeholder import dao_wkf_stakeholder
from ErpBackOffice.utils.print import weasy_print
# from ErpBackOffice.utils.relancebc import traitement_duree_vie_bc
from ModuleRessourcesHumaines.dao.dao_dependant import dao_dependant
from ModuleRessourcesHumaines.dao.dao_rib import dao_rib



# Create your views here.

# Dashboard Controller
def get_index(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)
	if response != None:
		return response
	#Test Automatique Run
	# traitement_duree_vie_bc()

	context = {
		'title' : 'Accueil',
		"utilisateur" : utilisateur,
		"modules" : modules,
		'organisation': dao_organisation.toGetMainOrganisation()
	}
	template = loader.get_template("ErpProject/ErpBackOffice/dashboard.html")
	return HttpResponse(template.render(context, request))

# PROFILE UTILISATEUR PAGE
def get_profile(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)
	if response != None:
		return response

	employe = dao_employe.toGetEmploye(identite.utilisateur(request).id)
	dependants = dao_dependant.toListDependantByEmploye(identite.utilisateur(request).id)
	ribs = dao_rib.toListRibsOfEmploye(identite.utilisateur(request).id)
	#print(employe)

	context ={
		'title' : 'Profile utilisateur',
		'utilisateur' : utilisateur,
		'sous_modules': sous_modules,
		'utilisateur': utilisateur,
		'modules' : modules,
		'model' : employe,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'dependants':dependants,
		'ribs':ribs

	}
	template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/profile.html")
	return HttpResponse(template.render(context, request))

def get_password(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

	if response != None:
		return response

	context = {
		'title' : 'Modifier votre mot de passe',
		'sous_modules': sous_modules,
		'utilisateur': utilisateur,
		"modules" : modules,
		'organisation': dao_organisation.toGetMainOrganisation()
	}
	template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/password.html")
	return HttpResponse(template.render(context, request))

def post_password(request):
	try:
		pswd = request.POST["pswd"]
		n_pswd = request.POST["n_pswd"]

		employe = dao_employe.toGetEmploye(identite.utilisateur(request).id)
		user = employe.user

		if pswd != n_pswd:
			messages.error(request,'Les deux champs doivent être identiques')
			return HttpResponseRedirect(reverse("backoffice_change_password"))

		user.set_password(n_pswd)
		user.save()
		messages.success(request,"Mot de Passe changé avec succès")
		return HttpResponseRedirect(reverse("backoffice_connexion"))

	except Exception as e:
		#print("Erreur lors du changement de mot de passe")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("backoffice_deconnexion"))


def get_connexion(request):

	try:
		accueil = request.POST["accueil"]
		#print("loula")

		if accueil != "OK":
			return HttpResponseRedirect(reverse("backoffice_acceuil"))


		context = {
			'title' : 'Identifiez-vous au système !',
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/login.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		#print("Erreur !")
		#print(e)
		return HttpResponseRedirect(reverse("backoffice_acceuil"))
		#print("Erreur !")
		#print(e)

def get_accueil(request):
	context = {
		'title' : "Bienvenue à L'ARPCE",
		'organisation': dao_organisation.toGetMainOrganisation()
	}
	template = loader.get_template("ErpProject/ErpBackOffice/utilisateur/home.html")
	return HttpResponse(template.render(context, request))


def post_connexion(request):
	try:
		password = request.POST["password"]
		username = request.POST["email"].lower().strip()
		#print("ICI")

		utilisateur = authenticate(request, password = password, username = username)
		if(utilisateur is not None):
			login(request, utilisateur)
			# dao_session.processingUniqueSession(request)

			return HttpResponseRedirect(reverse("backoffice_index"))
		else:
			#print("haha")
			messages.add_message(request, messages.ERROR, "Nous ne reconnaissons pas ces identifiants !")
			return HttpResponseRedirect(reverse("backoffice_connexion"))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentive de connexion")
		return HttpResponseRedirect(reverse("backoffice_connexion"))

def get_deconnexion(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse("backoffice_connexion"))

	logout(request)
	return HttpResponseRedirect(reverse("backoffice_connexion"))

def get_not_autorize(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

	if response != None:
		return response

	context = {
		'title' : "Faute d'autorisation",
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules,
	}
	template = loader.get_template("ErpProject/ErpBackOffice/erreur/autorisation.html")
	return HttpResponse(template.render(context, request))

def get_not_role(request):

	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(0, request)

	if response != None:
		return response

	context = {
		'title' : "Aucun role attribué",
		'organisation': dao_organisation.toGetMainOrganisation(),
		"utilisateur" : identite.utilisateur(request),
		"modules" : modules,
	}
	template = loader.get_template("ErpProject/ErpBackOffice/erreur/role.html")
	return HttpResponse(template.render(context, request))


def get_json_list_places_filles(request):
	try:
		data = []
		parent_id = int(request.GET["ref"])
		places = dao_place.toListPlacesFilles(parent_id)
		for place in places:
			item = {
				"id" : place.id,
				"designation" : place.designation,
				"code_telephone" : place.code_telephone,
				"code_pays" : place.code_pays,
				"place_type" : place.place_type
			}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)


def get_model(texte):
	"""
	Cette méthode permet de retourner une class à partir d'un string

	1. 'importlib' lui permet de récuperer dynamiquement un module. Pour notre Exemple
	Il va récupérer le module 'models' contenu dans le package ErpBackOffice par sa méthode
	'import_module()'

	2. 'getattr' quant à lui, retourner la classe contenu dans le module précedemment récupérer
	via un string ici Texte

	3. 'inspect.isclass()' vérifier si l'objet récupérer au point 2 est bel et bien une classe.


	"""
	model = 'ErpBackOffice.models'
	module = importlib.import_module(model, ".")
	obj = getattr(module, texte)
	if inspect.isclass(obj):
		return obj

def backoffice_list_model(request):
	try:
		data = []
		mod = get_model(request.GET['model_choix']).objects.all()
		for model in mod:
			item = {
				'id' : model.id,
				'designation': model.__str__()
			}
			data.append(item)
		return JsonResponse(data, safe = False)
	except :
		return JsonResponse([], safe = False)

def backoffice_delete_doc(request, ref, modele, the_url):
	try:
		id = int(ref)

		#Supprime le fichier static dans son emplacement
		docu = dao_document.toGetDocument(id)
		#print('je recupere ref %s' % (id))
		#print('je recupere url %s' % (the_url))
		#print('je recupere les doc à sup %s' % (docu))

		mygetcwd = os.getcwd()
		img = mygetcwd+"/static"+docu.url_document
		img = img.replace('\\', '/')
		os.remove(img)

		num = int(docu.source_document_id)

		objet = get_model(modele).objects.get(id=num)
		doc = dao_document.toDeleteDocument(id)
		#print("confirmation de la sup doc %s" % (doc))
		if doc == True:
			return HttpResponseRedirect(reverse(the_url, args=(objet.id,)))
		return HttpResponseRedirect(reverse(the_url, args=(objet.id,)))
	except Exception as e:
		#print("proble au niveau du sup %s"%(e))
		pass



@transaction.atomic
def post_workflow(request):
	''' Traitement du postworkflow '''
	sid = transaction.savepoint()
	url_add = request.POST["url_add"]
	#print(url_add)
	url_detail = request.POST["url_detail"]
	#print(url_detail)
	try:
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		#print(etape_id)
		objet_id = request.POST["doc_id"]
		#print(objet_id)
		content_id = request.POST["content_id"]
		#print(content_id)



		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		#print("puritotita")

		historique = wkf_task.postworkflow(objet_id, content_id,employe,etape_id, url_detail, request)
		#print("mama")

		if historique != None :
			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))


	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_add))


@transaction.atomic
def post_cancel_workflow(request):
	''' Traitement pour passage à Annuler d'un workflow '''
	sid = transaction.savepoint()
	try:
		url_add = request.POST["url_add"]
		url_detail = request.POST["url_detail"]
		objet_id = request.POST["doc_id"]
		content_id = request.POST["content_id"]
		type_document = request.POST["type_doc"]
		notes = request.POST["notes"]
		action_id = int(request.POST["action_id"])

		if type_document == "":
			type_document = None

		employe = identite.utilisateur(request)
		type_document = None

		etape_id = None if action_id == 0 else action_id
		historique = wkf_task.cancelWorkflow(employe,objet_id,content_id, notes, type_document, etape_id)

		if historique != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_add))


@transaction.atomic
def post_stakeholder_delegation_workflow(request):
	''' Traitement pour Délégation '''
	sid = transaction.savepoint()
	try:
		delegue_transition_id = request.POST["delegue_transition_id"]
		url_detail = request.POST["url_detail"]
		objet_id = request.POST["doc_id"]
		content_id = request.POST["content_id"]
		module_source = request.POST["module_source"] #String du style ErpModule.MODULE_ACHAT
		module_source = module_source.split(".")[1] #On obtient que "MODULE_ACHAT"
		comments = request.POST["comments"]
		est_delegation = True
		employes = []
		carbon_copies = []
		if 'employe_id' in request.POST: employes.append(request.POST["employe_id"])

		auteur = identite.utilisateur(request)
		stakeholder  = wkf_task.postStakeHolder(delegue_transition_id, objet_id, content_id,employes, carbon_copies, est_delegation, comments, url_detail, module_source, auteur)

		if stakeholder != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))

	except Exception as e:
		# print("ERREUR on post_stakeholder_workflow")
		# print(e)
		messages.error(request,'Une erreur est survenue pendant le traitement')
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))


@transaction.atomic
def post_stakeholder_configuration_workflow(request):
	''' Traitement pour Configurer '''
	sid = transaction.savepoint()
	try:
		url_detail = request.POST["url_detail"]
		objet_id = request.POST["doc_id"]
		content_id = request.POST["content_id"]
		module_source = request.POST["module_source"] #String du style ErpModule.MODULE_ACHAT
		module_source = module_source.split(".")[1] #On obtient que "MODULE_ACHAT"
		comments = request.POST["comments"]
		est_delegation = False
		employes = request.POST.getlist('employe_id', None)
		carbon_copies = request.POST.getlist('cc_id', None)
		current_transition_id = request.POST["current_transition_id"]

		#We can have multiple next transition or just one
		transition = dao_wkf_transition.toGetTransition(current_transition_id)


		auteur = identite.utilisateur(request)

		for next_transition in transition.transitions_suivantes:
			stakeholder  = wkf_task.postStakeHolder(next_transition.id, objet_id, content_id,employes, carbon_copies, est_delegation, comments, url_detail, module_source, auteur)


		if stakeholder != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))

	except Exception as e:
		#print("ERREUR on post_stakeholder_configuration_workflow")
		#print(e)
		messages.error(request,'Une erreur est survenue pendant le traitement')
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse(url_detail, args=(objet_id,)))


def post_weasyprint_objet(request):
	try:
		modele = request.POST["modele"]
		ref = request.POST["ref"]
		title = request.POST["title"]
		objet_modele = get_model(modele).objects.get(id=int(ref))
		contrat = Model_Contrat.objects.get(pk = ref)
		context = {
			'title' : title,
			'model':objet_modele,
			'date_now': timezone.now(),
			'contrat' : contrat
		}
		return weasy_print("ErpProject/ErpbackOffice/reporting/objet_print.html", f"{title}.pdf", context)

	except Exception as e:
		#print(e)
		#Back to previous link http
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def post_weasyprint_appel_doffre(request):
	try:

		modele = request.POST["modele"]
		ref = request.POST["ref"]
		title = request.POST["title"]
		objet_modele = get_model(modele).objects.get(id=int(ref))
		avis = Model_Avis_appel_offre.objects.get(pk = ref)
		context = {
			'title' : title,
			'model':objet_modele,
			'date_now': timezone.now(),
			'avis' : avis
		}
		return weasy_print("ErpProject/ErpbackOffice/reporting/avis_appel_doffre.html", f"{title}.pdf", context)

	except Exception as e:
		#print(e)
		#Back to previous link http
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post_weasyprint_lettre_commande(request):
	try:

		modele = request.POST["modele"]
		ref = request.POST["ref"]
		title = request.POST["title"]
		objet_modele = get_model(modele).objects.get(id=int(ref))
		lettre = Model_Lettre_commande.objects.get(pk = ref)
		context = {
			'title' : title,
			'model':objet_modele,
			'date_now': timezone.now(),
			'lettre' : lettre
		}
		return weasy_print("ErpProject/ErpbackOffice/reporting/lettre_de_commande.html", f"{title}.pdf", context)

	except Exception as e:
		#print(e)
		#Back to previous link http
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def post_supprimmer_objet(request,ref, modele, the_url):
	try:
		#print('Model from form %s'%(modele))

		objet = get_model(modele).objects.get(id=int(ref))
		#print(objet)
		#print("on est la")
		objet.delete()
		#print('Suppression reussie')
		return HttpResponseRedirect(reverse(the_url))
	except Exception as e:
		#print(e)
		return HttpResponseRedirect(reverse(the_url))


def post_generate_pdf(request):
	previous = request.POST.get('previous', '/')
	try:
		#template = loader.get_template("ErpProject/ErpBackOffice/shared/print.html")
		id = request.POST["id"]
		dao = request.POST["dao"]
		#model = None
		#print("************************************************")
		id = request.POST["id"]
		dao = request.POST["dao"]
		model = my_exec(dao,id)
		context = {
			'model':model,
			'organisation':dao_organisation.toGetMainOrganisation(),
		}
		#html = template.render(context)
		pdf = render_to_pdf('ErpProject/ErpBackOffice/printable/print.html', context, request)
		return HttpResponse(pdf, content_type='application/pdf')
		#return HttpResponse(html)

	except Exception as e:
		#print("ERREUR")
		#print(e)
		return HttpResponseRedirect(previous)


def post_print_html_to_pdf(request):

	fonction = request.POST["fonction"]
	return the_import_exec(fonction,request)


def get_json_next_transition(request):
	try:
		data = []
		transition_id = int(request.GET["ref"])
		content_type_id = (request.GET["content_type_id"])
		objet_id = int(request.GET["objet_id"])

		transition = dao_wkf_transition.toGetTransition(transition_id)
		for unetransition in transition.transitions_suivantes:
			#print("unetransition", unetransition.id , content_type_id, objet_id)
			stakeholder = dao_wkf_stakeholder.toListTransitionOfObject(unetransition.id,content_type_id, objet_id).first()
			if stakeholder:
				list_employes = []
				for employe in stakeholder.employes.all():
					list_employes.append(employe.nom_complet)
					item = {
						"id" : unetransition.id,
						"etape_source" : unetransition.etape_source.designation,
						"etape_destination" : unetransition.etape_destination.designation,
						"groupe_permission": ','.join(list_employes)
					}
			else:
				item = {
					"id" : unetransition.id,
					"etape_source" : unetransition.etape_source.designation,
					"etape_destination" : unetransition.etape_destination.designation,
					"groupe_permission": unetransition.groupe_permission.designation
				}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		#print(e)
		return JsonResponse([], safe=False)



def get_wizard_report(request, context, module = None):

	context["models"] = dao_query_builder.toListContentTypes()
	#print(context)



	template = loader.get_template(f"ErpProject/{module}/rapport/generate.html")
	return HttpResponse(template.render(context, request))





def post_wizard_report(request, context, module = None):
	try:
		#return
		#print(request.POST)
		list_modele_id = request.POST.getlist('modele_id', None)
		list_select = request.POST.getlist('my-select', None)
		list_filter = request.POST.getlist('item', None)
		list_operator = request.POST.getlist('operateur', None)
		list_value = request.POST.getlist('valeur', None)
		#La liste logique (qui conserve les operateurs logiques OR, AND) a
		# une taille  = t-1 par rapport aux autres listes.
		list_logique = request.POST.getlist('logical', None)
		auteur = identite.utilisateur(request)
		#raise Exception

		title = request.POST["titre"]

		est_graphique = False
		if "est_graphique" in request.POST : est_graphique = True

		est_card = False
		if "est_card" in request.POST : est_card = True


		fonction = None
		measure = None
		dimension = None
		model_graphique = None

		if est_graphique:
			fonction = request.POST["fonction"]
			measure = request.POST["measure"]
			dimension = request.POST["dimension"]
			model_graphique = request.POST["model_graphique"]

		card_attribute = None
		card_function = None
		if est_card:
			card_attribute = request.POST["card_attribute"]
			card_function = request.POST["card_function"]


		#print(list_modele_id, list_select, list_filter, list_operator, list_value, )

		query, model_row, model_card, model_graphic = dao_query_builder.toPerformRawQuery(auteur, title, est_graphique, list_modele_id, \
			list_select, list_filter, list_operator, list_value, list_logique, model_graphique, fonction,\
			measure, dimension, est_card, card_function, card_attribute)

		#Find all detail about what to show directly from you model, its




		context["model"] = model_row
		context["headers"] = list_select #Or query.select.split(",")
		context["query"] = query
		context["module"] = module
		chart = {} #Dictionnaire having all charts
		legend_dataset = f'{fonction} {measure}'
		card = {}
		if est_card:
			card = {
				"title": query.title,
				"value": model_card[0][0]
			}
		chart["card"] = card

		#piechart (#ne nomnbre pas si les result est > à 10)
		piechart = None
		if model_graphic: #Test if model_graphic is not None, if is_chart was true on the user's request
			if len(model_graphic["categories"]) <= 10:
				piechart = []
				chart["piechart"] = piechart

			#barchart
			barchart = []
			chart["barchart"] = barchart

			#horizontalbar
			horizontalbar = []
			chart["horizontalbar"] = horizontalbar



		#Test DataTables

		# table = DataTable(small = True, hide_controls = True)
		# table.add_column('time')
		# table.add_column('pressure')
		# table.add_column('temperature')
		# table.add_column('test')
		# table.add_row(time=12, pressure=53, temperature=25, test = 54)
		# table.add_row(time=13, pressure=63, temperature=24, test = 54)
		# table.add_row(time=14, pressure=73, temperature=23, test = 54)
		# chart["table"] = table



		# #Test Piechart
		# piechart = PieChart(title="New Customers Through July", money=True, legend=True, width='500', color=True)
		# piechart.set_categories(["January", "February", "March", "April", "May", "June", "July"])
		# piechart.add_dataset([75, 44, 92, 11, 44, 95, 35], "Central")
		# piechart.add_dataset([41, 92, 18, 35, 73, 87, 92], "Eastside")
		# piechart.add_dataset([87, 21, 94, 13, 90, 13, 65], "Westside")
		# chart["piechart"] = piechart





		# #Test BarChart

		# barchart = BarChart(title="New Customers Through July", money=True, legend=True, width='500', color=True)
		# barchart.set_categories(["January", "February", "March", "April", "May", "June", "July"])
		# barchart.add_dataset([75, 44, 92, 11, 44, 95, 35], "Central")
		# barchart.add_dataset([41, 92, 18, 35, 73, 87, 92], "Eastside")
		# barchart.add_dataset([87, 21, 94, 13, 90, 13, 65], "Westside")
		# chart["barchart"] = barchart

		# context['chart'] = chart

		# #Test Horit

		# horizontalbar = HorizontalStackedBarChart(title="New Customers Through July", money=True, legend=True, width='500', color=True)
		# horizontalbar.set_categories(["January", "February", "March", "April", "May", "June", "July"])
		# horizontalbar.add_dataset([75, 44, 92, 11, 44, 95, 35], "Central")
		# horizontalbar.add_dataset([41, 92, 18, 35, 73, 87, 92], "Eastside")
		# horizontalbar.add_dataset([87, 21, 94, 13, 90, 13, 65], "Westside")
		# chart["horizontalbar"] = horizontalbar

		context['chart'] = chart

		#print(context)


		template = loader.get_template(f"ErpProject/{module}/rapport/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print("error***********", e)
		return None


def post_wizard_view_report(request):
	view = request.POST["view"]
	query_id = request.POST["query_id"]
	query = dao_query.toGetQuery(query_id)
	module = request.POST["module"]
	context = {
		"module" : module,
		"query": query
		}

	if view == "list":
		context["headers"] = query.select.split(",")


	template = loader.get_template(f"ErpProject/{module}/rapport/generated.html")
	return HttpResponse(template.render(context, request))




def get_json_fields_model(request):
	try:
		data = []
		ident = int(request.GET["ref"])
		data = dao_query_builder.toListFieldOfModel(ident)

		return JsonResponse(data, safe=False)

	except Exception as e:
		#print("error", e)
		return JsonResponse([], safe=False)


def get_json_related_models(request):
	try:
		data = []
		ident = int(request.GET["ref"])
		models_related = dao_query_builder.toListRelatedOfModel(ident)
		fields = dao_query_builder.toListFieldOfModel(ident)
		for model in models_related:
			item = {
                "id": model.id,
                "name": model.model
                }
			data.append(item)

		return JsonResponse(data, safe=False)

	except Exception as e:
		#print("error", e)
		return JsonResponse([], safe=False)
