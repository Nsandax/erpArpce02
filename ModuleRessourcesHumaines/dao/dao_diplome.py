from __future__ import unicode_literals
from ErpBackOffice.models import Model_Diplome
from django.utils import timezone

class dao_diplome(object):
    id = 0
    designation = ''
    description  = ''
    institution  = ''
    type_id = None
    auteur_id = None

    @staticmethod
    def toList():
        return  Model_Diplome.objects.all().order_by("designation")

    @staticmethod
    def toCreate(designation, description, type_id = None, institution = ""):
        try:
            diplome = dao_diplome()
            diplome.designation = designation
            diplome.description = description
            diplome.type_id = type_id
            diplome.institution = institution
            return diplome
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_diplome)")
            #print(e)
            return None

    @staticmethod
    def toSave(auteur, dao_diplome_object):
        try:
            diplome =  Model_Diplome()
            diplome.designation = dao_diplome_object.designation
            diplome.description = dao_diplome_object.description
            diplome.type_id = dao_diplome_object.type_id
            diplome.institution = dao_diplome_object.institution
            diplome.auteur_id = auteur.id
            diplome.save()
            return diplome
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_diplome)")
            #print(e)
            return None

    @staticmethod
    def toUpdate(id, dao_diplome_object):
        try:
            diplome =   Model_Diplome.objects.get(pk = id)
            diplome.designation = dao_diplome_object.designation
            diplome.description = dao_diplome_object.description
            diplome.type_id = dao_diplome_object.type_id
            diplome.institution = dao_diplome_object.institution
            diplome.save()
            return diplome
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_diplome)")
            #print(e)
            return None

    @staticmethod
    def toDelete(dao_diplome_object):
        try:
            diplome =  Model_Diplome.objects.get(pk = dao_diplome_object.id)
            diplome.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGet(id):
        try:
            return Model_Diplome.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetOrCreatediplome(auteur, libelle):
        try:
            diplome = Model_Diplome.objects.filter(designation__icontains = libelle).first()
            if not diplome:
                undiplome = dao_diplome()
                diplome = undiplome.toCreate(libelle, "", None, "")
                diplome = undiplome.toSave(auteur, diplome)
            return diplome
        except Exception as e:
            print("Error toGetOrCreateDiplome", e)
            return None

