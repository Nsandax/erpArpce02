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

class balanceArray(object):

    @staticmethod
    def toGetInPeriode(date_debut, date_fin, devise):
        #On récupère tous les comptes dans un premier temps
        comptes = dao_compte.toListComptes()
        donnees_balance = []


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
                somme_debit = solde_initial_debit + mouvement_debit
                somme_credit = solde_initial_credit + mouvement_credit
                #Puis par rapport au signe de la différence obtenue, on affecte soit sfd(si +) ou sfc(si -)
                solde = somme_debit - somme_credit
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
        return donnees_balance