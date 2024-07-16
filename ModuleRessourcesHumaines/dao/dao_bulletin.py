# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Bulletin
from django.utils import timezone

class dao_bulletin(object):
    id = 0
    designation = ""
    reference = ""
    periode = ""
    image = ""
    type = ""
    employe_id = 0
    lot_id = 0
    auteur_id = 0

    @staticmethod
    def toList():
        return Model_Bulletin.objects.all().order_by("designation")

    @staticmethod
    def toListOfDossier(dossier_id):
        return Model_Bulletin.objects.filter(lot_id = dossier_id)
    
    @staticmethod
    def toCreate(auteur_id, designation, employe_id, lot_id, reference = "", periode = "", type = ""):
        try:
            bulletin = dao_bulletin()
            bulletin.auteur_id = auteur_id
            bulletin.designation = designation
            bulletin.employe_id = employe_id
            bulletin.lot_id = lot_id
            if reference == None or reference == "":
                bulletin.reference = dao_bulletin.toGenerateNumeroBulletin()
            else:
                bulletin.reference = reference
            bulletin.periode = periode
            bulletin.type = type
            return bulletin
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_bulletin_object):
        try:
            bulletin = Model_Bulletin()
            bulletin.designation = dao_bulletin_object.designation
            bulletin.auteur_id = dao_bulletin_object.auteur_id
            bulletin.employe_id = dao_bulletin_object.employe_id
            bulletin.lot_id = dao_bulletin_object.lot_id
            bulletin.reference = dao_bulletin_object.reference
            bulletin.type = dao_bulletin_object.type
            bulletin.creation_date = timezone.now()
            bulletin.save()
            return bulletin
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_bulletin_object):
        try:
            bulletin = Model_Bulletin.objects.get(pk = id)
            bulletin.designation = dao_bulletin_object.designation
            bulletin.employe_id = dao_bulletin_object.employe_id
            bulletin.lot_id = dao_bulletin_object.lot_id
            bulletin.reference = dao_bulletin_object.reference
            bulletin.type = dao_bulletin_object.type
            bulletin.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_bulletin_object):
        try:
            bulletin = Model_Bulletin.objects.get(pk = dao_bulletin_object.id)
            bulletin.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            bulletin = Model_Bulletin.objects.get(pk = id)
            return bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGenerateNumeroBulletin():
        total_bulletins = dao_bulletin.toList().count()
        total_bulletins = total_bulletins + 1
        temp_numero = str(total_bulletins)

        for i in range(len(str(total_bulletins)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "BP%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetNextId():
        total_bulletins = dao_bulletin.toList().count()
        total_bulletins = total_bulletins + 1
        
        if total_bulletins >= 1:
            return total_bulletins
        else:
            return 1