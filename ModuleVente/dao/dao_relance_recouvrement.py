# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_RelanceRecouvrement, TypeRelance
from django.utils import timezone

class dao_relance_recouvrement(object):
    id = 0
    designation = ""
    description = ""
    type_relance = 1
    client_id  =  None
    date_relance = None
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_RelanceRecouvrement.objects.all().order_by("designation")

    @staticmethod
    def togetNombreRelanceRecouvrement():
        temps= timezone.now().month
        return  Model_RelanceRecouvrement.objects.filter(creation_date__month=temps).count()

    @staticmethod
    def toCreate(auteur_id, designation, date_relance = None, type_relance = 1, client_id  =  None, description = ""):
        try:
            relance_recouvrement = dao_relance_recouvrement()
            if auteur_id == 0: auteur_id = None
            relance_recouvrement.auteur_id = auteur_id
            relance_recouvrement.designation = designation
            relance_recouvrement.description = description
            relance_recouvrement.type_relance = type_relance
            if client_id == 0: client_id = None
            relance_recouvrement.client_id = client_id
            relance_recouvrement.date_relance = date_relance
            return relance_recouvrement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_relance_recouvrement)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_relance_recouvrement_object):
        try:
            relance_recouvrement =  Model_RelanceRecouvrement()
            relance_recouvrement.designation = dao_relance_recouvrement_object.designation
            relance_recouvrement.auteur_id = dao_relance_recouvrement_object.auteur_id
            relance_recouvrement.description = dao_relance_recouvrement_object.description
            relance_recouvrement.type_relance = dao_relance_recouvrement_object.type_relance
            relance_recouvrement.client_id = dao_relance_recouvrement_object.client_id
            if dao_relance_recouvrement_object.date_relance != None: relance_recouvrement.date_relance = dao_relance_recouvrement_object.date_relance
            else: relance_recouvrement.date_relance = timezone.now()
            relance_recouvrement.save()
            return relance_recouvrement
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_relance_recouvrement)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_relance_recouvrement_object):
        try:
            relance_recouvrement =  Model_RelanceRecouvrement.objects.get(pk = id)
            relance_recouvrement.designation = dao_relance_recouvrement_object.designation
            relance_recouvrement.description = dao_relance_recouvrement_object.description
            relance_recouvrement.type_relance = dao_relance_recouvrement_object.type_relance
            relance_recouvrement.client_id = dao_relance_recouvrement_object.client_id
            relance_recouvrement.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_relance_recouvrement)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_relance_recouvrement_object):
        try:
            relance_recouvrement =  Model_RelanceRecouvrement.objects.get(pk = dao_relance_recouvrement_object.id)
            relance_recouvrement.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_relance_recouvrement)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            relance_recouvrement =  Model_RelanceRecouvrement.objects.get(pk = id)
            return relance_recouvrement
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_relance_recouvrement)")
            #print(e)
            return None
        
    @staticmethod
    def toListTypeRelance():
        list = []
        for key, value in TypeRelance:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
