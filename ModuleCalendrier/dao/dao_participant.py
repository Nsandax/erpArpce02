# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Participant, StatutParticipation, Disponibilite
from django.utils import timezone

class dao_participant(object):
    id = 0
    nom_complet = ""
    email = ""
    employe_id = None
    evenement_id = None
    description = ""
    statut_participation = 1
    disponibilite  =  1
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_Participant.objects.all().order_by("email")
    
    @staticmethod
    def toCreate(auteur_id, evenement_id, nom_complet = "", email = "", employe_id = None, statut_participation = 1, disponibilite  =  1, description = ""):
        try:
            participant = dao_participant()
            if auteur_id == 0: auteur_id = None
            participant.auteur_id = auteur_id
            if evenement_id == 0: evenement_id = None
            participant.evenement_id = evenement_id
            if employe_id == 0: employe_id = None
            participant.employe_id = employe_id
            participant.nom_complet = nom_complet
            participant.email = email
            participant.description = description
            participant.statut_participation = statut_participation
            participant.disponibilite = disponibilite
            return participant
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_participant)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_participant_object):
        try:
            participant =  Model_Participant()
            participant.nom_complet = dao_participant_object.nom_complet
            participant.email = dao_participant_object.email
            participant.auteur_id = dao_participant_object.auteur_id
            participant.evenement_id = dao_participant_object.evenement_id
            participant.employe_id = dao_participant_object.employe_id
            participant.description = dao_participant_object.description
            participant.statut_participation = dao_participant_object.statut_participation
            participant.disponibilite = dao_participant_object.disponibilite
            participant.save()
            return participant
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_participant)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_participant_object):
        try:
            participant =  Model_Participant.objects.get(pk = id)
            participant.nom_complet = dao_participant_object.nom_complet
            participant.email = dao_participant_object.email
            participant.auteur_id = dao_participant_object.auteur_id
            participant.evenement_id = dao_participant_object.evenement_id
            participant.employe_id = dao_participant_object.employe_id
            participant.description = dao_participant_object.description
            participant.statut_participation = dao_participant_object.statut_participation
            participant.disponibilite = dao_participant_object.disponibilite
            participant.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_participant)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_participant_object):
        try:
            participant =  Model_Participant.objects.get(pk = dao_participant_object.id)
            participant.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_participant)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            participant =  Model_Participant.objects.get(pk = id)
            return participant
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_participant)")
            #print(e)
            return None
        
    @staticmethod
    def toListStatutParticipations():
        list = []
        for key, value in StatutParticipation:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypesDisponibilites():
        list = []
        for key, value in Disponibilite:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
