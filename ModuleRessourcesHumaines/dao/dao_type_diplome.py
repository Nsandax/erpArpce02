from __future__ import unicode_literals
from ErpBackOffice.models import Model_Type_Diplome
from django.utils import timezone

class dao_type_diplome(object):
    id = 0
    designation = ''
    description  = ''
    auteur_id = 0

    @staticmethod
    def toList():
        return  Model_Type_Diplome.objects.all().order_by("designation")

    @staticmethod
    def toCreate(designation, description):
        try:
            type_diplome = dao_type_diplome()
            type_diplome.designation = designation
            type_diplome.description = description
            return type_diplome
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION (dao_type_diplome)")
            #print(e)
            return None

    @staticmethod
    def toSave(auteur, dao_type_diplome_object):
        try:
            type_diplome =  Model_Type_Diplome()
            type_diplome.designation = dao_type_diplome_object.designation
            type_diplome.description = dao_type_diplome_object.description
            type_diplome.auteur_id = auteur.id
            type_diplome.save()
            return type_diplome
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_type_diplome)")
            #print(e)
            return None

    @staticmethod
    def toUpdate(id, dao_type_diplome_object):
        try:
            type_diplome =   Model_Type_Diplome.objects.get(pk = id)
            type_diplome.designation = dao_type_diplome_object.designation
            type_diplome.description = dao_type_diplome_object.description
            type_diplome.save()
            return type_diplome
        except Exception as e:
            #print("ERREUR LORS DU SAVE (dao_type_diplome)")
            #print(e)
            return None

    @staticmethod
    def toDelete(dao_type_diplome_object):
        try:
            type_diplome =  Model_Type_Diplome.objects.get(pk = dao_type_diplome_object.id)
            type_diplome.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetType_diplome(id):
        try:
            return Model_Type_Diplome.objects.get(pk = id)
        except Exception as e:
            return None

