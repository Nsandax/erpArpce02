# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Article
from ErpBackOffice.models import Model_Unite_fonctionnelle
from django.utils import timezone

class dao_article(object):
    id = 0
    image	= ""
    designation = ""
    designation_court = ""
    code_article = ""
    code_barre	= ""
    type_article = None
    categorie_id = None
    unite_id = None
    prix_unitaire = 0
    est_vendable = True
    est_achetable = True
    est_manufacturable = True
    est_fabriquable = False
    est_amortissable = False
    compte_id = None
    auteur_id = 0
    unite_fonctionnelle_id = None

    @staticmethod
    def toListArticles():
        return Model_Article.objects.all().order_by('-id')

    @staticmethod
    def toListArticlesByAuteur(user_id):
        return Model_Article.objects.filter(auteur_id=user_id)

    @staticmethod
    def toListArticlesOfServiceReferent(service_ref_id):
        #print("aba")
        #print(service_ref_id)
        return Model_Article.objects.filter(unite_fonctionnelle_id = service_ref_id)

    @staticmethod
    def toListArticlesAchetablesOfServiceReferent(service_ref_id):
        return Model_Article.objects.filter(est_achetable = True).filter(unite_fonctionnelle_id = service_ref_id)

    @staticmethod
    def toListArticlesStockablesOfServiceReferent(service_ref_id):
        return Model_Article.objects.filter(est_stockable = True).filter(unite_fonctionnelle_id = service_ref_id)
    @staticmethod
    def toListArticlesVendablesOfServiceReferent(service_ref_id):
        return Model_Article.objects.filter(est_vendable = True).filter(unite_fonctionnelle_id = service_ref_id)
    @staticmethod
    def toListArticlesManufacturablesOfServiceReferent(service_ref_id):
        return Model_Article.objects.filter(est_manufacturable = True).filter(unite_fonctionnelle_id = service_ref_id)
    @staticmethod
    def toListArticlesAmortissablesOfServiceReferent(service_ref_id):
        return Model_Article.objects.filter(est_amortissable = True).filter(unite_fonctionnelle_id = service_ref_id)


    @staticmethod
    def toListArticlesOfServiceReferentByAuteur(service_ref_id, user_id):
        #print("aba")
        #print(service_ref_id)
        return Model_Article.objects.filter(unite_fonctionnelle_id = service_ref_id).filter(auteur_id=user_id)

    @staticmethod
    def toListArticlesOfEmplacementService(emplacement_id):
        return Model_Article.objects.filter(unite_fonctionnelle__emplacement_id = emplacement_id)

    @staticmethod
    def toListArticlesOfEmplacementServiceByAuteur(emplacement_id, user_id):
        return Model_Article.objects.filter(unite_fonctionnelle__emplacement_id = emplacement_id).filter(auteur_id = user_id)

    @staticmethod
    def toListArticlesDuType(type_article):
        return Model_Article.objects.filter(type_article = type_article).order_by("designation")

    @staticmethod
    def toListArticlesDuTypeByAuteur(type_article, user_id):
        return Model_Article.objects.filter(type_article = type_article).order_by("designation").filter(auteur_id=user_id)

    @staticmethod
    def toListArticlesCommercialisables():
        return Model_Article.objects.filter(est_vendable = True).order_by("designation")

    @staticmethod
    def toListArticlesCommercialisablesByAuteur(user_id):
        return Model_Article.objects.filter(est_vendable = True).order_by("designation").filter(auteur_id=user_id)

    @staticmethod
    def toListArticlesCommercialisablesOfCategorie(categorie_id):
        return Model_Article.objects.filter(est_vendable = True).filter(categorie_id = categorie_id).order_by("designation")

    @staticmethod
    def toListArticlesCommercialisablesOfCategorieByAuteur(categorie_id,user_id):
        return Model_Article.objects.filter(est_vendable = True).filter(categorie_id = categorie_id).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesAchetables():
        return Model_Article.objects.filter(est_achetable = True).order_by("designation")

    @staticmethod
    def toListArticlesAchetablesByAuteur(user_id):
        return Model_Article.objects.filter(est_achetable = True).filter(auteur_id=user_id).order_by("designation")

    
    @staticmethod
    def toListArticlesVendables():
        return Model_Article.objects.filter(est_vendable = True).order_by("designation")

    @staticmethod
    def toListArticlesVendablesByAuteur(user_id):
        return Model_Article.objects.filter(est_vendable = True).filter(auteur_id=user_id).order_by("designation")


    @staticmethod
    def toListArticlesNonService():
        return Model_Article.objects.exclude(type_article = 2)

    @staticmethod
    def toListArticlesNonServiceByAuteur(user_id):
        return Model_Article.objects.exclude(type_article = 2)


    @staticmethod
    def toListArticlesAchetablesOfCategorie(categorie_id):
        return Model_Article.objects.filter(est_achetable = True).filter(categorie_id = categorie_id).order_by("designation")

    @staticmethod
    def toListArticlesAchetablesOfCategorieByAuteur(categorie_id, user_id):
        return Model_Article.objects.filter(est_achetable = True).filter(categorie_id = categorie_id).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesManufacturables():
        return Model_Article.objects.filter(est_manufacturable = True).order_by("designation")

    @staticmethod
    def toListArticlesManufacturablesByAuteur(user_id):
        return Model_Article.objects.filter(est_manufacturable = True).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesManufacturablesOfCategorie(categorie_id):
        return Model_Article.objects.filter(est_manufacturable = True).filter(categorie_id = categorie_id).order_by("designation")

    @staticmethod
    def toListArticlesManufacturablesOfCategorieByAuteur(categorie_id):
        return Model_Article.objects.filter(est_manufacturable = True).filter(categorie_id = categorie_id).filter(auteur_id = user_id).order_by("designation")

    @staticmethod
    def toListArticlesFabriquables():
        return Model_Article.objects.filter(est_fabriquable = True).order_by("designation")

    @staticmethod
    def toListArticlesFabriquablesByAuteur(user_id):
        return Model_Article.objects.filter(est_fabriquable = True).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesFabriquablesOfCategorie(categorie_id):
        return Model_Article.objects.filter(est_fabriquable = True).filter(categorie_id = categorie_id).order_by("designation")

    @staticmethod
    def toListArticlesFabriquablesOfCategorieByAuteur(categorie_id, user_id):
        return Model_Article.objects.filter(est_fabriquable = True).filter(categorie_id = categorie_id).filter(auteur_id=user_id).order_by("designation")


	#Add By FMA

    @staticmethod
    def toListArticlesStockables():
        return Model_Article.objects.filter(type_article = 3).order_by("designation")
    @staticmethod
    def toListArticlesStockablesByAuteur(user_id):
        return Model_Article.objects.filter(type_article = 3).filter(auteur_id=user_id).order_by("designation")

    '''@staticmethod
    def toListArticlesStockablesOfServiceReferent(service_ref_id):
        return Model_Article.objects.filter(type_article = 3).filter(unite_fonctionnelle_id = service_ref_id).order_by("designation")'''

    @staticmethod
    def toListArticlesStockablesOfServiceReferentByAuteur(service_ref_id, user_id):
        return Model_Article.objects.filter(type_article = 3).filter(unite_fonctionnelle_id = service_ref_id).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesFiscales():
        return Model_Article.objects.filter(type_article = 4).order_by("designation")

    @staticmethod
    def toListArticlesFiscalesByAuteur(user_id):
        return Model_Article.objects.filter(type_article = 4).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesFiscalesOfCategorie(categorie_id):
        return Model_Article.objects.filter(type_article = 4).filter(categorie_id = categorie_id).order_by("designation")

    @staticmethod
    def toListArticlesFiscalesOfCategorieByAuteur(categorie_id, user_id):
        return Model_Article.objects.filter(type_article = 4).filter(categorie_id = categorie_id).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesStockablesOfCategorie(categorie_id):
        return Model_Article.objects.filter(type_article = 3).filter(categorie_id = categorie_id).order_by("designation")

    @staticmethod
    def toListArticlesStockablesOfCategorieByAuteur(categorie_id, user_id):
        return Model_Article.objects.filter(type_article = 3).filter(categorie_id = categorie_id).filter(auteur_id=user_id).order_by("designation")

    @staticmethod
    def toListArticlesStockablesOfId(article_id):
        return Model_Article.objects.filter(type_article = 3).filter(pk = article_id)

    @staticmethod
    def toListArticlesStockablesOfIdByAuteur(article_id, user_id):
        return Model_Article.objects.filter(type_article = 3).filter(auteur_id=user_id).filter(pk = article_id)

    @staticmethod
    def toGetArticlesCount():
        return Model_Article.objects.filter(type_article = 3).count()

    @staticmethod
    def toGetArticlesFiscalesCount():
        return Model_Article.objects.filter(type_article = 4).count()
	#End Add FMA

    @staticmethod
    def toCreateArticle(image, designation, unite_id, est_vendable, est_achetable, est_manufacturable, est_fabriquable, designation_court="",code_article="",code_barre="",type_article=None,categorie_id=None,prix_unitaire=0, compte_id=None, est_amortissable=False, unite_fonctionnelle_id =None ):
        try:
            article = dao_article()
            article.designation = designation
            article.unite_id = unite_id
            article.est_vendable = est_vendable
            article.est_achetable = est_achetable
            article.est_manufacturable = est_manufacturable
            article.est_fabriquable = est_fabriquable
            article.est_amortissable = est_amortissable
            if image != None:
                article.image = image
            if designation_court != None:
                article.designation_court = designation_court
            if code_article != None:
                article.code_article = code_article
            if code_barre != None:
                article.code_barre = code_barre
            article.type_article = type_article
            article.categorie_id = categorie_id
            article.prix_unitaire = prix_unitaire
            article.compte_id = compte_id
            article.unite_fonctionnelle_id = unite_fonctionnelle_id
            return article

        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toSaveArticle(auteur, object_dao_article):
        try:

            #print("ARTICLES TYPE %s" % object_dao_article.type_article)
            #print("ARTICLES COMPTE %s" % object_dao_article.compte_id)
            #print("ARTICLES CATEGORIE %s" % object_dao_article.categorie_id)


            article = Model_Article()
            article.designation = object_dao_article.designation
            article.image = object_dao_article.image
            article.unite_id = object_dao_article.unite_id
            article.est_vendable = object_dao_article.est_vendable
            article.est_achetable = object_dao_article.est_achetable
            article.est_manufacturable = object_dao_article.est_manufacturable
            article.est_fabriquable = object_dao_article.est_fabriquable
            article.est_amortissable = object_dao_article.est_amortissable
            article.designation_court = object_dao_article.designation_court
            article.code_article = object_dao_article.code_article
            article.code_barre = object_dao_article.code_barre
            article.type_article = object_dao_article.type_article
            article.categorie_id = object_dao_article.categorie_id
            article.prix_unitaire = object_dao_article.prix_unitaire
            article.compte_id = object_dao_article.compte_id
            article.unite_fonctionnelle_id = object_dao_article.unite_fonctionnelle_id
            article.creation_date = timezone.now()
            article.save()
            return article
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE L'ARTICLE")
            #print(e)
            return None

    @staticmethod
    def toCreateUpdateArticle(image, designation, unite_id, designation_court="",code_article="",code_barre="",type_article=None,categorie_id=None,prix_unitaire=0, compte_id=None, est_amortissable=False, unite_fonctionnelle_id =None ):
        try:
            article = dao_article()
            article.designation = designation
            article.unite_id = unite_id
            if image != None:
                article.image = image
            if designation_court != None:
                article.designation_court = designation_court
            if code_article != None:
                article.code_article = code_article
            if code_barre != None:
                article.code_barre = code_barre
            article.type_article = type_article
            article.categorie_id = categorie_id
            article.prix_unitaire = prix_unitaire
            article.compte_id = compte_id
            return article

        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ARTICLE")
            #print(e)
            return None
    
    @staticmethod
    def toUpdateArticle(id, object_dao_article):
        try:
            article = Model_Article.objects.get(pk = id)
            article.image = object_dao_article.image
            article.designation = object_dao_article.designation
            article.unite_id = object_dao_article.unite_id
            article.designation_court = object_dao_article.designation_court
            article.code_article = object_dao_article.code_article
            article.code_barre = object_dao_article.code_barre
            
            article.est_vendable = object_dao_article.est_vendable
            article.est_achetable = object_dao_article.est_achetable
            article.est_manufacturable = object_dao_article.est_manufacturable
            article.est_fabriquable = object_dao_article.est_fabriquable
            article.est_amortissable = object_dao_article.est_amortissable

            article.type_article = object_dao_article.type_article
            article.categorie_id = object_dao_article.categorie_id
            article.prix_unitaire = object_dao_article.prix_unitaire
            article.compte_id = object_dao_article.compte_id
            article.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'ARTICLE")
            #print(e)
            return False
    


    @staticmethod
    def toGetArticle(id):
        try:
            return Model_Article.objects.get(pk = id)
        except Exception as e:
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

