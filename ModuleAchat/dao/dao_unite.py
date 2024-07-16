# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Unite

class dao_unite(object):
    id = 0
    designation = ""
    symbole_unite = ""
    est_systeme = False
    categorie_unite_id = 0
    auteur_id = 0

    @staticmethod
    def toListUnite():
        return Model_Unite.objects.all().order_by("designation")

    @staticmethod
    def toCreateUnite(designation, symbole_unite, est_systeme, categorie_unite_id):
        try:
            unite = dao_unite()
            unite.designation = designation
            unite.symbole_unite = symbole_unite
            unite.est_systeme = est_systeme
            unite.categorie_unite_id = categorie_unite_id
            if est_systeme != False :
                unite.est_systeme = True           
            return unite
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toUpdateUnite(id, object_dao_unite):
        try:
            unite = Model_Unite.objects.get(pk = id)
            unite.designation = object_dao_unite.designation
            unite.symbole_unite = object_dao_unite.symbole_unite
            unite.est_systeme = object_dao_unite.est_systeme
            unite.categorie_unite_id = object_dao_unite.categorie_unite_id
            unite.auteur_id = object_dao_unite.auteur_id
            unite.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'UNITE")
            #print(e)
            return False

    @staticmethod
    def toSaveUnite(auteur, object_dao_unite):

        try:
            unite = Model_Unite()
            unite.designation = object_dao_unite.designation
            unite.designation = object_dao_unite.designation
            unite.symbole_unite = object_dao_unite.symbole_unite
            unite.est_systeme = object_dao_unite.est_systeme
            unite.categorie_unite_id = object_dao_unite.categorie_unite_id
            unite.auteur_id = auteur.id
            unite.save()
            return unite
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE L'UNITE")
            #print(e)
            return None
    

    @staticmethod
    def toGetUnite(id):
        try:
            return Model_Unite.objects.get(pk = id)
        except Exception as e:
            return None        

    @staticmethod
    def toDeleteUnite(id):
        try:
            unite = Model_Unite.objects.get(pk = id)
            unite.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE L'UNITE")
            #print(e)
            return False

    @staticmethod
    def toGetUniteName(name):
        try:
            return Model_Unite.objects.filter(designation__icontains = name).first()
        except Exception as e:
            return None  