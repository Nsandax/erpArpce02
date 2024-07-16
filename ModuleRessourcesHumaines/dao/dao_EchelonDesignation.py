# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_EchelonRH


class dao_EchelonDesignation(object):
    id = 0
    designation = ""
    description = ""
   

    @staticmethod
    def toListEchelon():
        return Model_EchelonRH.objects.all().order_by("designation")

    @staticmethod
    def toCreateEchelon(designation, description):
        try:
            echelon = dao_EchelonDesignation()
            echelon.designation = designation
            echelon.description = description
           
            return echelon
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION FONCTION")
            #print(e)
            return None

    @staticmethod
    def toSaveEchelon(dao_echelon_object):
        try:
            echelon = Model_EchelonRH()
            echelon.designation = dao_echelon_object.designation
            echelon.description = dao_echelon_object.description
            echelon.save()
            return echelon
        except Exception as e:
            #print("ERREUR LORS DU SAVE FONCTION")
            #print(e)
            return None

    @staticmethod
    def toUpdateEchelon(id, dao_echelon_object):
        try:
            echelon = Model_EchelonRH.objects.get(pk=id)
            echelon.designation = dao_echelon_object.designation
            echelon.description = dao_echelon_object.description
            
            echelon.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR FONCTION")
            #print(e)
            return False

    @staticmethod
    def toDeleteEchelon(id):
        try:
            echelon = Model_EchelonRH.objects.get(pk=id)
            echelon.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    @staticmethod
    def toGetEchelon(id):
        try:
            echelon = Model_EchelonRH.objects.get(pk=id)
            return echelon
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE FONCTION")
            #print(e)
            return None
