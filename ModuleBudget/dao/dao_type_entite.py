from __future__ import unicode_literals
from ErpBackOffice.models import TypeEntite

class dao_type_entite(object):
    @staticmethod
    def toListTypeEntites():
        list = []
        for key, value in TypeEntite:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeEntite(id):
        list = dao_type_entite.toListTypeEntites()
        for item in list:
            if item["id"] == id: return item
        return None