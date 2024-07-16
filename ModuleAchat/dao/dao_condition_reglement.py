# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_ConditionReglement
from django.utils import timezone

class dao_condition_reglement(object):
    id = 0
    designation = ""
    nombre_jours = 0
    auteur_id = None

    @staticmethod
    def toListConditionsReglement():
        return Model_ConditionReglement.objects.all().order_by("nombre_jours")

    @staticmethod
    def toCreateConditionReglement(designation, nombre_jours):        
        try:
            condition = dao_condition_reglement()
            condition.designation = designation
            condition.nombre_jours = nombre_jours
            return condition
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE LA CONDITION")
            #print(e)
            return None

    @staticmethod
    def toSaveConditionReglement(auteur, object_dao_condition_reglement):
        try:
            condition = Model_ConditionReglement()
            condition.designation = object_dao_condition_reglement.designation
            condition.nombre_jours = object_dao_condition_reglement.nombre_jours
            condition.auteur_id = auteur.id
            condition.creation_date = timezone.now()
            condition.save()
            return condition
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE LA CONDITION")
            #print(e)
            return None
        

    @staticmethod
    def toUpdateConditionReglement(id, object_dao_condition_reglement):
        try:
            condition = Model_ConditionReglement.objects.get(pk = id)
            condition.designation = object_dao_condition_reglement.designation
            condition.nombre_jours = object_dao_condition_reglement.nombre_jours
            #print(object_dao_condition_reglement.designation," toUpdateConditionReglement ",object_dao_condition_reglement.nombre_jours)
            condition.save()
            #print(condition)
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE LA CONDITION")
            #print(e)
            return False
  
    @staticmethod
    def toGetConditionReglement(id):
        try:
            return Model_ConditionReglement.objects.get(pk = id)
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return False

    @staticmethod
    def toGetConditionReglementImmediat():
        try:
            return Model_ConditionReglement.objects.get(nombre_jours = 0)
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return False

    @staticmethod
    def toDeleteConditionReglement(id):
        try:
            condition = Model_ConditionReglement.objects.get(pk = id)
            condition.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE LA CONDITION")
            #print(e)
            return False
        					
            