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

class compteResultatArray(object):

	@staticmethod
	def toGetOfBalance(donnees_balance):
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
		return donnees_compte_resultat