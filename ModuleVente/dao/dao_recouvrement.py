# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Recouvrement, StatutRecouvrement
from django.utils import timezone

class dao_recouvrement(object):
    id = 0
    designation = ""
    description = ""
    statut_recouvrement = 1
    client_id  =  1
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_Recouvrement.objects.all().order_by("designation")

    @staticmethod
    def togetNombreRecouvrement():
        temps= timezone.now().month
        return  Model_Recouvrement.objects.filter(creation_date__month=temps).count()

    @staticmethod
    def toCreate(auteur_id, designation, statut_recouvrement = 1, client_id  =  None, description = ""):
        try:
            recouvrement = dao_recouvrement()
            if auteur_id == 0: auteur_id = None
            recouvrement.auteur_id = auteur_id
            recouvrement.designation = designation
            recouvrement.description = description
            recouvrement.statut_recouvrement = statut_recouvrement
            if client_id == 0: client_id = None
            recouvrement.client_id = client_id
            return recouvrement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_recouvrement)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_recouvrement_object):
        try:
            recouvrement =  Model_Recouvrement()
            recouvrement.designation = dao_recouvrement_object.designation
            recouvrement.auteur_id = dao_recouvrement_object.auteur_id
            recouvrement.description = dao_recouvrement_object.description
            recouvrement.statut_recouvrement = dao_recouvrement_object.statut_recouvrement
            recouvrement.client_id = dao_recouvrement_object.client_id
            recouvrement.save()
            return recouvrement
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_recouvrement)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_recouvrement_object):
        try:
            recouvrement =  Model_Recouvrement.objects.get(pk = id)
            recouvrement.designation = dao_recouvrement_object.designation
            recouvrement.description = dao_recouvrement_object.description
            recouvrement.statut_recouvrement = dao_recouvrement_object.statut_recouvrement
            recouvrement.client_id = dao_recouvrement_object.client_id
            recouvrement.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_recouvrement)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_recouvrement_object):
        try:
            recouvrement =  Model_Recouvrement.objects.get(pk = dao_recouvrement_object.id)
            recouvrement.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_recouvrement)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            recouvrement =  Model_Recouvrement.objects.get(pk = id)
            return recouvrement
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_recouvrement)")
            #print(e)
            return None
        
    @staticmethod
    def toListStatutRecouvrements():
        list = []
        for key, value in StatutRecouvrement:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
