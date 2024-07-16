# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Civilite
from django.utils import timezone


class dao_civilite(object):
    @staticmethod
    def listeCivilite():
        try:
            return Model_Civilite.objects.all()
        except Exception :
           
            return None

    @staticmethod
    def getCivilite(id):
        try:
            return Model_Civilite.objects.get(pk=id)
        except Exception :
           
            return None