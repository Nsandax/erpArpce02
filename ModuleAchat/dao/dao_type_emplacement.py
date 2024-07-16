
from __future__ import unicode_literals

from ErpBackOffice.models import Model_TypeEmplacement
from django.utils import timezone

class dao_type_emplacement(object):
    id = 0
    designation = ""
    auteur_id = None
    est_systeme = False

    @staticmethod
    def toListTypesEmplacement():
        return Model_TypeEmplacement.objects.all().order_by("designation")

    @staticmethod
    def toListTypesEmplacementCrees():
        return Model_StockArticle.objects.filter(est_systeme = False).order_by("designation")

    @staticmethod
    def toCreateTypeEmplacement(designation, est_systeme=False):        
        try:
            type_emplacement = dao_type_emplacement()
            type_emplacement.designation = designation
            if est_systeme != False :
                type_emplacement.est_systeme = True
            return type_emplacement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DU TYPE D'EMPLACEMENT")
            #print(e)
            return None

    @staticmethod
    def toSaveTypeEmplacement(auteur, object_dao_type_emplacement):
        try:
            type_emplacement = Model_TypeEmplacement()
            type_emplacement.auteur_id = auteur.id
            type_emplacement.designation = object_dao_type_emplacement.designation
            type_emplacement.est_systeme = object_dao_type_emplacement.est_systeme
            type_emplacement.creation_date = timezone.now()
            return type_emplacement
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ARTICLE")
            #print(e)
            return None        

    @staticmethod
    def toUpdateTypeEmplacement(id, object_dao_type_emplacement):
        try:
            type_emplacement = Model_TypeEmplacement.objects.get(pk = id)
            type_emplacement.designation = object_dao_type_emplacement.designation
            type_emplacement.est_systeme = object_dao_type_emplacement.est_systeme
            type_emplacement.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA MISE A JOUR DU TYPE D'EMPLACEMENt")
            #print(e)
            return False        

    @staticmethod
    def toDeleteTypeEmplacement(id):
        try:
            type_emplacement = Model_TypeEmplacement.objects.get(pk = id)
            if type_emplacement.est_systeme != True:
                type_emplacement.delete()
                return True
            return False
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION DU TYPE D'EMPLACEMENT")
            #print(e)
            return False
  
    @staticmethod
    def toGetTypeEmplacement(id):
        try:
            return Model_TypeEmplacement.objects.get(pk = id)
        except Exception as e:
            return None
    
    
  
    @staticmethod
    def toGetTypeEmplacementEntree():
        try:
            return Model_TypeEmplacement.objects.filter(est_systeme = True).get(designation = "IN")
        except Exception as e:
            return None
  
    @staticmethod
    def toGetTypeEmplacementReserve():
        try:
            return Model_TypeEmplacement.objects.filter(est_systeme = True).get(designation = "RESERVE")
        except Exception as e:
            return None

    @staticmethod
    def toGetTypeEmplacementStock():
        try:
            return Model_TypeEmplacement.objects.filter(est_systeme = True).get(designation = "STOCK")
        except Exception as e:
            return None

    @staticmethod
    def toGetTypeEmplacementEntrepot():
        try:
            return Model_TypeEmplacement.objects.filter(est_systeme = True).get(designation = "ENTREPOT")
        except Exception as e:
            return None
        					
            