# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from ErpBackOffice.utils.auth import auth
from django.contrib.auth.models import User, Group
from django.db import transaction
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from rest_framework import viewsets
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max,Sum
from datetime import time, timedelta, datetime
import pandas as pd
import calendar
import base64
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ModuleAchat.dao.dao_categorie import dao_categorie
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
from celery.result import AsyncResult
from ErpBackOffice.models import *
from ModuleAchat.dao.dao_stock_article import dao_stock_article
from ModuleAchat.dao.dao_unite import dao_unite
from ModuleAchat.dao.dao_article import dao_article
from ModuleAchat.dao.dao_emplacement import dao_emplacement
from ModuleBudget.dao.dao_activite import dao_activite
from ErpBackOffice.dao.dao_devise import dao_devise
from django.utils import timezone
import json
import array
import unidecode

from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ErpBackOffice.dao.dao_document import dao_document
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_dependant import dao_dependant
from ModuleRessourcesHumaines.dao.dao_rib import dao_rib
from ErpBackOffice.dao.dao_devise import dao_devise
from ModulePayroll.dao.dao_pret import dao_pret
from ModulePayroll.dao.dao_ligne_paiement_pret import dao_ligne_paiement_pret
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModulePayroll.dao.dao_config_payroll import dao_config_payroll
from ErpBackOffice.utils.print import weasy_print
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
# from celery.result import AsyncResult
from ModuleComptabilite.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.models import *
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleRessourcesHumaines.dao.dao_poste import dao_poste
from ModuleRessourcesHumaines.dao.dao_profil import dao_profil


def run():
    print("---Execution script IMPORT BC---")
    # SaveBonCommande("bon_commande")
    # SaveLineBonCommande("Line_Bon_Comande")
    SaveRegroupement("regroupement")


def SaveBonCommande(file_name):
        """
        Fonction qui exécute le script migration de bon de commande
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("SaveBonCommande() ...")
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil1"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    po_header_id = df["PO_HEADER_ID"][i]
                    segment1 = df["SEGMENT1"][i]
                    start_date     = df["CREATION_DATE"][i]
                    comment     = df["COMMENTS"][i]
                    statut_close     = df["CLOSED_CODE"][i]
                    last_update  = df["LAST_UPDATE_DATE"][i]

                    devise = dao_devise.toGetDeviseByCodeIso("XAF")
                    bon = Model_Bon_reception()
                    bon.numero_reception = dao_bon_reception.toGenerateNumeroReception()
                    bon.date_prevue = start_date
                    bon.date_reception = start_date
                    bon.montant_total = 0
                    bon.devise_id = devise.id
                    bon.ligne_budgetaire_id = None
                    bon.codes_budgetaires_id = None
                    bon.est_realisee = True
                    bon.url = ""
                    bon.reference_document = ""
                    bon.description = comment
                    bon.document_id = None
                    bon.fournisseur_id = None
                    bon.demande_achat_id = None
                    bon.condition_reglement_id = None
                    bon.statut_id = None
                    bon.etat = statut_close
                    bon.receveur_id = None
                    bon.auteur_id = None
                    bon.update_date = last_update
                    bon.creation_date = start_date
                    bon.is_actif = False
                    bon.duree=1
                    bon.url=""
                    bon.po_header_id = po_header_id
                    bon.segment1 = segment1
                    bon.save()

        except Exception as e:
            print("--- ERREUR SAVE BON DE COMMANDE ---") 
            print(e)

def SaveLineBonCommande(file_name):
        """
        Fonction qui exécute le script migration de bon de commande
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("SaveBonCommande() ...")
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil1"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    line_header_id = df["PO_LINE_ID"][i]
                    po_header_id = df["PO_HEADER_ID"][i]
                    list_price_per = df["LIST_PRICE_PER_UNIT"][i]
                    price       = df["UNIT_PRICE"][i]
                    start_date  = df["CREATION_DATE"][i]
                    comment     = df["ITEM_DESCRIPTION"][i]
                    qt          = df["QUANTITY"][i]
                    last_update = df["LAST_UPDATE_DATE"][i]

                    bon_reception = Model_Bon_reception.objects.filter(po_header_id = "po_header_id").first()
                    print('BON RECEPTION', bon_reception)
                    
                    # devise = dao_devise.toGetDeviseByCodeIso("XAF").

                    bon = Model_Ligne_reception()
                    bon.bon_reception = bon_reception.id
                    bon.quantite_demande = qt
                    bon.quantite_fournie = qt
                    bon.ligne_budgetaire_id = None
                    bon.stock_article_id = None
                    bon.prix_unitaire = float(price)
                    bon.description = comment
                    bon.prix_lot = float(list_price_per)
                    bon.unite_achat = float(price)
                    bon.article_id = None
                    bon.description = comment
                    bon.statut_id = None
                    bon.etat = ""
                    bon.update_date = last_update
                    bon.creation_date = start_date                    
                    bon.url=""
                    bon.polineID = line_header_id
                    bon.auteur_id = None
                    bon.save()

        except Exception as e:
            print("--- ERREUR SAVE BON DE COMMANDE ---") 
            print(e)


    '''    """
        Fonction qui exécute le script migration de bon de commande
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("SaveRegroupement() ...")
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil1"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    code = df["code"][i]
                    detail = df["detail"][i]
                    budget = df["budget"][i]
                    detail_compte = df["detail_compte"][i]
                    compte = df["compte"][i]

                    regourpement = Model_regorupement_budgetaire()

                    regourpement.code = code
                    regourpement.detail = detail
                    regourpement.compte = compte
                    regourpement.detail_compte = detail_compte
                    regourpement.budget = budget
                    regourpement.save()

        except Exception as e:
            print("--- ERREUR SAVE BON DE COMMANDE ---") 
            print(e)'''