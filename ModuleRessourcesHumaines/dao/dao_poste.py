# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_Poste
from django.utils import timezone

class dao_poste(object):
    id = 0
    designation = ""
    description = ""
    auteur_id = 0
    departement_id = None
    # classification_pro_id = None
    nbr_subordonne = 0

    @staticmethod
    def toListPostes():
        return Model_Poste.objects.all().order_by("designation")

    @staticmethod
    def toCreatePoste(auteur, designation, description, departement_id, nbr_subordonne = 0):
        try:
            poste = dao_poste()
            poste.auteur_id = auteur.id
            poste.designation = designation
            poste.description = description
            # poste.classification_pro_id = classification_pro_id
            poste.nbr_subordonne = nbr_subordonne
            poste.departement_id = departement_id
            return poste
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSavePoste(dao_poste_object):
        try:
            poste = Model_Poste()
            poste.designation = dao_poste_object.designation
            #poste.auteur_id = dao_poste_object.auteur_id
            poste.description = dao_poste_object.description
            # poste.classification_pro_id = dao_poste_object.classification_pro_id
            poste.nbr_subordonne = dao_poste_object.nbr_subordonne
            poste.departement_id = dao_poste_object.departement_id
            poste.creation_date = timezone.now()
            poste.save()
            return poste
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None


    @staticmethod
    def toUpdatePoste(id, dao_poste_object):
        try:
            poste = Model_Poste.objects.get(pk = id)
            poste.designation = dao_poste_object.designation
            poste.description = dao_poste_object.description
            # poste.classification_pro_id = dao_poste_object.classification_pro_id
            poste.nbr_subordonne = dao_poste_object.nbr_subordonne
            poste.departement_id = dao_poste_object.departement_id
            poste.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR")
            #print(e)
            return False


    @staticmethod
    def toDeletePoste(dao_poste_object):
        try:
            poste = Model_Poste.objects.get(pk = dao_poste_object.id)
            poste.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False


    @staticmethod
    def toGetPoste(id):
        try:
            poste = Model_Poste.objects.get(pk = id)
            return poste
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toListPostesByDepartement(departement_id):
        return Model_Poste.objects.filter(departement_id = departement_id)


    @staticmethod
    def toGetOrCreatePoste(auteur, designation, classification_pro, nbr_subordonne, departement_id):
        try:
            objet_poste = Model_Poste.objects.filter(designation__icontains = designation).first()
            # print('POSTE OBJECT CHECK', objet_poste)
            if not objet_poste:
                poste = dao_poste()
                objet_poste = poste.toCreatePoste(auteur, designation, None, departement_id, nbr_subordonne)
                objet_poste = poste.toSavePoste(objet_poste)
            return objet_poste
        except Exception as e:
            # print("ERREUR LORS toGetOrCreatePoste")
            # print(e)
            return None
