from __future__ import unicode_literals
from ErpBackOffice.models import TypeResultat

class dao_type_resultat(object):
    @staticmethod
    def toList():
        list = []
        for key, value in TypeResultat:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGet(id):
        list = dao_type_resultat.toList()
        for item in list:
            if item["id"] == id: return item
        return None
