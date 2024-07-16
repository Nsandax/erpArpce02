from __future__ import unicode_literals
from ErpBackOffice.models import TypeOperation

class dao_type_operation_contrat(object):
    @staticmethod
    def toListTypeOperation():
        list = []
        for key, value in TypeOperation:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeOperation(id):
        list = dao_type_operation_contrat.toListTypeOperation()
        for item in list:
            if item["id"] == id: return item
        return None

