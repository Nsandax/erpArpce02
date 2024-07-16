# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ErpBackOffice.models import Model_Fonction


from django.utils import timezone


class dao_fonction(object):
    id = 0
    designation = ""
    description = ""
    auteur_id = 0
    departement_id = 0
    creation_date = None

    @staticmethod
    def toListFonction():
        return Model_Fonction.objects.all().order_by("designation")

    @staticmethod
    def toCreateFonction(auteur, designation, description, departement_id):
        try:
            fonction = dao_fonction()
            fonction.auteur_id = auteur.id
            fonction.designation = designation
            fonction.description = description
            fonction.departement_id = departement_id
            return fonction
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION FONCTION")
            #print(e)
            return None

    @staticmethod
    def toSaveFonction(dao_fonction_object):
        try:
            fonction = Model_Fonction()
            fonction.designation = dao_fonction_object.designation
            fonction.auteur_id = dao_fonction_object.auteur_id
            fonction.description = dao_fonction_object.description
            fonction.departement_id = dao_fonction_object.departement_id
            fonction.creation_date = timezone.now()
            fonction.save()
            return fonction
        except Exception as e:
            #print("ERREUR LORS DU SAVE FONCTION")
            #print(e)
            return None

    @staticmethod
    def toUpdateFontion(id, dao_fonction_object):
        try:
            fonction = Model_Fonction.objects.get(pk=id)
            fonction.designation = dao_fonction_object.designation
            fonction.description = dao_fonction_object.description
            fonction.departement_id = dao_fonction_object.departement_id
            fonction.creation_date = timezone.now()
            fonction.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE MISE A JOUR FONCTION")
            #print(e)
            return False

    @staticmethod
    def toDeleteFontion(dao_poste_object):
        try:
            fonction = Model_Fonction.objects.get(pk=dao_poste_object.id)
            fonction.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    @staticmethod
    def toGetFonction(id):
        try:
            fonction = Model_Fonction.objects.get(pk=id)
            return fonction
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE FONCTION")
            #print(e)
            return None


    @staticmethod
    def toGetOrCreateFonction(auteur, designation, departement_id, description):
        try:
            objet_poste = Model_Fonction.objects.filter(designation__icontains = designation).first()
            print('FONCTION OBJECT CHECK', objet_poste)
            if not objet_poste:
                poste = dao_fonction()
                objet_poste = poste.toCreateFonction(auteur, designation, description, departement_id)
                objet_poste = poste.toSaveFonction(objet_poste)
            # if objet_poste == None:
            #     poste = dao_fonction()
            #     objet_poste = poste.toCreateFonction(auteur, designation, description, departement_id)
            #     objet_poste = poste.toSaveFonction(objet_poste)
            return objet_poste
        except Exception as e:
            print("ERREUR LORS toGetOrCreateFonction")
            print(e)
            return None
