# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_ElementBulletin
from django.utils import timezone

class dao_element_bulletin(object):
    id = 0
    designation = ""
    reference = ""
    auteur_id = 0
    type_element = 0
    categorie_element = 0
    type_calcul = 0
    type_resultat = 0
    reference = ""
    montant = 0
    pourcentage = 0
    calcul = ""
    bareme_id = 0
    devise_id = 0
    compte_id = 0
    sequence = 0

    @staticmethod
    def toList():
        return Model_ElementBulletin.objects.all().order_by("sequence")

    @staticmethod
    def toListApayer():
        return Model_ElementBulletin.objects.all().filter(type_element = 1).order_by("sequence")

    @staticmethod
    def toListAretenir():
        return Model_ElementBulletin.objects.all().filter(type_element = 2).order_by("sequence")
    
    @staticmethod
    def toCreate(auteur_id, designation, type_element, categorie_element, reference="",  montant = 0, type_calcul = 0, type_resultat = 0, pourcentage = 0, calcul = "", bareme_id = 0, devise_id = 0, compte_id = 0, sequence = 100):
        try:
            element_bulletin = dao_element_bulletin()
            element_bulletin.auteur_id = auteur_id
            element_bulletin.designation = designation
            element_bulletin.type_element = type_element
            element_bulletin.categorie_element = categorie_element
            element_bulletin.type_calcul = type_calcul
            element_bulletin.type_resultat = type_resultat
            element_bulletin.reference = reference
            element_bulletin.montant = montant
            element_bulletin.calcul = calcul
            element_bulletin.pourcentage = pourcentage
            element_bulletin.bareme_id = bareme_id
            element_bulletin.devise_id = devise_id
            element_bulletin.compte_id = compte_id
            element_bulletin.sequence = sequence
            return element_bulletin
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_element_bulletin_object):
        try:
            element_bulletin = Model_ElementBulletin()
            element_bulletin.designation = dao_element_bulletin_object.designation
            element_bulletin.auteur_id = dao_element_bulletin_object.auteur_id
            if dao_element_bulletin_object.type_element != 0: element_bulletin.type_element = dao_element_bulletin_object.type_element
            if dao_element_bulletin_object.categorie_element != 0: element_bulletin.categorie_element = dao_element_bulletin_object.categorie_element
            if dao_element_bulletin_object.devise_id != 0: element_bulletin.devise_id = dao_element_bulletin_object.devise_id
            if dao_element_bulletin_object.compte_id != 0: element_bulletin.compte_id = dao_element_bulletin_object.compte_id
            if dao_element_bulletin_object.reference != "": element_bulletin.reference = dao_element_bulletin_object.reference
            if dao_element_bulletin_object.type_calcul != 0: element_bulletin.type_calcul = dao_element_bulletin_object.type_calcul
            if dao_element_bulletin_object.type_resultat != 0: element_bulletin.type_resultat = dao_element_bulletin_object.type_resultat
            if dao_element_bulletin_object.calcul != "": element_bulletin.calcul = dao_element_bulletin_object.calcul
            if dao_element_bulletin_object.bareme_id != 0: element_bulletin.bareme_id = dao_element_bulletin_object.bareme_id
            element_bulletin.pourcentage = dao_element_bulletin_object.pourcentage
            element_bulletin.montant = dao_element_bulletin_object.montant
            element_bulletin.sequence = dao_element_bulletin_object.sequence
            element_bulletin.creation_date = timezone.now()
            element_bulletin.save()
            return element_bulletin
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    
    @staticmethod
    def toUpdate(id, dao_element_bulletin_object):
        try:
            element_bulletin = Model_ElementBulletin.objects.get(pk = id)
            element_bulletin.designation = dao_element_bulletin_object.designation
            if dao_element_bulletin_object.type_element != 0: element_bulletin.type_element = dao_element_bulletin_object.type_element
            if dao_element_bulletin_object.categorie_element != 0: element_bulletin.categorie_element = dao_element_bulletin_object.categorie_element
            if dao_element_bulletin_object.devise_id != 0: element_bulletin.devise_id = dao_element_bulletin_object.devise_id
            if dao_element_bulletin_object.compte_id != 0: element_bulletin.compte_id = dao_element_bulletin_object.compte_id
            if dao_element_bulletin_object.reference != "": element_bulletin.reference = dao_element_bulletin_object.reference
            if dao_element_bulletin_object.type_calcul != 0: element_bulletin.type_calcul = dao_element_bulletin_object.type_calcul
            if dao_element_bulletin_object.type_resultat != 0: element_bulletin.type_resultat = dao_element_bulletin_object.type_resultat
            if dao_element_bulletin_object.pourcentage != 0: element_bulletin.pourcentage = dao_element_bulletin_object.pourcentage
            if dao_element_bulletin_object.calcul != "": element_bulletin.calcul = dao_element_bulletin_object.calcul
            if dao_element_bulletin_object.bareme_id != 0: element_bulletin.bareme_id = dao_element_bulletin_object.bareme_id
            element_bulletin.montant = dao_element_bulletin_object.montant
            element_bulletin.sequence = dao_element_bulletin_object.sequence
            element_bulletin.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False

    
    @staticmethod
    def toDelete(dao_element_bulletin_object):
        try:
            element_bulletin = Model_ElementBulletin.objects.get(pk = dao_element_bulletin_object.id)
            element_bulletin.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    
    @staticmethod
    def toGet(id):
        try:
            element_bulletin = Model_ElementBulletin.objects.get(pk = id)
            return element_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None