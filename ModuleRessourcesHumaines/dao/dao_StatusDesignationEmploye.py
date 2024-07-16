
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_StatusRH


class dao_StatusDesignationEmploye(object):
    id = 0
    designation = ""
    description = ""
    etat = ""
   

    @staticmethod
    def toListStatuts():
        return Model_StatusRH.objects.all().order_by("designation")

    @staticmethod
    def toCreateStatut(designation, description,etat):
        try:
            Statut = dao_StatusDesignationEmploye()
            Statut.designation = designation
            Statut.description = description
            Statut.etat = etat
           
            return Statut
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION FONCTION")
            #print(e)
            return None

    @staticmethod
    def toSaveStatut(dao_Statut_object):
        try:
            Statut = Model_StatusRH()
            Statut.designation = dao_Statut_object.designation
            Statut.description = dao_Statut_object.description
            Statut.etat = dao_Statut_object.etat
            Statut.save()
            return Statut
        except Exception as e:
            #print("ERREUR LORS DU SAVE FONCTION")
            #print(e)
            return None

    @staticmethod
    def toUpdateStatut(id, dao_Statut_object):
        try:
            Statut = Model_StatusRH.objects.get(pk=id)
            Statut.designation = dao_Statut_object.designation
            Statut.description = dao_Statut_object.description
            Statut.etat = dao_Statut_object.etat
            Statut.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR FONCTION")
            #print(e)
            return False

    @staticmethod
    def toDeleteStatut(id):
        try:
            Statut = Model_StatusRH.objects.get(pk=id)
            Statut.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    @staticmethod
    def toGetStatut(id):
        try:
            Statut = Model_StatusRH.objects.get(pk=id)
            return Statut
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE FONCTION")
            #print(e)
            return None
