# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_LignesLot
from django.utils import timezone

class dao_ligne_lot(object):
    id = 0
    reference = ""
    employe = None
    departement_id = None
    
    

    @staticmethod
    def toListLigneLot():
        return Model_LignesLot.objects.all()

    @staticmethod
    def toGetLigneLot(id):
        try:
            return Model_LignesLot.objects.get(pk = id)
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None
    
    @staticmethod
    def toCreateLigneLot(reference, employe, departement_id = None):
        try:
            ligne_lot = dao_ligne_lot()
            ligne_lot.reference = reference
            ligne_lot.employe = employe
            ligne_lot.departement_id = departement_id
            return ligne_lot
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSaveLigneLot(auteur, objet_ligne_lot):
        try:
            ligne_lot = Model_LignesLot()
            ligne_lot.reference = objet_ligne_lot.reference
            ligne_lot.employe = objet_ligne_lot.employe
            ligne_lot.departement_id = objet_ligne_lot.departement_id
            ligne_lot.creation_date = timezone.now()
            ligne_lot.auteur_id = auteur.id
            ligne_lot.save()
            return ligne_lot
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdateLigneLot(id, objet_ligne_lot):
        try:
            ligne_lot = Model_LignesLot.objects.get(pk = id)
            ligne_lot.reference = objet_ligne_lot.reference
            ligne_lot.employe = objet_ligne_lot.employe
            ligne_lot.departement_id = objet_ligne_lot.departement_id
            ligne_lot.creation_date = timezone.now()
            ligne_lot.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDeleteLigneLot(id):
        try:
            ligne_lot = Model_LignesLot.objects.get(pk = id)
            ligne_lot.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    