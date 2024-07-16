# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_CategorieRegle
from django.utils import timezone

class dao_categorie_regle(object):
    id = 0
    designation = ""
    description = ""
    code = ""
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_CategorieRegle.objects.all().order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, designation, code = "", description = ""):
        try:
            categorie_regle = dao_categorie_regle()
            if auteur_id == 0: auteur_id = None
            categorie_regle.auteur_id = auteur_id
            categorie_regle.designation = designation
            categorie_regle.description = description
            categorie_regle.code = code
            return categorie_regle
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_categorie_regle)")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_categorie_regle_object):
        try:
            categorie_regle =  Model_CategorieRegle()
            categorie_regle.designation = dao_categorie_regle_object.designation
            categorie_regle.auteur_id = dao_categorie_regle_object.auteur_id
            categorie_regle.description = dao_categorie_regle_object.description
            categorie_regle.code = dao_categorie_regle_object.code
            categorie_regle.save()
            return categorie_regle
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_categorie_regle)")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_categorie_regle_object):
        try:
            categorie_regle =  Model_CategorieRegle.objects.get(pk = id)
            categorie_regle.designation = dao_categorie_regle_object.designation
            categorie_regle.description = dao_categorie_regle_object.description
            categorie_regle.code = dao_categorie_regle_object.code
            categorie_regle.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR (dao_categorie_regle)")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_categorie_regle_object):
        try:
            categorie_regle =  Model_CategorieRegle.objects.get(pk = dao_categorie_regle_object.id)
            categorie_regle.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION (dao_categorie_regle)")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            categorie_regle =  Model_CategorieRegle.objects.get(pk = id)
            return categorie_regle
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_categorie_regle)")
            #print(e)
            return None
