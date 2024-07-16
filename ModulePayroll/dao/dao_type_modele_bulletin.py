from __future__ import unicode_literals
from ErpBackOffice.models import TypeModeleBulletin

class dao_type_modele_bulletin(object):
    @staticmethod
    def toList():
        list = []
        for key, value in TypeModeleBulletin:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGe(id):
        list = dao_type_modele_bulletin.toList()
        for item in list:
            if item["id"] == id: return item
        return None