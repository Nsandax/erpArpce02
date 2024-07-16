# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Bareme
from django.utils import timezone

class dao_bareme(object):
    id = 0
    designation = ""
    type = ""
    reference = ""
    devise_id = 0
    auteur_id = 0

    @staticmethod
    def toList():
        return Model_Bareme.objects.all().order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, designation, devise_id, reference = "", type = ""):
        try:
            bareme = dao_bareme()
            bareme.auteur_id = auteur_id
            bareme.designation = designation
            bareme.reference = reference
            bareme.type = type
            bareme.devise_id = devise_id
            return bareme
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_bareme_object):
        try:
            bareme = Model_Bareme()
            bareme.designation = dao_bareme_object.designation
            bareme.auteur_id = dao_bareme_object.auteur_id
            bareme.reference = dao_bareme_object.reference
            bareme.type = dao_bareme_object.type
            bareme.devise_id = dao_bareme_object.devise_id
            bareme.creation_date = timezone.now()
            bareme.save()
            return bareme
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_bareme_object):
        try:
            bareme = Model_Bareme.objects.get(pk = id)
            bareme.designation = dao_bareme_object.designation
            bareme.reference = dao_bareme_object.reference
            bareme.type = dao_bareme_object.type
            bareme.devise_id = dao_bareme_object.devise_id
            bareme.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_bareme_object):
        try:
            bareme = Model_Bareme.objects.get(pk = dao_bareme_object.id)
            bareme.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            bareme = Model_Bareme.objects.get(pk = id)
            return bareme
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None