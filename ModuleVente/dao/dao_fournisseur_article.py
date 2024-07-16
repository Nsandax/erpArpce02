# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_FournisseurArticle
from django.utils import timezone
from ErpBackOffice.models import Model_Article

class dao_fournisseur_article(object):
    id = 0
    article_id = 0
    fournisseur_id = 0
    auteur_id = 0
    quantite_minimale = 0
    prix_unitaire = 0

    @staticmethod
    def toListFournisseursOf(article_id):
        return Model_FournisseurArticle.objects.filter(article_id = article_id)

    @staticmethod
    def toCreateFournisseurArticle(article_id, fournisseur_id, prix_unitaire, quantite_minimale = 0):
        try:
            fournisseur_article = dao_fournisseur_article()
            fournisseur_article.article_id = article_id
            fournisseur_article.fournisseur_id = fournisseur_id
            fournisseur_article.prix_unitaire = prix_unitaire
            if quantite_minimale != 0 : fournisseur_article.quantite_minimale = quantite_minimale
            return fournisseur_article
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU FOURNISSEUR ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toUpdateFournisseurArticle(id, object_dao_fournisseur_article):
        try:
            fournisseur_article = Model_FournisseurArticle.objects.get(pk = id)
            fournisseur_article.article_id = object_dao_fournisseur_article.article_id
            fournisseur_article.fournisseur_id = object_dao_fournisseur_article.fournisseur_id
            fournisseur_article.prix_unitaire = object_dao_fournisseur_article.prix_unitaire
            fournisseur_article.quantite_minimale = object_dao_fournisseur_article.quantite_minimale
            fournisseur_article.save()
            return fournisseur_article
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU FOURNISSEUR ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toSaveFournisseurArticle(auteur, object_dao_fournisseur_article):
        try:
            fournisseur_article = Model_FournisseurArticle()
            fournisseur_article.article_id = object_dao_fournisseur_article.article_id
            fournisseur_article.fournisseur_id = object_dao_fournisseur_article.fournisseur_id
            fournisseur_article.prix_unitaire = object_dao_fournisseur_article.prix_unitaire
            fournisseur_article.quantite_minimale = object_dao_fournisseur_article.quantite_minimale
            fournisseur_article.auteur_id = auteur.id
            fournisseur_article.creation_date = timezone.now()
            fournisseur_article.save()
            return fournisseur_article
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DU FOURNISSEUR ARTICLE")
            #print(e)
            return None


    @staticmethod
    def toGetFournisseurArticle(id):
        try:
            return Model_FournisseurArticle.objects.get(pk = id)
        except Exception:
            return None

    @staticmethod
    def toGetFournisseurArticleOf(article_id, fournisseur_id):
        try:
            return Model_FournisseurArticle.objects.filter(article_id = article_id).get(fournisseur_id = fournisseur_id)
        except Exception:
            return None

    @staticmethod
    def toDeleteFournisseurArticle(id):
        try:
            fournisseur_article = Model_FournisseurArticle.objects.get(pk = id)
            fournisseur_article.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU FOURNISSEUR ARTICLE")
            #print(e)
            return False

    @staticmethod
    def toListefournisseurArticle():
        try:
            ListeFourByArticle = []
            ListeArticle = Model_Article.objects.all()
            for item in ListeArticle:
                ListeFourByArticle.append(dao_fournisseur_article.toListFournisseursOf(item.id))

            #print('Liste des Four By Articles %s' %ListeFourByArticle)
            return ListeFourByArticle
        except Exception as e:
            #print("Erreur lors d\'insertion liste Fournisseur by Article")
            #print(e)
            return  False