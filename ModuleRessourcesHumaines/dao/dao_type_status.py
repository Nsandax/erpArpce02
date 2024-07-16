from __future__ import unicode_literals
from ErpBackOffice.models import TypeStatus

class dao_type_status(object):
    @staticmethod
    def toListTypeStatus():
        list = []
        for key, value in TypeStatus:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeStatus(id):
        list = dao_type_status.toListTypeStatus()
        for item in list:
            if item["id"] == id: return item
            #else: return None


    @staticmethod
    def toGetTypeClient():
        return dao_type_status.toGetTypeStatus(1)

    @staticmethod
    def toGetTypeFournisseur():
        return dao_type_status.toGetTypeStatus(2)

    @staticmethod
    def toGetTypeCadre():
        return dao_type_status.toGetTypeStatus(3)