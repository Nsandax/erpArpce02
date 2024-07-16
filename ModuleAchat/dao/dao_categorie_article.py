# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .dao_categorie import dao_categorie
from ErpBackOffice.models import Model_Categorie

class dao_categorie_article(object):
    @staticmethod
    def toListCategoriesArticle():
        return Model_Categorie.objects.filter(type = "ARTICLE").order_by("designation")

    @staticmethod
    def toSaveCategorieArticle(auteur, dao_categorie_object):
        dao_categorie_object.auteur_id = auteur.id
        dao_categorie_object.type = "ARTICLE"
        return dao_categorie.toSaveCategorie(dao_categorie_object)

    @staticmethod
    def toUpdateCategorieArticle(id, dao_categorie_object):
        dao_categorie_object.type = "ARTICLE"
        return dao_categorie.toUpdateCategorie(id, dao_categorie_object)

    @staticmethod
    def toGetCagorieArticle(id):
        return dao_categorie.toGetCategorie(id)

    @staticmethod
    def toDeleteCagorieArticle(id):
        return dao_categorie.toDeleteCategorie(id)

    @staticmethod
    def toGetCagorieArticlebyid(id):
        return dao_categorie.objects.get(pk=id)

    @staticmethod
    def toGetCagorieArticlebyname(name):
        return Model_Categorie.objects.filter(designation__icontains = name).first()