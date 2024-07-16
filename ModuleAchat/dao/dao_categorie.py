# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Categorie
from django.utils import timezone

class dao_categorie(object):
    id = 0
    designation = ""
    auteur_id = None
    type = ""

    @staticmethod
    def toListCategorie():
        try:
            return Model_Categorie.objects.all()
        except Exception as e:
            return []

    @staticmethod
    def toCreateCategorie(designation):
        try:
            categorie = dao_categorie()
            categorie.designation = designation
            return categorie
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSaveCategorie(dao_categorie_object):
        try:
            categorie = Model_Categorie()
            categorie.designation = dao_categorie_object.designation
            categorie.auteur_id = dao_categorie_object.auteur_id
            categorie.type = dao_categorie_object.type
            categorie.creation_date = timezone.now()
            categorie.save()
            return categorie
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None


    @staticmethod
    def toUpdateCategorie(id, dao_categorie_object):
        try:
            categorie = Model_Categorie.objects.get(pk = id)
            categorie.designation = dao_categorie_object.designation
            categorie.type = dao_categorie_object.type
            categorie.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False


    @staticmethod
    def toDeleteCategorie(dao_categorie_object):
        try:
            categorie = Model_Categorie.objects.get(pk = dao_categorie_object.id)
            categorie.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False


    @staticmethod
    def toGetCategorie(id):
        try:
            categorie = Model_Categorie.objects.get(pk = id)
            return categorie
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None