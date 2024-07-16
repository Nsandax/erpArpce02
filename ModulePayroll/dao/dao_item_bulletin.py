# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_ItemBulletin
from django.utils import timezone

class dao_item_bulletin(object):
    id = 0
    designation = ""
    rubrique_id = 0
    bulletin_id = 0
    taux = 0.0
    nombre = 0.0
    base = 0.0
    montant = 0.0
    taux_parpat = 0.0
    montant_parpat = 0.0
    reference = ""
    periode = ""
    sequence = 0
    auteur_id = 0

    @staticmethod
    def toList():
        return Model_ItemBulletin.objects.all().order_by("sequence")

    @staticmethod
    def toGetItemOfBulletin(id):
        try:
            item_bulletins = Model_ItemBulletin.objects.filter(bulletin_id = id).order_by("sequence")
            return item_bulletins
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return []

    @staticmethod
    def toGetItemOfRubrique(bulletin_id, rubrique_id):
        try:
            item_bulletin = Model_ItemBulletin.objects.filter(bulletin_id = bulletin_id, rubrique_id = rubrique_id).first()
            return item_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toCreate(auteur_id, designation, rubrique_id, bulletin_id, nombre = 0.0, base = 0.0, taux = 0.0, montant = 0.0, sequence = 0, taux_parpat = 0.0, montant_parpat = 0.0, reference = "", periode = ""):
        try:
            item_bulletin = dao_item_bulletin()
            item_bulletin.auteur_id = auteur_id
            item_bulletin.designation = designation
            item_bulletin.rubrique_id = rubrique_id
            item_bulletin.bulletin_id = bulletin_id
            item_bulletin.nombre = nombre
            item_bulletin.base = base
            item_bulletin.taux = taux
            item_bulletin.montant = montant
            item_bulletin.sequence = sequence
            item_bulletin.taux_parpat = taux_parpat
            item_bulletin.montant_parpat = montant_parpat
            item_bulletin.reference = reference
            item_bulletin.periode = periode
            return item_bulletin
        except Exception as e:
            print("ERREUR LORS DE LA CREATION")
            print(e)
            return None

    @staticmethod
    def toSave(dao_item_bulletin_object):
        try:
            item_bulletin = Model_ItemBulletin()
            item_bulletin.designation = dao_item_bulletin_object.designation
            item_bulletin.auteur_id = dao_item_bulletin_object.auteur_id
            item_bulletin.rubrique_id = dao_item_bulletin_object.rubrique_id
            item_bulletin.bulletin_id = dao_item_bulletin_object.bulletin_id
            item_bulletin.nombre = dao_item_bulletin_object.nombre
            item_bulletin.base = dao_item_bulletin_object.base
            item_bulletin.taux = dao_item_bulletin_object.taux
            item_bulletin.montant = dao_item_bulletin_object.montant
            item_bulletin.taux_parpat = dao_item_bulletin_object.taux_parpat
            item_bulletin.montant_parpat = dao_item_bulletin_object.montant_parpat
            item_bulletin.sequence = dao_item_bulletin_object.sequence
            item_bulletin.reference = dao_item_bulletin_object.reference
            item_bulletin.periode = dao_item_bulletin_object.periode
            item_bulletin.creation_date = timezone.now()
            item_bulletin.save()
            return item_bulletin
        except Exception as e:
            print("ERREUR LORS DU SAVE")
            print(e)
            return None


    @staticmethod
    def toUpdate(id, dao_item_bulletin_object):
        try:
            item_bulletin = Model_ItemBulletin.objects.get(pk = id)
            item_bulletin.designation = dao_item_bulletin_object.designation
            item_bulletin.rubrique_id = dao_item_bulletin_object.rubrique_id
            item_bulletin.bulletin_id = dao_item_bulletin_object.bulletin_id
            item_bulletin.nombre = dao_item_bulletin_object.nombre
            item_bulletin.base = dao_item_bulletin_object.base
            item_bulletin.taux = dao_item_bulletin_object.taux
            item_bulletin.montant = dao_item_bulletin_object.montant
            item_bulletin.sequence = dao_item_bulletin_object.sequence
            item_bulletin.taux_parpat = dao_item_bulletin_object.taux_parpat
            item_bulletin.montant_parpat = dao_item_bulletin_object.montant_parpat
            item_bulletin.reference = dao_item_bulletin_object.reference
            item_bulletin.periode = dao_item_bulletin_object.periode
            item_bulletin.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False


    @staticmethod
    def toDelete(dao_item_bulletin_object):
        try:
            item_bulletin = Model_ItemBulletin.objects.get(pk = dao_item_bulletin_object.id)
            item_bulletin.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False


    @staticmethod
    def toGet(id):
        try:
            item_bulletin = Model_ItemBulletin.objects.get(pk = id)
            return item_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None