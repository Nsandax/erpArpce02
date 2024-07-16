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
import base64
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
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleRessourcesHumaines.dao.dao_dependant import dao_dependant
from ModuleRessourcesHumaines.dao.dao_rib import dao_rib
from ErpBackOffice.dao.dao_devise import dao_devise
from ModulePayroll.dao.dao_pret import dao_pret
from ModulePayroll.dao.dao_ligne_paiement_pret import dao_ligne_paiement_pret
from ModuleComptabilite.dao.dao_journal import dao_journal
from ModulePayroll.dao.dao_config_payroll import dao_config_payroll
from ErpBackOffice.utils.print import weasy_print
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
from ModuleRessourcesHumaines.dao.dao_poste import dao_poste
from ModuleRessourcesHumaines.dao.dao_profil import dao_profil
import json
import array
import unidecode

# LANCER LE FICHIER SCRIPT : python manage.py runscript ModuleComptabilite.import

def run():
    print("---Execution script IMPORT RH---")
    # importBalance("Balance_globale_ouverture", 0)
    # importBalance("Balance_Cloture", 0)
    #importRubrique("Fiche_de_paie_2021")
    # showmereealdate("Fiche_de_paie_2021_test_date")
    # savenombrepart("Nbre_Part_Trimeste_1")
    saveOtherRubrique("Elementpaie2021")


#THIS FUNCTION CONVERT ARRAY TO STRING
def convert_list_to_string(org_list, seperator=' '):
	return seperator.join(org_list)


# @transaction.atomic
def saveOtherRubrique(file_name):
        """
        Fonction qui exécute le script Item Bulletin from 4 charge Patronale
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("saveOtherRubrique() ...")
        # sid = transaction.savepoint()
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil2"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = Model_Employe()
                auteur.nom_complet = "SYSTEM"
                auteur.id = None
                compteur = 0
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    inputval = df["INPUT_VALUE_NAME"][i]
                    resultval = df["RESULT_VALUE"][i]
                    matricule = df["EMP_NUMBER"][i]
                    periodeEnd = df["PERIOD_END_DATE"][i]
                    taux = 0.0
                    nombre = 0.0
                    base = 0.0
                    type = ""

                    #On recupere l'employé
                    employe = dao_employe.toGetEmployeByMatricule(matricule)
                    print("GET EMPLOYE", employe)
                    if employe:
                        employe_id = employe.id
                        #On recupere le bulletin de l'employe
                        bulletin = dao_bulletin.toGetOfEmployeFromPeriode(employe_id, periodeEnd)

                        #print("reportname {} ::: inputval {}".format(reportname, inputval))

                        if bulletin != None:
                            # print('BULLETIN FOUND', bulletin)
                            nombrepart = 1
                            #On update le nombre de part et cycle diplome
                            if inputval == 'Nbre_parts':
                                nombrepart = resultval
                                bulletin.nombrepart = nombrepart
                            if inputval == 'Anciennete': anciennete = resultval
                            if inputval == 'Cycle':
                                bulletin.cycle_diplome = resultval
                                if resultval == "SUP": bulletin.dipome = "Cycle supérieur"
                                elif resultval == "SEC2": bulletin.dipome = "Cycle secondaire de 2ème degré"
                                elif resultval == "SEC1": bulletin.dipome = "Cycle secondaire de 1er degré"
                            bulletin.save()

                            #On update la quotité familliale à partir du nombre de parts
                            rubrique_bi80an = dao_rubrique.toGetRubriqueByReference("BASEIMPO80AN")
                            item_bulletin_bi80an = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = rubrique_bi80an.id).first()

                            rubrique = dao_rubrique.toGetRubriqueByReference("QTEFAM")
                            item_bulletin_qte = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = rubrique.id).first()
                            item_bulletin_qte.montant = makeFloat(item_bulletin_bi80an.montant) / makeFloat(bulletin.nombrepart)
                            item_bulletin_qte.save()

                            #On update les 3 cumuls
                            if inputval == 'cumul_brut_taxable':
                                rubrique = dao_rubrique.toGetRubriqueByReference("CUMBRUTAX")
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = rubrique.id).first()
                                item_bulletin.montant = resultval
                                item_bulletin.save()
                            if inputval == 'cumul_cotis_retraite':
                                rubrique = dao_rubrique.toGetRubriqueByReference("CUMCOTRET")
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = rubrique.id).first()
                                item_bulletin.montant = resultval
                                item_bulletin.save()
                            if inputval == 'Cumul_net_taxable':
                                rubrique = dao_rubrique.toGetRubriqueByReference("CUMNETIRPP")
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin_id = bulletin.id, rubrique_id = rubrique.id).first()
                                item_bulletin.montant = resultval
                                item_bulletin.save()

                            #On Check les information pour 4 charge Patronale
                            """if reportname == 'CNSS Allocations famililales' and inputval == 'Pay Value':
                                rubprimeallfam = dao_rubrique.toGetRubriqueByReference("ALLFAM")
                                item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeallfam.designation, rubprimeallfam.id, bulletin.id, nombre, base, taux, resultval, rubprimeallfam.sequence)
                                item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                                print("item_bulletin ALLFAM", item_bulletin)

                            elif reportname == 'CNSS Acc. trav. Mal. Prof.' and inputval == 'Pay Value':
                                print("item_bulletin CNACCTRMALPRO")
                                rubprimemalprof = dao_rubrique.toGetRubriqueByReference("CNACCTRMALPRO")
                                print('RUBRIQUE FIND', rubprimemalprof)
                                item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimemalprof.designation, rubprimemalprof.id, bulletin.id, nombre, base, taux, resultval, rubprimemalprof.sequence)
                                item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                            elif reportname == 'CNSS Part Patronale' and inputval == 'Pay Value':
                                rubprimepatron = dao_rubrique.toGetRubriqueByReference("PARTPATRON")
                                item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimepatron.designation, rubprimepatron.id, bulletin.id, nombre, base, taux, resultval, rubprimepatron.sequence)
                                item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                                print("item_bulletin PARTPATRON", item_bulletin)

                            elif reportname == 'Taxe unique sur les salaires' and inputval == 'Pay Value':
                                rubtaxunsal = dao_rubrique.toGetRubriqueByReference("TAXUNSAL")
                                item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubtaxunsal.designation, rubtaxunsal.id, bulletin.id, nombre, base, taux, resultval, rubtaxunsal.sequence)
                                item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                                print("item_bulletin TAXUNSAL", item_bulletin)"""


                            # print("item_bulletin")
                    else:
                        continue
                    # lot = dao_lot_bulletin.toGetOrCreatelotbyperiode(auteur.id,datepaiement)
                    # print("Lot ID: {}".format(lot.id))
                    # print("Lot Designation: {}".format(lot.designation))
                    # print("Fin Iterration ID {}".format(i))

            # transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---")
            print(e)
            # transaction.savepoint_rollback(sid)

