from __future__ import unicode_literals
from ErpBackOffice.models import Type_Mobilite

class dao_type_mobilite(object):
    @staticmethod
    def toListTypesMobilite():
        list = []
        for key, value in Type_Mobilite:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeMobilite(id):
        list = dao_type_mobilite.toListTypesArticle()
        for item in list:
            if item["id"] == id: return item
        return None
    

    @staticmethod
    def toListTypesMobiliteEvolution():
        list = []
        for key, value in Type_Mobilite:
            if key != 1:#On se passe de la partie Recrutement qui se fait normalement automatiquement à la création
                item = {
                    "id" : key,
                    "designation" : value
                }
                list.append(item)
        return list

    