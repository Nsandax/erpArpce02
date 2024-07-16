# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_CategorieRH


class dao_categorieDesignation(object):
    id = 0
    designation = ""
    description = ""


    @staticmethod
    def toListcategories():
        return Model_CategorieRH.objects.all().order_by("designation")

    @staticmethod
    def toCreateCategorie(designation, description):
        try:
            categorie = dao_categorieDesignation()
            categorie.designation = designation
            categorie.description = description

            return categorie
        except Exception as e:
            # print("ERREUR LORS DE LA CREATION CATEGORIE")
            # print(e)
            return None

    @staticmethod
    def toSaveCategorie(dao_categorie_object):
        try:
            categorie = Model_CategorieRH()
            categorie.designation = dao_categorie_object.designation
            categorie.description = dao_categorie_object.description
            categorie.save()
            return categorie
        except Exception as e:
            # print("ERREUR LORS DU SAVE CATEGORIE")
            # print(e)
            return None

    @staticmethod
    def toUpdateCategorie(id, dao_categorie_object):
        try:
            categorie = Model_CategorieRH.objects.get(pk=id)
            categorie.designation = dao_categorie_object.designation
            categorie.description = dao_categorie_object.description

            categorie.save()
            return True
        except Exception as e:
            # print("ERREUR LORS DE MISE A JOUR CATEGORIE")
            # print(e)
            return False

    @staticmethod
    def toDeleteCategorie(id):
        try:
            categorie = Model_CategorieRH.objects.get(pk=id)
            categorie.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    @staticmethod
    def toGetCategorie(id):
        try:
            categorie = Model_CategorieRH.objects.get(pk=id)
            return categorie
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE FONCTION")
            #print(e)
            return None


    @staticmethod
    def toGetOrCreateCategorie(libelle):
        try:
            # print('CATEGORIE CHECKIN', libelle)
            categorie = Model_CategorieRH.objects.filter(designation__icontains = libelle).first()

            if categorie == None:
                # print('GET IN CATEGORIE CREATE')
                uncat = dao_categorieDesignation()
                categorie = uncat.toCreateCategorie(libelle, "")
                categorie = uncat.toSaveCategorie(categorie)
            return categorie
        except Exception as e:
            # print("Error toGetOrCreateCategorie", e)
            return None
