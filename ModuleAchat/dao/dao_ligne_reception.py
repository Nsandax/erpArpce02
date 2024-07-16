from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_reception, Model_StockArticle, Model_Article
from django.db.models import Max, Sum, F,FloatField
from django.utils import timezone


class dao_ligne_reception(object):
    id = 0
    bon_reception_id = None
    article_id = None
    quantite_demande = 0
    quantite_fournie = 0
    prix_unitaire = 0
    unite_achat_id = None
    ligne_budgetaire_id = None


    @staticmethod
    def toCreateLigneReception(bon_reception_id, article_id, quantite_demande, prix_unitaire, unite_achat_id, ligne_budgetaire_id = None):
        try:
            ligne = dao_ligne_reception()
            ligne.bon_reception_id = bon_reception_id
            ligne.article_id = article_id
            ligne.quantite_demande = quantite_demande
            ligne.prix_unitaire = prix_unitaire
            ligne.unite_achat_id = unite_achat_id
            ligne.ligne_budgetaire_id = ligne_budgetaire_id
            return ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None

    @staticmethod
    def toSaveLigneReception(objet_dao_ligne_ligne):
        try :
            ligne = Model_Ligne_reception()
            ligne.bon_reception_id = objet_dao_ligne_ligne.bon_reception_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.ligne_budgetaire_id = objet_dao_ligne_ligne.ligne_budgetaire_id
            ligne.save()

            return ligne
        except Exception as e:
            #print("ERREUR SAVE ORDER")
            #print(e)
            return None

    @staticmethod
    def toUpdateLigneReception(id, objet_dao_ligne_ligne):
        try:
            ligne = Model_Ligne_reception.objects.get(pk = id)
            ligne.bon_reception_id = objet_dao_ligne_ligne.bon_reception_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.ligne_budgetaire_id = objet_dao_ligne_ligne.ligne_budgetaire_id
            ligne.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toGetLigneReception(id):
        try:
            return Model_Ligne_reception.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toDeleteLigneReception(id):
        try:
            ligne = Model_Ligne_reception.objects.get(pk = id)
            ligne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListLigneReceptions():
        try:
            lignes = Model_Ligne_reception.objects.all().order_by('-id')
            return lignes
        except Exception as e:
            return None


    @staticmethod
    def toListLigneOfReceptions(id):
        try:
            lignes = Model_Ligne_reception.objects.filter(bon_reception = id)
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toListLigneOfReceptionsSortByLigneBudgetaire(id):
        try:
            #lignes = Model_Ligne_reception.objects.filter(bon_reception_id = id).values('ligne_budgetaire_id').annotate(montant_total=Sum('prix_unitaire',field="prix_unitaire*quantite_demande"))
            lignes = Model_Ligne_reception.objects.filter(bon_reception_id = id).values('ligne_budgetaire_id').annotate(montant_total=Sum(F('prix_unitaire') * F('quantite_demande'),output_field=FloatField()))
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toListLignesDuStock(stock_article_id):
        return Model_Ligne_reception.objects.filter(stock_article_id = stock_article_id)

    @staticmethod
    def toListLignesDeArticle(article_id):
        try:
            list = []
            list_stocks = Model_StockArticle.objects.filter(article_id = article_id)
            for stock in list_stocks :
                lignes_fourniture = dao_ligne_reception.toListLignesDuStock(stock.id)

                for ligne in lignes_fourniture :
                    list.append(ligne)
            return list
        except Exception as e:
            ##print("ERREUR")
            ##print(e)
            return []

    @staticmethod
    def toGetMontantTotalOfBon(id):
        try:
            lignes = Model_Ligne_reception.objects.filter(bon_reception = id)
            ##print(lignes)

            somme = 0
            for ligne in lignes:
                ##print(ligne)
                ##print(ligne.quantite_demande)
                ##print(ligne.prix_unitaire)
                somme = somme + ligne.quantite_demande * ligne.prix_unitaire
            return somme
        except Exception as e:
            return None
