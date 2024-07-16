from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_demande_achat
from django.db.models import Max
from django.utils import timezone


class dao_ligne_demande_achat(object):
    id = 0
    demande_achat_id = None
    article_id = None
    quantite_demande = 0
    prix_unitaire = 0
    unite_achat_id = None
    description =""
    

    @staticmethod
    def toCreateLigneDemande(demande_achat_id, article_id, quantite_demande, prix_unitaire, unite_achat_id, description):
        try:
            ligne = dao_ligne_demande_achat()
            ligne.demande_achat_id = demande_achat_id
            ligne.article_id = article_id
            ligne.quantite_demande = quantite_demande
            ligne.prix_unitaire = prix_unitaire
            ligne.unite_achat_id = unite_achat_id
            ligne.description = description
            return ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None
    
    @staticmethod
    def toTreatLigneDemande(ligne_id, prix_unitaire):
        try:
            ligne = Model_Ligne_demande_achat.objects.get(pk = ligne_id)
            ligne.prix_unitaire = prix_unitaire
            ligne.save()
            return ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None
    
    @staticmethod
    def toSaveLigneDemande(objet_dao_ligne_ligne):
        try :
            ligne = Model_Ligne_demande_achat()
            ligne.demande_achat_id = objet_dao_ligne_ligne.demande_achat_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.description = objet_dao_ligne_ligne.description
            ligne.save()

            return ligne
        except Exception as e:
            #print("ERREUR SAVE ORDER")
            #print(e)
            return None

    @staticmethod
    def toUpdateLigneDemande(id, objet_dao_ligne_ligne):
        try:
            ligne = Model_Ligne_demande_achat.objects.get(pk = id)
            ligne.demande_achat_id = objet_dao_ligne_ligne.demande_achat_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.description = objet_dao_ligne_ligne.description
            ligne.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGetLigneDemande(id):
        try:
            return Model_Ligne_demande_achat.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toDeleteLigneDemande(id):
        try:
            ligne = Model_Ligne_demande_achat.objects.get(pk = id)
            ligne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListLigneDemandes():
        try:
            lignes = Model_Ligne_demande_achat.objects.all()
            return lignes
        except Exception as e:
            return None

    
    @staticmethod
    def toListLigneOfDemandes(id):
        try:
            lignes = Model_Ligne_demande_achat.objects.filter(demande_achat = id)
            return lignes
        except Exception as e:
            return None

    

'''    @staticmethod
    def toInsertLigneDemande(demande_achat_id, article_id, quantite_demande, prix_unitaire, unite_achat_id, description):
        try:
            maligne = Model_Ligne_demande_achat.object.filter(demande_achat_id= demande_achat_id).filter(article_id = article_id).first()
            if maligne == None:
                ligne = dao_ligne_demande_achat()
                ligne.demande_achat_id = demande_achat_id
                ligne.article_id = article_id
                ligne.quantite_demande = quantite_demande
                ligne.prix_unitaire = prix_unitaire
                ligne.unite_achat_id = unite_achat_id
                ligne.description = description
                dao_ligne_demande_achat.toSaveLigneDemande(ligne)
            else:
                ligne = dao_ligne_demande_achat()
                ligne.demande_achat_id = demande_achat_id
                ligne.article_id = article_id
                ligne.quantite_demande = maligne.quantite_demande + quantite_demande
                ligne.prix_unitaire = prix_unitaire
                ligne.unite_achat_id = unite_achat_id
                ligne.description = maligne.description + description
                dao_ligne_demande_achat.toUpdateLigneDemande(maligne.id, ligne)
            return ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None'''
