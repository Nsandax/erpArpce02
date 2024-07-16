# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_TypeStructure, TypeSalaire, HorairePaye
from django.utils import timezone

class dao_type_structure(object):
    id = 0
    designation = ""
    description = ""
    type_salaire = 1
    horaire_paye  =  1
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_TypeStructure.objects.all().order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, designation, type_salaire = 1, horaire_paye  =  1, description = ""):
        try:
            type_structure = dao_type_structure()
            type_structure.auteur_id = auteur_id
            type_structure.designation = designation
            type_structure.description = description
            type_structure.type_salaire = type_salaire
            type_structure.horaire_paye = horaire_paye
            return type_structure
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_type_structure)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_type_structure_object):
        try:
            type_structure =  Model_TypeStructure()
            type_structure.designation = dao_type_structure_object.designation
            type_structure.auteur_id = dao_type_structure_object.auteur_id
            type_structure.description = dao_type_structure_object.description
            type_structure.type_salaire = dao_type_structure_object.type_salaire
            type_structure.horaire_paye = dao_type_structure_object.horaire_paye
            type_structure.save()
            return type_structure
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_type_structure)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_type_structure_object):
        try:
            type_structure =  Model_TypeStructure.objects.get(pk = id)
            type_structure.designation = dao_type_structure_object.designation
            type_structure.description = dao_type_structure_object.description
            type_structure.type_salaire = dao_type_structure_object.type_salaire
            type_structure.horaire_paye = dao_type_structure_object.horaire_paye
            type_structure.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_type_structure)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_type_structure_object):
        try:
            type_structure =  Model_TypeStructure.objects.get(pk = dao_type_structure_object.id)
            type_structure.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_type_structure)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            type_structure =  Model_TypeStructure.objects.get(pk = id)
            return type_structure
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_type_structure)")
            #print(e)
            return None
        
    @staticmethod
    def toListTypeSalaire():
        list = []
        for key, value in TypeSalaire:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListHorairePaye():
        list = []
        for key, value in HorairePaye:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
