from __future__ import unicode_literals

from ErpBackOffice.models import Model_Emplacement
from django.utils import timezone

class dao_emplacement(object):
    id = 0
    designation = ""
    couloir = 0		
    rayon = 0		
    hauteur = 0
    code_barre = ""
    type_emplacement_id = 0
    est_systeme = False
    auteur_id = 0

    @staticmethod
    def toListEmplacements():
        try:
            return Model_Emplacement.objects.all().order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return []

    @staticmethod
    def toListEmplacementsCrees():
        try:
            return Model_Emplacement.objects.filter(est_systeme = False).order_by("designation")
        except Exception as e:
            #print("ERREUR LORS DU SELECT")
            #print(e)
            return []

    @staticmethod
    def toListEmplacementsInEntrepot(entrepot_id):
        try:
            return Model_Emplacement.objects.filter(parent_id = entrepot_id).order_by("designation")
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []

    @staticmethod
    def toListEmplacementsOfType(type_emplacement_id):
        return Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement_id).order_by("designation")

    @staticmethod
    def toCreateEmplacement(designation, couloir = 0, rayon = 0, hauteur = 0, code_barre = None, type_emplacement_id = 0):        
        try:
            emplacement = dao_emplacement()
            emplacement.designation = designation
            if couloir != 0 :
                emplacement.couloir = couloir
            if rayon != 0 :
                emplacement.rayon = rayon
            if hauteur != 0 :
                emplacement.hauteur = hauteur
            if code_barre != None :
                emplacement.code_barre = code_barre
            if type_emplacement_id != 0 :
                emplacement.type_emplacement_id = type_emplacement_id
            return emplacement
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toSaveEmplacement(auteur, object_dao_emplacement):
        try:
            emplacement = Model_Emplacement()
            emplacement.designation = object_dao_emplacement.designation
            emplacement.couloir = object_dao_emplacement.couloir
            emplacement.rayon = object_dao_emplacement.rayon
            emplacement.hauteur = object_dao_emplacement.hauteur
            emplacement.code_barre = object_dao_emplacement.code_barre
            emplacement.type_emplacement_id = object_dao_emplacement.type_emplacement_id
            emplacement.auteur_id = auteur.id
            emplacement.creation_date = timezone.now()
            emplacement.save()
            return emplacement
        except Exception as e:
            #print("ERREUR LORS DE L'ENREGISTREMENT DE L'EMPLACEMENT")
            #print(e)
            return None

    @staticmethod
    def toUpdateEmplacement(id, object_dao_emplacement):
        try:
            emplacement = Model_Emplacement.objects.get(pk = id)
            emplacement.designation = object_dao_emplacement.designation
            emplacement.couloir = object_dao_emplacement.couloir
            emplacement.rayon = object_dao_emplacement.rayon
            emplacement.hauteur = object_dao_emplacement.hauteur
            emplacement.code_barre = object_dao_emplacement.code_barre
            emplacement.type_emplacement_id = object_dao_emplacement.type_emplacement_id
            emplacement.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE DE L'EMPLACEMENT")
            #print(e)
            return False

    @staticmethod
    def toDeleteEmplacement(id):
        try:
            emplacement = Model_Emplacement.objects.get(pk = id)
            emplacement.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False

    @staticmethod
    def toGetEmplacement(id):
        try:
            return Model_Emplacement.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toGetEmplacementEntree(type_emplacement_entree):
        try:
            return Model_Emplacement.objects.filter(est_systeme = True).get(type_emplacement_id = type_emplacement_entree.id)
        except Exception as e:
            return None

    @staticmethod
    def toGetEmplacementStock(type_emplacement_stock):
        try:
            return Model_Emplacement.objects.filter(est_systeme = True).filter(type_emplacement_id = type_emplacement_stock.id)
        except Exception as e:
            return []

    @staticmethod
    def toGetEmplacementReserve(type_emplacement_reserve):
        try:
            return Model_Emplacement.objects.filter(est_systeme = True).get(type_emplacement_id = type_emplacement_reserve.id)
        except Exception as e:
            return None

    @staticmethod
    def toGetEmplacementEntrepot(type_emplacement_entrepot):
        try:
            return Model_Emplacement.objects.filter(est_systeme = True).get(type_emplacement_id = type_emplacement_entrepot.id)
        except Exception as e:
            return None
    
    @staticmethod
    def toGetEmplacementInternalBusiness():
        try:
            return Model_Emplacement.objects.filter(designation = 'internal_busness_good').filter()
        except Exception as e:
            return None
    
    
    
    @staticmethod
    def toGetEmplacementBySBA():
        try:
            return Model_Emplacement.objects.filter(designation = 'Stockage SBA').first()
        except Exception as e:
            return None

    @staticmethod
    def toGetEmplacementBySMG():
        try:
            return Model_Emplacement.objects.filter(designation = 'Stockage Moyens généraux').first()
        except Exception as e:
            return None

    @staticmethod
    def toGetEmplacementBySI():
        try:
            return Model_Emplacement.objects.filter(designation = 'Stockage IT').first()
        except Exception as e:
            return None