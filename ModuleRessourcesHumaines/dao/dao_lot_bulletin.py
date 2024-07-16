# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_LotBulletins
from django.utils import timezone

class dao_lot_bulletin(object):
    id = 0
    designation = ""
    reference = ""
    type = ""
    auteur_id = 0
    departement_id = 0
    date_dossier = None


    @staticmethod
    def toList():
        return Model_LotBulletins.objects.all().order_by("designation")

    @staticmethod
    def toListSoumis():
        return Model_LotBulletins.objects.filter(est_soumis = True).order_by("designation")

    @staticmethod
    def toListValide():
        return Model_LotBulletins.objects.filter(est_valide = True).order_by("designation")
    
    @staticmethod
    def toCreate(auteur_id, designation, departement_id, type = "", reference = "", date_dossier = None, date_debut = None, date_fin = None):
        try:
            lot_bulletin = dao_lot_bulletin()
            lot_bulletin.auteur_id = auteur_id
            lot_bulletin.designation = designation
            if reference == None or reference == "": reference = dao_lot_bulletin.toGenerateNumero()
            lot_bulletin.reference = reference
            lot_bulletin.type = type
            lot_bulletin.departement_id = departement_id
            lot_bulletin.date_dossier = date_dossier
            lot_bulletin.date_debut = date_debut
            lot_bulletin.date_fin = date_fin
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_lot_bulletin_object):
        try:
            lot_bulletin = Model_LotBulletins()
            lot_bulletin.designation = dao_lot_bulletin_object.designation
            lot_bulletin.auteur_id = dao_lot_bulletin_object.auteur_id
            lot_bulletin.reference = dao_lot_bulletin_object.reference
            lot_bulletin.type = dao_lot_bulletin_object.type
            lot_bulletin.departement_id = dao_lot_bulletin_object.departement_id
            lot_bulletin.creation_date = timezone.now()
            lot_bulletin.date_dossier = dao_lot_bulletin_object.date_dossier
            lot_bulletin.save()
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_lot_bulletin_object):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            lot_bulletin.designation = dao_lot_bulletin_object.designation
            lot_bulletin.reference = dao_lot_bulletin_object.reference
            lot_bulletin.type = dao_lot_bulletin_object.type
            lot_bulletin.departement_id = dao_lot_bulletin_object.departement_id
            lot_bulletin.date_dossier = dao_lot_bulletin_object.date_dossier
            lot_bulletin.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_lot_bulletin_object):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = dao_lot_bulletin_object.id)
            lot_bulletin.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetMois(id):
        try:
            mois = ""
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            date_du_mois = lot_bulletin.creation_date
            if lot_bulletin.date_dossier != None : date_du_mois = lot_bulletin.date_dossier
            mois = lot_bulletin.date_dossier.strftime("%B")
            return mois
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toSoumetre(id):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            lot_bulletin.est_soumis = True
            lot_bulletin.save()
            return lot_bulletin
        except Exception as e:
            #print("ERREUR toSoumetre(id)")
            #print(e)
            return None

    @staticmethod
    def toGenerateNumero():
        total = dao_lot_bulletin.toList().count()
        total = total + 1
        temp_numero = str(total)
        
        for i in range(len(str(total)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois
        
        temp_numero = "DOS-PAY-%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetOrderMax():
        try:
            max = dao_lot_bulletin.toList().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None