# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Evenement, Model_Participant, TypeRecurrent, Confidentialite, TypeFinRecurrent, ParJour, ParMois, JoursDelaSemaine
from ErpBackOffice.dao.dao_personne import dao_personne
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ModuleComptabilite.dao.dao_local import dao_local
from ModuleConversation.dao.dao_notif import dao_notif
from ModuleConversation.dao.dao_temp_notification import dao_temp_notification
from ModuleCalendrier.dao.dao_alarme import dao_alarme
from ModuleCalendrier.dao.dao_participant import dao_participant
from ModuleCalendrier.dao.dao_type_evenement import dao_type_evenement

from django.utils import timezone
from datetime import time, timedelta, datetime
import json
from ErpBackOffice.utils.EmailThread import send_async_mail

class dao_evenement(object):
    id = 0
    designation = ""
    description = ""
    duree = 1
    date_debut = None
    date_fin = None
    local_id = None
    type_evenement_id = None
    confidentialite = 1
    date_du_mois  =  1
    est_actif  =  True
    journee  =  False
    auteur_id = 0
    
    est_recurrent = False
    interval_recurrent = 1
    type_recurrent = 1
    compte_recurrent = 1
    type_fin_recurrent = 1
    date_fin_recurrent = None
    
    lundi = False
    mardi =  False
    mercredi = False
    jeudi = False
    vendredi = False
    samedi = False
    dimanche =  False
    
    par_jour = 1
    par_mois =  1
    date_du_mois =  1
    jour_de_semaine = '1'
    recurrent_id = 0
    
    

    @staticmethod
    def toList():
        return  Model_Evenement.objects.all().order_by("-creation_date")
    
    @staticmethod
    def toListDeUtilisateur(utilisateur):
        try:
            list = []
            evenements = Model_Evenement.objects.all().order_by("-creation_date")
            for evenement in evenements:
                participation = Model_Participant.objects.filter(employe_id = utilisateur.id, evenement_id = evenement.id).count()
                if evenement.auteur.id == utilisateur.id or participation > 0:
                    list.append(evenement)
            return list
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_evenement)")
            #print(e)
            return []
    
    @staticmethod
    def toCreate(auteur_id, date_debut = None, date_fin = None, type_evenement_id = None, designation = "", description = "", local_id = None ,confidentialite = 1, duree = "00:00", journee = False):
        try:
            evenement = dao_evenement()
            if auteur_id == 0: auteur_id = None
            evenement.auteur_id = auteur_id
            if type_evenement_id == 0: type_evenement_id = None
            evenement.type_evenement_id = type_evenement_id
            if local_id == 0: local_id = None
            evenement.local_id = local_id
            evenement.designation = designation
            evenement.description = description
            evenement.date_debut = date_debut
            evenement.date_fin = date_fin
            evenement.confidentialite = confidentialite
            evenement.duree = duree
            evenement.journee = journee
            return evenement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_evenement)")
            #print(e)
            return None
        
    @staticmethod
    def toCreateRecurrent(dao_evenement, est_recurrent = True, interval_recurrent = 1,type_recurrent = 1,compte_recurrent = 1,type_fin_recurrent = 1,date_fin_recurrent = None, par_jour = 1, par_mois =  1, date_du_mois =  1, jour_de_semaine = '1',lundi = False, mardi =  False, mercredi = False, jeudi = False, vendredi = False, samedi = False, dimanche =  False, recurrent_id = 0):
        try:
            dao_evenement.est_recurrent = est_recurrent
            dao_evenement.interval_recurrent = interval_recurrent
            dao_evenement.type_recurrent = type_recurrent
            dao_evenement.compte_recurrent = compte_recurrent
            dao_evenement.type_fin_recurrent = type_fin_recurrent
            dao_evenement.date_fin_recurrent = date_fin_recurrent

            dao_evenement.lundi = lundi
            dao_evenement.mardi =  mardi
            dao_evenement.mercredi = mercredi
            dao_evenement.jeudi = jeudi
            dao_evenement.vendredi = vendredi
            dao_evenement.samedi = samedi
            dao_evenement.dimanche =  dimanche

            dao_evenement.par_jour = par_jour
            dao_evenement.par_mois =  par_mois
            dao_evenement.date_du_mois =  date_du_mois
            dao_evenement.jour_de_semaine = jour_de_semaine 
            dao_evenement.recurrent_id = recurrent_id

            return dao_evenement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION RECURRENT(dao_evenement)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_evenement_object):
        try:
            evenement =  Model_Evenement()
            evenement.designation = dao_evenement_object.designation
            evenement.description = dao_evenement_object.description
            evenement.auteur_id = dao_evenement_object.auteur_id
            evenement.type_evenement_id = dao_evenement_object.type_evenement_id
            evenement.local_id = dao_evenement_object.local_id
            evenement.description = dao_evenement_object.description
            #print("confid save {}".format(dao_evenement_object.confidentialite))
            evenement.confidentialite = dao_evenement_object.confidentialite
            evenement.duree = dao_evenement_object.duree
            evenement.journee = dao_evenement_object.journee
            evenement.date_debut = dao_evenement_object.date_debut
            evenement.date_fin = dao_evenement_object.date_fin
            if dao_evenement_object.est_recurrent == True:
                evenement.est_recurrent = dao_evenement_object.est_recurrent
                evenement.recurrent_id = dao_evenement_object.recurrent_id
                evenement.interval_recurrent = dao_evenement_object.interval_recurrent
                evenement.type_recurrent = dao_evenement_object.type_recurrent
                evenement.compte_recurrent = dao_evenement_object.compte_recurrent
                evenement.type_fin_recurrent = dao_evenement_object.type_fin_recurrent
                evenement.date_fin_recurrent = dao_evenement_object.date_fin_recurrent
                evenement.lundi = dao_evenement_object.lundi
                evenement.mardi = dao_evenement_object.mardi
                evenement.mercredi = dao_evenement_object.mercredi
                evenement.jeudi = dao_evenement_object.jeudi
                evenement.vendredi = dao_evenement_object.vendredi
                evenement.samedi = dao_evenement_object.samedi
                evenement.dimanche = dao_evenement_object.dimanche
                evenement.par_jour = dao_evenement_object.par_jour
                evenement.par_mois = dao_evenement_object.par_mois
                evenement.date_du_mois = dao_evenement_object.date_du_mois
                evenement.jour_de_semaine = dao_evenement_object.jour_de_semaine 
            evenement.save()
            return evenement
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_evenement)")
            #print(e)
            return None
        
    @staticmethod
    def toSaveEvent(dao_evenement_object, date_debut, date_fin, duree, list_proprietaire_id, list_rappel_id, list_participant_employe_id, list_participant_email, list_participant_nom):
        try:
            #On remplace ces quelques variables passées en paramètre
            dao_evenement_object.date_debut = date_debut
            dao_evenement_object.date_fin = date_fin
            dao_evenement_object.duree = duree
            #On enregistre l'évènement
            evenement = dao_evenement.toSave(dao_evenement_object)
            #print("Evenement {} cree".format(evenement.id))

            confidentialite = evenement.confidentialite
            # Gestion participant (OneToMany - Creation)
            #print("confidentialite {}".format(confidentialite))
            if confidentialite == 1:
                #print("tout le monde")
                #print("Nombre de ligne {}".format(len(list_participant_nom)))
                for i in range(0, len(list_participant_nom)) :
                    nom = list_participant_nom[i] 
                    email = list_participant_email[i]
                    employe_id = int(list_participant_employe_id[i])
                    if employe_id == "" or employe_id == 0: employe_id = None
                    participant = dao_participant.toCreate(dao_evenement_object.auteur_id, evenement.id, nom, email, employe_id)
                    participant = dao_participant.toSave(participant)
                    #print("participant {} cree".format(participant.id))
            elif confidentialite == 2:
                #print("Employe seulement")
                #print("Nombre de ligne {}".format(len(list_participant_nom)))
                for i in range(0, len(list_participant_nom)) :
                    nom = list_participant_nom[i] 
                    email = list_participant_email[i]
                    employe_id = list_participant_employe_id[i]
                    if employe_id == "" or employe_id == 0: continue
                    participant = dao_participant.toCreate(dao_evenement_object.auteur_id, evenement.id, nom, email, employe_id)
                    participant = dao_participant.toSave(participant)
                    #print("participant {} cree".format(participant.id))	
                    
            #Ajout des rappels (ManyToMany - Creation)
            for i in range(0, len(list_rappel_id)):
                alarme_id = int(list_rappel_id[i])
                alarme = dao_alarme.toGet(alarme_id)
                evenement.rappels.add(alarme)
                #print("rappel {} cree".format(alarme.id))
                
            #Ajout des propriétaires (ManyToMany - Creation)
            for i in range(0, len(list_proprietaire_id)):
                proprietaire_id = int(list_proprietaire_id[i])
                proprietaire = dao_employe.toGetEmploye(proprietaire_id)
                evenement.proprietaires.add(proprietaire)
                #print("propriétaire {} cree".format(proprietaire.id))
            return evenement
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_evenement - toSaveEvent)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_evenement_object):
        try:
            evenement =  Model_Evenement.objects.get(pk = id)
            evenement.designation = dao_evenement_object.designation
            evenement.description = dao_evenement_object.description
            evenement.auteur_id = dao_evenement_object.auteur_id
            evenement.type_evenement_id = dao_evenement_object.type_evenement_id
            evenement.local_id = dao_evenement_object.local_id
            evenement.description = dao_evenement_object.description
            #print("confid update {}".format(dao_evenement_object.confidentialite))
            evenement.confidentialite = dao_evenement_object.confidentialite
            evenement.duree = dao_evenement_object.duree
            evenement.journee = dao_evenement_object.journee
            evenement.date_debut = dao_evenement_object.date_debut
            evenement.date_fin = dao_evenement_object.date_fin
            if dao_evenement_object.est_recurrent == True:
                evenement.est_recurrent = dao_evenement_object.est_recurrent
                evenement.interval_recurrent = dao_evenement_object.interval_recurrent
                evenement.type_recurrent = dao_evenement_object.type_recurrent
                evenement.compte_recurrent = dao_evenement_object.compte_recurrent
                evenement.type_fin_recurrent = dao_evenement_object.type_fin_recurrent
                evenement.date_fin_recurrent = dao_evenement_object.date_fin_recurrent
                evenement.lundi = dao_evenement_object.lundi
                evenement.mardi = dao_evenement_object.mardi
                evenement.mercredi = dao_evenement_object.mercredi
                evenement.jeudi = dao_evenement_object.jeudi
                evenement.vendredi = dao_evenement_object.vendredi
                evenement.samedi = dao_evenement_object.samedi
                evenement.dimanche = dao_evenement_object.dimanche
                evenement.par_jour = dao_evenement_object.par_jour
                evenement.par_mois = dao_evenement_object.par_mois
                evenement.date_du_mois = dao_evenement_object.date_du_mois
                evenement.jour_de_semaine = dao_evenement_object.jour_de_semaine 
            evenement.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_evenement)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_evenement_object):
        try:
            evenement =  Model_Evenement.objects.get(pk = dao_evenement_object.id)
            evenement.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_evenement)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            evenement =  Model_Evenement.objects.get(pk = id)
            return evenement
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_evenement)")
            #print(e)
            return None
        
    @staticmethod
    def toListTypeRecurrents():
        list = []
        for key, value in TypeRecurrent:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeFinRecurrent():
        list = []
        for key, value in TypeFinRecurrent:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListConfidentialites():
        list = []
        for key, value in Confidentialite:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListJoursDelaSemaines():
        list = []
        for key, value in JoursDelaSemaine:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListParMoiss():
        list = []
        for key, value in ParMois:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListParJours():
        list = []
        for key, value in ParJour:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toGenerateRecurrentId():
        evenements = dao_evenement.toList().count()
        total_evenements = evenements + 1		
        numero = "%s%s" % (timezone.now().year, total_evenements)
        numero = int(numero)
        return numero
