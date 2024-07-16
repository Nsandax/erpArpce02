from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_Expression
from django.db.models import Max
from django.utils import timezone


class dao_ligne_expression(object):
    id = 0
    expression_id = None
    article_id = None
    quantite_demande = 0
    quantite_restante = 0
    prix_unitaire = 0
    description = None
    unite_achat_id = None


    @staticmethod
    def toCreateLigneExpression(expression_id, article_id, quantite_demande, prix_unitaire, unite_achat_id, description):
        try:
            ligne = dao_ligne_expression()
            ligne.expression_id = expression_id
            ligne.article_id = article_id
            ligne.quantite_demande = quantite_demande
            ligne.quantite_restante = quantite_demande
            ligne.prix_unitaire = prix_unitaire
            #print("unite achat", unite_achat_id)
            ligne.unite_achat_id = unite_achat_id
            ligne.description = description
            return ligne
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None

    @staticmethod
    def toSaveLigneExpression(objet_dao_ligne_ligne):
        try :
            ligne = Model_Ligne_Expression()
            ligne.expression_id = objet_dao_ligne_ligne.expression_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.quantite_restante = objet_dao_ligne_ligne.quantite_demande
            ligne.prix_unitaire = objet_dao_ligne_ligne.prix_unitaire
            #print("unite achat", objet_dao_ligne_ligne.unite_achat_id)
            ligne.unite_achat_id = objet_dao_ligne_ligne.unite_achat_id
            ligne.description = objet_dao_ligne_ligne.description
            ligne.save()

            return ligne
        except Exception as e:
            #print("ERREUR SAVE ORDER")
            #print(e)
            return None

    @staticmethod
    def toUpdateLigneExpression(id, objet_dao_ligne_ligne):
        try:
            ligne = Model_Ligne_Expression.objects.get(pk = id)
            ligne.expression_id = objet_dao_ligne_ligne.expression_id
            ligne.article_id = objet_dao_ligne_ligne.article_id
            ligne.quantite_demande = objet_dao_ligne_ligne.quantite_demande
            ligne.quantite_restante = objet_dao_ligne_ligne.quantite_demande
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
    def toGetLigneExpression(id):
        try:
            return Model_Ligne_Expression.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toDeleteLigneExpression(id):
        try:
            ligne = Model_Ligne_Expression.objects.get(pk = id)
            ligne.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListLigneExpressions():
        try:
            lignes = Model_Ligne_Expression.objects.all().order_by('-id')
            return lignes
        except Exception as e:
            return None


    @staticmethod
    def toListLigneOfExpressions(id):
        try:
            lignes = Model_Ligne_Expression.objects.filter(expression_id = id)
            return lignes
        except Exception as e:
            return None

    @staticmethod
    def toupdateLigneExpressionLivraisonPartielle(id,articleid,qte_restant):
        try:
            # ligne = Model_Ligne_Expression.objects.get(expression_id = id)
            ligne = Model_Ligne_Expression.objects.filter(expression_id = id,article_id = articleid).update(quantite_restante = qte_restant)
            #print('**La ligne d\'expression a modifié est:',ligne)
            # ligne.quantite_restante = qte_restant
            # ligne.save()

            return ligne

        except Exception as e:
            #print(e)
            return None
