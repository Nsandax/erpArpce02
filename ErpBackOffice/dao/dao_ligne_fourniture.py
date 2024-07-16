# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ErpBackOffice.models import Model_Ligne_reception, Model_Article, Model_StockArticle

class dao_ligne_fourniture(dao_ligne_reception):
    @staticmethod
    def toListLignesFourniture(fourniture_id):
        return Model_Ligne_reception.objects.filter(bon_reception_id = fourniture_id)

    @staticmethod
    def toListLignesFournitureDuStock(stock_article_id):
        return Model_Ligne_reception.objects.filter(stock_article_id = stock_article_id)
    
    @staticmethod
    def toListLignesFournitureArticle(article_id):
        try:
            list = []
            list_stocks = Model_StockArticle.objects.filter(article_id = article_id)
            for stock in list_stocks :
                lignes_fourniture = dao_ligne_fourniture.toListLignesFournitureDuStock(stock.id)

                for ligne in lignes_fourniture :
                    list.append(ligne)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
            
    @staticmethod
    def toSaveLigneFourniture(auteur, objet_dao_ligne_reception):
        return dao_ligne_reception.toSaveLigneReception(objet_dao_ligne_reception)

    @staticmethod
    def toUpdateLigneFourniture(id, objet_dao_ligne_reception):
        objet_dao_ligne_reception.id = id
        return dao_ligne_reception.toUpdateLigneReception(id, objet_dao_ligne_reception)
    
    @staticmethod
    def toGetLigneFourniture(id):
        return dao_ligne_reception.toGetLigneReception(id)

    @staticmethod
    def toDeleteFourniture(id):
        return dao_ligne_reception.toDeleteLigneReception(id)