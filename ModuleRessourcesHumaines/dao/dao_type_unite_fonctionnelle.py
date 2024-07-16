
from __future__ import unicode_literals

from ErpBackOffice.models import Model_TypeUnite_fonctionnelle
from django.utils import timezone

class dao_type_unite_fonctionnelle(object):
    id = 0
    designation = ""
    auteur_id = None
    description = ""

    @staticmethod
    def toList():
        return Model_TypeUnite_fonctionnelle.objects.all()#.order_by("designation")

    @staticmethod
    def toCreate(designation, description= ""):        
        try:
            type_unite_fonctionnelle = dao_type_unite_fonctionnelle()
            type_unite_fonctionnelle.designation = designation
            type_unite_fonctionnelle.description = description
            return type_unite_fonctionnelle
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU TYPE D UNITE FONCTIONNELLE")
            #print(e)
            return None

    @staticmethod
    def toSave(auteur, object_dao_type_unite_fonctionnelle):
        try:
            type_unite_fonctionnelle = Model_TypeUnite_fonctionnelle()
            type_unite_fonctionnelle.auteur_id = auteur.id
            type_unite_fonctionnelle.designation = object_dao_type_unite_fonctionnelle.designation
            type_unite_fonctionnelle.description = object_dao_type_unite_fonctionnelle.description
            type_unite_fonctionnelle.creation_date = timezone.now()
            type_unite_fonctionnelle.save()
            return type_unite_fonctionnelle
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ARTICLE")
            #print(e)
            return None        

    @staticmethod
    def toUpdate(id, object_dao_type_unite_fonctionnelle):
        try:
            type_unite_fonctionnelle = Model_TypeUnite_fonctionnelle.objects.get(pk = id)
            type_unite_fonctionnelle.designation = object_dao_type_unite_fonctionnelle.designation
            type_unite_fonctionnelle.description = object_dao_type_unite_fonctionnelle.description
            type_unite_fonctionnelle.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU TYPE D UNITE FONCTIONNELLE")
            #print(e)
            return False        

    @staticmethod
    def toDelete(id):
        try:
            type_unite_fonctionnelle = Model_TypeUnite_fonctionnelle.objects.get(pk = id)
            type_unite_fonctionnelle.delete()
            return True
            return False
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU TYPE D UNITE FONCTIONNELLE")
            #print(e)
            return False
  
    @staticmethod
    def toGet(id):
        try:
            return Model_TypeUnite_fonctionnelle.objects.get(pk = id)
        except Exception as e:
            return None

        					
            