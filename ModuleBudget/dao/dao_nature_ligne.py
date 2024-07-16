from __future__ import unicode_literals
from ErpBackOffice.models import natureLigneBgt

class dao_nature_ligne(object):
    @staticmethod
    def toListNatureLigneBgts():
        list = []
        for key, value in natureLigneBgt:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetnatureLigneBgt(id):
        list = dao_nature_ligne.toListNatureLigneBgts()
        for item in list:
            if item["id"] == id: return item
        return None

    @staticmethod
    def toGetActive():
        return dao_nature_ligne.toGetnatureLigneBgt(0)

    @staticmethod
    def toGetInactive():
        return dao_nature_ligne.toGetnatureLigneBgt(1)
