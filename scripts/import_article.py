# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from ErpBackOffice.utils.auth import auth
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
    print("---Execution script IMPORT ARTICLES---")
    # saveNature("activite")
    # saveSite("activite")
    # saveCentreCout("activite")
    # saveProjet("activite")
    # saveClient("activite")
    # saveUpdateEmploye("employe_up")
    saveFss("fournisseur")

def saveFss(file_name):
        """
        Fonction qui exécute le script migration type Client
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("saveFss() ...")
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
                    # code = str(df["code"][i])
                    designation = df["VENDOR_NAME"][i]
                    desc = df["NUM_1099"][i]
                    start_date     = df["START_DATE_ACTIVE"][i]


                    #SAVE FOURNISSEUR
                    fournisseur = Model_Fournisseur()
                    fournisseur.nom_complet = designation
                    fournisseur.denomination = designation
                    fournisseur.domaine = desc
                    fournisseur.date_fondation = start_date
                    fournisseur.save()
                    
            # transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE TYPE CLIENT ---") 
            print(e)
            # transaction.savepoint_rollback(sid) 

def saveClient(file_name):
        """
        Fonction qui exécute le script migration type Client
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("saveClient() ...")
        # sid = transaction.savepoint()
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil6"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    # code = str(df["code"][i])
                    designation = df["designation"][i]
                    type_client = df["type_client"][i]
                    prefixe     = df["prefixe"][i]
                    prenom      = df["prenom"][i]
                    postnom     = df["postnom"][i]
                    nom         = df["nom"][i]
                    connu_as    = df["KNOWN_AS"][i]
                    country     = df["COUNTRY"][i]
                    adress1     = df["ADDRESS1"][i]
                    city        = df["CITY"][i]
                    postal_code = str(df["POSTAL_CODE"][i])
                    email       = df["EMAIL_ADDRESS"][i]
                    name_phonetic = df["NAME_PHONETIC"][i]
                    phonecode   = df["PHONE_CODE"][i]
                    phone       = df["PHONE_NUMBER"][i]
                    status      = df["STATUS"][i]

                    numero_compte_b = ""
                    nui = ""
                    personne_contact = ""
                    bp = postal_code
                    raison_sociale = ""
                    fax = ""
                    fiscale = ""
                    autre_info = ""
                    typeclient = ""
                    mode_reglement = ""
                    langue = ""
                    lieu_de_naissance = ""
                    date_de_naissance= "2050-5-25"
                    prenom = prenom
                    nom = ""
                    nom_complet = designation
                    email = email
                    phone = phone
                    adresse = ""
                    commune_quartier = ""
                    est_actif = False
                    est_particulier = False
                    sexe= ""

                    #GENRER LE TYPE CLIENT
                    typeclient = Model_TypeClient.objects.filter(designation = type_client).first()
                    if status == "A":est_actif = True
                    if  typeclient.designation == "PERSON": est_particulier = True

                    #RECUPERE CLIENT
                    client = Model_Client()
                    client.prenom = prenom
                    client.nom = nom
                    client.nom_complet = nom_complet
                    client.sexe = sexe
                    client.numero_compte_b = numero_compte_b
                    client.personne_contact = personne_contact
                    client.bp = bp
                    client.raison_sociale = raison_sociale
                    client.fiscale = fiscale
                    client.autre_info = connu_as
                    client.typeclient_id = typeclient.id
                    client.mode_reglement_id = None
                    client.langue = ""
                    client.lieu_de_naissance = lieu_de_naissance
                    client.date_de_naissance = date_de_naissance
                    client.email = email
                    client.phone = phone
                    client.est_actif = est_actif
                    client.est_particulier = est_particulier
                    client.adresse = adress1
                    client.save()
                    
            # transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE TYPE CLIENT ---") 
            print(e)
            # transaction.savepoint_rollback(sid)  

def savearticle(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("savearticle() ...")
        sid = transaction.savepoint()
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
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    code = str(df["code"][i])
                    designation = df["designation"][i]
                    categorie = str(df["categorie"][i])
                    unite = str(df["unite"][i])

                    est_commercialisable = False
                    est_achetable = True
                    est_manufacturable = False
                    est_fabriquable = False
                    est_amortissable = False

                    designation_court = ""
                    code_article = code
                    code_barre = ""
                    type_article = 3 #Article Stockable
                    categorie_id = None
                    prix_unitaire = 0.0
                    service_ref_id = 6 #Moyen Generaux
                    unite_id = None
                    image = ""
                    auteur = None

                    #RECUPERER LA CATEGORIE ARTICLE
                    categorie = dao_categorie_article.toGetCagorieArticlebyname(categorie)
                    if categorie: categorie_id = categorie.id

                    #RECUPERER L'UNITE MESURE
                    unitemesure = dao_unite.toGetUniteName(unite)
                    if unitemesure: unite_id = unitemesure.id

                    article = dao_article.toCreateArticle(image, designation, unite_id, est_commercialisable, est_achetable, est_manufacturable, est_fabriquable,
                     designation_court, code_article, code_barre, type_article, categorie_id, prix_unitaire, None, est_amortissable,service_ref_id)
                    article = dao_article.toSaveArticle(auteur, article)

                    if article != None :
                        if type_article != "2":
                            emplacement_smg = dao_emplacement.toGetEmplacementBySI()
                            stock_article = dao_stock_article.toCreateStockArticle(article.id,0,emplacement_smg.id)
                            stock_article = dao_stock_article.toSaveStockArticle(stock_article)
            transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            transaction.savepoint_rollback(sid)           

def saveNature(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("savearticle() ...")
        sid = transaction.savepoint()
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
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    code = str(df["code"][i])
                    designation = df["designation"][i]

                    #RECUPERE ACTIVITE
                    activite = Model_Nature()
                    activite.code = code
                    activite.designation = designation
                    activite.created_at = timezone.now()
                    activite.updated_at = timezone.now()
                    activite.auteur_id = auteur
                    activite.save()
                    
            transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            transaction.savepoint_rollback(sid)

def saveSite(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("savearticle() ...")
        sid = transaction.savepoint()
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil3"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    code = str(df["code"][i])
                    designation = df["designation"][i]

                    #RECUPERE ACTIVITE
                    activite = Model_LieuTravail()
                    activite.code = code
                    activite.designation = designation
                    activite.created_at = timezone.now()
                    activite.updated_at = timezone.now()
                    activite.auteur_id = auteur
                    activite.save()
                    
            transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            transaction.savepoint_rollback(sid)

def saveCentreCout(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("saveCentreCout() ...")
        sid = transaction.savepoint()
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil4"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    code = str(df["code"][i])
                    designation = df["designation"][i]

                    #RECUPERE ACTIVITE
                    centre = Model_Centre_cout()
                    centre.designation = designation
                    centre.abbreviation = code
                    centre.centre_cout = None
                    centre.groupe_analytique = None
                    centre.date_debut = timezone.now()
                    centre.date_fin = timezone.now()
                    centre.created_at = timezone.now()
                    centre.updated_at = timezone.now()
                    centre.auteur_id = auteur
                    centre.save()
                    
            transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            transaction.savepoint_rollback(sid)        

def saveProjet(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("saveCentreCout() ...")
        sid = transaction.savepoint()
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xlsx")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil5"
                print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                auteur = None
                print('---DEBUT Iteration')

                for i in df.index:
                    print('---Iteration', i)
                    code = str(df["code"][i])
                    designation = df["designation"][i]

                    devise = dao_devise.toGetDeviseByCodeIso("XAF")

                    #RECUPERE PROJET
                    projet = Model_Projet()
                    projet.designation = designation
                    projet.codeprojet = code
                    projet.categoriebudget = None
                    projet.montant = 0.0
                    projet.date_debut = timezone.now()
                    projet.devise_id = devise.id
                    projet.solde = 0.0
                    projet.date_fin = timezone.now()
                    projet.created_at = timezone.now()
                    projet.updated_at = timezone.now()
                    projet.auteur_id = auteur
                    projet.save()
                    
            transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            transaction.savepoint_rollback(sid)     

def saveUpdateEmploye(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("savearticle() ...")
        # sid = transaction.savepoint()
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
                    person_id = df["PERSON_ID"][i]
                    lastname = df["LAST_NAME"][i]
                    firstname = df["FIRST_NAME"][i]
                    nom_complet = df["FULL_NAME"][i]
                    birthday = df["DATE_OF_BIRTH"][i]
                    ville_naissance = df["TOWN_OF_BIRTH"][i]
                    region_naissance = df["REGION_OF_BIRTH"][i]
                    pays_naissance = df["COUNTRY_OF_BIRTH"][i]
                    sex = df["SEX"][i]
                    title = df["TITLE"][i]
                    status_marital = df["MARITAL_STATUS"][i]
                    nationalite = df["NATIONALITE"][i]
                    matricule = df["EMPLOYEE_NUMBER"][i]
                    date_engagement = df["START_DATE"][i]

                    employe = dao_employe.toGetEmployeByMatricule(matricule)
                    etat_civil = ""
                    if status_marital == 'M': etat_civil = "Marié(e)"
                    elif status_marital == 'C': etat_civil = 'Célibataire'
                    elif status_marital == 'D': etat_civil = 'Divorcé(e)'
                    elif status_marital == 'V': etat_civil = 'Veuf(ve)'
                    elif status_marital == 'UL': etat_civil = 'Union Libre'

                    # categorie_employe = employe.categorie_employe.categorie.designation

                    if employe:
                        print('---Iteration', i)
                        employe.person_id = person_id
                        employe.save()
                    
                        profil_id = employe.profilrh.id

                        profil = dao_profil.toGetProfil(profil_id)
                        profil.date_naissance = birthday
                        profil.lieu_naissance = ville_naissance
                        profil.nationalite = nationalite
                        profil.etat_civil = etat_civil
                        profil.date_engagement = date_engagement
                        profil.Statutrh_id = 1
                        profil.save()
                    else:
                        continue

                    #RECUPERE ACTIVITE                    
            # transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            # transaction.savepoint_rollback(sid)

@transaction.atomic
def saveAsset(file_name):
        """
        Fonction qui exécute le script migration articles
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        print("savearticle() ...")
        sid = transaction.savepoint()
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
                    numeroserie = df["TAG_NUMBER"][i]
                    asset_number = df["ASSET_NUMBER"][i]
                    attribute_cat = df["ATTRIBUTE_CATEGORY_CODE"][i]
                    serialnum = df["SERIAL_NUMBER"][i]
                    asset_type = df["ASSET_TYPE"][i]
                    created_at = df["CREATION_DATE"][i]

                    emplacement_smg = dao_emplacement.toGetEmplacementBySMG()
                    if numeroserie == None: numeroserie = 'asset{}'.format(i) 

                    numero_identification = numeroserie
                    type = ""
                    local = None
                    article = None
                    description = ""
                    employe = None
                    bon_entree = None
                    bon_reception = None
                    emplacement = emplacement_smg.id
                    created_at = created_at

                    asset = Model_Asset()
                    asset.numero_identification = numero_identification
                    asset.type = type
                    asset.local_id = local
                    asset.article_id = article
                    asset.description = description
                    asset.employe_id = employe
                    asset.bon_entree_id = bon_entree
                    asset.bon_reception_id = bon_reception
                    asset.emplacement_id = emplacement
                    asset.created_at = created_at

                    asset.asset_number = asset_number
                    asset.attribute_categorie_code = attribute_cat
                    asset.serial_number = serialnum
                    asset.asset_type = asset_type
                    asset.save()
                    #RECUPERE ACTIVITE                    
            transaction.savepoint_commit(sid)
        except Exception as e:
            print("--- ERREUR SAVE OTHER RUBRIQUE ---") 
            print(e)
            transaction.savepoint_rollback(sid)


