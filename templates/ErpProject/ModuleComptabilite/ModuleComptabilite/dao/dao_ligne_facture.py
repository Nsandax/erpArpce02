from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_facture, Model_StockArticle, Model_Article
from django.db.models import Max
from django.utils import timezone
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId

class dao_ligne_facture(object):
    id = 0
    designation = ""
    facture_id = None
    article_id = None
    quantite_demande = 0
    prix_unitaire = 0
    unite_achat_id = None
    ligne_montant_taxe = 0
    remise = 0
    compte_comptable_id = None


    @staticmethod
    def toCreateLigneFacture(designation,facture_id, article_id, quantite_demande, prix_unitaire, unite_achat_id, ligne_montant_taxe = 0, remise = 0, compte_comptable_id = None):
        try:
            ligne = dao_ligne_facture()
            ligne.designation = designation
            ligne.facture_id = facture_id
            ligne.article_id = article_id
            ligne.quantite_demande = quantite_demande
            ligne.prix_unitaire = prix_unitaire
            ligne.unite_achat_id = unite_achat_id
            ligne.remise = remise
            ligne.ligne_montant_taxe = ligne_montant_taxe
            ligne.compte_comptable_id = compte_comptable_id
            return ligne
        except Exception as e:
            print("ERREUR LORS DE LA CREATION DE ORDRE")
            print(e)
            return None

    @staticmethod
    def toSaveLigneFacture(objet_dao_ligne_ligne):
        try :
            ligne = Model_Ligne_facture()
            ligne.designation  = objet_dao_ligne_ligne.designation
            ligne.facture_id = objet_dao_ligne_ligne.facture_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande

            print("/////",objet_dao_ligne_ligne.quantite_demande, objet_dao_ligne_ligne.prix_unitaire)

            total = float(objet_dao_ligne_ligne.quantite_demande) * float(objet_dao_ligne_ligne.prix_unitaire)
            ligne.prix_lot = total - (total * objet_dao_ligne_ligne.remise / 100 )
            print("-----------------", total)

            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.remise = objet_dao_ligne_ligne.remise
            print("Laure manaudao", objet_dao_ligne_ligne.ligne_montant_taxe)
            ligne.ligne_montant_taxe = makeFloat(objet_dao_ligne_ligne.ligne_montant_taxe)
            ligne.compte_comptable_id = objet_dao_ligne_ligne.compte_comptable_id
            ligne.save()
            print("qlq chose se psse ici")

            return ligne
        except Exception as e:
            print("ERREUR SAVE ORDER of minimum")
            print(e)
            return None

    @staticmethod
    def toUpdateLigneFacture(id, objet_dao_ligne_ligne):
        try:
            ligne = Model_Ligne_facture.objects.get(pk = id)
            ligne.designation  = objet_dao_ligne_ligne.designation
            ligne.facture_id = objet_dao_ligne_ligne.facture_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.remise = makeFloat(objet_dao_ligne_ligne.remise)
            ligne.ligne_montant_taxe = objet_dao_ligne_ligne.ligne_montant_taxe
            ligne.compte_comptable_id = objet_dao_ligne_ligne.compte_comptable_id
            ligne.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGetLigneFacture(id):
        try:
            return Model_Ligne_facture.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toDeleteLigneFacture(id):
        try:
            ligne = Model_Ligne_facture.objects.get(pk = id)
            ligne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListLigneFactures():
        try:
            lignes = Model_Ligne_facture.objects.all().order_by('-id')
            return lignes
        except Exception as e:
            return None


    @staticmethod
    def toListLigneOfFacture(id):
        try:
            lignes = Model_Ligne_facture.objects.filter(facture_id = id)
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toListLignesDeArticle(article_id):
        try:
            list = []
            list_stocks = Model_StockArticle.objects.filter(article_id = article_id)
            for stock in list_stocks :
                lignes_fourniture = dao_ligne_facture.toListLignesDuStock(stock.id)

                for ligne in lignes_fourniture :
                    list.append(ligne)
            return list
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return []
