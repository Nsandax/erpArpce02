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
import os
from django.conf import settings
from django.core.files.storage import default_storage

from ErpBackOffice.utils.identite import identite
from django.contrib.contenttypes.models import ContentType
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.dao.dao_compte import dao_compte
from ModuleBudget.dao.dao_transactionbudgetaire import dao_transactionbudgetaire
from ModuleBudget.dao.dao_ligne_budgetaire import dao_ligne_budgetaire
from ModuleInventaire.dao.dao_ligne_traitementimmobilisation import dao_ligne_traitementimmobilisation
from ModuleRessourcesHumaines.dao.dao_ligne_competence import dao_ligne_competence


class function_workflow(object):
    
    @staticmethod
    def createTransactionEngagementBudgetaire(auteur,objet_modele):
        '''Fonction de création d'une transaction budgétaire à partir d'un bon de commande'''
        dao_transactionbudgetaire.toCreateTransactionEngagementBudgetaire(auteur, objet_modele)


    

    @staticmethod
    def processingImmobilisationAsset(auteur,objet_modele):
        #print("I'm inside of Immo Asset")
        #Recuperation des lignes de l'objet traitement d'immobilisation
        lignes = dao_ligne_traitementimmobilisation.toListLigneOfTraitement(objet_modele.id)

        for ligne in lignes:
            #print("lign",ligne)
            asset = ligne.immobilisation.immobilier
            asset.employe = None
            asset.est_immobilise = True
            asset.save()
    
    @staticmethod
    def createTransactionBudgetaireOfMission(auteur,objet_modele):
        #print("I'm inside, Good Job Girl")
        #Recuperation des lignes du bon de reception
        devise = dao_devise.toGetDeviseReference()

        if objet_modele.ligne_budgetaire_id:
            ligne_budgetaire = dao_ligne_budgetaire.toGetLigneBudgetaire(objet_modele.ligne_budgetaire_id)
            transactionBudgetaire = dao_transactionbudgetaire.toCreateTransactionbudgetaire("Paiement Frais de mission "+objet_modele.numero_ordre,objet_modele.frais_mission,"",devise.id,ligne_budgetaire.poste_budgetaire_id,auteur.id,ligne_budgetaire.id,1,2)
            transactionBudgetaire = dao_transactionbudgetaire.toSaveTransactionbudgetaire(auteur, transactionBudgetaire)
            transactionBudgetaire.ordre_mission_id = objet_modele.id
            transactionBudgetaire.save()
        
        #print("end of that")
    
    @staticmethod
    def createLigneCompetenceOfEmploye(auteur,objet_modele):
        #print("I'm inside, Good Job Girl")
        #Recuperation des lignes du bon de reception
        ligne_competence = dao_ligne_competence.toCreateLigneCompetence(objet_modele.competence, objet_modele.observation, objet_modele.employe_id)
        ligne_competence = dao_ligne_competence.toSaveLigneCompetence(auteur, ligne_competence)
        
    