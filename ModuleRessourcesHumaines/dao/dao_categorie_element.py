from __future__ import unicode_literals
from ErpBackOffice.models import CategorieElementBulletin

class dao_categorie_element(object):
    @staticmethod
    def toList():
        list = []
        for key, value in CategorieElementBulletin:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGet(id):
        list = dao_categorie_element.toList()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetImposable():
        return dao_categorie_element.toGet(1)

    @staticmethod
    def toGetNonImposable():
        return dao_categorie_element.toGet(2)
