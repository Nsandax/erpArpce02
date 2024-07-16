# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import *
from django.utils import timezone

class dao_constante(object):
    id = 0
    designation             =    ""
    reference               =    ""
    description             =    ""
    code                    =    ""
    auteur_id               =    None
    type_constant           =    1
    base_test               =    0.0
    base_test_is_const      =    False
    base_test_const_id      =    None
    rubrique_id             =    None
    valeur                  =    0.0
    valeur_is_const         =    False
    valeur_const_id         =    None
    devise_id               =    None

    
    @staticmethod
    def toList():
        return  Model_Constante.objects.all().order_by("id")
    
    @staticmethod
    def toCreate(auteur_id, designation, reference = "", code = "", description = "", type_constant  =  1, base_test = 0.0, base_test_is_const = False, base_test_const_id = None, rubrique_id = None, valeur = 0.0, valeur_is_const = False, valeur_const_id = None, devise_id = None):
        try:
            constante = dao_constante()
            if auteur_id == 0: auteur_id = None 
            constante.auteur_id               =    auteur_id
            constante.designation             =    designation
            constante.description             =    description
            constante.code                    =    code
            constante.reference               =    reference
            constante.type_constant           =    type_constant
            constante.base_test               =    base_test
            constante.base_test_is_const      =    base_test_is_const
            constante.base_test_const_id      =    base_test_const_id
            constante.rubrique_id             =    rubrique_id
            constante.valeur                  =    valeur
            constante.valeur_is_const         =    valeur_is_const
            constante.valeur_const_id         =    valeur_const_id
            constante.devise_id               =    devise_id
            return constante
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_constante)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_constante_object):
        try:
            constante =  Model_Constante()
            constante.designation             =    dao_constante_object.designation
            constante.auteur_id               =    dao_constante_object.auteur_id
            constante.description             =    dao_constante_object.description
            constante.code                    =    dao_constante_object.code
            constante.reference               =    dao_constante_object.reference
            constante.type_constant           =    dao_constante_object.type_constant
            constante.base_test               =    dao_constante_object.base_test
            constante.base_test_is_const      =    dao_constante_object.base_test_is_const
            constante.base_test_const_id      =    dao_constante_object.base_test_const_id
            constante.rubrique_id             =    dao_constante_object.rubrique_id
            constante.valeur                  =    dao_constante_object.valeur
            constante.valeur_is_const         =    dao_constante_object.valeur_is_const
            constante.valeur_const_id         =    dao_constante_object.valeur_const_id
            constante.devise_id               =    dao_constante_object.devise_id
            constante.save()
            return constante
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_constante)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_constante_object):
        try:
            constante                         =  Model_Constante.objects.get(pk = id)
            constante.designation             =    dao_constante_object.designation
            constante.description             =    dao_constante_object.description
            constante.code                    =    dao_constante_object.code
            constante.reference               =    dao_constante_object.reference
            constante.type_constant           =    dao_constante_object.type_constant
            constante.base_test               =    dao_constante_object.base_test
            constante.base_test_is_const      =    dao_constante_object.base_test_is_const
            constante.base_test_const_id      =    dao_constante_object.base_test_const_id
            constante.rubrique_id             =    dao_constante_object.rubrique_id
            constante.valeur                  =    dao_constante_object.valeur
            constante.valeur_is_const         =    dao_constante_object.valeur_is_const
            constante.valeur_const_id         =    dao_constante_object.valeur_const_id
            constante.devise_id               =    dao_constante_object.devise_id
            constante.save()
            return True, constante 
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_constante)")
            #print(e)
            return False, None

    
    @staticmethod
    def toDelete(dao_constante_object):
        try:
            constante =  Model_Constante.objects.get(pk = dao_constante_object.id)
            constante.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_constante)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            constante =  Model_Constante.objects.get(pk = id)
            return constante
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_constante)")
            #print(e)
            return None
        
    @staticmethod
    def toGetByCode(code):
        try:
            constante =  Model_Constante.objects.get(code__iexact = code)
            return constante
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_constante)")
            #print(e)
            return None
    
    @staticmethod
    def toListTypeConstante():
        list = []
        for key, value in TypeConstante:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeOperationCalcul():
        list = []
        for key, value in TypeOperationCalcul:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeOperationTest():
        list = []
        for key, value in TypeOperationTest:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
    
    @staticmethod
    def toListTypeConditionTest():
        list = []
        for key, value in TypeConditionTest:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list
