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
    # SaveRegroupement("regroupement")
    SaveFacture("facture")


def SaveFacture(file_name):
        """
            Fonction qui exécute le script migration de bon de commande
            :param file_name: (string) une chaine de caractère,le nom du fichier à importer
            :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("SaveFacture() ...")
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
                    Numero = df["Numero"][i]
                    DateFacture = df["DateFacture"][i]
                    Description = df["Description"][i]
                    Fournisseur = df["Fournisseur"][i]
                    Montant     = df[" Montant"][i]
                    Montant_paye = df["Montant_paye"][i]

                    devise = dao_devise.toGetDeviseByCodeIso("XAF")
                    
                    
                    facturefsr = Model_Facture()
                    facturefsr.facture_mere_id = None
                    facturefsr.fournisseur_id = None
                    facturefsr.client_id = None
                    facturefsr.bon_commande_id = None
                    facturefsr.bon_reception_id = None
                    facturefsr.devise_id = devise.id
                    facturefsr.periode = DateFacture
                    facturefsr.numero_facture = Numero
                    facturefsr.montant = Montant
                    facturefsr.montant_en_lettre = ""
                    facturefsr.montant_ht = Montant
                    facturefsr.montant_taxe = 0.0
                    facturefsr.document = ""
                    facturefsr.type_facture_id = None
                    facturefsr.est_soldee = True
                    facturefsr.condition_reglement_id = None
                    facturefsr.lettrage_id = None
                    facturefsr.est_facture_avoir = False
                    facturefsr.est_nullable = False
                    facturefsr.type_service_id = False
                    facturefsr.objet_facture = None
                    facturefsr.type  = "FOURNISSEUR"
                    facturefsr.type_facture_client = ""
                    facturefsr.etat_facturation_id = None
                    facturefsr.date_facturation = DateFacture
                    facturefsr.date_echeance  = DateFacture
                    facturefsr.statut_id = None
                    facturefsr.etat_id = None
                    facturefsr.journal_comptable_id= None
                    facturefsr.auteur_id= None
                    facturefsr.save()

                    linefacture = Model_Ligne_facture()
                    linefacture.id = facturefsr.id
                    linefacture.quantite_demande = 1
                    linefacture.prix_unitaire = Montant
                    linefacture.remise = 0.0
                    linefacture.prix_lot= Montant
                    linefacture.ligne_montant_taxe= 0.0
                    linefacture.unite_achat_id= None
                    linefacture.designation = Description
                    linefacture.article_id= None
                    linefacture.compte_comptable_id= None
                    linefacture.statut_id=None
                    linefacture.etat_id=None
                    linefacture.save()

        except Exception as e:
            print("--- ERREUR SAVE FACTURE ---") 
            print(e)
