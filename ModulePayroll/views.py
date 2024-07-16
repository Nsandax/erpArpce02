# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework import viewsets
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max,Sum
from datetime import time, timedelta, datetime
from django.core import serializers
from collections import namedtuple
from random import randint
import pandas as pd
import calendar
import numpy as np
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.dao.dao_place_type import dao_place_type
from ErpBackOffice.dao.dao_place import dao_place
from ModuleAchat.dao.dao_categorie import dao_categorie
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_document import dao_document
from ModuleRessourcesHumaines.dao.dao_banque import dao_banque
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_dependant import dao_dependant
from ModuleRessourcesHumaines.dao.dao_rib import dao_rib
from ErpBackOffice.dao.dao_devise import dao_devise
from ModulePayroll.dao.dao_pret import dao_pret
from ModulePayroll.dao.dao_ligne_paiement_pret import dao_ligne_paiement_pret
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModulePayroll.dao.dao_config_payroll import dao_config_payroll
from ErpBackOffice.utils.print import weasy_print, weasy_print_bulletin
#from ModulePayroll.dao.dao_departement import dao_departement
#from ModulePayroll.dao.dao_poste import dao_poste
#Pagination
from ErpBackOffice.utils.pagination import pagination
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ModulePayroll.dao.dao_categorie_element import dao_categorie_element
from ModulePayroll.dao.dao_structure_salariale import dao_structure_salariale
from ModulePayroll.dao.dao_type_structure import dao_type_structure
from ModulePayroll.dao.dao_categorie_regle import dao_categorie_regle
from ModulePayroll.dao.dao_rubrique import dao_rubrique
from ModulePayroll.dao.dao_constante import dao_constante
from ModulePayroll.dao.dao_bulletin_modele import dao_bulletin_modele

from ErpBackOffice.dao.dao_paiement_interne import dao_paiement_interne
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
from ModulePayroll.dao.dao_bareme import dao_bareme
from ModulePayroll.dao.dao_tranche_bareme import dao_tranche_bareme
from ModulePayroll.dao.dao_bulletin import dao_bulletin
from ModulePayroll.dao.dao_item_bulletin import dao_item_bulletin
from ModulePayroll.dao.dao_element_bulletin import dao_element_bulletin
from ModulePayroll.dao.dao_lot_bulletin import dao_lot_bulletin
from ModulePayroll.dao.dao_type_element_bulletin import dao_type_element_bulletin
from ModulePayroll.dao.dao_profil_paie import dao_profil_paie
from ModulePayroll.dao.dao_item_profil_paie import dao_item_profil_paie
from ModulePayroll.dao.dao_type_calcul import dao_type_calcul
from ModulePayroll.dao.dao_type_resultat import dao_type_resultat
from ModulePayroll.dao.dao_regle_salariale import dao_regle_salariale
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ErpBackOffice.dao.dao_model import dao_model
from ErpBackOffice.utils.function_constante import function_constante
from ModulePayroll.dao.dao_temp_ecriture_comptable import dao_temp_ecriture_comptable
from ModulePayroll.dao.dao_ligne_lot import dao_ligne_lot
from ModulePayroll.dao.dao_type_lot_bulletin import dao_type_lot_bulletin
from ModulePayroll.dao.dao_type_modele_bulletin import dao_type_modele_bulletin

from ErpBackOffice.dao.dao_wkf_historique_lotbulletin import dao_wkf_historique_lotbulletin
from ErpBackOffice.dao.dao_wkf_historique_bulletin import dao_wkf_historique_bulletin
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation
from ModulePayroll.dao.dao_dossier_paie import dao_dossier_paie
from ErpBackOffice.dao.dao_mois_annee import dao_mois_annee
from ModulePayroll.dao.dao_task import dao_task
from celery.result import AsyncResult
from ModuleComptabilite.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.models import *
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
import json
import array
import datetime
##############################""
FRAIS_PAR_DEPENDANT_ENFANTS =  100 #dao_organisation.toGetMainOrganisation().frais_dependant_enfant
FRAIS_PAR_DEPENDANT_FEMME   =  100 #dao_organisation.toGetMainOrganisation().frais_dependant_femme
INDEMNITE_TRANSPORT         =  1500 #dao_organisation.toGetMainOrganisation().indemnite_transp
INDEMNITE_LOGEMENT_ENFANT   =  50 #dao_organisation.toGetMainOrganisation().indemnite_log_enfant
INDEMNITE_LOGEMENT_FEMME    =  50 #dao_organisation.toGetMainOrganisation().indemnite_log_femme
INSS_QPO    =  3.5 #dao_organisation.toGetMainOrganisation().INSS_QPO
MONTANT_ANCIENNETE = 50
NOMBRE_AGENT = 43

##########""
#LOGGING
import logging, inspect
monLog = logging.getLogger("logger")
module= "ModulePayroll"
var_module_id = 19

#DASHBOARD
def get_dashboard(request):
	#droit = "LISTER"
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(19, request)
	if response != None:
		return response
	#WAY OF NOTIFCATION
	module_name = "MODULE_PAYROLL"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()
	#print("way")
	#print(temp_notif_count)
	#END WAY

	context = {
			"title" : "Module de gestion de paie",
			"utilisateur" : identite.utilisateur(request),
			"modules" : modules,
			'sous_modules': sous_modules,
			'actions': auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'temp_notif_count':temp_notif_count,
			'temp_notif_list':temp_notif_list,
			"module" : ErpModule.MODULE_PAYROLL,
			"menu" : 1
			}
	template = loader.get_template("ErpProject/ModulePayroll/index.html")
	return HttpResponse(template.render(context, request))


def calcul_paie(employe_id, lot_id = None, auteur_id = None):
	try:
		print( "Entre dans la fonction calcul_paie")
		employe = dao_employe.toGetEmploye(employe_id)
		print(employe.nom_complet)
		lot = dao_lot_bulletin.toGet(lot_id)
		if lot.type_modele == 1:
			modele_bulletin = dao_bulletin_modele.toGet(employe.modele_bulletin_id)
			if modele_bulletin == None: raise Exception("Modele bulletin non configure pour l employe")
		elif lot.type_modele == 2:
			modele_bulletin = lot.modele_bulletin
			if modele_bulletin == None: raise Exception("Modele bulletin non configure pour le lot")

		#On crée l'objet Bulletin
		designation = '{} - {}'.format(modele_bulletin.libelle_bulletin, employe.nom_complet)
		bulletin = dao_bulletin.toCreate(auteur_id, designation, employe.id, lot_id)
		bulletin = dao_bulletin.toSave(bulletin)

		# recuperation des elements de paie
		rubriques = modele_bulletin.rubriques.all()
		rubriques = sorted(rubriques, key=lambda rubrique: rubrique.sequence, reverse=False)
  
		rubriques_calcules = []
		for rubrique in rubriques:
			context = {'rubriques' : rubriques,'item_bulletins' : rubriques_calcules} 
			nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat = get_rubrique_value(rubrique, employe.id, context)
			item_bulletin = dao_item_bulletin.toCreate(auteur_id, rubrique.designation, rubrique.id, bulletin.id, nombre_parsal, base_parsal, taux_parsal, montant_parsal, rubrique.sequence, taux_parpat, montant_parpat)
			rubriques_calcules.append(item_bulletin)
			item_bulletin = dao_item_bulletin.toSave(item_bulletin)
			#print ("Item bulletin: %i" % item_bulletin.id)

			#Rubrique Remboursement pret : Test pour enregistrement de la ligne de paiement
			rubrique_remboursement_pret = dao_rubrique.toGetRubriqueRemboursementPret()
			if rubrique == rubrique_remboursement_pret:
				dao_pret.toComputeMontantARembourser(employe_id)


		# On affecte le cumul dans les bulletins
		np_const = dao_constante.toGetByCode("NETPAIE")
		ni_const = dao_constante.toGetByCode("NETIMPO")
		#bulletin.net_a_payer = get_constante_value(np_const, employe.id, rubriques)
		#bulletin.net_imposable = get_constante_value(ni_const, employe.id, rubriques)
		bulletin.save()
		#TODO Faire pareil pour les trois autres cumuls par défaut
		print ("Bulletin modifie avec cumul", bulletin)
		return bulletin
	except Exception as e:
		print("ERREUR calcul paie Function")
		print(e)
		return None

def recalcul_paie(bulletin_id, rubriques_updated = [], auteur_id = None):
	try:
		#print( "Entre dans la fonction recalcul_paie")
		bulletin = dao_bulletin.toGet(bulletin_id)
		employe = dao_employe.toGetEmploye(bulletin.employe_id)
		#print(employe.nom_complet)
		lot = dao_lot_bulletin.toGet(bulletin.lot_id)

		if lot.type_modele == 1:
			modele_bulletin = dao_bulletin_modele.toGet(employe.modele_bulletin_id)
			if modele_bulletin == None: raise Exception("Modele bulletin non configure pour l employe")
		elif lot.type_modele == 2:
			modele_bulletin = lot.modele_bulletin
			if modele_bulletin == None: raise Exception("Modele bulletin non configure pour le lot")

		# recuperation des elements de paie
		rubriques = modele_bulletin.rubriques.all()
		rubriques = sorted(rubriques, key=lambda rubrique: rubrique.sequence, reverse=False)
		for rubrique in rubriques:
			nombre_parsal = base_parsal = montant_parsal = taux_parsal = montant_parpat = taux_parpat = 0
			for item in rubriques_updated:
				if item["rubrique"] == rubrique.code and item["champs"] == "nombre":
					print ("nombre: {} modifie".format(item["valeur"]))
					nombre_parsal = item["valeur"]
				if item["rubrique"] == rubrique.code and item["champs"] == "base":
					print ("base: {} modifie".format(item["valeur"]))
					base_parsal = item["valeur"]
				if item["rubrique"] == rubrique.code and item["champs"] == "taux":
					print ("taux: {} modifie".format(item["valeur"]))
					taux_parsal = item["valeur"]
				if item["rubrique"] == rubrique.code and item["champs"] == "montant":
					print ("montant: {} modifie".format(item["valeur"]))
					montant_parsal = item["valeur"]
				if item["rubrique"] == rubrique.code and item["champs"] == "taux_parpat":
					print ("taux_parpat: {} modifie".format(item["valeur"]))
					taux_parpat = item["valeur"]
				if item["rubrique"] == rubrique.code and item["champs"] == "montant_parpat":
					print ("montant_parpat: {} modifie".format(item["valeur"]))
					montant_parpat = item["valeur"]
			nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat = get_rubrique_value(rubrique, employe.id, rubriques, nombre_parsal, base_parsal, montant_parsal, taux_parsal, montant_parpat, taux_parpat)

			object_dao_item_bulletin = dao_item_bulletin.toCreate(auteur_id, rubrique.designation, rubrique.id, bulletin.id, nombre_parsal, base_parsal, taux_parsal, montant_parsal, rubrique.sequence, taux_parpat, montant_parpat)
			item_bulletin = dao_item_bulletin.toGetItemOfRubrique(bulletin.id, rubrique.id)
			if item_bulletin == None:
				item_bulletin = dao_item_bulletin.toSave(object_dao_item_bulletin)
				print ("Item bulletin: %i cree" % item_bulletin.id)
			else:
				dao_item_bulletin.toUpdate(item_bulletin.id, object_dao_item_bulletin)
				print ("Item bulletin: %i modifie" % item_bulletin.id)


			#Rubrique Remboursement pret: Test pour enregistrement de la ligne de paiement
			rubrique_remboursement_pret = dao_rubrique.toGetRubriqueRemboursementPret()
			if rubrique == rubrique_remboursement_pret:
				dao_pret.toComputeMontantARembourser(employe.id)


		# On affecte le cumul dans les bulletins
		np_const = dao_constante.toGetByCode("NETPAIE")
		ni_const = dao_constante.toGetByCode("NETIMPO")
		bulletin.net_a_payer = get_constante_value(np_const, employe.id, rubriques)
		bulletin.net_imposable = get_constante_value(ni_const, employe.id, rubriques)
		bulletin.save()
		#TODO Faire pareil pour les trois autres cumuls par défaut
		print ("Bulletin modifie avec cumul")
		return bulletin
	except Exception as e:
		#print("ERREUR calcul paie")
		#print(e)
		return None

def get_constante_value(constante, employe_id = None, rubriques = []):
	try:
		if constante == None: return 0.0

		if constante.type_constant == 1:
			#print("traitement constante type calcul")
			valeur = 0.0
			for calcul in constante.parametres_calculs.all():
				# On récupère le code de calcul
				code = 0.0
				if calcul.code_is_const: code = get_constante_value(calcul.code_const, employe_id, rubriques)
				else: code = makeFloat(calcul.code)
				#On initialise avec le premier élèment
				if calcul.type_operation == 1:
					valeur = code
				elif calcul.type_operation == 2:
					valeur = makeFloat(valeur) + code
				elif calcul.type_operation == 3:
					valeur = makeFloat(valeur) - code
				elif calcul.type_operation == 4:
					valeur = makeFloat(valeur) * code
				elif calcul.type_operation == 5:
					valeur = makeFloat(valeur) / code
				elif calcul.type_operation == 6:
					valeur = makeFloat(valeur) % code
			#print("valeur Calcul {} cree".format(valeur))
			return valeur
		elif constante.type_constant == 2:
			#print("traitement constante type test")
			alors = 0.0
			if constante.alors_is_const: alors = get_constante_value(constante.alors_const, employe_id, rubriques)
			else: alors = makeFloat(constante.alors)
			sinon = 0.0
			if constante.sinon_is_const: sinon = get_constante_value(constante.sinon_const, employe_id, rubriques)
			else: sinon = makeFloat(constante.sinon)
			expression = ""
			valeur_returned = 0.0
			#print("recuperation des lignes")
			for test in constante.parametres_tests.all():
				# On récupère le code et la valeur du test
				code = 0.0
				if test.code_is_const: code = get_constante_value(test.code_const, employe_id, rubriques)
				else: code = makeFloat(test.code)
				valeur = 0.0
				if test.valeur_is_const: valeur = get_constante_value(test.valeur_const, employe_id, rubriques)
				else: valeur = makeFloat(test.valeur)
				#print("valeur recuperes")
				if test.type_condition == 1:
					expression = "{} {}{}{}".format(expression, code, test.value_type_operation, valeur)
				elif test.type_condition == 2:
					expression = "{} or {}{}{}".format(expression, code, test.value_type_operation, valeur)
				elif test.type_condition == 3:
					expression = "{} and {}{}{}".format(expression, code, test.value_type_operation, valeur)
				elif test.type_condition == 4:
					expression = "{} and not {}{}{}".format(expression, code, test.value_type_operation, valeur)
			#print("expression {}".format(expression))
			if eval(expression) : valeur_returned = alors
			else: valeur_returned = sinon
			#print("valeur Test {} cree".format(valeur_returned))
			return valeur_returned
		elif constante.type_constant == 3:
			#print("traitement constante type tranche")
			base_test = 0.0
			if constante.base_test_is_const: base_test = get_constante_value(constante.base_test_const, employe_id, rubriques)
			else: base_test = makeFloat(constante.base_test)
			valeur_returned = 0.0
			expression = ""
			for tranche in constante.parametres_tranches.all():
				# On récupère la tranche_debut, la tranche_fin et la valeur
				tranche_debut = 0.0
				if tranche.tranche_debut_is_const: tranche_debut = get_constante_value(tranche.tranche_debut_const, employe_id, rubriques)
				else: tranche_debut = makeFloat(tranche.tranche_debut)

				tranche_fin = 0.0
				if tranche.tranche_fin_is_const: tranche_fin = get_constante_value(tranche.tranche_fin_const, employe_id, rubriques)
				else: tranche_fin = makeFloat(tranche.tranche_fin)

				valeur = 0.0
				if tranche.valeur_is_const: valeur = get_constante_value(tranche.valeur_const, employe_id, rubriques)
				else: valeur = makeFloat(tranche.valeur)


				if tranche.type_operation_debut == None and tranche.tranche_debut == 0.0:
					#cas de la première tranche
					expression = "{}{}{}".format(base_test, tranche.value_type_operation_fin, tranche_fin)
					if eval(expression) :
						valeur_returned = valeur
						#print("valeur Tranche {}".format(valeur_returned))
						return valeur_returned
				elif tranche.type_operation_fin == None and tranche.tranche_fin == 0.0:
					#cas de la dernière tranche
					expression = "{}{}{}".format(tranche_debut, tranche.value_type_operation_debut, base_test)
					if eval(expression) :
						valeur_returned = valeur
						#print("valeur Tranche {}".format(valeur_returned))
						return valeur_returned
				else:
					#Pour les autres tranches
					expression = "{}{}{} and {}{}{}".format(tranche_debut, tranche.value_type_operation_debut, base_test, base_test, tranche.value_type_operation_fin, tranche_fin)
					if eval(expression) :
						valeur_returned = valeur
						#print("valeur Tranche {}".format(valeur_returned))
						return valeur_returned
		elif constante.type_constant == 4:
			#print("traitement constante type valeur")
			valeur = 0.0
			if constante.valeur_is_const: valeur = get_constante_value(constante.valeur_const, employe_id, rubriques)
			else: valeur = makeFloat(constante.valeur)
			#print("valeur Constante {}".format(valeur))
			return valeur
		elif constante.type_constant == 5:
			#print("traitement constante type rubrique")
			valeur = 0.0
			nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat = get_rubrique_value(constante.rubrique, employe_id, rubriques)
			valeur = makeFloat(montant_parsal)
			#print("valeur Constante Rubrique {}".format(valeur))
			return valeur
		elif constante.type_constant == 6:
			print("traitement constante type predefiniii")
			#print(rubriques["item_bulletins"])
			valeur = 0.0
			#Si c'est une constante prédefinie alors on a trois cas:
			#print("1er cas")
			# Le 1er cas: c'est une constante de catégorie configuration, sa valeur est insérée dans les paramètrages du Module Paie
			if makeFloat(constante.valeur) != 0 and constante.parametres_calculs.all().count() == 0:
				#print("2e cas")
				valeur = makeFloat(constante.valeur)

			# Le 2e cas: c'est une constance de catégorie cumul des rubriques
			elif constante.parametres_calculs.all().count() > 0:
				print("3e cas")
				for cumul in constante.parametres_calculs.all():
					if cumul.rubrique in rubriques["rubriques"]:
						print("rubrique {}".format(cumul.rubrique.reference))
						est_calcule = False
						montant_parsal = 0
						montant_parpat = 0
						for item in rubriques["item_bulletins"]:
							if item.rubrique_id == cumul.rubrique.id: 
								est_calcule = True
								montant_parsal = item.montant
								montant_parpat = item.montant_parpat
								print(f"est_calcule = True montant_parsal: {montant_parsal} montant_parpat: {montant_parpat}")
								break
						if est_calcule == False: 
							nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat = get_rubrique_value(cumul.rubrique, employe_id, rubriques)
						#On ajoute ou soustrait les montants des rubriques
						if constante.code in ("COTIPAT", "COUTOTPAT", "SOUS_PAT"):
							expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, montant_parpat)
							#print("expression {}".format(expression))
							valeur = eval(expression)
						else:
							expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, montant_parsal)
							#print("expression {}".format(expression))
							valeur = eval(expression)
			# Le 3e cas: la valeur de la constante est récupérée à partir d'une fonction prédéfinie
			elif constante.fonction != None and constante.fonction != "":
				valeur = eval("function_constante."+ str(constante.fonction) +"()")
				valeur = makeFloat(valeur)
			#print("valeur Constante predefinie {}".format(valeur))
			return valeur
		elif constante.type_constant == 7:
			#print("traitement constante type individuel")
			valeur = 0.0
			valeur = eval("function_constante."+ str(constante.fonction) +"("+str(employe_id)+")")
			valeur = makeFloat(valeur)
			#print("valeur Constante Individuelle {}".format(valeur))
			return valeur
		elif constante.type_constant == 8:
			#print("traitement constante type cumul")
			valeur = 0.0

			if constante.periode_cumul == 1:
				#Paie en cours
				valeur = 0.0
				for cumul in constante.parametres_calculs.all():
					# On récupère la valeur de la rubrique
					nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat = get_rubrique_value(cumul.rubrique, employe_id, rubriques)

					#On fait le cumul selon opération choisie
					expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, montant_parsal)
					#print("expression {}".format(expression))
					valeur = eval(expression)
				#print("valeur Cumul {} cree".format(valeur))
				return valeur
			elif constante.periode_cumul == 2:
				#Mensuelle
				valeur = 0.0
				annee_encours = int(datetime.datetime.now().strftime("%Y"))
				mois_encours = int(datetime.datetime.now().strftime("%m"))
				mois_anterieurs = Model_DossierPaie.objects.filter(annee__iexact = str(annee_encours), mois__lt = mois_encours).order_by("mois")
				for cumul in constante.parametres_calculs.all():
					for dossier in mois_anterieurs:
						bulletins = Model_Bulletin.objects.filter(employe_id = employe_id, lot__dossier_paie_id = dossier.id)
						for bulletin in bulletins:
							#Pour les autres constantes leurs valeurs doivent être affectées dans une rubrique
							item = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = cumul.rubrique_id).first()
							if item != None:
								code = makeFloat(item.montant)
								#On fait le cumul selon opération choisie
								expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
								#print("expression {}".format(expression))
								valeur = eval(expression)
					#On fait le cumul aussi avec le mois en cours selon opération choisie
					code = get_constante_value(cumul.code_const, employe_id, rubriques)
					expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
					#print("expression {}".format(expression))
					valeur = eval(expression)
				return valeur
			elif constante.periode_cumul == 3:
				#Trimestrielle
				valeur = 0.0
				annee_encours = int(datetime.datetime.now().strftime("%Y"))
				mois_encours = int(datetime.datetime.now().strftime("%m"))
				mois_anterieurs = Model_DossierPaie.objects.filter(annee__iexact = str(annee_encours), mois__lt = mois_encours).order_by("mois")
				for cumul in constante.parametres_calculs.all():
					for dossier in mois_anterieurs:
						bulletins = Model_Bulletin.objects.filter(employe_id = employe_id, lot__dossier_paie_id = dossier.id)
						for bulletin in bulletins:
							#Pour les autres constantes leurs valeurs doivent être affectées dans une rubrique
							item = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = cumul.rubrique_id).first()
							if item != None:
								code = makeFloat(item.montant)
								#On fait le cumul selon opération choisie
								expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
								#print("expression {}".format(expression))
								valeur = eval(expression)
					#On fait le cumul aussi avec le mois en cours selon opération choisie
					code = get_constante_value(cumul.code_const, employe_id, rubriques)
					expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
					#print("expression {}".format(expression))
					valeur = eval(expression)
				return valeur
			elif constante.periode_cumul == 4:
				#Annuelle
				valeur = 0.0
				annee_encours = int(datetime.datetime.now().strftime("%Y"))
				mois_encours = int(datetime.datetime.now().strftime("%m"))
				dossiers_anterieurs = Model_DossierPaie.objects.all().exclude(annee__iexact = str(annee_encours), mois = mois_encours).order_by("created_at")
				for cumul in constante.parametres_calculs.all():
					for dossier in dossiers_anterieurs:
						bulletins = Model_Bulletin.objects.filter(employe_id = employe_id, lot__dossier_paie_id = dossier.id)
						for bulletin in bulletins:
							#Pour les autres constantes leurs valeurs doivent être affectées dans une rubrique
							item = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = cumul.rubrique_id).first()
							if item != None:
								code = makeFloat(item.montant)
								#On fait le cumul selon opération choisie
								expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
								#print("expression {}".format(expression))
								valeur = eval(expression)
					#On fait le cumul aussi avec le mois en cours selon opération choisie
					code = get_constante_value(cumul.code_const, employe_id, rubriques)
					expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
					#print("expression {}".format(expression))
					valeur = eval(expression)
				return valeur
			elif constante.periode_cumul == 5:
				#De date à date
				valeur = 0.0
				date_debut_cumul = constante.date_debut_cumul
				date_debut_cumul = datetime.datetime.fromtimestamp(date_debut_cumul)
				date_fin_cumul = constante.date_fin_cumul
				date_fin_cumul = datetime.datetime.fromtimestamp(date_fin_cumul)
				annee_encours = int(datetime.datetime.now().strftime("%Y"))
				mois_encours = int(datetime.datetime.now().strftime("%m"))
				dossiers_anterieurs = Model_DossierPaie.objects.filter(date_dossier__range = [date_debut_cumul, date_fin_cumul]).exclude(annee__iexact = str(annee_encours), mois = mois_encours).order_by("created_at")
				for cumul in constante.parametres_calculs.all():
					for dossier in dossiers_anterieurs:
						bulletins = Model_Bulletin.objects.filter(employe_id = employe_id, lot__dossier_paie_id = dossier.id)
						for bulletin in bulletins:
							#Pour les autres constantes leurs valeurs doivent être affectées dans une rubrique
							item = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = cumul.rubrique_id).first()
							if item != None:
								code = makeFloat(item.montant)
								#On fait le cumul selon opération choisie
								expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
								#print("expression {}".format(expression))
								valeur = eval(expression)
					#On fait le cumul aussi avec le mois en cours selon opération choisie si le dossier est dans l'interval
					dossier_encours = Model_DossierPaie.objects.filter(date_dossier__range = [date_debut_cumul, date_fin_cumul], annee__iexact = str(annee_encours), mois = mois_encours).first()
					if dossier_encours != None:
						code = get_constante_value(cumul.code_const, employe_id, rubriques)
						expression = "{} {} {}".format(makeFloat(valeur), cumul.value_type_operation, code)
						#print("expression {}".format(expression))
						valeur = eval(expression)
				return valeur
		elif constante.type_constant == 9:
			#print("traitement constante type date")
			valeur = 0
			valeur = makeFloat(valeur.date_constante)
			#print("valeur Constante Date {}".format(valeur))
			return valeur
	except Exception as e:
		print("ERREUR get_constante_value")
		print(e)
		return 0.0

def get_rubrique_value(rubrique, employe_id = None, rubriques = [], nombre_parsal = 0, base_parsal = 0, montant_parsal = 0, taux_parsal = 0, montant_parpat = 0, taux_parpat = 0):
	try:
		#print("Debut get_rubrique_value")
		#print(rubrique)
		if rubrique == None: return nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat
		if rubrique.type_formule == 1:
			# Nombre x Base
			#Si la valeur est saisie à la main (Cas de récalcul), on considère cette valeur là
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			montant_parsal = makeFloat(nombre_parsal) * makeFloat(base_parsal)
		elif rubrique.type_formule == 2:
			# Nombre x Taux
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)
			montant_parsal = makeFloat(nombre_parsal) * ( makeFloat(taux_parsal) / 100 )

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) * ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 3:
			# Nombre x Base x Taux
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(nombre_parsal) * makeFloat(base_parsal) * (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) * makeFloat(base_parsal) * ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 4:
			# Base x Taux
			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(base_parsal) * (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(base_parsal) * ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 5:
			# Nombre / Base
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			montant_parsal = makeFloat(nombre_parsal) * makeFloat(base_parsal)
		elif rubrique.type_formule == 6:
			# Nombre / Taux
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(nombre_parsal) / (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) / ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 7:
			# Nombre / Base / Taux
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(nombre_parsal) / makeFloat(base_parsal) / (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) / makeFloat(base_parsal) / ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 8:
			# Base / Taux
			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(nombre_parsal) / (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) / ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 9:
			# Nombre / Base X Taux
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(nombre_parsal) / makeFloat(base_parsal) * (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) / makeFloat(base_parsal) * ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 10:
			# Nombre X Base / Taux
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = makeFloat(nombre_parsal) * makeFloat(base_parsal) / (makeFloat(taux_parsal) / 100)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = makeFloat(nombre_parsal) * makeFloat(base_parsal) / ( makeFloat(taux_parpat) / 100 )
		elif rubrique.type_formule == 11:
			# Taux / Base
			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = (makeFloat(taux_parsal) / 100) / makeFloat(base_parsal)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = ( makeFloat(taux_parpat) / 100 ) / makeFloat(base_parsal)
		elif rubrique.type_formule == 12:
			# Taux / Nombre
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = (makeFloat(taux_parsal) / 100) / makeFloat(nombre_parsal)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = ( makeFloat(taux_parpat) / 100 ) / makeFloat(nombre_parsal)
		elif rubrique.type_formule == 13:
			# Taux / Nombre / Base
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = (makeFloat(taux_parsal) / 100) / makeFloat(nombre_parsal) / makeFloat(base_parsal)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = ( makeFloat(taux_parpat) / 100 ) / makeFloat(nombre_parsal) / makeFloat(base_parsal)
		elif rubrique.type_formule == 14:
			# Taux / Nombre X Base
			if nombre_parsal == 0 :
				if rubrique.nombre_parsal_is_const: nombre_parsal = get_constante_value(rubrique.nombre_parsal_const, employe_id, rubriques)
				else: nombre_parsal = makeFloat(rubrique.nombre_parsal)
			else: nombre_parsal = makeFloat(nombre_parsal)

			if base_parsal == 0 :
				if rubrique.base_parsal_is_const: base_parsal = get_constante_value(rubrique.base_parsal_const, employe_id, rubriques)
				else: base_parsal = makeFloat(rubrique.base_parsal)
			else: base_parsal = makeFloat(base_parsal)

			if taux_parsal == 0 :
				if rubrique.taux_parsal_is_const: taux_parsal = get_constante_value(rubrique.taux_parsal_const, employe_id, rubriques)
				else: taux_parsal = makeFloat(rubrique.taux_parsal)
			else: taux_parsal = makeFloat(taux_parsal)

			montant_parsal = (makeFloat(taux_parsal) / 100) / makeFloat(nombre_parsal) * makeFloat(base_parsal)

			if rubrique.type_rubrique == 2:
				if taux_parpat == 0 :
					if rubrique.taux_parpat_is_const: taux_parpat = get_constante_value(rubrique.taux_parpat_const, employe_id, rubriques)
					else: taux_parpat = makeFloat(rubrique.taux_parpat)
				else: taux_parpat = makeFloat(taux_parpat)

				montant_parpat = ( makeFloat(taux_parpat) / 100 ) / makeFloat(nombre_parsal) * makeFloat(base_parsal)
		elif rubrique.type_formule == 15:
			# Montant fixe
			if montant_parsal == 0 :
				if rubrique.montant_parsal_is_const: montant_parsal = get_constante_value(rubrique.montant_parsal_const, employe_id, rubriques)
				else: montant_parsal = makeFloat(rubrique.montant_parsal)
			else: montant_parsal = makeFloat(montant_parsal)

			if rubrique.type_rubrique == 2:
				if montant_parpat == 0 :
					if rubrique.montant_parpat_is_const: montant_parpat = get_constante_value(rubrique.montant_parpat_const, employe_id, rubriques)
					else: montant_parpat = makeFloat(rubrique.montant_parpat)
				else: montant_parpat = makeFloat(montant_parpat)

		return nombre_parsal, base_parsal, taux_parsal, montant_parsal, taux_parpat, montant_parpat
	except Exception as e:
		#print("ERREUR get_rubrique_value")
		#print(e)
		return 0.0
###############################

# CALCUL PAIE CONTROLLER

# FONCTION DU CALCUL DE PAIE D'UN AGENT SPECIFIQUE AVEC ID PASSER EN PARAMETRE
@transaction.atomic
def get_calcul_paie_employe(request, ref):
	sid = transaction.savepoint()
	employe_id = int(ref)
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		dossier_paie = dao_dossier_paie.toGetActiveDossierPaie()
		if dossier_paie == None: raise Exception("Aucun dossier de paie n'est actif en ce moment, svp configurez d'abord un nouveau dossier de paie")
		lot_bulletin = dao_lot_bulletin.toGetLotRegulierFromDossierPaie(dossier_paie.id)
		if lot_bulletin == None: raise Exception("Le dossier actif ne contient pas de lot régulier, svp configurez d'abord le dossier de paie actif")
		old_bulletin = dao_bulletin.toGetOfEmployeFromLot(employe_id, lot_bulletin.id)
		if old_bulletin != None : old_bulletin.delete()
		bulletin = calcul_paie(employe_id, lot_bulletin.id, utilisateur.id)
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_bulletin',args=(bulletin.id,)))
	except Exception as e:
		#print("ERREUR DETAIL")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_payroll_detail_employe',args=(employe_id,)))


# FONCTION DU CALCUL DE PAIE DES AGENTS AVEC ID DU DOSSIER PAIE PASSER EN PARAMETRE
@transaction.atomic
def get_calcul_paie_dossier(request, ref):
	sid = transaction.savepoint()
	try:
		# droit="LISTER_EMPLOYE" # 'CALCUL_PAIE' Rôle à configuré
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		#On recupère le dossier de paie
		dossier_id = int(ref)
		dossier = dao_lot_bulletin.toGet(dossier_id)
		#print("Dossier recupere {}".format(dossier.designation))

		#On recupère les employes du dossier
		employes = dao_employe.toListEmployesActifs()
		if dossier.type == "Tous": employes = dao_employe.toListEmployesActifs()
		elif dossier.type == "Par departement": employes = dao_employe.toListEmployesOfDepartement(dossier.departement.id)
		#print("Employe(s) recupere(s) {}".format(employes))

		#On calcul la paye pour chaque employé du dossier dans cette boucle
		for employe in employes:
			#print("Employe {}".format(employe.nom_complet))
			bulletin = calcul_paie(employe.id, dossier.id, utilisateur.id)

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(dossier.id,)))
	except Exception as e:
		#print("ERREUR DETAIL")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du bulletin!")
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_payroll_list_salarie'))


# FONCTION QUI RE-CALCUL LE BULLETIN PAIE D'UN AGENT SPECIFIQUE AVEC ID DU BULLETINPASSER EN PARAMETRE
@transaction.atomic
def get_recalcul_paie_bulletin(request, ref):
	sid = transaction.savepoint()
	bulletin_id = int(ref)
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		rubriques_updated = []

		list_input_valeur = request.POST.getlist("input_valeur", None)
		list_input_champs = request.POST.getlist("input_champs", None)
		list_input_rubrique = request.POST.getlist("input_rubrique", None)

		for i in range(0, len(list_input_rubrique)) :
			ligne = {
				'rubrique': list_input_rubrique[i],
				'champs': list_input_champs[i],
				'valeur': list_input_valeur[i]
			}
			rubriques_updated.append(ligne)

		bulletin = recalcul_paie(bulletin_id, rubriques_updated, utilisateur.id)
		if bulletin == None: raise Exception("Une erreur est survenue pendant le calcule du bulletin")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_bulletin',args=(bulletin.id,)))
	except Exception as e:
		#print("ERREUR DETAIL")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_bulletin',args=(bulletin_id,)))


# FONCTION DE LA LISTE D'EMPLOYES POUR LE CALCUL DE PAIE
def get_list_salarie(request):
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","kanban"))
		except Exception as e:
			view = "kanban"
		model = pagination.toGet(request, model)

		context = {
			'title' : 'Liste des salariés',
			'model' : model,
			'view' : view,
			#'can_create' : dao_droit.toGetDroitRole('CREER_EMPLOYE',nom_role,utilisateur.nom_complet),
			'menu' : 12,
			'modules' : modules,
			'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/employe/list.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_details_salarie(request,ref):
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		employe = dao_employe.toGetEmploye(ref)
		documents = dao_document.toListDocumentbyObjetModele(employe)
		dependants = dao_dependant.toListDependantByEmploye(employe.id)
		ribs = dao_rib.toListRibsOfEmploye(employe.id)

		context = {
			'title' : 'Détails d\'un salarié',
			'model' : employe,
			'dependants':dependants,
			'documents': documents,
			'ribs': ribs,
			'menu' : 12,
			'modules' : modules,
			'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/employe/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur detailer Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_salarie'))


#LOT BULLETIN CONTROLLER
def get_lister_lotbulletin(request):
	try:
		# droit="LISTER_LOT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 180
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_lot_bulletin.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_lot_bulletin.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Lots de bulletins de paie',
			'model' : model,
			'view':view,
			'menu' : 8,
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/lotbulletin/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER LOTS BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Lots Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_lotbulletin(request):
	try:
		# droit="CREER_LOT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 181
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		types_lot_bulletins = dao_type_lot_bulletin.toListTypesLotBulletins()
		types_modeles_bulletins = dao_type_modele_bulletin.toList()
		modele_bulletins = dao_bulletin_modele.toList()
		rubriques = dao_rubrique.toList()
		context = {
			'title' : 'Nouveau Lot de bulletins',
			'menu' : 8,
			'isPopup' : isPopup,
			'departements' : departements,
			'types_lot_bulletins': types_lot_bulletins,
			'types_modeles_bulletins': types_modeles_bulletins,
			'modele_bulletins' : modele_bulletins,
			'rubriques' : rubriques,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/lotbulletin/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER LOTS BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Lots Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_lotbulletin"))


@transaction.atomic
def post_creer_lotbulletin(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		departement_id = int(request.POST["departement_id"])
		if departement_id == 0: departement_id = None
		reference = request.POST["reference"]
		type = request.POST["type_dossier"]
		date_debut = request.POST["date_debut"]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		date_dossier = date_fin
		type_modele = request.POST["type_modele"]
		modele_bulletin_id = int(request.POST["modele_bulletin_id"])
		if modele_bulletin_id == 0: modele_bulletin_id = None

		dossier_paie_actif = dao_dossier_paie.toGetActiveDossierPaie()
		if not dossier_paie_actif:
			messages.add_message(request, messages.ERROR, "Aucune période paie active définie")
			return HttpResponseRedirect(reverse('module_payroll_add_lotbulletin'))

		lotbulletin = dao_lot_bulletin.toCreate(auteur.id, designation, departement_id, type, reference, date_dossier, dossier_paie_id = dossier_paie_actif.id)
		lotbulletin = dao_lot_bulletin.toSave(lotbulletin)
		lotbulletin.date_debut = date_debut
		lotbulletin.date_fin = date_fin
		lotbulletin.modele_bulletin_id = modele_bulletin_id
		lotbulletin.type_modele = type_modele
		lotbulletin.save()
		#print("Dossier cree ID %s" % lotbulletin.id)
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lotbulletin.id,)))
	except Exception as e:
		#print("ERREUR ! POST")
		transaction.savepoint_rollback(sid)
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du lot de bulletins!")
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_lotbulletin'))

def get_details_lotbulletin(request, ref):
	# droit="LISTER_LOT_BULLETIN"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	permission_number = 180
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	try:
		ref = int(ref)
		lotbulletin = dao_lot_bulletin.toGet(ref)
		mois = dao_lot_bulletin.toGetMois(ref)
		#documents = dao_document.toListDocumentbyDossierPaie(lotbulletin.id)
		bulletins = dao_bulletin.toListOfDossier(lotbulletin.id)

		#Si le lot est de type Tous ou certains, on  renvoit la liste de tous les employés
		if lotbulletin.type == "TOUS" or lotbulletin.type == "CERTAINS":
			employes = dao_employe.toListEmployesActifs()
		else:
			if lotbulletin.departement:
				employes = dao_employe.toListEmployesOfDepartement(lotbulletin.departement_id)

		#Si le lot est de type "departement"

		structures = dao_structure_salariale.toList()
		total = 0

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,lotbulletin)

		context = {
			'title' : lotbulletin.designation,
			'model' : lotbulletin,
			'mois' : mois,
			'bulletins' : bulletins,
			'employes' : employes,
			'structures' : structures,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'total' : total,
			'menu' : 8,
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/lotbulletin/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR DETAIL")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_lotbulletin'))


def post_generer_lot_bulletin(request, ref):
	try:
		permission_number = 541
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		bulletins = dao_bulletin.toListOfDossier(ref)

		context = {
			'title' : 'BULLETIN DE SALAIRE',
			'bulletins' : bulletins,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			"utilisateur" : utilisateur,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
		}
		#template = loader.get_template("ErpProject/ModulePayroll/lotbulletin/generated.html")
		#return HttpResponse(template.render(context, request))
		return weasy_print("ErpProject/ModulePayroll/lotbulletin/generated.html", "lot_bulletin.pdf", context)
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bulletin'))


#BULLETIN CONTROLLER
def get_lister_bulletin(request):
	try:
		# droit="LISTER_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 185
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_bulletin.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_bulletin.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des Bulletins de paie',
			'model' : model,
			'view':view,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'menu' : 7,
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/bulletin/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_lotbulletin(request):
	try:
		# droit="CREER_LOT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 181
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		types_lot_bulletins = dao_type_lot_bulletin.toListTypesLotBulletins()
		types_modeles_bulletins = dao_type_modele_bulletin.toList()
		modele_bulletins = dao_bulletin_modele.toList()
		rubriques = dao_rubrique.toList()
		context = {
			'title' : 'Nouveau Lot de bulletins',
			'menu' : 8,
			'isPopup' : isPopup,
			'departements' : departements,
			'types_lot_bulletins': types_lot_bulletins,
			'types_modeles_bulletins': types_modeles_bulletins,
			'modele_bulletins' : modele_bulletins,
			'rubriques' : rubriques,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/lotbulletin/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER LOTS BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Lots Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_lotbulletin"))

@transaction.atomic
def post_creer_lotbulletin(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		departement_id = int(request.POST["departement_id"])
		if departement_id == 0: departement_id = None
		reference = request.POST["reference"]
		type = request.POST["type_dossier"]
		date_debut = request.POST["date_debut"]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		date_dossier = date_debut
		type_modele = request.POST["type_modele"]
		modele_bulletin_id = int(request.POST["modele_bulletin_id"])
		if modele_bulletin_id == 0: modele_bulletin_id = None
		modele_personnalisee = False
		if "modele_personnalisee" in request.POST : modele_personnalisee = True


		dossier_paie_actif = dao_dossier_paie.toGetActiveDossierPaie()
		#print("dossier_paie_actif {}".format(dossier_paie_actif))
		if not dossier_paie_actif:
			messages.add_message(request, messages.ERROR, "Aucune période paie active définie")
			return HttpResponseRedirect(reverse('module_payroll_add_lotbulletin'))

		date_debut_periode = timezone.datetime(int(dossier_paie_actif.annee), int(dossier_paie_actif.mois), int("01"))
		last_day_periode = calendar.monthrange(int(dossier_paie_actif.annee), int(dossier_paie_actif.mois))[1]
		date_fin_periode = timezone.datetime(int(dossier_paie_actif.annee), int(dossier_paie_actif.mois), int(last_day_periode))

		if date_debut < date_debut_periode or date_fin > date_fin_periode:
			messages.add_message(request, messages.ERROR, "Les dates de début et de fin de ce lot ne correspondent pas à la période de paie en cours")
			return HttpResponseRedirect(reverse('module_payroll_add_lotbulletin'))

		lotbulletin = dao_lot_bulletin.toCreate(auteur.id, designation, departement_id, type, reference, date_dossier, dossier_paie_id = dossier_paie_actif.id)
		lotbulletin = dao_lot_bulletin.toSave(lotbulletin)
		#print("lotbulletin {}".format(lotbulletin))
		lotbulletin.date_debut = date_debut
		lotbulletin.date_fin = date_fin
		lotbulletin.type_modele = type_modele
		if modele_personnalisee :
			#print("modele_personnalisee {}".format(modele_personnalisee))
			modele_bulletin = dao_bulletin_modele.toCreate(auteur.id, designation = "Modèle de Bulletin personnalisé du Lot {}".format(designation), libelle_bulletin = "Bulletin de Paie")
			modele_bulletin = dao_bulletin_modele.toSave(modele_bulletin)
			#print("MODELE DE BULLETIN {} cree".format(modele_bulletin.id))
			list_rubriques = request.POST.getlist('multi_select_rubriques[]', None)
			#print("list_rubriques {}".format(list_rubriques))

			for i in range(0, len(list_rubriques)) :
				rubrique_id = int(list_rubriques[i])
				#print("Rubrique_id {}".format(rubrique_id))
				rubrique = Model_Rubrique.objects.filter(id = rubrique_id).first()
				#print("rubrique {}".format(rubrique))
				modele_bulletin.rubriques.add(rubrique)
			lotbulletin.modele_bulletin_id = modele_bulletin.id
		else: lotbulletin.modele_bulletin_id = modele_bulletin_id
		lotbulletin.save()
		#print("Dossier cree ID %s" % lotbulletin.id)
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lotbulletin.id,)))
	except Exception as e:
		print("ERREUR ! POST")
		transaction.savepoint_rollback(sid)
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du lot de bulletins!")
		return HttpResponseRedirect(reverse('module_payroll_add_lotbulletin'))

def get_modifier_lotbulletin(request, ref):
	ref = int(ref)
	try:
		# droit="CREER_LOT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 181
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		types_lot_bulletins = dao_type_lot_bulletin.toListTypesLotBulletins()
		types_modeles_bulletins = dao_type_modele_bulletin.toList()
		modele_bulletins = dao_bulletin_modele.toList()
		rubriques = dao_rubrique.toList()
		lotbulletin = dao_lot_bulletin.toGet(ref)
		context = {
			'title' : 'Modifier {}'.format(lotbulletin.designation),
			'model' : lotbulletin,
			'departements' : departements,
			'types_lot_bulletins': types_lot_bulletins,
			'types_modeles_bulletins': types_modeles_bulletins,
			'modele_bulletins' : modele_bulletins,
			'rubriques' : rubriques,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/lotbulletin/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER LOTS BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Lots Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(ref,)))

@transaction.atomic
def post_modifier_lotbulletin(request):
	sid = transaction.savepoint()
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		departement_id = int(request.POST["departement_id"])
		if departement_id == 0: departement_id = None
		reference = request.POST["reference"]
		type = request.POST["type_dossier"]
		date_debut = request.POST["date_debut"]
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST["date_fin"]
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		date_dossier = date_debut
		type_modele = request.POST["type_modele"]
		modele_bulletin_id = int(request.POST["modele_bulletin_id"])
		if modele_bulletin_id == 0: modele_bulletin_id = None
		modele_personnalisee = False
		if "modele_personnalisee" in request.POST : modele_personnalisee = True


		dossier_paie_actif = dao_dossier_paie.toGetActiveDossierPaie()
		if not dossier_paie_actif:
			messages.add_message(request, messages.ERROR, "Aucune période paie active définie")
			return HttpResponseRedirect(reverse('module_payroll_add_lotbulletin'))

		date_debut_periode = timezone.datetime(int(dossier_paie_actif.annee), int(dossier_paie_actif.mois), int("01"))
		last_day_periode = calendar.monthrange(int(dossier_paie_actif.annee), int(dossier_paie_actif.mois))[1]
		date_fin_periode = timezone.datetime(int(dossier_paie_actif.annee), int(dossier_paie_actif.mois), int(last_day_periode))

		if date_debut < date_debut_periode or date_fin > date_fin_periode:
			messages.add_message(request, messages.ERROR, "Les dates de début et de fin de ce lot ne correspondent pas à la période de paie en cours")
			return HttpResponseRedirect(reverse('module_payroll_update_lotbulletin',args=(ref,)))

		lotbulletin = dao_lot_bulletin.toCreate(auteur.id, designation, departement_id, type, reference, date_dossier, dossier_paie_id = dossier_paie_actif.id)
		updated, lotbulletin = dao_lot_bulletin.toUpdate(ref, lotbulletin)
		if updated == False: raise Exception("Erreur")
		lotbulletin.date_debut = date_debut
		lotbulletin.date_fin = date_fin
		lotbulletin.type_modele = type_modele
		if modele_personnalisee :
			modele_bulletin = dao_bulletin_modele.toCreate(auteur.id, designation = "Modèle de Bulletin personnalisé du Lot {}".format(designation), libelle_bulletin = "Bulletin de Paie")
			modele_bulletin = dao_bulletin_modele.toSave(modele_bulletin)
			#print("MODELE DE BULLETIN {} cree".format(modele_bulletin.id))
			list_rubriques = request.POST.getlist('multi_select_rubriques[]', None)

			for i in range(0, len(list_rubriques)) :
				rubrique_id = int(list_rubriques[i])
				rubrique = Model_Rubrique.objects.filter(id = rubrique_id).first()
				modele_bulletin.rubriques.add(rubrique)
			lotbulletin.modele_bulletin_id = modele_bulletin.id
		else: lotbulletin.modele_bulletin_id = modele_bulletin_id
		lotbulletin.save()
		#print("Dossier cree ID %s" % lotbulletin.id)
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lotbulletin.id,)))
	except Exception as e:
		#print("ERREUR ! POST")
		transaction.savepoint_rollback(sid)
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du lot de bulletins!")
		return HttpResponseRedirect(reverse('module_payroll_update_lotbulletin',args=(ref,)))

@transaction.atomic
def post_generer_bulletin(request):
	sid = transaction.savepoint()
	lot_id = int(request.POST["lot_id"])
	try:
		auteur = identite.utilisateur(request)
		structure_id = int(request.POST["structure_id"])
		structure = dao_structure_salariale.toGet(structure_id)
		#print(structure)
		#print("ICII")
		if structure == None:
			#print("STUCTURE NONE")
			raise Exception("Sélectionner la structure salariale SVP!")

		#print("PASSER 1")
		list_employe_id = request.POST.getlist('employe_id', None)
		#print(len(list_employe_id))
		for i in range(0, len(list_employe_id)) :
			employe_id = int(list_employe_id[i])
			employe = dao_employe.toGetEmploye(employe_id)
			#print("PASSER 2")
			if employe.type_structure != None and employe.type_structure.id == structure.type.id:
				#print("PASSER 3")
				lot_bulletin = dao_lot_bulletin.toGet(lot_id)

				designation = "Bulletin de paie {}".format(employe.nom_complet)
				reference = ""
				periode = ""
				type = ""

				bulletin = dao_bulletin.toCreate(auteur.id, designation, employe_id, lot_id, reference, periode, type)
				bulletin = dao_bulletin.toSave(bulletin)
				#print("Bulletin cree ID {}".format(bulletin.id))

				#itemstructures = Model_ItemStructureSalariale.objects.filter(structure_id = structure.id)
				regles = structure.regles.all()

				for item in regles :
					#print("PASSER 4")
					regle_id = item.id
					montant = makeFloat("100")
					temps = makeFloat("1")
					taux = makeFloat("22")

					regle = dao_regle_salariale.toGet(regle_id)
					designation = "{}".format(regle.designation)

					item_bulletin = dao_item_bulletin.toCreate(auteur.id, designation, regle_id, bulletin.id, temps, taux, montant)
					item_bulletin = dao_item_bulletin.toSave(item_bulletin)
					#print("item_bulletin %i creee".format(item_bulletin))

		#print("PASSER 5")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lot_id,)))
	except Exception as e:
		#print("ERREUR POST BULLETIN")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lot_id,)))

@transaction.atomic
def post_generer_lignes_lot(request):
	sid = transaction.savepoint()
	lot_id = int(request.POST["lot_id"])
	try:
		lot = dao_lot_bulletin.toGet(lot_id)
		if lot.lignes:
			lot.lignes.all().delete()
		auteur = identite.utilisateur(request)
		list_employe_id = request.POST.getlist('employe_id', None)
		for i in range(0, len(list_employe_id)) :
			employe_id = int(list_employe_id[i])
			employe = dao_employe.toGetEmploye(employe_id)
			ligne_lot = dao_ligne_lot.toCreateLigneLot("", employe, employe.unite_fonctionnelle.id)
			ligne_lot = dao_ligne_lot.toSaveLigneLot(auteur, ligne_lot)
			lot.lignes.add(ligne_lot)


		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "Configurations réussies!")
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lot_id,)))
	except Exception as e:
		#print("ERREUR POST BULLETIN")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lot_id,)))


def get_details_bulletinold(request, ref):

	# droit="LISTER_BULLETIN"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

	permission_number = 185
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	try:
		ref = int(ref)
		bulletin = dao_bulletin.toGet(ref)
		item_bulletins = dao_item_bulletin.toGetItemOfBulletin(bulletin.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bulletin)
		#print("Nombre item bulletin {}".format(item_bulletins.count()))




		context = {
			'title' : bulletin.designation,
			'model' : bulletin,
			'item_bulletins' : item_bulletins,
			'menu' : 7,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/bulletin/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bulletin'))

#BULLETIN CONTROLLER
def get_lister_bulletin(request):
	try:
		# droit="LISTER_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 185
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_bulletin.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_bulletin.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des Bulletins de paie',
			'model' : model,
			'view':view,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'menu' : 7,
			'modules' : modules,'sous_modules': sous_modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModulePayroll/bulletin/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_bulletin(request):
	try:
		# droit="CREER_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 184
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else :
			isPopup = False

		employes = dao_employe.toListEmployes()
		lots = dao_lot_bulletin.toList()

		context = {
			'title' : 'Nouveau bulletin',
			'menu' : 7,
			'employes' : employes,
			'lots' : lots,
			'isPopup' : isPopup,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			'regles_salariales': dao_regle_salariale.toList(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/bulletin/add.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_bulletin"))


@transaction.atomic
def post_creer_bulletin(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		employe_id = int(request.POST["employe_id"])
		employe = dao_employe.toGetEmploye(employe_id)

		devise_id = int(request.POST["devise_id"])
		devise = dao_devise.toGetDevise(devise_id)

		lot_id = int(request.POST["lot_id"])
		lot_bulletin = dao_lot_bulletin.toGet(lot_id)

		designation = request.POST["designation"]
		reference = request.POST["reference"]
		periode = request.POST["periode"]
		type = ""

		bulletin = dao_bulletin.toCreate(auteur.id, designation, employe_id, lot_id, reference, periode, type)
		bulletin = dao_bulletin.toSave(bulletin)
		#print("Bulletin cree ID {}".format(bulletin.id))

		list_regle_id = request.POST.getlist('regle_id', None)
		list_montant = request.POST.getlist("montant", None)
		list_temps = request.POST.getlist("temps", None)
		list_taux = request.POST.getlist("taux", None)

		for i in range(0, len(list_regle_id)) :
			regle_id = int(list_regle_id[i])
			montant = makeFloat(list_montant[i])
			temps = makeFloat(list_temps[i])
			taux = makeFloat(list_taux[i])

			regle = dao_regle_salariale.toGet(regle_id)
			designation = "{}".format(regle.designation)

			item_bulletin = dao_item_bulletin.toCreate(auteur.id, designation, regle_id, bulletin.id, temps, taux, montant)
			item_bulletin = dao_item_bulletin.toSave(item_bulletin)
			#print("item_bulletin %i creee".format(item_bulletin))

			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse('module_payroll_details_bulletin',args=(bulletin.id,)))
	except Exception as e:
		#print("ERREUR ! POST BULLETIN")
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du bulletin!")
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_bulletin'))

@transaction.atomic
def post_generer_bulletin(request):
	sid = transaction.savepoint()
	lot_id = int(request.POST["lot_id"])
	try:
		auteur = identite.utilisateur(request)
		structure_id = int(request.POST["structure_id"])
		structure = dao_structure_salariale.toGet(structure_id)
		#print(structure)
		#print("ICII")
		if structure == None:
			#print("STUCTURE NONE")
			raise Exception("Sélectionner la structure salariale SVP!")

		#print("PASSER 1")
		list_employe_id = request.POST.getlist('employe_id', None)
		#print(len(list_employe_id))
		for i in range(0, len(list_employe_id)) :
			employe_id = int(list_employe_id[i])
			employe = dao_employe.toGetEmploye(employe_id)
			#print("PASSER 2")
			if employe.type_structure != None and employe.type_structure.id == structure.type.id:
				#print("PASSER 3")
				lot_bulletin = dao_lot_bulletin.toGet(lot_id)

				designation = "Bulletin de paie {}".format(employe.nom_complet)
				reference = ""
				periode = ""
				type = ""

				bulletin = dao_bulletin.toCreate(auteur.id, designation, employe_id, lot_id, reference, periode, type)
				bulletin = dao_bulletin.toSave(bulletin)
				#print("Bulletin cree ID {}".format(bulletin.id))

				#itemstructures = Model_ItemStructureSalariale.objects.filter(structure_id = structure.id)
				regles = structure.regles.all()

				for item in regles :
					#print("PASSER 4")
					regle_id = item.id
					montant = makeFloat("100")
					temps = makeFloat("1")
					taux = makeFloat("22")

					regle = dao_regle_salariale.toGet(regle_id)
					designation = "{}".format(regle.designation)

					item_bulletin = dao_item_bulletin.toCreate(auteur.id, designation, regle_id, bulletin.id, temps, taux, montant)
					item_bulletin = dao_item_bulletin.toSave(item_bulletin)
					#print("item_bulletin %i creee".format(item_bulletin))

		#print("PASSER 5")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lot_id,)))
	except Exception as e:
		#print("ERREUR POST BULLETIN")
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin',args=(lot_id,)))

def get_details_bulletin(request, ref):

	# droit="LISTER_BULLETIN"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
	# print("********DETAIL BULLETIN*******")
	permission_number = 185
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	# bulletin = ""
	# item_bulletins =""


	if response != None:
		return response

	try:
		ref = int(ref)
		bulletin = dao_bulletin.toGet(ref)
		item_bulletins = dao_item_bulletin.toGetItemOfBulletin(bulletin.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bulletin)
		# print(f"******employe {bulletin.employe.nom_complet} ")
		# print(f"******Grade {bulletin.employe.grade} Diplome {bulletin.employe.cycle_diplome}")

		context = {
			'title' : bulletin.designation,
			'model' : bulletin,
			'item_bulletins' : item_bulletins,
			'menu' : 7,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/bulletin/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bulletin'))


@transaction.atomic
def post_workflow_bulletin(request):
	sid = transaction.savepoint()
	try:
		utilisateur_id = request.user.id
		etape_id = request.POST["etape_id"]
		bulletin_id = request.POST["doc_id"]

		#print("print 1 %s %s %s" % (utilisateur_id, etape_id, bulletin_id))

		employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
		etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
		bulletin = dao_bulletin.toGet(bulletin_id)

		#print("print 2 %s %s %s " % (employe, etape, bulletin))

		transitions_etapes_suivantes = dao_wkf_etape.toListEtapeSuivante(bulletin.statut_id)
		for item in transitions_etapes_suivantes:

			"""
			if item.condition.designation == "CodeBudget":
				nombre_a_signer = bulletin.codes_budgetaires.all().count()
				nombre_deja_signer = dao_wkf_historique_lotbulletin.getCountSignatures( etape.id, bulletin.id)
				#print("nombre_a_signer %i " % nombre_a_signer)
				#print("nombre_deja_signer %i " % nombre_deja_signer)
				#On verifie si tous les utilisateurs hormis la personne, ont signé, si oui
				if int(nombre_a_signer) - int(nombre_deja_signer) == 1:
					# Gestion des transitions dans le document
					bulletin.statut_id = etape.id
					bulletin.etat = etape.designation
					bulletin.save()
			else:"""

			# Gestion des transitions dans le document
			bulletin.statut_id = etape.id
			bulletin.etat = etape.designation
			bulletin.save()

		historique = dao_wkf_historique_bulletin.toCreateHistoriqueWorkflow(employe.id, etape.id, bulletin.id)
		historique = dao_wkf_historique_bulletin.toSaveHistoriqueWorkflow(historique)

		if historique != None :
			transaction.savepoint_commit(sid)
			#print("OKAY")
			return HttpResponseRedirect(reverse('module_payroll_details_bulletin', args=(bulletin_id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_payroll_details_bulletin', args=(bulletin_id,)))

	except Exception as e:
		#print("ERREUR")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bulletin'))

#ELEMENT BULLETIN CONTROLLER
def get_lister_element(request):
	try:
		# droit="LISTER_ELEMENT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 190
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_element_bulletin.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_element_bulletin.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		# #print('rrrrrrrrrrrrrrrrrrrrrrrr')
		# for m in model:
		# 	#print("Désignation : {} ,  ID : {} ".format(m.designation, m.id))

		context = {
			'title' : 'Liste des éléments du bulletin',
			'model' : model,
			'view':view,
			'menu' : 9,
			'types_element' : dao_type_element_bulletin.toList(),
			'categories_element' : dao_categorie_element.toList(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/elementbulletin/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER ELEMENTS DE BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister éléments de Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_element(request):
	try:
		# droit="CREER_ELEMENT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 190
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False


		context = {
			'title' : 'Nouvel élément',
			'menu' : 9,
			'modules' : modules,'sous_modules': sous_modules,
			'isPopup' : isPopup,
			'types_element' : dao_type_element_bulletin.toList(),
			'categories_element' : dao_categorie_element.toList(),
			'types_calcul' : dao_type_calcul.toList(),
			'types_resultat' : dao_type_resultat.toList(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			'baremes' : dao_bareme.toList(),
			'comptes' : dao_compte.toListComptes(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/elementbulletin/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER ELEMENTS DE BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer éléments de Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_element"))

def post_creer_element(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		reference = request.POST["reference"]
		type_element = request.POST["type_element"]
		categorie_element = request.POST["categorie_element"]
		type_calcul = request.POST["type_calcul"]
		type_resultat = request.POST["type_resultat"]
		montant = makeFloat(request.POST["montant"])
		pourcentage = makeFloat(request.POST["pourcentage"])
		calcul = request.POST["calcul"]
		bareme_id = int(request.POST["bareme_id"])
		devise_id = int(request.POST["devise_id"])
		compte_id = int(request.POST["compte_id"])
		isPopup = request.POST['isPopup']
		sequence = int(request.POST["sequence"])

		element = dao_element_bulletin.toCreate(auteur.id, designation, type_element, categorie_element, reference, montant, type_calcul, type_resultat, pourcentage, calcul, bareme_id, devise_id, compte_id, sequence)
		element = dao_element_bulletin.toSave(element)

		url = '<a class="lien chargement-au-click" href="/payroll/elementbulletin/item/'+ str(element.id) +'/">'+ element.designation + '</a>'
		element.url = url
		element.save()

		if element != None :
			if isPopup == 'isPopup':
				return HttpResponseRedirect(reverse('module_payroll_details_element',args=(element.id,)))
			else:
				return HttpResponse('<script type="text/javascript">window.close();</script>')
		else :
			if isPopup == 'isPopup':
				messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement de l'élément du bulletin!")
				return HttpResponseRedirect(reverse('module_payroll_add_element'))
			else:
				return HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER ELEMENTS DE BULLETINS \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer éléments de Bulletins')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_element'))

def get_details_element(request, ref):
	try:
		# droit="LISTER_ELEMENT_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 189
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		ref = int(ref)
		element = dao_element_bulletin.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,element)

		context = {
			'title' : element.designation,
			'model' : element,
			'types_element' : dao_type_element_bulletin.toList(),
			'categories_element' : dao_categorie_element.toList(),
			'types_resultat' : dao_type_resultat.toList(),
			'types_calcul' : dao_type_calcul.toList(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'menu' : 9,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/elementbulletin/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER ELEMENTS BULLETIN \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Détailler éléments de bulletin')
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_element'))

#BAREME CONTROLLER
def get_lister_bareme(request):
	try:
		# droit="LISTER_BAREME"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 193
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_bareme.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_bareme.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des Barêmes',
			'model' : model,
			'view':view,
			'menu' : 10,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation()
		}
		template = loader.get_template("ErpProject/ModulePayroll/bareme/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER BAREME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister éléments de barème')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_bareme(request):
	try:
		# droit="CREER_BAREME"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 194
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False


		context = {
			'title' : 'Nouveau Barême',
			'menu' : 10,
			'modules' : modules,'sous_modules': sous_modules,
			'isPopup' : isPopup,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/bareme/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER BAREME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer barèmes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_bareme"))

@transaction.atomic
def post_creer_bareme(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		devise_id = request.POST["devise_id"]
		reference = request.POST["reference"]
		type = request.POST["type"]
		isPopup = 'isPopup'

		bareme = dao_bareme.toCreate(auteur.id, designation, devise_id, reference, type)
		bareme = dao_bareme.toSave(bareme)

		url = '<a class="lien chargement-au-click" href="/payroll/bareme/item/'+ str(bareme.id) +'/">'+ bareme.designation + '</a>'
		bareme.url = url
		bareme.save()

		if bareme != None :
			#list_tranche_id = request.POST.getlist('tranche_id', None)
			list_montant_ni = request.POST.getlist("montant", None)
			list_pourcentage_ni = request.POST.getlist("pourcentage_ni", None)
			list_tranche_debut = request.POST.getlist("tranche_debut", None)
			list_tranche_fin = request.POST.getlist("tranche_fin", None)
			list_sequence = request.POST.getlist("sequence", None)
			#print("Nbre Tranche")
			#print(len(list_sequence))
			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				montant_net_impot = makeFloat(list_montant_ni[i])
				pourcentage_net_impot = makeFloat(list_pourcentage_ni[i])
				tranche_debut = makeFloat(list_tranche_debut[i])
				tranche_fin = makeFloat(list_tranche_fin[i])
				designation = "Tranche %i du bareme %s (%.2f - %.2f)" % (sequence, bareme.designation, tranche_debut, tranche_fin)
				tranche_bareme = dao_tranche_bareme.toCreate(auteur.id, designation, bareme.id, bareme.devise_id, montant_net_impot, tranche_debut, tranche_fin, pourcentage_net_impot, sequence)
				tranche_bareme = dao_tranche_bareme.toSave(tranche_bareme)
				#print("Tranche %i creee" % tranche_bareme.sequence)

			if isPopup == 'isPopup':
				transaction.savepoint_commit(sid)
				return HttpResponseRedirect(reverse('module_payroll_details_bareme',args=(bareme.id,)))
			else:
				return HttpResponse('<script type="text/javascript">window.close();</script>')
		else :
			if isPopup == 'isPopup':
				messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du bareme!")
				transaction.savepoint_rollback(sid)
				return HttpResponseRedirect(reverse('module_payroll_add_bareme'))
			else:
				return HttpResponse('<script type="text/javascript">window.close();</script>')

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER BAREME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer barèmes')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_bareme'))

def get_details_bareme(request, ref):
	try:
		# droit="LISTER_BAREME"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 193
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		bareme = dao_bareme.toGet(ref)
		tranches = dao_tranche_bareme.toGetDuBareme(bareme.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,bareme)


		context = {
			'title' : bareme.designation,
			'model' : bareme,
			'tranches' : tranches,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'menu' : 10,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/bareme/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER BAREME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister barèmes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bareme'))

#PROFIL PAIE CONTROLLER
def get_lister_profilpaie(request):
	try:
		# droit="LISTER_PROFIL_PAIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 197
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response
		# model = dao_profil_paie.toListProfil()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_profil_paie.toListProfil(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des Profils paies',
			'model' : model,
			'view':view,
			'menu' : 11,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/profilpaie/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER PROFIL PAIE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister les profils de paie')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_profilpaie(request):
	try:
		# droit="CREER_PROFIL_PAIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 198
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		context = {
			'title' : 'Nouveau Profil Paye',
			'menu' : 11,
			'isPopup': isPopup,
			'modules' : modules,'sous_modules': sous_modules,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			'employes' : dao_employe.toListEmployesActifs(),
			'types_element' : dao_type_element_bulletin.toList(),
			'types_calcul' : dao_type_calcul.toList(),
			'types_resultat' : dao_type_resultat.toList(),
			'elements' : dao_element_bulletin.toList(),
			'categories_element' : dao_categorie_element.toList(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template("ErpProject/ModulePayroll/profilpaie/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER PROFIL PAIE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer profil paie')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_bareme"))

@transaction.atomic
def post_creer_profilpaie(request):
	sid = transaction.savepoint()
	try:
		#print(request.POST)
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		devise_id = request.POST["devise_id"]
		employe_id = request.POST["employe_id"]
		reference = request.POST["reference"]
		#type = request.POST["type"]

		profil_paie = dao_profil_paie.toCreateProfil(auteur.id, designation, employe_id, reference)
		profil_paie = dao_profil_paie.toSaveProfil(profil_paie)

		if profil_paie != None :
			list_id_element = request.POST.getlist('id_element', None)
			list_sequence = request.POST.getlist('sequence', None)
			list_designation_element = request.POST.getlist('designation_element', None)
			list_montant_element = request.POST.getlist("montant_element", None)
			list_pourcentage_element = request.POST.getlist("pourcentage_element", None)
			list_id_actif = request.POST.getlist("id_actif", None)
			#print(len(list_designation_element))
			#print(len(list_sequence))
			#print(len(list_montant_element))
			#print(len(list_pourcentage_element))
			#print(len(list_id_element))
			#print(len(list_id_actif))
			for i in range(0, len(list_id_element)) :
				if list_id_actif[i] == "2":
					itemProfil = Model_ItemProfilPaye()
					itemProfil.designation = list_designation_element[i]
					#print(list_designation_element[i])
					itemProfil.sequence = int(list_sequence[i])
					#print(list_sequence[i])
					itemProfil.montant = makeFloat(list_montant_element[i])
					#print(list_montant_element[i])
					itemProfil.valeur_pourcentage = makeFloat(list_pourcentage_element[i])
					#print(list_pourcentage_element[i])
					itemProfil.element_id = int(list_id_element[i])
					#print(list_id_element[i])
					itemProfil.creation_date = timezone.now()
					itemProfil.profil_paie_id = profil_paie.id
					itemProfil.save()
					#print("Item Profil %i creee" % itemProfil.id)

			transaction.savepoint_commit(sid)
			return HttpResponseRedirect(reverse('module_payroll_details_profilpaie',args=(profil_paie.id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du bareme!")
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_payroll_add_profilpaie'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER PROFIL PAIE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post Créer profil paie')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_profilpaie'))

def get_details_profilpaie(request, ref):
	try:
		# droit="LISTER_PROFIL_PAIE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 197
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#print("REF")
		#print(ref)
		ref = int(ref)
		#print(ref)
		profilpaie = dao_profil_paie.toGetProfil(ref)
		item_profilpaies = Model_ItemProfilPaye.objects.filter(profil_paie_id = profilpaie.id).order_by("creation_date")

		#print(item_profilpaies)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,profilpaie)

		context = {
			'title' : profilpaie.designation,
			'model' : profilpaie,
			'item_profilpaies' : item_profilpaies,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'types_element' : dao_type_element_bulletin.toList(),
			'types_resultat' : dao_type_resultat.toList(),
			'types_calcul' : dao_type_calcul.toList(),
			'categories_element' : dao_categorie_element.toList(),
			'menu' : 11,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
		}
		template = loader.get_template("ErpProject/ModulePayroll/profilpaie/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST DETAILLER PROFIL PAIE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post détailler profil paie')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_profilpaie'))


# TYPE STRUCTURE SALARIALE CONTROLLERS
def get_lister_type_structure(request):
	try:
		# droit = "LISTER_TYPE_structure"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 395
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		# model = dao_type_structure.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_type_structure.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		title = "Liste des type structures"
		context ={
			'title' : title,
			'model' : model,
			'view':view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/type_structure/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des type structures \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des type structures')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

def get_details_type_structure(request, ref):
	try:
		# droit="LISTER_TYPE_STRUCTURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 395
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		model = dao_type_structure.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'title' : 'Type structure {}'.format(model.designation),
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
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/type_structure/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details type structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail type structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_type_structure'))

def get_creer_type_structure(request):
	try:
		# droit="CREER__TYPE_STRUCTURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 396
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_salaires = dao_type_structure.toListTypeSalaire()
		horaire_payes = dao_type_structure.toListHorairePaye()

		context = {
			'title' : 'Créer un type structure',
			'isPopup': isPopup,
			'utilisateur' : utilisateur,
			'type_salaires': type_salaires,
			'horaire_payes' : horaire_payes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/type_structure/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_type_structure'))

def post_creer_type_structure(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		type_salaire = request.POST["type_salaire"]
		horaire_paye = request.POST["horaire_paye"]

		type_structure = dao_type_structure.toCreate(auteur.id, designation, type_salaire, horaire_paye, description)
		type_structure = dao_type_structure.toSave(type_structure)
		return HttpResponseRedirect(reverse('module_payroll_details_type_structure', args=(type_structure.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer type structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer type structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_type_structure'))

def get_modifier_type_structure(request, ref):
	try:
		# droit="MODIFIER_TYPE_STRUCTURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 397
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_type_structure.toGet(ref)

		type_salaires = dao_type_structure.toListTypeSalaire()
		horaire_payes = dao_type_structure.toListHorairePaye()

		context = {
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			'type_salaires': type_salaires,
			'horaire_payes' : horaire_payes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/type_structure/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier type structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier type structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_type_structure'))

def post_modifier_type_structure(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		type_salaire = request.POST["type_salaire"]
		horaire_paye = request.POST["horaire_paye"]

		type_structure = dao_type_structure.toCreate(auteur.id, designation, type_salaire, horaire_paye, description)
		type_structure = dao_type_structure.toUpdate(ref, type_structure)

		if type_structure == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_payroll_details_type_structure', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier type structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_type_structure'))

def get_upload_type_structure(request):
	try:
		permission_number = 396
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des types structure",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModulePayroll/type_structure/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD type_structure")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_type_structure"))


@transaction.atomic
def post_upload_type_structure(request):
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
			designation = str(df['designation'][i])
			description = str(df['description'][i])
			type_salaire = str(df['type_salaire'][i])
			horaire_paye = str(df['horaire_paye'][i])

			type_structure = dao_type_structure.toCreate(auteur.id, designation, type_salaire, horaire_paye, description)
			type_structure = dao_type_structure.toSave(type_structure)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_payroll_list_type_structure"))
	except Exception as e:
		#print("ERREUR POST UPLOAD type_structure")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD type_structure \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_payroll_add_type_structure"))

#STRUCTURE SALARIALE CONTROLLER
def get_lister_structure_salariale(request):
	try:
		# droit="LISTER_STRUCTURE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 399
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_structure_salariale.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_structure_salariale.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des structures salariales',
			'model' : model,
			'view':view,
			'menu' : 11,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/structure_salariale/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER STRUCTURE SALARIALE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister les profils de paie')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_structure_salariale(request):
	try:
		# droit="CREER_STRUCTURE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 400
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False
		type_structures = dao_type_structure.toList()
		horaire_payes = dao_structure_salariale.toListHorairePaye()
		journaux = dao_journal.toListJournauxPaie()
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		regles = dao_regle_salariale.toList()

		context = {
			'title' : 'Nouvelle Structure de salaire',
			'menu' : 11,
			'isPopup': isPopup,
			"modules" : modules,
			'devise_ref' : devise_ref,
			'devises' : devises,
			'type_structures' : type_structures,
			'horaire_payes' : horaire_payes,
			'journaux' : journaux,
			'regles' : regles,
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/structure_salariale/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER STRUCTURE SALARIALE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer STRUCTURE SALARIALE')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_structure_salariale"))

@transaction.atomic
def post_creer_structure_salariale(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		devise_id = request.POST["devise_id"]
		journal_id = request.POST["journal_id"]
		type_id = request.POST["type_id"]
		horaire_paye = request.POST["horaire_paye"]
		libelle_bulletin = request.POST["libelle_bulletin"]
		par_defaut = False
		if "par_defaut" in request.POST : par_defaut = True
		list_regle_id = request.POST.getlist('regle_id', None)

		structure_salariale = dao_structure_salariale.toCreate(auteur.id, designation, type_id, horaire_paye, libelle_bulletin, journal_id, devise_id, par_defaut, description)
		structure_salariale = dao_structure_salariale.toSave(structure_salariale)
		#print("Structure salariale {} cree".format(structure_salariale.id))

		#Ajout des règles slariales  (ManyToMany - Creation)
		for i in range(0, len(list_regle_id)):
			regle_id = int(list_regle_id[i])
			regle = Model_RegleSalariale.objects.get(pk = regle_id)
			structure_salariale.regles.add(regle)

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_structure_salariale',args=(structure_salariale.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER STRUCTURE SALARIALE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post Créer STRUCTURE SALARIALE')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_structure_salariale'))

def get_details_structure_salariale(request, ref):
	try:
		# droit="LISTER_STRUCTURE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 399
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		#print(ref)
		structure = dao_structure_salariale.toGet(ref)
		regles = structure.regles.all()
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,structure)

		context = {
			'title' : structure.designation,
			'model' : structure,
			'regles' : regles,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'menu' : 11,
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/structure_salariale/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST DETAILLER STRUCTURE SALARIALE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post détailler STRUCTURE SALARIALE')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_structure_salariale'))

def get_modifier_structure_salariale(request, ref):
	try:
		# droit="MODIFIER_STRUCTURE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 401
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		model = dao_structure_salariale.toGet(ref)
		type_structures = dao_type_structure.toList()
		horaire_payes = dao_structure_salariale.toListHorairePaye()
		journaux = dao_journal.toListJournauxPaie()
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		regles = dao_regle_salariale.toList()

		context = {
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'regles' : regles,
			'utilisateur' : utilisateur,
			'devise_ref' : devise_ref,
			'devises' : devises,
			'type_structures' : type_structures,
			'horaire_payes' : horaire_payes,
			'journaux' : journaux,
			'actions': auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/structure_salariale/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_structure_salariale'))

@transaction.atomic
def post_modifier_structure_salariale(request):
	ref = int(request.POST["ref"])
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		devise_id = request.POST["devise_id"]
		journal_id = request.POST["journal_id"]
		type_id = request.POST["type_id"]
		horaire_paye = request.POST["horaire_paye"]
		libelle_bulletin = request.POST["libelle_bulletin"]
		par_defaut = False
		if "par_defaut" in request.POST : par_defaut = True
		list_regle_id = request.POST.getlist('regle_id', None)

		structure_salariale = dao_structure_salariale.toCreate(auteur.id, designation, type_id, horaire_paye, libelle_bulletin, journal_id, devise_id, par_defaut, description)
		is_updated = dao_structure_salariale.toUpdate(ref, structure_salariale)
		structure_salariale = dao_structure_salariale.toGet(ref)

		if is_updated == False:
			raise  Exception("Erreur modification")

		#Ajout des regles (ManyToMany - Modification)
		reglesOld = structure_salariale.regles.all()
		reglesUpdated = []
		for i in range(0, len(list_regle_id)):
			existe = False
			regle_id = int(list_regle_id[i])
			regle = Model_RegleSalariale.objects.get(pk = regle_id)
			for item in reglesOld:
				if item.id == regle.id:
					existe = True
			reglesUpdated.append(regle.id)
			# Enregistrement  nouvel élément
			if existe == False: structure_salariale.regles.add(regle)
		# Suppression éléments qui n'existent plus
		for item in reglesOld:
			if item.id not in reglesUpdated:
				#print("regle {} recupere".format(item.id))
				structure_salariale.regles.remove(item)
				#print("regle supprime")

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_structure_salariale', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier la structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier la structure')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_structure_salariale'))


# CATEGORIE REGLE CONTROLLERS
def get_lister_categorie_regle(request):
	try:
		# droit = "LISTER_CATEGORIE_REGLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 403
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_categorie_regle.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_categorie_regle.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#

		title = "Liste des categories"
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
			'title' : title,
			'model' : model,
			'view':view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/categorie_regle/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des categorie_regles \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des categorie_regles')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

def get_details_categorie_regle(request, ref):
	try:
		# droit="LISTER_CATEGORIE_REGLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 403
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_categorie_regle.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'title' : 'Catégorie règle {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/categorie_regle/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details categorie_regle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail categorie_regle')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_categorie_regle'))

def get_creer_categorie_regle(request):
	try:
		# droit="CREER_CATEGORIE_REGLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 404
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False
		context = {
			'title' : 'Créer une catégorie règle',
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/categorie_regle/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer categorie_regle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer categorie_regle')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_categorie_regle'))

def post_creer_categorie_regle(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		code = request.POST["code"]

		categorie_regle = dao_categorie_regle.toCreate(auteur.id, designation, code, description)
		categorie_regle = dao_categorie_regle.toSave(categorie_regle)
		return HttpResponseRedirect(reverse('module_payroll_details_categorie_regle', args=(categorie_regle.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer categorie_regle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer categorie_regle')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_categorie_regle'))

def get_modifier_categorie_regle(request, ref):
	try:
		# droit = "MODIFIER_CATEGORIE_REGLE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 405
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		model = dao_categorie_regle.toGet(ref)

		context = {
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/categorie_regle/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier categorie_regle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier categorie_regle')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_categorie_regle'))

def post_modifier_categorie_regle(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		code = request.POST["code"]

		categorie_regle = dao_categorie_regle.toCreate(auteur.id, designation, code, description)
		categorie_regle = dao_categorie_regle.toUpdate(ref, categorie_regle)

		if categorie_regle == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_payroll_details_categorie_regle', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier categorie_regle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier categorie regle')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_categorie_regle'))

def get_upload_categorie_regle(request):
	try:
		permission_number = 403
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des catégories règles",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModulePayroll/categorie_regle/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD categorie_regle")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_categorie_regle"))


@transaction.atomic
def post_upload_categorie_regle(request):
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
			code = str(df['code'][i])
			designation = str(df['designation'][i])
			description = str(df['description'][i])

			categorie_regle = dao_categorie_regle.toCreate(auteur.id, designation, code, description)
			categorie_regle = dao_categorie_regle.toSave(categorie_regle)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_payroll_list_categorie_regle"))
	except Exception as e:
		#print("ERREUR POST UPLOAD categorie_regle")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD categorie_regle \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_payroll_add_categorie_regle"))

# REGLE SALARIALE CONTROLLERS
def get_lister_regle_salariale(request):
	try:
		# droit = "LISTER_REGLE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 408
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_regle_salariale.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_regle_salariale.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		title = "Liste des règles salariales"
		context ={
			'title' : title,
			'model' : model,
			'view':view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/regle_salariale/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des regle_salariales \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des regle_salariales')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

def get_details_regle_salariale(request, ref):
	try:
		# droit="LISTER_REGLE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 408
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_regle_salariale.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'title' : 'règle salariale {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/regle_salariale/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details regle_salariale\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail regle_salariale')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_regle_salariale'))

def get_creer_regle_salariale(request):
	try:
		# droit="CREER_REGLE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 407
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_calculs = dao_regle_salariale.toListTypeCalcul()
		type_conditions = dao_regle_salariale.toListTypeCondition()
		baremes = dao_bareme.toList()
		comptes = dao_compte.toListComptes()
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		categories = dao_categorie_regle.toList()

		context = {
			'title' : 'Créer une règle salariale',
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'type_calculs': type_calculs,
			'type_conditions': type_conditions,
			'types_element' : dao_type_element_bulletin.toList(),
			'baremes': baremes,
			'comptes': comptes,
			'devises': devises,
			'categories': categories,
			'devise_ref': devise_ref,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/regle_salariale/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer regle_salariale\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer regle_salariale')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_regle_salariale'))

def post_creer_regle_salariale(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		devise_id = int(request.POST["devise_id"])
		compte_debit_id = int(request.POST["compte_debit_id"])
		compte_credit_id = int(request.POST["compte_credit_id"])
		bareme_id = int(request.POST["bareme_id"])
		categorie_id = int(request.POST["categorie_id"])
		code = request.POST["code"]
		sequence = request.POST["sequence"]
		quantite = request.POST["quantite"]
		type_calcul = request.POST["type_calcul"]
		type_condition = request.POST["type_condition"]
		plage_condition = request.POST["plage_condition"]
		code_condition = request.POST["code_condition"]
		plage_min_condition = request.POST["plage_min_condition"]
		plage_max_condition = request.POST["plage_max_condition"]
		montant_fixe = request.POST["montant_fixe"]
		pourcentage = request.POST["pourcentage"]
		pourcentage_sur = request.POST["pourcentage_sur"]
		code_python = request.POST["code_python"]
		type_element = request.POST["type_element"]
		apparait_dans_bulletin = False
		if "apparait_dans_bulletin" in request.POST : apparait_dans_bulletin = True
		type_resultat = 1


		regle_salariale = dao_regle_salariale.toCreate(auteur.id, designation, code, description, sequence, quantite, categorie_id, type_condition, plage_condition, code_condition, plage_min_condition, plage_max_condition, type_calcul, type_resultat, montant_fixe, pourcentage, pourcentage_sur, code_python, bareme_id, devise_id, compte_debit_id, compte_credit_id, apparait_dans_bulletin, True, type_element)
		regle_salariale = dao_regle_salariale.toSave(regle_salariale)
		#print("Regle salariale {} cree".format(regle_salariale.id))
		return HttpResponseRedirect(reverse('module_payroll_details_regle_salariale', args=(regle_salariale.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer regle_salariale\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer regle_salariale')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_regle_salariale'))

def get_modifier_regle_salariale(request, ref):
	try:
		# droit="MODIFIER_REGLE_SALARIALE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 409
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		model = dao_regle_salariale.toGet(ref)
		type_calculs = dao_regle_salariale.toListTypeCalcul()
		type_conditions = dao_regle_salariale.toListTypeCondition()
		baremes = dao_bareme.toList()
		comptes = dao_compte.toListComptes()
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		categories = dao_categorie_regle.toList()

		context = {
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'type_calculs': type_calculs,
			'type_conditions': type_conditions,
			'baremes': baremes,
			'comptes': comptes,
			'devises': devises,
			'categories': categories,
			'types_element' : dao_type_element_bulletin.toList(),
			'devise_ref': devise_ref,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/regle_salariale/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier regle_salariale\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier regle_salariale')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_regle_salariale'))

def post_modifier_regle_salariale(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		devise_id = int(request.POST["devise_id"])
		compte_debit_id = int(request.POST["compte_debit_id"])
		compte_credit_id = int(request.POST["compte_credit_id"])
		bareme_id = int(request.POST["bareme_id"])
		categorie_id = int(request.POST["categorie_id"])
		code = request.POST["code"]
		sequence = request.POST["sequence"]
		quantite = request.POST["quantite"]
		type_calcul = request.POST["type_calcul"]
		type_condition = request.POST["type_condition"]
		plage_condition = request.POST["plage_condition"]
		code_condition = request.POST["code_condition"]
		plage_min_condition = request.POST["plage_min_condition"]
		plage_max_condition = request.POST["plage_max_condition"]
		montant_fixe = request.POST["montant_fixe"]
		pourcentage = request.POST["pourcentage"]
		pourcentage_sur = request.POST["pourcentage_sur"]
		code_python = request.POST["code_python"]
		type_element = request.POST["type_element"]
		apparait_dans_bulletin = False
		if "apparait_dans_bulletin" in request.POST : apparait_dans_bulletin = True
		type_resultat = 1


		regle_salariale = dao_regle_salariale.toCreate(auteur.id, designation, code, description, sequence, quantite, categorie_id, type_condition, plage_condition, code_condition, plage_min_condition, plage_max_condition, type_calcul, type_resultat, montant_fixe, pourcentage, pourcentage_sur, code_python, bareme_id, devise_id, compte_debit_id, compte_credit_id, apparait_dans_bulletin, True, type_element)
		regle_salariale = dao_regle_salariale.toUpdate(ref, regle_salariale)

		if regle_salariale == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_payroll_details_regle_salariale', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier regle_salariale\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier regle_salariale')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_regle_salariale'))

# RUBRIQUE CONTROLLERS
def get_lister_rubrique(request):
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_rubrique.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_rubrique.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		title = "Liste des rubriques"
		context = {
			'title' : title,
			'model' : model,
			'view':view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/rubrique/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des rubriques \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des rubriques')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

def get_details_rubrique(request, ref):
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		model = dao_rubrique.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)

		context ={
			'title' : 'rubrique {}'.format(model.designation),
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
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/rubrique/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details rubrique\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail rubrique')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_rubrique'))

def get_creer_rubrique(request):
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False


		type_elements = dao_rubrique.toListTypeElementBulletin()
		type_rubriques = dao_rubrique.toListTypeRubrique()
		type_formules = dao_rubrique.toListTypeFormule()
		comptes = dao_compte.toListComptes()
		devises = dao_devise.toListDevisesActives()

		constantes = dao_constante.toList()

		context = {
			'title' : 'Créer une rubrique',
			'isPopup': isPopup,
			'utilisateur' : utilisateur,
			'type_elements': type_elements,
			'type_rubriques' : type_rubriques,
			'type_formules' : type_formules,
			'comptes': comptes,
			'devises': devises,
			'constantes':constantes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/rubrique/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer rubrique\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer rubrique')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_rubrique'))

def post_creer_rubrique(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		reference = request.POST["reference"]
		code = request.POST["code"]
		sequence = request.POST["sequence"]
		description = request.POST["description"]
		devise_id = int(request.POST["devise_id"])
		if devise_id == 0: devise_id = None
		compte_debit_id = int(request.POST["compte_debit_id"])
		if compte_debit_id == 0: compte_debit_id = None
		compte_credit_id = int(request.POST["compte_credit_id"])
		if compte_credit_id == 0: compte_credit_id = None
		type_element = int(request.POST["type_element"])
		if type_element == 0: type_element = None
		type_rubrique = int(request.POST["type_rubrique"])
		type_formule = int(request.POST["type_formule"])
		apparait_dans_bulletin = False
		if "apparait_dans_bulletin" in request.POST : apparait_dans_bulletin = True
		est_cumul = False
		if "est_cumul" in request.POST : est_cumul = True

		nombre_est_modifiable = False
		if "nombre_est_modifiable" in request.POST : nombre_est_modifiable = True
		base_est_modifiable = False
		if "base_est_modifiable" in request.POST : base_est_modifiable = True
		taux_est_modifiable = False
		if "taux_est_modifiable" in request.POST : taux_est_modifiable = True
		montant_est_modifiable = False
		if "montant_est_modifiable" in request.POST : montant_est_modifiable = True
		taux_pp_est_modifiable = False
		if "taux_pp_est_modifiable" in request.POST : taux_pp_est_modifiable = True
		montant_pp_est_modifiable = False
		if "montant_pp_est_modifiable" in request.POST : montant_pp_est_modifiable = True

		cumul_brut = int(request.POST["brut"])
		cumul_brutcong = int(request.POST["brutcong"])
		cumul_coutotsal = int(request.POST["coutotsal"])
		cumul_coutotpat = int(request.POST["coutotpat"])
		cumul_netpaie = int(request.POST["netpaie"])
		cumul_netimpo = int(request.POST["netimpo"])
		cumul_cotisal = int(request.POST["cotisal"])
		cumul_cotipat = int(request.POST["cotipat"])
		cumul_sous_pat = int(request.POST["sous_pat"])
		cumul_avantur = int(request.POST["avantur"])
		cumul_totapay = int(request.POST["totapay"])
		cumul_totaret = int(request.POST["totaret"])

		nombre_parsal  = 0.0
		nombre_parsal_is_const  = False
		nombre_parsal_const_id  =  None
		if "nombre_input" in request.POST :
			nombre_parsal_is_const = int(request.POST["nombre_input_is_const"])
			if nombre_parsal_is_const == 0: nombre_parsal_is_const = False
			else: nombre_parsal_is_const = True
			nombre_parsal = makeFloat(request.POST["nombre_input"])
			nombre_parsal_const_id = int(request.POST["nombre_select"])
			if nombre_parsal_const_id == 0: nombre_parsal_const_id = None

		base_parsal  = 0.0
		base_parsal_is_const  = False
		base_parsal_const_id  =  None
		if "base_input" in request.POST :
			base_parsal_is_const = int(request.POST["base_input_is_const"])
			if base_parsal_is_const == 0: base_parsal_is_const = False
			else: base_parsal_is_const = True
			base_parsal = makeFloat(request.POST["base_input"])
			base_parsal_const_id = int(request.POST["base_select"])
			if base_parsal_const_id == 0: base_parsal_const_id = None

		taux_parsal  = 0.0
		taux_parsal_is_const  = False
		taux_parsal_const_id  =  None
		if "taux_input" in request.POST :
			taux_parsal_is_const = int(request.POST["taux_input_is_const"])
			if taux_parsal_is_const == 0: taux_parsal_is_const = False
			else: taux_parsal_is_const = True
			taux_parsal = makeFloat(request.POST["taux_input"])
			taux_parsal_const_id = int(request.POST["taux_select"])
			if taux_parsal_const_id == 0: taux_parsal_const_id = None

		montant_parsal  = 0.0
		montant_parsal_is_const  = False
		montant_parsal_const_id  =  None
		if "montant_input" in request.POST :
			montant_parsal_is_const = int(request.POST["montant_input_is_const"])
			if montant_parsal_is_const == 0: montant_parsal_is_const = False
			else: montant_parsal_is_const = True
			montant_parsal = makeFloat(request.POST["montant_input"])
			montant_parsal_const_id = int(request.POST["montant_select"])
			if montant_parsal_const_id == 0: montant_parsal_const_id = None

		taux_parpat  = 0.0
		taux_parpat_is_const  = False
		taux_parpat_const_id  =  None
		if "patronal_taux_input" in request.POST :
			taux_parpat_is_const = int(request.POST["patronal_taux_input_is_const"])
			if taux_parpat_is_const == 0: taux_parpat_is_const = False
			else: taux_parpat_is_const = True
			taux_parpat = makeFloat(request.POST["patronal_taux_input"])
			taux_parpat_const_id = int(request.POST["patronal_taux_select"])
			if taux_parpat_const_id == 0: taux_parpat_const_id = None

		montant_parpat  = 0.0
		montant_parpat_is_const  = False
		montant_parpat_const_id  =  None
		if "patronal_montant_input" in request.POST :
			montant_parpat_is_const = int(request.POST["patronal_montant_input_is_const"])
			if montant_parpat_is_const == 0: montant_parpat_is_const = False
			else: montant_parpat_is_const = True
			montant_parpat = makeFloat(request.POST["patronal_montant_input"])
			montant_parpat_const_id = int(request.POST["patronal_montant_select"])
			if montant_parpat_const_id == 0: montant_parpat_const_id = None

		rubrique = dao_rubrique.toCreate(auteur.id, designation,  reference, code, description, sequence, type_rubrique, type_formule, type_element, nombre_parsal, nombre_parsal_is_const, nombre_parsal_const_id, base_parsal, base_parsal_is_const, base_parsal_const_id, taux_parsal, taux_parsal_is_const, taux_parsal_const_id, montant_parsal, montant_parsal_is_const, montant_parsal_const_id, taux_parpat, taux_parpat_is_const, taux_parpat_const_id, montant_parpat, montant_parpat_is_const, montant_parpat_const_id,  True, apparait_dans_bulletin, compte_debit_id, compte_credit_id, devise_id)
		rubrique = dao_rubrique.toSave(rubrique)
		rubrique.nombre_est_modifiable = nombre_est_modifiable
		rubrique.base_est_modifiable = base_est_modifiable
		rubrique.taux_est_modifiable = taux_est_modifiable
		rubrique.montant_est_modifiable = montant_est_modifiable
		rubrique.taux_pp_est_modifiable = taux_pp_est_modifiable
		rubrique.montant_pp_est_modifiable = montant_pp_est_modifiable
		rubrique.est_cumul = est_cumul
		rubrique.save()
		#print("Rubrique {} cree".format(rubrique.code))

		#Gestion des cumuls
		if cumul_brut != 1:
			brut = dao_constante.toGetByCode("brut")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = brut.id, type_operation = cumul_brut, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_brutcong != 1:
			brutcong = dao_constante.toGetByCode("brutcong")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = brutcong.id, type_operation = cumul_brutcong, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_coutotsal != 1:
			coutotsal = dao_constante.toGetByCode("coutotsal")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = coutotsal.id, type_operation = cumul_coutotsal, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_coutotpat != 1:
			coutotpat = dao_constante.toGetByCode("coutotpat")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = coutotpat.id, type_operation = cumul_coutotpat, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_netpaie != 1:
			netpaie = dao_constante.toGetByCode("netpaie")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = netpaie.id, type_operation = cumul_netpaie, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_netimpo != 1:
			netimpo = dao_constante.toGetByCode("netimpo")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = netimpo.id, type_operation = cumul_netimpo, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_cotisal != 1:
			cotisal = dao_constante.toGetByCode("cotisal")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = cotisal.id, type_operation = cumul_cotisal, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_cotipat != 1:
			cotipat = dao_constante.toGetByCode("cotipat")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = cotipat.id, type_operation = cumul_cotipat, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_sous_pat != 1:
			sous_pat = dao_constante.toGetByCode("sous_pat")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = sous_pat.id, type_operation = cumul_sous_pat, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_avantur != 1:
			avantur = dao_constante.toGetByCode("avantur")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = avantur.id, type_operation = cumul_avantur, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_totapay != 1:
			totapay = dao_constante.toGetByCode("totapay")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = totapay.id, type_operation = cumul_totapay, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		if cumul_totaret != 1:
			totaret = dao_constante.toGetByCode("totaret")
			calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = totaret.id, type_operation = cumul_totaret, rubrique_id = rubrique.id)
			calcul.save()
			#print("Ligne Calcul {} cree".format(calcul.sequence))
		return HttpResponseRedirect(reverse('module_payroll_details_rubrique', args=(rubrique.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer rubrique\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer rubrique')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_rubrique'))

def get_modifier_rubrique(request, ref):
	try:
		# droit="MODIFIER_rubrique"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		rubrique = dao_rubrique.toGet(ref)

		type_elements = dao_rubrique.toListTypeElementBulletin()
		type_rubriques = dao_rubrique.toListTypeRubrique()
		type_formules = dao_rubrique.toListTypeFormule()
		comptes = dao_compte.toListComptes()
		devises = dao_devise.toListDevisesActives()

		constantes = dao_constante.toList()
		comptes = dao_compte.toListComptes()

		brut = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "brut", rubrique_id = rubrique.id).first()
		brutcong = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "brutcong", rubrique_id = rubrique.id).first()
		coutotsal = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "coutotsal", rubrique_id = rubrique.id).first()
		coutotpat = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "coutotpat", rubrique_id = rubrique.id).first()
		netpaie = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "netpaie", rubrique_id = rubrique.id).first()
		netimpo = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "netimpo", rubrique_id = rubrique.id).first()
		cotisal = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "cotisal", rubrique_id = rubrique.id).first()
		cotipat = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "cotipat", rubrique_id = rubrique.id).first()
		sous_pat = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "sous_pat", rubrique_id = rubrique.id).first()
		avantur = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "avantur", rubrique_id = rubrique.id).first()
		totapay = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "totapay", rubrique_id = rubrique.id).first()
		totaret = Model_ConstanteCalcul.objects.filter(constante_parent__code__iexact = "totaret", rubrique_id = rubrique.id).first()

		context = {
			'title' : 'Modifier {}'.format(rubrique.designation),
			'model' : rubrique,
			'utilisateur' : utilisateur,
			'type_elements': type_elements,
			'type_rubriques' : type_rubriques,
			'type_formules' : type_formules,
			'constantes' : constantes,
			'comptes': comptes,
			'brut' : brut,
			'brutcong': brutcong,
			'coutotsal' : coutotsal,
			'coutotpat' : coutotpat,
			'netpaie' : netpaie,
			'netimpo' : netimpo,
			'cotisal': cotisal,
			'cotipat' : cotipat,
			'sous_pat' : sous_pat,
			'avantur' : avantur,
			'totapay' : totapay,
			'totaret' : totaret,
			'devises': devises,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/rubrique/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier rubrique\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier rubrique')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_rubrique'))

def post_modifier_rubrique(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)

		designation = request.POST["designation"]
		reference = request.POST["reference"]
		code = request.POST["code"]
		sequence = request.POST["sequence"]
		description = request.POST["description"]
		devise_id = int(request.POST["devise_id"])
		if devise_id == 0: devise_id = None
		compte_debit_id = int(request.POST["compte_debit_id"])
		if compte_debit_id == 0: compte_debit_id = None
		compte_credit_id = int(request.POST["compte_credit_id"])
		if compte_credit_id == 0: compte_credit_id = None
		type_element = int(request.POST["type_element"])
		if type_element == 0: type_element = None
		type_rubrique = int(request.POST["type_rubrique"])
		type_formule = int(request.POST["type_formule"])
		apparait_dans_bulletin = False
		if "apparait_dans_bulletin" in request.POST : apparait_dans_bulletin = True

		est_cumul = False
		if "est_cumul" in request.POST : est_cumul = True

		nombre_est_modifiable = False
		if "nombre_est_modifiable" in request.POST : nombre_est_modifiable = True
		base_est_modifiable = False
		if "base_est_modifiable" in request.POST : base_est_modifiable = True
		taux_est_modifiable = False
		if "taux_est_modifiable" in request.POST : taux_est_modifiable = True
		montant_est_modifiable = False
		if "montant_est_modifiable" in request.POST : montant_est_modifiable = True
		taux_pp_est_modifiable = False
		if "taux_pp_est_modifiable" in request.POST : taux_pp_est_modifiable = True
		montant_pp_est_modifiable = False
		if "montant_pp_est_modifiable" in request.POST : montant_pp_est_modifiable = True

		cumul_brut = int(request.POST["brut"])
		cumul_brutcong = int(request.POST["brutcong"])
		cumul_coutotsal = int(request.POST["coutotsal"])
		cumul_coutotpat = int(request.POST["coutotpat"])
		cumul_netpaie = int(request.POST["netpaie"])
		cumul_netimpo = int(request.POST["netimpo"])
		cumul_cotisal = int(request.POST["cotisal"])
		cumul_cotipat = int(request.POST["cotipat"])
		cumul_sous_pat = int(request.POST["sous_pat"])
		cumul_avantur = int(request.POST["avantur"])
		cumul_totapay = int(request.POST["totapay"])
		cumul_totaret = int(request.POST["totaret"])

		nombre_parsal  = 0.0
		nombre_parsal_is_const  = False
		nombre_parsal_const_id  =  None
		if "nombre_input" in request.POST :
			nombre_parsal_is_const = int(request.POST["nombre_input_is_const"])
			if nombre_parsal_is_const == 0: nombre_parsal_is_const = False
			else: nombre_parsal_is_const = True
			nombre_parsal = makeFloat(request.POST["nombre_input"])
			nombre_parsal_const_id = int(request.POST["nombre_select"])
			if nombre_parsal_const_id == 0: nombre_parsal_const_id = None

		base_parsal  = 0.0
		base_parsal_is_const  = False
		base_parsal_const_id  =  None
		if "base_input" in request.POST :
			base_parsal_is_const = int(request.POST["base_input_is_const"])
			if base_parsal_is_const == 0: base_parsal_is_const = False
			else: base_parsal_is_const = True
			base_parsal = makeFloat(request.POST["base_input"])
			base_parsal_const_id = int(request.POST["base_select"])
			if base_parsal_const_id == 0: base_parsal_const_id = None

		taux_parsal  = 0.0
		taux_parsal_is_const  = False
		taux_parsal_const_id  =  None
		if "taux_input" in request.POST :
			taux_parsal_is_const = int(request.POST["taux_input_is_const"])
			if taux_parsal_is_const == 0: taux_parsal_is_const = False
			else: taux_parsal_is_const = True
			taux_parsal = makeFloat(request.POST["taux_input"])
			taux_parsal_const_id = int(request.POST["taux_select"])
			if taux_parsal_const_id == 0: taux_parsal_const_id = None

		montant_parsal  = 0.0
		montant_parsal_is_const  = False
		montant_parsal_const_id  =  None
		if "montant_input" in request.POST :
			montant_parsal_is_const = int(request.POST["montant_input_is_const"])
			if montant_parsal_is_const == 0: montant_parsal_is_const = False
			else: montant_parsal_is_const = True
			montant_parsal = makeFloat(request.POST["montant_input"])
			montant_parsal_const_id = int(request.POST["montant_select"])
			if montant_parsal_const_id == 0: montant_parsal_const_id = None

		taux_parpat  = 0.0
		taux_parpat_is_const  = False
		taux_parpat_const_id  =  None
		if "patronal_taux_input" in request.POST :
			taux_parpat_is_const = int(request.POST["patronal_taux_input_is_const"])
			if taux_parpat_is_const == 0: taux_parpat_is_const = False
			else: taux_parpat_is_const = True
			taux_parpat = makeFloat(request.POST["patronal_taux_input"])
			taux_parpat_const_id = int(request.POST["patronal_taux_select"])
			if taux_parpat_const_id == 0: taux_parpat_const_id = None

		montant_parpat  = 0.0
		montant_parpat_is_const  = False
		montant_parpat_const_id  =  None
		if "patronal_montant_input" in request.POST :
			montant_parpat_is_const = int(request.POST["patronal_montant_input_is_const"])
			if montant_parpat_is_const == 0: montant_parpat_is_const = False
			else: montant_parpat_is_const = True
			montant_parpat = makeFloat(request.POST["patronal_montant_input"])
			montant_parpat_const_id = int(request.POST["patronal_montant_select"])
			if montant_parpat_const_id == 0: montant_parpat_const_id = None

		rubrique = dao_rubrique.toCreate(auteur.id, designation,  reference, code, description, sequence, type_rubrique, type_formule, type_element, nombre_parsal, nombre_parsal_is_const, nombre_parsal_const_id, base_parsal, base_parsal_is_const, base_parsal_const_id, taux_parsal, taux_parsal_is_const, taux_parsal_const_id, montant_parsal, montant_parsal_is_const, montant_parsal_const_id, taux_parpat, taux_parpat_is_const, taux_parpat_const_id, montant_parpat, montant_parpat_is_const, montant_parpat_const_id,  True, apparait_dans_bulletin, compte_debit_id, compte_credit_id, devise_id)
		rubrique = dao_rubrique.toUpdate(ref, rubrique)
		if rubrique == False: raise Exception("Erreur modification")

		rubrique = dao_rubrique.toGet(ref)
		rubrique.nombre_est_modifiable = nombre_est_modifiable
		rubrique.base_est_modifiable = base_est_modifiable
		rubrique.taux_est_modifiable = taux_est_modifiable
		rubrique.montant_est_modifiable = montant_est_modifiable
		rubrique.taux_pp_est_modifiable = taux_pp_est_modifiable
		rubrique.montant_pp_est_modifiable = montant_pp_est_modifiable
		rubrique.est_cumul = est_cumul
		rubrique.save()
		#print("Rubrique {} modifiee".format(rubrique.code))

		#Gestion des cumuls
		brut = dao_constante.toGetByCode("brut")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = brut.id, rubrique_id = rubrique.id).first()
		if cumul_brut != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = brut.id, type_operation = cumul_brut, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_brut
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_brut == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		brutcong = dao_constante.toGetByCode("brutcong")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = brutcong.id, rubrique_id = rubrique.id).first()
		if cumul_brutcong != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = brutcong.id, type_operation = cumul_brutcong, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_brutcong
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_brutcong == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		coutotsal = dao_constante.toGetByCode("coutotsal")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = coutotsal.id, rubrique_id = rubrique.id).first()
		if cumul_coutotsal != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = coutotsal.id, type_operation = cumul_coutotsal, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_coutotsal
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_coutotsal == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		coutotpat = dao_constante.toGetByCode("coutotpat")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = coutotpat.id, rubrique_id = rubrique.id).first()
		if cumul_coutotpat != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = coutotpat.id, type_operation = cumul_coutotpat, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_coutotpat
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_coutotpat == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		netpaie = dao_constante.toGetByCode("netpaie")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = netpaie.id, rubrique_id = rubrique.id).first()
		if cumul_netpaie != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = netpaie.id, type_operation = cumul_netpaie, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_netpaie
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_netpaie == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		netimpo = dao_constante.toGetByCode("netimpo")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = netimpo.id, rubrique_id = rubrique.id).first()
		if cumul_netimpo != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = netimpo.id, type_operation = cumul_netimpo, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_netimpo
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_netimpo == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		cotisal = dao_constante.toGetByCode("cotisal")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = cotisal.id, rubrique_id = rubrique.id).first()
		if cumul_cotisal != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = cotisal.id, type_operation = cumul_cotisal, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_cotisal
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_cotisal == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		cotipat = dao_constante.toGetByCode("cotipat")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = cotipat.id, rubrique_id = rubrique.id).first()
		if cumul_cotipat != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = cotipat.id, type_operation = cumul_cotipat, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_cotipat
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_cotipat == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		sous_pat = dao_constante.toGetByCode("sous_pat")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = sous_pat.id, rubrique_id = rubrique.id).first()
		if cumul_sous_pat != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = sous_pat.id, type_operation = cumul_sous_pat, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_sous_pat
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_sous_pat == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		avantur = dao_constante.toGetByCode("avantur")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = avantur.id, rubrique_id = rubrique.id).first()
		if cumul_avantur != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = avantur.id, type_operation = cumul_avantur, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_avantur
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_avantur == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		totapay = dao_constante.toGetByCode("totapay")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = totapay.id, rubrique_id = rubrique.id).first()
		if cumul_totapay != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = totapay.id, type_operation = cumul_totapay, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_totapay
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_totapay == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		totaret = dao_constante.toGetByCode("totaret")
		calcul = Model_ConstanteCalcul.objects.filter(sequence = rubrique.sequence, constante_parent_id = totaret.id, rubrique_id = rubrique.id).first()
		if cumul_totaret != 1:
			if calcul == None:
				calcul = Model_ConstanteCalcul(sequence = rubrique.sequence, constante_parent_id = totaret.id, type_operation = cumul_totaret, rubrique_id = rubrique.id)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
			else:
				calcul.type_operation = cumul_totaret
				calcul.save()
				#print("Ligne Calcul {} modifie".format(calcul.sequence))
		elif cumul_totaret == 1 and calcul != None:
				calcul.delete()
				#print("Ligne Calcul {} supprime".format(rubrique.sequence))

		return HttpResponseRedirect(reverse('module_payroll_details_rubrique', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier rubrique\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier rubrique')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_update_rubrique', args=(ref,)))

# CONSTANTES CONTROLLERS
def get_lister_constante(request):
	try:
		# droit = "LISTER_CONSTANTE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		# model = dao_constante.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_constante.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		title = "Liste des constantes"
		context ={
			'title' : title,
			'model' : model,
			'view':view,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/constante/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des constantes \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des constantes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

def get_details_constante(request, ref):
	try:
		# droit="LISTER_constante"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		model = dao_constante.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)
		context ={
			'title' : 'constante {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/constante/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details constante\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail constante')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_constante'))

def get_creer_constante(request):
	try:
		# droit="CREER__constante"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_constantes = dao_constante.toListTypeConstante()

		context = {
			'title' : 'Choisir un type de constante',
			'isPopup': isPopup,
			'utilisateur' : utilisateur,
			'type_constantes': type_constantes,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/constante/add_choose_type.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer constante\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer constante')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_constante'))

def post_creer_choix_constante(request):
	try:
		# droit="CREER__constante"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_constante = request.POST["type_constante"]
		type_constantes = dao_constante.toListTypeConstante()
		type_condition_tests = dao_constante.toListTypeConditionTest()
		type_operation_tests = dao_constante.toListTypeOperationTest()
		type_operation_calculs = dao_constante.toListTypeOperationCalcul()

		constantes = dao_constante.toList()
		rubriques = dao_rubrique.toList()

		context = {
			'title' : 'Créer une constante',
			'isPopup': isPopup,
			'type_constante': type_constante,
			'type_constantes': type_constantes,
			'type_condition_tests': type_condition_tests,
			'type_operation_tests': type_operation_tests,
			'type_operation_calculs': type_operation_calculs,
			'constantes' : constantes,
			'rubriques' : rubriques,
			'utilisateur' : utilisateur,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/constante/add.html')
		if type_constante == "1":
			template = loader.get_template('ErpProject/ModulePayroll/constante/add_type_calcul.html')
		elif type_constante == "2":
			template = loader.get_template('ErpProject/ModulePayroll/constante/add_type_test.html')
		elif type_constante == "3":
			template = loader.get_template('ErpProject/ModulePayroll/constante/add_type_tranche.html')
		elif type_constante == "8":
			template = loader.get_template('ErpProject/ModulePayroll/constante/add_type_cumul.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer constante\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer constante')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_constante'))

def post_creer_constante(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		reference = request.POST["reference"]
		code = request.POST["code"]
		description = request.POST["description"]
		type_constante = int(request.POST["type_constante"])

		if type_constante == 1:
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			constante = dao_constante.toSave(constante)
			#print("constante calcul {} cree".format(constante.code))

			list_sequence = request.POST.getlist("sequence", None)
			list_operation_select = request.POST.getlist("operation_select", None)
			list_code_input_is_const = request.POST.getlist("code_input_is_const", None)
			list_code_input = request.POST.getlist("code_input", None)
			list_code_select = request.POST.getlist("code_select", None)

			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_select = int(list_operation_select[i])

				code_input_is_const = int(list_code_input_is_const[i])
				if code_input_is_const == 0: code_input_is_const = False
				else: code_input_is_const = True
				code_input = makeFloat(list_code_input[i])
				code_select = int(list_code_select[i])
				if code_select == 0: code_select = None

				calcul = Model_ConstanteCalcul(sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, code = code_input, code_is_const = code_input_is_const, code_const_id = code_select)
				calcul.save()
				#print("Ligne Calcul {} cree".format(calcul.sequence))
		elif type_constante == 2:
			alors_input_is_const = int(request.POST["alors_input_is_const"])
			if alors_input_is_const == 0: alors_input_is_const = False
			else: alors_input_is_const = True
			alors_input = makeFloat(request.POST["alors_input"])
			alors_select = int(request.POST["alors_select"])
			if alors_select == 0: alors_select = None

			sinon_input_is_const = int(request.POST["sinon_input_is_const"])
			if sinon_input_is_const == 0: sinon_input_is_const = False
			else: sinon_input_is_const = True
			sinon_input = makeFloat(request.POST["sinon_input"])
			sinon_select = int(request.POST["sinon_select"])
			if sinon_select == 0: sinon_select = None

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			constante = dao_constante.toSave(constante)
			#print("constante test {} cree".format(constante.code))

			constante.alors = alors_input
			constante.alors_is_const = alors_input_is_const
			constante.alors_const_id = alors_select

			constante.sinon = sinon_input
			constante.sinon_is_const = sinon_input_is_const
			constante.sinon_const_id = sinon_select

			constante.save()

			list_sequence = request.POST.getlist("sequence", None)
			list_condition_select = request.POST.getlist("condition_select", None)
			list_operation_select = request.POST.getlist("operation_select", None)
			list_code_input_is_const = request.POST.getlist("code_input_is_const", None)
			list_code_input = request.POST.getlist("code_input", None)
			list_code_select = request.POST.getlist("code_select", None)
			list_valeur_input_is_const = request.POST.getlist("valeur_input_is_const", None)
			list_valeur_input = request.POST.getlist("valeur_input", None)
			list_valeur_select = request.POST.getlist("valeur_select", None)

			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_select = int(list_operation_select[i])
				condition_select = int(list_condition_select[i])

				code_input_is_const = int(list_code_input_is_const[i])
				if code_input_is_const == 0: code_input_is_const = False
				else: code_input_is_const = True
				code_input = makeFloat(list_code_input[i])
				code_select = int(list_code_select[i])
				if code_select == 0: code_select = None

				valeur_input_is_const = int(list_valeur_input_is_const[i])
				if valeur_input_is_const == 0: valeur_input_is_const = False
				else: valeur_input_is_const = True
				valeur_input = makeFloat(list_valeur_input[i])
				valeur_select = int(list_valeur_select[i])
				if valeur_select == 0: valeur_select = None

				test = Model_ConstanteTest(sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, type_condition = condition_select, code = code_input, code_is_const = code_input_is_const, code_const_id = code_select, valeur = valeur_input, valeur_is_const = valeur_input_is_const, valeur_const_id = valeur_select)
				test.save()
				#print("Ligne Test {} cree".format(test.sequence))
		elif type_constante == 3:
			base_test_input_is_const = int(request.POST["base_test_input_is_const"])
			if base_test_input_is_const == 0: base_test_input_is_const = False
			else: base_test_input_is_const = True
			base_test_input = makeFloat(request.POST["base_test_input"])
			base_test_select = int(request.POST["base_test_select"])
			if base_test_select == 0: base_test_select = None

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante, base_test = base_test_input, base_test_is_const = base_test_input_is_const, base_test_const_id = base_test_select)
			constante = dao_constante.toSave(constante)
			#print("constante Tranche {} cree".format(constante.code))

			list_sequence = request.POST.getlist("sequence", None)
			list_operation_debut = request.POST.getlist("operation_debut", None)
			list_operation_fin = request.POST.getlist("operation_fin", None)
			list_code_input_is_const = request.POST.getlist("code_input_is_const", None)
			list_code_input = request.POST.getlist("code_input", None)
			list_code_select = request.POST.getlist("code_select", None)
			list_left_input_is_const = request.POST.getlist("left_input_is_const", None)
			list_left_input = request.POST.getlist("left_input", None)
			list_left_select = request.POST.getlist("left_select", None)
			list_valeur_input_is_const = request.POST.getlist("valeur_input_is_const", None)
			list_valeur_input = request.POST.getlist("valeur_input", None)
			list_valeur_select = request.POST.getlist("valeur_select", None)

			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_debut = int(list_operation_debut[i])
				if operation_debut == 0: operation_debut = None
				operation_fin = int(list_operation_fin[i])
				if operation_fin == 0: operation_fin = None

				left_input_is_const = int(list_left_input_is_const[i])
				if left_input_is_const == 0: left_input_is_const = False
				else: left_input_is_const = True
				left_input = makeFloat(list_left_input[i])
				left_select = int(list_left_select[i])
				if left_select == 0: left_select = None

				code_input_is_const = int(list_code_input_is_const[i])
				if code_input_is_const == 0: code_input_is_const = False
				else: code_input_is_const = True
				code_input = makeFloat(list_code_input[i])
				code_select = int(list_code_select[i])
				if code_select == 0: code_select = None

				valeur_input_is_const = int(list_valeur_input_is_const[i])
				if valeur_input_is_const == 0: valeur_input_is_const = False
				else: valeur_input_is_const = True
				valeur_input = makeFloat(list_valeur_input[i])
				valeur_select = int(list_valeur_select[i])
				if valeur_select == 0: valeur_select = None

				tranche = Model_ConstanteTranche(sequence = sequence, constante_parent_id = constante.id, type_operation_debut = operation_debut, type_operation_fin = operation_fin, tranche_debut = left_input, tranche_debut_is_const = left_input_is_const, tranche_debut_const_id = left_select, tranche_fin = code_input, tranche_fin_is_const = code_input_is_const, tranche_fin_const_id = code_select, valeur = valeur_input, valeur_is_const = valeur_input_is_const, valeur_const_id = valeur_select)
				tranche.save()
				#print("Ligne tranche {} cree".format(tranche.sequence))
		elif type_constante == 4:
			valeur_input_is_const = int(request.POST["valeur_input_is_const"])
			if valeur_input_is_const == 0: valeur_input_is_const = False
			else: valeur_input_is_const = True
			valeur_input = makeFloat(request.POST["valeur_input"])
			valeur_select = int(request.POST["valeur_select"])
			if valeur_select == 0: valeur_select = None

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante, 0.0, False, None, None, valeur_input, valeur_input_is_const, valeur_const_id = valeur_select)
			constante = dao_constante.toSave(constante)
			#print("constante valeur {} cree".format(constante.code))
		elif type_constante == 5:
			rubrique_id = request.POST["rubrique_id"]
			if rubrique_id == 0: rubrique_id = None
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante, 0.0, False, None, rubrique_id)
			constante = dao_constante.toSave(constante)
			#print("constante rubrique {} cree".format(constante.code))
		elif type_constante == 6:
			fonction = request.POST["fonction"]
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			constante = dao_constante.toSave(constante)
			#print("constante predefinie {} cree".format(constante.code))
			constante.fonction = fonction
			constante.save()
		elif type_constante == 7:
			fonction = request.POST["fonction"]
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			constante = dao_constante.toSave(constante)
			#print("constante Individuelle {} cree".format(constante.code))
			constante.fonction = fonction
			constante.save()
		elif type_constante == 8:
			date_debut_cumul = None
			date_fin_cumul = None
			periode_cumul = int(request.POST["periode_cumul"])
			if "date_debut_cumul" in request.POST :
				date_debut_cumul = request.POST["date_debut_cumul"]
				date_debut_cumul = timezone.datetime(int(date_debut_cumul[6:10]), int(date_debut_cumul[3:5]), int(date_debut_cumul[0:2]))
				date_debut_cumul = int(datetime.timestamp(date_debut_cumul))
			if "date_fin_cumul" in request.POST :
				date_fin_cumul = request.POST["date_fin_cumul"]
				date_fin_cumul = timezone.datetime(int(date_fin_cumul[6:10]), int(date_fin_cumul[3:5]), int(date_fin_cumul[0:2]))
				date_fin_cumul = int(datetime.timestamp(date_fin_cumul))

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			constante = dao_constante.toSave(constante)
			#print("constante cumul {} cree".format(constante.code))
			constante.periode_cumul = periode_cumul
			constante.date_debut_cumul = date_debut_cumul
			constante.date_fin_cumul = date_fin_cumul
			constante.save()

			list_sequence = request.POST.getlist("sequence", None)
			list_operation_select = request.POST.getlist("operation_select", None)
			list_rubrique_id = request.POST.getlist("rubrique_id", None)

			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_select = int(list_operation_select[i])

				rubrique_id = int(list_rubrique_id[i])
				if rubrique_id == 0: rubrique_id = None

				cumul = Model_ConstanteCalcul(sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, rubrique_id = rubrique_id)
				cumul.save()
				#print("Ligne Cumul {} cree".format(cumul.sequence))
		elif type_constante == 9:
			date_constante = request.POST["date_constante"]
			date_constante = timezone.datetime(int(date_constante[6:10]), int(date_constante[3:5]), int(date_constante[0:2]))
			date_constante = int(datetime.timestamp(date_constante))
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			constante = dao_constante.toSave(constante)
			#print("constante Date {} cree".format(constante.code))
			constante.date_constante = date_constante
			constante.save()
		return HttpResponseRedirect(reverse('module_payroll_details_constante', args=(constante.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer constante\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer constante')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_constante'))

def get_modifier_constante(request, ref):
	try:
		# droit="MODIFIER_constante"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		model = dao_constante.toGet(ref)

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		type_constante = str(model.type_constant)
		type_constantes = dao_constante.toListTypeConstante()
		type_condition_tests = dao_constante.toListTypeConditionTest()
		type_operation_tests = dao_constante.toListTypeOperationTest()
		type_operation_calculs = dao_constante.toListTypeOperationCalcul()

		constantes = dao_constante.toList()
		rubriques = dao_rubrique.toList()

		context = {
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'isPopup': isPopup,
			'type_constante': type_constante,
			'type_constantes': type_constantes,
			'type_condition_tests': type_condition_tests,
			'type_operation_tests': type_operation_tests,
			'type_operation_calculs': type_operation_calculs,
			'constantes' : constantes,
			'rubriques' : rubriques,
			'utilisateur' : utilisateur,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/constante/update.html')
		if type_constante == "1":
			template = loader.get_template('ErpProject/ModulePayroll/constante/update_type_calcul.html')
		elif type_constante == "2":
			template = loader.get_template('ErpProject/ModulePayroll/constante/update_type_test.html')
		elif type_constante == "3":
			template = loader.get_template('ErpProject/ModulePayroll/constante/update_type_tranche.html')
		elif type_constante == "8":
			template = loader.get_template('ErpProject/ModulePayroll/constante/update_type_cumul.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier constante\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier constante')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_constante'))

def post_modifier_constante(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		reference = request.POST["reference"]
		code = request.POST["code"]
		description = request.POST["description"]
		type_constante = int(request.POST["type_constante"])

		if type_constante == 1:
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante calcul {} modifiee".format(constante.code))

			list_sequence = request.POST.getlist("sequence", None)
			list_operation_select = request.POST.getlist("operation_select", None)
			list_code_input_is_const = request.POST.getlist("code_input_is_const", None)
			list_code_input = request.POST.getlist("code_input", None)
			list_code_select = request.POST.getlist("code_select", None)

			listCalculUpdated = []
			listCalculOld = []
			calculs = Model_ConstanteCalcul.objects.filter(constante_parent_id = constante.id).all()
			for calcul in calculs:
				listCalculOld.append(calcul.id)
			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_select = int(list_operation_select[i])

				code_input_is_const = int(list_code_input_is_const[i])
				if code_input_is_const == 0: code_input_is_const = False
				else: code_input_is_const = True
				code_input = makeFloat(list_code_input[i])
				code_select = int(list_code_select[i])
				if code_select == 0: code_select = None

				calcul = Model_ConstanteCalcul.objects.filter(sequence = sequence, constante_parent_id = constante.id).first()
				if calcul == None:
					calcul = Model_ConstanteCalcul(sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, code = code_input, code_is_const = code_input_is_const, code_const_id = code_select)
					calcul.save()
					#print("Ligne Calcul {} cree".format(calcul.sequence))
				else:
					calcul = Model_ConstanteCalcul(id = calcul.id, sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, code = code_input, code_is_const = code_input_is_const, code_const_id = code_select, creation_date = calcul.creation_date)
					calcul.save()
					#print("Ligne Calcul {} modifiee".format(calcul.sequence))
					listCalculUpdated.append(calcul.id)
			#print("listCalculUpdated: {}".format(listCalculUpdated))
			# Suppression éléments qui n'existent plus
			for id in listCalculOld:
				if id not in listCalculUpdated:
					#print("calcul {} recupere".format(id))
					calcul = Model_ConstanteCalcul.objects.get(pk = id)
					calcul.delete()
					#print("calcul supprime")
		elif type_constante == 2:
			alors_input_is_const = int(request.POST["alors_input_is_const"])
			if alors_input_is_const == 0: alors_input_is_const = False
			else: alors_input_is_const = True
			alors_input = makeFloat(request.POST["alors_input"])
			alors_select = int(request.POST["alors_select"])
			if alors_select == 0: alors_select = None

			sinon_input_is_const = int(request.POST["sinon_input_is_const"])
			if sinon_input_is_const == 0: sinon_input_is_const = False
			else: sinon_input_is_const = True
			sinon_input = makeFloat(request.POST["sinon_input"])
			sinon_select = int(request.POST["sinon_select"])
			if sinon_select == 0: sinon_select = None

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante test {} modifiee".format(constante.code))

			constante.alors = alors_input
			constante.alors_is_const = alors_input_is_const
			constante.alors_const_id = alors_select

			constante.sinon = sinon_input
			constante.sinon_is_const = sinon_input_is_const
			constante.sinon_const_id = sinon_select

			constante.save()

			list_sequence = request.POST.getlist("sequence", None)
			list_condition_select = request.POST.getlist("condition_select", None)
			list_operation_select = request.POST.getlist("operation_select", None)
			list_code_input_is_const = request.POST.getlist("code_input_is_const", None)
			list_code_input = request.POST.getlist("code_input", None)
			list_code_select = request.POST.getlist("code_select", None)
			list_valeur_input_is_const = request.POST.getlist("valeur_input_is_const", None)
			list_valeur_input = request.POST.getlist("valeur_input", None)
			list_valeur_select = request.POST.getlist("valeur_select", None)

			listTestUpdated = []
			listTestOld = []
			tests = Model_ConstanteTest.objects.filter(constante_parent_id = constante.id).all()
			for test in tests:
				listTestOld.append(test.id)
			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_select = int(list_operation_select[i])
				condition_select = int(list_condition_select[i])

				code_input_is_const = int(list_code_input_is_const[i])
				if code_input_is_const == 0: code_input_is_const = False
				else: code_input_is_const = True
				code_input = makeFloat(list_code_input[i])
				code_select = int(list_code_select[i])
				if code_select == 0: code_select = None

				valeur_input_is_const = int(list_valeur_input_is_const[i])
				if valeur_input_is_const == 0: valeur_input_is_const = False
				else: valeur_input_is_const = True
				valeur_input = makeFloat(list_valeur_input[i])
				valeur_select = int(list_valeur_select[i])
				if valeur_select == 0: valeur_select = None

				test = Model_ConstanteTest.objects.filter(sequence = sequence, constante_parent_id = constante.id).first()
				if test == None :
					test = Model_ConstanteTest(sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, type_condition = condition_select, code = code_input, code_is_const = code_input_is_const, code_const_id = code_select, valeur = valeur_input, valeur_is_const = valeur_input_is_const, valeur_const_id = valeur_select)
					test.save()
					#print("Ligne Test {} cree".format(test.sequence))
				else:
					test = Model_ConstanteTest(id = test.id, sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, type_condition = condition_select, code = code_input, code_is_const = code_input_is_const, code_const_id = code_select, valeur = valeur_input, valeur_is_const = valeur_input_is_const, valeur_const_id = valeur_select, creation_date = test.creation_date)
					test.save()
					#print("Ligne Test {} modifiee".format(test.sequence))
					listTestUpdated.append(test.id)
			# Suppression éléments qui n'existent plus
			for id in listTestOld:
				if id not in listTestUpdated:
					#print("test {} recupere".format(id))
					test = Model_ConstanteTest.objects.get(pk = id)
					test.delete()
					#print("test supprime")
		elif type_constante == 3:
			base_test_input_is_const = int(request.POST["base_test_input_is_const"])
			if base_test_input_is_const == 0: base_test_input_is_const = False
			else: base_test_input_is_const = True
			base_test_input = makeFloat(request.POST["base_test_input"])
			base_test_select = int(request.POST["base_test_select"])
			if base_test_select == 0: base_test_select = None

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante, base_test = base_test_input, base_test_is_const = base_test_input_is_const, base_test_const_id = base_test_select)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante Tranche {} modifiee".format(constante.code))

			list_sequence = request.POST.getlist("sequence", None)
			list_operation_debut = request.POST.getlist("operation_debut", None)
			list_operation_fin = request.POST.getlist("operation_fin", None)
			list_code_input_is_const = request.POST.getlist("code_input_is_const", None)
			list_code_input = request.POST.getlist("code_input", None)
			list_code_select = request.POST.getlist("code_select", None)
			list_left_input_is_const = request.POST.getlist("left_input_is_const", None)
			list_left_input = request.POST.getlist("left_input", None)
			list_left_select = request.POST.getlist("left_select", None)
			list_valeur_input_is_const = request.POST.getlist("valeur_input_is_const", None)
			list_valeur_input = request.POST.getlist("valeur_input", None)
			list_valeur_select = request.POST.getlist("valeur_select", None)

			listTrancheUpdated = []
			listTrancheOld = []
			tranches = Model_ConstanteTranche.objects.filter(constante_parent_id = constante.id).all()
			for tranche in tranches:
				listTrancheOld.append(tranche.id)
			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])

				operation_debut = int(list_operation_debut[i])
				if operation_debut == 0: operation_debut = None

				operation_fin = int(list_operation_fin[i])
				if operation_fin == 0: operation_fin = None

				left_input_is_const = int(list_left_input_is_const[i])
				if left_input_is_const == 0: left_input_is_const = False
				else: left_input_is_const = True
				left_input = makeFloat(list_left_input[i])
				left_select = int(list_left_select[i])
				if left_select == 0: left_select = None

				code_input_is_const = int(list_code_input_is_const[i])
				if code_input_is_const == 0: code_input_is_const = False
				else: code_input_is_const = True
				code_input = makeFloat(list_code_input[i])
				code_select = int(list_code_select[i])
				if code_select == 0: code_select = None

				valeur_input_is_const = int(list_valeur_input_is_const[i])
				if valeur_input_is_const == 0: valeur_input_is_const = False
				else: valeur_input_is_const = True
				valeur_input = makeFloat(list_valeur_input[i])
				valeur_select = int(list_valeur_select[i])
				if valeur_select == 0: valeur_select = None

				tranche = Model_ConstanteTranche.objects.filter(sequence = sequence, constante_parent_id = constante.id).first()
				if tranche == None:
					tranche = Model_ConstanteTranche(sequence = sequence, constante_parent_id = constante.id, type_operation_debut = operation_debut, type_operation_fin = operation_fin, tranche_debut = left_input, tranche_debut_is_const = left_input_is_const, tranche_debut_const_id = left_select, tranche_fin = code_input, tranche_fin_is_const = code_input_is_const, tranche_fin_const_id = code_select, valeur = valeur_input, valeur_is_const = valeur_input_is_const, valeur_const_id = valeur_select)
					tranche.save()
					#print("Ligne tranche {} cree".format(tranche.sequence))
				else:
					tranche = Model_ConstanteTranche(id = tranche.id, sequence = sequence, constante_parent_id = constante.id, type_operation_debut = operation_debut, type_operation_fin = operation_fin, tranche_debut = left_input, tranche_debut_is_const = left_input_is_const, tranche_debut_const_id = left_select, tranche_fin = code_input, tranche_fin_is_const = code_input_is_const, tranche_fin_const_id = code_select, valeur = valeur_input, valeur_is_const = valeur_input_is_const, valeur_const_id = valeur_select, creation_date = tranche.creation_date)
					tranche.save()
					#print("Ligne tranche {} modifiee".format(tranche.sequence))
					listTrancheUpdated.append(tranche.id)
			# Suppression éléments qui n'existent plus
			for id in listTrancheOld:
				if id not in listTrancheUpdated:
					#print("tranche {} recuperee".format(id))
					tranche = Model_ConstanteTranche.objects.get(pk = id)
					tranche.delete()
					#print("tranche supprimee")
		elif type_constante == 4:
			valeur_input_is_const = int(request.POST["valeur_input_is_const"])
			if valeur_input_is_const == 0: valeur_input_is_const = False
			else: valeur_input_is_const = True
			valeur_input = makeFloat(request.POST["valeur_input"])
			valeur_select = int(request.POST["valeur_select"])
			if valeur_select == 0: valeur_select = None

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante, 0.0, False, None, None, valeur_input, valeur_input_is_const, valeur_const_id = valeur_select)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante valeur {} modifiee".format(constante.code))
		elif type_constante == 5:
			rubrique_id = request.POST["rubrique_id"]
			if rubrique_id == 0: rubrique_id = None
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante, 0.0, False, None, rubrique_id)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante rubrique {} modifiee".format(constante.code))
		elif type_constante == 6:
			fonction = request.POST["fonction"]
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante predefinie {} modifiee".format(constante.code))
			constante.fonction = fonction
			constante.save()
		elif type_constante == 7:
			fonction = request.POST["fonction"]
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante Individuelle {} modifiee".format(constante.code))
			constante.fonction = fonction
			constante.save()
		elif type_constante == 8:
			date_debut_cumul = None
			date_fin_cumul = None
			periode_cumul = int(request.POST["periode_cumul"])
			if "date_debut_cumul" in request.POST :
				date_debut_cumul = request.POST["date_debut_cumul"]
				date_debut_cumul = timezone.datetime(int(date_debut_cumul[6:10]), int(date_debut_cumul[3:5]), int(date_debut_cumul[0:2]))
				date_debut_cumul = int(datetime.timestamp(date_debut_cumul))
			if "date_fin_cumul" in request.POST :
				date_fin_cumul = request.POST["date_fin_cumul"]
				date_fin_cumul = timezone.datetime(int(date_fin_cumul[6:10]), int(date_fin_cumul[3:5]), int(date_fin_cumul[0:2]))
				date_fin_cumul = int(datetime.timestamp(date_fin_cumul))

			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante cumul {} modifiee".format(constante.code))
			constante.periode_cumul = periode_cumul
			constante.date_debut_cumul = date_debut_cumul
			constante.date_fin_cumul = date_fin_cumul
			constante.save()

			list_sequence = request.POST.getlist("sequence", None)
			list_operation_select = request.POST.getlist("operation_select", None)
			list_rubrique_id = request.POST.getlist("rubrique_id", None)

			listCumulUpdated = []
			listCumulOld = []
			cumuls = Model_ConstanteCalcul.objects.filter(constante_parent_id = constante.id).all()
			for cumul in cumuls:
				listCumulOld.append(cumul.id)
			for i in range(0, len(list_sequence)) :
				#print("Initialisation")
				sequence = int(list_sequence[i])
				operation_select = int(list_operation_select[i])

				rubrique_id = int(list_rubrique_id[i])
				if rubrique_id == 0: rubrique_id = None

				cumul = Model_ConstanteCalcul.objects.filter(sequence = sequence, constante_parent_id = constante.id).first()
				if cumul == None :
					cumul = Model_ConstanteCalcul(sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, rubrique_id = rubrique_id)
					cumul.save()
					#print("Ligne Cumul {} cree".format(cumul.sequence))
				else:
					cumul = Model_ConstanteCalcul(id = cumul.id, sequence = sequence, constante_parent_id = constante.id, type_operation = operation_select, rubrique_id = rubrique_id, creation_date = cumul.creation_date)
					cumul.save()
					#print("Ligne Cumul {} modifiee".format(cumul.sequence))
					listCumulUpdated.append(cumul.id)
			# Suppression éléments qui n'existent plus
			for id in listCumulOld:
				if id not in listCumulUpdated:
					#print("cumul {} recupere".format(id))
					cumul = Model_ConstanteCalcul.objects.get(pk = id)
					cumul.delete()
					#print("cumul supprime")
		elif type_constante == 9:
			date_constante = request.POST["date_constante"]
			date_constante = timezone.datetime(int(date_constante[6:10]), int(date_constante[3:5]), int(date_constante[0:2]))
			date_constante = int(datetime.timestamp(date_constante))
			constante = dao_constante.toCreate(auteur.id, designation, reference, code, description, type_constante)
			est_modifiee, constante = dao_constante.toUpdate(ref, constante)
			if est_modifiee == False: raise  Exception("Erreur modification")
			#print("constante Date {} modifiee".format(constante.code))
			constante.date_constante = date_constante
			constante.save()
		return HttpResponseRedirect(reverse('module_payroll_details_constante', args=(constante.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier constante\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier constante')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_update_constante', args=(ref,)))


#MODELE DE BULLETIN CONTROLLER
def get_lister_modele_bulletin(request):
	try:
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_bulletin_modele.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_bulletin_modele.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End rubrique *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'title' : 'Liste des modèles de bulletin',
			'model' : model,
			'view':view,
			'menu' : 11,
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/modele_bulletin/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER MODELE DE BULLETIN \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lister les profils de paie')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_tableau_de_bord"))

def get_creer_modele_bulletin(request):
	try:
		# droit="CREER_BULLETIN_MODELE
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False
		type_structures = dao_type_structure.toList()
		horaire_payes = dao_bulletin_modele.toListHorairePaye()
		journaux = dao_journal.toListJournauxPaie()
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		rubriques = Model_Rubrique.objects.all()

		context = {
			'title' : 'Nouveau modèle de salaire',
			'menu' : 11,
			'isPopup': isPopup,
			"modules" : modules,
			'devise_ref' : devise_ref,
			'devises' : devises,
			'type_structures' : type_structures,
			'horaire_payes' : horaire_payes,
			'journaux' : journaux,
			'rubriques' : rubriques,
			'modules' : modules,
			'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/modele_bulletin/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER MODELE DE BULLETIN \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer MODELE DE BULLETIN')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_modele_bulletin'))

@transaction.atomic
def post_creer_modele_bulletin(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		devise_id = int(request.POST["devise_id"])
		if devise_id == 0: devise_id = None
		#journal_id = request.POST["journal_id"]
		type_id = request.POST["type_id"]
		horaire_paye = request.POST["horaire_paye"]
		libelle_bulletin = request.POST["libelle_bulletin"]
		par_defaut = False
		if "par_defaut" in request.POST : par_defaut = True
		list_rubrique_id = request.POST.getlist('multi_select_rubriques[]', None)

		modele_bulletin = dao_bulletin_modele.toCreate(auteur.id, designation, None, horaire_paye, libelle_bulletin, None, devise_id, par_defaut, description)
		modele_bulletin = dao_bulletin_modele.toSave(modele_bulletin)
		#print("MODELE DE BULLETIN {} cree".format(modele_bulletin.id))

		#Ajout des règles slariales  (ManyToMany - Creation)
		#print("Nbre Ligne {}".format(len(list_rubrique_id)))
		for i in range(0, len(list_rubrique_id)):
			rubrique_id = int(list_rubrique_id[i])
			#print("rubrique_id {}".format(rubrique_id))
			rubrique = Model_Rubrique.objects.get(pk = rubrique_id)
			modele_bulletin.rubriques.add(rubrique)
			#print("LIGNE MODELE DE BULLETIN {} cree".format(modele_bulletin.id))

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_modele_bulletin',args=(modele_bulletin.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER MODELE DE BULLETIN \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post Créer MODELE DE BULLETIN')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_add_modele_bulletin'))

def get_details_modele_bulletin(request, ref):
	try:
		# droit="LISTER_BULLETIN_MODELE
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		#print(ref)
		modele_bulletin = dao_bulletin_modele.toGet(ref)
		rubriques = modele_bulletin.rubriques.all()

		context = {
			'title' : modele_bulletin.designation,
			'model' : modele_bulletin,
			'rubriques' : rubriques,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'menu' : 11,
			'modules' : modules,
			'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_PAYROLL,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur)
		}
		template = loader.get_template("ErpProject/ModulePayroll/modele_bulletin/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModulePayroll"
		monLog.error("{} :: {}::\nERREUR LORS DE POST DETAILLER MODELE DE BULLETIN \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post détailler MODELE DE BULLETIN')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_modele_bulletin'))

def get_modifier_modele_bulletin(request, ref):
	try:
		# droit="MODIFIER_MODELE_BULLETIN"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 0
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		model = dao_bulletin_modele.toGet(ref)
		type_structures = dao_type_structure.toList()
		horaire_payes = dao_bulletin_modele.toListHorairePaye()
		journaux = dao_journal.toListJournauxPaie()
		devises = dao_devise.toListDevisesActives()
		devise_ref = dao_devise.toGetDeviseReference()
		rubriques = Model_Rubrique.objects.all()

		context = {
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'rubriques' : rubriques,
			'utilisateur' : utilisateur,
			'devise_ref' : devise_ref,
			'devises' : devises,
			'type_structures' : type_structures,
			'horaire_payes' : horaire_payes,
			'journaux' : journaux,
			'actions': auth.toGetActions(modules,utilisateur),
			'modules' : modules,'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/modele_bulletin/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier structure\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier structure')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_modele_bulletin'))

@transaction.atomic
def post_modifier_modele_bulletin(request):
	ref = int(request.POST["ref"])
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		devise_id = int(request.POST["devise_id"])
		if devise_id == 0: devise_id = None
		journal_id = int(request.POST["journal_id"])
		if journal_id == 0: journal_id = None
		type_id = int(request.POST["type_id"])
		if type_id == 0: type_id = None
		horaire_paye = request.POST["horaire_paye"]
		libelle_bulletin = request.POST["libelle_bulletin"]
		par_defaut = False
		if "par_defaut" in request.POST : par_defaut = True
		list_rubrique_id = request.POST.getlist('multi_select_rubriques[]', None)

		modele_bulletin = dao_bulletin_modele.toCreate(auteur.id, designation, type_id, horaire_paye, libelle_bulletin, journal_id, devise_id, par_defaut, description)
		is_updated = dao_bulletin_modele.toUpdate(ref, modele_bulletin)
		modele_bulletin = dao_bulletin_modele.toGet(ref)

		if is_updated == False:
			raise  Exception("Erreur modification")

		#Ajout des rubriques (ManyToMany - Modification)
		rubriquesOld = modele_bulletin.rubriques.all()
		rubriquesUpdated = []
		for i in range(0, len(list_rubrique_id)):
			existe = False
			rubrique_id = int(list_rubrique_id[i])
			rubrique = Model_Rubrique.objects.get(pk = rubrique_id)
			for item in rubriquesOld:
				if item.id == rubrique.id:
					existe = True
			rubriquesUpdated.append(rubrique.id)
			# Enregistrement  nouvel élément
			if existe == False: modele_bulletin.rubriques.add(rubrique)
		# Suppression éléments qui n'existent plus
		for item in rubriquesOld:
			if item.id not in rubriquesUpdated:
				#print("rubrique {} recupere".format(item.id))
				modele_bulletin.rubriques.remove(item)
				#print("rubrique supprime")

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_modele_bulletin', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier le modele\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier le modele')
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_modele_bulletin'))

# ANALYSE PAYROLL
def get_analyse_payroll(request):
	try:
		permission_number = 424
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'title' : 'Analyse PayRoll',
			#'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'modules' : modules,
			'sous_modules': sous_modules,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 5,
		}
		template = loader.get_template('ErpProject/ModulePayroll/bulletin/analyse.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des declaration nominatives \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des declaration nominatives')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

# DECLATION NOMINATIVE CONTROLLERS
#ADD
def get_add_declaration_nominative(request):
	permission_number = 394
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		context = {
			'title' : 'Générer La Declaration nominative mensuelle des salaires et des cotisations',
			"devises" : dao_devise.toListDevisesActives(),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			"utilisateur" : utilisateur,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModulePayroll/declaration_nominative/generate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('ERREUR LORS DU POST GENERATE')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la générationdu reporting")
		return HttpResponseRedirect(reverse('module_payroll_tableau'))


def post_generated_declaration_nominative(request):
	permission_number = 394
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		utilisateur = identite.utilisateur(request)
		context = post_printing_model_declaration_nominative(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModulePayroll/declaration_nominative/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('ERREUR LORS DU POST GENERATE')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la générationdu reporting")
		return HttpResponseRedirect(reverse('module_payroll_add_declaration_nominative'))

# ETAT IMPOT CONTROLLERS
#Generate
def get_add_etat_impot(request):
	permission_number = 393
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	try:
		context = {
			'title' : 'Générer Etat des impôts sur salaire',
			"lots": dao_lot_bulletin.toList(),
			"devises" : dao_devise.toListDevisesActives(),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			"utilisateur" : utilisateur,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 7
		}
		template = loader.get_template("ErpProject/ModulePayroll/etat_impot/generate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('ERREUR LORS DU POST GENERATE')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la générationdu reporting")
		return HttpResponseRedirect(reverse('module_payroll_tableau'))

def post_generated_etat_impot(request):
	permission_number = 393
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		utilisateur = identite.utilisateur(request)
		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModulePayroll/etat_impot/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('ERREUR LORS DU POST GENERATE')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la générationdu reporting")
		return HttpResponseRedirect(reverse('module_payroll_add_etat_impot'))

#Prets
def get_lister_prets_payroll(request):
	try:
		permission_number = 610
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_pret.toListPret()

		#Filtrage des regles + fixation sur les prêts de l'employé uniquement
		model = dao_model.toListModel(dao_pret.toListPret(), permission_number, groupe_permissions, identite.utilisateur(request))

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)

		context = {
			'title' : "Liste des prêts",
			'model' : model,
			'view': view,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'sous_modules':sous_modules,
			"modules" : modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModulePayroll/pret/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau'))

def get_creer_pret_payroll(request):
	try:
		permission_number = 611
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Demande de prêt',
			'reference': dao_pret.toGenerateNumero(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			'rubriques': dao_rubrique.toListRubriques(),
			'employes' : dao_employe.toListEmployes(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModulePayroll/pret/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_pret'))


def post_valider_pret_payroll(request):
	try:
		# droit="CREER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 611
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		#Test de la validité de la date en fonction de l'activation d'une période dans un module
		#if not auth.toPostValidityDate(var_module_id, request.POST["date_facturation"]): return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, msg ="La période sélectionnée n'est pas activée")

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL


		reference = request.POST["reference"]
		date_premiere_echeance = request.POST["date_premiere_echeance"]
		devise_id = request.POST["devise_id"]
		montant = makeFloat(request.POST["montant"])
		employe_id = request.POST["employe_id"]
		nbre_mensualite = request.POST["nbre_mensualite"]
		taux_interet = request.POST["taux_interet"]
		taux_valeur = float(taux_interet) / 100
		description = request.POST["description"]
		rubrique_id = request.POST["rubrique_id"]

		devise = dao_devise.toGetDevise(devise_id)
		rubrique = dao_rubrique.toGetRubrique(rubrique_id)


		demande_pret = {
			'reference': reference,
			'date_premiere_echeance': date_premiere_echeance,
			'montant': montant,
			'employe_id': employe_id,
			'devise_id': devise_id,
			'nbre_mensualite': nbre_mensualite,
			'taux_interet': taux_interet,
			'employe': auteur.nom_complet,
			'devise': devise,
			'description': description,
			'rubrique_id':rubrique_id,
			'rubrique': rubrique
		}

		lignes_remboursement = []

		montant_anterieur = 0
		for i in range(0, int(nbre_mensualite)) :
			date_remboursement = timezone.datetime(int(date_premiere_echeance[6:10]), int(date_premiere_echeance[3:5]), int(date_premiere_echeance[0:2])) + relativedelta(months = i)
			montant = float(montant)
			mensualite = (montant + (montant * taux_valeur)) / int(nbre_mensualite)
			ligne = {
				'date_remboursement': date_remboursement,
				'montant_pret': montant,
				'devise_iso': devise.symbole_devise,
				'mensualite': mensualite,
				'prelevement_anterieur': montant_anterieur,
				'montant_du_prelevement': mensualite,
				'reste_a_recouvrer': montant - montant_anterieur - mensualite
			}
			montant_anterieur += mensualite
			lignes_remboursement.append(ligne)


		context = {
			'title' : 'Confirmation demande de prêt',
			'demande_pret' : demande_pret,
			'lignes_remboursement' : lignes_remboursement,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"utilisateur" : utilisateur,
			'modules' : modules,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModulePayroll/pret/validate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		#messages.error(request,"Veuillez sélectionner une taxe applicable")
		return HttpResponseRedirect(reverse("module_payroll_add_pret"))


@transaction.atomic
def post_creer_pret_payroll(request) :
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)

		#print("resues", request.POST)

		reference = request.POST["reference"]
		date_premiere_echeance = request.POST["date_premiere_echeance"]
		devise_id = request.POST["devise_id"] if (request.POST["devise_id"] and request.POST["devise_id"] != 'None' ) else None
		montant = makeFloat(request.POST["montant"])
		employe_id = request.POST["employe_id"] if (request.POST["employe_id"] and request.POST["employe_id"] != 'None' ) else None
		nbre_mensualite = request.POST["nbre_mensualite"]
		description = request.POST["description"]
		taux_interet = request.POST["taux_interet"]
		taux_valeur = float(taux_interet) / 100
		rubrique_id = request.POST["rubrique_id"] if (request.POST["rubrique_id"] and request.POST["rubrique_id"] != 'None' ) else None

		#conversion de la date
		date_premiere_echeance = timezone.datetime(int(date_premiere_echeance[6:10]), int(date_premiere_echeance[3:5]), int(date_premiere_echeance[0:2]))

		pret = dao_pret.toCreatePret(reference,montant, devise_id, nbre_mensualite, employe_id, description, date_premiere_echeance, taux_valeur, rubrique_id)
		pret = dao_pret.toSavePret(auteur, pret)

		#Initialisation du workflow expression
		wkf_task.initializeWorkflow(auteur,pret)

		transaction.savepoint_commit(sid)

		#print("Pret cree ID {}".format(pret.id))
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_payroll_detail_pret', args=(pret.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		transaction.savepoint_rollback(sid)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du prêt")
		return HttpResponseRedirect(reverse('module_payroll_add_pret'))


def get_modifier_pret_payroll(request, ref):
	try:
		permission_number = 612
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		pret = dao_pret.toGetPret(id)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % pret.reference,
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			'employes' : dao_employe.toListEmployes(),
			'model' : pret,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModulePayroll/pret/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU MODIFIER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Modifier')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_pret'))

def post_modifier_pret_payroll(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		employe_id = request.POST["employe_id"]
		devise_id = request.POST["devise_id"]
		montant = request.POST["montant"]
		tranche_mensuelle = request.POST["tranche_mensuelle"]
		date_pret = request.POST["date_pret"]
		delai = request.POST["delai"]

		#conversion de la date
		date_pret = timezone.datetime(int(date_pret[6:10]), int(date_pret[3:5]), int(date_pret[0:2]))
		delai = timezone.datetime(int(delai[6:10]), int(delai[3:5]), int(delai[0:2]))

		pret = dao_pret.toCreatePret(montant, devise_id, tranche_mensuelle, employe_id, delai, date_pret)
		is_done = dao_pret.toUpdatePret(id, pret)

		if is_done == True :
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_payroll_detail_pret', args=(id,)))
		else : return HttpResponseRedirect(reverse('module_payroll_update_pret', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFIER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_update_pret', args=(id,)))

def get_details_pret_payroll(request, ref):
	try:
		permission_number = 610
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		pret = dao_pret.toGetPret(ref)
		#reste_a_payer_periode = dao_pret.toGetResttoPayToDate(pret.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,pret)

		lignes_remboursement = []

		montant = pret.montant
		nbre_mensualite = pret.nbre_mensualite
		taux_valeur = pret.taux_interet
		date_premiere_echeance = pret.date_premiere_echeance
		devise = pret.devise

		montant_anterieur = 0
		for i in range(0, int(nbre_mensualite)) :
			#date_remboursement = timezone.datetime(int(date_premiere_echeance[6:10]), int(date_premiere_echeance[3:5]), int(date_premiere_echeance[0:2])) + relativedelta(months = i)
			date_remboursement = date_premiere_echeance + relativedelta(months = i)
			montant = float(montant)
			mensualite = (montant + (montant * taux_valeur)) / int(nbre_mensualite)
			ligne = {
				'date_remboursement': date_remboursement,
				'montant_pret': montant,
				'devise_iso': devise.symbole_devise,
				'mensualite': mensualite,
				'prelevement_anterieur': montant_anterieur,
				'montant_du_prelevement': mensualite,
				'reste_a_recouvrer': montant - montant_anterieur - mensualite
			}
			montant_anterieur += mensualite
			#print("lignes", ligne)
			lignes_remboursement.append(ligne)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : pret.reference,
			'model' : pret,
			'lignes_remboursement': lignes_remboursement,
			'lignes_paiement_pret': dao_ligne_paiement_pret.toListLignePaiementOfPret(ref),
			'paiements_internes' : dao_paiement_interne.toListPaiementsOfPret(ref),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			#"can_create" : dao_droit.toGetDroitRole('CREER_pret_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_pret_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_pret_DE_MESURE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModulePayroll/pret/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_pret'))

#Paiement Interne
def get_lister_paiement_internes(request):
	try:
		# droit="LISTER_PAIEMENT_INTERNE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 205
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		# model = dao_paiement_interne.toListPaiements()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_paiement_interne.toListPaiements(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		context = {
			'title' : "Liste des paiements internes",
			'model' : model,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModulePayroll/paiement_interne/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE PAIEMENT INTERNE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_tableau_de_bord'))

def get_details_paiement_interne(request, ref):
	try:
		# droit="LISTER_PAIEMENT_INTERNE"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 205
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response
		ref = int(ref)
		paiement = dao_paiement_interne.toGetPaiement(ref)
		context = {
			'title' : paiement.designation,
			'model' : paiement,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			'modules' : modules,'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModulePayroll/paiement_interne/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL PAIEMENT INTERNE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('MODULE_PAYROLL_list_paiement_interne'))

@transaction.atomic
def post_paiement_allocation(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		dossier_id = request.POST["dossier_id"]

		list_devise_id = request.POST.getlist('devise_id', None)
		list_montant = request.POST.getlist("montant", 0.0)
		list_conge_id = request.POST.getlist('conge_id', None)
		#print(len(list_devise_id))
		#print(len(list_montant))
		#print(len(list_conge_id))
		for i in range(0, len(list_conge_id)) :
			conge_id = int(list_conge_id[i])
			devise_id = int(list_devise_id[i])
			montant = makeFloat(list_montant[i])

			paiement = dao_paiement_interne.toCreatePaiement(montant, devise_id, None, dossier_id, None, conge_id, None, auteur.id)
			paiement = dao_paiement_interne.toSavePaiement(paiement)
			#print("Paiement interne cree avec ID {}".format(paiement.id))
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin', args=(dossier_id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		transaction.savepoint_rollback(sid)
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('MODULE_PAYROLL_list_paiement_interne'))

@transaction.atomic
def post_paiement_pret(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		dossier_id = request.POST["dossier_id"]

		list_devise_id = request.POST.getlist('devise_id', None)
		list_montant = request.POST.getlist("montant", 0.0)
		list_pret_id = request.POST.getlist('pret_id', None)
		#print(len(list_devise_id))
		#print(len(list_montant))
		#print(len(list_pret_id))
		for i in range(0, len(list_pret_id)) :
			pret_id = int(list_pret_id[i])
			devise_id = int(list_devise_id[i])
			montant = makeFloat(list_montant[i])

			paiement = dao_paiement_interne.toCreatePaiement(montant, devise_id, pret_id, dossier_id, None, None, None, auteur.id)
			paiement = dao_paiement_interne.toSavePaiement(paiement)
			#print("Paiement interne cree avec ID {}".format(paiement.id))
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_payroll_details_lotbulletin', args=(dossier_id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		transaction.savepoint_rollback(sid)
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('MODULE_PAYROLL_list_paiement_interne'))

#FONCTION POUR GENERER LE RAPPORT DE LA BALANCE DE PAIE
def get_generer_balance_paie(request):

	permission_number = 535
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer la balance de paie',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/Balance_paie/generate.html")
	return HttpResponse(template.render(context, request))

#FONCTION POUR GENERER LE RAPPORT DE BULLETIN INDIVIDUEL
def get_generer_Bulletin_individuel(request):


	permission_number = 542
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response


	context = {
		'title' : 'Générer le bulletin individuel',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/Bulletin_individuel/generate.html")
	return HttpResponse(template.render(context, request))


#FONCTION POUR GENERER LE RAPPORT DE PAIEMENT DE SALAIRE
def get_generer_Paiement_salaire(request):

	permission_number = 540
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	array = []
	years = dao_dossier_paie.toListDossierPaie()
	for item in years:
		array.append(item.annee)

	list_years = np.array(array)
	list_years = np.unique(list_years)
	#Ici on va trier les années pour garder uniquement celle qui a plusieurs occurence

	context = {
		'title' : 'Générer le paiement de salaire',
		"banques" : dao_banque.toListBank(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7,'list_years':list_years
	}
	template = loader.get_template("ErpProject/ModulePayroll/Paiement_de_salaire/generate.html")
	return HttpResponse(template.render(context, request))


#FONCTION POST GENERATE PAIEMENTDES SALAIRES
def post_generer_Paiement_salaire(request):
	permission_number = 540
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		utilisateur = identite.utilisateur(request)
		context = post_printing_model_paiement_salaire(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModulePayroll/Paiement_de_salaire/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print('ERREUR LORS DU POST GENERATE')
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la génération du reporting")
		return HttpResponseRedirect(reverse('module_payroll_generate_Paiement_salaire'))

def post_printing_model_paiement_salaire(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_PAYROLL):
	'''fonction de traitement de calcul pour extraction paiement par caisse'''
	auteur = utilisateur
	exercice = int(request.POST["exercice"])
	periode = int(request.POST["periode"])
	banque = int(request.POST["banque_id"])
	data=[]

	# personnel = Model_Employe.objects.filter(model_person_ptr_id = employe.id).first()
	# matricule = personnel.profilrh.matricule
	month = int(request.POST["periode"])
	month = datetime.date(1900, month, 1).strftime('%B')
	# print(month)
	banking = Model_Banque.objects.get(pk = banque)
	comptebanquaires = Model_CompteBanque_Employe.objects.filter(banque_id = banque)
	somme = 0
	for item in comptebanquaires:
		# print('***** Debut Iteration cycle*****', item)
		employe = Model_Employe.objects.filter(profilrh = item.profilrh.id).first()
		# print(f'*****employe {employe}')
		if not employe:
			pass

		person = dao_employe.toGetEmploye(employe.id)
		# print(f'*****person {person}')
		bulletins = Model_Bulletin.objects.filter(employe__id = person.id,lot__date_fin__month=periode,lot__date_fin__year=exercice).first()
		if not bulletins:
			pass
		else:
			# print(f'*****bulletins {bulletins}')
			montant_net = Model_ItemBulletin.objects.filter(bulletin__id = bulletins.id, rubrique__reference = "NETAPAY").first()
			# print(f'*****Item bulletins {montant_net}')
			somme += montant_net.montant
			# print(f'*****somme {somme}')
			models = {
				'employe_name': employe.nom,
				'employe_firstname': employe.prenom,
				'matricule': employe.profilrh.matricule,
				'numero_compte': item.numero_compte,
				'Montant_pay': montant_net.montant
			}
			data.append(models)

	context = {
		'title' : 'Paiement des Salaires',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		"utilisateur" : utilisateur,
		'models': data,
		'sommes': somme,
		'exercice': exercice,'periode':periode,
		'banking': banking,
		'month': month,
		'exercice_id' : int(request.POST["exercice"]),
		'periode_id': int(request.POST["periode"]),
		'banque_id' : int(request.POST["banque_id"]),
	}
	return context


#FONCTION POUR GENERER LE RAPPORT DE PRELEVEMENT A TERME SUR SALAIRE
def get_generer_Prelevement_sur_salaire(request):
	permission_number = 541
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le prelevement à terme sur salaire',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/Prelevement_sur_salaire/generate.html")
	return HttpResponse(template.render(context, request))



#FONCTION POUR GENERER LA DETERMINATION DE LA PROVISION POUR CONGE A PAYER
def get_generer_Provision_conge(request):

	permission_number = 536
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response



	context = {
		'title' : 'Générer la provision de congé',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/Provision_conge/generate.html")
	return HttpResponse(template.render(context, request))



#FONCTION POUR GENERER LE RAPPORT DE PROVISION DE DEPART DE RETRAITE
def get_generer_Provision_depart_retraite(request):

	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response



	context = {
		'title' : 'Générer la provision de depart de retraite',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/Provision_depart_retraite/generate.html")
	return HttpResponse(template.render(context, request))

#FONCTION JOURNAL COMP
def get_generer_journal_comp(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le Journal Comparatif',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/Journal/generate.html")
	return HttpResponse(template.render(context, request))


def post_generer_journal_comp(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'JOURNAL COMPARATIF',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	template = loader.get_template("ErpProject/ModulePayroll/Journal/generated.html")
	return HttpResponse(template.render(context, request))


#FONCTION POUR GENERER LE RAPPORT DE JOURNAL GLOBAL
def get_generer_journal_global(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	array = []
	years = dao_dossier_paie.toListDossierPaie()
	for item in years:
		array.append(item.annee)
	#Ici on va trier les années pour garder uniquement celle qui a plusieurs occurence
	list_years = np.array(array)
	list_years = np.unique(list_years)
	context = {
		'title' : 'JOURNAL GLOBAL DE PAIE',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	'list_years':list_years
	}
	template = loader.get_template("ErpProject/ModulePayroll/Journal_Global/generate.html")
	return HttpResponse(template.render(context, request))

def post_generer_journalglobal_paie(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		utilisateur = identite.utilisateur(request)
		context = post_printing_model_jglobal(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModulePayroll/Journal_Global/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print('ERREUR LORS DU POST GENERATE')
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la génération du reporting")
		return HttpResponseRedirect(reverse('module_payroll_get_generer_journal_global'))

def post_printing_model_jglobal(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_PAYROLL):
	'''fonction de traitement de calcul pour extraction paiement par caisse'''
	auteur = utilisateur
	exercice = int(request.POST["exercice"])
	periode = int(request.POST["periode"])
	month = int(request.POST["periode"])
	data = []
	month = datetime.date(1900, month, 1).strftime('%B')
	bulletins = Model_Bulletin.objects.filter(lot__date_fin__month=periode,lot__date_fin__year=exercice)
	for item in bulletins:
		# print(f'----iteration:: {item} employe {item.employe}')
		if item.employe != None:
			montant_net = Model_ItemBulletin.objects.filter(bulletin__id = item.id, rubrique__reference = "NETAPAY").first()
			item_baseImpo = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "BASEIMPO").first()
			item_Irpp = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "IRPP").first()
			item_Salbrut = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SALBRUT ").first()
			item_taxunsal = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "TAXUNSAL").first()
			item_salbase = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SALBASE").first()
			item_sursale = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SURSAL").first()
			item_anc = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIMANC").first()
			item_fonc = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIFONCT").first()
			item_log = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRILOG").first()
			item_diplom = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIDIPLOM").first()
			item_dom = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIDOM").first()
			item_eloign = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIELOIGN").first()
			item_caisse = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRICAISSE").first()
			item_risque = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIRISQUE").first()
			item_allconge = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "ALLOCONGE").first()
			item_astr = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIASTR").first()
			item_paie = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIPAIE").first()
			item_salbrute = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SALBRUT").first()
			item_cnss = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "CNSS").first()
			item_mutuel = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "COTARPCE").first()
			item_repr = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIREPR").first()
			item_indtrans = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "INDTRANSP").first()
			item_repr = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "CMPLTRANSP").first()
			item_cpttrans = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRIREPR").first()
			item_pret = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PRET").first()

			personnel = dao_employe.toGetEmploye(item.employe.id)
			models ={
				'nom_complet':item.employe.nom_complet,
				'matricule':personnel.profilrh.matricule,
				'genre':personnel.profilrh.genre,
				'fonction':item.fonction,
				'grade':item.grade,
				'echelon':personnel.categorie_employe,
				'dept':item.departemant,
				'end_date':item.lot.date_fin,
				'sal_base':item_salbase.montant,
				'sur_salaire':item_sursale.montant,
				'prim_anc':item_anc.montant,
				'prim_fonct':item_fonc.montant,
				'prim_lgt':item_log.montant,
				'prim_diplome':item_diplom.montant,
				'prim_domesticite':item_dom.montant,
				'prim_eloignement':item_eloign.montant,
				'prim_caisse':item_caisse.montant,
				'prim_risque':item_risque.montant,
				'allocation_conge':item_allconge.montant,
				'prim_astrinte':item_astr.montant,
				'prim_paie':item_paie.montant,
				'sal_brut':item_salbrute.montant,
				'cnss':item_cnss.montant,
				'ac_irpp':item_Irpp.montant,
				'prel_mutuel': item_mutuel.montant,
				'prim_rep': item_repr.montant,
				'indemn_trans': item_indtrans.montant,
				'cplt_indemn_trans': item_cpttrans.montant,
				'pret': item_pret.montant,
				'net_a_payer': montant_net.montant
			}
			data.append(models)
		else:
			pass
	context = {
		'title' : f'Journal Global de Paie: {month} {exercice}',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		"utilisateur" : utilisateur,
		"exercice" : (request.POST["exercice"]),
		"periode" : (request.POST["periode"]),
		"models" : data,
	}
	return context


def to_print_journal_global(request):
	try:
		permission_number = 537
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_jglobal(request, utilisateur, modules, sous_modules)
		# template = loader.get_template("ErpProject/ModulePayroll/declaration_nominative/generated.html")
		return weasy_print_bulletin("ErpProject/ModulePayroll/reporting/journal_global.html", "journalGlobal.pdf", context, request)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)





#FONCTION  POUR GENERER LE RAPPORT DE CAISSE
def get_generer_caisse(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	array = []
	years = dao_dossier_paie.toListDossierPaie()
	for item in years:
		array.append(item.annee)
	#Ici on va trier les années pour garder uniquement celle qui a plusieurs occurence
	list_years = np.array(array)
	list_years = np.unique(list_years)
	context = {
		'title' : 'Générer rapport de la Caisse',
		"employes" : dao_personne.toListPersonnesActif(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7,'list_years':list_years
	}
	template = loader.get_template("ErpProject/ModulePayroll/Caisse/generate.html")
	return HttpResponse(template.render(context, request))


#FONCTION POST GENERATE CAISSE
def post_generer_caisse(request):
	permission_number = 535
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		utilisateur = identite.utilisateur(request)
		context = post_printing_model_caisse(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModulePayroll/Caisse/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print('ERREUR LORS DU POST GENERATE')
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la génération du reporting")
		return HttpResponseRedirect(reverse('module_payroll_generate_caisse'))

def post_printing_model_caisse(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_PAYROLL):
	'''fonction de traitement de calcul pour extraction paiement par caisse'''
	auteur = utilisateur
	exercice = int(request.POST["exercice"])
	periode = int(request.POST["periode"])
	employe = int(request.POST["employe_id"])

	month = int(request.POST["periode"])
	month = datetime.date(1900, month, 1).strftime('%B')
	# print(month)

	employe = dao_employe.toGetEmploye(employe)
	bulletins = Model_Bulletin.objects.filter(employe_id = employe, lot__date_fin__month=periode,lot__date_fin__year=exercice).first()
	montant_net = Model_ItemBulletin.objects.filter(bulletin__id = bulletins.id, rubrique__reference = "NETAPAY").first()
	context = {
		'title' : f'CAISSE Siege ARPCE: {month} {exercice}',
		"employe" : employe.nom_complet,
		"matricule" : employe.profilrh.numero_ss,
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		"utilisateur" : utilisateur,
		"exercice" : (request.POST["exercice"]),
		"periode" : (request.POST["periode"]),
		"models" : bulletins,
		'montant_net': montant_net.montant,
		"employe_id": int(request.POST["employe_id"])
	}
	return context

#FONCTION POST GENERATE BULLETIN INDIVIDUEL
def post_generer_bulletin_individuel(request):
	permission_number = 542
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'BULLETIN INDIVIDUEL',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	template = loader.get_template("ErpProject/ModulePayroll/Bulletin_individuel/genered.html")
	return HttpResponse(template.render(context, request))



#FONCTION  POUR GENERER LE RAPPORT DE BULLETIN DE PAIE
def get_generer_Bulletin_paie(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Générer le Bulletin de paie',
		"devises" : dao_devise.toListDevisesActives(),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
		'menu' : 7
	}
	template = loader.get_template("ErpProject/ModulePayroll/bulletin_paie/generate.html")
	return HttpResponse(template.render(context, request))

#FONCTION POST GENERATE BALANCE DE PAIE
def post_generer_balance_paie(request):
	permission_number = 535
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response
	try:
		context = post_printing_model_balance_paie(request, utilisateur, modules, sous_modules)
		template = loader.get_template("ErpProject/ModulePayroll/Balance_paie/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModulePayroll'
		monLog.error("{} :: {}::\nERREUR LORS DU POST GENERATE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('ERREUR LORS DU POST GENERATE')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la générationdu reporting")
		return HttpResponseRedirect(reverse('get_generer_balance_paie'))

#FONCTION POST GENERATE DETERMINATION DE LA PROVISION POUR CONGE A PAYER
def post_generer_provision_conge(request):
	permission_number = 536
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'Détermination de la provision pour congésà payer (Acquis en 2019 et à payer en 2020)',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	template = loader.get_template("ErpProject/ModulePayroll/Provision_conge/generated.html")
	return HttpResponse(template.render(context, request))

#FONCTION POST GENERATE PROVISION DE DEPART A LA RETRAITE
def post_generer_Provision_depart_retraite(request):
	permission_number = 537
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	context = {
		'title' : 'PROVISION DE DEPART A LA RETRAITE EN 2018',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	template = loader.get_template("ErpProject/ModulePayroll/Provision_depart_retraite/generated.html")
	return HttpResponse(template.render(context, request))



#FONCTION POST GENERATE PRELEVEMENT A TERME SUR SALAIRES
def post_generer_Prelevement_sur_salaire(request):
	permission_number = 541
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	date_periode = request.POST["date_periode"]
	date_send = request.POST["date_periode"]
	devise_id = request.POST["devise_id"]

	date_periode = timezone.datetime(int(date_periode[6:10]), int(date_periode[3:5]), int(date_periode[0:2]))
	prets = dao_pret.toListPretAvailableOnDate(date_periode)

	context = {
		'title' : 'PRELEVEMENTS A TERME SUR SALAIRES',
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model': prets,
		# 'date_periode': date_periode,
		'devise_id': devise_id,
		"modules" : modules ,
		'date_periode': date_send,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	template = loader.get_template("ErpProject/ModulePayroll/Prelevement_sur_salaire/generated.html")
	return HttpResponse(template.render(context, request))

def to_Prelevement_sur_salaire_print(request):
	permission_number = 541
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

	if response != None:
		return response

	date_periode = request.POST["date_periode"]

	devise_id = request.POST["devise_id"]

	date_periode = timezone.datetime(int(date_periode[6:10]), int(date_periode[3:5]), int(date_periode[0:2]))
	prets = dao_pret.toListPretAvailableOnDate(date_periode)



	context = {
		'title' : 'PRELEVEMENTS A TERME SUR SALAIRES',
		'organisation': dao_organisation.toGetMainOrganisation(),
		'model': prets,
		'date_periode':date_periode,
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	# template = loader.get_template("ErpProject/ModulePayroll/Prelevement_sur_salaire/generated.html")
	return weasy_print_bulletin("ErpProject/ModulePayroll/reporting/Prelevement_sur_salaire.html", "Prelevement_sur_salaire.pdf", context, request)


#MODEL GENERIQUE DE PRINT
def post_printing_model_etat(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_PAYROLL):
	'''fonction de traitement de calcul pour extraction d'un diplôme'''
	auteur = utilisateur
	exercice = int(request.POST["exercice"])
	periode = int(request.POST["periode"])

	lot = Model_LotBulletins.objects.filter(date_fin__month=periode,date_fin__year=exercice,est_regulier=True).first()
	bulletins = Model_Bulletin.objects.filter(lot_id = lot.id).all()
	models = []
	for item in bulletins:
		base_irpp = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "BASEIMPO").first()
		if item_bull != None: base_irpp = item_bull.montant

		montant_irpp = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "IRPP").first()
		if item_bull != None: montant_irpp = item_bull.montant

		base_tus = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SALBRUT ").first()
		if item_bull != None: base_tus = item_bull.montant

		montant_tus = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "TAXUNSAL").first()
		if item_bull != None: montant_tus = item_bull.montant_parpat

		total_employeur = montant_tus
		total_impots = makeFloat(montant_tus)  + makeFloat(montant_irpp)
		model = {
			"employe" : item.employe.nom_complet,
			"niu" : "",
			"base_irpp" : base_irpp,
			"montant_irpp" : montant_irpp,
			"base_tus" : base_tus,
			"montant_tus" : montant_tus,
			"total_employeur" : total_employeur,
			"total_impots" : total_impots
		}
		models.append(model)


	context = {
		'title' : 'Etat des impôts sur salaires',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"lot" : lot ,
		"bulletins" : bulletins,
		"models":models,
		"exercice" : exercice,
		"periode" : periode,
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	return context

def post_printing_model_declaration_nominative(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_PAYROLL):
	'''fonction de traitement de calcul pour extraction d'un diplôme'''
	auteur = utilisateur
	exercice = int(request.POST["exercice"])
	periode = int(request.POST["periode"])

	lot = Model_LotBulletins.objects.filter(date_fin__month=periode,date_fin__year=exercice,est_regulier=True).first()
	bulletins = Model_Bulletin.objects.filter(lot_id = lot.id).all()
	models = []
	i = 1
	for item in bulletins:
		salbrut = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "TOTGAIN").first()
		if item_bull != None: salbrut = item_bull.montant

		salbrutimpo = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SALBRUT").first()
		if item_bull != None: salbrutimpo = item_bull.montant

		base_pvid = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "BASEPVID ").first()
		if item_bull != None: base_pvid = item_bull.montant

		base_atmp = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "BASEATMAF").first()
		if item_bull != None: base_atmp = item_bull.montant

		cnss_pat = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "PARTPATRON").first()
		if item_bull != None: cnss_pat = item_bull.montant_parpat

		cnss_sal = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "CNSS").first()
		if item_bull != None: cnss_sal = item_bull.montant

		cnss_af = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "ALLFAM").first()
		if item_bull != None: cnss_af = item_bull.montant_parpat

		cnss_atmp = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "CNACCTRMALPRO").first()
		if item_bull != None: cnss_atmp = item_bull.montant_parpat

		total_af_atmp = makeFloat(cnss_af)  + makeFloat(cnss_atmp) + makeFloat(cnss_pat)  + makeFloat(cnss_sal)
		employe = Model_Employe.objects.get(pk = item.employe.id)
		model = {
			"id" : i,
			"employe" : employe.nom_complet,
			"matricule" : employe.profilrh.numero_ss,
			"salbrut" : salbrut,
			"salbrutimpo" : salbrutimpo,
			"base_pvid" : base_pvid,
			"base_atmp" : base_atmp,
			"cnss_pat" : cnss_pat,
			"cnss_sal" : cnss_sal,
			"cnss_af" : cnss_af,
			"cnss_atmp" : cnss_atmp,
			"total_af_atmp" : total_af_atmp
		}
		models.append(model)
		i = i + 1


	context = {
		'title' : 'DECLARATION NOMINATIVE MENSUELLE DES SALAIRES ET DES COTISATIONS',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"lot" : lot ,
		"bulletins" : bulletins,
		"models":models,
		"exercice" : exercice,
		"periode" : periode,
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	return context

def post_printing_model_balance_paie(request, utilisateur, modules, sous_modules, enum_module = ErpModule.MODULE_PAYROLL):
	'''fonction de traitement de calcul pour extraction d'un diplôme'''
	auteur = utilisateur
	exercice = int(request.POST["exercice"])
	periode = int(request.POST["periode"])

	lot = Model_LotBulletins.objects.filter(date_fin__month=periode,date_fin__year=exercice,est_regulier=True).first()
	bulletins = Model_Bulletin.objects.filter(lot_id = lot.id).all()
	models = []
	for item in bulletins:
		base_irpp = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "BASEIMPO").first()
		if item_bull != None: base_irpp = item_bull.montant

		montant_irpp = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "IRPP").first()
		if item_bull != None: montant_irpp = item_bull.montant

		base_tus = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "SALBRUT ").first()
		if item_bull != None: base_tus = item_bull.montant

		montant_tus = 0
		item_bull = Model_ItemBulletin.objects.filter(bulletin_id = item.id, rubrique__reference = "TAXUNSAL").first()
		if item_bull != None: montant_tus = item_bull.montant_parpat

		total_employeur = montant_tus
		total_impots = makeFloat(montant_tus)  + makeFloat(montant_irpp)
		model = {
			"employe" : item.employe.nom_complet,
			"niu" : "",
			"base_irpp" : base_irpp,
			"montant_irpp" : montant_irpp,
			"base_tus" : base_tus,
			"montant_tus" : montant_tus,
			"total_employeur" : total_employeur,
			"total_impots" : total_impots
		}
		models.append(model)


	context = {
		'title' : 'Balance de la paie',
		'organisation': dao_organisation.toGetMainOrganisation(),
		"lot" : lot ,
		"bulletins" : bulletins,
		"models":models,
		"exercice" : exercice,
		"periode" : periode,
		"modules" : modules ,
		"utilisateur" : utilisateur,
		'sous_modules': sous_modules,
		"module" : ErpModule.MODULE_PAYROLL,
	}
	return context

def to_print_journal_comparatif(request):
	try:
		permission_number = 537
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModulePayroll/reporting/journal.html", "journal.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)



def to_print_balance_paie(request):
	try:
		permission_number = 394
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModulePayroll/reporting/Balance_paie.html", "balance.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def to_print_declaration_nom(request):
	try:
		permission_number = 394
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_declaration_nominative(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModulePayroll/reporting/declaration_nominative.html", "declaration_nominative.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def to_print_etat_impot(request):
	try:
		permission_number = 393
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModulePayroll/reporting/etat_impot.html", "etat_impot.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)


def to_print_paiement_sal(request):
	try:
		permission_number = 540
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_paiement_salaire(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModulePayroll/reporting/Paiement_salaire.html", "Paiement_de_salaire.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def to_print_prelevement_salaire(request):
	try:
		permission_number = 541
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		# template = loader.get_template("ErpProject/ModulePayroll/Paiement_de_salaire/generated.html")
		return weasy_print("ErpProject/ModulePayroll/reporting/Prelevement_sur_salaire.html", "prelevement_salaire.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def to_print_provision_conge(request):
	try:
		permission_number = 536
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		# template = loader.get_template("ErpProject/ModulePayroll/Provision_conge/generated.html")
		return weasy_print("ErpProject/ModulePayroll/reporting/Provision_conge.html", "Provision_conge.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def to_print_provision_depart_retrt(request):
	try:
		permission_number = 537
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		# template = loader.get_template("ErpProject/ModulePayroll/Provision_depart_retraite/generated.html")
		return weasy_print("ErpProject/ModulePayroll/reporting/Provision_depart_retraite.html", "Provision_depart_retraite.pdf", context)
		# return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def to_print_provision_depart_caisse_virement(request):
	try:
		permission_number = 537
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		# template = loader.get_template("ErpProject/ModulePayroll/Provision_depart_retraite/generated.html")
		return weasy_print("ErpProject/ModulePayroll/reporting/caisse_virement.html", "caisse_virement.pdf", context)
		# return HttpResponse(template.render(context, request))
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)



def to_print_caisse(request):
	try:
		permission_number = 535
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		context = post_printing_model_caisse(request, utilisateur, modules, sous_modules)
		return weasy_print("ErpProject/ModulePayroll/reporting/Caisse.html", "Caisse.pdf", context)
	except Exception as e:
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

def to_print_bulletin_individuel(request):
	try:
		permission_number = 542
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = post_printing_model_etat(request, utilisateur, modules, sous_modules)
		# template = loader.get_template("ErpProject/ModulePayroll/Bulletin_individuel/genered.html")
		return weasy_print("ErpProject/ModulePayroll/reporting/Bulletin_individuel.html", "bulletin_individuel.pdf", context)
	except Exception as e:
		print(e)
		return auth.toReturnFailed(request, inspect.getframeinfo(inspect.currentframe()).function, module, e)

#FONCTION POST GENERATE BULLETIN DE PAIE
def post_generer_Bulletin_paie(request, ref):
	try:
		permission_number = 541
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		bulletin = dao_bulletin.toGet(ref)
		item_bulletins = dao_item_bulletin.toGetItemOfBulletin(bulletin.id)
		employe = dao_employe.toGetEmploye(bulletin.employe_id)

		context = {
			'title' : 'BULLETIN DE SALAIRE',
			'model' : bulletin,
			'item_bulletins' : item_bulletins,
			'employe': employe,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			"utilisateur" : utilisateur,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
		}
		template = loader.get_template("ErpProject/ModulePayroll/bulletin_paie/generated.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bulletin'))

#FONCTION POST GENERATE BULLETIN DE PAIE
def post_printing_Bulletin_paie(request, ref):
	try:
		permission_number = 542
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		ref = int(ref)
		bulletin = dao_bulletin.toGet(ref)
		item_bulletins = dao_item_bulletin.toGetItemOfBulletin(bulletin.id)
		employe = dao_employe.toGetEmploye(bulletin.employe_id)

		context = {
			'title' : 'BULLETIN DE SALAIRE',
			'model' : bulletin,
			'item_bulletins' : item_bulletins,
			'employe': employe,
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			"utilisateur" : utilisateur,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
		}
		# template = loader.get_template("ErpProject/ModulePayroll/bulletin_paie/generated.html")
		# return HttpResponse(template.render(context, request))
		return weasy_print_bulletin("ErpProject/ModulePayroll/bulletin_paie/printing_bulletin.html", "Bulletin_Salaire.pdf", context, request)
	except Exception as e:
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_bulletin'))



def get_lister_dossier_paie(request):
	# droit="LISTER_EXERCICE_BUDGETAIRE"
	# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
	permission_number = 608
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


	if response != None:
		return response

	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_dossier_paie.toListDossierPaie(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"

	#Pagination
	model = pagination.toGet(request, model)

	dossier_en_cours = dao_dossier_paie.toGetActiveDossierPaie()


	context ={
		'title' : 'Période de paie',
		'model' : model,
		'dossier_en_cours':dossier_en_cours,
		'dossier_paie_actif': dao_dossier_paie.toGetActiveDossierPaie(),
		'mois': dao_mois_annee.toListMoisAnnee(),
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'view' : view,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'sous_modules': sous_modules,
		'module' : ErpModule.MODULE_PAYROLL,
		'menu' : 1}
	template = loader.get_template('ErpProject/ModulePayroll/dossier_paie/list.html')
	return HttpResponse(template.render(context, request))


@transaction.atomic
def post_creer_dossier_paie(request):
	sid = transaction.savepoint()
	try:
		#print("post_creer_ouverture_exercice")

		auteur = identite.utilisateur(request)
		annee = request.POST["annee"]
		mois = request.POST["mois"]
		designation = request.POST["designation"]
		reference = request.POST["reference"]
		type = "TOUS"
		est_regulier = True
		date_dossier = timezone.datetime(int(annee), int(mois), int("01"))
		date_debut = timezone.datetime(int(annee), int(mois), int("01"))
		last_day = calendar.monthrange(int(annee), int(mois))[1]
		date_fin = timezone.datetime(int(annee), int(mois), int(last_day))

		dossier_find = dao_dossier_paie.toGetDossierPaieByDesignation(mois, annee)
		if dossier_find:
			messages.add_message(request, messages.ERROR, "La période saisie existe déja!")
			return HttpResponseRedirect(reverse('module_payroll_list_dossier_paie'))

		dossier_paie = dao_dossier_paie.toCreateDossierPaie(mois, annee, True, False)
		dossier_paie = dao_dossier_paie.toSaveDossierPaie(auteur, dossier_paie)

		lot_regulier = dao_lot_bulletin.toCreate(auteur.id, designation, None, type, reference, date_dossier, dossier_paie_id = dossier_paie.id, est_regulier = est_regulier)
		lot_regulier = dao_lot_bulletin.toSave(lot_regulier)
		lot_regulier.date_debut = date_debut
		lot_regulier.date_fin = date_fin
		lot_regulier.type_modele = 1
		lot_regulier.save()

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		#return HttpResponse('<script type="text/javascript">window.close();</script>')
		return HttpResponseRedirect(reverse('module_payroll_list_dossier_paie'))
	except Exception as e:
		#print("ERREUR POST OUVERTURE COMPTABLE")
		#print(e)
		transaction.savepoint_rollback(sid)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_payroll_list_dossier_paie"))


def get_details_dossier_paie(request, ref):
	try:
		# droit="LISTER_constante"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit,request)
		permission_number = 608
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)


		if response != None:
			return response

		ref = int(ref)
		model = dao_dossier_paie.toGetDossierPaie(ref)
		lots = dao_lot_bulletin.toListLotBulletinFromDossierPaie(ref) #Liste des lots
		temp_ecritures_comptables = []
		lots = dao_lot_bulletin.toListLotBulletinFromDossierPaie(ref)
		temp_ecritures_comptables = dao_temp_ecriture_comptable.toListEcrituresComptablesOfDossierPaie(ref)


		#print("temp_ecritures_comptables", temp_ecritures_comptables)
		montant_credit = 0
		montant_debit = 0

		if temp_ecritures_comptables:
			for item in temp_ecritures_comptables:
				montant_credit = montant_credit + item.montant_credit
				montant_debit += item.montant_debit

		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)
		context ={
			'title' : 'Période de paie {}'.format(model),
			'model' : model,
			'lots_bulletin': lots,
			'utilisateur' : utilisateur,
			"historique": historique,
			'montant_credit':montant_credit,
			'montant_debit': montant_debit,
			'temp_ecritures_comptables':temp_ecritures_comptables,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules': sous_modules,
			'module' : ErpModule.MODULE_PAYROLL,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModulePayroll/dossier_paie/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details paie\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail Dossier paie')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_payroll_list_dossier_paie'))


#Json lançant le calcul de la paie
def post_calcul_paie(request):
	try:
		print('****CALCUL TASK')
		data = []
		data_employe = []
		lot_bulletin_id = int(request.GET["ref"])
		auteur = identite.utilisateur(request)

		lot_bulletin = dao_lot_bulletin.toGet(lot_bulletin_id)
		#deleting all old bulletin
		lot_bulletin.lot_of_this_bulletins.all().delete()
		for ligne in lot_bulletin.lignes.all():
			print(f'employe: {ligne.employe_id}')
			item = {
				'employe_id': ligne.employe_id
			}
			data_employe.append(item)


		task = dao_task.toProcessCalculPaie(auteur.id, lot_bulletin.id, data_employe, lot_bulletin.dossier_paie_id)
		print(f'****CALCUL {task}')
		if task:
			item = {'task_id': task.id,}
		else:
			item = {'task_id': task.id}

		data.append(item)
		return JsonResponse(data, safe=False)

	except Exception as e:
		print("erreur",e )
		return JsonResponse([], safe=False)


def get_progress(request, task_id):
	result = AsyncResult(task_id)
	response_data = {
		'state': result.state,
		'details': result.info,
	}
	return HttpResponse(json.dumps(response_data), content_type='application/json')


#Json lançant le calcul de la paie
def post_cloture_dossier_paie(request):
	try:
		data = []
		ref = int(request.GET["ref"])
		is_done = dao_dossier_paie.toClotureDossierPaie(ref)
		item = { 'status': is_done }

		data.append(item)
		#print("data", data)
		return JsonResponse(data, safe=False)


	except Exception as e:
		#print("erreur",e )
		return JsonResponse([], safe=False)


# CONFIGURATION CONTROLLER
def get_modifier_parametre_payroll(request):
	try:
		permission_number = 613
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		rubriques = dao_rubrique.toListRubriques()
		comptes = dao_compte.toListComptes()

		tx_cnss =  dao_constante.toGetByCode("txcnss")
		if tx_cnss == None : tx_cnss = 0.0
		else : tx_cnss = tx_cnss.valeur

		nbre_jrs_travail = dao_constante.toGetByCode("jrtrav")
		if nbre_jrs_travail == None : nbre_jrs_travail = 0.0
		else : nbre_jrs_travail = nbre_jrs_travail.valeur

		nbre_jrs_conge = dao_constante.toGetByCode("jrconge")
		if nbre_jrs_conge == None : nbre_jrs_conge = 0.0
		else : nbre_jrs_conge = nbre_jrs_conge.valeur

		config_payroll = dao_config_payroll.toGetMainConfigPayroll()

		#print("FIN AFFETACTION")

		context = {
			'title' : 'Paramètrage des comptes',
			'rubriques': rubriques,
			'comptes': comptes,
			'config_payroll': config_payroll,
			"tx_cnss" : tx_cnss,
			"nbre_jrs_travail" : nbre_jrs_travail,
			"nbre_jrs_conge" : nbre_jrs_conge,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_PAYROLL,
			'menu' : 10
		}
		template = loader.get_template("ErpProject/ModulePayroll/configuration/index.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR CONFIGURATION")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_comptabilite_tableau_de_bord"))



@transaction.atomic
def post_modifier_parametre_payroll(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		tx_cnss_value = makeFloat(request.POST["tx_cnss"])
		nbre_jrs_travail_value = makeFloat(request.POST["nbre_jrs_travail"])
		nbre_jrs_conge_value = makeFloat(request.POST["nbre_jrs_conge"])
		nbre_mensualite_pret = makeFloat(request.POST["nbre_mensualite_pret"])
		taux_interet = makeFloat(request.POST["taux_interet"])

		config_payroll = dao_config_payroll.toCreateConfigPayroll(tx_cnss_value, nbre_jrs_travail_value, nbre_mensualite_pret, taux_interet,)
		config_payroll = dao_config_payroll.toUpdateOrSaveConfigPayroll(config_payroll)


		list_rubrique_id = request.POST.getlist('rubrique_id', None)
		list_compte_debit_id = request.POST.getlist("compte_debit_id", None)
		list_compte_credit_id = request.POST.getlist("compte_credit_id", None)

		tx_cnss =  dao_constante.toGetByCode("txcnss")
		if tx_cnss != None :
			tx_cnss.valeur = tx_cnss_value
			tx_cnss.save()

		nbre_jrs_travail = dao_constante.toGetByCode("jrtrav")
		if nbre_jrs_travail != None :
			nbre_jrs_travail.valeur = nbre_jrs_travail_value
			nbre_jrs_travail.save()

		nbre_jrs_conge = dao_constante.toGetByCode("jrconge")
		if nbre_jrs_conge != None :
			nbre_jrs_conge.valeur = nbre_jrs_conge_value
			nbre_jrs_conge.save()



		for i in range(0, len(list_rubrique_id)) :
			rubrique_id = int(list_rubrique_id[i])
			compte_debit_id = int(list_compte_debit_id[i])
			compte_credit_id = int(list_compte_credit_id[i])

			if compte_credit_id == 0: compte_credit_id = None
			if compte_debit_id == 0: compte_debit_id = None

			rubrique = dao_rubrique.toUpdateCompteComptable(rubrique_id, compte_debit_id, compte_credit_id)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_payroll_modifier_configuration'))
	except Exception as e:
		#print("ERREUR")
		#print(e)
		#messages.error(request,e)
		messages.add_message(request, messages.ERROR, "L'opération a échoué")
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_payroll_modifier_configuration'))


@transaction.atomic
def post_generer_ecriture_comptable(request):
	sid = transaction.savepoint()
	try:
		data = []
		item1 = { 'status': True }
		auteur = identite.utilisateur(request)
		ref = int(request.GET["ref"])
		dossier_paie = dao_dossier_paie.toGetDossierPaie(ref)
		#print("lot", lot)
		#lot = dao_lot_bulletin.toGetLotBulletinSoumisFromDossierPaie(dossier_paie.id)
		lots = dao_lot_bulletin.toListLotBulletinFromDossierPaie(dossier_paie.id)
		journal = dao_journal.toGetJournalDivers()
		#print("journal", journal)
		date_piece = timezone.now()
		#ON UTILISERA DIRECTEMENT LE LOT BULLETIN EN LIEU ET PLACE DE PIECE COMPTABLE

		#piece_comptable = dao_piece_comptable.toCreatePieceComptable(lot.designation, lot.reference, 0, journal.id, date_piece,lot_bulletin_id = lot.id)
		#piece_comptable = dao_piece_comptable.toSavePieceComptable(auteur, piece_comptable)
		bulletins = [] #dao_bulletin.toListOfDossier(lot.id)
		ecritures_credit = []
		ecritures_debit = []

		for lot in lots:
			#on efface les ecritures précédentes
			dao_temp_ecriture_comptable.toDeleteEcritureComptableOfDossierPaie(dossier_paie.id)
			bulletins.extend(dao_bulletin.toListOfDossier(lot.id))
			for bulletin in bulletins:
				items = dao_item_bulletin.toGetItemOfBulletin(bulletin.id)
				for item in items:
					if item.rubrique.compte_credit_id:
						ecriture = {
						"id" : item.rubrique.compte_credit_id,
						"libelle" : item.rubrique.compte_credit.designation,
						"compte" : "%s %s" % (item.rubrique.compte_credit.numero, item.rubrique.compte_credit.designation),
						"montant" : bulletin.net_a_payer,
						"centre_cout_id": None,
						}
						ecritures_credit.append(ecriture)
					if item.rubrique.compte_debit_id:
						ecriture = {
						"id" : item.rubrique.compte_debit_id,
						"libelle" : item.rubrique.compte_debit.designation,
						"compte" : "%s %s" % (item.rubrique.compte_debit.numero, item.rubrique.compte_debit.designation),
						"montant" : bulletin.net_a_payer,
						"centre_cout_id": None,
						}
						ecritures_debit.append(ecriture)

		#print("ecritures_credit", ecritures_credit)
		#print("ecritures_debit", ecritures_debit)
		ecritures_credit = dao_temp_ecriture_comptable.toAgregateEcritureComptable(ecritures_credit)
		ecritures_debit  = dao_temp_ecriture_comptable.toAgregateEcritureComptable(ecritures_debit)

		#print("ecritures_credit 2", ecritures_credit)
		#print("ecritures_debit 2", ecritures_debit)

		for ecriture in ecritures_credit:
			ecriture_credit = dao_temp_ecriture_comptable.toCreateEcritureComptable(ecriture['libelle'], 0, ecriture['montant'], ecriture['id'], None, None, None, dossier_paie_id = dossier_paie.id)
			ecriture_credit = dao_temp_ecriture_comptable.toSaveEcritureComptable(ecriture_credit)
			ecriture_credit.save()

		for ecriture in ecritures_debit:
			ecriture_debit = dao_temp_ecriture_comptable.toCreateEcritureComptable(ecriture['libelle'], ecriture['montant'], 0, ecriture['id'], None, None, dossier_paie_id = dossier_paie.id)
			ecriture_debit = dao_temp_ecriture_comptable.toSaveEcritureComptable(ecriture_debit)
			ecriture_debit.save()

		#print("bulletin", bulletin)
		auteur = identite.utilisateur(request)



		data.append(item1)
		transaction.savepoint_commit(sid)
		return JsonResponse(data, safe=False)


	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print("erreur",e )
		return JsonResponse([], safe=False)


#Json lançant l'activation du lot bulletin
def post_activer_lot_bulletin(request):
	try:
		data = []
		ref = int(request.GET["ref"])
		is_done = dao_lot_bulletin.toSetLotBulletinActifOfDossierPaie(ref)
		item = { 'status': is_done }

		data.append(item)
		return JsonResponse(data, safe=False)

	except Exception as e:
		#print("erreur",e )
		return JsonResponse([], safe=False)