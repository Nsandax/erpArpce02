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
from ErpBackOffice.utils.print import weasy_print
import os
import pandas as pd
import calendar
import base64
from ModulePayroll.dao.dao_ligne_paiement_pret import dao_ligne_paiement_pret
from django.db import transaction
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_place import dao_place
from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.models import Model_Dependant, Model_ItemProfilPaye, Model_ItemStructureSalariale, Model_StatusRH, Model_StructureSalariale, Model_TypeStructure, Model_CategorieRegle, Model_RegleSalariale
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.dao.dao_paiement_interne import dao_paiement_interne
from ErpBackOffice.dao.dao_document import dao_document
from locale import atof, setlocale, LC_NUMERIC
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId, makeStringFromFloatExcel, makeInt, makeIntId
from ErpBackOffice.dao.dao_model import dao_model
import numpy as np
from dateutil.relativedelta import relativedelta
from ModuleRessourcesHumaines.dao.dao_requete_competence import dao_requete_competence
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation

from ModuleRessourcesHumaines.dao.dao_lieu_travail import dao_lieu_travail
from ModuleRessourcesHumaines.dao.dao_profil_paie import dao_profil_paie
from ModuleRessourcesHumaines.dao.dao_rib import dao_rib
from ModuleRessourcesHumaines.dao.dao_compte_bancaire_employe import dao_compte_banque_employe
from ModuleRessourcesHumaines.dao.dao_profil import dao_profil
from ModuleRessourcesHumaines.dao.dao_tranche_bareme import dao_tranche_bareme
from ModuleRessourcesHumaines.dao.dao_type_resultat import dao_type_resultat
from ModuleRessourcesHumaines.dao.dao_type_calcul import  dao_type_calcul
from ModuleRessourcesHumaines.dao.dao_categorie_element import dao_categorie_element
from ModuleRessourcesHumaines.dao.dao_type_element_bulletin import dao_type_element_bulletin
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_type_unite_fonctionnelle import dao_type_unite_fonctionnelle
from ModuleRessourcesHumaines.dao.dao_bareme import dao_bareme
from ModuleRessourcesHumaines.dao.dao_element_bulletin import dao_element_bulletin
from ModuleRessourcesHumaines.dao.dao_lot_bulletin import dao_lot_bulletin
from ModuleRessourcesHumaines.dao.dao_demande_achat import dao_demande_achat
from ModuleRessourcesHumaines.dao.dao_bulletin import dao_bulletin
from ModuleRessourcesHumaines.dao.dao_StatusDesignationEmploye import dao_StatusDesignationEmploye
from ModulePayroll.dao.dao_config_payroll import dao_config_payroll
from ModuleRessourcesHumaines.dao.dao_item_bulletin import dao_item_bulletin
from ErpBackOffice.dao.dao_wkf_historique_lotbulletin import dao_wkf_historique_lotbulletin
from ErpBackOffice.dao.dao_wkf_historique_bulletin import dao_wkf_historique_bulletin
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation
from ModuleRessourcesHumaines.dao.dao_ligne_demande_achat import dao_ligne_demande_achat
from ModuleRessourcesHumaines.dao.dao_requete_demande import dao_requete_demande
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_poste import dao_poste
from ModuleRessourcesHumaines.dao.dao_pret import dao_pret
from ModuleRessourcesHumaines.dao.dao_conge import dao_conge
from ModuleRessourcesHumaines.dao.dao_dependant import dao_dependant
from ModuleRessourcesHumaines.dao.dao_formation import dao_formation
from ModuleRessourcesHumaines.dao.dao_fonction import dao_fonction
#from ModuleRessourcesHumaines.dao.dao_analyse import dao_analyse
from ModulePayroll.dao.dao_structure_salariale import dao_structure_salariale
from ModulePayroll.dao.dao_type_structure import dao_type_structure
from ModuleRessourcesHumaines.dao.dao_categorie_regle import dao_categorie_regle
from ModuleRessourcesHumaines.dao.dao_regle_salariale import dao_regle_salariale
from ModuleRessourcesHumaines.dao.dao_rubrique import dao_rubrique
from ModuleConversation.dao.dao_notif import dao_notif
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ModulePayroll.dao.dao_bulletin_modele import dao_bulletin_modele
from ModuleRessourcesHumaines.dao.dao_classification_pro import dao_classification_professionnelle
from ModulePayroll.dao.dao_bulletin_modele import dao_bulletin_modele
from ModuleConversation.dao.dao_notification import dao_notification
from ErpBackOffice import models
from ModuleRessourcesHumaines import serializer
from rest_framework import viewsets
from ModuleRessourcesHumaines.dao.dao_dossier_social import dao_dossier_social

from ModuleRessourcesHumaines.dao.dao_categorie_employe import dao_categorie_employe
from ModuleRessourcesHumaines.dao.dao_syndicat import dao_syndicat
from ModuleRessourcesHumaines.dao.dao_ligne_syndicat import dao_ligne_syndicat
from ModuleRessourcesHumaines.dao.dao_ligne_formation import dao_ligne_formation
from ModuleRessourcesHumaines.dao.dao_evaluation import dao_evaluation
from ModuleRessourcesHumaines.dao.dao_mobilite import dao_mobilite
from ModuleRessourcesHumaines.dao.dao_mobilite_employe import dao_mobilite_employe
from ModuleRessourcesHumaines.dao.dao_type_mobilite import dao_type_mobilite
from ModuleRessourcesHumaines.dao.dao_emploi import dao_emploi
from ModuleRessourcesHumaines.dao.dao_type_diplome import dao_type_diplome
from ModuleRessourcesHumaines.dao.dao_diplome import dao_diplome
from ModuleRessourcesHumaines.dao.dao_ligne_competence import dao_ligne_competence
from ModuleRessourcesHumaines.dao.dao_vehicule import dao_vehicule

from ModuleRessourcesHumaines.dao.dao_ligne_competence import dao_ligne_competence
from ModuleRessourcesHumaines.dao.dao_ligne_releve import dao_ligne_releve
from ModuleRessourcesHumaines.dao.dao_projet_professionnel import dao_projet_professionnel

from ModuleRessourcesHumaines.dao.dao_type_evenement_social import dao_type_evenement_social
from ModuleRessourcesHumaines.dao.dao_recrutement_interne import dao_recrutement_interne

from ModuleRessourcesHumaines.dao.dao_requete import dao_requete
from ModuleRessourcesHumaines.dao.dao_ligne_requete import dao_ligne_requete
from ModuleRessourcesHumaines.dao.dao_ordre_de_mission import dao_ordre_de_mission
from ModuleRessourcesHumaines.dao.dao_ligne_ordre_de_mission import dao_ligne_ordre_de_mission
from ModuleRessourcesHumaines.dao.dao_type_status import dao_type_status


from ModuleBudget.dao.dao_centre_cout import dao_centre_cout
from ModuleBudget.dao.dao_ligne_budgetaire import dao_ligne_budgetaire

from ErpBackOffice.utils.auth import auth
from ErpBackOffice.utils.wkf_task import wkf_task
from ErpBackOffice.utils.endpoint import endpoint
from ModuleRessourcesHumaines.dao.dao_banque import dao_banque

# ANALYSE DAO
from ModuleRessourcesHumaines.dao.dao_analyse_formation import dao_analyse_formation
from ModuleRessourcesHumaines.dao.dao_analyse_mobilite import dao_analyse_mobilite
from ModuleRessourcesHumaines.dao.dao_analyse_indices import dao_analyse_indices
from ModuleRessourcesHumaines.dao.dao_analyse_mouvement_personnel import dao_analyse_mouvement_personnel

from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleComptabilite.dao.dao_compte import dao_compte
from ModuleComptabilite.dao.dao_ecriture_comptable import dao_ecriture_comptable
from ModuleComptabilite.dao.dao_journal import dao_journal

from ModuleRessourcesHumaines.dao.dao_categorieDesignation import dao_categorieDesignation
from ModuleRessourcesHumaines.dao.dao_EchelonDesignation import dao_EchelonDesignation
from ModuleRessourcesHumaines.dao.dao_StatusDesignationEmploye import dao_StatusDesignationEmploye
#Pagination
from ErpBackOffice.utils.pagination import pagination
#POUR LOGGING
import logging, inspect
monLog = logging.getLogger('logger')
module= "ModuleRessourcesHumaines"
var_module_id = 10

# Create your views here.

# Tableau de board
def get_dashboard(request):
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(10, request)

	if response != None:
		return response

	#WAY OF NOTIFCATION
	module_name = "MODULE_RESSOURCES_HUMAINES"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()
	#print("way")
	#print(temp_notif_count)
	#END WAY
	NombreEmploye = dao_employe.toListEmployes().count()
	NombreDepart = dao_unite_fonctionnelle.toListUniteFonctionnelle().count()
	NombreConge = dao_conge.toListConge().count()
	# NombreFormation = dao_formation.toListFormation().count()
	# NombreBulletinPaie = dao_bulletin.toList().count()
	# NombreProjetPro = dao_projet_professionnel.toListProjet_professionnel().count()
	# NombreCalculPaie = dao_syndicat.toListSyndicat().count()
	# NombreRecru = dao_recrutement_interne.toListRecrutement_interne().count()
	# ListeCongo = dao_conge.toListConge()
	# ListeFormation = dao_formation.toListFormation()
	# ListSyndicat = dao_syndicat.toListSyndicat()[:4]
	# Listerecru = dao_recrutement_interne.toListRecrutement_interne()[:4]
	# ListNumberCongebyMonth,ListeQueryConge = dao_conge.ListeNumberCongeByMunth()

	#ANALYSE MOBILITE INTERNE
	# List_Agent_by_Mobilite_year = dao_analyse_mobilite.toCount_Agent_by_Mobilite_year()
	# ListMobiliteByCategorie = dao_analyse_mobilite.toCountMobiliteByCategorie()
	# Part_Recru_by_Mobilite, Nombre_recru_via_mobilite = dao_analyse_mobilite.toGet_Part_Recru_by_Mobilite()
	# Mouvement_Perso = dao_analyse_mobilite.toMouvement_Personnel()
	# Taux_de_Mobilite, Nombre_Recru = dao_analyse_mobilite.taux_Mobilite_interne()
	# recrutement_total_mobilite = dao_analyse_mobilite.toGet_Nombre_recrutement_mobilite()
	# recrutement_total_year = dao_analyse_mobilite.toGet_Nombre_recrutement_Total()

	# Recru_Post_vacant_year = dao_recrutement_interne.toGet_Recru_by_year()

	#ANALYSE FORMATION
	# Taux_formation = dao_analyse_formation.toGet_taux_depart_formation_by_categorie()
	# Taux_formation_Direction = dao_analyse_formation.toGet_taux_depart_formation_by_Direction()
	# Nombre_Agent = dao_analyse_formation.toGet_Agent_Categorie_Formation()

	#ANALYSE INDICES
	# Tx_formation_pro = dao_analyse_indices.toGet_training_prof_family()

	#Total
	# Traitement Taux de mobilite
	# Value_Mobilite = []
	# for item in Taux_de_Mobilite.values():
	# 	Value_Mobilite.append(item)

	# Traitement Mouvement Personnel
	# keys_Mouvement_P = []
	# values_Mouvement_P = []
	# for cle in Mouvement_Perso.keys():
	# 	keys_Mouvement_P.append(cle)

	# for valeur in Mouvement_Perso.values():
	# 	values_Mouvement_P.append(valeur)

	# Traitement Mobilité par Categorie
	# keys_Mobilitie = []
	# values_Mobilitie = []
	# for cle in ListMobiliteByCategorie.keys():
	# 	keys_Mobilitie.append(cle)

	# for valeur in ListMobiliteByCategorie.values():
	# 	values_Mobilitie.append(valeur)

	# # Traitement Mobilité des Agents par year
	# keys_Year = []
	# values_Mobilite_Year = []
	# for cle in List_Agent_by_Mobilite_year.keys():
	# 	keys_Year.append(cle)


	# for value in List_Agent_by_Mobilite_year.values():
	# 	values_Mobilite_Year.append(value)


	# ordreM = dao_ordre_de_mission.toListOrdre_de_mission().count()

	# Traitement Part Recrutement de Mobilite by Year
	# Keys_recru_year = []
	# valuer_recru_year = []
	# for cle in Part_Recru_by_Mobilite.keys():
	# 	Keys_recru_year.append(cle)

	# for val in Part_Recru_by_Mobilite.values():
	# 	valuer_recru_year.append(val)

	# # Traitement Recrutement sur le post vacant
	# Keys_recru_post_year = []
	# valuer_recru_post_year = []
	# for cle in Recru_Post_vacant_year.keys():
	# 	Keys_recru_post_year.append(cle)

	# for val in Recru_Post_vacant_year.values():
	# 	valuer_recru_post_year.append(val)

	# Traitement Taux de Formation
	# Keys_Taux_formation = []
	# valeur_Taux_formation = []
	# for cle in Taux_formation.keys():
	# 	Keys_Taux_formation.append(cle)
	# for val in Taux_formation.values():
	# 	valeur_Taux_formation.append(val)


	#Traitement Taux de formation Direction
	# Keys_Taux_formation_direct = []
	# valeur_Taux_formation_direct = []
	# for cle in Taux_formation_Direction.keys():
	# 	Keys_Taux_formation_direct.append(cle)
	# for val in Taux_formation_Direction.values():
	# 	valeur_Taux_formation_direct.append(val)

	# Traitement Nombre d'Agents
	# keys_Agent = []
	# val_Agent = []
	# for cle in Nombre_Agent.keys():
	# 	keys_Agent.append(cle)
	# for val in Nombre_Agent.values():
	# 	val_Agent.append(val)

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Tableau de Bord',
		'temp_notif_count':temp_notif_count,
		'temp_notif_list':temp_notif_list,
		#'model' : model,
		'modules':modules,
		'sous_modules':sous_modules,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'modules':modules,
		'sous_modules':sous_modules,
		'NombreEmploye' : NombreEmploye,
		'NombreDepart' : NombreDepart,
		'NombreConge' : NombreConge,
		# 'NombreFormation' : NombreFormation,
		# 'NombreBulletinPaie' : NombreBulletinPaie,
		# 'NombreProjetPro' : NombreProjetPro,
		# 'NombreCalculPaie' : NombreCalculPaie,
		# 'NombreRecru' : NombreRecru,
		# 'ListeConge' : ListeCongo[:4],
		# 'ListeFormation' : ListeFormation[:3],
		# 'ListeFormationComplet':ListeFormation,
		# 'ListSyndicat' : ListSyndicat,
		# 'Listerecru' : Listerecru,
		# 'ListNumberCongebyMonth': ListNumberCongebyMonth,
		# 'ListeQueryConge': ListeQueryConge,
		# 'ordreM': ordreM,
		# 'keys_Mobilitie': keys_Mobilitie,
		# 'values_Mobilitie': values_Mobilitie,
		# 'ListMobiliteByCategorie': ListMobiliteByCategorie,
		# 'keys_Year': keys_Year,
		# 'values_Mobilite_Year': values_Mobilite_Year,
		# 'Keys_recru_year': Keys_recru_year,
		# 'valuer_recru_year': valuer_recru_year,
		# 'keys_Mouvement_P': keys_Mouvement_P,
		# 'values_Mouvement_P': values_Mouvement_P,
		# 'Keys_recru_post_year' : Keys_recru_post_year,
		# 'valuer_recru_post_year': valuer_recru_post_year,
		# 'Keys_Taux_formation': Keys_Taux_formation,
		# 'valeur_Taux_formation': valeur_Taux_formation,
		# 'Keys_Taux_formation_direct': Keys_Taux_formation_direct,
		# 'valeur_Taux_formation_direct': valeur_Taux_formation_direct,
		# 'keys_Agent': keys_Agent,
		# 'val_Agent': val_Agent,
		# 'Value_Mobilite':Value_Mobilite,
		# 'Nombre_recru_via_mobilite':Nombre_recru_via_mobilite,
		# 'Nombre_Recru': Nombre_Recru,
		# 'Tx_formation_pro':Tx_formation_pro
	}
	# template = loader.get_template('ErpProject/ModuleRessourcesHumaines/dashbord.html')
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/index.html')
	return HttpResponse(template.render(context, request))

#Overviews :
	#Formation
def get_overview_rapport(request):
	permission_number = 447
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	#WAY OF NOTIFCATION
	module_name = "MODULE_RESSOURCES_HUMAINES"

	#ANALYSE MOBILITE INTERNE
	ListMobiliteByCategorie = dao_analyse_mobilite.toCountMobiliteByCategorie()
	#ANALYSE FORMATION
	Taux_formation = dao_analyse_formation.toGet_taux_depart_formation_by_categorie()
	Taux_formation_Direction = dao_analyse_formation.toGet_taux_depart_formation_by_Direction()

	#ANALYSE INDICES
	taux_entre = dao_analyse_indices.toGet_Taux_entree()
	taux_sortie = dao_analyse_indices.toGet_Taux_sortie()
	ratio = dao_analyse_indices.toGet_Ratio_remplacement()
	Mouvement_Perso_info, TxDv, TxSt = dao_analyse_mouvement_personnel.toget_last_Mouvement_Personnel()
	Age_Moyen = dao_analyse_indices.toGet_meddle_age()
	ancien = dao_analyse_indices.anciennete()
	indice_principal,  value_returTxDv = dao_analyse_indices.toget_last_indice_principal()
	Agent_Direction = dao_analyse_indices.toGet_agent_by_direction()

	# Traitement Mobilité par Categorie
	keys_Mobilitie = []
	values_Mobilitie = []
	for cle in ListMobiliteByCategorie.keys():
		keys_Mobilitie.append(cle)

	for valeur in ListMobiliteByCategorie.values():
		values_Mobilitie.append(valeur)

	#Traitement Taux de formation Direction
	Keys_Taux_formation_direct = []
	valeur_Taux_formation_direct = []
	for cle in Taux_formation_Direction.keys():
		Keys_Taux_formation_direct.append(cle)
	for val in Taux_formation_Direction.values():
		valeur_Taux_formation_direct.append(val)

	# Traitement Taux de Formation
	Keys_Taux_formation = []
	valeur_Taux_formation = []
	for cle in Taux_formation.keys():
		Keys_Taux_formation.append(cle)
	for val in Taux_formation.values():
		valeur_Taux_formation.append(val)

	context = {
		'modules':modules, 'sous_modules':sous_modules,
		'title' : 'Overview',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'keys_Mobilitie': keys_Mobilitie,
		'values_Mobilitie': values_Mobilitie,
		'valeur_Taux_formation_direct': valeur_Taux_formation_direct,
		'Keys_Taux_formation': Keys_Taux_formation,
		'valeur_Taux_formation': valeur_Taux_formation,
		'taux_entre':taux_entre,
		'taux_sortie':taux_sortie,
		'ratio':ratio,
		'Mouvement_Perso_info': Mouvement_Perso_info,
		'Age_Moyen':Age_Moyen,
		'ancien': ancien,
		'indice_principal':indice_principal,
		'TxDv':TxDv, 'TxSt':TxSt, 'value_returTxDv':value_returTxDv,
		'Agent_Direction':Agent_Direction
	}

	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/rapport/overview.html')
	return HttpResponse(template.render(context, request))

def get_update_notification(request,ref):
	dao_temp_notification.toUpdateTempNotificationRead(ref)
	return get_dashboard(request)

#Get Person To Liste Formation
def lister_personnel_part_dep_json(request):
	id=request.GET['id']
	lister_personnel=dao_ligne_formation.toList_employer_by_formation(id)

	person=[]

	for item in lister_personnel:
		person.append(item.employe.nom_complet)
	#print('*****les personnes dans la formation*****%s' %person)
	return JsonResponse(person, safe=False)


#Get More Information to Mobility
def list_more_info_mobility(request):
	permission_number = 170
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	#WAY OF NOTIFCATION
	module_name = "MODULE_RESSOURCES_HUMAINES"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()

	#ANALYSE MOBILITE INTERNE
	recrutement_total_mobilite = dao_analyse_mobilite.toGet_Nombre_recrutement_mobilite()
	recrutement_total_year = dao_analyse_mobilite.toGet_Nombre_recrutement_Total()
	ListMobiliteByCategorie = dao_analyse_mobilite.toCountMobiliteByCategorie()
	Part_Recru_by_Mobilite, Nombre_recru_via_mobilite = dao_analyse_mobilite.toGet_Part_Recru_by_Mobilite()
	Taux_de_Mobilite, Nombre_Recru = dao_analyse_mobilite.taux_Mobilite_interne()
	Agent_Permanent = dao_analyse_mouvement_personnel.toGet_numberofAgentPermanent()


	# Traitement Mobilité par Categorie
	keys_Mobilitie = []
	values_Mobilitie = []
	for cle in ListMobiliteByCategorie.keys():
		keys_Mobilitie.append(cle)

	for valeur in ListMobiliteByCategorie.values():
		values_Mobilitie.append(valeur)

	# Traitement Part Recrutement de Mobilite by Year
	Keys_recru_year = []
	valuer_recru_year = []
	for cle in Part_Recru_by_Mobilite.keys():
		Keys_recru_year.append(cle)

	for val in Part_Recru_by_Mobilite.values():
		valuer_recru_year.append(val)

	# Traitement Taux de mobilite graphic
	Value_Mobilite = []
	for item in Taux_de_Mobilite.values():
		Value_Mobilite.append(item)

	#Traitement Recrutement total l'année
	recrutement_total = []
	for item in recrutement_total_year.values():
		recrutement_total.append(item)

	#Traitement Recrutement total de mobilité
	recru_total_mobilite = []
	for item in recrutement_total_mobilite.values():
		recru_total_mobilite.append(item)

	#Traitement Taux de mobilite Interne
	Taux = []
	for x, y in zip(recru_total_mobilite, Agent_Permanent):
		if x != 0 and y != 0:
			z = np.divide(x, y)
			Taux.append(z)
		else:
			Taux.append(x*y)

	#Traitement Part de recrutement
	Part = []
	for x, y in zip(recru_total_mobilite, recrutement_total):
		if x != 0 and y != 0 :
			T = np.divide(x, y)
			Part.append(T)
		else:
			Part.append(x*y)

	context = {
		'title' : 'Overview mobilité',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'ListMobiliteByCategorie': ListMobiliteByCategorie,
		'Keys_recru_year': Keys_recru_year,
		'valuer_recru_year': valuer_recru_year,
		'Nombre_recru_via_mobilite':Nombre_recru_via_mobilite,
		'Nombre_Recru': Nombre_Recru,
		'Value_Mobilite':Value_Mobilite,
		'recru_total_mobilite': recru_total_mobilite,
		'recrutement_total': recrutement_total,
		'Agent_Permanent': Agent_Permanent,
		'Taux': Taux,
		'Part': Part,
		'values_Mobilitie': values_Mobilitie,
		'keys_Mobilitie': keys_Mobilitie,
		'modules':modules,
		'sous_modules':sous_modules,


	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/mobilite/overview.html')
	return HttpResponse(template.render(context, request))

#To Get More info to Personnel movement
def list_more_info_personnel_mouvement(request):
	permission_number = 427
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	#WAY OF NOTIFCATION
	module_name = "MODULE_RESSOURCES_HUMAINES"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()

	#ANALYSE MOUVEMENT PERSONNEL, INDICE, MOBILITE INTERNE
	Part_Recru_by_Mobilite, Nombre_recru_via_mobilite = dao_analyse_mobilite.toGet_Part_Recru_by_Mobilite()
	Mouvement_Perso_info = dao_analyse_mouvement_personnel.toGet_Personnel_Mouvement()

	Recru_Post_vacant_year = dao_recrutement_interne.toGet_Recru_by_year()

	Mouvement_Perso = dao_analyse_mobilite.toMouvement_Personnel()
	agent_mois_cinq = dao_analyse_indices.toGet_Agent_moins_cinq_ans()


	# Traitement Part Recrutement de Mobilite by Year
	Keys_recru_year = []
	valuer_recru_year = []
	for cle in Part_Recru_by_Mobilite.keys():
		Keys_recru_year.append(cle)

	# Traitement Recrutement sur le post vacant
	Keys_recru_post_year = []
	valuer_recru_post_year = []
	for cle in Recru_Post_vacant_year.keys():
		Keys_recru_post_year.append(cle)

	for val in Recru_Post_vacant_year.values():
		valuer_recru_post_year.append(val)


	# Traitement Mouvement Personnel
	keys_Mouvement_P = []
	values_Mouvement_P = []
	for cle in Mouvement_Perso.keys():
		keys_Mouvement_P.append(cle)

	for valeur in Mouvement_Perso.values():
		values_Mouvement_P.append(valeur)


	context = {
		'title' : 'Mouvement Personnel',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'Keys_recru_year': Keys_recru_year,
		'Mouvement_Perso': Mouvement_Perso_info,
		'keys_Mouvement_P': keys_Mouvement_P,
		'values_Mouvement_P': values_Mouvement_P,
		'Keys_recru_post_year' : Keys_recru_post_year,
		'valuer_recru_post_year': valuer_recru_post_year,
		'agent_mois_cinq': agent_mois_cinq,
		'modules':modules,
		'sous_modules':sous_modules,

	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/personnel_mouve.html')
	return HttpResponse(template.render(context, request))

# LES INDICATEURS
########Indicateurs Principaux de Suivi#######
def get_indicateurs_principaux_de_suivi(request):
	try:
		permission_number = 445
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		#WAY OF NOTIFCATION
		module_name = "MODULE_RESSOURCES_HUMAINES"

		temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
		temp_notif_count = temp_notif_list.count()

		#ANALYSE MOBILITE INTERNE
		Part_Recru_by_Mobilite, Nombre_recru_via_mobilite = dao_analyse_mobilite.toGet_Part_Recru_by_Mobilite()
		#ANALYSE FORMATION
		Nombre_Agent = dao_analyse_formation.toGet_Agent_Categorie_Formation()
		Mouvement_Perso_info = dao_analyse_mouvement_personnel.toGet_Personnel_Mouvement()

		#ANALYSE INDICES
		ratio = dao_analyse_indices.toGet_Ratio_remplacement()
		taux_entre = dao_analyse_indices.toGet_Taux_entree()
		Nbre_Agent = dao_analyse_indices.toGet_Agent_by_Year()
		taux_sortie = dao_analyse_indices.toGet_Taux_sortie()
		turn_over = dao_analyse_indices.toGet_Turn_over()
		indice_principal = dao_analyse_indices.toGet_indices_principaux_suivi()
		Taux_ancien = dao_analyse_indices.toGet_taux_anciennete()
		Agent_cat_A,Agent_cat_B,Agent_cat_C,Agent_cat_D,Agent_cat_E,Agent_cat_F = dao_analyse_indices.toGet_Agent_cat()
		NumA, NumB, NumC, NumD, NumE, NumF, TotalAg, txPat= dao_analyse_indices.toGet_effectif_cat()
		Age_Moyen = dao_analyse_indices.toGet_meddle_age()
		ancien = dao_analyse_indices.anciennete()

		# Traitement Nombre d'Agents
		keys_Agent = []
		val_Agent = []
		for cle in Nombre_Agent.keys():
			keys_Agent.append(cle)
		for val in Nombre_Agent.values():
			val_Agent.append(val)

		# Traitement Part Recrutement de Mobilite by Year
		Keys_recru_year = []
		valuer_recru_year = []
		for cle in Part_Recru_by_Mobilite.keys():
			Keys_recru_year.append(cle)


		context = {
			'title' : 'indicateurs principaux de suivi',
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'keys_Agent': keys_Agent,
			'val_Agent': val_Agent,
			'ratio':ratio,
			'taux_entre':taux_entre,
			'taux_sortie': taux_sortie,
			'turn_over': turn_over,
			'indice_principal': indice_principal,
			'Nbre_Agent': Nbre_Agent,
			'Mouvement_Perso_info': Mouvement_Perso_info,
			'Keys_recru_year': Keys_recru_year,
			'Taux_ancien': Taux_ancien,
			'Agent_cat_A':Agent_cat_A,
			'Agent_cat_B':Agent_cat_B,
			'Agent_cat_C':Agent_cat_C,
			'Agent_cat_D':Agent_cat_D,
			'Agent_cat_E':Agent_cat_E,
			'Agent_cat_F':Agent_cat_F,
			'NumA': NumA,
			'NumB': NumB,
			'NumC': NumC,
			'NumD': NumD,
			'NumE': NumE,
			'NumF': NumF,
			'TotalAg': TotalAg,
			'txPat': txPat,
			'Age_Moyen': Age_Moyen,
			'ancien': ancien,
			'modules':modules,
			'sous_modules':sous_modules,

		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/Indicateurs/suivi.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:

		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_formation'))



########Indicateurs de la formation professionnelle #######
def get_indicateurs_formation_prof(request):
	try:
		permission_number = 446
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		#WAY OF NOTIFCATION
		module_name = "MODULE_RESSOURCES_HUMAINES"
		temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
		temp_notif_count = temp_notif_list.count()
		#ANALYSE INDICES
		Agent_cat_A,Agent_cat_B,Agent_cat_C,Agent_cat_D,Agent_cat_E,Agent_cat_F = dao_analyse_indices.toGet_Agent_cat()
		NumA, NumB, NumC, NumD, NumE, NumF, TotalAg, txPat= dao_analyse_indices.toGet_effectif_cat()
		indice_principal = dao_analyse_indices.toGet_indices_principaux_suivi()
		#ANALYSE FORMATION
		Nombre_Agent = dao_analyse_formation.toGet_Agent_Categorie_Formation()
		Taux_formation = dao_analyse_formation.toGet_taux_depart_formation_by_categorie()
		Taux_formation_Direction = dao_analyse_formation.toGet_taux_depart_formation_by_Direction()

		# Traitement Nombre d'Agents
		keys_Agent = []
		val_Agent = []
		for cle in Nombre_Agent.keys():
			keys_Agent.append(cle)
		for val in Nombre_Agent.values():
			val_Agent.append(val)

		#taux de depart en formation par categorie
		TxA = []
		for item, ele in zip(Agent_cat_A, NumA):
			if ele != 0 and item != 0:
				val = np.divide(item, ele)
			else:
				val = ele * item
			TxA.append(val)

		TxB = []
		for item, ele in zip(Agent_cat_B, NumA):
			if ele != 0 and item != 0:
				val = np.divide(item, ele)
			else:
				val = ele * item
			TxB.append(val)

		TxC = []
		for item, ele in zip(Agent_cat_C, NumA):
			if ele != 0 and item != 0:
				val = np.divide(item, ele)
			else:
				val = ele * item
			TxC.append(val)

		TxD = []
		for item, ele in zip(Agent_cat_D, NumA):
			if ele != 0 and item != 0:
				val = np.divide(item, ele)
			else:
				val = ele * item
			TxD.append(val)

		TxE = []
		for item, ele in zip(Agent_cat_E, NumA):
			if ele != 0 and item != 0:
				val = np.divide(item, ele)
			else:
				val = ele * item
			TxE.append(val)

		TxF = []
		for item, ele in zip(Agent_cat_F, NumA):
			if ele != 0 and item != 0:
				val = np.divide(item, ele)
			else:
				val = ele * item
			TxF.append(val)

		# Traitement Taux de Formation
		Keys_Taux_formation = []
		valeur_Taux_formation = []
		for cle in Taux_formation.keys():
			Keys_Taux_formation.append(cle)
		for val in Taux_formation.values():
			valeur_Taux_formation.append(val)


		#Traitement Taux de formation Direction
		Keys_Taux_formation_direct = []
		valeur_Taux_formation_direct = []
		for cle in Taux_formation_Direction.keys():
			Keys_Taux_formation_direct.append(cle)
		for val in Taux_formation_Direction.values():
			valeur_Taux_formation_direct.append(val)


		context = {
			'title' : 'indicateurs de la formation professionnelle',
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'keys_Agent': keys_Agent,
			'TxA':TxA,'TxB':TxB, 'TxC':TxC, 'TxD':TxD, 'TxE':TxE, 'TxF':TxF,
			'indice':indice_principal,
			'Keys_Taux_formation': Keys_Taux_formation,
			'valeur_Taux_formation': valeur_Taux_formation,
			'Keys_Taux_formation_direct': Keys_Taux_formation_direct,
			'valeur_Taux_formation_direct': valeur_Taux_formation_direct,
			'modules':modules,
			'sous_modules':sous_modules,
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/Indicateurs/formation_pro.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:

		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_formation'))


########Taux de formation par famille professionnelle #######
def get_indicateurs_formation_famille_prof(request):

	permission_number = 446
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	#WAY OF NOTIFCATION
	module_name = "MODULE_RESSOURCES_HUMAINES"
	temp_notif_list = dao_temp_notification.toGetListTempNotificationUnread(identite.utilisateur(request).id, module_name)
	temp_notif_count = temp_notif_list.count()

	#ANALYSE INDICES
	Tx_formation_pro = dao_analyse_indices.toGet_training_prof_family()
	Tx_Info, Tx_Rh, Tx_Compta = dao_analyse_indices.toGet_training_by_cat()
	tx_cg, tx_tel, tx_eco  = dao_analyse_indices.toGet_training_by_cat_s()
	tx_lg, tx_aj, tx_com, tx_poste  = dao_analyse_indices.toGet_training_by_cat_s_s()
	#ANALYSE FORMATION
	Taux_formation_Direction = dao_analyse_formation.toGet_taux_depart_formation_by_Direction()



	#Traitement Taux de formation Direction
	Keys_Taux_formation_direct = []
	valeur_Taux_formation_direct = []
	for cle in Taux_formation_Direction.keys():
		Keys_Taux_formation_direct.append(cle)
	for val in Taux_formation_Direction.values():
		valeur_Taux_formation_direct.append(val)

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'indicateurs de la formation professionnelle',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'Tx_formation_pro': Tx_formation_pro,
		'Keys_Taux_formation_direct': Keys_Taux_formation_direct,
		'Tx_Info':Tx_Info,
		'Tx_Rh':Tx_Rh,
		'Tx_Compta': Tx_Compta,
		'tx_cg':tx_cg, 'tx_tel':tx_tel, 'tx_eco':tx_eco,
		'tx_lg':tx_lg, 'tx_aj':tx_aj, 'tx_com':tx_com, 'tx_poste':tx_poste,
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/Indicateurs/formation_famille.html')
	return HttpResponse(template.render(context, request))

##### END INDICATEURS


##### UPDATE INDICATEURS
def post_mouvement_Personnel_masse_salariale(request):
	try:
		masse= int(request.POST['masse_salariale'])
		year = int(request.POST['annee'])
		masse_sal = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_masse_sal(year, masse)
		#print('CouCou!!!!!!', masse_sal)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_masse_salariale \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_masse_salariale')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_propagatio_stage(request):
	try:
		prop= int(request.POST['propagation_stage'])
		year = int(request.POST['annee_pg'])
		#print('CouCou!!!!!!', year)
		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnelpropagation_stage(year, prop)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_propation_stage \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_propation_stage')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_total_mise_stage(request):
	try:
		stage= int(request.POST['mise_stage'])
		year = int(request.POST['annee_st'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_total_mise_stage(year, stage)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_total_Mise_stage \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_total_Mise_stage')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_depart_def(request):
	try:
		D_def= int(request.POST['Depart_D'])
		year = int(request.POST['annee_D'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_Depart_Def(year, D_def)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_depart_def \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_depart_def')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_Depart_provoir(request):
	try:
		D_Pro= int(request.POST['Depart_Pro'])
		year = int(request.POST['annee_Pro'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_Depart_provoir(year, D_Pro)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_Depart_provoir \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_Depart_provoir')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_eff_physique(request):
	try:
		eff_physique = int(request.POST['eff_physique'])
		year = int(request.POST['annee_eff'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_eff_physique(year, eff_physique)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_eff_physique \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_eff_physique')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_Depart_vol(request):
	try:
		D_vol = int(request.POST['D_vol'])
		year = int(request.POST['annee_vol'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_Depart_vol(year, D_vol)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_Depart_vol \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_Depart_vol')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_Demission(request):
	try:
		Demission = int(request.POST['Demission'])
		year = int(request.POST['annee_Dem'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_Demission(year, Demission)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_Demission \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_Demission')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_arriver(request):
	try:
		Arrive = int(request.POST['arrive'])
		year = int(request.POST['annee_Arriv'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_arriver(year, Arrive)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_Arriver \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_Arriver')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_post_vacant(request):
	try:
		postvac = int(request.POST['postvac'])
		year = int(request.POST['annee_Arriv'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_poste_vacant_by_mob(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_postvac \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_postvac')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_poste_vacant_pouvu(request):
	try:
		postvac = int(request.POST['postvacP'])
		year = int(request.POST['annee_P'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_poste_vacant_pouvu(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_postvac \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_postvac')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_recru_emploi_permanent(request):
	try:
		postvac = int(request.POST['recru'])
		year = int(request.POST['annee_recru'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_recru_emploi_permanent(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_recru \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_recru')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_concours(request):
	try:
		postvac = int(request.POST['concour'])
		year = int(request.POST['annee_concour'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_concours(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_concours \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_concours')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))


def post_mouvement_Personnel_mutation(request):
	try:
		postvac = int(request.POST['mut'])
		year = int(request.POST['annee_mut'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_mutation(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_mutation \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_mutation')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_detachement(request):
	try:
		postvac = int(request.POST['detachement'])
		year = int(request.POST['annee_det'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_detachement(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_detachement \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_detachement')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_recru_direct(request):
	try:
		postvac = int(request.POST['recru_direct'])
		year = int(request.POST['annee_RD'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_recru_direct(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_recru_direct \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_recru_direct')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_interimaire(request):
	try:
		postvac = int(request.POST['interim'])
		year = int(request.POST['annee_interim'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_interimaire(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_interim \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_interim')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))

def post_mouvement_Personnel_total_recru(request):
	try:
		postvac = int(request.POST['tot_recru'])
		year = int(request.POST['annee_tot_recru'])

		propo = dao_analyse_mouvement_personnel.toUpdateMouvement_personnel_total_recru(year, postvac)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_tot_recru \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_tot_recru')
		messages.error(request,e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_more_info_personnel_mouvement'))



def get_json_ListeFormation(request):
	try:
		#print("les get JSON Liste Formation")
		data = []
		ListeFormation = dao_formation.toGetFormationByMounth()
		#print(ListeFormation)
		return JsonResponse(ListeFormation, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)

def get_json_ListeConge(request):
	try:
		#print("***Le resultat congé***")
		data = []
		ListNumberCongebyMonth,ListeQueryConge = dao_conge.ListeNumberCongeByMunth()
		#print(ListNumberCongebyMonth)
		return JsonResponse(ListNumberCongebyMonth, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)



# EMPLOYE
def get_lister_employe(request):
	try:
		permission_number = 72
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployesActifs(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)

		context ={
		'modules':modules,
		'sous_modules':sous_modules,
		'title' : 'Liste des employés',
		'model' : model,
		'view' : view,
		'sous_modules': sous_modules,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_employes_of_departement(request, filter):
	try :
		permission_number = 72
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response


		filter = int(filter)
		# model = dao_employe.toListEmployesOfDepartement(filter)
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployesOfDepartement(filter), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		departement = dao_unite_fonctionnelle.toGetUniteFonctionnelle(filter)
		#print(departement)
		#print("FILTER")
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des employés - ' + departement.libelle,
			'model' : model,
			'view' : view,
			#'can_create' : dao_droit.toGetDroitRole('CREER_EMPLOYE',nom_role,utilisateur.nom_complet),
			'menu' : 1,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/employe/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))

def get_creer_employe(request):
	try:
		permission_number = 73
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		postes = dao_poste.toListPostes()
		employes = dao_employe.toListEmployesActifs()
		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		banque=dao_banque.toListBank()
		fonctions=dao_fonction.toListFonction()
		categories=dao_categorieDesignation.toListcategories()
		diplome = dao_diplome.toList()
		bulletin_modeles = dao_bulletin_modele.toList()
		statutEmploye = dao_StatusDesignationEmploye.toListStatuts()
		lieuTravail = dao_lieu_travail.toListLieuTravail()
		type_structure = dao_type_structure.toList()

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Nouvel employé',
		'postes' : postes,
		'employe' : employes,
		'categories':categories,
		'departements' : departements,
		'categorie_employes': dao_categorie_employe.toListCategorie_employe(),
		'isPopup': isPopup,
		'pays' : dao_place.toListPlacesOfType(1),
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'fonctions':fonctions,
		'banque':banque,
		'diplome':diplome,
		'bulletin_modeles' : bulletin_modeles,
		'statuts':statutEmploye,
		'lieuTravail':lieuTravail,
		'type_structure':type_structure
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))

def get_creer_fonction(request):
	try:
		permission_number = 349
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()

		context ={
		'title' : 'Nouvelle fonction',
		#'isPopup': isPopup,
		'modules':modules,
		'sous_modules': sous_modules,
		'departements' : departements,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		}

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/fonctions/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))

def get_modifier_fonction(request,ref):
	try:
		permission_number = 351
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		ref = int(ref)
		fonction = dao_fonction.toGetFonction(ref)
		#print('get_modifier_fonction')

		#print(fonction)
		#print('end get_modifier_fonction')

		context ={
		'modules':modules,
		'sous_modules':sous_modules,
		'title' : 'Modifier une fonction',
		'departements' : departements,
		'utilisateur' : utilisateur,
		'model':fonction,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		}

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/fonctions/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))

def get_details_fonction(request, ref):
	try:
		permission_number = 350
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		fonction = dao_fonction.toGetFonction(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,fonction)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : fonction.designation,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'model' : fonction,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/fonctions/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER FONCTION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_fonction'))


def get_lister_fonction(request):
		permission_number = 350
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_fonction.toListFonction()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_fonction.toListFonction(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		# #print('rrrrrrrrrrrrrrrrrrrrrrrr')
		# for m in model:
		# 	#print("Désignation : {} ,  ID : {} ".format(m.designation, m.id))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des fonctions',
			'model' : model,
			'menu' : 5,
			'view':view,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/fonctions/list.html")
		return HttpResponse(template.render(context, request))


def post_creer_fonction_of_departement(request):
	departement_id = int(request.POST["departement"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		fonction_dao = dao_fonction.toCreateFonction(auteur, designation, description, departement_id)
		fonction = dao_fonction.toSaveFonction(fonction_dao)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_fonction"))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_fonction_of_departement \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_fonction_of_departement')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'exécution")
		return HttpResponseRedirect(reverse('module_ressources_humaines_add_fonction'))


def post_modifier_fonction_of_departement(request):
	id=int(request.POST["ref"])
	departement_id = int(request.POST["departement"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		fonction_dao = dao_fonction.toCreateFonction(auteur, designation, description, departement_id)
		fonction = dao_fonction.toUpdateFontion(id,fonction_dao)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_fonction"))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES post_creer_fonction_of_departement \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer post_creer_fonction_of_departement')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_add_fonction'))

def get_upload_fonction(request):
	try:
		permission_number = 349
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des fonctions",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/fonctions/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD FONCTION")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_fonction"))


@transaction.atomic
def post_upload_fonction(request):
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


			departement_id = None
			departement = str(df['departement'][i])
			departement = models.Model_Unite_fonctionnelle.objects.filter(libelle__icontains = departement).first()
			if departement != None : departement_id = departement.id

			fonction_dao = dao_fonction.toCreateFonction(auteur, designation, description, departement_id)
			fonction = dao_fonction.toSaveFonction(fonction_dao)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_fonction"))
	except Exception as e:
		#print("ERREUR POST UPLOAD FONCTION")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD FONCTION \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressources_humaines_add_fonction"))

def getAdressBanque_json(request):
	try:
		ref=request.GET['ref']
		banque=dao_banque.toGetBank(ref)
		dic={
			'designation':banque.designation,
			'adresse': banque.adresse
		}
		return JsonResponse(dic, safe=False)
	except Exception as e:
		#print('getAdressBanque_json %s'%(e))
		pass

@transaction.atomic
def post_creer_employe(request):
	sid = transaction.savepoint()
	try:

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		image = ""

		#Identification de l'employé
		matricule = request.POST["matricule"]
		prenom = request.POST["prenom"]
		nom = request.POST["nom"]
		nom_complet = nom + ' ' + prenom
		lieu_travail = request.POST["lieu_travail"]
		email = request.POST["email"]
		phone = request.POST["phone"]
		phone_professionnel = request.POST["phone_professionnel"]
		phone_pro2 = request.POST["phone_bureau"]

		#Poste
		unite_fonctionnelle_id = int(request.POST["departement"])
		poste_id = int(request.POST["poste"])
		fonction_list_id = request.POST.getlist("fonction", None)
		est_particulier = True
		est_permanent = True
		adresse = request.POST["adresse"]
		categorie_employe_id = request.POST["categorie_employe_id"]
		contrat = request.POST["contrat"]
		categorie_socio_professionnelle = request.POST["categorie_socio_professionnelle"]
		numero_ss = request.POST["numero_ss"]
		date_engagement = request.POST["date_engagement"]
		prisecharge = request.POST["prisecharge"]
		statutEmploye = request.POST["statutEmploye"]
		modelBulletin = request.POST["modelbulletin"]
		# typestructure = request.POST["typestructure"]
		# if typestructure == 0: typestructure = None

		#Adresse Personelle
		commune_quartier_id = int(request.POST["commune_quartier_id"])

		#Naissance
		date_naissance = request.POST["date_naissance"]
		lieu_naissance = request.POST["lieu_naissance"]

		#Nationalite
		nationalite = request.POST["nationalite"]
		numero_identification = request.POST["numero_identification"]
		numero_passeport = request.POST["numero_passeport"]
		sexe = request.POST["genre"]
		etat_civil = request.POST["etat_civil"]
		diplome = int(request.POST["diplome"])
		if diplome == 0: diplome = None

		isPopup = request.POST["isPopup"]

		#conversion de la date
		date_naissance = timezone.datetime(int(date_naissance[6:10]), int(date_naissance[3:5]), int(date_naissance[0:2]))
		prisecharge = timezone.datetime(int(prisecharge[6:10]), int(prisecharge[3:5]), int(prisecharge[0:2]))
		date_engagement = timezone.datetime(int(date_engagement[6:10]), int(date_engagement[3:5]), int(date_engagement[0:2]))


		#EMPLOYE CREATED
		employe = dao_employe.toCreateEmploye(prenom,nom,nom_complet,"",email,phone,adresse,commune_quartier_id,True,None,est_particulier,None,unite_fonctionnelle_id,lieu_travail,categorie_employe_id,poste_id,categorie_socio_professionnelle,diplome,modelBulletin,statutEmploye, None)
		employe = dao_employe.toSaveEmploye(auteur, employe)
		# print("****EMPLOYE SAVED")

		if employe != None :
			if 'image_upload' in request.FILES:
				file = request.FILES["image_upload"]
				employe_img_dir = 'personnes/'
				media_dir = media_dir + '/' + employe_img_dir
				save_path = os.path.join(media_dir, str(employe.id) + ".jpg")
				path = default_storage.save(save_path, file)
				#On affecte le chemin de l'Image
				employe.image = media_url + employe_img_dir + str(employe.id) + ".jpg"
				employe.save()

			#Enregistrement Profil
			#print("debut")
			est_enconge = False
			if "est_enconge" in  request.POST : est_enconge = True

			# print("****DEBUT PROFIL")
			profil_agent = dao_profil.toCreateProfil(date_engagement, prisecharge, date_naissance, lieu_naissance, nationalite,numero_passeport,numero_identification,etat_civil,numero_ss,sexe,matricule,email,phone_professionnel,phone,phone_pro2,contrat,est_permanent)
			profil = dao_profil.toSaveProfil(auteur,profil_agent)
			#END PROFIL

			# print("****DEBUT FONCTION")
			for i in range(0, len(fonction_list_id)) :
				fonction_id = fonction_list_id[i]
				#print('Afficher les cles des fonctions %s' % (fonction_id))
				profil.fonctions.add(fonction_id)

			profil.save()

			#COMPTE BANCAIRE
			list_banque_name = request.POST.getlist('banque_name', None)
			list_numero_compte = request.POST.getlist("numero_compte",None)
			list_repartition = request.POST.getlist("repartition",None)
			mode_paiement = request.POST["mode_paiement"]
			list_code_guichet = request.POST.getlist("code_guichet",None)
			list_titulaire_compte = request.POST.getlist("titulaire_compte",None)
			list_iban = request.POST.getlist("iban",None)
			list_bic = request.POST.getlist("bic",None)
			list_cle_rib = request.POST.getlist("cle_rib",None)


			# print('****DEBUT BANQUE')
			for i in range(0, len(list_banque_name)):

				banque_id = list_banque_name[i]
				pays_id = commune_quartier_id
				code_guichet = list_code_guichet[i]
				nom_guichet = ""
				titulaire_compte = list_titulaire_compte[i]
				iban = list_iban[i]
				bic = list_bic[i]
				cle_rib = list_cle_rib[i]

				numero_compte = list_numero_compte[i]
				repartition = list_repartition[i]

				designation = titulaire_compte
				description = ""
				type_compte = "epargne"

				compteBanque = models.Model_CompteBanque_Employe(designation = designation, description = description, numero_compte = numero_compte, type_compte = type_compte, profilrh_id = profil.id, banque_id = banque_id, repartition = repartition, mode_paiement = mode_paiement, auteur_id = auteur.id )
				compteBanque.save()
				# #print(compteBanque)

				rib = models.Model_Rib(banque_id = banque_id, cle_rib = cle_rib, code_guichet = code_guichet, nom_guichet = nom_guichet, titulaire_compte = titulaire_compte, iban = iban, bic = bic, comptebanque_id = compteBanque.id, auteur_id = auteur.id )
				rib.save()
				# #print(rib)
				#print("compte {} et RIB {} crees".format(compteBanque.numero_compte, rib.cle_rib))

			employe.profilrh_id = profil.id
			employe.save()

			#Enregistrement des fichiers upload
			docs_dir = 'documents/'
			media_dir = media_dir + '/' + docs_dir

			#1. CV
			if 'curriculum_vitae' in request.FILES:
				nom_fichier = request.FILES['curriculum_vitae']
				dao_document.toUploadDocument(auteur,nom_fichier, employe)


			#2 Contrat de travail
			if 'contrat_travail' in request.FILES:
				nom_fichier = request.FILES.getlist("contrat_travail",None)
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#3 diplome_etude
			if 'diplome_etude' in request.FILES:
				nom_fichier = request.FILES.getlist("diplome_etude",None)
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#4 document_annexe
			if 'document_annexe' in request.FILES:
				nom_fichier = request.FILES.getlist("document_annexe",None)
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#AYANT DROIT
			# print("****DEBUT AYANT DROIT")
			list_noms_ayant_droit = request.POST.getlist('noms_ayant_droit', None)
			list_date_naissance = request.POST.getlist("birthday_ayant", None)
			list_lien_parente = request.POST.getlist("lien_parente", None)
			list_description = request.POST.getlist("description",None)

			#print(len(list_noms_ayant_droit))
			#print(len(list_lien_parente))
			#print(len(list_description))
			for i in range(0, len(list_noms_ayant_droit)) :
				#print("argh")
				noms = list_noms_ayant_droit[i]
				lien_parente = list_lien_parente[i]
				description = list_description[i]
				date_naissance_ayant = list_date_naissance[i]

				date_naissance_ayant = timezone.datetime(int(date_naissance_ayant[6:10]), int(date_naissance_ayant[3:5]), int(date_naissance_ayant[0:2]))
				lien_parente = lien_parente.lower()

				dependant = dao_dependant.toCreateDependant(noms,lien_parente,description,employe.id, None, date_naissance_ayant)
				dependant = dao_dependant.toSaveDependant(auteur,dependant)

				#SAVE BIRTHDAY DEPENDANT
				# dependant.date_naissance = date_naissance_ayant
				# dependant.save()

			# Nous créons une première mobilité pour un employé
			dep = dao_unite_fonctionnelle.toGetUniteFonctionnelle(unite_fonctionnelle_id)
			service = dep.libelle
			fonctions_occupees = dao_poste.toGetPoste(poste_id).designation

			modalites = "Engagement de l'employé"
			direction = dep.unite_fonctionnelle

			#date_entree = request.POST['date_entree']
			#date_sortie = request.POST['date_sortie']

			#print(employe)
			# categorie_socio_professionnelle = employe.categorie_employe
			#print(employe.categorie_employe)
			categorie_socia_pro_precedent =""
			type_mobilite = "Promotion"


			#date_engagement = timezone.datetime(int(date_engagement[6:10]), int(date_engagement[3:5]), int(date_engagement[0:2]))
			#date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))
			auteur = identite.utilisateur(request)

			#Ajout de la pondération en fonction occupée
			"""
			Les pondérations sont sur 10 suivant le barême suivant :

			DG = 10
			Autres Directeurs = 8
			Chef de service = 6
			Chef de bureau et Chef de projet = 4
			Assistant = 2

			"""
			ponderation = 0

			if "assistant" in fonctions_occupees.lower():
				ponderation = 2
			elif "projet" in fonctions_occupees.lower() or "bureau" in fonctions_occupees.lower():
				ponderation = 4
			elif "service" in fonctions_occupees.lower():
				ponderation = 6
			elif "directeur" in fonctions_occupees.lower():
				ponderation = 8
			elif fonctions_occupees.lower() == "directeur général" or fonctions_occupees.lower() == "directeur general":
				ponderation = 10
			else:
				ponderation = 0


			# mobilite=dao_mobilite.toCreateMobilite(direction,service,type_mobilite,fonctions_occupees,ponderation,categorie_socio_professionnelle,modalites,date_entree,None,employe_id,categorie_socia_pro_precedent)
			# print("****DEBUT MOBILITE EMPLOYE")
			mobilite=dao_mobilite.toCreateMobilite(direction,service,type_mobilite,fonctions_occupees,ponderation,categorie_socio_professionnelle,modalites,date_engagement,None,employe.id,categorie_socia_pro_precedent)
			mobilite=dao_mobilite.toSaveMobilite(auteur, mobilite)


			#print("PROFIL SAVED")
			transaction.savepoint_commit(sid)

		if isPopup == 'False':
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_rh_detail_employe', args=(employe.id,)))
		else:
			return HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_add_employe'))

def get_details_employe(request,ref):
	try:
		permission_number = 72
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref=int(ref)
		employe=dao_employe.toGetEmploye(ref)
		documents = dao_document.toListDocumentbyObjetModele(employe)
		dependants = dao_dependant.toListDependantByEmploye(employe.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,employe)
		compteB = dao_compte_banque_employe.toGet_compteBancaire_employe(ref)
		ribs = dao_rib.toListRibsOfEmploye(ref)
		mobilite_employe = dao_mobilite_employe.toGetMobiliteByEmploye(employe)


		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Détails d\'un employé',
		'model' : employe,
		'dependants':dependants,
		'ribs' : ribs,
		'mobilite_employe': mobilite_employe,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'documents':documents,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'compteB':compteB
		}

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_list_employe'))


def get_details_carriere_employe(request,ref):
	try:
		permission_number = 72
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref=int(ref)
		employe=dao_employe.toGetEmploye(ref)

		mobilite_employe = dao_mobilite_employe.toGetMobiliteByEmploye(employe)
		types_mobilite = dao_type_mobilite.toListTypesMobiliteEvolution()
		postes = dao_poste.toListPostes()
		classifications = dao_classification_professionnelle.toListClassificationProfessionnelle()
		categories = dao_categorieDesignation.toListcategories()
		unites_fonctionnelles = dao_unite_fonctionnelle.toListUniteFonctionnelle()

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Carrière d\'un employé',
		'model' : employe,
		'mobilite_employe': mobilite_employe,
		'types_mobilite': types_mobilite,
		'postes':postes,
		'classifications':classifications,
		'categories': categories,
		'unites_fonctionnelles': unites_fonctionnelles,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"roles": groupe_permissions,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/carriere/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_list_employe'))



def get_details_employe_me(request):
	try:
		permission_number = 442
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response


		documents = dao_document.toListDocumentbyObjetModele(utilisateur)
		dependants = dao_dependant.toListDependantByEmploye(utilisateur.id)

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/me/item.html')
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Détails sur {}'.format(utilisateur.nom_complet),
		'model' : utilisateur,
		'dependants':dependants,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'documents':documents,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER EMPLOYE ME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Me')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))


def get_modifier_employe(request, ref):
	try:
		permission_number = 74
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		employe = dao_employe.toGetEmploye(ref)
		postes = dao_poste.toListPostes()
		employes = dao_employe.toListEmployesActifs()
		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		banque=dao_banque.toListBank()
		documents = dao_document.toListDocumentbyObjetModele(employe)
		bulletin_modeles = dao_bulletin_modele.toList()
		# for doc in documents:
		# 	num = int(doc.source_document_id)
		# 	employe = models.Model_Employe.objects.get(id = num)
		# 	#print(type(employe))
		num = 0
		num = documents.count()
		#print(documents)
		dependants = dao_dependant.toListDependantByEmploye(employe.id)
		typediplome= dao_type_diplome.toList()
		diplome= models.Model_Diplome.objects.all()
		#print(dependants)

		fonctions=dao_fonction.toListFonction()

		pays = province = ville = commune = None
		#print("QUARTIER")
		#print(employe.commune_quartier_id)
		if employe.commune_quartier_id != None and employe.commune_quartier_id != 0:
			#print("ICI")
			commune = dao_place.toGetPlace(employe.commune_quartier_id)
			ville = dao_place.toGetPlace(commune.parent_id)
			province = dao_place.toGetPlace(ville.parent_id)
			pays = dao_place.toGetPlace(province.parent_id)
			# print('*******LE PAYS', pays)

		ribs = dao_rib.toListRibsOfEmploye(employe.id)
		statutEmploye = dao_StatusDesignationEmploye.toListStatuts()
		lieuTravail = dao_lieu_travail.toListLieuTravail()
		# print('*Lieu de Travail', lieuTravail)
		# print('*Lieu de Travail', lieuTravail)

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier employé',
		'model' : employe,
		'postes' : postes,
		'employe' : employes,
		'banques':dao_banque.toListBank(),
		'statuts':statutEmploye,
		'type_structures': dao_type_structure.toList(),
		'num':num,
		'departements' : departements,
		'lieuTravail':lieuTravail,
		'categories':dao_categorieDesignation.toListcategories(),
		'categorie_employes': dao_categorie_employe.toListCategorie_employe(),
		'pays' : dao_place.toListPlacesOfType(1),
		'le_pays' : pays,
		'la_province' : province,
		'la_ville' : ville,
		'la_commune' : commune,
		'documents': documents,
		'dependants':dependants,
		'ribs' : ribs,
		'bulletin_modeles' : bulletin_modeles,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'fonctions':fonctions,
		'banque' : banque,
		'menu' : 5,
		'typediplome': typediplome,
		'diplome': diplome,

		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur modifier Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_list_employe'))


@transaction.atomic
def post_modifier_employe(request):
	sid = transaction.savepoint()
	ref = int(request.POST["ref"])

	try:
		adresse=""

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		image = ""

		#Identification de l'employé
		matricule = request.POST["matricule"]
		prenom = request.POST["prenom"]
		nom = request.POST["nom"]
		nom_complet = nom + ' ' + prenom
		lieu_travail = request.POST["lieu_travail"]
		email = request.POST["email"]
		phone = request.POST["phone"]
		phone_pro2 = request.POST["phone_bureau"]
		phone_professionnel = request.POST["phone_professionnel"]

		type_structure_id = int(request.POST["type_structure_id"])
		#est_particulier = int(request.POST["est_particulier"])
		#commune_quartier_id = int(request.POST["commune_quartier_id"])

		#Poste
		departement_id = int(request.POST["departement"])
		poste_id = int(request.POST["poste"])
		un_poste_id = poste_id
		fonction_list_id = request.POST.getlist("fonction", None)
		est_particulier = True
		est_permanent = True
		adresse = request.POST["adresse"]
		categorie_employe_id = request.POST["categorie_employe_id"]
		contrat = request.POST["contrat"]
		categorie_socio_professionnelle = request.POST["categorie_socio_professionnelle"]
		numero_ss = request.POST["numero_ss"]
		date_engagement = request.POST["date_engagement"]
		prisecharge = request.POST["prisecharge"]
		statutEmploye = request.POST["statutEmploye"]
		modelBulletin = request.POST["modelbulletin"]


		#Naissance
		date_naissance = request.POST["date_naissance"]
		lieu_naissance = request.POST["lieu_naissance"]

		#Nationalite
		nationalite = request.POST["nationalite"]
		numero_identification = request.POST["numero_identification"]
		numero_passeport = request.POST["numero_passeport"]
		sexe = request.POST["genre"]
		etat_civil = request.POST["etat_civil"]
		diplome_ = request.POST["diplome"]


		#conversion de la date
		prisecharge = timezone.datetime(int(prisecharge[6:10]), int(prisecharge[3:5]), int(prisecharge[0:2]))
		date_naissance = timezone.datetime(int(date_naissance[6:10]), int(date_naissance[3:5]), int(date_naissance[0:2]))
		date_engagement = timezone.datetime(int(date_engagement[6:10]), int(date_engagement[3:5]), int(date_engagement[0:2]))


		pers = dao_employe.toGetEmploye(ref)
		poste = dao_poste.toGetPoste(un_poste_id)

		#print("FIN POST")
		#print('alert adress %s'%(adresse))
		items = ''
		for item in adresse:
			items = adresse.split(',')
		#print('List adr %s' % (list(set(items))))
		stringAdr=list(set(items))
		adr_from_list=','.join(stringAdr)
		est_particulier = True

		#print('adress from a list %s' % (adr_from_list))
		# print("**DEBUT CREATE EMPLOYE")

		img=dao_employe.getchangeImag(ref)
		old_employe = dao_employe.toGetEmploye(ref)
		employe = dao_employe.toCreateEmploye(prenom, nom, nom_complet, img, email, phone, adr_from_list, old_employe.commune_quartier_id,
											True, None,est_particulier,None, departement_id, lieu_travail, categorie_employe_id, poste_id, categorie_socio_professionnelle,
											diplome_, modelBulletin, statutEmploye,None)
		employe = dao_employe.toUpdateEmploye(ref, employe)
		print('EMPLOYE', employe)

		#Random
		number=randint(3, employe.id)
		#print('VALEUR FROM FORM INPUT FILE I')
		if employe != None :
			# if type_structure_id != 0:
			# 	employe.type_structure_id = type_structure_id
			# 	employe.save()
			#print('VALEUR FROM FORM INPUT FILE II')
			if 'image_upload' in request.FILES:
				file = request.FILES["image_upload"]
				#print('VALEUR FROM FORM INPUT FILE ',file)
				employe_img_dir = 'personnes/'
				media_dir = media_dir + '/' + employe_img_dir

				save_path = os.path.join(media_dir, str(employe.id)+""+str(number)+""+" .jpg")
				path = default_storage.save(save_path, file)
				#On affecte le chemin de l'Image
				image = media_url + employe_img_dir + str(employe.id)+""+str(number)+""+" .jpg"
				dao_employe.changeImag(image,employe.id)

			#Enregistrement Profil

			est_enconge = False
			if "est_enconge" in  request.POST : est_enconge = True
			# designation_banque = ""
			# adresse_banque = ""
			# code_swift = ""
			# education = ""
			# compte_bancaire = ""

			# print("DEBUT CREATE PROFIL")
			#print('ID = ',employe.profilrh_id)
			profil_agent = dao_profil.toCreateProfil(date_engagement, prisecharge, date_naissance, lieu_naissance, nationalite,numero_passeport,numero_identification,etat_civil,numero_ss,sexe,matricule,email,phone_professionnel,phone,phone_pro2,contrat,est_permanent)
			profil = dao_profil.toUpdateProfil(employe.profilrh_id,profil_agent)
			# profil.phone_personnel = phone
			# profil.phone_professionnel2 = phone_pro2
			# profil.permis = permis
			# profil.debut_service = prisecharge
			# profil.save()
			# print("NIVEAU PROFIL END")

			for i in range(0, len(fonction_list_id)) :
				fonction_id = fonction_list_id[i]
				profil.fonctions.add(fonction_id)

			profil.save()

			# print("***DEBUT CREATE COMPTE BANCAIRE")

			#COMPTE BANCAIRE
			list_banque_id = request.POST.getlist('banque_name', None)
			list_numero_compte = request.POST.getlist("numero_compte",None)
			list_repartition = request.POST.getlist("repartition",None)
			mode_paiement = request.POST["mode_paiement"]
			list_code_guichet = request.POST.getlist("code_guichet",None)
			# list_nom_guichet = request.POST.getlist("nom_guichet",None)
			list_titulaire_compte = request.POST.getlist("titulaire_compte",None)
			list_iban = request.POST.getlist("iban",None)
			list_bic = request.POST.getlist("bic",None)
			list_cle_rib = request.POST.getlist("cle_rib",None)


			# #print(len(list_banque_id))
			# print('****DEBUT ITERATION')

			listCompteUpdated = []
			listCompteOld = []
			comptebancaires = models.Model_CompteBanque_Employe.objects.filter(profilrh_id = profil.id).all()
			for comptebancaire in comptebancaires:
				listCompteOld.append(comptebancaire.id)

			for i in range(0, len(list_banque_id)):
				banque_id = list_banque_id[i]
				pays_id = 7 # Congo Brazzaville
				code_guichet = list_code_guichet[i]
				nom_guichet = ""
				titulaire_compte = list_titulaire_compte[i]
				iban = list_iban[i]
				bic = list_bic[i]
				cle_rib = list_cle_rib[i]

				numero_compte = list_numero_compte[i]
				repartition = list_repartition[i]

				# #print('****BANQUE', i, banque_id, numero_compte, repartition)

				designation = titulaire_compte
				description = ""
				type_compte = "epargne"
				# #print('**** ITERATION before objet dao', i)

				compteBanque = models.Model_CompteBanque_Employe.objects.filter(numero_compte = numero_compte, profilrh_id = profil.id).first()
				if compteBanque == None:
					compteBanque = models.Model_CompteBanque_Employe(designation = designation, description = description, numero_compte = numero_compte, type_compte = type_compte, profilrh_id = profil.id, banque_id = banque_id, repartition = repartition, mode_paiement = mode_paiement, auteur_id = auteur.id )
					compteBanque.save()
					# print(compteBanque)

					rib = models.Model_Rib(banque_id = banque_id, cle_rib = cle_rib, code_guichet = code_guichet, nom_guichet = nom_guichet, titulaire_compte = titulaire_compte, iban = iban, bic = bic, comptebanque_id = compteBanque.id, auteur_id = auteur.id )
					rib.save()
					# print(rib)
					# print("compte {} et RIB {} crees".format(compteBanque.numero_compte, rib.cle_rib))
				else:
					compteBanque = models.Model_CompteBanque_Employe(designation = designation, description = description, numero_compte = numero_compte, type_compte = type_compte, profilrh_id = profil.id, banque_id = banque_id, repartition = repartition, mode_paiement = mode_paiement, auteur_id = auteur.id, created_at = compteBanque.created_at)
					compteBanque.save()

					rib = models.Model_Rib(pays_id = pays_id, banque_id = banque_id, cle_rib = cle_rib, code_guichet = code_guichet, nom_guichet = nom_guichet, titulaire_compte = titulaire_compte, iban = iban, bic = bic, comptebanque_id = compteBanque.id, auteur_id = auteur.id, created_at = compteBanque.created_at)
					rib.save()
					# print("compte {} et RIB {} modifiees".format(compteBanque.numero_compte, rib.cle_rib))
					listCompteUpdated.append(compteBanque.id)
			# print("listCompteUpdated: {}".format(listCompteUpdated))
			# Suppression éléments qui n'existent plus
			for id in listCompteOld:
				if id not in listCompteUpdated:
					#print("compte {} recupere".format(id))
					compte = models.Model_CompteBanque_Employe.objects.get(pk = id)
					compte.delete()
					# RIB associé supprimé en cascade
					# print("compte et RIB supprimes")

			#Enregistrement des fichiers upload
			#1. CV
			if 'curriculum_vitae' in request.FILES:
				nom_fichier = request.FILES['curriculum_vitae'].name
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#2 Contrat de travail
			if 'contrat_travail' in request.FILES:
				nom_fichier = request.FILES.getlist("contrat_travail",None)
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#3 diplome_etude
			if 'diplome_etude' in request.FILES:
				nom_fichier = request.FILES.getlist("diplome_etude",None)
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#4 document_annexe
			if 'document_annexe' in request.FILES:
				nom_fichier = request.FILES.getlist("document_annexe",None)
				dao_document.toUploadDocument(auteur,nom_fichier, employe)

			#AYANT DROIT
			# print("DEBUT CREATE AYANT DROIT")
			list_identitie = request.POST.getlist('identitie', None)
			list_noms_ayant_droit = request.POST.getlist('noms_ayant_droit', None)
			list_date_naissance = request.POST.getlist("birthday_ayant", None)
			list_lien_parente = request.POST.getlist("lien_parente", None)
			list_description = request.POST.getlist("description",None)
			list_id = request.POST.getlist("ligne_id", None)


			for i in range(0, len(list_id)):
				if isinstance(list_id[i], int):
					ligne_id = int(list_id[i])
					dao_dependant.toDeleteDependant(ligne_id)

			for i in range(0, len(list_noms_ayant_droit)) :
				# print("get in dependant")
				noms = list_noms_ayant_droit[i]
				lien_parente = list_lien_parente[i]
				description = list_description[i]
				date_naissance_ayant = list_date_naissance[i]
				dependantid = int(list_identitie[i])

				# print("id dependant",dependantid)

				# print("name", noms)

				#models.Model_Dependant.objects.filter(employe = employe).delete()
				date_naissance_ayant = timezone.datetime(int(date_naissance_ayant[6:10]), int(date_naissance_ayant[3:5]), int(date_naissance_ayant[0:2]))
				lien_parente = lien_parente.lower()

				if dependantid == 0 :
					dependant = dao_dependant.toCreateDependant(noms,lien_parente,description,employe.id, None, date_naissance_ayant)
					dependant = dao_dependant.toSaveDependant(auteur,dependant)
				else :
					dependant = dao_dependant.toCreateDependant(noms,lien_parente,description,employe.id, None, date_naissance_ayant)
					dependant = dao_dependant.toUpdateDependant(dependantid,dependant)
				# print(dependant)
			# print("sorti ?")


			if poste != employe.poste:
				#print("lelo ehh", departement_id)
				# Nous créons une première mobilité pour un employé
				dep = dao_unite_fonctionnelle.toGetUniteFonctionnelle(departement_id)
				service = dep.libelle
				fonctions_occupees = poste.designation

				modalites = "Changement de poste"
				direction = dep.unite_fonctionnelle

				#date_entree = request.POST['date_entree']
				#date_sortie = request.POST['date_sortie']

				#print(employe)
				categorie_socio_professionnelle = employe.categorie_employe.categorie
				#print(employe.categorie_employe)


				#date_engagement = timezone.datetime(int(date_engagement[6:10]), int(date_engagement[3:5]), int(date_engagement[0:2]))
				#date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))

				#Ajout de la pondération en fonction occupée
				"""
				Les pondérations sont sur 10 suivant le barême suivant :

				DG = 10
				Autres Directeurs = 8
				Chef de service = 6
				Chef de bureau et Chef de projet = 4
				Assistant = 2

				"""
				ponderation = 0

				if "assistant" in fonctions_occupees.lower():
					ponderation = 2
				elif "projet" in fonctions_occupees.lower() or "bureau" in fonctions_occupees.lower():
					ponderation = 4
				elif "service" in fonctions_occupees.lower():
					ponderation = 6
				elif "directeur" in fonctions_occupees.lower():
					ponderation = 8
				elif fonctions_occupees.lower() == "directeur général" or fonctions_occupees.lower() == "directeur general":
					ponderation = 10
				else:
					ponderation = 0

				type_mobilite = "Modification"
				mobilite=dao_mobilite.toCreateMobilite(direction,service, type_mobilite,fonctions_occupees,ponderation,categorie_socio_professionnelle,modalites,date_engagement,None,ref)
				mobilite=dao_mobilite.toSaveMobilite(auteur, mobilite)

			transaction.savepoint_commit(sid)

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_rh_detail_employe', args=(ref,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		transaction.savepoint_rollback(sid)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		# print('Erreur post modifier Employes')
		# print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_update_employe', args=(ref,)))


def get_modifier_statut_employe(request, ref):
	try:
		permission_number = 442
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		employe = dao_employe.toGetEmploye(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/statut/update.html')
		statutEmploye = dao_StatusDesignationEmploye.toListStatuts()
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modification Statut Employe {}'.format(utilisateur.nom_complet),
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'model': employe,
			'statuts':statutEmploye,
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFICATION STATUT EMPLOYE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Me')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_detail_employe', args=(ref,)))


@transaction.atomic
def post_modifier_statut_employe(request):
	sid = transaction.savepoint()
	ref = int(request.POST["ref"])
	try:
		statutEmploye = int(request.POST["statutEmploye"])
		employe = dao_employe.toGetEmploye(ref)
		employe.statutrh_id = statutEmploye
		if statutEmploye != 1:
			employe.est_actif = False
		employe.save()
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_rh_detail_employe', args=(ref,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		transaction.savepoint_rollback(sid)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST MODIFIER STATUT EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		messages.error(request,e)
		print(e)
		return HttpResponseRedirect(reverse('module_rh_detail_employe', args=(ref,)))




def get_upload_employe(request):
	try:
		permission_number = 73
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des employés",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/employe/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD PIECE COMPTABLE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))


@transaction.atomic
def post_upload_employe(request):
	sid = transaction.savepoint()
	try:
		# print("upload_employe")
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


		# print("Sheet : {} file: {}".format(sheet, file_name))
		df = pd.read_excel(io=file_name, sheet_name=sheet)
		df = df.fillna("") #Replace all nan value by ""

		auteur = identite.utilisateur(request)


		for i in df.index:
			nom = ""
			prenom = ""
			est_particulier = True
			nom_complet = str(df['nom_complet'][i])
			nom_complet = nom_complet.strip()
			matricule = makeStringFromFloatExcel(df['matricule'][i])
			sexe = str(df['genre'][i])
			email = str(df['email'][i])
			phone = str(df['phone'][i])
			arrondissement = ""
			adresse = ""
			categorie = str(df['categorie'][i])
			classification = str(df['classification'][i])
			lieu_travail = str(df['lieu_travail'][i])
			date_engagement = str(df['date_engagement'][i])
			contrat = str(df['contrat'][i])
			date_naissance = str(df['date_naissance'][i])
			education = str(df['education'][i])
			diplome = str(df['diplome'][i])
			numero_ss = str(df['numero_ss'][i])
			code_unite_fonctionnelle = str(df['departement'][i])
			situation_famille = str(df['situation_famille'][i])
			poste_designation = str(df['poste'][i])
			designation_banque = str(df['banque'][i])
			code_banque = makeStringFromFloatExcel(df['code_banque'][i])
			code_guichet = makeStringFromFloatExcel(df['code_guichet'][i])
			numero_compte = makeStringFromFloatExcel(df['numero_compte'][i])
			cle_rib = makeStringFromFloatExcel(df['cle_rib'][i])
			image = ""


			#Fixation valeur modele bulletin deja exista
			bulletin_modele_default = dao_bulletin_modele.toGetBulletinModeleParDefaut()
			modele_bulletin_id = bulletin_modele_default.id if bulletin_modele_default else None

			#lieu_naissance = str(df['lieu_naissance'][i])
			#echelon = str(df['echelon'][i])
			#responsable_id=request.POST["responsable_id"]
			lieu_naissance = ""
			echelon = ""
			responsable_id = None
			# grade = str(df['grade'][i])
			nombre_subordonne = str(df['nombre_subordonne'][i])
			#print("****************************************** All debut GOOOD")

			#TRAITEMENT NON & PRENOM POUR IMPORT EMPLOYE
			tab=[]
			tab2 = []
			listname = nom_complet.split(sep=" ")

			for item in listname:
				if item.isupper():
					tab.append(item)
				else:
					tab2.append(item)
			nom = convert_list_to_string(tab)
			prenom = convert_list_to_string(tab2)

			#TRAITEMENT GENDER
			gender = ""
			sexe.upper() #RENDRE UNIFORME LE SEXE
			if sexe == 'F': gender = 'Feminin'
			elif sexe == 'M': gender = 'Masculin'

			#TRAITEMENT ETAT-CIVIL
			etat_civil = ""
			if situation_famille == 'M': etat_civil = "Marié(e)"
			elif situation_famille == 'C': etat_civil = 'Célibataire'
			elif situation_famille == 'D': etat_civil = 'Divorcé(e)'
			elif situation_famille == 'V': etat_civil = 'Veuf(ve)'
			elif situation_famille == 'UL': etat_civil = 'Union Libre'

			#TRAITEMENT Categorie SOCIO PROFESSIONNEL
			# categorie_socio_pro = ""
			# sizecat = len(categorie)
			# if sizecat == 4:
			# 	categorie_socio_pro = categorie[0]
			# elif sizecat == 5:
			# 	categorie_socio_pro = categorie[0:2]

			# print('Categorie File', categorie_socio_pro)
			# categorieS_id = None
			# categorieS = dao_categorieDesignation.toGetOrCreateCategorie(categorie_socio_pro)
			# print('CAT SOCIO PRO', categorieS)
			# if categorieS != None : categorieS_id = categorieS.id


			# Conversion de la date
			if len(date_naissance) == 10:
				date_naissance = timezone.datetime(int(date_naissance[6:10]), int(date_naissance[3:5]), int(date_naissance[0:2]))
			elif len(date_naissance) > 10:
				date_naissance = timezone.datetime(int(date_naissance[0:4]), int(date_naissance[5:7]), int(date_naissance[8:10]))
			else:
				date_naissance = None

			if len(date_engagement) == 10:
				date_engagement = timezone.datetime(int(date_engagement[6:10]), int(date_engagement[3:5]), int(date_engagement[0:2]))
			elif len(date_engagement) > 10:
				date_engagement = timezone.datetime(int(date_engagement[0:4]), int(date_engagement[5:7]), int(date_engagement[8:10]))
			else:
				date_naissance = None


			unite_fonctionnelle_id = None
			unite_fonctionnelle = dao_unite_fonctionnelle.toGetOrCreateUniteFonctionnelle(auteur, code_unite_fonctionnelle)
			# print("the Unite Fonct", unite_fonctionnelle)
			if unite_fonctionnelle != None : unite_fonctionnelle_id = unite_fonctionnelle.id

			classification_pro = dao_classification_professionnelle.toGetOrCreateClassificationProfessionnelle(auteur, classification)
			# print("the classification_pro I Found", classification_pro)
			classification_pro_id = classification_pro.id if classification_pro else None


			poste_id = None
			poste = dao_poste.toGetOrCreatePoste(auteur,poste_designation, classification_pro_id, nombre_subordonne, unite_fonctionnelle_id)
			# print("the poste I Found", poste)
			if poste != None : poste_id = poste.id

			categorie_id = None
			categorie = dao_categorie_employe.toGetCategorieByLabel(categorie)
			# print("the categorie I Found", categorie)
			if categorie != None : categorie_id = categorie.id

			lieutravail_id = None
			lieu = dao_lieu_travail.toGetOrCreateLieuTravail(auteur,lieu_travail)
			# print('I found Lieu Tra', lieu)
			if lieu != None : lieutravail_id = lieu.id

			diplome_id = None
			diplome = dao_diplome.toGetOrCreatediplome(auteur,diplome)
			# print('I found Diplome', diplome)
			if diplome != None : diplome_id = diplome.id

			est_particulier = True


			#TEST EXISTENCE EMPLOYE AVANT CREATION, SI EMPLOYE EXISTE, ON MET A JOUR LES INFORMATIONS, SINON ON CREE
			# print('Confirme Moi Nom_Complet', nom_complet)
			employe_exist = dao_employe.toGetEmployeByFullName(nom_complet)
			# print("employe exist", employe_exist)
			employe = dao_employe.toCreateEmploye(prenom, nom, nom_complet, "", email, phone, adresse, None, True, None, est_particulier, None, unite_fonctionnelle_id,lieutravail_id, categorie_id,poste_id,None, diplome_id, modele_bulletin_id, None, None)
			if employe_exist != None:
				employe = dao_employe.toUpdateEmploye(employe_exist.id, employe)
			else:
				employe = dao_employe.toSaveEmploye(auteur, employe)
			# print("value of employe after all", employe)

			# CREATION PROFIL RH
			est_enconge = False

			profilrh_id = None
			nationalite = "Congolaise"
			numero_passeport = ""
			numero_identification = ""
			phone_professionnel = ""
			phone_pro2 = ""
			seconde_nationalite = ""
			prisecharge = date_engagement
			est_permanent = True


			profil_agent = dao_profil.toCreateProfil(date_engagement, prisecharge, date_naissance, lieu_naissance,  nationalite, numero_passeport,
													numero_identification,etat_civil,numero_ss,gender, matricule,  email, phone_professionnel,phone,phone_pro2,contrat,est_permanent)

			#SI le profil RH existe déjà, fais la mise à jour, sinon, tu peux récréer!
			if employe != None:
				if employe.profilrh:
					profil = dao_profil.toUpdateProfil(employe.profilrh_id, profil_agent)
					profilrh_id = profil.id
				else:
					profil = dao_profil.toSaveProfil(auteur, profil_agent)
					employe.profilrh_id = profil.id
					employe.save()
					profilrh_id = profil.id
					#ADD EDUCATION
					profil.education = education
					profil.save()
			# print("profil {}".format(i), profil)
			# print()

			#Banque, Compte Banque et RIB
			#Test si la banque est bien renseigné par sa designation et son code
			if (designation_banque and code_banque) :
				banque = dao_banque.toGetOrCreateBank(auteur, designation_banque, code_banque)
				if banque:
					compte_banque_employe = dao_compte_banque_employe.toGetOrCreateCompteBanqueEmploye(auteur, nom_complet, numero_compte, profilrh_id, banque.id)
					if compte_banque_employe:
						rib = dao_rib.toGetOrCreateRIB(auteur, code_guichet, cle_rib, compte_banque_employe.id, banque.id, nom_complet)
						#print("rib created", rib)

			# if profil == None: raise Exception("Un problème est survenu à la création du profil de l'employé")

			# print('********************Fin iteration {} / {}'.format(i, employe))

		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))
	except Exception as e:
		#print("ERREUR POST UPLOAD EMPLOYE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_rh_add_employe"))

def get_upload_mailing_employe(request):
	try:
		permission_number = 73
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import la liste d\'emails des employés",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/employe/upload_mail.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))

@transaction.atomic
def post_upload_email_employe(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		base_dir = settings.BASE_DIR
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
		print("**FICHIER**", sheet)

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		auteur = identite.utilisateur(request)
		for i in df.index:
			nom_complet = str(df['noms'][i])
			nom_complet = nom_complet.strip()
			new_mail = str(df['email'][i])
			tab=[]
			tab2 = []
			listname = nom_complet.split(sep=" ")
			print('Les contenu du fichier', nom_complet +' '+ new_mail)

			for item in listname:
				if item.isupper():
					tab.append(item)
				else:
					tab2.append(item)
			nom = convert_list_to_string(tab)
			prenom = convert_list_to_string(tab2)
			# employe = models.Model_Employe.objects.filter(nom_complet__icontains = nom_employe).first()
			Employe = models.Model_Employe.objects.filter(nom__icontains = nom).first()
			print(Employe)
			# EmployeM = models.Model_Employe()
			if Employe != None:
				Employe.email = new_mail
				Employe.save()


		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD EMAIL EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_get_upload_mailing_employe"))


def get_upload_dependant_employe(request):
	try:
		permission_number = 73
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des dépendants d'employés",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/employe/upload_dependant.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))


@transaction.atomic
def post_upload_dependant(request):
	sid = transaction.savepoint()
	try:
		media_dir = settings.MEDIA_ROOT
		base_dir = settings.BASE_DIR
		media_url = settings.MEDIA_URL
		# #print("*UPLOAD FUNCTION IN ACTION**")

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
		# #print("**FICHIER**", sheet)

		df = pd.read_excel(io=file_name, sheet_name=sheet)
		auteur = identite.utilisateur(request)

		globalSt = None
		for i in df.index:
			numero = str(df['N°'][i])
			statut = str(df['STATUT'][i])
			nom_complet = str(df['AYANT DROIT'][i])
			sexe = str(df['SEXE'][i])
			date_naissance = str(df['DATE DE NAIS'][i])
			# ayant_droit = str(df['AYANT_DROIT'][i])
			description = ""
			# #print('**NOM COMPLET',nom_complet)

			if len(date_naissance) == 10:
				date_naissance = timezone.datetime(int(date_naissance[6:10]), int(date_naissance[3:5]), int(date_naissance[0:2]))
			elif len(date_naissance) > 10:
				date_naissance = timezone.datetime(int(date_naissance[0:4]), int(date_naissance[5:7]), int(date_naissance[8:10]))

			#TRAITEMENT DE RECONNAISSANCE
			list_agent = nom_complet.split()
			nom_employe = list_agent[::len(list_agent)-0]
			# ayant_droit = list_agent.pop(0)
			# ayant_droit = convert_list_to_string(ayant_droit)
			statut = statut.lower()
			nom_employe =convert_list_to_string(nom_employe)
			# #print("**NOM EMPLOYE SEARCH", nom_employe)

			if statut == 'principal':
				employe_id = None
				employe = models.Model_Employe.objects.filter(nom_complet__icontains = nom_employe).first()
				if employe != None :
					globalSt = employe.id
					# #print("**ok EMPLOYE** {}".format(i), employe.nom_complet)
				else:
					globalSt = None
					#print("**KO******************************* EMPLOYE NOT FOUND", nom_employe)

			else:
				if globalSt:
					dependant_exist = dao_dependant.toGetDependantByFullName(nom_complet)
					dependant = dao_dependant.toCreateDependant(nom_complet,statut,description,globalSt,None, date_naissance)
					if dependant_exist:
						dependant = dao_dependant.toUpdateDependant(dependant_exist.id, dependant)
						#print(" Existing Dependant {}".format(i), dependant)
					else:
						dependant = dao_dependant.toSaveDependant(auteur,dependant)
						#print(" New Dependant {}".format(i), dependant)


		transaction.savepoint_commit(sid)
		#print("***FIN UPLOAD***")
		return HttpResponseRedirect(reverse("module_rh_list_employe"))
	except Exception as e:
		#print("ERREUR POST UPLOAD DEPANDANT")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_get_upload_dependant_employe"))

#THIS FUNCTION CONVERT ARRAY TO STRING
def convert_list_to_string(org_list, seperator=' '):
	return seperator.join(org_list)

########################## DOSSIER DU SOCIAL #############################
def get_lister_dossier_social(request):
	try:
		permission_number = 164
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_dossier_social.toListDossierSocial()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_dossier_social.toListDossierSocial(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)

		event = dao_type_evenement_social.toListTypeEvenementSocial()
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des dossiers de la gestion du social',
		'model' : model,
		'view':view,
		'event':event,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/dossier_social/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_dossier_social(request):
	try:
		permission_number = 165
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		model = dao_dossier_social.toListDossierSocial()
		employes = dao_employe.toListEmployes()
		evenement_social = dao_type_evenement_social.toListTypeEvenementSocial()
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Nouveau dossier social',
		'model' : model,
		'evenement_social': evenement_social,
		'employes':employes,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/dossier_social/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

@transaction.atomic
def post_creer_dossier_social(request):
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		employe_id = int(request.POST["employe_id"])
		employe = dao_employe.toGetEmploye(employe_id)
		# responsable_id = int(request.POST["responsable_id"])
		# responsable = dao_employe.toGetEmploye(responsable_id)
		lieu = request.POST["lieu"]
		structure = request.POST["structure"]
		sujet = int(request.POST["sujet"])
		description = request.POST["description"]

		numero_dossier_social = str(dao_dossier_social.toGenerateNumeroDossier())
		#print("FIN POST DOSSIER SOCIAL")

		statute = dao_type_evenement_social.toGetTypeEvenementSocial(sujet)

		#print(statute)

		#toCreateDossierSocial(numero_dossier_social, description, structure, lieu = "", sujet_plainte = "", observation = "", employe = None, responsable = None, mail_envoyé = "", date_fermeture = None, statut = "", alerte = False)
		dossier = dao_dossier_social.toCreateDossierSocial(numero_dossier_social, description,structure, lieu, statute["designation"], "",employe, None, "", None, statute["id"],False)
		dossier = dao_dossier_social.toSaveDossierSocial(auteur.id, dossier)

		docs_dir = 'documents/'
		media_dir = media_dir + '/' + docs_dir

		#1. Doc
		if 'doc' in request.FILES:
			nom_fichier = request.FILES.getlist("doc",None)
			doc=dao_document.toUploadDocument(auteur,nom_fichier, dossier)

		#Envoie du mail au concerné
		#Initialisation du workflow expression
		wkf_task.initializeWorkflow(auteur,dossier)


		#print("DOSSIER SAVED !")
		transaction.savepoint_commit(sid)

		return HttpResponseRedirect(reverse('module_ressources_humaines_details_dossier_social', args=(dossier.id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER DOSSIER SOCIAL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post modifier dossier social')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_add_dossier_social'))

def get_modifier_dossier_social(request,ref):
	try:
		permission_number = 166
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		id = int(ref)
		model = dao_dossier_social.toGetDossierSocial(id)
		employe = dao_employe.toListEmployes()
		evenement_social = dao_type_evenement_social.toListTypeEvenementSocial()
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier Dossier N° {}'.format(model.numero_dossier_social),
		'model' : model,
		'employe':employe,
		'evenement_social': evenement_social,
		'roles':roles,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/dossier_social/update.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

@transaction.atomic
def post_modifier_dossier_social(request):
	sid = transaction.savepoint()
	id = int(request.POST["ref"])

	try:

		auteur = identite.utilisateur(request)
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL
		employe_id = int(request.POST["employe_id"])
		employe = dao_employe.toGetEmploye(employe_id)
		responsable_id = int(request.POST["responsable_id"])
		responsable = dao_employe.toGetEmploye(responsable_id)
		lieu = request.POST["lieu"]
		structure = request.POST["structure"]
		sujet = int(request.POST["sujet"])
		description = request.POST["description"]
		#print("ref ",id)

		#print("FIN POST MODIFIER DOSSIER SOCIAL")
		dossier_p = models.Model_Dossier_Social.objects.get(id = id)
		#print(dossier.numero_dossier_social, dossier.lieu)

		statute = dao_type_evenement_social.toGetTypeEvenementSocial(sujet)

		#toCreateDossierSocial(numero_dossier_social, description, structure, lieu = "", sujet_plainte = "", observation = "", employe = None, responsable = None, mail_envoyé = "", date_fermeture = None, statut = "", alerte = False)
		dossier = dao_dossier_social.toCreateDossierSocial(dossier_p.numero_dossier_social, description,structure, lieu, statute["designation"], "",employe, responsable, "", None, statute["id"],False)
		dossier = dao_dossier_social.toUpdateDossierSocial(id, dossier)

		#print(dossier.lieu)

		docs_dir = 'documents/'
		media_dir = media_dir + '/' + docs_dir

		#print("documents uploader debut ")

		#1. Doc
		if 'doc' in request.FILES:
			#print("inside")
			nom_fichier = request.FILES.getlist("doc",None)
			doc=dao_document.toUploadDocument(auteur,nom_fichier, dossier)

		#print("documents uploader Fin ")

		# dossier.employe.id = employe.id
		# dossier.responsable.id = responsable.id
		# dossier.lieu = lieu
		# dossier.structure = structure
		# dossier.sujet = sujet
		# dossier.description = description
		# #toCreateDossierSocial(numero_dossier_social, description, structure, lieu = "", sujet_plainte = "", observation = "", employe = None, responsable = None, mail_envoyé = "", date_fermeture = None, statut = "", alerte = False)
		# # dossier = dao_dossier_social.toCreateDossierSocial(dossier.numero_dossier_social, description,structure, lieu, sujet, "",employe, responsable, "", None, "",False)

		# # dossier = dao_dossier_social.toUpdateDossierSocial(id, dossier)
		# dossier.save()

		#Envoie du mail au concerné


		#print("DOSSIER UPDATED !")
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressources_humaines_details_dossier_social', args=(id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER DOSSIER SOCIAL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur post modifier dossier social')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_update_dossier_social', args=(id,)))

def get_upload_dossier_social(request):
	try:
		permission_number = 164
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des dossiers sociaux",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/dossier_social/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD DOSSIER SOCIAL")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_dossier_social"))


@transaction.atomic
def post_upload_dossier_social(request):
	sid = transaction.savepoint()
	try:
		#print("upload_dossier_social")
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
			lieu = str(df['lieu'][i])
			description = str(df['description'][i])
			type_evenement = int(df['type_evenement'][i])
			structure = str(df['structure'][i])

			matricule = str(df['matricule'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				#print("employe {}".format(employe))

			numero_dossier_social = str(dao_dossier_social.toGenerateNumeroDossier())

			statut = dao_type_evenement_social.toGetTypeEvenementSocial(type_evenement)

			dossier = dao_dossier_social.toCreateDossierSocial(numero_dossier_social, description, structure, lieu, statut["designation"], "", employe, None, "", None, statut["id"], False)
			dossier = dao_dossier_social.toSaveDossierSocial(auteur.id, dossier)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_dossier_social"))
	except Exception as e:
		#print("ERREUR POST UPLOAD DOSSIER SOCIAL")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD DOSSIER SOCIAL \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressources_humaines_add_dossier_social"))


def get_details_dossier_social(request, ref):
	try:
		permission_number = 164
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		id = int(ref)
		#print("id ",id)
		model = dao_dossier_social.toGetDossierSocial(id)

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)
		# #print(model.sujet_plainte)
		documents = dao_document.toListDocumentbyObjetModele(model)
		# evenement = None
		# for item in dao_type_evenement_social.toListTypeEvenementSocial():
		# 	if item["id"] == model.statute:
		# 		evenement = item["designation"]
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Dossier {} de l\'employé {}'.format(model.numero_dossier_social, model.employe),
		'model' : model,
		'historique' : historique,
		'etapes_suivantes' : transition_etape_suivant,
		'content_type_id':content_type_id,
		"utilisateur" : utilisateur,
		"signee": signee,
		'roles':groupe_permissions,
		'documents':documents,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' :modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/dossier_social/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER UN EMPLOYE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur detailler un Employe')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_print_rapport_dossier_social(request, ref):
	try:
		permission_number = 164
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		id = int(ref)
		#print("id ",id)
		model = dao_dossier_social.toGetDossierSocial(id)

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)
		# #print(model.sujet_plainte)
		documents = dao_document.toListDocumentbyObjetModele(model)
		# evenement = None
		# for item in dao_type_evenement_social.toListTypeEvenementSocial():
		# 	if item["id"] == model.statute:
		# 		evenement = item["designation"]
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Dossier {} de l\'employé {}'.format(model.numero_dossier_social, model.employe),
		'model' : model,
		'historique' : historique,
		'etapes_suivantes' : transition_etape_suivant,
		'content_type_id':content_type_id,
		"utilisateur" : utilisateur,
		'documents':documents,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' :modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5,
		'datenow':datetime.datetime.now()
		}
		return weasy_print("ErpProject/ModuleRessourcesHumaines/reporting/dossier_social.html", "dossier_social.pdf", context)

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {} ::\nERREUR LORS DE DETAILLER UN EMPLOYE \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")

		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))


######################### FIN DOSSIER DU SOCIAL ##########################

# DEPARTEMENT CONTROLLERS
def get_lister_departement(request):
	try:
		permission_number = 77
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_type_unite_fonctionnelle.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		# #print('rrrrrrrrrrrrrrrrrrrrrrrr')
		# for m in model:
		# 	#print("Désignation : {} ,  ID : {} ".format(m.libelle, m.id))

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des organisations',
		'model' : model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/departement/list_type.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_departement_of_type(request, ref):
	try:
		permission_number = 77
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		ref = int(ref)
		type_unite = dao_type_unite_fonctionnelle.toGet(ref)
		print("type_unite ", type_unite)
		print("unite fonct", dao_unite_fonctionnelle.toListUniteFonctionnelleType(type_unite.id))
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_unite_fonctionnelle.toListUniteFonctionnelleType(type_unite.id), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#

		#Traitement des vues
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		#Pagination
		model = pagination.toGet(request, model)

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des organisations de type {}'.format(type_unite.designation),
		'model' : model,
		'type_id' : type_unite.id,
		'view': view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/departement/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_departement(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False
		ref = int(ref)
		type_unite = None
		#Dans le cas où un type particulier est passé en paramètre
		if ref != 0:
			type_unite = dao_type_unite_fonctionnelle.toGet(ref)
		type_unite_fonctionnelles = dao_type_unite_fonctionnelle.toList()

		employes = dao_employe.toListEmployes()
		unite = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Nouvelle organisation',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'employes': employes,
		'type_unite': type_unite,
		'type_unite_fonctionnelles': type_unite_fonctionnelles,
		'departements':unite,
		'isPopup':isPopup,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/departement/add.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_employe"))

def post_creer_departement(request):

	try:
		libelle = request.POST['libelle']
		description = request.POST['description']
		niveau = 0
		type_id = request.POST['type_id']
		type = ''
		unite_fonctionnelle_id = request.POST['unite_fonctionnelle_id']
		code = request.POST['code']
		responsable_id = None
		isPopup = request.POST['isPopup']

		est_racine = False

		auteur = identite.utilisateur(request)

		unite = dao_unite_fonctionnelle.toCreateUniteFonctionnelle(libelle,est_racine,description,niveau,type,unite_fonctionnelle_id,responsable_id, type_id, code)
		unite = dao_unite_fonctionnelle.toSaveUniteFonctionnelle(auteur,unite)

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")

		if isPopup == 'False':
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_rh_detail_departement', args=(unite.id,)))
		else:
			return HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer Département')
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'exécution")
		return HttpResponseRedirect(reverse('module_rh_list_employe'))


def get_details_departement(request,ref):
	try:
		permission_number = 77
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref=int(ref)
		unite=dao_unite_fonctionnelle.toGetUniteFonctionnelle(ref)
		postes = dao_poste.toListPostesByDepartement(unite.id)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/departement/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,unite)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Détails sur "{}" '.format(unite.code),
			'model' : unite,
			'postes' : postes,
			'utilisateur' : utilisateur,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur détailler Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_list_departement'))

def get_modifier_departement(request, ref):

	try:
		permission_number = 78
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		departement = dao_unite_fonctionnelle.toGetUniteFonctionnelle(id)
		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		employes = dao_employe.toListEmployesOfDepartement(ref)
		type_unite_fonctionnelles = dao_type_unite_fonctionnelle.toList()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % departement.code,
			'model' : departement,
			'departements':departements,
			'type_unite_fonctionnelles':type_unite_fonctionnelles,
			'employes':employes,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/departement/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Postes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))

def post_modifier_departement(request):
	id = int(request.POST["ref"])
	try:
		libelle = request.POST['libelle']
		description = request.POST['description']
		niveau = 0
		code = request.POST['code']
		type = ""
		type_unite_fonctionnelle_id = request.POST['type_unite_fonctionnelle_id']
		unite_fonctionnelle_id = request.POST['unite_fonctionnelle_id']
		responsable_id = request.POST["responsable_id"]

		if responsable_id == "":
			responsable_id = None

		if unite_fonctionnelle_id == "":
			unite_fonctionnelle_id = None

		est_racine = False


		auteur = identite.utilisateur(request)

		unite = dao_unite_fonctionnelle.toCreateUniteFonctionnelle(libelle,est_racine,description,niveau,type,unite_fonctionnelle_id,responsable_id, type_unite_fonctionnelle_id, code)
		is_done = dao_unite_fonctionnelle.toUpdateUniteFonctionnelle(id,unite)

		if is_done == True :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_rh_detail_departement', args=(id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement des modifications apportées sur l'organisation !")
			return HttpResponseRedirect(reverse('module_rh_update_departement', args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Post Créer Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_update_departement', args=(id,)))

def get_upload_departement(request):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des organisations",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/departement/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD PIECE COMPTABLE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_list_departement"))


@transaction.atomic
def post_upload_departement(request):
	sid = transaction.savepoint()
	try:
		#print("upload_departement")
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
			libelle = str(df['libelle'][i])
			description = str(df['description'][i])
			est_racine = str(df['est_racine'][i])
			niveau = str(df['niveau'][i])

			type_unite_id = None
			type_unite = str(df['type'][i])
			type_unite = models.Model_TypeUnite_fonctionnelle.objects.filter(designation__icontains = type_unite).first()
			if type_unite != None : type_unite_id = type_unite.id

			if "oui" in est_racine.lower():
				est_racine = True
			else : est_racine = False

			unite_fonctionnelle_id = None
			responsable_id = None

			unite_fonctionnelle = dao_unite_fonctionnelle.toCreateUniteFonctionnelle(libelle, est_racine, description, niveau, "", unite_fonctionnelle_id, responsable_id)
			unite_fonctionnelle = dao_unite_fonctionnelle.toSaveUniteFonctionnelle(auteur, unite_fonctionnelle)

			unite_fonctionnelle.type_unite_fonctionnelle_id = type_unite_id
			unite_fonctionnelle.save()
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_rh_list_departement"))
	except Exception as e:
		#print("ERREUR POST UPLOAD DEPARTEMENT")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD DEPARTEMENT \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_rh_list_employe"))


# POSTE CONTROLLER
def get_lister_postes(request):
	try:
		permission_number = 81
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_poste.toListPostes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_poste.toListPostes(), permission_number, groupe_permissions, identite.utilisateur(request))
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
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des postes',
			'model' : model,
			'view':view,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/poste/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Poste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))


def get_details_poste(request, ref):

	try:
		permission_number = 81
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		poste = dao_poste.toGetPoste(ref)
		documents = dao_document.toListDocumentbyObjetModele(poste)
		#print(documents)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,poste)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : poste.designation,
			'model' : poste,
			'documents':documents,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/poste/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Détailler Poste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))

def get_creer_poste_of_departement(request,ref):
	try:
		permission_number = 80
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		ref = int(ref)

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		departement = dao_unite_fonctionnelle.toGetUniteFonctionnelle(ref)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Nouveau poste',
			'menu' : 5,
			'departement' : departement,
			"modules" : modules,
			'isPopup': isPopup,
			'organisation': dao_organisation.toGetMainOrganisation(),
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/departement/poste/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))

def post_creer_poste_of_departement(request):
	departement_id = int(request.POST["departement"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		isPopup = request.POST['isPopup']

		poste_dao = dao_poste.toCreatePoste(auteur, designation, description, departement_id)
		poste = dao_poste.toSavePoste(poste_dao)

		if 'document_upload' in request.FILES:
			nom_fichier = request.FILES.getlist("document_upload",None)
			doc=dao_document.toUploadDocument(auteur,nom_fichier, poste)

		if poste != None :
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_rh_detail_departement', args=(departement_id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du poste !")
			return HttpResponseRedirect(reverse('module_rh_detail_departement', args=(departement_id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Postes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_detail_departement', args=(departement_id,)))

def get_modifier_poste_of_departement(request, idt, ref):

	try:

		permission_number = 82
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		idt = int(idt)
		poste = dao_poste.toGetPoste(id)
		departement = dao_unite_fonctionnelle.toGetUniteFonctionnelle(idt)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % poste.designation,
			'model' : poste,
			'departement' : departement,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'menu' : 5,
			'utilisateur' : identite.utilisateur(request)
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/departement/poste/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Postes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))

def post_modifier_poste_of_departement(request):
	id = int(request.POST["ref"])
	idt = int(request.POST["idt"])
	#print(request.POST)
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		departement_id = int(request.POST["departement"])

		poste = dao_poste.toCreatePoste(auteur, designation, description, departement_id)
		is_done = dao_poste.toUpdatePoste(id, poste)
		if is_done == True :
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_ressources_humaines_detail_poste_from_department', args=(idt,id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement des modifications apportées sur le poste !")
			return HttpResponseRedirect(reverse('module_ressources_humaines_update_poste_from_department', args=(idt,id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Postes')
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_poste_from_department', args=(idt,id,)))

def get_details_poste_of_departement(request, idt,ref):

	try:
		permission_number = 81
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		idt = int(idt)
		poste = dao_poste.toGetPoste(ref)
		departement = dao_unite_fonctionnelle.toGetUniteFonctionnelle(idt)
		documents = dao_document.toListDocumentbyObjetModele(poste)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,poste)



		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : poste.designation,
			'model' : poste,
			'departement':departement,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/departement/poste/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Détailler Poste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))

def get_creer_poste(request):
	try:
		permission_number = 80
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET:
			isPopup = True
		else:
			isPopup = False

		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Nouveau poste',
			'menu' : 5,
			'departements' : departements,
			"modules" : modules,
			'isPopup': isPopup,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/poste/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER DEPARTEMENT \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Département')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))

@transaction.atomic
def post_creer_poste(request):
	sid = transaction.savepoint()
	try:
		base_dir = settings.BASE_DIR
		media_dir = settings.MEDIA_ROOT
		media_url = settings.MEDIA_URL

		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		departement_id = int(request.POST["departement"])
		isPopup = request.POST['isPopup']

		poste_dao = dao_poste.toCreatePoste(auteur, designation, description, departement_id)
		poste = dao_poste.toSavePoste(poste_dao)

		url = '<a class="lien chargement-au-click" href="/ressourceshumaines/poste/item/'+ str(poste.id) +'/">'+ poste.designation + '</a>'
		poste.url = url
		#print("in post creer")
		poste.save()

		if 'document_upload' in request.FILES:
			nom_fichier = request.FILES.getlist("document_upload",None)
			doc=dao_document.toUploadDocument(auteur,nom_fichier, poste)


		if poste != None :
			transaction.savepoint_commit(sid)
			if isPopup == 'False':
				messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
				return HttpResponseRedirect(reverse('module_ressources_humaines_details_poste', args=(poste.id,)))
			else:
				return HttpResponse('<script type="text/javascript">window.close();</script>')
		else :
			transaction.savepoint_rollback(sid)
			if isPopup == 'False' :

				messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du poste !")
				return HttpResponseRedirect(reverse('module_ressources_humaines_add_poste'))
			else:
				return HttpResponse('<script type="text/javascript">window.close();</script>')
	except Exception as e:
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE CREER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Créer Postes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_add_poste'))

def get_modifier_poste(request, ref):

	try:

		permission_number = 82
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response


		id = int(ref)
		poste = dao_poste.toGetPoste(id)
		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()
		documents = dao_document.toListDocumentbyObjetModele(poste)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % poste.designation,
			'model' : poste,
			'departements' : departements,
			'documents':documents,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'menu' : 5,
			'utilisateur' : identite.utilisateur(request)
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/poste/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Modifier Postes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_postes'))
@transaction.atomic
def post_modifier_poste(request):
	sid = transaction.savepoint()
	id = int(request.POST["ref"])
	try:

		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		departement_id = int(request.POST["departement"])

		poste = dao_poste.toCreatePoste(auteur, designation, description, departement_id)
		is_done = dao_poste.toUpdatePoste(id, poste)
		if is_done == False :
			raise Exception("Une erreur est survenue lors de l'enregistrement des modifications apportées sur le poste !")

		poste = dao_poste.toGetPoste(id)

		if 'document_upload' in request.FILES:
			nom_fichier = request.FILES.getlist("document_upload",None)
			doc=dao_document.toUploadDocument(auteur,nom_fichier, poste)
		messages.add_message(request, messages.SUCCESS, "L'opération est effectuée avec succès")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse('module_ressources_humaines_details_poste', args=(id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER POSTES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		transaction.savepoint_rollback(sid)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_update_poste', args=(id,)))

def get_upload_poste(request):
	try:
		permission_number = 80
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des postes",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/poste/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD POSTE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_postes"))


@transaction.atomic
def post_upload_poste(request):
	sid = transaction.savepoint()
	try:
		#print("upload_poste")
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

			departement_id = None
			departement = str(df['departement'][i])
			departement = models.Model_Unite_fonctionnelle.objects.filter(libelle__icontains = departement).first()
			if departement != None : departement_id = departement.id

			poste_dao = dao_poste.toCreatePoste(auteur, designation, description, departement_id)
			poste = dao_poste.toSavePoste(poste_dao)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_postes"))
	except Exception as e:
		#print("ERREUR POST UPLOAD POSTE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD POSTE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressources_humaines_add_poste"))

#Prets
def get_lister_prets(request):

	try:
		permission_number = 201
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_pret.toListPret()

		#Filtrage des regles + fixation sur les prêts de l'employé uniquement
		print("utilisateur", utilisateur, utilisateur.id)
		model = dao_model.toListModel(dao_pret.toListPretOfEmploye(utilisateur.id), permission_number, groupe_permissions, identite.utilisateur(request))

		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"

		#Pagination
		model = pagination.toGet(request, model)


		context = {
			'title' : "Liste des prêts de {0}".format(utilisateur.nom_complet),
			'model' : model,
			'view': view,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'sous_modules':sous_modules,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/pret/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print('Erreut Get Liste')
		print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))

def get_creer_pret(request):
	try:
		permission_number = 204
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		config_payroll = dao_config_payroll.toGetMainConfigPayroll()
		nbre_mensualite = 10
		taux_interet = 0
		if config_payroll:
			nbre_mensualite = config_payroll.nbre_mensualite
			taux_interet = config_payroll.taux_interet

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Demande de prêt',
			'reference': dao_pret.toGenerateNumero(),
			'devise_ref' : dao_devise.toGetDeviseReference(),
			'devises' : dao_devise.toListDevisesActives(),
			'nbre_mensualite': nbre_mensualite,
			'taux_interet': taux_interet,
			#'rubriques': dao_rubrique.toListRubriques(),
			'rubrique': dao_rubrique.toGetRubriqueRemboursementPret(),
			'employes' : dao_employe.toListEmployes(),
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/pret/add.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_pret'))


def post_valider_pret(request):
	try:
		# droit="CREER_FACTURE_FOURNISSEUR"
		# modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)
		permission_number = 204
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
		taux_interet = makeFloat(request.POST["taux_interet"])
		taux_valeur = float(taux_interet) / 100
		description = request.POST["description"]
		rubrique_id = request.POST["rubrique_id"]

		devise = dao_devise.toGetDevise(devise_id)
		rubrique = dao_rubrique.toGetRubrique(rubrique_id)

		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			files = request.FILES.getlist("document_upload",None)




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
			#'document_upload':files,
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
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 23
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/pret/validate.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		print("ERREUR")
		print(e)
		messages.error(request,"Vérifiez les données saisies")
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_pret"))


@transaction.atomic
def post_creer_pret(request) :
	sid = transaction.savepoint()
	try:
		auteur = identite.utilisateur(request)

		reference = request.POST["reference"]
		date_premiere_echeance = request.POST["date_premiere_echeance"]
		devise_id = request.POST["devise_id"] if (request.POST["devise_id"] and request.POST["devise_id"] != 'None' ) else None
		montant = makeFloat(request.POST["montant"])
		employe_id = request.POST["employe_id"] if (request.POST["employe_id"] and request.POST["employe_id"] != 'None' ) else None
		nbre_mensualite = makeFloat(request.POST["nbre_mensualite"])
		description = request.POST["description"]
		taux_interet = makeFloat(request.POST["taux_interet"])
		taux_valeur = float(taux_interet) / 100
		rubrique_id = request.POST["rubrique_id"] if (request.POST["rubrique_id"] and request.POST["rubrique_id"] != 'None' ) else None

		#conversion de la date
		date_premiere_echeance = timezone.datetime(int(date_premiere_echeance[6:10]), int(date_premiere_echeance[3:5]), int(date_premiere_echeance[0:2]))

		pret = dao_pret.toCreatePret(reference,montant, devise_id, nbre_mensualite, employe_id, description, date_premiere_echeance, taux_valeur, rubrique_id)
		pret = dao_pret.toSavePret(auteur, pret)

		### Début Enregistrement du document
		if 'document_upload' in request.FILES:
			print("yessssssssssssssssssssss")
			files = request.FILES.getlist("document_upload",None)
			print("files", files)
			dao_document.toUploadDocument(auteur, files, pret)


		#Initialisation du workflow expression
		wkf_task.initializeWorkflow(auteur,pret)

		transaction.savepoint_commit(sid)

		#print("Pret cree ID {}".format(pret.id))
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_details_pret', args=(pret.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		transaction.savepoint_rollback(sid)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		print('Erreut Get Creer')
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la création du prêt")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_pret'))


def get_modifier_pret(request, ref):
	try:
		permission_number = 202
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
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/pret/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU MODIFIER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Modifier')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_pret'))

def post_modifier_pret(request):
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
			return HttpResponseRedirect(reverse('module_ressourceshumaines_details_pret', args=(id,)))
		else : return HttpResponseRedirect(reverse('module_ressourceshumaines_update_pret', args=(id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU POST MODIFIER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Post Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_update_pret', args=(id,)))

def get_details_pret(request, ref):
	try:
		permission_number = 201
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		pret = dao_pret.toGetPret(ref)
		#reste_a_payer_periode = dao_pret.toGetResttoPayToDate(pret.id)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,pret)

		lignes_remboursement = []
		lignes_paiement_pret = []
		lignes_paiements = dao_ligne_paiement_pret.toListLignePaiementOfPret(ref)

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

		montant_anterieur = 0
		for ligne in lignes_paiements:
			uneligne = {
				'created_at': ligne.created_at,
				'montant': ligne.montant,
				'mensualite': ligne.montant,
				'devise_iso': devise.symbole_devise,
				'prelevement_anterieur': montant_anterieur,
				'montant_du_prelevement': ligne.montant,
				'reste_a_recouvrer': montant - montant_anterieur - ligne.montant
			}
			montant_anterieur += ligne.montant
			lignes_paiement_pret.append(uneligne)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : pret.reference,
			'model' : pret,
			'lignes_remboursement': lignes_remboursement,
			'lignes_paiement_pret': lignes_paiement_pret,
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
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/pret/item.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_pret'))

#Paiement Interne
def get_lister_paiement_internes(request):
	try:
		permission_number = 205
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_paiement_interne.toListPaiements()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_paiement_interne.toListPaiements(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Liste des paiements internes",
			'model' : model,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			#"can_create" : dao_droit.toGetDroitRole('CREER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/paiement_interne/list.html")
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU LISTE PAIEMENT INTERNE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))

def get_details_paiement_interne(request, ref):
	try:
		dpermission_number = 205
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		ref = int(ref)
		paiement = dao_paiement_interne.toGetPaiement(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,paiement)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : paiement.designation,
			'model' : paiement,
			"utilisateur" : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			#"can_create" : dao_droit.toGetDroitRole('CREER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_delete" : dao_droit.toGetDroitRole('SUPPRIMER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			#"can_update" : dao_droit.toGetDroitRole('MODIFIER_paiement_interne_DE_MESURE',nom_role,utilisateur.nom_complet),
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 8
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/paiement_interne/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU DETAIL PAIEMENT INTERNE\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_paiement_interne'))

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
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressources_humaines_details_lotbulletin', args=(dossier_id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		transaction.savepoint_rollback(sid)
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_paiement_interne'))

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
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressources_humaines_details_lotbulletin', args=(dossier_id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DU POST CREER pret\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		transaction.savepoint_rollback(sid)
		#print('Erreut Get Creer')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_paiement_interne'))

#Fonction pour recuperer les allocations à payer du mois en cours
def get_allocations_a_payer(dossier):
	alloc = []
	conges = dao_conge.toListCongeApayer()

	for conge in conges:
		#print(conge)
		if conge.date_allocation.strftime("%m-%Y") == dossier.date_dossier.strftime("%m-%Y") :
			element = {
				'conge_id':conge.id,
				'conge':conge,
				'employe_id':conge.employe.id,
				'employe':conge.employe.nom_complet,
				'montant':conge.montant_allocation,
				'symbole_devise':conge.devise_allocation.symbole_devise,
				'devise_id':conge.devise_allocation.id
			}
			alloc.append(element)
	return alloc

def get_prets_a_recuperer(dossier):
	prets_a_payer = []
	prets = dao_pret.toListPretNoPaidOfDossier(dossier)
	#prets = dao_pret.toListPretActif()

	for pret in prets:
		#print(pret)
		montant = 0
		if pret.tranche_mensuelle > pret.rest_to_pay : montant = pret.rest_to_pay
		else : montant = pret.tranche_mensuelle
		element = {
			'pret_id': pret.id,
			'pret': pret,
			'employe_id': pret.employe.id,
			'employe': pret.employe.nom_complet,
			'montant': montant,
			'symbole_devise': pret.devise.symbole_devise,
			'devise_id': pret.devise.id
		}
		prets_a_payer.append(element)
	return prets_a_payer

## DataTables Server Side
class EmployeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Employe.objects.all()
	serializer_class = serializer.EmployeSerializer


class DepartementViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Unite_fonctionnelle.objects.all()
	serializer_class = serializer.UniteFonctionnelleSerializer

class PosteViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Poste.objects.all()
	serializer_class = serializer.PosteSerializer

class LotBulletinViewSet(viewsets.ModelViewSet):
	queryset = models.Model_LotBulletins.objects.all()
	serializer_class = serializer.LotBulletinSerializer

class BulletinViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Bulletin.objects.all()
	serializer_class = serializer.BulletinSerializer

class ElementBulletinViewSet(viewsets.ModelViewSet):
	queryset = models.Model_ElementBulletin.objects.all().order_by("sequence")
	serializer_class = serializer.ElementBulletinSerializer

class BaremeViewSet(viewsets.ModelViewSet):
	queryset = models.Model_Bareme.objects.all().order_by("designation")
	serializer_class = serializer.BaremeSerializer

class ProfilViewSet(viewsets.ModelViewSet):
	queryset = models.Model_ProfilPaye.objects.all()
	serializer_class = serializer.ProfilPayeSerializer






"""
def get_lister_demande_achat(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))

	model = dao_demande_achat.toListDemandeAchat()
	context ={
	'title' : 'Liste de demande_achat',
	'model' : model,
	'utilisateur' : identite.utilisateur(request),
	'modules' : dao_module.toListModulesInstalles(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
	'menu' : 5
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/demande_achat/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_demande_achat(request):
	is_connect=identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))

	context ={
	'title' : 'Nouvelle demande_achat',
	'utilisateur' : identite.utilisateur(request),
	'modules' : dao_module.toListModulesInstalles(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
	'menu' : 5
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/demande_achat/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_demande_achat(request):

	try:
		numero_demande = request.POST['numero_demande']
		date_demande = request.POST['date_demande']
		description = request.POST['description']
		requete_id = request.POST['requete_id']
		employe_id = request.POST['employe_id']

		auteur = identite.utilisateur(request)

		demande_achat=dao_demande_achat.toCreateDemandeAchat(numero_demande,date_demande,description,requete_id,employe_id)
		demande_achat=dao_demande_achat.toSaveDemandeAchat(auteur,demande_achat)
		HttpResponseRedirect(reverse('module_arpce_list_demande_achat'))
	except Exception as e:
		module='ModuleRH'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
	returnHttpResponseRedirect(reverse('module_arpce_add_demande_achat'))


def get_details_demande_achat(request,ref):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))
	try:
		ref=int(ref)
		demande_achat=dao_demande_achat.toGetDemandeAchat(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/demande_achat/item.html')
		context ={
		'title' : 'Détails d une demande_achat',
		'demande_achat' : demande_achat,
		'utilisateur' : identite.utilisateur(request),
		'modules' : dao_module.toListModulesInstalles(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRH'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES Détails\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		return HttpResponseRedirect(reverse('module_arpce_list_demande_achat'))

def get_lister_ligne_demande_achat(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))

	model = dao_ligne_demande_achat.toListLigneDemandeAchat()
	context ={
	'title' : 'Liste de ligne_demande_achat',
	'model' : model,
	'utilisateur' : identite.utilisateur(request),
	'modules' : dao_module.toListModulesInstalles(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
	'menu' : 5
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ligne_demande_achat/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_ligne_demande_achat(request):
	is_connect=identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))

	context ={
	'title' : 'Nouvelle ligne_demande_achat',
	'utilisateur' : identite.utilisateur(request),
	'modules' : dao_module.toListModulesInstalles(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
	'menu' : 5
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ligne_demande_achat/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_ligne_demande_achat(request):

	try:
		quantite_demande = request.POST['quantite_demande']
		prix_unitaire = request.POST['prix_unitaire']
		article_id = request.POST['article_id']
		demande_id = request.POST['demande_id']

		auteur = identite.utilisateur(request)

		ligne_demande_achat=dao_ligne_demande_achat.toCreateLigneDemandeAchat(quantite_demande,prix_unitaire,article_id, demande_id)
		ligne_demande_achat=dao_ligne_demande_achat.toSaveLigneDemandeAchat(auteur, ligne_demande_achat)
		HttpResponseRedirect(reverse('module_arpce_list_ligne_demande_achat'))
	except Exception as e:
		module='ModuleRH'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
	returnHttpResponseRedirect(reverse('module_arpce_add_ligne_demande_achat'))


def get_details_ligne_demande_achat(request,ref):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))
	try:
		ref=int(ref)
		ligne_demande_achat=dao_ligne_demande_achat.toGetLigneDemandeAchat(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ligne_demande_achat/item.html')
		context ={
		'title' : 'Détails d une ligne_demande_achat',
		'ligne_demande_achat' : ligne_demande_achat,
		'utilisateur' : identite.utilisateur(request),
		'modules' : dao_module.toListModulesInstalles(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRH'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES Détails\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		return HttpResponseRedirect(reverse('module_arpce_list_ligne_demande_achat'))

def get_lister_requete_demande(request):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))

	model = dao_requete_demande.toListRequeteDemande()
	context ={
	'title' : 'Liste de requete_demande',
	'model' : model,
	'utilisateur' : identite.utilisateur(request),
	'modules' : dao_module.toListModulesInstalles(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
	'menu' : 5
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete_demande/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_requete_demande(request):
	is_connect=identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))

	context ={
	'title' : 'Nouvelle requete_demande',
	'utilisateur' : identite.utilisateur(request),
	'modules' : dao_module.toListModulesInstalles(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
	'menu' : 2
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete_demande/add.html')
	return HttpResponse(template.render(context, request))



	try:
		designation = request.POST['designation']
		type_requete = request.POST['type_requete']
		description = request.POST['description']

		requete_demande=dao_requete_demande.toCreateRequeteDemande(designation,type_requete,description)
		requete_demande=dao_requete_demande.toSaveRequeteDemande(requete_demande)
		HttpResponseRedirect(reverse('module_arpce_list_requete_demande'))
	except Exception as e:
		module='ModuleRH'
		monLog.error("{} :: {}::\nErreur lors de l'enregistrement\n {}".format(auteur.nom_complet, module, e))
		#print('Erreur lors de l enregistrement')
		#print(e)
	returnHttpResponseRedirect(reverse('module_arpce_add_requete_demande'))


def get_details_requete_demande(request,ref):
	is_connect = identite.est_connecte(request)
	if is_connect == False: return HttpResponseRedirect(reverse('backoffice_connexion'))
	try:
		ref=int(ref)
		requete_demande=dao_requete_demande.toGetRequete_demande(ref)
		template = loader.get_template('ErpProject/ModuleArpce/requete_demande/item.html')
		context ={'title' : 'Détails d une requete_demande','requete_demande' : requete_demande,'utilisateur' : identite.utilisateur(request),'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_ARPCE,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRH'
		monLog.error("{} :: {}::\nERREUR LORS DU CHARGEMENT DES Détails\n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Get Detail')
		#print(e)
		return HttpResponseRedirect(reverse('module_arpce_list_requete_demande'))

"""

def get_lister_categorie_employe(request):
	permission_number = 209
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_categorie_employe.toListCategorie_employe()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_categorie_employe.toListCategorie_employe(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Catégorie & Echelon','model' : model,'view':view,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/categorie_employe/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_categorie_employe(request):
	permission_number = 210
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	echelons=dao_EchelonDesignation.toListEchelon()

	categories=dao_categorieDesignation.toListcategories()

	context ={'modules':modules,'sous_modules':sous_modules,'modules':modules,'sous_modules':sous_modules,'title' : 'Ajouter une catégorie','utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'echelons':echelons,
	'categories':categories,
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/categorie_employe/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_categorie_employe(request):

	try:
		categorie_id = request.POST['categorie']
		echelon_id = request.POST['echelon']
		salaire_base = makeFloat(request.POST['salaire_base'])
		devise_id = request.POST['devise_id']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		categorie_employe=dao_categorie_employe.toCreateCategorie_employe(categorie_id,echelon_id,salaire_base,devise_id,description)
		categorie_employe=dao_categorie_employe.toSaveCategorie_employe(auteur, categorie_employe)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_categorie_employe'))
	except Exception as e:
		#print('Erreur post_creer_categorie_employe')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER CATEGORIE_EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_update_categorie_employe'))


def get_details_categorie_employe(request,ref):
	permission_number = 209
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		categorie_employe=dao_categorie_employe.toGetCategorie_employe(ref)
		# print('categorie',categorie_employe)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/categorie_employe/item.html')
		# historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categorie_employe)

		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Détails sur "{} {}" '.format(categorie_employe.categorie, categorie_employe.echelon),'categorie_employe' : categorie_employe,'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		# "historique": historique,
		# "etapes_suivantes": etapes_suivantes,
		# "signee": signee,
		# "content_type_id": content_type_id,
		# "documents": documents,
		"roles": groupe_permissions,
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}
		# print('categorie returne')

		return HttpResponse(template.render(context, request))
	except Exception as e:
		print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS CATEGORIE_EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_categorie_employe'))
def get_modifier_categorie_employe(request,ref):
	permission_number = 211
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	echelons=dao_EchelonDesignation.toListEchelon()
	categories=dao_categorieDesignation.toListcategories()

	ref = int(ref)
	model = dao_categorie_employe.toGetCategorie_employe(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier une catégorie','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'echelons':echelons,
	'categories':categories,
	'devises': dao_devise.toListDevisesActives(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/categorie_employe/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_categorie_employe(request):

	id = int(request.POST['ref'])
	try:
		categorie = request.POST['categorie']
		echelon = request.POST['echelon']
		salaire_base = makeFloat(request.POST['salaire_base'])
		devise_id = request.POST['devise_id']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		categorie_employe=dao_categorie_employe.toCreateCategorie_employe(categorie,echelon,salaire_base,devise_id,description)
		categorie_employe=dao_categorie_employe.toUpdateCategorie_employe(id, categorie_employe)
		print('Categorie save',categorie_employe)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_categorie_employe'))
	except Exception as e:
		print('Erreur post_modifier_categorie_employe')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER CATEGORIE_EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		print(e)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_update_categorie_employe'))

def get_upload_categorie_employe(request):
	try:
		permission_number = 210
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response

		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des catégories",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/categorie_employe/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD CATEGORIE EMPLOYE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_categorie_employe"))


@transaction.atomic
def post_upload_categorie_employe(request):
	sid = transaction.savepoint()
	try:
		#print("upload_categorie_employe")
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
			categorie = str(df['categorie'][i])
			description = str(df['description'][i])
			echelon = str(df['echelon'][i])
			salaire_base = makeFloat(df['salaire_base'][i])

			devise_id = None
			code_iso = str(df['code_devise'][i])
			devise = models.Model_Devise.objects.filter(code_iso__icontains = code_iso).first()
			if devise != None : devise_id = devise.id

			categorie_employe=dao_categorie_employe.toCreateCategorie_employe(categorie,echelon,salaire_base,devise_id,description)
			categorie_employe=dao_categorie_employe.toSaveCategorie_employe(auteur, categorie_employe)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_categorie_employe"))
	except Exception as e:
		#print("ERREUR POST UPLOAD CATEGORIE EMPLOYE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD CATEGORIE EMPLOYE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_categorie_employe"))

def get_json_poste(request):
	try:
		#print("ima")
		data1 = []
		data2 = []
		data = [data1, data2]
		ident = int(request.GET["ref"])
		#print(ident)
		#print("dazom")
		postes = dao_poste.toListPostesByDepartement(ident)
		employes = dao_employe.toListEmployesOfDepartement(ident)
		#print(postes)
		for poste in postes:
				item = {"id": poste.id,'designation' : poste.designation}
				data1.append(item)
		for employe in employes:
				item = {"id": employe.id,'nom_complet' : employe.nom_complet}
				data2.append(item)

		#print(data)
		return JsonResponse(data, safe=False)

	except Exception as e:
		return JsonResponse([], safe=False)

def get_json_employe(request):
	try:
		#print("ima")
		data = []
		ident = int(request.GET["ref"])
		#print(ident)
		#print("dazom")
		employes = dao_employe.toListEmployesOfDepartement(ident)
		#print(employes)
		for employe in employes:
				item = {"id": employe.id,'nom_complet' : employe.nom_complet}
				data.append(item)
		#print(data)
		return JsonResponse(data, safe=False)

	except Exception as e:
		return JsonResponse([], safe=False)

def get_lister_syndicat(request):
	permission_number = 278
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	# model = dao_syndicat.toListSyndicat()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_syndicat.toListSyndicat(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste des syndicats','view':view,'model' : model,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/syndicat/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_syndicat(request):
	permission_number = 213
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	employes = dao_employe.toListEmployes()

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Ajouter un syndicat','employes':employes, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/syndicat/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_syndicat(request):

	try:
		designation = request.POST['designation']
		role = request.POST['role']
		objectifs = request.POST['objectifs']
		delegue_principal_id = request.POST['delegue_principal_id']
		delegue_secondaire_id = request.POST['delegue_secondaire_id']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		if delegue_principal_id == "":
			delegue_principal_id = None
		if delegue_secondaire_id == "":
			delegue_secondaire_id = None

		syndicat=dao_syndicat.toCreateSyndicat(designation,role,objectifs,delegue_principal_id,delegue_secondaire_id,description)
		syndicat=dao_syndicat.toSaveSyndicat(auteur, syndicat)
		if syndicat == None: raise Exception("")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_syndicat', args=(syndicat.id,)))
	except Exception as e:
		#print('Erreur post_creer_syndicat')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Erreur pendant L'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_syndicat'))


def get_details_syndicat(request,ref):
	permission_number = 278
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		syndicat=dao_syndicat.toGetSyndicat(ref)
		ligne_syndicat = dao_ligne_syndicat.toListLigneSyndicatBySyndicat(syndicat.id)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/syndicat/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,syndicat)


		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Détails sur "{}" '.format(syndicat.designation.upper()),'syndicat' : syndicat,'ligne_syndicat':ligne_syndicat,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_syndicat'))
def get_modifier_syndicat(request,ref):
	permission_number = 279
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_syndicat.toGetSyndicat(ref)
	employes = dao_employe.toListEmployes()
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier Syndicat','employes':employes,'model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/syndicat/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_syndicat(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		role = request.POST['role']
		objectifs = request.POST['objectifs']
		delegue_principal_id = request.POST['delegue_principal_id']
		delegue_secondaire_id = request.POST['delegue_secondaire_id']
		description = request.POST['description']
		auteur = identite.utilisateur(request)

		syndicat=dao_syndicat.toCreateSyndicat(designation,role,objectifs,delegue_principal_id,delegue_secondaire_id,description)
		syndicat=dao_syndicat.toUpdateSyndicat(id, syndicat)
		if syndicat == None: raise Exception("erreur")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_syndicat', args=(syndicat.id,)))
	except Exception as e:
		#print('Erreur post_modifier_syndicat')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Erreur pendant L'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_syndicat'))

def get_creer_ligne_syndicat(request,ref):
	permission_number = 213
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	ref = int(ref)
	syndicat = dao_syndicat.toGetSyndicat(ref)
	employes = dao_employe.toListEmployes()
	ligne_syndicat = dao_ligne_syndicat.toListLigneSyndicatBySyndicat(syndicat.id)

	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Affilier un employé au syndicat','ligne_syndicat':ligne_syndicat,'syndicat':syndicat,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'employes':employes, 'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/syndicat/ligne_syndicat/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_ligne_syndicat(request):
	sid = transaction.savepoint()
	syndicat_id = request.POST['syndicat_id']
	try:
		list_employe = request.POST.getlist('employe', None)
		list_description = request.POST.getlist('description', None)
		list_ligne_id = request.POST.getlist('ligne_id', None)
		list_all_ligne_id = request.POST.getlist('all_ligne_id', None)

		#print(list_ligne_id)
		#print(list_all_ligne_id)
		#print(lokole)

		auteur = identite.utilisateur(request)
		#dao_ligne_syndicat.toDeleteLigneSyndicatOfSyndicat(syndicat_id)

		for i in range(0, len(list_all_ligne_id)):
			is_find = False
			the_item = list_all_ligne_id[i]
			for j in range(0, len(list_ligne_id)):
				if the_item == list_ligne_id[j]:
					is_find = True
			if is_find == False:
				dao_ligne_syndicat.toDeleteLigneSyndicat(the_item)


		for i in range(0, len(list_employe)):
			#print("you've win")
			employe_id = int(list_employe[i])
			description = list_description[i]
			ligne_id = int(list_ligne_id[i])

			if ligne_id != 0:
				ligne_syndicat = dao_ligne_syndicat.toCreateLigneSyndicat(syndicat_id,employe_id,description)
				dao_ligne_syndicat.toUpdateLigneSyndicat(ligne_id,ligne_syndicat)
			else:
				ligne_syndicat = dao_ligne_syndicat.toCreateLigneSyndicat(syndicat_id,employe_id,description)
				ligne_syndicat = dao_ligne_syndicat.toSaveLigneSyndicat(auteur,ligne_syndicat)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_syndicat',args=(syndicat_id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur post_creer_ligne_syndicat')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Erreur pendant L'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_ligne_syndicat',args=(syndicat_id,)))

def get_upload_syndicat(request):
	try:
		permission_number = 213
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des syndicats",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/syndicat/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD SYNDICAT")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_syndicat"))


@transaction.atomic
def post_upload_syndicat(request):
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
			role = str(df['role'][i])
			objectifs = str(df['objectifs'][i])

			delegue_principal_id = None
			delegue_secondaire_id = None

			matricule = str(df['matricule_delegue_principal'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				delegue_principal_id = employe.id

			matricule = str(df['matricule_delegue_secondaire'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				delegue_secondaire_id = employe.id

			syndicat = dao_syndicat.toCreateSyndicat(designation,role,objectifs,delegue_principal_id,delegue_secondaire_id,description)
			syndicat = dao_syndicat.toSaveSyndicat(auteur, syndicat)
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_syndicat"))
	except Exception as e:
		#print("ERREUR POST UPLOAD SYNDICAT")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_syndicat"))

def get_lister_employe_for_emploi(request):
	try:
		permission_number = 217
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return responsee

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Référentiel des emplois: Liste des employés',
		'model' : model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/emploi/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

# EMPLOYE
def get_lister_employe_for_evaluation(request):
	try:
		permission_number = 221
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Evaluation: Liste des employés',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evaluation/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_employe_for_competence(request):
	try:
		permission_number = 353
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Compétences: Liste des employés',
		'view':view,
		'model' : model,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/competence/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_details_competence(request,idt):
	permission_number = 353
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	idt = int(idt)
	try:
		ligne_competence = dao_ligne_competence.toListLigneCompetenceByEmploye(idt)
		employe = dao_employe.toGetEmploye(idt)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/competence/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,ligne_competence)

		context ={'modules':modules,'sous_modules':sous_modules,'title' : employe.nom_complet +': Référentiel des compétences', 'ligne_competence':ligne_competence, 'employe':employe,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS EVALUATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_evaluation', args=(idt,)))

def get_creer_ligne_competence(request,idt):
	permission_number = 355
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)

	ligne_competence = dao_ligne_competence.toListLigneCompetenceByEmploye(idt)

	context ={
	'modules':modules,
	'sous_modules':sous_modules,
	'title' : 'Ajouter une compétence à '+employe.nom_complet,'ligne_competence':ligne_competence,
	#'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'employe':employe, 'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/competence/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_ligne_competence(request):
	sid = transaction.savepoint()
	employe_id = request.POST['employe_id']
	try:
		list_competence = request.POST.getlist('competence', None)
		list_observation = request.POST.getlist('observation', None)
		list_ligne_id = request.POST.getlist('ligne_id', None)
		list_all_ligne_id = request.POST.getlist('all_ligne_id', None)

		#print(list_ligne_id)
		#print(list_all_ligne_id)
		#print(lokole)

		auteur = identite.utilisateur(request)
		#dao_ligne_syndicat.toDeleteLigneSyndicatOfSyndicat(syndicat_id)

		for i in range(0, len(list_all_ligne_id)):
			is_find = False
			the_item = list_all_ligne_id[i]
			for j in range(0, len(list_ligne_id)):
				if the_item == list_ligne_id[j]:
					is_find = True
			if is_find == False:
				dao_ligne_competence.toDeleteLigneCompetence(the_item)


		for i in range(0, len(list_competence)):
			#print("you've win")
			competence =list_competence[i]
			observation = list_observation[i]
			ligne_id = int(list_ligne_id[i])

			if ligne_id != 0:
				ligne_competence = dao_ligne_competence.toCreateLigneCompetence(competence,observation,employe_id)
				ligne_competence = dao_ligne_competence.toUpdateLigneCompetence(ligne_id,ligne_competence)

			else:
				ligne_competence = dao_ligne_competence.toCreateLigneCompetence(competence,observation,employe_id)
				ligne_competence = dao_ligne_competence.toSaveLigneCompetence(auteur,ligne_competence)
			if ligne_competence == None : raise Exception("")
		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_competence',args=(employe_id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur post_creer_ligne_competence')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Erreur lors L'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_competence',args=(employe_id,)))

def get_upload_competence(request):
	try:
		permission_number = 355
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des compétences",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/competence/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD COMPETENCE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_employe_for_competence"))


@transaction.atomic
def post_upload_competence(request):
	sid = transaction.savepoint()
	try:
		#print("upload_competence")
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
			competence = str(df['competence'][i])
			observation = str(df['observation'][i])

			employe_id = None
			matricule = str(df['matricule'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				employe_id = employe.id


			ligne_competence = models.Model_Ligne_Competence.objects.filter(competence__icontains = competence, employe_id = employe_id).first()

			if ligne_competence != None :
				ligne_competence = dao_ligne_competence.toCreateLigneCompetence(competence, observation, employe_id)
				ligne_competence = dao_ligne_competence.toUpdateLigneCompetence(ligne_id, ligne_competence)
			else:
				ligne_competence = dao_ligne_competence.toCreateLigneCompetence(competence,observation,employe_id)
				ligne_competence = dao_ligne_competence.toSaveLigneCompetence(auteur,ligne_competence)
			if ligne_competence == None : raise Exception("")

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_employe_for_competence"))
	except Exception as e:
		#print("ERREUR POST UPLOAD COMPETENCE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, "Erreur lors de L'opération")
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD COMPETENCE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_get_upload_competence"))

def get_lister_evaluation(request, idt):
	permission_number = 221
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_evaluation.toListEvaluation()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_evaluation.toListEvaluation(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste des évaluations de '+employe.nom_complet, 'employe':employe, 'model' : model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evaluation/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_evaluation(request, idt):
	permission_number = 220
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Ajouter une évaluation de ' + employe.nom_complet, 'employe':employe,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evaluation/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_evaluation(request):
	employe_id = request.POST['employe_id']
	try:
		description = request.POST['description']
		instructions = request.POST['instructions']
		echelle_notation = request.POST['echelle_notation']
		echelle_performance = request.POST['echelle_performance']
		echelle_coefficient = request.POST['echelle_coefficient']
		appreciation = request.POST['appreciation']
		date_appreciation = request.POST['date_appreciation']
		#print(' start')
		date_appreciation = timezone.datetime(int(date_appreciation[6:10]), int(date_appreciation[3:5]), int(date_appreciation[0:2]))
		#print(date_appreciation)
		auteur = identite.utilisateur(request)

		evaluation=dao_evaluation.toCreateEvaluation(description,instructions,echelle_notation,echelle_performance,echelle_coefficient,appreciation,date_appreciation,employe_id)
		evaluation=dao_evaluation.toSaveEvaluation(auteur, evaluation)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_evaluation', args=(employe_id,)))
	except Exception as e:
		#print('post_creer_evaluation')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, "Erreur L'opération")
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER EVALUATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_evaluation', args=(employe_id,)))


def get_details_evaluation(request,idt, ref):
	permission_number = 221
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	idt = int(idt)
	try:
		ref=int(ref)
		evaluation=dao_evaluation.toGetEvaluation(ref)
		employe = dao_employe.toGetEmploye(idt)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evaluation/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,evaluation)



		context ={'modules':modules,'sous_modules':sous_modules,'title' : employe.nom_complet +':Détails sur une évaluation','employe':employe,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'evaluation' : evaluation,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS EVALUATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_evaluation', args=(idt,)))
def get_modifier_evaluation(request,idt,ref):
	permission_number = 222
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	model = dao_evaluation.toGetEvaluation(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : employe.nom_complet +':Modifier une évaluation','employe':employe, 'model':model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evaluation/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_evaluation(request):

	id = int(request.POST['ref'])
	employe_id = request.POST['employe_id']
	try:
		description = request.POST['description']
		instructions = request.POST['instructions']
		echelle_notation = request.POST['echelle_notation']
		echelle_performance = request.POST['echelle_performance']
		echelle_coefficient = request.POST['echelle_coefficient']
		appreciation = request.POST['appreciation']
		date_appreciation = request.POST['date_appreciation']
		date_appreciation = timezone.datetime(int(date_appreciation[6:10]), int(date_appreciation[3:5]), int(date_appreciation[0:2]))
		employe_id = request.POST['employe_id']
		auteur = identite.utilisateur(request)

		evaluation=dao_evaluation.toCreateEvaluation(description,instructions,echelle_notation,echelle_performance,echelle_coefficient,appreciation,date_appreciation,employe_id)
		evaluation=dao_evaluation.toUpdateEvaluation(id, evaluation)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_evaluation', args=(employe_id,id,)))
	except Exception as e:
		#print('post_modifier_evaluation')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER EVALUATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Erreur lors de l'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_evaluation', args=(employe_id,)))



# EMPLOYE
def get_lister_employe_for_emploi(request):
	try:
		permission_number = 217
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Référentiel des emplois: Liste des employés',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/emploi/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))



def get_lister_emploi(request, idt):
	permission_number = 217
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	idt = int(idt)
	# model = dao_emploi.toListEmploiOfEmploye(idt)
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_emploi.toListEmploiOfEmploye(idt), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	employe = dao_employe.toGetEmploye(idt)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Liste des emplois référencés de '+employe.nom_complet ,'employe':employe,'model' : model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/emploi/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_emploi(request,idt):
	permission_number = 216
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Ajouter un emploi de '+employe.nom_complet,'employe':employe,'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/emploi/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_emploi(request):
	employe_id = request.POST['employe_id']
	try:
		etablissement = request.POST['etablissement']
		lieu = request.POST['lieu']
		fonctions = request.POST['fonctions']
		categorie_socio_professionnelle = request.POST['categorie_socio_professionnelle']
		date_entree = request.POST['date_entree']
		date_sortie = request.POST['date_sortie']
		auteur = identite.utilisateur(request)
		date_entree = timezone.datetime(int(date_entree[6:10]), int(date_entree[3:5]), int(date_entree[0:2]))
		date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))

		emploi=dao_emploi.toCreateEmploi(etablissement,lieu,fonctions,categorie_socio_professionnelle,date_entree,date_sortie,employe_id)
		emploi=dao_emploi.toSaveEmploi(auteur, emploi)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_emploi', args=(employe_id,)))
	except Exception as e:
		#print('Erreur post_creer_emploi')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, "Erreur lors L'opération")
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER EMPLOI \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_emploi', args=(employe_id,)))

def get_upload_emploi(request):
	try:
		permission_number = 216
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des emplois",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/emploi/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD EMPLOI")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_employe_for_emploi"))


@transaction.atomic
def post_upload_emploi(request):
	sid = transaction.savepoint()
	try:
		#print("upload_emploi")
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
			etablissement = str(df['etablissement'][i])
			lieu = str(df['lieu'][i])
			fonctions = str(df['fonctions'][i])
			categorie_socio_professionnelle = str(df['categorie_professionnelle'][i])
			date_entree = str(df['date_entree'][i])
			date_sortie = str(df['date_sortie'][i])

			#conversion de la date
			#print("date_entree: {}".format(date_entree))
			if len(date_entree) == 10:
				date_entree = timezone.datetime(int(date_entree[6:10]), int(date_entree[3:5]), int(date_entree[0:2]))
			elif len(date_entree) > 10:
				date_entree = timezone.datetime(int(date_entree[0:4]), int(date_entree[5:7]), int(date_entree[8:10]))

			#print("date_sortie: {}".format(date_sortie))
			if len(date_sortie) == 10:
				date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))
			elif len(date_sortie) > 10:
				date_sortie = timezone.datetime(int(date_sortie[0:4]), int(date_sortie[5:7]), int(date_sortie[8:10]))

			employe_id = None
			matricule = str(df['matricule'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				employe_id = employe.id

			emploi = dao_emploi.toCreateEmploi(etablissement, lieu, fonctions, categorie_socio_professionnelle, date_entree,date_sortie,employe_id)
			emploi = dao_emploi.toSaveEmploi(auteur, emploi)
			if emploi == None: raise Exception("Une erreur est survenue lors de l'enregistrement d'un emploi")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_employe_for_emploi"))
	except Exception as e:
		#print("ERREUR POST UPLOAD EMPLOI")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD EMPLOI \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_get_upload_emploi"))

def get_details_emploi(request,idt,ref):
	permission_number = 217
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	idt = int(idt)
	try:
		ref=int(ref)

		emploi=dao_emploi.toGetEmploi(ref)
		employe = dao_employe.toGetEmploye(idt)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/emploi/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,emploi)


		context ={'modules':modules,'sous_modules':sous_modules,'title' : employe.nom_complet +': Détails sur un emploi référencé', 'employe':employe, 'emploi' : emploi,
		'actions':auth.toGetActions(modules,utilisateur),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS EMPLOI \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_emploi', args=(idt,)))

def get_modifier_emploi(request,idt,ref):
	permission_number = 218
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	model = dao_emploi.toGetEmploi(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : employe.nom_complet +': Modifier un emploi référencé','employe':employe,'model':model,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : identite.utilisateur(request),'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/emploi/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_emploi(request):

	id = int(request.POST['ref'])
	employe_id = request.POST['employe_id']
	try:
		etablissement = request.POST['etablissement']
		lieu = request.POST['lieu']
		fonctions = request.POST['fonctions']
		categorie_socio_professionnelle = request.POST['categorie_socio_professionnelle']
		date_entree = request.POST['date_entree']
		date_sortie = request.POST['date_sortie']
		auteur = identite.utilisateur(request)
		date_entree = timezone.datetime(int(date_entree[6:10]), int(date_entree[3:5]), int(date_entree[0:2]))
		date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))

		emploi=dao_emploi.toCreateEmploi(etablissement,lieu,fonctions,categorie_socio_professionnelle,date_entree,date_sortie,employe_id)
		emploi=dao_emploi.toUpdateEmploi(id, emploi)
		if emploi == None: raise Exception("Erreur lors de la modification d'un emploi")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_emploi', args=(employe_id,id,)))
	except Exception as e:
		#print('Erreur post_modifier_emploi')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER EMPLOI \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_emploi', args=(employe_id,)))



def get_lister_formation(request):
	permission_number = 225
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_formation.toListFormation()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_formation.toListFormation(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	title = "Liste des formations"
	isStatus = False

	if 'success' in request.GET:
		model = dao_formation.toListFormationByStatus("success")
		title = "Liste des formations réalisées"
		isStatus = True
	if 'cancel' in request.GET:
		model = dao_formation.toListFormationByStatus("cancel")
		title = "Liste des formations annulées"
		isStatus = True
	if 'created' in request.GET:
		model = dao_formation.toListFormationByStatus("created")
		title = "Liste des formations prévues"
		isStatus = True
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
		model = pagination.toGet(request, model)

	context ={'modules':modules,'sous_modules':sous_modules,'title' : title,'view':view, 'isStatus':isStatus, 'model' : model,'utilisateur' : utilisateur,'modules' : modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/formation/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_formation(request):
	try:
		#print('Touché')
		permission_number = 224
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		departements = dao_unite_fonctionnelle.toListUniteFonctionnelle()

		context ={
			'modules':modules,
			'sous_modules':sous_modules,
			'title' : 'Ajouter formation',
			'departements':departements,
			'utilisateur' : utilisateur,
			#'modules' : modules,
			#'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/formation/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('ERREUR get_creer_formation:', e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))

def post_creer_formation(request):

	try:
		departement = request.POST['departement']
		theme = request.POST['theme']
		objectif = request.POST['objectif']
		public_cible = request.POST['public_cible']
		annee = request.POST['annee']
		nombre_jour_formation = request.POST['nombre_jour_formation']
		type = request.POST['type']
		organisme_formation = request.POST['organisme_formation']
		localite_organisme = request.POST['localite_organisme']
		nombre_heure_par_jour = request.POST['nombre_heure_par_jour']
		cout_formation =  request.POST['cout_formation']
		nombre_participant_par_jour =request.POST['nombre_participant_par_jour']
		frais_mission_hebergement =float(request.POST['frais_mission_hebergement'].replace(',','.'))
		frais_deplacement_ht =float( request.POST['frais_deplacement_ht'].replace(',','.'))
		priorite = request.POST['priorite']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))

		auteur = identite.utilisateur(request)

		libelle_departement = dao_unite_fonctionnelle.toGetUniteFonctionnelle(departement)

		formation=dao_formation.toCreateFormation(libelle_departement,theme,objectif,public_cible,annee,nombre_jour_formation,type,organisme_formation,localite_organisme,nombre_heure_par_jour,cout_formation,nombre_participant_par_jour,frais_mission_hebergement,frais_deplacement_ht,priorite, date_debut, date_fin,"created")
		formation=dao_formation.toSaveFormation(auteur, formation)
		if formation == None: raise Exception("Erreur survenue pendant l'enregistrement de la formation")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_formation'))
	except Exception as e:
		#print('Erreur post_creer_formation ',e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER FORMATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_formation'))


def get_details_formation(request,ref):
	permission_number = 225
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		formation=dao_formation.toGetFormation(ref)
		ligne_formation = dao_ligne_formation.toListLigneFormationByFormation(formation.id)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/formation/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,formation)


		context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Détails sur formation','formation' : formation,'ligne_formation':ligne_formation,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		"historique": historique,
		"etapes_suivantes": etapes_suivantes,
		"signee": signee,
		"content_type_id": content_type_id,
		"documents": documents,
		"roles": groupe_permissions,
		'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS FORMATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_formation'))
def get_modifier_formation(request,ref):
	permission_number = 226
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_formation.toGetFormation(ref)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier Formation','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/formation/update.html')
	return HttpResponse(template.render(context, request))

def get_cancel_formation(request,ref):
	permission_number = 226
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	formation = dao_formation.toUpdateStatusFormation(ref,"cancel")
	model = dao_formation.toGetFormation(formation.id)
	context ={'modules':modules,'sous_modules':sous_modules,'title' : 'Modifier Formation','model':model, 'utilisateur' : utilisateur,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/formation/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_formation(request):

	id = int(request.POST['ref'])
	try:
		departement = request.POST['departement']
		theme = request.POST['theme']
		objectif = request.POST['objectif']
		public_cible = request.POST['public_cible']
		annee = request.POST['annee']
		nombre_jour_formation = request.POST['nombre_jour_formation']
		type = request.POST['type']
		organisme_formation = request.POST['organisme_formation']
		localite_organisme = request.POST['localite_organisme']
		nombre_heure_par_jour = request.POST['nombre_heure_par_jour']
		cout_formation =request.POST['cout_formation']
		nombre_participant_par_jour = request.POST['nombre_participant_par_jour']
		frais_mission_hebergement = request.POST['frais_mission_hebergement'].replace(',','.')
		frais_deplacement_ht = request.POST['frais_deplacement_ht'].replace(',','.')
		priorite = request.POST['priorite']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		auteur = identite.utilisateur(request)

		formation=dao_formation.toCreateFormation(departement,theme,objectif,public_cible,annee,nombre_jour_formation,type,organisme_formation,localite_organisme,nombre_heure_par_jour,cout_formation,nombre_participant_par_jour,frais_mission_hebergement,frais_deplacement_ht,priorite, date_debut, date_fin)
		formation=dao_formation.toUpdateFormation(id, formation)
		if formation == None: raise Exception("Erreur survenue pendant la modification de la formation")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_formation'))
	except Exception as e:
		#print('Erreur post_modifier_formation ',e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER FORMATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_formation'))



def get_creer_ligne_formation(request,ref):
	permission_number = 224
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	formation = dao_formation.toGetFormation(ref)
	employes = dao_employe.toListEmployes()
	ligne_formation = dao_ligne_formation.toListLigneFormationByFormation(formation.id)


	context ={
		'title' : 'Réaliser une formation',
		'ligne_formation':ligne_formation,
		'formation':formation,
		'employes':employes,
		#'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'sous_modules' : sous_modules,
		#'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/formation/ligne_formation/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_ligne_formation(request):
	sid = transaction.savepoint()
	formation_id = request.POST['formation_id']
	try:
		cout_formation_effective = request.POST['cout_formation_effective']
		frais_mission_hebergement_effective = request.POST['frais_mission_hebergement_effective']
		frais_deplacement_ht_effective = request.POST['frais_deplacement_ht_effective']
		nombre_participant_par_jour_effective = request.POST['nombre_participant_par_jour_effective']
		list_employe = request.POST.getlist('employe', None)
		list_competence = request.POST.getlist('competence', None)
		list_description = request.POST.getlist('description', None)
		list_ligne_id = request.POST.getlist('ligne_id', None)
		list_all_ligne_id = request.POST.getlist('all_ligne_id', None)


		#print(list_ligne_id)
		#print(list_all_ligne_id)
		#print(lokole)

		auteur = identite.utilisateur(request)
		#dao_ligne_syndicat.toDeleteLigneSyndicatOfSyndicat(syndicat_id)

		for i in range(0, len(list_all_ligne_id)):
			is_find = False
			the_item = list_all_ligne_id[i]
			for j in range(0, len(list_ligne_id)):
				if the_item == list_ligne_id[j]:
					is_find = True
			if is_find == False:
				dao_ligne_formation.toDeleteLigneFormation(the_item)


		for i in range(0, len(list_employe)):
			#print("you've win")
			employe_id = int(list_employe[i])
			competence = list_competence[i]
			description = list_description[i]
			ligne_id = int(list_ligne_id[i])

			if ligne_id != 0:
				ligne_formation = dao_ligne_formation.toCreateLigneFormation(formation_id,employe_id,competence,description)
				dao_ligne_formation.toUpdateLigneFormation(ligne_id,ligne_formation)
			else:
				ligne_formation = dao_ligne_formation.toCreateLigneFormation(formation_id,employe_id,competence,description)
				ligne_formation = dao_ligne_formation.toSaveLigneFormation(auteur,ligne_formation)



		formation = dao_formation.toRealiseFormation(formation_id,cout_formation_effective,frais_mission_hebergement_effective,frais_deplacement_ht_effective,nombre_participant_par_jour_effective,"success")

		for i in range(0, len(list_employe)):
			employe_id = int(list_employe[i])
			ligne_competence = dao_ligne_competence.toCreateLigneCompetence(competence,"Formation ARPCE : " + formation.theme + " du "+ str(formation.date_debut),employe_id)
			ligne_competence = dao_ligne_competence.toSaveLigneCompetence(auteur,ligne_competence)
			if ligne_competence == None: raise Exception("Erreur survenue pendant l'enregistrement d'une compétence")

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_formation',args=(formation_id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur post_creer_ligne_formation')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER FORMATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_ligne_formation',args=(formation_id,)))

def get_upload_formation(request):
	try:
		permission_number = 224
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des formations",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/formation/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD FORMATION")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_formation"))


@transaction.atomic
def post_upload_formation(request):
	sid = transaction.savepoint()
	try:
		#print("upload_formation")
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
			theme = str(df['theme'][i])
			objectif = str(df['objectif'][i])
			annee = str(df['annee'][i])
			public_cible = str(df['public_cible'][i])
			type = str(df['type'][i])

			nombre_jour_formation = str(df['nombre_jour_formation'][i])
			nombre_heure_par_jour = str(df['nombre_heure_par_jour'][i])
			nombre_participant_par_jour = str(df['nombre_participant_par_jour'][i])

			organisme_formation = str(df['organisme_formation'][i])
			localite_organisme = str(df['localite_organisme'][i])

			cout_formation = makeFloat(df['cout_formation'][i])
			frais_mission_hebergement = makeFloat(df['frais_mission_hebergement'][i])
			frais_deplacement_ht = makeFloat(df['frais_deplacement_ht'][i])

			date_debut = str(df['date_debut'][i])
			date_fin = str(df['date_fin'][i])
			priorite = str(df['priorite'][i])

			unite_fonctionnelle = str(df['departement'][i])
			departement = models.Model_Unite_fonctionnelle.objects.filter(libelle__icontains = unite_fonctionnelle).first()

			#conversion de la date
			#print("date_debut: {}".format(date_debut))
			if len(date_debut) == 10:
				date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
			elif len(date_debut) > 10:
				date_debut = timezone.datetime(int(date_debut[0:4]), int(date_debut[5:7]), int(date_debut[8:10]))

			#print("date_fin: {}".format(date_fin))
			if len(date_fin) == 10:
				date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
			elif len(date_fin) > 10:
				date_fin = timezone.datetime(int(date_fin[0:4]), int(date_fin[5:7]), int(date_fin[8:10]))

			formation = dao_formation.toCreateFormation(departement, theme, objectif, public_cible, annee, nombre_jour_formation, type, organisme_formation, localite_organisme, nombre_heure_par_jour, cout_formation, nombre_participant_par_jour, frais_mission_hebergement, frais_deplacement_ht, priorite, date_debut, date_fin,"created")
			formation = dao_formation.toSaveFormation(auteur, formation)
			if formation == None: raise Exception("Erreur survenue pendant l'enregistrement d'une' formation")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_formation"))

	except Exception as e:
		#print("ERREUR POST UPLOAD FORMATION")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD FORMATION \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_formation"))


#### Mobilité
def get_lister_mobilite(request):
	permission_number = 230
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_mobilite.toListMobilite()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_mobilite.toListMobilite(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des Mobilités',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}

	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/mobilite/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_mobilite(request):
	permission_number = 228
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	services = dao_unite_fonctionnelle.toListUniteFonctionnelle()
	postes = dao_poste.toListPostes()

	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Ajouter une mobilité',
		'utilisateur' : utilisateur,
		'services': services,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/mobilite/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_mobilite(request):

	try:
		service = int(request.POST['service'])
		dep = dao_unite_fonctionnelle.toGetUniteFonctionnelle(service)
		service = dep.libelle
		fonctions_occupees = int(request.POST['fonctions_occupees'])
		fonctions_occupees = dao_poste.toGetPoste(fonctions_occupees)
		modalites = request.POST['modalites']
		direction = dep.unite_fonctionnelle
		type_mobilite = request.POST['type_mobilite']

		date_entree = request.POST['date_entree']
		#date_sortie = request.POST['date_sortie']
		employe_id = int(request.POST['employe_id'])
		categorie_socio_professionnelle = request.POST['categorie_socio_professionnelle']
		employe = dao_employe.toGetEmploye(employe_id)
		#print(employe)
		#print(categorie_socio_professionnelle)

		mob = dao_mobilite.toGetMobiliteByEmploye(employe_id).last()
		# categorie_socio_professionnelle = employe.categorie_employe

		if categorie_socio_professionnelle != None:
			if mob:
				categorie_socia_pro_precedent = mob.categorie_socio_professionnelle
				#print('**Information CATEGORIE SOCIO PRO ACTUELLE ** %s' %categorie_socio_professionnelle)
				#print('**Information CATEGORIE SOCIO PRO PRECEDENTE ** %s' %categorie_socia_pro_precedent)
			else:
				categorie_socia_pro_precedent = None
		else:
			categorie_socia_pro_precedent = None

		#print(employe.categorie_employe)

		date_entree = timezone.datetime(int(date_entree[6:10]), int(date_entree[3:5]), int(date_entree[0:2]))

		if mob != None:
			mob.date_sortie = date_entree
			mob.save()

		#date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))
		auteur = identite.utilisateur(request)

		#Ajout de la pondération en fonction occupée
		"""
		Les pondérations sont sur 10 suivant le barême suivant :

		DG = 10
		Autres Directeurs = 8
		Chef de service = 6
		Chef de bureau et Chef de projet = 4
		Assistant = 2

		"""
		ponderation = 0

		if "assistant" in fonctions_occupees.designation.lower():
			ponderation = 2
		elif "projet" in fonctions_occupees.designation.lower() or "bureau" in fonctions_occupees.designation.lower():
			ponderation = 4
		elif "service" in fonctions_occupees.designation.lower():
			ponderation = 6
		elif "directeur" in fonctions_occupees.designation.lower():
			ponderation = 8
		elif fonctions_occupees.designation.lower() == "directeur général" or fonctions_occupees.designation.lower() == "directeur general":
			ponderation = 10
		else:
			ponderation = 0

		#
		mobilite=dao_mobilite.toCreateMobilite(direction,service,type_mobilite,fonctions_occupees,ponderation,categorie_socio_professionnelle,modalites,date_entree,None,employe_id,categorie_socia_pro_precedent)
		mobilite=dao_mobilite.toSaveMobilite(auteur, mobilite)

		#Modification du service de l'employé

		employe.unite_fonctionnelle_id = dep.id
		employe.save()
		if mobilite == None: raise Exception("Erreur survenue pendant l'enregistrement de la mobilité")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_mobilite', args=(mobilite.id,)))
	except Exception as e:
		#print('Erreur post_creer_mobilite')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER MOBILITE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_mobilite'))


def get_details_mobilite(request,ref):
	permission_number = 230
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		mobilite=dao_mobilite.toGetMobilite(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,mobilite)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Détails sur une mobilité',
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'mobilite' : mobilite,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
			}

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/mobilite/item.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS MOBILITE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_mobilite'))
def get_modifier_mobilite(request,ref):
	permission_number = 229
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	services = dao_unite_fonctionnelle.toListUniteFonctionnelle()
	postes = dao_poste.toListPostes()

	ref = int(ref)
	model = dao_mobilite.toGetMobilite(ref)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier une mobilité',
		'model':model,
		'services':services,
		'postes':postes,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/mobilite/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_mobilite(request):

	id = int(request.POST['ref'])
	try:
		service = request.POST['service']

		#print("Arrivé I")
		fonctions_occupees = request.POST['fonctions_occupees']
		categorie_socio_professionnelle = request.POST['categorie_socio_professionnelle']
		modalites = request.POST['modalites']
		type_mobilite = request.POST['type_mobilite']
		direction = request.POST['direction']
		#print("Arrivé II")

		date_entree = request.POST['date_entree']
		date_sortie = request.POST['date_sortie']
		employe_id = request.POST['employe_id']

		employe = dao_employe.toGetEmploye(employe_id)
		mob = dao_mobilite.toGetMobiliteByEmploye(employe_id).last()
		#print("Arrivé III")
		categorie_socio_professionnelle = request.POST['categorie_socio_professionnelle']
		categorie_socia_pro_precedent=request.POST['categorie_socia_pro_precedent']

		date_entree = timezone.datetime(int(date_entree[6:10]), int(date_entree[3:5]), int(date_entree[0:2]))
		date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))

		#print("Arrivé III",date_entree)
		#print("Arrivé IV",date_sortie)
		auteur = identite.utilisateur(request)

		#Ajout de la pondération en fonction occupée
		"""
		Les pondérations sont sur 10 suivant le barême suivant :

		DG = 10
		Autres Directeurs = 8
		Chef de service = 6
		Chef de bureau et Chef de projet = 4
		Assistant = 2

		"""
		ponderation = 0

		if "assistant" in fonctions_occupees.lower():
			ponderation = 2
		elif "projet" in fonctions_occupees.lower() or "bureau" in fonctions_occupees.lower():
			ponderation = 4
		elif "service" in fonctions_occupees.lower():
			ponderation = 6
		elif "directeur" in fonctions_occupees.lower():
			ponderation = 8
		elif fonctions_occupees.lower() == "directeur général" or fonctions_occupees.lower() == "directeur general":
			ponderation = 10
		else:
			ponderation = 0

		#mobilite=dao_mobilite.toCreateMobilite(direction,service,type_mobilite,fonctions_occupees, ponderation,categorie_socio_professionnelle,categorie_socia_pro_precedent,modalites,date_entree,date_sortie,employe_id)
		mobilite=dao_mobilite.toCreateMobilite(direction,service,type_mobilite,fonctions_occupees, ponderation,categorie_socio_professionnelle,modalites,date_entree,date_sortie,employe_id,categorie_socia_pro_precedent="")
		mobilite=dao_mobilite.toUpdateMobilite(id, mobilite)

		if mobilite == None: raise Exception("Erreur survenue pendant la modification de la mobilité")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_mobilite', args=(id,)))
	except Exception as e:
		#print('Erreur post_modifier_mobilite')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER MOBILITE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_mobilite'))

def get_upload_mobilite(request):
	try:
		permission_number = 228
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des mobilités",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/mobilite/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD MOBILITE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_mobilite"))


@transaction.atomic
def post_upload_mobilite(request):
	sid = transaction.savepoint()
	try:
		#print("upload_mobilite")
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
			modalites = str(df['modalites'][i])
			type_mobilite = str(df['type_mobilite'][i])
			date_entree = str(df['date_entree'][i])
			date_sortie = str(df['date_sortie'][i])
			categorie_socio_professionnelle = str(df['categorie_professionnelle'][i])
			categorie_socia_pro_precedent = ""

			service = str(df['service'][i])
			departement = models.Model_Unite_fonctionnelle.objects.filter(libelle__icontains = service).first()
			if departement != None : service = departement.libelle

			direction = departement

			fonction = str(df['poste'][i])
			fonctions_occupees = models.Model_Poste.objects.filter(designation__icontains = fonction).first()

			employe_id = None
			matricule = str(df['matricule'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				employe_id = employe.id

			#conversion de la date
			#print("date_entree: {}".format(date_entree))
			if len(date_entree) == 10:
				date_entree = timezone.datetime(int(date_entree[6:10]), int(date_entree[3:5]), int(date_entree[0:2]))
			elif len(date_entree) > 10:
				date_entree = timezone.datetime(int(date_entree[0:4]), int(date_entree[5:7]), int(date_entree[8:10]))

			#print("date_sortie: {}".format(date_sortie))
			if len(date_sortie) == 10:
				date_sortie = timezone.datetime(int(date_sortie[6:10]), int(date_sortie[3:5]), int(date_sortie[0:2]))
			elif len(date_sortie) > 10:
				date_sortie = timezone.datetime(int(date_sortie[0:4]), int(date_sortie[5:7]), int(date_sortie[8:10]))

			# Ajout de la pondération en fonction occupée
			"""
			Les pondérations sont sur 10 suivant le barême suivant :
			DG = 10
			Autres Directeurs = 8
			Chef de service = 6
			Chef de bureau et Chef de projet = 4
			Assistant = 2
			"""
			ponderation = 0
			if fonctions_occupees != None:
				if "assistant" in fonctions_occupees.designation.lower():
					ponderation = 2
				elif "projet" in fonctions_occupees.designation.lower() or "bureau" in fonctions_occupees.designation.lower():
					ponderation = 4
				elif "service" in fonctions_occupees.designation.lower():
					ponderation = 6
				elif "directeur" in fonctions_occupees.designation.lower():
					ponderation = 8
				elif fonctions_occupees.designation.lower() == "directeur général" or fonctions_occupees.designation.lower() == "directeur general":
					ponderation = 10
				else:
					ponderation = 0

			# Création mobilité
			mobilite = dao_mobilite.toCreateMobilite(direction, service, type_mobilite, fonctions_occupees, ponderation, categorie_socio_professionnelle, modalites, date_entree, date_sortie, employe_id, categorie_socia_pro_precedent)
			mobilite = dao_mobilite.toSaveMobilite(auteur, mobilite)
			if mobilite == None : raise Exception("Une erreur est survenue pendant la création d'une mobilité interne")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_mobilite"))
	except Exception as e:
		#print("ERREUR POST UPLOAD MOBILITE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD MOBILITE \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_mobilite"))


#Evolution des employés
def get_lister_evolution(request):
	try:
		permission_number = 237
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des employés',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evolution_personnelle/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_evolution_personnelle(request, idt):
	permission_number = 237
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	mobilite = dao_mobilite.toGetMobiliteByEmploye(employe.id)
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(mobilite, permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Les évolutions de '+employe.nom_complet,
		'employe':employe,
		'mobilite' : model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evolution_personnelle/employe/list.html')
	return HttpResponse(template.render(context, request))


#Plans de releve
def get_lister_plan_releve(request):
	try:
		permission_number = 234
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Plan de relève : Liste des employés',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/releve/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_details_releve(request, ref):
	permission_number = 234
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref=int(ref)
	#print(ref)
	employe = dao_employe.toGetEmploye(ref)
	releve = dao_ligne_releve.toListLigneReleveByEmploye(employe.id)
	#print(employe)
	try:

		#releve = dao_ligne_releve.toGetLigneReleve(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/releve/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,employe)

		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : employe.nom_complet +':Détails sur rélèves',
			'employe':employe,
			'ligne_releve':releve,
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
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
			}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS EVALUATION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_plan_releve'))

def get_creer_releve(request, ref):
	permission_number = 233
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_employe.toGetEmploye(ref)
	#print(model)

	ligne_releve = dao_ligne_releve.toListLigneReleveByEmploye(model.id)
	#print(ligne_releve)

	employe = dao_employe.toListEmployes()
	#print(employe)

	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Ajouter rélèves',
		'utilisateur' : utilisateur,
		'employe': employe,
		'ligne_releve':ligne_releve,
		'model':model,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/releve/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_releve(request):
	sid = transaction.savepoint()
	employe_id = int(request.POST['employe_id'])
	try:
		list_releve = request.POST.getlist('employe', None)
		list_degre = request.POST.getlist('degre', None)
		list_ligne_id = request.POST.getlist('ligne_id', None)
		list_all_ligne_id = request.POST.getlist('all_ligne_id', None)

		#print(lokole)

		auteur = identite.utilisateur(request)
		#dao_ligne_syndicat.toDeleteLigneSyndicatOfSyndicat(syndicat_id)

		for i in range(0, len(list_all_ligne_id)):
			is_find = False
			the_item = list_all_ligne_id[i]
			for j in range(0, len(list_ligne_id)):
				if the_item == list_ligne_id[j]:
					is_find = True
			if is_find == False:
				dao_ligne_releve.toDeleteLignereleve(the_item)


		for i in range(0, len(list_releve)):
			#print("you've win")
			releve = int(list_releve[i])
			degre = list_degre[i]
			ligne_id = int(list_ligne_id[i])

			if ligne_id != 0:
				ligne_releve = dao_ligne_releve.toCreateLigneReleve(degre,releve,employe_id)
				ligne_releve = dao_ligne_releve.toUpdateLigneReleve(ligne_id,ligne_releve)

			else:
				ligne_releve = dao_ligne_releve.toCreateLigneReleve(degre,releve,employe_id)
				ligne_releve = dao_ligne_releve.toSaveLigneReleve(auteur,ligne_releve)

		transaction.savepoint_commit(sid)
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_details_plan_releve',args=(employe_id,)))
	except Exception as e:
		transaction.savepoint_rollback(sid)
		#print('Erreur post_creer_releve')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER SYNDICAT \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, "Erreur lors de L'opération")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_plan_releve',args=(employe_id,)))

#Reconversion Professionnelle
def get_lister_reconversion_professionnelle(request):
	try:
		permission_number = 72
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des employés',
		'model' : model,
		'utilisateur' : utilisateur,
		'modules' : dao_module.toListModulesInstalles(),
		'module' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evolution_personnelle/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))


###  Projets Professionnels

def get_lister_projet_professionnel(request):
	permission_number = 241
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	# model = dao_projet_professionnel.toListProjet_professionnel()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_projet_professionnel.toListProjet_professionnel(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)

	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste de Mes Projets Professionnels',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/projet_professionnel/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_projet_professionnel(request):
	permission_number = 240
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Ajouter un Projet Professionnel',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/projet_professionnel/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_projet_professionnel(request):
	try:
		auteur = identite.utilisateur(request)
		# employe_id = request.POST['employe_id']
		projet = request.POST['projet']
		#print(projet)
		employe = auteur
		#print(employe)

		numero_projet = dao_projet_professionnel.toGenerateProjetProfessionel()
		#print(numero_projet)

		projet_professionnel=dao_projet_professionnel.toCreateProjet_professionnel(projet,employe,numero_projet)
		projet_professionnel=dao_projet_professionnel.toSaveProjet_professionnel(auteur, projet_professionnel)
		if projet_professionnel == None: raise Exception("Une erreur est survenue lors de l'enregistrement du projet professionnel")
		messages.add_message(request, messages.SUCCESS, "L'opération s'est déroulée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_projet_professionnel', args=(projet_professionnel.id,)))
	except Exception as e:
		#print('Erreur post_creer_projet_professionnel')
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER PROJET_PROFESSIONNEL \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_projet_professionnel'))


def get_details_projet_professionnel(request,ref):
	permission_number = 241
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response
	try:
		ref=int(ref)
		projet_professionnel=dao_projet_professionnel.toGetProjet_professionnel(ref)
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/projet_professionnel/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,projet_professionnel)


		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Détails sur {}'.format(projet_professionnel.numero_projet),
			'projet_professionnel' : projet_professionnel,
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
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
			}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS PROJET_PROFESSIONNEL \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_projet_professionnel'))

def get_modifier_projet_professionnel(request,ref):
	permission_number = 242
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_projet_professionnel.toGetProjet_professionnel(ref)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier Projet Professionnel',
		'model':model,
		'utilisateur' :utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/projet_professionnel/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_projet_professionnel(request):

	id = int(request.POST['ref'])
	try:
		auteur = identite.utilisateur(request)
		projet = request.POST['projet']
		employe = auteur

		projet_professionnel = dao_projet_professionnel.toGetProjet_professionnel(id)
		numero_projet = projet_professionnel.numero_projet

		projet_professionnel=dao_projet_professionnel.toCreateProjet_professionnel(projet,employe,numero_projet)
		projet_professionnel=dao_projet_professionnel.toUpdateProjet_professionnel(id, projet_professionnel)
		if projet_professionnel == None: raise Exception("Une erreur est survenue lors de la mise à jour du projet professionnel")
		messages.add_message(request, messages.SUCCESS, "L'opération s'est déroulée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_projet_professionnel', args=(id,)))
	except Exception as e:
		#print('Erreur post_modifier_projet_professionnel')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER PROJET_PROFESSIONNEL \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_projet_professionnel'))

def get_lister_projet(request):
	try:
		permission_number = 72
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des employés',
		'view':view,
		'model' : model,
		'utilisateur' : utilisateur,
		'modules' : modules,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/projet_professionnel/employe/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_projet_employe(request, idt):
	permission_number = 241 #72
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	idt = int(idt)
	employe = dao_employe.toGetEmploye(idt)
	# projet = dao_projet_professionnel.toListProjet_professionnelByEmploye(employe.id)
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_projet_professionnel.toListProjet_professionnelByEmploye(employe.id), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Projets professionnels de '+employe.nom_complet,
		'employe':employe,
		'view':'list',
		'model' : model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/evolution_personnelle/list.html')
	return HttpResponse(template.render(context, request))

def get_upload_projet_professionnel(request):
	try:
		permission_number = 240
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des projets professionnels",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/projet_professionnel/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD PROJET PROFESSIONNEL")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_projet_professionnel"))


@transaction.atomic
def post_upload_projet_professionnel(request):
	sid = transaction.savepoint()
	try:
		#print("upload_projet_professionnel")
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
			projet = str(df['Description du projet'][i])

			"""employe_id = None
			matricule = str(df['matricule'][i])
			employe = models.Model_ProfilRH.objects.filter(matricule__icontains = matricule).first()
			if employe != None :
				employe = models.Model_Employe.objects.filter(profilrh_id = employe.id).first()
				employe_id = employe.id"""

			employe = auteur
			#print(employe)

			numero_projet = dao_projet_professionnel.toGenerateProjetProfessionel()

			projet_professionnel = dao_projet_professionnel.toCreateProjet_professionnel(projet,employe,numero_projet)
			projet_professionnel = dao_projet_professionnel.toSaveProjet_professionnel(auteur, projet_professionnel)
			if projet_professionnel == None: raise Exception("Une erreur est survenue lors de l'enregistrement d'un projet professionnel")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_projet_professionnel"))
	except Exception as e:
		#print("ERREUR POST UPLOAD PROJET PROFESSIONNEL")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD PROJET PROFESSIONNEL \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_projet_professionnel"))


### Recrutement interne
def get_lister_recrutement_interne(request):
	permission_number = 244
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_recrutement_interne.toListRecrutement_interne()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_recrutement_interne.toListRecrutement_interne(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#

	for item in model:
		if item.date_debut == item.date_fin:
			item.est_fini = True
			item.save()
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
		model = pagination.toGet(request, model)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des récrutements internes',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'modules' : modules,
	'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/recrutement_interne/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_recrutement_interne(request):
	permission_number = 245
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	service = dao_unite_fonctionnelle.toListUniteFonctionnelle()
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Ajouter un récrutement interne',
		'utilisateur' : utilisateur,
		'service': service,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/recrutement_interne/add.html')
	return HttpResponse(template.render(context, request))

def post_creer_recrutement_interne(request):

	try:
		designation = request.POST['designation']
		description = request.POST['description']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
		service_id = int(request.POST['service_id'])
		auteur = identite.utilisateur(request)

		est_fini = False

		recrutement_interne=dao_recrutement_interne.toCreateRecrutement_interne(designation,description,date_debut,date_fin,est_fini,service_id)
		recrutement_interne=dao_recrutement_interne.toSaveRecrutement_interne(auteur, recrutement_interne)
		if recrutement_interne == None: raise Exception("Erreur survenue pendant l'enregistrement du recrutement interne")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_recrutement_interne', args=(recrutement_interne.id,)))
	except Exception as e:
		#print('Erreur post_creer_recrutement_interne')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER RECRUTEMENT_INTERNE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_recrutement_interne'))


def get_details_recrutement_interne(request,ref):
	permission_number = 244
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		recrutement_interne=dao_recrutement_interne.toGetRecrutement_interne(ref)

		if recrutement_interne.date_debut == recrutement_interne.date_fin:
			recrutement_interne.est_fini = True
			recrutement_interne.save()

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/recrutement_interne/item.html')
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,recrutement_interne)

		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Détails sur "{}" '.format(recrutement_interne.designation),
			'recrutement_interne' : recrutement_interne,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS RECRUTEMENT_INTERNE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_recrutement_interne'))

def get_modifier_recrutement_interne(request,ref):
	permission_number = 246
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	service = dao_unite_fonctionnelle.toListUniteFonctionnelle()

	ref = int(ref)
	model = dao_recrutement_interne.toGetRecrutement_interne(ref)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier "{}" '.format(model.designation),
		'model':model,
		'utilisateur' : utilisateur,
		'service':service,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/recrutement_interne/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_recrutement_interne(request):

	id = int(request.POST['ref'])
	try:
		designation = request.POST['designation']
		description = request.POST['description']
		date_debut = request.POST['date_debut']
		date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
		date_fin = request.POST['date_fin']
		date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))

		service_id = int(request.POST['service_id'])
		auteur = identite.utilisateur(request)

		est_fini = False
		if 'est_fini' in request.POST: est_fini=True

		recrutement_interne=dao_recrutement_interne.toCreateRecrutement_interne(designation,description,date_debut,date_fin,est_fini,service_id)
		recrutement_interne=dao_recrutement_interne.toUpdateRecrutement_interne(id, recrutement_interne)
		if recrutement_interne == None: raise Exception("Erreur survenue pendant la modification du recrutemnt interne")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_recrutement_interne', args=(id,)))
	except Exception as e:
		#print('Erreur post_modifier_recrutement_interne')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER RECRUTEMENT_INTERNE \n {}'.format(auteur.nom_complet, module,e))
		messages.add_message(request, messages.ERROR, e)
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_update_recrutement_interne', args=(id,)))

def get_upload_recrutement_interne(request):
	try:
		permission_number = 245
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)

		if response != None:
			return response


		context = {
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"title" : "Import de la liste des recrutements internes",
			"utilisateur" : utilisateur,
			"modules" : modules ,
			'sous_modules': sous_modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/recrutement_interne/upload.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print("ERREUR GET UPLOAD RECRUTEMENT INTERNE")
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_ressources_humaines_list_recrutement_interne"))


@transaction.atomic
def post_upload_recrutement_interne(request):
	sid = transaction.savepoint()
	try:
		#print("upload_recrutement_interne")
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
			date_debut = str(df['date_debut'][i])
			date_fin = str(df['date_fin'][i])

			service_id = None
			service = str(df['service'][i])
			service = models.Model_Unite_fonctionnelle.objects.filter(libelle__icontains = service).first()
			if service != None : service_id = service.id

			#conversion de la date
			#print("date_debut: {}".format(date_debut))
			if len(date_debut) == 10:
				date_debut = timezone.datetime(int(date_debut[6:10]), int(date_debut[3:5]), int(date_debut[0:2]))
			elif len(date_debut) > 10:
				date_debut = timezone.datetime(int(date_debut[0:4]), int(date_debut[5:7]), int(date_debut[8:10]))

			#print("date_fin: {}".format(date_fin))
			if len(date_fin) == 10:
				date_fin = timezone.datetime(int(date_fin[6:10]), int(date_fin[3:5]), int(date_fin[0:2]))
			elif len(date_fin) > 10:
				date_fin = timezone.datetime(int(date_fin[0:4]), int(date_fin[5:7]), int(date_fin[8:10]))

			est_fini = False

			recrutement_interne = dao_recrutement_interne.toCreateRecrutement_interne(designation, description, date_debut, date_fin, est_fini, service_id)
			recrutement_interne = dao_recrutement_interne.toSaveRecrutement_interne(auteur, recrutement_interne)
			if recrutement_interne == None: raise Exception("Erreur survenue pendant l'enregistrement d'un recrutemnt interne")
		messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
		transaction.savepoint_commit(sid)
		return HttpResponseRedirect(reverse("module_ressourceshumaines_list_recrutement_interne"))
	except Exception as e:
		#print("ERREUR POST UPLOAD RECRUTEMENT INTERNE")
		#print(e)
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST UPLOAD FONCTION \n {}'.format(auteur.nom_complet, module,e))
		return HttpResponseRedirect(reverse("module_ressourceshumaines_add_recrutement_interne"))


#### Requête

def get_lister_requete(request):
	permission_number = 280
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_requete.toListRequete()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_requete.toListRequete(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des requêtes des besoins de mission',
		'model' : model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete/list.html')
	return HttpResponse(template.render(context, request))

def get_lister_requete_by_user(request):
	permission_number = 280
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	# model = dao_requete.toListRequeteByUser(utilisateur.id)
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_requete.toListRequeteByUser(utilisateur.id), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des requêtes de besoin de {}'.format(utilisateur.nom_complet),
		'model' : model,
		'view':view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_requete(request):
	permission_number = 281
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	demandeurs = dao_employe.toListEmployesActifs()
	# fournisseurs = dao_fournisseur.toListFournisseursActifs()
	# articles = dao_article.toListArticlesAchetables()
	# categories = dao_categorie_article.toListCategoriesArticle()
	dep_entrepots = dao_unite_fonctionnelle.toListUniteFonctionnelleWH()

	centre_cout = dao_centre_cout.toListCentre_cout()
	numero_requete = dao_requete.toGenerateNumeroRequete()
	ligne_budgetaires = dao_ligne_budgetaire.toListLigneBudgetaires()


	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Créer une requête de mission',
		'utilisateur' : utilisateur,
		'modules' : modules,
		'numero_requete': numero_requete,
		'demandeurs' : demandeurs,
		'centre_cout':centre_cout,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'ligne_budgetaires' : ligne_budgetaires,
		# 'articles' : articles,
		'warehouses' : dep_entrepots,
		# 'categories' : categories,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_requete(request):
	sid = transaction.savepoint()
	try:
		#numero_reference = request.POST['numero_reference']
		demandeur_id = int(request.POST['demandeur_id'])
		#print(demandeur_id)
		date_requete = request.POST['date_requete']
		date_requete = timezone.datetime(int(date_requete[6:10]), int(date_requete[3:5]), int(date_requete[0:2]))
		date_retour = request.POST['date_retour']
		date_retour = timezone.datetime(int(date_retour[6:10]), int(date_retour[3:5]), int(date_retour[0:2]))
		description = request.POST['description_id']
		#print(description)
		service_ref_id = int(request.POST['service_ref_id'])
		#centre_cout_id = request.POST['centre_cout_id']
		#document = request.POST['document']
		#statut_id = request.POST['statut_id']
		#etat = request.POST['etat']
		#auteur_id = request.POST['auteur_id']
		#url = request.POST['url']
		auteur = identite.utilisateur(request)
		numero_reference = dao_requete.toGenerateNumeroRequete()

		requete=dao_requete.toCreateRequete(numero_reference,demandeur_id,date_requete,date_retour,description,service_ref_id,None,"","","")
		requete=dao_requete.toSaveRequete(auteur, requete)
		#print('**VIEWS REQUETE DE MISSION**', requete)
		url = '<a class="lien chargement-au-click" href="/ressourceshumaines/requete/item/'+str(requete.id)+'/">'+requete.numero_reference+'</a>'
		requete.url = url
		requete.save()

		list_ligne_requete = []
		est_viable = False


		if requete != None:
			list_ligne_requete = request.POST.getlist('ligne_requete', None)
			list_ligne_requet = request.POST.getlist('ligne_requet', None)
			#print("Test %s" %list_ligne_requete)
			# #print("Ma liste %s" %list_ligne_requete)
			list_id1 = request.POST.getlist('id1', None)
			list_description = request.POST.getlist('description', None)
			#print("Ma description %s" %list_description)
			#print("Taille de la ligne de requete %s" %len(list_ligne_requete))
			#print(kk)
			## Demandeur add by galo
			demandeur = dao_employe.toGetEmploye(demandeur_id)
			#print(demandeur.poste.designation)

			if len(list_ligne_requete) >=1:
				if list_ligne_requete[0]:
					est_viable = True

			status = 0

			if "assistant" in demandeur.poste.designation.lower():
				status = 3
			# elif "projet" in demandeur.poste.designation.lower() or "bureau" in demandeur.poste.designation.lower():
			# 	status = 4
			elif "service" in demandeur.poste.designation.lower():
				status = 2
			elif "directeur" in demandeur.poste.designation.lower():
				status = 1
			elif demandeur.poste.designation.lower() == "directeur général" or demandeur.poste.designation.lower() == "directeur general":
				status = 1
			else:
				status = 4

			#print(status)

			status = dao_type_status.toGetTypeStatus(int(status))

			#print(status)
			ligne_requete_add = dao_ligne_requete.toCreateLigne_requete(requete.id,demandeur_id,0,0,"", status["designation"])
			ligne_requete_add = dao_ligne_requete.toSaveLigne_requete(auteur, ligne_requete_add)


			if len(list_ligne_requete) >= 1 and est_viable:
				for i in range(0, len(list_ligne_requete)) :
					#print("argh")
					employe_id =int(list_ligne_requete[i])
					employe = dao_employe.toGetEmploye(employe_id)
					#print("Nom de l'employé %s" %employe.nom_complet)
					#Ajout de la pondération en fonction occupée
					"""
					Les pondérations sont sur 10 suivant le barême suivant :

					DG = 10
					Autres Directeurs = 8
					Chef de service = 6
					Chef de bureau et Chef de projet = 4
					Assistant = 2

					"""

					status = 0

					if employe.poste:
						if "assistant" in employe.poste.designation.lower():
							status = 3
						# elif "projet" in employe.poste.designation.lower() or "bureau" in employe.poste.designation.lower():
						# 	status = 4
						elif "service" in employe.poste.designation.lower():
							status = 2
						elif "directeur" in employe.poste.designation.lower():
							status = 1
						elif employe.poste.designation.lower() == "directeur général" or employe.poste.designation.lower() == "directeur general":
							status = 1
						else:
							status = 4
					else:
						status = 4

					status = dao_type_status.toGetTypeStatus(int(status))

					#print("POSTE de l'employe %s" %employe.poste)
					#print("employe done!")
					ligne_requete=dao_ligne_requete.toCreateLigne_requete(requete.id,employe_id,0,0,"", status["designation"])
					ligne_requete=dao_ligne_requete.toSaveLigne_requete(auteur, ligne_requete)

			#Initialisation du workflow expression
			wkf_task.initializeWorkflow(auteur,requete)

			transaction.savepoint_commit(sid)
			#print("OKAY")
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_requete', args=(requete.id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_ressourceshumaines_add_requete'))

		#return HttpResponseRedirect(reverse('module_ressourceshumaines_list_requete'))
	except Exception as e:
		#print('Erreur lors de l\'enregistrement')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER REQUETE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_requete'))


def get_details_requete(request,ref):
	permission_number = 280
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		requete=dao_requete.toGetRequete(ref)

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,requete)

		lignes = dao_ligne_requete.toGetLigneRequeteOfRequete(requete.id)

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete/item.html')
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Détails sur la requête de mission',
			'requete' : requete,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'model':requete,
			'lignes' : lignes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'content_type_id':content_type_id,
			"utilisateur" : utilisateur,
			'roles':groupe_permissions,
			'documents':documents,
			'modules' : modules,
			'signee':signee,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
			}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS REQUETE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_requete'))
def get_modifier_requete(request,ref):
	permission_number = 282
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	ref = int(ref)
	model = dao_requete.toGetRequete(ref)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier la requête de besoin de mission',
		'model':model,
		'utilisateur': utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : dao_module.toListModulesInstalles(),
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete/update.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_modifier_requete(request):
	sid = transaction.savepoint()
	id = int(request.POST['ref'])
	try:
		numero_reference = request.POST['numero_reference']
		demandeur_id = request.POST['demandeur_id']
		date_requete = request.POST['date_requete']
		date_requete = timezone.datetime(int(date_requete[6:10]), int(date_requete[3:5]), int(date_requete[0:2]))
		#ligne_budgetaire_id = int(request.POST['ligne_budgetaire_id'])
		description = request.POST['description']
		service_ref_id = request.POST['service_ref_id']
		#centre_cout_id = request.POST['centre_cout_id']
		#document = request.POST['document']
		#statut_id = request.POST['statut_id']
		#etat = request.POST['etat']
		auteur_id = request.POST['auteur_id']
		#url = request.POST['url']
		#auteur = identite.utilisateur(request)

		requete=dao_requete.toCreateRequete(numero_reference,demandeur_id,date_requete,None,description,service_ref_id,None,"","","")
		requete=dao_requete.toUpdateRequete(id, requete)

		if requete != None:
			list_ligne_requete = request.POST.getlist('ligne_requete', None)
			#print(len(list_ligne_requete))
			for i in range(0, len(list_ligne_requete)) :
				#print("argh")
				employe_id =int(list_ligne_requete[i])
				employe = dao_employe.toGetEmploye(employe_id)

				#print("employe done!")
				ligne_requete=dao_ligne_requete.toCreateLigne_requete(requete.id,employe.id,0,0.0,description,status)
				ligne_requete=dao_ligne_requete.toUpdateLigne_requete(auteur, ligne_requete)

			transaction.savepoint_commit(sid)
			#print("OKAY")
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_requete', args=(requete.id,)))

		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_ressourceshumaines_update_requete'))

		#return HttpResponseRedirect(reverse('module_ressourceshumaines_list_requete'))
	except Exception as e:
		#print('Erreur post_modifier_requete')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER REQUETE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		messages.add_message(request, messages.ERROR, e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_update_requete'))


###### Ordre de mission
def get_lister_ordre_de_mission(request):
	permission_number = 284 #285
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_ordre_de_mission.toListOrdre_de_mission()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_ordre_de_mission.toListOrdre_de_mission(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des ordres de mission',
		'model' : model,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ordre_de_mission/list.html')
	return HttpResponse(template.render(context, request))

def get_lister_ordre_by_user(request):
	permission_number = 284
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_ordre_de_mission.toListOrdreByUser(utilisateur.id)
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_ordre_de_mission.toListOrdreByUser(utilisateur.id), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des ordres de mission de {}'.format(utilisateur.nom_complet),
		'model' : model,
		'view':view,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'utilisateur' : utilisateur,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 1
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ordre_de_mission/list.html')
	return HttpResponse(template.render(context, request))


def get_creer_ordre_de_mission(request):
	permission_number = 286
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	requetes = dao_requete.toListRequete()

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
		etat = dao_requete.toGetRequete(etat_actuel_id)
		lignes = dao_ligne_requete.toGetLigneRequeteOfRequete(etat.id)
		etape_wkf_id = request.POST["etape_id"]
		expression_wkf_id = request.POST["doc_id"]
		#etat_besoins = dao_expression_besoin.toListExpressionsServiceReferent()
	except Exception as e:
		#print("Aucun etat de besoin trouvé")
		pass

	#print("ETAAAAAAAAATTTTTTTTTTTTT %s" % etat_actuel_id)

	ligne_budgetaires = dao_ligne_budgetaire.toListLigneBudgetaires()


	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Créer un ordre de mission',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'etat' : etat,
		'ligne_budgetaires' : ligne_budgetaires,
		'demandeurs':dao_employe.toListEmployesActifs(),
		'requetes':requetes,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'lignes_etat'  : lignes,
		'expression_wkf' : expression_wkf_id,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ordre_de_mission/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_ordre_de_mission(request):
	sid = transaction.savepoint()

	try:
		objet_mission = request.POST['objet_mission']
		#print(objet_mission)
		destination = request.POST['destination']
		#print('****La destination*****%s' %destination)
		moyen_transport = request.POST['moyen_transport']
		#print(moyen_transport)
		date_depart = request.POST['date_depart']
		ligne_budgetaire_id = request.POST['ligne_budgetaire_id']
		if ligne_budgetaire_id == "" or ligne_budgetaire_id == "0":
			ligne_budgetaire_id = None
		else:
			ligne_budgetaire_id = int(ligne_budgetaire_id)

		#print(date_depart)
		date_depart = timezone.datetime(int(date_depart[6:10]), int(date_depart[3:5]), int(date_depart[0:2]))
		date_retour = request.POST['date_retour']
		#print(date_retour)
		date_retour = timezone.datetime(int(date_retour[6:10]), int(date_retour[3:5]), int(date_retour[0:2]))
		# frais_mission = request.POST['frais_mission']
		description = request.POST['description']
		#print(description)
		type = request.POST['type']
		demandeur = int(request.POST['demandeur_id'])
		demandeur = dao_employe.toGetEmploye(demandeur)
		observation = request.POST['objectif']
		#url = request.POST['url']
		auteur = identite.utilisateur(request)


		requete_id = None
		#print("moma")
		if 'requete_id' in request.POST:
			requete_id = request.POST['requete_id']
			if requete_id == "":
				requete_id = None

		ordre_de_mission=dao_ordre_de_mission.toCreateOrdre_de_mission(objet_mission,destination,moyen_transport,date_depart,date_retour,description,observation,type,requete_id,ligne_budgetaire_id)
		ordre_de_mission=dao_ordre_de_mission.toSaveOrdre_de_mission(auteur, ordre_de_mission)

		#print(ordre_de_mission)
		ordre_de_mission.demandeur = demandeur
		url = '<a class="lien chargement-au-click" href="/ressourceshumaines/ordre_de_mission/item/'+str(ordre_de_mission.id)+'/">'+ordre_de_mission.numero_ordre+'</a>'
		ordre_de_mission.url = url
		ordre_de_mission.save()

		total_frais_mission = 0
		total_frais_hebergement = 0
		total = 0

		if ordre_de_mission != None:
			list_ligne_ordre = request.POST.getlist('employe', None)
			#print("Ma liste %s" %list_ligne_ordre)
			#list_id1 = request.POST.getlist('id1', None)
			list_frais_mission = request.POST.getlist('frais_mission', None)
			list_frais_hebergement = request.POST.getlist('frais_hebergement', None)
			list_description = request.POST.getlist('description', None)
			#print("Taille de la ligne de ordre %s" %len(list_ligne_ordre))
			for i in range(0, len(list_ligne_ordre)) :
				#print("argh")
				employe_id =int(list_ligne_ordre[i])
				employe = dao_employe.toGetEmploye(employe_id)
				frais_de_mission = int(list_frais_mission[i])
				total_frais_mission+= frais_de_mission
				frais_hebergement = makeFloat(list_frais_hebergement[i])
				total_frais_hebergement += frais_hebergement
				total = makeFloat(total_frais_mission)+makeFloat(total_frais_hebergement)

				ordre_de_mission.frais_mission = makeFloat(total)
				#print('******POST ORDRE DE MISSION*******')
				#print("Nom de l'employé %s" %employe.nom_complet)
				#print("POSTE de l'employe %s" %employe.poste)
				#print("employe done!")


				status = 0


				if employe.poste:
					if "assistant" in employe.poste.designation.lower():
						status = 3
						#print(models.TypeStatus[3])
					# elif "projet" in employe.poste.designation.lower() or "bureau" in employe.poste.designation.lower():
					# 	status = 4
					elif "service" in employe.poste.designation.lower():
						status = 2
					elif "directeur" in employe.poste.designation.lower():
						status = 1
					elif employe.poste.designation.lower() == "directeur général" or employe.poste.designation.lower() == "directeur general":
						status = 1
					else:
						status = 4
				else:
					status = 4

				status = dao_type_status.toGetTypeStatus(int(status))

													#toCreateLigne_ordre_de_mission(ordre_mission_id,employe_id,frais_de_mission,frais_hebergement,status)
				ligne_ordre=dao_ligne_ordre_de_mission.toCreateLigne_ordre_de_mission(ordre_de_mission.id,employe.id,frais_de_mission,frais_hebergement,status["designation"])
				ligne_ordre=dao_ligne_ordre_de_mission.toSaveLigne_ordre_de_mission(auteur, ligne_ordre)


			#Initialisation du workflow expression
			wkf_task.initializeWorkflow(auteur,ordre_de_mission)


			if (requete_id != "" and requete_id != None):
				#print("inside the box")
				requete = dao_requete.toGetRequete(requete_id)
				wkf_task.passingStepWorkflow(auteur,requete)

			# else:
			# 	#MyWay MaTransition
			# 	for i in range(0, len(list_expression_id)) :
			# 		requete_id = list_expression_id[i]
			# 		expression = dao_requete.toGetRequete(requete_id)
			# 		wkf_task.passingStepWorkflow(auteur,expression)

			transaction.savepoint_commit(sid)
			#print("OKAY")
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_ordre_de_mission', args=(ordre_de_mission.id,)))

		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_ressourceshumaines_add_ordre_de_mission'))
		# return HttpResponseRedirect(reverse('module_ressourceshumaines_list_ordre_de_mission'))
	except Exception as e:
		#print('Erreur post_creer_ordre_de_mission')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de L'opération")
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER ORDRE_DE_MISSION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_ordre_de_mission'))


def get_details_ordre_de_mission(request,ref):
	permission_number = 284
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		ordre_de_mission=dao_ordre_de_mission.toGetOrdre_de_mission(ref)

		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,ordre_de_mission)

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ordre_de_mission/item.html')

		lignes = dao_ligne_ordre_de_mission.toGetLigneRequeteOfOrdreMission(ordre_de_mission.id)

		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Détails sur l\' ordre de mission',
			'model' : ordre_de_mission,
			'historique' : historique,
			'etapes_suivantes' : transition_etape_suivant,
			'content_type_id':content_type_id,
			"utilisateur" : utilisateur,
			'roles':groupe_permissions,
			'lignes':lignes,
			'signee':signee,
			'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
			'documents':documents,
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
			}

		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreur get_details_ordre_de_mission')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS ORDRE_DE_MISSION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_ordre_de_mission'))
def get_modifier_ordre_de_mission(request,ref):
	permission_number = 287
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

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
		etat = dao_requete.toGetRequete(etat_actuel_id)
		lignes = dao_ligne_requete.toGetLigneRequeteOfRequete(etat.id)
		etape_wkf_id = request.POST["etape_id"]
		expression_wkf_id = request.POST["doc_id"]
	except Exception as e:
		#print("Aucun etat de besoin trouvé")
		pass

	#print("ETAAAAAAAAATTTTTTTTTTTTT %s" % etat_actuel_id)

	ref = int(ref)
	model = dao_ordre_de_mission.toGetOrdre_de_mission(ref)
	context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Modifier l\'ordre de mission',
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'etat' : etat,
		'model':model,
		'demandeurs':dao_employe.toListEmployesActifs(),
		'requetes':requetes,
		'etat_actuel_id' : int(etat_actuel_id),
		'etape_wkf' : etape_wkf_id,
		'lignes_etat'  : lignes,
		'expression_wkf' : expression_wkf_id,
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 2
		}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ordre_de_mission/update.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_modifier_ordre_de_mission(request):
	sid = transaction.savepoint()
	try:
		id = int(request.POST['ref'])
		objet_mission = request.POST['objet_mission']
		#print(objet_mission)
		destination = request.POST['destination']
		#print(destination)
		moyen_transport = request.POST['moyen_transport']
		#print(moyen_transport)
		date_depart = request.POST['date_depart']
		ligne_budgetaire_id = int(request.POST['ligne_budgetaire_id'])
		#print(date_depart)
		date_depart = timezone.datetime(int(date_depart[6:10]), int(date_depart[3:5]), int(date_depart[0:2]))
		date_retour = request.POST['date_retour']
		#print(date_retour)
		date_retour = timezone.datetime(int(date_retour[6:10]), int(date_retour[3:5]), int(date_retour[0:2]))
		#frais_mission = request.POST['frais_mission']
		description = request.POST['description']
		#print(description)
		type = request.POST['type']
		demandeur = int(request.POST['demandeur_id'])
		demandeur = dao_employe.toGetEmploye(demandeur)
		observation = request.POST['objectif']
		#url = request.POST['url']
		auteur = identite.utilisateur(request)


		requete_id = None
		#print("moma")
		if 'requete_id' in request.POST:
			requete_id = request.POST['requete_id']
			if requete_id == "":
				requete_id = None

		ordre_de_mission=dao_ordre_de_mission.toCreateOrdre_de_mission(objet_mission,destination,moyen_transport,date_depart,date_retour,description,observation,type,requete_id,ligne_budgetaire_id)
		ordre_de_mission=dao_ordre_de_mission.toUpdateOrdre_de_mission(id, ordre_de_mission)

		# ligne_ordre_de_mission=dao_ligne_ordre_de_mission.toCreateLigne_ordre_de_mission(ordre_mission_id,employe_id,quantite_unitaire,prix_unitaire,description,url,auteur_id)
		# ligne_ordre_de_mission=dao_ligne_ordre_de_mission.toUpdateLigne_ordre_de_mission(id, ligne_ordre_de_mission)

		#print(ordre_de_mission)
		ordre_de_mission.demandeur = demandeur
		url = '<a class="lien chargement-au-click" href="/ressourceshumaines/ordre_de_mission/item/'+str(ordre_de_mission.id)+'/">'+ordre_de_mission.numero_ordre+'</a>'
		ordre_de_mission.url = url
		ordre_de_mission.save()

		total_frais_mission = 0
		total_frais_hebergement = 0
		total = 0

		if ordre_de_mission != None:
			list_ligne_ordre = request.POST.getlist('employe', None)
			#print("Ma liste %s" %list_ligne_ordre)
			#list_id1 = request.POST.getlist('id1', None)
			list_frais_mission = request.POST.getlist('frais_mission', None)
			list_frais_hebergement = request.POST.getlist('frais_hebergement', None)
			list_description = request.POST.getlist('description', None)
			#print("Taille de la ligne de ordre %s" %len(list_ligne_ordre))
			for i in range(0, len(list_ligne_ordre)) :
				#print("argh")
				employe_id =int(list_ligne_ordre[i])
				employe = dao_employe.toGetEmploye(employe_id)
				frais_de_mission = int(list_frais_mission[i])
				total_frais_mission+= frais_de_mission
				frais_hebergement = makeFloat(list_frais_hebergement[i])
				total_frais_hebergement += frais_hebergement
				total = makeFloat(total_frais_mission)+makeFloat(total_frais_hebergement)

				ordre_de_mission.frais_mission = makeFloat(total)

				#print("Nom de l'employé %s" %employe.nom_complet)
				_description = list_description[i]

				#print("POSTE de l'employe %s" %employe.poste)
				#print("employe done!")


				status = 0


				if "assistant" in employe.poste.designation.lower():
					status = 3
					#print(models.TypeStatus[3])
				# elif "projet" in employe.poste.designation.lower() or "bureau" in employe.poste.designation.lower():
				# 	status = 4
				elif "service" in employe.poste.designation.lower():
					status = 2
				elif "directeur" in employe.poste.designation.lower():
					status = 1
				elif employe.poste.designation.lower() == "directeur général" or employe.poste.designation.lower() == "directeur general":
					status = 1
				else:
					status = 4

				status = dao_type_status.toGetTypeStatus(int(status))

													#toCreateLigne_ordre_de_mission(ordre_mission_id,employe_id,frais_de_mission,frais_hebergement,status)
				ligne_ordre=dao_ligne_ordre_de_mission.toCreateLigne_ordre_de_mission(ordre_de_mission.id,employe.id,frais_de_mission,frais_hebergement,status["designation"])
				ligne_ordre=dao_ligne_ordre_de_mission.toSaveLigne_ordre_de_mission(auteur, ligne_ordre)


			# else:
			# 	#MyWay MaTransition
			# 	for i in range(0, len(list_expression_id)) :
			# 		requete_id = list_expression_id[i]
			# 		expression = dao_requete.toGetRequete(requete_id)
			# 		wkf_task.passingStepWorkflow(auteur,expression)

			transaction.savepoint_commit(sid)
			#print("OKAY")
			if ligne_ordre == None: raise Exception("Erreur survenue pendant l'enregistrement")
			messages.add_message(request, messages.SUCCESS, "L'opération effectuée avec succès")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_ordre_de_mission', args=(ordre_de_mission.id,)))
		else:
			transaction.savepoint_rollback(sid)
			return HttpResponseRedirect(reverse('module_ressourceshumaines_add_ordre_de_mission'))
	except Exception as e:
		#print('Erreur post_modifier_ordre_de_mission')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER ORDRE_DE_MISSION \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_ordre_de_mission'))


######################################################## RAPPORTS ################################################################

def get_print_ordre_mission(request):
	try:
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetDashboardAuthentification(8, request)
		if response != None:
			return response

		id = request.POST["id"]
		#print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK " + str(id))

		end = endpoint.reportingEndPoint()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Impression d\'un ordre de mission ',
			'id' : id,
			'endpoint' : end,
			'utilisateur' : utilisateur,
			'modules' : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 4
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/ordre_de_mission/print.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module='ModuleRessourcesHumaines'
		monLog.error("{} :: {}::\nERREUR LORS DE L'IMPRESSION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreut Liste')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))


def get_lister_employe_suivi_carriere(request):
	try:
		permission_number = 392
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_employe.toListEmployes()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_employe.toListEmployes(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Suivi de carrière: Liste des employés',
		'model' : model,
		'view':view,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/rapport/Suivi_carriere/list.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_print_rapport_suivi_carriere_employe(request, ref):
	try:
		permission_number =392
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		#print(id)

		model = dao_employe.toGetEmploye(id)
		#print("Employe : ", model)
		emplois = dao_emploi.toListEmploiOfEmploye(id)
		#print("Emplois : ", emplois)
		mobilites = dao_mobilite.toGetMobiliteByEmploye(id)
		#print("Mobilités : ", mobilites)
		evaluations = dao_evaluation.toGetEvaluationByEmploye(id)
		#print("Evaluation : ", evaluations)
		formations = dao_ligne_formation.toGetLigneFormationOfEmploye(id)
		#print("Formations : ", formations)
		documents = dao_document.toListDocumentbyObjetModele(model)

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Suivi de carrière de {}'.format(model.nom_complet),
		'model' : model,
		'emplois':emplois,
		'mobilites' : mobilites,
		'documents' : documents,
		'evaluations':evaluations,
		'formations': formations,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		return weasy_print("ErpProject/ModuleRessourcesHumaines/reporting/suivi_carriere.html", "suivi_carriere.pdf", context)
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_suivi_carriere_employe(request, ref):
	try:
		permission_number = 392
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		#print(id)

		model = dao_employe.toGetEmploye(id)
		#print("Employe : ", model)
		emplois = dao_emploi.toListEmploiOfEmploye(id)
		#print("Emplois : ", emplois)
		mobilites = dao_mobilite.toGetMobiliteByEmploye(id)
		#print("Mobilités : ", mobilites)
		evaluations = dao_evaluation.toGetEvaluationByEmploye(id)
		#print("Evaluation : ", evaluations)
		formations = dao_ligne_formation.toGetLigneFormationOfEmploye(id)
		#print("Formations : ", formations)
		documents = dao_document.toListDocumentbyObjetModele(model)

		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Suivi de carrière de {}'.format(model.nom_complet),
		'model' : model,
		'emplois':emplois,
		'mobilites' : mobilites,
		'documents' : documents,
		'evaluations':evaluations,
		'formations': formations,
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 5
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/rapport/Suivi_carriere/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur Lister Employes')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_lister_requete_competence(request):
	permission_number = 365
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	# model = dao_requete_competence.toListRequete_competence()
	#*******Filtre sur les règles **********#
	model = dao_model.toListModel(dao_requete_competence.toListRequete_competence(), permission_number, groupe_permissions, identite.utilisateur(request))
	#******* End Regle *******************#
	try:
		view = str(request.GET.get("view","list"))
	except Exception as e:
		view = "list"
	model = pagination.toGet(request, model)

	context ={
	'modules':modules,'sous_modules':sous_modules,
		'title' : 'Liste des requêtes de compétence',
			'view':view,
				'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
	'model' : model,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 1}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete_competence/list.html')
	return HttpResponse(template.render(context, request))

def get_creer_requete_competence(request):
	permission_number = 364
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	context ={'modules':modules,'sous_modules':sous_modules,
	'title' : 'Effectuer une requête de compétence',
	'actions':auth.toGetActions(modules,utilisateur),
		'numero_requete': dao_requete_competence.toGenerateNumeroRequete(),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete_competence/add.html')
	return HttpResponse(template.render(context, request))

@transaction.atomic
def post_creer_requete_competence(request):
	sid = transaction.savepoint()
	try:
		#print("here we are")
		numero_requete = dao_requete_competence.toGenerateNumeroRequete()
		competence = request.POST['competence']
		observation = request.POST['observation']
		employe_id = request.POST['employe_id']


		auteur = identite.utilisateur(request)

		requete_competence=dao_requete_competence.toCreateRequete_competence(numero_requete,competence,observation,employe_id)
		requete_competence=dao_requete_competence.toSaveRequete_competence(auteur, requete_competence)
		#print("saved ?")

		if requete_competence:
			#Integre le dossiers Uploader here
			#print("we inn")
			if 'file_upload' in request.FILES:
				files = request.FILES.getlist("file_upload",None)
				dao_document.toUploadDocument(auteur,files, requete_competence)

		wkf_task.initializeWorkflow(auteur, requete_competence)
		transaction.savepoint_commit(sid)

		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_requete_competence'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		transaction.savepoint_rollback(sid)
		auteur = identite.utilisateur(request)
		messages.error(request,e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER REQUETE_COMPETENCE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_requete_competence'))


def get_details_requete_competence(request,ref):
	permission_number = 365
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response
	try:
		ref=int(ref)
		requete_competence=dao_requete_competence.toGetRequete_competence(ref)

		#Traitement et recuperation des informations importantes à afficher dans l'item.html
		historique, transition_etape_suivant, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,requete_competence)

		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete_competence/item.html')
		context ={
		'modules':modules,'sous_modules':sous_modules,
		'title' : 'Détails sur une requête de compétence',
		'historique' : historique,
		'etapes_suivantes' : transition_etape_suivant,
		'signee' : signee,
		'roles' : groupe_permissions,
		'documents': documents,
		'content_type_id':content_type_id,
		'model' : requete_competence,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),'requete_competence' : requete_competence,'utilisateur' : utilisateur,'modules' : modules,'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 4}


		return HttpResponse(template.render(context, request))
	except Exception as e:
		#print('Erreut Get Detail')
		messages.error(request,e)
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU GET DETAILS REQUETE_COMPETENCE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_requete_competence'))
def get_modifier_requete_competence(request,ref):
	permission_number = 366
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
			return response

	ref = int(ref)
	model = dao_requete_competence.toGetRequete_competence(ref)
	context ={
	'modules':modules,'sous_modules':sous_modules,
	'title' : 'Modifier une requête de compétence',
	'actions':auth.toGetActions(modules,utilisateur),
	'organisation': dao_organisation.toGetMainOrganisation(),
	'model':model, 'utilisateur': utilisateur,'modules' : dao_module.toListModulesInstalles(),'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,'menu' : 2}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/requete_competence/update.html')
	return HttpResponse(template.render(context, request))

def post_modifier_requete_competence(request):

	id = int(request.POST['ref'])
	try:
		numero_requete = request.POST['numero_requete']
		competence = request.POST['competence']
		observation = request.POST['observation']
		employe_id = request.POST['employe_id']
		auteur = identite.utilisateur(request)

		requete_competence=dao_requete_competence.toCreateRequete_competence(numero_requete,competence,observation,employe_id)
		requete_competence=dao_requete_competence.toUpdateRequete_competence(id, requete_competence)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_requete_competence'))
	except Exception as e:
		#print('Erreur lors de l enregistrement')
		auteur = identite.utilisateur(request)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST MODIFIER REQUETE_COMPETENCE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_requete_competence'))




# TYPE UNITE FONCTIONNELLE CONTROLLERS
def get_lister_type_unite_fonctionnelle(request):
	try:
		permission_number = 77
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		# model = dao_type_unite_fonctionnelle.toList()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_type_unite_fonctionnelle.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		title = "Liste des types d'organisation"
		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : title,
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_unite_fonctionnelle/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de la recuperation des type_unite_fonctionnelles \n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de la recuperation des type_unite_fonctionnelles')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_unite_fonctionnelle'))

def get_details_type_unite_fonctionnelle(request, ref):
	try:
		permission_number = 77
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_type_unite_fonctionnelle.toGet(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,model)



		context ={
			'modules':modules,'sous_modules':sous_modules,
			'title' : "type d'organisation {}".format(model.designation),
			'model' : model,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_unite_fonctionnelle/item.html')
		return HttpResponse(template.render(context, request))

	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Details type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Detail type_unite_fonctionnelle')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_unite_fonctionnelle'))

def get_creer_type_unite_fonctionnelle(request):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer un type d'organisation",
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_unite_fonctionnelle/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_unite_fonctionnelle'))

def post_creer_type_unite_fonctionnelle(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		type_unite_fonctionnelle = dao_type_unite_fonctionnelle.toCreate(designation, description)
		type_unite_fonctionnelle = dao_type_unite_fonctionnelle.toSave(auteur,type_unite_fonctionnelle)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_type_unite_fonctionnelle', args=(type_unite_fonctionnelle.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur lors de Post Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_type_unite_fonctionnelle'))

def get_modifier_type_unite_fonctionnelle(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		ref = int(ref)
		model = dao_type_unite_fonctionnelle.toGet(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier {}'.format(model.designation),
			'model' : model,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_unite_fonctionnelle/update.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Modifier type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Get Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_unite_fonctionnelle'))

def post_modifier_type_unite_fonctionnelle(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		type_unite_fonctionnelle = dao_type_unite_fonctionnelle.toCreate(designation, description)
		type_unite_fonctionnelle = dao_type_unite_fonctionnelle.toUpdate(ref, type_unite_fonctionnelle)

		if type_unite_fonctionnelle == False:
			raise  Exception("Erreur modification")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_type_unite_fonctionnelle', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier type organisation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_unite_fonctionnelle'))


#
def get_creer_Categorie(request):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer Catégorie",
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26

		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/categorie/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

def post_add_CategorieDesignation(request):

	try:

		designation = request.POST["designation"]
		description = request.POST["description"]

		categorie = dao_categorieDesignation.toCreateCategorie(designation, description)
		categorie = dao_categorieDesignation.toSaveCategorie(categorie)

		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_CategorieDesignation', args=(categorie.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier CategorieDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

def post_update_CategorieDesignation(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		categorie = dao_categorieDesignation.toCreateCategorie(designation, description)
		categorie = dao_categorieDesignation.toUpdateCategorie(ref,categorie)

		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_CategorieDesignation', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier type CategorieDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

def get_details_Categorie(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		categorie = dao_categorieDesignation.toGetCategorie(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,categorie)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : categorie.designation,
			'model' : categorie,
			'menu' : 5,
			"modules" : modules,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/categorie/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER CATEGORIE DESIGNATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

def get_lister_CategorieDesignation(request):
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_fonction.toListFonction()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_categorieDesignation.toListcategories(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		# #print('rrrrrrrrrrrrrrrrrrrrrrrr')
		# for m in model:
		# 	#print("Désignation : {} ,  ID : {} ".format(m.designation, m.id))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des catégories',
			'model' : model,
			'menu' : 5,
			'view':view,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/categorie/list.html")
		return HttpResponse(template.render(context, request))

def get_update_Categorie(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		categorie = dao_categorieDesignation.toGetCategorie(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : categorie.designation,
			'model' : categorie,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/categorie/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER CATEGORIE DESIGNATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

#
def get_creer_Echelon(request):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer Echelon",
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26

		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/echelon/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_EchelonDesignation'))

def post_add_EchelonDesignation(request):

	try:

		designation = request.POST["designation"]
		description = request.POST["description"]

		echelon = dao_EchelonDesignation.toCreateEchelon(designation, description)
		echelon = dao_EchelonDesignation.toSaveEchelon(echelon)

		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_EchelonDesignation', args=(echelon.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier EchelonDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_EchelonDesignation'))

def post_update_EchelonDesignation(request):
	ref = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		echelon = dao_EchelonDesignation.toCreateEchelon(designation, description)
		echelon = dao_EchelonDesignation.toUpdateEchelon(ref,echelon)

		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_EchelonDesignation', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier type echelonDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_EchelonDesignation'))

def get_details_Echelon(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		echelon = dao_EchelonDesignation.toGetEchelon(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,echelon)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : echelon.designation,
			'model' : echelon,
			'menu' : 5,
			"modules" : modules,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/echelon/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER CATEGORIE DESIGNATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

def get_lister_EchelonDesignation(request):
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_fonction.toListFonction()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_EchelonDesignation.toListEchelon(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		# #print('rrrrrrrrrrrrrrrrrrrrrrrr')
		# for m in model:
		# 	#print("Désignation : {} ,  ID : {} ".format(m.designation, m.id))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des Echelons',
			'model' : model,
			'menu' : 5,
			'view':view,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/echelon/list.html")
		return HttpResponse(template.render(context, request))

def get_update_Echelon(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		echelon = dao_EchelonDesignation.toGetEchelon(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : echelon.designation,
			'model' : echelon,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/echelon/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER CATEGORIE DESIGNATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_CategorieDesignation'))

#

def get_creer_StatusDesignation(request):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer statut employé",
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26

		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/statutEmploye/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_StatutDesignation'))

def post_add_StatusDesignationDesignation(request):

	try:

		designation = request.POST["designation"]
		description = request.POST["description"]
		etat = request.POST["etat"]

		StatusDesignation = dao_StatusDesignationEmploye.toCreateStatut(designation, description,etat)
		StatusDesignation = dao_StatusDesignationEmploye.toSaveStatut(StatusDesignation)

		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_StatutDesignation', args=(StatusDesignation.id,)))
	except Exception as e:

		monLog.error("{} :: {}::\nErreur lors de Post Modifier StatusDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_StatutDesignation'))

def post_update_StatusDesignationDesignation(request):
	ref = int(request.POST["ref"])
	try:

		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		etat = request.POST["etat"]

		StatusDesignation = dao_StatusDesignationEmploye.toCreateStatut(designation, description,etat)
		StatusDesignation = dao_StatusDesignationEmploye.toUpdateStatut(ref,StatusDesignation)

		return HttpResponseRedirect(reverse('module_ressources_humaines_detail_StatutDesignation', args=(ref,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier type StatusDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_StatutDesignation'))

def get_details_StatusDesignation(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		StatusDesignation = dao_StatusDesignationEmploye.toGetStatut(ref)
		historique, etapes_suivantes, signee, content_type_id, documents = wkf_task.getDetailObject(utilisateur,StatusDesignation)


		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : StatusDesignation.designation,
			'model' : StatusDesignation,
			"historique": historique,
			"etapes_suivantes": etapes_suivantes,
			"signee": signee,
			"content_type_id": content_type_id,
			"documents": documents,
			"roles": groupe_permissions,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/statutEmploye/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER STATUS DESIGNATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_StatutDesignation'))

def get_lister_StatusDesignationDesignation(request):
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		# model = dao_fonction.toListFonction()
		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_StatusDesignationEmploye.toListStatuts(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		# #print('rrrrrrrrrrrrrrrrrrrrrrrr')
		# for m in model:
		# 	#print("Désignation : {} ,  ID : {} ".format(m.designation, m.id))
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Liste des statuts employés',
			'model' : model,
			'menu' : 5,
			'view':view,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/statutEmploye/list.html")
		return HttpResponse(template.render(context, request))

def get_update_StatusDesignation(request, ref):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		StatusDesignation = dao_StatusDesignationEmploye.toGetStatut(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : StatusDesignation.designation,
			'model' : StatusDesignation,
			'menu' : 5,
			"modules" : modules,
			'actions':auth.toGetActions(modules,utilisateur),
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'utilisateur' : utilisateur
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/statutEmploye/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER STATUS DESIGNATION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print('Erreur get_details_fonction %s'%(e))

		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressources_humaines_liste_StatutDesignation'))

def get_vue_exploratoire(request):
	try:
		permission_number = 77
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		model = dao_model.toListModel(dao_type_unite_fonctionnelle.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		unite_fonctionnelle = dao_unite_fonctionnelle.toListUniteFonctionnelle()

		data = []
		for departement in unite_fonctionnelle:
			if departement.libelle:
				un_departement = {
					'id': departement.id,
					'parent': departement.unite_fonctionnelle_id if departement.unite_fonctionnelle else '#',
					'departement': departement.libelle,
					'code': departement.code,
					'responsable': departement.responsable.nom_complet if departement.responsable else "Non défini",
					'parent_libelle': departement.unite_fonctionnelle.libelle if departement.unite_fonctionnelle else 'Aucun',
					'label': departement.get_label
				}
				data.append(un_departement)


		print(modules, module)


		context = {
			'title' : "Organisations: Vue exploratoire",
			'data': data,
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'sous_modules':sous_modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26,
			'model':model,


		}
		#template = loader.get_template('ErpProject/ModuleRessourcesHumaines/organigram/organigram.html')
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/departement/tree.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))

def get_organigram_unite_fonctionnel(request):
	try:
		permission_number = 76
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request)
		if response != None:
				return response

		if 'isPopup' in request.GET: isPopup = True
		else: isPopup = False

		model = dao_model.toListModel(dao_type_unite_fonctionnelle.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		uni_fonc=dao_unite_fonctionnelle.toListUniteFonctionnelle()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Organigramme",
			'utilisateur' : utilisateur,
			'isPopup': isPopup,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26,
			'model':model,
			'uni_fonc':uni_fonc

		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/organigram/organigram_parent.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Get Creer type_unite_fonctionnelle\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		messages.error(request,e)
		#print('Erreur lors de Get Creer type organisation')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))

#TYPE DE DIPLOME
def get_lister_type_diplome(request):
	try:
		permission_number = 615
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_type_diplome.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		typediplome = dao_type_diplome.toList()
		# #print('Model', typediplome)
		context ={
			'modules':modules,
			'title' : 'Liste des types des diplomes',
			'model' : model,
			'view' : view,
			'sous_modules': sous_modules,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'typediplome':typediplome
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_diplome/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		messages.error(request,e)
		#print('ERREUR')
		#print(e)
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_typediplome(request):
	permission_number = 614
	modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
	if response != None:
		return response

	context = {
		'modules':modules,'sous_modules':sous_modules,
		'title' : "Créer type diplome",
		'utilisateur' : utilisateur,
		'actions':auth.toGetActions(modules,utilisateur),
		'organisation': dao_organisation.toGetMainOrganisation(),
		'modules' : modules,
		'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
		'menu' : 26
	}
	template = loader.get_template('ErpProject/ModuleRessourcesHumaines/type_diplome/add.html')
	return HttpResponse(template.render(context, request))


def post_creer_typediplome(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		# #print(designation, description)
		Type_Diplome = dao_type_diplome.toCreate(designation, description)
		# #print(Type_Diplome)
		Type_Diplome = dao_type_diplome.toSave(auteur,Type_Diplome)
		# #print(Type_Diplome)

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_type_diplome', args=(Type_Diplome.id,)))
	except Exception as e:
		monLog.error("{} :: {}::\nErreur lors de Post Modifier StatusDesignation\n {}".format(identite.utilisateur(request).nom_complet, module, e))
		#print('Erreur lors de Post Modifier type diplome')
		#print(e)
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_type_diplome'))

def get_details_type_diplome(request, ref):
	try:
		permission_number = 615
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		ref = int(ref)
		# #print('reference', ref)
		typeDiplome = dao_type_diplome.toGetType_diplome(ref)
		# #print(typeDiplome)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : typeDiplome.designation,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'model':typeDiplome,
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/type_diplome/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER FONCTION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_type_diplome'))


def get_modifier_type_diplome(request, ref):
	id = int(ref)
	try:
		permission_number = 616
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		typeDiplome = dao_type_diplome.toGetType_diplome(id)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % typeDiplome.designation,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'model':typeDiplome,

		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/type_diplome/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER TYPE DIPLOME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_type_diplome', args=(id,)))

def post_modifier_type_diplome(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]


		type_diplome = dao_type_diplome.toCreate(designation, description)

		type_diplome = dao_type_diplome.toUpdate(id,type_diplome)

		if type_diplome:
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_type_diplome', args=(id,)))
		else :
			messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement des modifications apportées")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_type_diplome', args=(id,)))

	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER TYPE DIPLOME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		messages.error(request,e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_update_type_diplome', args=(id,)))

# DIPLOME CONTROLLER
def get_lister_diplome(request):
	try:
		permission_number = 618
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_diplome.toList(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		diplome = dao_diplome.toList()
		# #print('Model', diplome)
		context ={
			'modules':modules,
			'title' : 'Liste des diplômes',
			'model' : model,
			'view' : view,
			'sous_modules': sous_modules,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'diplome':diplome
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/diplome/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER EMPLOYES \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur get_lister_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_diplome(request):
	try:
		permission_number = 617
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		type_diplomes = dao_type_diplome.toList()

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer un diplôme",
			'utilisateur' : utilisateur,
			'type_diplomes' : type_diplomes,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 26
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/diplome/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nErreur lors de Post Modifier diplome\n {}".format(auteur.nom_complet, module, e))
		#print("Erreur get_creer_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_diplome'))

def post_creer_diplome(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		institution = request.POST["institution"]
		type_id = int(request.POST["type_id"])
		if type_id == 0 : type_id = None

		# #print(designation, description)
		diplome = dao_diplome.toCreate(designation, description, type_id, institution)
		# #print(diplome)
		diplome = dao_diplome.toSave(auteur,diplome)
		# #print(diplome)

		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_diplome', args=(diplome.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nErreur lors de Post Modifier diplome\n {}".format(auteur.nom_complet, module, e))
		#print("Erreur post_creer_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_add_diplome'))

def get_details_diplome(request, ref):
	try:
		permission_number = 618
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response
		ref = int(ref)
		# #print('reference', ref)
		diplome = dao_diplome.toGet(ref)
		# #print(diplome)
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : diplome.designation,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'model':diplome,
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/diplome/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER FONCTION \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur get_details_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_diplome'))


def get_modifier_diplome(request, ref):
	try:
		permission_number = 619
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		diplome = dao_diplome.toGet(id)
		type_diplomes = dao_type_diplome.toList()
		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % diplome.designation,
			"type_diplomes" : type_diplomes,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'model':diplome,

		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/diplome/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER DIPLOME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur get_modifier_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_list_diplome'))

def post_modifier_diplome(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]
		institution = request.POST["institution"]
		type_id = int(request.POST["type_id"])
		if type_id == 0 : type_id = None

		# #print(designation, description)
		diplome = dao_diplome.toCreate(designation, description, type_id, institution)
		diplome = dao_diplome.toUpdate(id,diplome)

		if diplome:
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès!")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_diplome', args=(id,)))
		else :
			raise Exception("Une erreur est survenue lors de l'enregistrement des modifications apportées")
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER DIPLOME \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur post_modifier_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_diplome', args=(id,)))


#LIEU DE TRAVAIL
def get_lister_lieu_travail(request):
	try:
		permission_number = 621
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		#*******Filtre sur les règles **********#
		model = dao_model.toListModel(dao_lieu_travail.toListLieuTravail(), permission_number, groupe_permissions, identite.utilisateur(request))
		#******* End Regle *******************#
		try:
			view = str(request.GET.get("view","list"))
		except Exception as e:
			view = "list"
		model = pagination.toGet(request, model)
		lieu = dao_lieu_travail.toListLieuTravail()
		# #print('Model', diplome)
		context ={
			'modules':modules,
			'title' : 'Liste des lieux de travail',
			'model' : model,
			'view' : view,
			'sous_modules': sous_modules,
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 10,
			'lieu':lieu
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/lieu_travail/list.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE LISTER LIEU TRAVAIL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur get_lister_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse("module_rh_tableau_de_bord"))

def get_creer_lieu_travail(request):
	try:
		permission_number = 621
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : "Créer un lieu de travail",
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 12
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/lieu_travail/add.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nErreur lors de Post Creer Lieu de travail\n {}".format(auteur.nom_complet, module, e))
		#print("Erreur get_creer_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_lieu_travail'))

def post_creer_lieu_travail(request):
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]


		lieu = dao_lieu_travail.toCreateLieuTravail(designation, description)
		lieu = dao_lieu_travail.toSaveLieuTravail(auteur,lieu)


		messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès !")
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_lieu_travail', args=(lieu.id,)))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nErreur lors de Post Creer Lieu de travail\n {}".format(auteur.nom_complet, module, e))
		print("Erreur post_creer_lieu_travail {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressources_humaines_add_lieu_travail'))

def get_details_lieu_travail(request, ref):
	try:
		permission_number = 621
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response
		ref = int(ref)
		lieu = dao_lieu_travail.toGetLieuTravail(ref)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : lieu.designation,
			"modules" : modules,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'model':lieu,
		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/lieu_travail/item.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE DETAILLER LIEU DE TRAVAIL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur get_details_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_lieu_travail'))


def get_modifier_lieu_travail(request, ref):
	try:
		permission_number = 622
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
				return response

		id = int(ref)
		lieu = dao_lieu_travail.toGetLieuTravail(id)

		context = {
			'modules':modules,'sous_modules':sous_modules,
			'title' : 'Modifier %s' % lieu.designation,
			"module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 5,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'utilisateur' : utilisateur,
			'model':lieu,

		}
		template = loader.get_template("ErpProject/ModuleRessourcesHumaines/lieu_travail/update.html")
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE MODIFIER LIEU DE TRAVAIL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur get_modifier_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors du chargement")
		return HttpResponseRedirect(reverse('module_ressources_humaines_list_lieu_travail'))

def post_modifier_lieu_travail(request):
	id = int(request.POST["ref"])
	try:
		auteur = identite.utilisateur(request)
		designation = request.POST["designation"]
		description = request.POST["description"]

		# #print(designation, description)
		lieu = dao_lieu_travail.toCreateLieuTravail(designation, description)
		lieu = dao_lieu_travail.toUpdateLieuTravail(id,lieu)

		if lieu:
			messages.add_message(request, messages.SUCCESS, "L'operation effectuée avec succès !")
			return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_lieu_travail', args=(id,)))
		else :
			raise Exception("Une erreur est survenue lors de l'enregistrement des modifications apportées")
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER LIEU DE TRAVAIL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur post_modifier_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_ressourceshumaines_detail_lieu_travail', args=(id,)))

##Generate Rapport Employe
def get_generate_rapport_employe(request):
	try:
		permission_number = 621
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		statutrh = Model_StatusRH.objects.all()

		context = {
			'modules':modules,
			'sous_modules':sous_modules,
			'title' : "Génération Rapport des Employés",
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 12,
			'status':statutrh
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/Rapport/create.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nErreur lors de la Create Rapport Employe \n {}".format(auteur.nom_complet, module, e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la creation Rapport Employé")
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))


def post_generate_rapport_employe(request):
	try:
		permission_number = 621
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		auteur = identite.utilisateur(request)
		statut = int(request.POST["groupe_statut"])
		employes = ""

		#verification
		if statut == 0:
			employes =  dao_employe.toListEmployes()
		else:
			employes = dao_employe.toListEmployefromStatutRh(statut)

		context = {
			'modules':modules,
			'sous_modules':sous_modules,
			'title' : "Rapport des Employés",
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 12,
			'model':employes,
			'nombre':len(employes)
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/Rapport/generated.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nERREUR LORS DE POST CREER LIEU DE TRAVAIL \n {}".format(auteur.nom_complet, module, e))
		monLog.debug("Info")
		#print("Erreur post_modifier_diplome {}".format(e))
		messages.add_message(request, messages.ERROR, e)
		return HttpResponseRedirect(reverse('module_rh_get_generate_rapport_employe'))



##Generate Rapport Dependant - Employe
def get_generate_rapport_dependant(request):
	try:
		permission_number = 621
		modules, sous_modules, utilisateur, groupe_permissions, response = auth.toGetAuthentification(permission_number, request, inspect.getframeinfo(inspect.currentframe()).function)
		if response != None:
			return response

		dependants = Model_Dependant.objects.filter(employe__est_actif = True)
		# print(dependants)
		data = []
		employes = dao_employe.toListEmployesActifs()
		for item in employes:
			dependants = Model_Dependant.objects.filter(employe__id = item.id, employe__est_actif = True)
			item = {
				'iteration' : item.id,
				'dependants' : dependants,
				'qte' : len(dependants),
				'employe': item.nom_complet
            }
			data.append(item)

		context = {
			'modules':modules,
			'sous_modules':sous_modules,
			'title' : "Génération Rapport des Dépendants",
			'utilisateur' : utilisateur,
			'actions':auth.toGetActions(modules,utilisateur),
			'organisation': dao_organisation.toGetMainOrganisation(),
			'modules' : modules,
			'module' : ErpModule.MODULE_RESSOURCES_HUMAINES,
			'menu' : 12,
			'models':data
		}
		template = loader.get_template('ErpProject/ModuleRessourcesHumaines/employe/Dependant/generated.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		auteur = identite.utilisateur(request)
		module= "ModuleRessourcesHumaines"
		monLog.error("{} :: {}::\nErreur lors de Generate Rapport DEPENDANT \n {}".format(auteur.nom_complet, module, e))
		messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la creation Rapport Dépendant")
		return HttpResponseRedirect(reverse('module_rh_tableau_de_bord'))


def get_json_poste_of_unite_fonctionnelle(request):
	try:
		data = []
		localisation = ""
		ident = int(request.GET["ref"])
		postes = dao_poste.toListPostesByDepartement(ident)
		print(postes)
		for poste in postes:
			if poste.localisation: localisation = poste.localisation.designation
			item = {
				"id": poste.id,
				"designation": poste.designation,
				"localisation": localisation,
				"description": poste.description,
			}
			data.append(item)
		return JsonResponse(data, safe=False)
	except Exception as e:
		return JsonResponse([], safe=False)



@transaction.atomic
def post_creer_mobilite_employe(request):
	sid = transaction.savepoint()
	employe_id = int(request.POST['employe_id'])
	try:
		poste_id = classification_id = categorie_id = None
		reference = request.POST['reference']
		observation = request.POST['observation']
		type_mobilite = request.POST['type_mobilite']
		date_mobilite = request.POST['date_mobilite']
		date_mobilite = timezone.datetime(int(date_mobilite[6:10]), int(date_mobilite[3:5]), int(date_mobilite[0:2]))
		poste = int(request.POST['poste_id'])
		classification = int(request.POST['classification_id'])
		categorie = int(request.POST['categorie_id'])
		if poste != 0: poste_id = poste
		if classification != 0: classification_id = classification
		if categorie != 0: categorie_id = categorie

		auteur = identite.utilisateur(request)

		mobilite_employe = dao_mobilite_employe.toCreateMobiliteEmploye(reference, employe_id, type_mobilite, date_mobilite, poste_id, categorie_id, classification_id, observation)
		mobilite_employe = dao_mobilite_employe.toSaveMobiliteEmploye(auteur, mobilite_employe)

		return HttpResponseRedirect(reverse('module_rh_detail_carriere_employe', args=(employe_id,)))


	except Exception as e:
		#print('Erreur lors de l\'enregistrement')
		auteur = identite.utilisateur(request)
		messages.add_message(request, messages.ERROR, e)
		monLog.error('{} :: {} :: \nERREUR LORS DU POST CREER REQUETE \n {}'.format(auteur.nom_complet, module,e))
		#print(e)
		transaction.savepoint_rollback(sid)
		return HttpResponseRedirect(reverse('module_rh_detail_carriere_employe', args=(employe_id,)))

