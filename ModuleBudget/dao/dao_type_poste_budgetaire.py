# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_TypeArticle
from django.utils import timezone

class dao_type_article(object):
    id = 0
    nature =""
    est_stockable=False
    est_amortissable=False
    duree_amortissement=""
    auteur_id = 0

    @staticmethod
    def toListTypeArticles():
        return Model_TypesArticle.objects.all().order_by('-id')

    @staticmethod
    def toListArticlesDeNature(nature_article):
        return Model_Article.objects.filter(nature = nature_article)

    @staticmethod
    def toListTypeArticlesAmortissables():
        return Model_Article.objects.filter(est_amortissable = True)

    @staticmethod
    def toListArticlesStockables():
        return Model_Article.objects.filter(est_stockable = True)

    @staticmethod
    def toCreateTypeArticle(nature, est_stockable,est_amortissable,duree_amortissement):
        try:
            typearticle = dao_dao_type_articlearticle()
            typearticle.nature = nature
            typearticle.est_stockable = est_stockable
            typearticle.est_amortissable = est_amortissable
            typearticle.duree_amortissement = duree_amortissement


        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU TYPE D'ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toSaveArticle(auteur, object_dao_type_article):
        try:
            typearticle = Model_TypeArticle()
            typearticle.nature = object_dao_type_article.nature
            typearticle.est_amortissable = object_dao_type_article.est_amortissable
            typearticle.est_stockable = object_dao_type_article.est_stockable
            typearticle.duree_amortissement = object_dao_type_article.duree_amortissement
            typearticle.creation_date = timezone.now()
            typearticle.auteur_id = auteur.id
            typearticle.save()
            return typearticle
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT Du TYPE 'ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toUpdateArticle(id, object_dao_type_article):
        try:
            typearticle = Model_TypeArticle.objects.get(pk = id)
            typearticle.nature = object_dao_type_article.nature
            typearticle.est_amortissable = object_dao_type_article.est_amortissable
            typearticle.est_stockable = object_dao_type_article.est_stockable
            typearticle.duree_amortissement = object_dao_type_article.duree_amortissement
            typearticle.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'ARTICLE")
            #print(e)
            return False

    @staticmethod
    def toGetTypeArticle(id):
        try:
            return Model_TypeArticle.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteTypeArticle(id):
        try:
            typearticle = Model_TypeArticle.objects.get(pk = id)
            typearticle.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE L'ARTICLE")
            #print(e)
            return False

