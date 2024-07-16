from __future__ import unicode_literals
from ErpBackOffice.models import TypeElementBulletin

class dao_type_element_bulletin(object):
    @staticmethod
    def toList():
        list = []
        for key, value in TypeElementBulletin:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGet(id):
        list = dao_type_element_bulletin.toList()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetTypeApayer():
        return dao_type_element_bulletin.toGet(1)

    @staticmethod
    def toGetTypeAretenir():
        return dao_type_element_bulletin.toGet(2)
