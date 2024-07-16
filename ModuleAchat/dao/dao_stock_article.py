# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_StockArticle

class dao_stock_article(object):
    id = 0
    article_id = 0
    quantite_disponible = 0
    emplacement_id = 0
    transformation_source_id = None

    @staticmethod
    def toListStocksOfArticle(article_id):
        try:
            return Model_StockArticle.objects.filter(article_id = article_id)
        except Exception as e:
            return None

    @staticmethod
    def toListStocksArticles():
        return Model_StockArticle.objects.all()


    @staticmethod
    def toListStocksInEmplacement(emplacement_id):
        try:
            return Model_StockArticle.objects.filter(emplacement_id = emplacement_id)
        except Exception as e:
            return None

    @staticmethod
    def toListStocksArticleInEmplacement(article_id,emplacement_id):
        try:
            return Model_StockArticle.objects.filter(emplacement_id = emplacement_id).filter(article_id = article_id)
        except Exception as e:
            return None

    @staticmethod
    def toListStocksOfArticleInEmplacement(article_id, emplacement_id):
        try:
            return Model_StockArticle.objects.filter(article_id = article_id).filter(emplacement_id = emplacement_id)
            # print('***STOCK GET', stock)
            #   stock
        except Exception as e:
            return None

    @staticmethod
    def toGetStocksOfArticleInEmplacement(article_id, emplacement_id):
        try:
            stock = Model_StockArticle.objects.filter(article__id = article_id, emplacement__id = emplacement_id).first()
            # print('***STOCK GET', stock)
            return stock
        except Exception as e:
            return None

    @staticmethod
    def toListStocksOfArticleInStockageSBA(article_id):
        try:
            return Model_StockArticle.objects.filter(article_id = article_id).filter(emplacement__designation = "Stockage SBA")
        except Exception as e:
            return None


    @staticmethod
    def toListStocksFromTransformation(transformation_id):
        try:
            return Model_StockArticle.objects.filter(transformation_source_id = transformation_id)
        except Exception as e:
            return None
    @staticmethod
    def toCreateStockArticle(article_id, quantite_disponible = 0, emplacement_id = None, transformation_source_id = None):
        try:
            stock = dao_stock_article()
            stock.article_id = article_id
            stock.quantite_disponible = 0
            if quantite_disponible != 0 :
                stock.quantite_disponible = quantite_disponible
            stock.emplacement_id = emplacement_id
            stock.transformation_source_id = transformation_source_id
            return stock
        except Exception as e:
            # print("ERREUR LORS DE LA CREATION DU STOCK")
            # print(e)
            return None

    @staticmethod
    def toSaveStockArticle(object_dao_stock_article):
        try:
            stock = Model_StockArticle()
            ###print("dans le dao", object_dao_stock_article)
            ###print("emplacemen",object_dao_stock_article.emplacement_id)
            stock.article_id = object_dao_stock_article.article_id
            stock.quantite_disponible = object_dao_stock_article.quantite_disponible
            stock.emplacement_id = object_dao_stock_article.emplacement_id
            #stock.transformation_source_id = object_dao_stock_article.transformation_source_id
            stock.save()
            return stock
        except Exception as e:
            # print("ERREUR LORS DE L'ENREGISTREMENT DU STOCK")
            # print(e)
            return None

    @staticmethod
    def toUpdateStockArticle(id, object_dao_stock_article):
        try:
            stock = Model_StockArticle.objects.get(pk = id)
            stock.article_id = object_dao_stock_article.article_id
            stock.quantite_disponible = object_dao_stock_article.quantite_disponible
            stock.emplacement_id = object_dao_stock_article.emplacement_id
            #stock.transformation_source_id = object_dao_stock_article.transformation_source_id
            stock.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DE L'ARTICLE")
            #print(e)
            return False

    @staticmethod
    def toGetStockArticle(id):
        try:
            return Model_StockArticle.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toGetQuantiteStockOfEmplacement(article, id_emplacement):
        try:
            # ###print("ARRIVED ICI 1")
            # if article.est_service: return "INFINIE"
            # ###print("ARRIVED ICI 2")
			# ###print("Article Id", article.id)
            quantite_stock = 0
            # ###print("ARRIVED ICI 3")
            # ###print(id_emplacement)
            if id_emplacement != 0:
                # ###print("2")
                stocks = Model_StockArticle.objects.filter(article_id = article).filter(emplacement_id = id_emplacement)
                # ###print("Stock", stocks)
                for stock in stocks :

					###print("4")
                    quantite_stock = quantite_stock + stock.quantite_disponible
            return quantite_stock
        except Exception as e:
            return None