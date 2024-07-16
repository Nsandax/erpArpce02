from __future__ import unicode_literals
from ErpBackOffice.models import TypeCalcul

class dao_type_calcul(object):
    @staticmethod
    def toList():
        list = []
        for key, value in TypeCalcul:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGet(id):
        list = dao_type_calcul.toList()
        for item in list:
            if item["id"] == id: return item
        return None
