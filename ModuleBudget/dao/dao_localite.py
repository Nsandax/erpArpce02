from __future__ import unicode_literals
from ErpBackOffice.models import localite

class dao_localite(object):
    @staticmethod
    def toListLocalites():
        list = []
        for key, value in localite:
            item = {
                "id" : key,
                "designation" : value
            }
            list.append(item)
        return list

    @staticmethod
    def toGetlocalite(id):
        list = dao_localite.toListLocalites()
        for item in list:
            if item["id"] == id: return item
        return None