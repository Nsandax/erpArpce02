# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from ErpBackOffice.utils.auth import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from collections import namedtuple
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ErpBackOffice.dao.dao_place_type import dao_place_type
from ErpBackOffice.dao.dao_place import dao_place
from ModuleAchat.dao.dao_categorie import dao_categorie
from ModuleAchat.dao.dao_categorie_article import	 dao_categorie_article
from ErpBackOffice.dao.dao_personne import dao_personne
from ErpBackOffice.dao.dao_utilisateur import dao_utilisateur
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
#from ModuleRessourcesHumaines.dao.dao_departement import dao_departement
#from ModuleRessourcesHumaines.dao.dao_poste import dao_poste

from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId


from ErpBackOffice.dao.dao_paiement_interne import dao_paiement_interne
from ErpBackOffice.dao.dao_module import dao_module
from ErpBackOffice.dao.dao_sous_module import dao_sous_module
from ErpBackOffice.utils.identite import identite
from ErpBackOffice.utils.tools import ErpModule
from ModuleRessourcesHumaines.dao.dao_bareme import dao_bareme
from ModuleRessourcesHumaines.dao.dao_tranche_bareme import dao_tranche_bareme
from ModuleRessourcesHumaines.dao.dao_bulletin import dao_bulletin
from ModuleRessourcesHumaines.dao.dao_item_bulletin import dao_item_bulletin
from ModuleRessourcesHumaines.dao.dao_element_bulletin import dao_element_bulletin
from ModuleRessourcesHumaines.dao.dao_lot_bulletin import dao_lot_bulletin
from ModuleRessourcesHumaines.dao.dao_type_element_bulletin import dao_type_element_bulletin
from ModuleRessourcesHumaines.dao.dao_profil_paie import dao_profil_paie
from ModuleRessourcesHumaines.dao.dao_item_profil_paie import dao_item_profil_paie
from ModuleRessourcesHumaines.dao.dao_type_calcul import dao_type_calcul
from ModuleRessourcesHumaines.dao.dao_type_resultat import dao_type_resultat


from ErpBackOffice.dao.dao_wkf_historique_lotbulletin import dao_wkf_historique_lotbulletin
from ErpBackOffice.dao.dao_wkf_historique_bulletin import dao_wkf_historique_bulletin
from ErpBackOffice.dao.dao_wkf_workflow import dao_wkf_workflow
from ErpBackOffice.dao.dao_wkf_etape import dao_wkf_etape
from ErpBackOffice.dao.dao_wkf_transition import dao_wkf_transition
from ErpBackOffice.dao.dao_wkf_condition import dao_wkf_condition
from ErpBackOffice.dao.dao_wkf_approbation import dao_wkf_approbation

from ErpBackOffice.dao.dao_compte import dao_compte
from ErpBackOffice.dao.dao_role import dao_role
from ErpBackOffice.dao.dao_droit import dao_droit
from ErpBackOffice.models import Model_ItemProfilPaye
from ErpBackOffice.models import Model_ProfilPaye
from ErpBackOffice.models import Model_PaiementInterne
from ModuleRessourcesHumaines.dao.dao_organisation import dao_organisation
import datetime
import json
import array
##############################""
FRAIS_PAR_DEPENDANT_ENFANTS =  100 #dao_organisation.toGetMainOrganisation().frais_dependant_enfant
FRAIS_PAR_DEPENDANT_FEMME   =  100 #dao_organisation.toGetMainOrganisation().frais_dependant_femme
INDEMNITE_TRANSPORT         =  1500 #dao_organisation.toGetMainOrganisation().indemnite_transp
INDEMNITE_LOGEMENT_ENFANT   =  50 #dao_organisation.toGetMainOrganisation().indemnite_log_enfant
INDEMNITE_LOGEMENT_FEMME    =  50 #dao_organisation.toGetMainOrganisation().indemnite_log_femme
INSS_QPO    =  3.5 #dao_organisation.toGetMainOrganisation().INSS_QPO 
MONTANT_ANCIENNETE = 50
NOMBRE_AGENT = 43

##########""

def get_jours_travailles(employee_id):
    #TODO Récupérer le nombre de jours prestés de l'employé (disponible grace au sous Module présence à finaliser)
    nbre_jours = 22 # Par défaut
    return nbre_jours

def get_jours_conges_circ(employee_id):
    #TODO Récupérer le nombre de jours de congé de circonstance de l'employé durant le mois en cours (disponible grace au sous Module congé à finaliser)
    nbre_jours = 4 # Par défaut
    return nbre_jours

def get_temps_engagement(employee_id):
    #TODO recupéré le nombre jour depuis l'engagement jusqu'à la fin du mois en cours
    temps = 26 # Par défaut
    return temps


def calcul_impot_sur_bareme(bareme_id, ni):
    #print("Fonction: calcul_impot_sur_bareme") 
    resultat = 0
    bareme = dao_bareme.toGet(bareme_id)
    tranches = dao_tranche_bareme.toGetDuBareme(bareme.id)
    #impot_d=[0,11297.85,21199.8,35999.775,54999.75,75000]
    impot_d=[]
    for tranche in tranches:
        n = tranche.montant_net_impot * tranche.pourcentage_net_impot
        impot_d.append(n)

    max_seq=tranches.count()
    ni_calcul= ni
    impot = 0
    control_i     = 1 #

    for tranche in tranches:
        if control_i == tranche.sequence and (control_i not in  (max_seq,0)) :                       
            if ni < tranche.tranche_fin:
                #print("IF 1")
                delta = ni - tranche.tranche_debut
                impot += delta * tranche.pourcentage_net_impot 
                ni_calcul -= delta
                control_i +=1
                return impot
            elif ni > tranche.tranche_fin:
                #print("IF 2") 
                delta = tranche.tranche_fin - tranche.tranche_debut
                r = control_i-1
                impot += impot_d[control_i-1]
                ni_calcul -= delta
                control_i +=1
            else:
                #print('erreur cas ni < max tranche de bareme')
                pass
        elif control_i == tranche.sequence and (control_i in (max_seq,0)) :
            if ni < tranche.tranche_fin:
                #print("IF 3") 
                delta = ni - tranche.tranche_debut
                impot += delta * tranche.pourcentage_net_impot                 
                ni_calcul -= delta
                control_i +=1
                return impot
            else:
                #print('erreur cas ni > max tranche de bareme')
                pass
        else:
            #print('erreur sequencing')
            pass
    return impot


def calcul_paie(employee_id,code_element_paie,type_calcul,base_de_calcul,pourcentage, montant=0, bi=None, ni=None, bareme=None):
    #print( "Entre dans la fonction calcul_paie" )
    #print( "%s %s  %s  %s %s"  %( employee_id,code_element_paie,type_calcul,base_de_calcul,pourcentage))
    if code_element_paie == 'BASE':
        #Salaire 	A payer 	imposable
        #print('BASE')
        BASE = 0
        temps = get_jours_travailles(employee_id)
        BASE = temps * montant/22
        return BASE
    elif code_element_paie == 'CIRC':
        #Congé de circonstance 	A payer imposable
        #print('CIRC')
        CIRC = 0
        temps = get_jours_conges_circ(employee_id)
        #CIRC = temps * montant/22
        CIRC = montant
        return CIRC
    elif code_element_paie == 'ANC':
        #Ancienneté A payer imposable 
        #print('ANC')
        ANC = 0
        temps = get_temps_engagement(employee_id)
        #ANC = temps * MONTANT_ANCIENNETE
        ANC = montant
        return ANC
    elif(code_element_paie == 'PRIPRO'):
        #Prime Professionelle A payer imposable 
        #print('PRIPRO')
        PRIPRO = montant
        return PRIPRO
    elif(code_element_paie == 'VIECH'):
            #Vie chère 	A payer 	Non imposable 
        #print('VIECH')
        VIECH = montant
        return VIECH
    elif code_element_paie == 'ALFAMLEG':
        #Alloc. Familliale Légales 	A payer 	Non imposable 
        #print('ALFAMLEG')
        ALFAMLEG = 0
        # get employe à partir du employee_id
        dependant_enfant = 1 #employe.dependant_enfant
        dependant_femme = 1 #employe.dependant_femme
        ALFAMLEG  =  (dependant_enfant * FRAIS_PAR_DEPENDANT_ENFANTS) + (dependant_femme * FRAIS_PAR_DEPENDANT_FEMME) 
        ALFAMLEG  =  montant
        return ALFAMLEG
    elif(code_element_paie == 'INDTR'):
        #Indemnité Transport 	A payer 	Non imposable 
        #print('INDTR')
        INDTR = INDEMNITE_TRANSPORT
        INDTR  = montant 
        return INDTR
    elif(code_element_paie == 'INDLOG'):
        #Indemnité Logement 	A payer 	Non imposable *
        #print('INDLOG')
        dependant_enfant = 1 #employe.dependant_enfant
        dependant_femme = 1 #employe.dependant_femme
        INDLOG  =  (dependant_enfant * FRAIS_PAR_DEPENDANT_ENFANTS) + (dependant_femme * FRAIS_PAR_DEPENDANT_FEMME) 
        INDLOG  = montant 
        return INDLOG
    elif (code_element_paie == 'IMP'):
        #Impôt 	A retenir 	Non imposable 
        #print('IMP')
        IMP = 0
        if ni != None and bareme != 0:
            #print('NI et Bareme entres')
            IMP = calcul_impot_sur_bareme(bareme, ni)
        return IMP
    elif (code_element_paie == 'INSS'):
        #INSS 	A retenir 	Non imposable 
        #print('INSS')
        INSS = 0
        if bi != None:
            INSS = (bi * INSS_QPO) / 100
        return INSS
    elif (code_element_paie == 'ONEM'):
        #ONEM 	A retenir 	Non imposable 
        #print('ONEM')
        ONEM = 0
        if bi != None:
            ONEM = (bi * 0.2) / 100
        return ONEM
    elif (code_element_paie == 'SYND'):
        #Syndicat 	A retenir 	Non imposable 
        #print('SYND')
        SYND = 0
        if ni != None:
            SYND = (ni * 2) / 100
        return SYND
    elif (code_element_paie == 'INPP'):
        #INPP 	A retenir 	Non imposable 
        #print('INPP')
        INPP = 0
        if ni != None:
            if NOMBRE_AGENT < 51: INPP = (ni * 3) / 100 # de 0 à 50 agents
            if NOMBRE_AGENT > 50 and NOMBRE_AGENT < 101: INPP = (ni * 2) / 100 # de 51 à 100 agents
            if NOMBRE_AGENT > 100: INPP = (ni * 1) / 100 # plus de 100 agents
        return INPP
    else:
        #print('erreur')
        return 0
    

###############################

# CALCUL PAIE CONTROLLER

# FONCTION DU CALCUL DE PAIE D'UN AGENT SPECIFIQUE AVEC ID PASSER EN PARAMETRE
@transaction.atomic
def get_calcul_paie_employe(request, ref):  
    sid = transaction.savepoint() 	
    try:
        droit="LISTER_EMPLOYE" # 'CALCUL_PAIE' Rôle à configuré
        modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

        if response != None:
            return response

        employee_id = int(ref)
        employe = dao_employe.toGetEmploye(employee_id)
        #print(employe.nom_complet)
        profilpaie = dao_profil_paie.toGetProfilOfEmployee(employe.id)
        #print(profilpaie.designation)

        #impot = calcul_impot_sur_bareme(1, 434429.49)

            
        # dictionaire 
        element_payable_imposable =  {}
        element_payable_non_imposable =  {}
        element_a_retenir= {}
        elements =  {}

        # recuperation des elements
        employee_pay_profile = dao_item_profil_paie.toGetItemOfProfil(profilpaie.id)
        for element in employee_pay_profile:
            if element.element.type_element == 1 and element.element.categorie_element == 1: #A PAYER ET IMPOSABLE
                element_payable_imposable[element.element.reference] =  calcul_paie(employee_id,element.element.reference,element.element.type_calcul,element.element.type_resultat,element.element.pourcentage, element.montant)
            if element.element.type_element == 1 and element.element.categorie_element == 2: #A PAYER ET NON IMPOSABLE
                element_payable_non_imposable[element.element.reference] =  calcul_paie(employee_id,element.element.reference,element.element.type_calcul,element.element.type_resultat,element.element.pourcentage, element.montant)
            if element.element.type_element == 2: #A RETENIR
                #print("Element a retenir")
                #print(element_payable_imposable.values())
                bi = 0
                for montant in element_payable_imposable.values(): bi = bi + makeFloat(montant) # calcul du brut imposable en recuperant le montant total du dictionnaire element_payable_imposable
                inss_qpo = bi * (INSS_QPO / 100) 
                ni = bi - inss_qpo 
                element_a_retenir[element.element.reference] =  calcul_paie(employee_id,element.element.reference,element.element.type_calcul,element.element.type_resultat,element.element.pourcentage, element.montant, bi, ni, element.element.bareme_id)


        #print("Debut calcul")
        # Calcul du total à retenir
        total_a_retenir = 0
        for montant in element_a_retenir.values(): 
            total_a_retenir = total_a_retenir + makeFloat(montant)

        #print("Total retenir caculer")
        #print(total_a_retenir)

        # Calcul du total à payer (Brut Total)
        brut_total = 0
        total_imposable = 0
        total_non_imposable = 0
        for montant in element_payable_imposable.values(): 
            total_imposable = total_imposable + makeFloat(montant)
        for montant in element_payable_non_imposable.values(): 
            total_non_imposable = total_non_imposable + makeFloat(montant)
        brut_total = total_imposable + total_non_imposable

        #print("Total payer caculer")
        #print(brut_total)

        # Calcul du Net à Payer
        net_a_payer = brut_total - total_a_retenir

        #print("Net a payer caculer")
        #print(net_a_payer)

        #On crée l'objet Bulletin
        lot_id = 1
        designation = 'Bulletin de paie de l\'agent %s' % employe.nom_complet
        bulletin = dao_bulletin.toCreate(utilisateur.id, designation, employe.id, lot_id)
        bulletin = dao_bulletin.toSave(bulletin)

        if bulletin != None :
            #print("Bulletin cree")
            # On rajoute les valeurs calculées dans le bulletin crée 
            bulletin.total_a_retenir = total_a_retenir
            bulletin.brut_total = brut_total
            bulletin.net_a_payer = net_a_payer
            bulletin.brut_imposable = bi
            bulletin.net_imposable = ni
            bulletin.save()
            # On crée les items liés au bulletin que nous de créer
            item_bulletins = []
            for element in employee_pay_profile:
                temps = 0
                taux = 1
                montant = 0.0
                if element.element.type_element == 1 and element.element.categorie_element == 1: #A PAYER ET IMPOSABLE
                    montant = element_payable_imposable.get(element.element.reference)
                    if element.element.reference == "BASE":
                        temps = get_jours_travailles(employee_id)
                        taux = montant / temps
                    if element.element.reference == "ANC":
                        temps = get_temps_engagement(employee_id)
                        taux = montant / temps
                    if element.element.reference == "CIRC":
                        temps = get_jours_conges_circ(employee_id)
                        taux = montant / temps
                if element.element.type_element == 1 and element.element.categorie_element == 2: #A PAYER ET NON IMPOSABLE
                    montant = element_payable_non_imposable.get(element.element.reference)
                if element.element.type_element == 2: #A RETENIR
                    montant = element_a_retenir.get(element.element.reference)
                item_bulletin = dao_item_bulletin.toCreate(utilisateur.id, element.designation, element.element.id, bulletin.id, temps, taux, montant)
                item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                print ("Item bulletin: %i" % item_bulletin.id)
                item_bulletin.sequence = element.element.sequence
                item_bulletin.save()
                item_bulletins.append(item_bulletin)

            transaction.savepoint_commit(sid)
            return HttpResponseRedirect(reverse('module_ressources_humaines_details_bulletin',args=(bulletin.id,)))
        else : 
            messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du bulletin!")
            transaction.savepoint_rollback(sid)
            return HttpResponseRedirect(reverse('module_ressources_humaines_calcul_paie_list'))
    except Exception as e:
        #print("ERREUR DETAIL")
        #print(e)
        transaction.savepoint_rollback(sid)
        return HttpResponseRedirect(reverse('module_ressources_humaines_calcul_paie_list'))


# FONCTION DU CALCUL DE PAIE DES AGENTS AVEC ID DU DOSSIER PAIE PASSER EN PARAMETRE
@transaction.atomic
def get_calcul_paie_dossier(request, ref):  
    sid = transaction.savepoint() 	
    try:
        droit="LISTER_EMPLOYE" # 'CALCUL_PAIE' Rôle à configuré
        modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

        if response != None:
            return response

        #On recupère les input du workflow
        utilisateur_id = request.user.id
        etape_id = request.POST["etape_id"]
        lotbulletin_id = request.POST["doc_id"]
        #print("print 1 %s %s %s" % (utilisateur_id, etape_id, lotbulletin_id))

        #A partir de ces Inputs, on recupère les objet
        employe = dao_employe.toGetEmployeFromUser(utilisateur_id)
        etape = dao_wkf_etape.toGetEtapeWorkflow(etape_id)
        lot_bulletin = dao_lot_bulletin.toGet(lotbulletin_id)
        #print("print 2 %s %s %s " % (employe, etape, lot_bulletin))

        #On recupère le dossier de paie
        dossier_id = int(ref)
        dossier = dao_lot_bulletin.toGet(dossier_id)
        #print("Dossier recupere {}".format(dossier.designation))

        #On recupère les employes du dossier
        employes = dao_employe.toListEmployesActifs() 
        if dossier.type == "Tous": employes = dao_employe.toListEmployesActifs()  
        elif dossier.type == "Par departement": employes = dao_employe.toListEmployesOfDepartement(dossier.departement.id)
        #print("Employe(s) recupere(s) {}".format(employes)) 

        #On recupère les paiements
        paiements = dao_paiement_interne.toListPaiementsOfDossierPaie(dossier.id)
        #print("Paiement(s) recupere(s) {}".format(paiements))

		#On calcul la paye pour chaque employé du dossier dans cette boucle
        for employe in employes:
            #print("Employe {}".format(employe.nom_complet))
            profilpaie = dao_profil_paie.toGetProfilOfEmployee(employe.id)
            #print("Profil Paie recupere {}".format(profilpaie.designation))

            #impot = calcul_impot_sur_bareme(1, 434429.49)
            
            # dictionaire 
            element_payable_imposable =  {}
            element_payable_non_imposable =  {}
            element_a_retenir= {}
            elements =  {}

            # recuperation des elements (1ere Boucle pour les élèments à payer)
            employee_pay_profile = dao_item_profil_paie.toGetItemOfProfil(profilpaie.id)
            for element in employee_pay_profile:
                if element.element.type_element == 1 and element.element.categorie_element == 1: #A PAYER ET IMPOSABLE
                    #Gestion Allocation de congé
                    if element.element.reference == "CONGE":
                        allocation_conge = get_allocation_amount(employe, paiements)
                        element_payable_imposable[element.element.reference] = allocation_conge
                    #Fin Gestion Allocation de congé
                    else : element_payable_imposable[element.element.reference] =  calcul_paie(employe.id,element.element.reference,element.element.type_calcul,element.element.type_resultat,element.element.pourcentage, element.montant)
                if element.element.type_element == 1 and element.element.categorie_element == 2: #A PAYER ET NON IMPOSABLE
                    element_payable_non_imposable[element.element.reference] =  calcul_paie(employe.id,element.element.reference,element.element.type_calcul,element.element.type_resultat,element.element.pourcentage, element.montant)



            # recuperation des elements (2eme Boucle pour les élèments à retenir)
            for element in employee_pay_profile:
                if element.element.type_element == 2: #A RETENIR
                    #print("Element a retenir")
                    #print(element_payable_imposable.values())
                    bi = 0
                    for montant in element_payable_imposable.values(): bi = bi + makeFloat(montant) # calcul du brut imposable en recuperant le montant total du dictionnaire element_payable_imposable
                    inss_qpo = bi * (INSS_QPO / 100) 
                    ni = bi - inss_qpo 
                    #Gestion des prêts
                    if element.element.reference == "PRET":
                        pret = get_pret_amount(employe, paiements)
                        element_a_retenir[element.element.reference] = pret
                    #Fin Gestion des prêts
                    else : element_a_retenir[element.element.reference] =  calcul_paie(employe.id,element.element.reference,element.element.type_calcul,element.element.type_resultat,element.element.pourcentage, element.montant, bi, ni, element.element.bareme_id)


            #print("Debut calcul")
            # Calcul du total à retenir
            total_a_retenir = 0
            for montant in element_a_retenir.values(): 
                total_a_retenir = total_a_retenir + makeFloat(montant)

            #print("Total retenir caculer")
            #print(total_a_retenir)

            # Calcul du total à payer (Brut Total)
            brut_total = 0
            total_imposable = 0
            total_non_imposable = 0
            for montant in element_payable_imposable.values(): 
                total_imposable = total_imposable + makeFloat(montant)
            for montant in element_payable_non_imposable.values(): 
                total_non_imposable = total_non_imposable + makeFloat(montant)
            brut_total = total_imposable + total_non_imposable

            #print("Total payer caculer")
            #print(brut_total)

            # Calcul du Net à Payer
            net_a_payer = brut_total - total_a_retenir

            #print("Net a payer caculer")
            #print(net_a_payer)

            #On crée l'objet Bulletin
            lot_id = dossier_id
            designation = 'Bulletin de paie de l\'agent %s' % employe.nom_complet
            bulletin = dao_bulletin.toCreate(utilisateur.id, designation, employe.id, lot_id)
            bulletin = dao_bulletin.toSave(bulletin)

            #print("Bulletin cree ID {}".format(bulletin.id))
            # On rajoute les valeurs calculées dans le bulletin crée 
            bulletin.total_a_retenir = total_a_retenir
            bulletin.brut_total = brut_total
            bulletin.net_a_payer = net_a_payer
            bulletin.brut_imposable = bi
            bulletin.net_imposable = ni
            bulletin.save()
            #print("Bulletin ID {} modifie avec les champs de calcul".format(bulletin.id))
            # On crée les items liés au bulletin que nous de créer
            item_bulletins = []
            for element in employee_pay_profile:
                temps = 0
                taux = 1
                montant = 0.0
                if element.element.type_element == 1 and element.element.categorie_element == 1: #A PAYER ET IMPOSABLE
                    montant = element_payable_imposable.get(element.element.reference)
                    if element.element.reference == "BASE":
                        temps = get_jours_travailles(employe.id)
                        taux = montant / temps
                    if element.element.reference == "ANC":
                        temps = get_temps_engagement(employe.id)
                        taux = montant / temps
                    if element.element.reference == "CIRC":
                        temps = get_jours_conges_circ(employe.id)
                        taux = montant / temps
                if element.element.type_element == 1 and element.element.categorie_element == 2: #A PAYER ET NON IMPOSABLE
                    montant = element_payable_non_imposable.get(element.element.reference)
                if element.element.type_element == 2: #A RETENIR
                    montant = element_a_retenir.get(element.element.reference)
                #On ne prends pas les élèments où le montant est null (0)
                if montant > 0:
                    item_bulletin = dao_item_bulletin.toCreate(utilisateur.id, element.designation, element.element.id, bulletin.id, temps, taux, montant)
                    item_bulletin = dao_item_bulletin.toSave(item_bulletin)
                    print ("Item bulletin: %i" % item_bulletin.id)
                    item_bulletin.sequence = element.element.sequence
                    item_bulletin.save()
                    item_bulletins.append(item_bulletin)

        # Gestion des transitions dans le document
        lot_bulletin.statut_id = etape.id
        lot_bulletin.etat = etape.designation
        lot_bulletin.est_soumis = True
        lot_bulletin.save()
        #print("Dossier ID: {} modifie avec nouvelle etape ".format(lot_bulletin.id))

        #On enregistre l'historique de cette transition d'étape du workflow
        historique = dao_wkf_historique_lotbulletin.toCreateHistoriqueWorkflow(employe.id, etape.id, lot_bulletin.id)
        historique = dao_wkf_historique_lotbulletin.toSaveHistoriqueWorkflow(historique)
        #print("Historique ID: {}".format(historique.id))

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('module_ressources_humaines_details_lotbulletin',args=(lot_bulletin.id,)))
    except Exception as e:
        #print("ERREUR DETAIL")
        #print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de l'enregistrement du bulletin!")
        transaction.savepoint_rollback(sid)
        return HttpResponseRedirect(reverse('module_ressources_humaines_calcul_paie_list'))


# FONCTION DE LA LISTE D'EMPLOYES POUR LE CALCUL DE PAIE
def get_calcul_paie_list(request):
    droit = "LISTER_EMPLOYE"
    modules, utilisateur, roles, response = auth.toGetAuthDroit(droit, request)

    if response != None:
        return response

	
    model = dao_employe.toListEmployes()
    context = {
        'title' : 'Liste des employes ( Calcul paie )',
        'model' : model,
        #'can_create' : dao_droit.toGetDroitRole('CREER_EMPLOYE',nom_role,utilisateur.nom_complet),
        'menu' : 12,
        "modules" : modules,
        'actions':auth.toGetActions(modules,utilisateur),
        'organisation': dao_organisation.toGetMainOrganisation(),
        "module" : ErpModule.MODULE_RESSOURCES_HUMAINES,
        'utilisateur' : utilisateur
    }
    template = loader.get_template("ErpProject/ModuleRessourcesHumaines/calculpaie/list.html")
    return HttpResponse(template.render(context, request))

# FONCTION POUR TESTER LE BAREME
def get_test_bareme(request):
    data = {}
    try:
        bareme_id = int(request.GET["ref"])
        montant_ni = makeFloat(request.GET["ref_montant"])

        impot = calcul_impot_sur_bareme(bareme_id, montant_ni)

        data = {
            "impot" : impot
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        #print(e)
        return JsonResponse(data, safe=False)    

# FONCTION POUR TESTER LE BAREME
def get_allocation_amount(employe, paiements):
    montant = 0
    try:
        for paiement in paiements:
            if paiement.conge.employe.id == employe.id:
                montant = montant + paiement.montant
        return montant
    except Exception as e:
        #print(e)
        return montant

# FONCTION POUR TESTER LE BAREME
def get_pret_amount(employe, paiements):
    montant = 0
    try:
        for paiement in paiements:
            if paiement.pret.employe.id == employe.id:
                montant = montant + paiement.montant
        return montant
    except Exception as e:
        #print(e)
        return montant