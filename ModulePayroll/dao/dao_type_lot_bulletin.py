from __future__ import unicode_literals
from ErpBackOffice.models import TypeLotBulletin

class dao_type_lot_bulletin(object):
    @staticmethod
    def toListTypesLotBulletins():
        list = []
        for key, value in TypeLotBulletin:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetTypeLotBulletins(id):
        list = dao_type_lot_bulletin.toListTypesLotBulletins()
        for item in list:
            if item["id"] == id: return item
        return None