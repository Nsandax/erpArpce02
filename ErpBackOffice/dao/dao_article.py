# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Article, Model_TypeArticle
from django.utils import timezone

class dao_article(object):
    id = 0
    image	= ""
    designation = ""
    designation_court = ""	
    code_article = ""		
    code_barre	= ""
    type_article = 0		
    prix_unitaire = 0		
    est_achetable = True
    est_vendable = True
    compte_id = None
    auteur_id = 0

    @staticmethod
    def toListArticles():
        return Model_Article.objects.all()
    
    @staticmethod
    def toListArticlesNonService():
        return Model_Article.objects.exclude(type_article = 2)
    
    @staticmethod
    def toListArticlesAchetables():
        return Model_Article.objects.filter(est_achetable = True).order_by("designation")

    @staticmethod
    def toListArticlesVendables():
        return Model_Article.objects.filter(est_vendable = True).order_by("designation")

    @staticmethod
    def toCreateArticle(image, designation, designation_court, code_article,code_barre, est_achetable, est_vendable, compte_id):        
        try:
            article = dao_article()
            article.designation = designation
            article.unite_id = unite_id
            article.est_vendable = est_vendable
            article.est_achetable = est_achetable
            
            article.est_amortissable = est_amortissable
            if image != None:
                article.image = image
            if designation_court != None:
                article.designation_court = designation_court
            if code_article != None:
                article.code_article = code_article
            if code_barre != None:
                article.code_barre = code_barre
            if prix_unitaire != 0 :
                article.prix_unitaire = prix_unitaire
            if compte_id != 0:
                article.compte_id = compte_id
            return article
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toSaveArticle(auteur, object_dao_article):
        try:
            article = Model_Article()
            article.designation = object_dao_article.designation
            article.image = object_dao_article.image
            article.est_achetable = object_dao_article.est_achetable
            article.est_vendable = object_dao_article.est_fabriquable
            article.designation_court = object_dao_article.designation_court
            article.code_article = object_dao_article.code_article
            article.code_barre = object_dao_article.code_barre
            article.type_article = object_dao_article.type_article
            article.prix_unitaire = object_dao_article.prix_unitaire
            article.compte_id = object_dao_article.compte_id
            article.auteur_id = auteur.id
            article.creation_date = timezone.now()
            article.save()
            return article
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE L'ARTICLE")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateArticle(id, object_dao_article):
        try:
            article = Model_Article.objects.get(pk = id)
            article.designation = object_dao_article.designation
            article.image = object_dao_article.image
            article.est_achetable = object_dao_article.est_achetable
            article.est_vendable = object_dao_article.est_fabriquable
            article.designation_court = object_dao_article.designation_court
            article.code_article = object_dao_article.code_article
            article.code_barre = object_dao_article.code_barre
            article.type_article = object_dao_article.type_article
            article.prix_unitaire = object_dao_article.prix_unitaire
            article.compte_id = object_dao_article.compte_id
            article.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'ARTICLE")
            #print(e)
            return False
  
    @staticmethod
    def toUpdateCompteofArticle(id, compte_id):
        try:
            article = Model_Article.objects.get(pk = id)
            article.compte_id = compte_id
            article.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'ARTICLE")
            #print(e)
            return False

    @staticmethod
    def toGetArticle(id):
        try:
            #print("this is the id", id)
            #print("I'm here bro")
            article =  Model_Article.objects.get(pk = id)
            return article
        except Exception as e:
            #print("erreur", e)
            return None        

    @staticmethod
    def toDeleteArticle(id):
        try:
            article = Model_Article.objects.get(pk = id)
            article.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DE L'ARTICLE")
            #print(e)
            return False
        					
            