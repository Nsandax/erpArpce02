from __future__ import unicode_literals
from ErpBackOffice.models import CategorieOperation

class dao_categorie_operation_contrat(object):
    @staticmethod
    def toListCategorieOperation():
        list = []
        for key, value in CategorieOperation:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetCategorieOperation(id):
        list = dao_categorie_operation_contrat.toListCategorieOperation()
        for item in list:
            if item["id"] == id: return item
        return None

