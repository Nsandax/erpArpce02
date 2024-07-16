# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_UniteAchatArticle
from django.utils import timezone

class dao_unite_achat_article(object):
    id = 0
    article_id = None
    unite_id = None
    auteur_id = None

    @staticmethod
    def toListUnitesAchatOf(article_id):
        return Model_UniteAchatArticle.objects.filter(article_id = article_id)

    @staticmethod
    def toCreateUniteAchat(article_id, unite_id):
        try:
            unite = dao_unite_achat_article()
            unite.article_id = article_id
            unite.unite_id = unite_id         
            return unite
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'UNITE D'ACHAT")
            #print(e)
            return None

    @staticmethod
    def toUpdateUniteAchat(id, object_dao_unite_achat):
        try:
            unite = Model_UniteAchatArticle.objects.get(pk = id)
            unite.article_id = object_dao_unite_achat.article_id
            unite.unite_id = object_dao_unite_achat.unite_id
            unite.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'UNITE D'ACHAT")
            #print(e)
            return False

    @staticmethod
    def toSaveUniteAchat(auteur, object_dao_unite_achat):
        try:
            unite = Model_UniteAchatArticle()
            unite.article_id = object_dao_unite_achat.article_id
            unite.unite_id = object_dao_unite_achat.unite_id
            #unite.auteur_id = auteur.id
            unite.creation_date = timezone.now()
            unite.save()
            return unite
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE L'UNITE D'ACHAT")
            #print(e)
            return None
    

    @staticmethod
    def toGetUniteAchat(id):
        try:
            return Model_UniteAchatArticle.objects.get(pk = id)
        except Exception as e:
            return None  

    @staticmethod
    def toGetUniteAchatOfArticle(article_id, unite_id):
        try:
            return Model_UniteAchatArticle.objects.filter(article_id = article_id).get(unite_id = unite_id)
        except Exception as e:
            return None

         

    @staticmethod
    def toDeleteUniteAchat(id):
        try:
            unite = Model_UniteAchatArticle.objects.get(pk = id)
            unite.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE L'UNITE D'ACHAT")
            #print(e)
            return False