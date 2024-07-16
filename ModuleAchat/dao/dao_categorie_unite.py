# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .dao_categorie import dao_categorie
from ErpBackOffice.models import Model_Categorie

class dao_categorie_unite(object):
    @staticmethod
    def toListCategoriesUnite():
        return Model_Categorie.objects.filter(type = "UNITE").order_by("designation")

    @staticmethod
    def toSaveCategorieUnite(auteur, dao_categorie_object):
        dao_categorie_object.auteur_id = auteur.id
        dao_categorie_object.type = "UNITE"
        return dao_categorie.toSaveCategorie(dao_categorie_object)

    @staticmethod
    def toUpdateCategorieUnite(id, dao_categorie_object):
        dao_categorie_object.type = "UNITE"
        return dao_categorie.toUpdateCategorie(id, dao_categorie_object)

    @staticmethod
    def toGetCagorieUnite(id):
        return dao_categorie.toGetCategorie(id)

    @staticmethod
    def toDeleteCagorieUnite(id):
        return dao_categorie.toDeleteCategorie(id)