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
    importRubrique("data2021")
    # showmereealdate("Fiche_de_paie_2021_test_date")
    # savenombrepart("Nbre_Part_Trimeste_1")
    # saveOtherRubrique("test_nbre_part")


#THIS FUNCTION CONVERT ARRAY TO STRING
def convert_list_to_string(org_list, seperator=' '):
	return seperator.join(org_list)


# @transaction.atomic
def importRubrique(file_name, est_regulier = True):
        """
        Fonction qui exécute le script qui import les rubriques de paiement des employes
        :param file_name: (string) une chaine de caractère,le nom du fichier à importer
        :return : (void)  renvoie rien juste affiche le deroulement
        """
        # print("importRubrique() ...")
        # sid = transaction.savepoint()
        try:
            import_dir = settings.MEDIA_ROOT
            file_dir = 'excel/'
            import_dir = import_dir + '/' + file_dir
            file_path = os.path.join(import_dir, str(file_name) + ".xls")
            if default_storage.exists(file_path):
                filename = default_storage.generate_filename(file_path)
                sheet = "Feuil2"
                # print("Sheet : {} file: {}".format(sheet, filename))
                df = pd.read_excel(io=filename, sheet_name=sheet)
                # transaction.savepoint_commit(sid)

                auteur = Model_Employe()
                auteur.nom_complet = "SYSTEM"
                auteur.id = None
                compteur = 0
                ListEmployeMiss = []

                for i in df.index:
                    print('---Iteration', i)
                    matricule = df["matricule"][i]
                    # On recupere l'employe par son numero matricule
                    employe = dao_employe.toGetEmployeByMatricule(matricule)
                    print("Employé ID {}".format(employe))
                    if employe:
                        employe_id = employe.id
                    else:
                        print('--- La Création des Employés')
                        est_particulier = True
                        nom_complet = str(df['nom_complet'][i])
                        nom_complet = nom_complet.strip()
                        nom_complet_array = nom_complet.split(",")
                        nom = nom_complet_array[0].strip()
                        prenom = nom_complet_array[1].strip()
                        sexe = str(df['genre'][i])
                        first_name = prenom.split(' ')[0].lower()
                        last_name = nom.split(' ')[0].lower()
                        email = f"{first_name}.{last_name}22@arpce.cg"
                        phone = ''
                        arrondissement = ""
                        adresse = ""
                        categorie = ""
                        classification = ""
                        lieu_travail = ''
                        date_engagement = ''
                        contrat = ''
                        date_naissance = ''
                        education = ''
                        diplome = ''
                        numero_ss = ''
                        code_unite_fonctionnelle = str(df['dept'][i])
                        situation_famille = ''
                        poste_designation = ''
                        designation_banque = ''
                        code_banque = ''
                        code_guichet = ''
                        numero_compte = ''
                        cle_rib = ''
                        image = ""
                        poste_designation = str(df['fonction'][i])

                        #Fixation valeur modele bulletin deja exista
                        bulletin_modele_default = dao_bulletin_modele.toGetBulletinModeleParDefaut()
                        modele_bulletin_id = bulletin_modele_default.id if bulletin_modele_default else None

                        lieu_naissance = ""
                        echelon = "" #str(df['echelon'][i])
                        responsable_id = None
                        nombre_subordonne = ""

                        #TRAITEMENT NON & PRENOM POUR IMPORT EMPLOYE
                        # print("Employé  {} {}".format(nom, prenom))
                        # print("---SHOW EMAIL {}".format(email))


                        #TRAITEMENT GENDER
                        gender = str(df['genre'][i])
                        # sexe.upper() #RENDRE UNIFORME LE SEXE
                        # if sexe == 'F': gender = 'Feminin'
                        # elif sexe == 'M': gender = 'Masculin'

                        etat_civil = ""
                        unite_fonctionnelle_id = None
                        '''unite_fonctionnelle = dao_unite_fonctionnelle.toGetOrCreateUniteFonctionnelle(auteur, code_unite_fonctionnelle)
                        if unite_fonctionnelle != None : unite_fonctionnelle_id = unite_fonctionnelle.id
                        print("UNITE FONCTIONNELLE {}".format(unite_fonctionnelle))

                        classification_pro_id = None
                        poste_id = None
                        poste = dao_poste.toGetOrCreatePoste(auteur,poste_designation, classification_pro_id, nombre_subordonne, unite_fonctionnelle_id)
                        if poste != None : poste_id = poste.id
                        print("poste {}".format(poste))'''

                        categorie_id = None
                        lieutravail_id = None
                        diplome_id = None
                        est_particulier = True
                        user_id = None
                        user = None
                        # print("UNITE FONCTIONNELLE {}".format(unite_fonctionnelle))

                        # employe = dao_employe.toCreateEmploye(prenom, nom, nom_complet, "", email, phone, adresse, None, True, None, est_particulier, None, unite_fonctionnelle_id,lieutravail_id, categorie_id,poste_id,None, diplome_id, modele_bulletin_id, None, None)
                        employe = Model_Employe()
                        # employe = dao_employe.toSaveEmploye(auteur, employe)
                        employe.prenom = prenom
                        employe.nom = nom
                        employe.nom_complet = unidecode.unidecode(nom_complet)
                        employe.email = email
                        employe.modele_bulletin_id = modele_bulletin_id

                        '''
                        employe.image = ""
                        employe.phone = phone
                        employe.adresse = adresse
                        employe.commune_quartier_id = None
                        employe.est_actif = True
                        employe.compte_id = None
                        employe.est_particulier = True
                        employe.profilrh_id = None
                        print("Avant la création Unite Fonctionnelle")
                        employe.unite_fonctionnelle_id = unite_fonctionnelle_id

                        employe.lieu_travail_id = lieutravail_id
                        employe.categorie_employe_id = categorie_id
                        employe.poste_id = poste_id
                        employe.classification_pro_id = classification_pro_id
                        employe.poste_id = poste_id
                        # employe.type_structure_id = type_structure_id
                        employe.diplome_id = diplome_id

                        print("Avant la création du profil dans Employe")
                        employe.statutrh_id = None
                        employe.auteur_id = None
                        employe.document_id = None'''

                        # print("Avant save USER")
                        testuser = User.objects.filter(username = email).first()
                        # print('SHOW ME USER ID {}'.format(testuser))
                        if testuser == None:
                            # print('---TESTUSER IS NONE')
                            user = User.objects.create_user(
                                username = email,
                                password = "Nsandax2016",
                                email = email
                            )
                            user_id = user.id
                        else:
                            # print('---TESTUSER IS NOT NONE')
                            user_id = testuser.id
                        # print('----USER CREER:', user_id)
                        employe.user_id = user_id
                        employe.save()
                        print("L'employe Cree {}".format(employe.id))

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

                        # profil_agent = dao_profil.toCreateProfil(date_engagement, prisecharge, date_naissance, lieu_naissance,  nationalite, numero_passeport,
													# numero_identification,etat_civil,numero_ss,gender, matricule,  email, phone_professionnel,phone,phone_pro2,contrat,est_permanent)

                        profil = Model_ProfilRH()
                        '''profil.date_engagement = date_engagement
                        profil.debut_service = prisecharge
                        profil.date_naissance = date_naissance'''
                        profil.lieu_naissance = lieu_naissance
                        profil.nationalite = nationalite
                        profil.numero_passeport = numero_passeport
                        profil.numero_identification = numero_identification
                        profil.etat_civil = etat_civil
                        profil.est_permanent = True
                        profil.numero_ss = numero_ss
                        profil.genre = gender
                        profil.matricule = matricule
                        profil.email_professionnel = email
                        profil.phone_professionnel = phone_professionnel
                        profil.phone_personnel = phone
                        profil.phone_professionnel2 = phone_pro2
                        profil.contrat = contrat
                        profil.est_permanent=est_permanent
                        profil.auteur_id = auteur.id

                        profil.save()
                        # print("Le Profile Crée ID {}".format(profil.id))

                        employe.profilrh_id = profil.id
                        employe.save()

                        #On conserve l'employé Crée
                        if not (matricule in ListEmployeMiss):
                            ListEmployeMiss.append(matricule)

                    if employe:
                        employe_id = employe.id
                        # On fixe la devise
                        devise = dao_devise.toGetDeviseByCodeIso("XAF")
                        datepaiement = df["end_date"][i]
                        periode = datepaiement
                        if int(periode.month) == 12 and df["SALBASE"][i] == 0: est_regulier = False

                        lot = dao_lot_bulletin.toGetOrCreatelotbyperiode(auteur.id,periode,est_regulier)
                        lot_id = lot.id
                        designation = "Bulletin de Paie de {0}".format(employe.nom_complet)
                        # print(designation)
                        reference = df["PERSON_ID"][i]
                        type = ""
                        listRubrique = []
                        nombre = 0.0
                        base = 0.0
                        taux = 0.0

                        fonc = str(df["fonction"][i])
                        grade = str(df["grade"][i])
                        dept = str(df["dept"][i])
                        fonc = str(df["fonction"][i])

                        #On Cree le Bulletin
                        bulletin = dao_bulletin.toCreate(auteur.id, designation, employe_id, lot_id, reference, periode, type)
                        bulletin = dao_bulletin.toSave(bulletin)
                        bulletin.fonction = fonc
                        bulletin.grade = grade
                        bulletin.departemant = dept
                        bulletin.diplome = ''
                        bulletin.save()
                        # print("Bulletin cree ID {}".format(bulletin.id))

                        #On traite maintenant la rubrique
                        salbase = df["SALBASE"][i]
                        sursal = df["SURSAL"][i]
                        primeanc = df["PRIMANC"][i]
                        primefonc = df["PRIFONCT"][i]
                        primelog = df["PRILOG"][i]
                        primediplom = df["PRIDIPLOM"][i]
                        primedom = df["PRIDOM"][i]
                        primeloign = df["PRIELOIGN"][i]
                        primecaisse = df["PRICAISSE"][i]
                        primerisque = df["PRIRISQUE"][i]
                        allconge = df["ALLOCONGE"][i]
                        primeastr = df["PRIASTR"][i]
                        primepaie = df["PRIPAIE"][i]
                        salbrut = df["SALBRUT"][i]
                        cnss = df["CNSS"][i]
                        irpp = df["IRPP"][i]
                        indtrans = df["INDTRANSP"][i]
                        cmptrans = df["CMPLTRANSP"][i]
                        pret = df["PRET"][i]
                        primerep = df["PRIREPR"][i]
                        cotmutuel = df["COTARPCE"][i]
                        netpay = df["NETPAYER"][i]
                        # print('-***Recuperation des Chanmps sur Excel')

                        #Salaire de base (Valeur recuperee sur fichier Excel)
                        rubsalbase = dao_rubrique.toGetRubriqueByReference("SALBASE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubsalbase.designation, rubsalbase.id, bulletin.id, nombre, base, taux, salbase, rubsalbase.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimeanc = dao_rubrique.toGetRubriqueByReference("PRIMANC")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeanc.designation, rubprimeanc.id, bulletin.id, nombre, base, taux, primeanc, rubprimeanc.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimefonc = dao_rubrique.toGetRubriqueByReference("PRIFONCT")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimefonc.designation, rubprimefonc.id, bulletin.id, nombre, base, taux, primefonc, rubprimefonc.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimelog = dao_rubrique.toGetRubriqueByReference("PRILOG")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimelog.designation, rubprimelog.id, bulletin.id, nombre, base, taux, primelog, rubprimelog.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimediplom = dao_rubrique.toGetRubriqueByReference("PRIDIPLOM")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimediplom.designation, rubprimediplom.id, bulletin.id, nombre, base, taux, primediplom, rubprimediplom.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimedom = dao_rubrique.toGetRubriqueByReference("PRIDOM")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimedom.designation, rubprimedom.id, bulletin.id, nombre, base, taux, primedom, rubprimedom.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimeloign = dao_rubrique.toGetRubriqueByReference("PRIELOIGN")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeloign.designation, rubprimeloign.id, bulletin.id, nombre, base, taux, primeloign, rubprimeloign.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimecaisse = dao_rubrique.toGetRubriqueByReference("PRICAISSE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimecaisse.designation, rubprimecaisse.id, bulletin.id, nombre, base, taux,primecaisse, rubprimecaisse.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubrisque = dao_rubrique.toGetRubriqueByReference("PRIRISQUE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubrisque.designation, rubrisque.id, bulletin.id, nombre, base, taux, primerisque, rubrisque.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimeastr = dao_rubrique.toGetRubriqueByReference("PRIASTR")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeastr.designation, rubprimeastr.id, bulletin.id, nombre, base, taux, primeastr, rubprimeastr.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimepaie = dao_rubrique.toGetRubriqueByReference("PRIPAIE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimepaie.designation, rubprimepaie.id, bulletin.id, nombre, base, taux, primepaie, rubprimepaie.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubprimerep = dao_rubrique.toGetRubriqueByReference("PRIREPR")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimerep.designation, rubprimerep.id, bulletin.id, nombre, base, taux, primerep, rubprimerep.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        rubsursal = dao_rubrique.toGetRubriqueByReference("SURSAL")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubsursal.designation, rubsursal.id, bulletin.id, nombre, base, taux, sursal, rubsursal.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #PRIME IMPOSABLE (Valeur recuperee sur fichier Excel)
                        ruballconge = dao_rubrique.toGetRubriqueByReference("ALLOCONGE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, ruballconge.designation, ruballconge.id, bulletin.id, nombre, base, taux, allconge, ruballconge.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Salaire brut taxable (Valeur recuperee sur fichier Excel)
                        rubsalbrut = dao_rubrique.toGetRubriqueByReference("SALBRUT")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubsalbrut.designation, rubsalbrut.id, bulletin.id, nombre, base, taux, salbrut, rubsalbrut.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Base cotisation PVID (Calcul sur script)
                        primepvid = salbrut
                        if makeFloat(salbrut) > 1200000 : primepvid = 1200000
                        rubprimepvid = dao_rubrique.toGetRubriqueByReference("BASEPVID")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimepvid.designation, rubprimepvid.id, bulletin.id, nombre, base, taux, primepvid, rubprimepvid.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Base cotisation AT/MAF (Calcul sur script)
                        primebasecot = salbrut
                        if makeFloat(salbrut) > 600000 : primebasecot = 600000
                        rubprimebasecot = dao_rubrique.toGetRubriqueByReference("BASEATMAF")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimebasecot.designation, rubprimebasecot.id, bulletin.id, nombre, base, taux, primebasecot, rubprimebasecot.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #CNSS (Valeur recuperee sur fichier Excel)
                        rubcnss = dao_rubrique.toGetRubriqueByReference("CNSS")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubcnss.designation, rubcnss.id, bulletin.id, nombre, base, taux, cnss, rubcnss.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Base imposable (Calcul sur script)(A confirmer 2e script)
                        primebaseimpo = makeFloat(salbrut) - makeFloat(cnss)
                        rubprimebaseimpo = dao_rubrique.toGetRubriqueByReference("BASEIMPO")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimebaseimpo.designation, rubprimebaseimpo.id, bulletin.id, nombre, base, taux, primebaseimpo, rubprimebaseimpo.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Base imposable 80% (Calcul sur script)
                        primebaseimpo80 = primebaseimpo * 0.8
                        rubprimebaseimpo80 = dao_rubrique.toGetRubriqueByReference("BASEIMPO80")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimebaseimpo80.designation, rubprimebaseimpo80.id, bulletin.id, nombre, base, taux, primebaseimpo80, rubprimebaseimpo80.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Base imposable annuelle (Calcul sur script)
                        primebaseimpoannu = primebaseimpo80 * 12
                        rubprimebaseimpoannu = dao_rubrique.toGetRubriqueByReference("BASEIMPO80AN")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimebaseimpoannu.designation, rubprimebaseimpoannu.id, bulletin.id, nombre, base, taux, primebaseimpoannu, rubprimebaseimpoannu.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Quotité familliale (Calcul sur script a mettre a jour avec le 2e script)
                        primeqtefam = 0
                        rubprimeqtefam = dao_rubrique.toGetRubriqueByReference("QTEFAM")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeqtefam.designation, rubprimeqtefam.id, bulletin.id, nombre, base, taux, primeqtefam, rubprimeqtefam.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #IRPP (Valeur recuperee sur fichier Excel)
                        rubirpp = dao_rubrique.toGetRubriqueByReference("IRPP")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubirpp.designation, rubirpp.id, bulletin.id, nombre, base, taux, irpp, rubirpp.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Salaire brut après impôts  (Calcul sur script)
                        primesalbrutimpot = makeFloat(primebaseimpo) - makeFloat(irpp)
                        rubprimesalb = dao_rubrique.toGetRubriqueByReference("BRUTAPIMP")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimesalb.designation, rubprimesalb.id, bulletin.id, nombre, base, taux, primesalbrutimpot, rubprimesalb.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        ###### PRIME ET IMDEMNITES NON IMPOSABLES #########
                        #Imdemnité transport (Valeur recuperee sur fichier Excel)
                        rubindtrans = dao_rubrique.toGetRubriqueByReference("INDTRANSP")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubindtrans.designation, rubindtrans.id, bulletin.id, nombre, base, taux, indtrans, rubindtrans.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Complément transport (Valeur recuperee sur fichier Excel)
                        rubcmptrans = dao_rubrique.toGetRubriqueByReference("CMPLTRANSP")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubcmptrans.designation, rubcmptrans.id, bulletin.id, nombre, base, taux, cmptrans, rubcmptrans.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Indemnité de départ
                        primeinddepart = 0
                        rubprimeinddepart = dao_rubrique.toGetRubriqueByReference("INDDEPART")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeinddepart.designation, rubprimeinddepart.id, bulletin.id, nombre, base, taux, primeinddepart, rubprimeinddepart.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                        ###### FIN PRIME ET IMDEMNITES NON IMPOSABLES #########

                        ###### RETENUES #########
                        #Mutuelle ARPCE
                        rubcotmutuel = dao_rubrique.toGetRubriqueByReference("COTARPCE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubcotmutuel.designation, rubcotmutuel.id, bulletin.id, nombre, base, taux, cotmutuel, rubcotmutuel.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #gérer les prêts façon ERP NSANDAX
                        rubpret = dao_rubrique.toGetRubriqueByReference("PRET")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubpret.designation, rubpret.id, bulletin.id, nombre, base, taux, pret, rubpret.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Retenue avance sur salaire
                        primeretavsal = 0
                        rubprimeretavsal = dao_rubrique.toGetRubriqueByReference("RETAVSAL")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeretavsal.designation, rubprimeretavsal.id, bulletin.id, nombre, base, taux, primeretavsal, rubprimeretavsal.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Cotisation Retraite
                        primecolretr = 0
                        rubprimecolretr = dao_rubrique.toGetRubriqueByReference("COTRETR")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimecolretr.designation, rubprimecolretr.id, bulletin.id, nombre, base, taux, primecolretr, rubprimecolretr.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        ###### FIN RETENUES #########

                        ###### CHARGES PATRONALES #########
                        #CNSS Allocation familiale (A confirmer sur 2e script)
                        base = primebasecot
                        taux = 10.03
                        primeallfam = base * (taux/100)
                        rubprimeallfam = dao_rubrique.toGetRubriqueByReference("ALLFAM")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimeallfam.designation, rubprimeallfam.id, bulletin.id, nombre, base, 0, 0, rubprimeallfam.sequence, taux, primeallfam)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #CNSS Part Patronale
                        base = primepvid
                        taux = 8
                        primepatron = base * (taux/100)
                        rubprimepatron = dao_rubrique.toGetRubriqueByReference("PARTPATRON")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimepatron.designation, rubprimepatron.id, bulletin.id, nombre, base, 0, 0, rubprimepatron.sequence, taux, primepatron)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Taxe unique sur les salaires
                        base = salbrut
                        taux = 7.5
                        primetaxunsal = base * (taux/100)
                        rubtaxunsal = dao_rubrique.toGetRubriqueByReference("TAXUNSAL")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubtaxunsal.designation, rubtaxunsal.id, bulletin.id, nombre, base, 0, 0, rubtaxunsal.sequence, taux, primetaxunsal)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #CNSS Acc trav Mal Prof
                        base = primebasecot
                        taux = 2.25
                        primemalprof = base * (taux/100)
                        rubprimemalprof = dao_rubrique.toGetRubriqueByReference("CNACCTRMALPRO")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimemalprof.designation, rubprimemalprof.id, bulletin.id, nombre, base, 0, 0, rubprimemalprof.sequence, taux, primemalprof)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        base = 0
                        taux = 0
                        ###### FIN CHARGES PATRONALES #########

                        ###### TOTAUX #########
                        #Total Cotisations salariales
                        primetotalcot = cnss
                        rubprimetotalcat = dao_rubrique.toGetRubriqueByReference("TOTCOTISAL")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimetotalcat.designation, rubprimetotalcat.id, bulletin.id, nombre, base, taux, primetotalcot, rubprimetotalcat.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Total Cotisations patronales
                        primetotcotipat = primepatron + primemalprof + primeallfam
                        rubprimetotcotipat = dao_rubrique.toGetRubriqueByReference("TOTCOTIPAT")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimetotcotipat.designation, rubprimetotcotipat.id, bulletin.id, nombre, base, taux, primetotcotipat, rubprimetotcotipat.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Total gain (A confirmer 2e script)
                        primetotgain = salbrut + indtrans + cmptrans + primeinddepart
                        rubprimetotgain = dao_rubrique.toGetRubriqueByReference("TOTGAIN")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimetotgain.designation, rubprimetotgain.id, bulletin.id, nombre, base, taux, primetotgain, rubprimetotgain.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Total retenue (A confirmer 2e script)
                        primetotret = cnss + irpp + pret + primeretavsal + cotmutuel
                        rubprimetotret = dao_rubrique.toGetRubriqueByReference("TOTRET")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimetotret.designation, rubprimetotret.id, bulletin.id, nombre, base, taux, primetotret, rubprimetotret.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                        ###### FIN TOTAUX #########

                        ##### NET A PAYER #####
                        rubnetpay = dao_rubrique.toGetRubriqueByReference("NETAPAY")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubnetpay.designation, rubnetpay.id, bulletin.id, nombre, base, taux, netpay, rubnetpay.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        ###### AUTRES RUBRIQUES #########
                        #Total présences en jour (Configuration sur script)
                        primetotjour = 26
                        rubprimetotjour = dao_rubrique.toGetRubriqueByReference("TOTPRESJR")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimetotjour.designation, rubprimetotjour.id, bulletin.id, nombre, base, taux, primetotjour, rubprimetotjour.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Jours congés (Configuration sur script)
                        primejrconge = 2.17
                        rubprimejrconge = dao_rubrique.toGetRubriqueByReference("JRSCONGES")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimejrconge.designation, rubprimejrconge.id, bulletin.id, nombre, base, taux, primejrconge, rubprimejrconge.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                        #Base de congé (Configuration sur script)
                        primebaseconge = salbrut
                        rubprimebaseconge = dao_rubrique.toGetRubriqueByReference("BASECONGE")
                        item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimebaseconge.designation, rubprimebaseconge.id, bulletin.id, nombre, base, taux, primebaseconge, rubprimebaseconge.sequence)
                        item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                        ###### FIN AUTRES RUBRIQUES #########

                        if est_regulier == True:
                            ###### CUMULS #########
                            #Cumul brut taxable (2e script Cumul_net_taxable)
                            primecumbrutax = 0
                            rubprimecumbru = dao_rubrique.toGetRubriqueByReference("CUMBRUTAX")
                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimecumbru.designation, rubprimecumbru.id, bulletin.id, nombre, base, taux, primecumbrutax, rubprimecumbru.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                            #Cumul cotisation retraite (2e script )
                            primecumul = 0
                            rubprimecumul = dao_rubrique.toGetRubriqueByReference("CUMCOTRET")
                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimecumul.designation, rubprimecumul.id, bulletin.id, nombre, base, taux, primecumul, rubprimecumul.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                            #Cumul net taxe IRPP (2e script )
                            primenettaxeirpp = 0
                            rubprimenettaxeirpp = dao_rubrique.toGetRubriqueByReference("CUMNETIRPP")
                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimenettaxeirpp.designation, rubprimenettaxeirpp.id, bulletin.id, nombre, base, taux, primenettaxeirpp, rubprimenettaxeirpp.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)

                            #Cumul IRPP
                            rubprimecumulirpp = dao_rubrique.toGetRubriqueByReference("CUMIRPP")
                            # print('-----rubprimecumulirpp', rubprimecumulirpp)
                            print('--Show Me Periode', periode)
                            if int(periode.month) == 1: primecumulirpp = irpp
                            elif int(periode.month) > 1:
                                mois = periode.month
                                mois = mois - 1
                                annee = periode.year
                                lot = Model_LotBulletins.objects.filter(date_fin__month=mois,date_fin__year=annee,est_regulier=est_regulier).first()
                                print('-----rubprimecumulirpp ID {} lot ID {} et employe ID {}'.format(rubprimecumulirpp.id,lot.id,employe_id))
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin__lot_id = lot.id, bulletin__employe_id = employe_id, rubrique_id = rubprimecumulirpp.id).first()
                                print('-----rubprimecumulirpp item_bulletin', item_bulletin)
                                if item_bulletin == None:
                                    montantirpp = 0
                                    primecumulirpp =  makeFloat(montantirpp) + makeFloat(irpp)
                                else:
                                    primecumulirpp =  makeFloat(item_bulletin.montant) + makeFloat(irpp)
                                # print('-----rubprimecumulirpp', rubprimecumulirpp)
                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimecumulirpp.designation, rubprimecumulirpp.id, bulletin.id, nombre, base, taux, primecumulirpp, rubprimecumulirpp.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                            print('-----item_bulletin', item_bulletin)

                            #Base des congés
                            primebaseconge = salbrut
                            rubprimebaseconge = dao_rubrique.toGetRubriqueByReference("CUMBASCONGE")

                            if int(periode.month) == 1:
                                primebaseconge = salbrut
                            elif int(periode.month) > 1:
                                mois = periode.month
                                mois = mois - 1
                                annee = periode.year
                                lot = Model_LotBulletins.objects.filter(date_fin__month=mois,date_fin__year=annee,est_regulier=est_regulier).first()
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin__lot_id = lot.id, bulletin__employe_id = employe_id, rubrique_id = rubprimebaseconge.id).first()
                                if item_bulletin == None:
                                    montantirpp = 0
                                    primebaseconge =  makeFloat(montantirpp) + makeFloat(irpp)
                                else:
                                    primebaseconge =  makeFloat(item_bulletin.montant) + makeFloat(irpp)
                                # primebaseconge =  makeFloat(item_bulletin.montant) + makeFloat(salbrut)

                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimebaseconge.designation, rubprimebaseconge.id, bulletin.id, nombre, base, taux, primebaseconge, rubprimebaseconge.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                            print('-----item_bulletin', item_bulletin)

                            #Cumul Nombre de jours présence
                            primepresence = primetotjour
                            rubprimepresence = dao_rubrique.toGetRubriqueByReference("CUMPRESENCE")

                            if int(periode.month) == 1:
                                primepresence = primetotjour
                            elif int(periode.month) > 1:
                                mois = periode.month
                                mois = mois - 1
                                annee = periode.year
                                lot = Model_LotBulletins.objects.filter(date_fin__month=mois,date_fin__year=annee,est_regulier=est_regulier).first()
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin__lot_id = lot.id, bulletin__employe_id = employe_id, rubrique_id = rubprimepresence.id).first()
                                if item_bulletin == None:
                                    montantirpp = 0
                                    primepresence =  makeFloat(montantirpp) + makeFloat(irpp)
                                else:
                                    primepresence =  makeFloat(item_bulletin.montant) + makeFloat(irpp)
                                # primepresence =  makeFloat(item_bulletin.montant) + makeFloat(primetotjour)

                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimepresence.designation, rubprimepresence.id, bulletin.id, nombre, base, taux, primepresence, rubprimepresence.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                            print('-----item_bulletin', item_bulletin)

                            #Cumul Jours congés acquis
                            primejourconge = primejrconge
                            rubprimejourconge = dao_rubrique.toGetRubriqueByReference("CUMJRSCONGES")

                            if int(periode.month) == 1:
                                primejourconge = primejrconge
                            elif int(periode.month) > 1:
                                mois = periode.month
                                mois = mois - 1
                                annee = periode.year
                                lot = Model_LotBulletins.objects.filter(date_fin__month=mois,date_fin__year=annee,est_regulier=est_regulier).first()
                                item_bulletin = Model_ItemBulletin.objects.filter(bulletin__lot_id = lot.id, bulletin__employe_id = employe_id, rubrique_id = rubprimepresence.id).first()
                                if item_bulletin == None:
                                    montantirpp = 0
                                    primejourconge =  makeFloat(montantirpp) + makeFloat(irpp)
                                else:
                                    primejourconge =  makeFloat(item_bulletin.montant) + makeFloat(irpp)
                                # primejourconge =  makeFloat(item_bulletin.montant) + makeFloat(primejrconge)

                            item_bulletin = dao_item_bulletin.toCreate(auteur.id, rubprimejourconge.designation, rubprimejourconge.id, bulletin.id, nombre, base, taux, primejourconge, rubprimejourconge.sequence)
                            item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                            ###### FIN CUMULS #########

                        print("Fin Iterration ID {}".format(i))
                    else:
                        compteur = compteur + 1
                        continue

            print('LES EMPLOYES MANQUANT', len(ListEmployeMiss))
            # transaction.savepoint_commit(sid)
        except Exception as e:
            print("---ERREUR IMPORT RUBRIQUE DE PAIE---")
            print(e)
            # transaction.savepoint_rollback(sid)