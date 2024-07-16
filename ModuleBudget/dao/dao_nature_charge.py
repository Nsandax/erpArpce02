from __future__ import unicode_literals
from ErpBackOffice.models import natureCharge

class dao_nature_charge(object):
    @staticmethod
    def toListNatureCharges():
        list = []
        for key, value in natureCharge:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetnatureCharge(id):
        list = dao_nature_charge.toListNatureCharges()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetVariable():
        return dao_nature_charge.toGetnatureCharge(0)

    @staticmethod
    def toGetFixe():
        return dao_nature_charge.toGetnatureCharge(1)