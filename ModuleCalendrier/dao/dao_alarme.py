# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Alarme, TypeIntervalle, TypeAlarme
from django.utils import timezone

class dao_alarme(object):
    id = 0
    designation = ""
    description = ""
    type_intervalle = 1
    type_alarme  =  1
    temps  =  1
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_Alarme.objects.all().order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, designation, type_intervalle = 1, type_alarme  =  1, temps  =  1, description = ""):
        try:
            alarme = dao_alarme()
            if auteur_id == 0: auteur_id = None
            alarme.auteur_id = auteur_id
            alarme.designation = designation
            alarme.description = description
            alarme.type_intervalle = type_intervalle
            alarme.type_alarme = type_alarme
            alarme.temps = temps
            return alarme
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_alarme)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_alarme_object):
        try:
            alarme =  Model_Alarme()
            alarme.designation = dao_alarme_object.designation
            alarme.auteur_id = dao_alarme_object.auteur_id
            alarme.description = dao_alarme_object.description
            alarme.type_intervalle = dao_alarme_object.type_intervalle
            alarme.type_alarme = dao_alarme_object.type_alarme
            alarme.temps = dao_alarme_object.temps
            alarme.save()
            return alarme
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_alarme)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_alarme_object):
        try:
            alarme =  Model_Alarme.objects.get(pk = id)
            alarme.designation = dao_alarme_object.designation
            alarme.description = dao_alarme_object.description
            alarme.type_intervalle = dao_alarme_object.type_intervalle
            alarme.type_alarme = dao_alarme_object.type_alarme
            alarme.temps = dao_alarme_object.temps
            alarme.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_alarme)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_alarme_object):
        try:
            alarme =  Model_Alarme.objects.get(pk = dao_alarme_object.id)
            alarme.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_alarme)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            alarme =  Model_Alarme.objects.get(pk = id)
            return alarme
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_alarme)")
            #print(e)
            return None

    @staticmethod
    def toListTypeIntervalles():
        list = []
        for key, value in TypeIntervalle:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeAlarme():
        list = []
        for key, value in TypeAlarme:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list