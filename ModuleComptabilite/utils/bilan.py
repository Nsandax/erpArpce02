from __future__ import unicode_literals
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from random import randint
from django.core.mail import send_mail
import datetime
import json

# Import from ModuleComptabilite
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModuleComptabilite.dao.dao_compte import dao_compte
from ModuleComptabilite.dao.dao_portee_taxe import dao_portee_taxe
from ModuleComptabilite.dao.dao_type_compte import dao_type_compte
from ModuleComptabilite.dao.dao_type_journal import dao_type_journal
from ModuleComptabilite.dao.dao_type_of_typecompte import dao_type_of_typecompte
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleComptabilite.dao.dao_ecriture_comptable import dao_ecriture_comptable
from ModuleComptabilite.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleComptabilite.dao.dao_taux_change import dao_taux_change
from ModuleComptabilite.dao.dao_annee_fiscale import dao_annee_fiscale
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId

class bilanArray(object):
	@staticmethod
	def toGetOfBalance(donnees_balance, donnees_compte_resultat):
		donnees_bilan_passif = []
		donnees_bilan_actif = []


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
			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:4] in ("2811", "2911", "2918", "2919"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde
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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:4] in ("2812", "2813", "2814", "2912", "2913", "2914", "2919"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:4] in ("2815", "2816", "2915", "2916"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:4] in ("2817", "2818", "2917", "2918"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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
				item_bilan["balance_n1"] = total_immo_incorporelle
    
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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] in ("282", "292"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:4] in ("2831", "2832", "2833", "2837", "2931", "2932", "2933", "2937", "2939"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "283" and item_balance["numero_compte"][0:4] not in ("2831", "2832", "2833", "2837") or item_balance["numero_compte"][0:4] == "2939" :
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] in ("284", "294") and item_balance["numero_compte"][0:4] not in ("2845", "2945", "2949"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:4] in ("2845", "2945", "2949"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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
				item_bilan["balance_n1"] = total_immo_corporelle	

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "295":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "296":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "297":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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
				item_bilan["balance_n1"] = total_immo_financiere	

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "498":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:2] == "39":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "490":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "491":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] in ("492", "493", "495", "496", "497"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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
				item_bilan["amort"] = creances_emplois_amort
				item_bilan["balance_n"] = creances_emplois
				item_bilan["balance_n1"] = creances_emplois
  
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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "590":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] == "591":
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			#Pour l' amortissement et dépreciation
			elif item_balance["numero_compte"][0:3] in ("592", "592", "594"):
				solde = float(item_balance["credit_solde"])
				amort = amort + solde

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

			elif item_balance["numero_compte"][0:3] == "129" :
				solde = float(item_balance["debit_solde"])
				debit = debit + solde

		balance = float(credit) - float(debit)
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

		item = {
			"reference" : "DH",
			"libelle" : "Dettes circulantes HAO",
			"note" : "5",
			"est_total" : False,
			"balance_n" : "%.2f" % balance,
			"balance_n1" : "%.2f" % balance
		}
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

		return donnees_bilan_actif, donnees_bilan_passif