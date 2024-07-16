from __future__ import unicode_literals
from ErpBackOffice.models import TypeArticle

class dao_type_article(object):
    @staticmethod
    def toListTypesArticle():
        list = []
        for key, value in TypeArticle:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeArticle(id):
        list = dao_type_article.toListTypesArticle()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypeConsommable():
        return dao_type_article.toGetTypeArticle(1)

    @staticmethod
    def toGetTypeService():
        return dao_type_article.toGetTypeArticle(2)

    @staticmethod
    def toGetTypeStockable():
        return dao_type_article.toGetTypeArticle(3)

    @staticmethod
    def toGetTypeFiscale():
        return dao_type_article.toGetTypeArticle(4)
		
    @staticmethod
    def toGetTypeImmobilier():
        return dao_type_article.toGetTypeArticle(5)