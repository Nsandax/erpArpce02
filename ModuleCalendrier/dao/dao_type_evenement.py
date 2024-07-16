# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_TypeEvenement
from django.utils import timezone

class dao_type_evenement(object):
    id = 0
    designation = ""
    description = ""
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_TypeEvenement.objects.all().order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, designation, description = ""):
        try:
            type_evenement = dao_type_evenement()
            if auteur_id == 0: auteur_id = None
            type_evenement.auteur_id = auteur_id
            type_evenement.designation = designation
            type_evenement.description = description
            return type_evenement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_type_evenement)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_type_evenement_object):
        try:
            type_evenement =  Model_TypeEvenement()
            type_evenement.designation = dao_type_evenement_object.designation
            type_evenement.auteur_id = dao_type_evenement_object.auteur_id
            type_evenement.description = dao_type_evenement_object.description
            type_evenement.save()
            return type_evenement
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_type_evenement)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_type_evenement_object):
        try:
            type_evenement =  Model_TypeEvenement.objects.get(pk = id)
            type_evenement.designation = dao_type_evenement_object.designation
            type_evenement.description = dao_type_evenement_object.description
            type_evenement.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_type_evenement)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_type_evenement_object):
        try:
            type_evenement =  Model_TypeEvenement.objects.get(pk = dao_type_evenement_object.id)
            type_evenement.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_type_evenement)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            type_evenement =  Model_TypeEvenement.objects.get(pk = id)
            return type_evenement
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_type_evenement)")
            #print(e)
            return None
