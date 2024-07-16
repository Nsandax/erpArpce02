from __future__ import unicode_literals
from ErpBackOffice.models import Model_ItemBon
from django.utils import timezone

class dao_item_bon_special(object):
    id = 0
    bon_id = 0
    article_id = None
    quantite_demandee = 0
    quantite_fournie = 0
    unite = ""
    prix_unitaire = 0
    prix_lot = 0
    type = ""	
    auteur_id = 0

    @staticmethod
    def toCreateItemBonSpecial(bon_id, article_id, quantite_demandee, quantite_fournie, unite, prix_lot = 0, prix_unitaire = 0):
        try:
            item_bon_special = dao_item_bon_special()
            if bon_id != 0 :
                item_bon_special.bon_id = bon_id
            item_bon_special.article_id = article_id
            item_bon_special.quantite_demandee = quantite_demandee
            item_bon_special.quantite_fournie = quantite_fournie
            item_bon_special.prix_lot = prix_lot
            item_bon_special.prix_unitaire = prix_unitaire
            item_bon_special.unite = unite            
            return item_bon_special
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE L'ITEM ORDER")
            #print(e)
            return None
            
    @staticmethod
    def toSaveItemBonSpecial(auteur, objet_dao_item_bon_special):
        try:
            item_bon_special  = Model_ItemBon()
            item_bon_special.auteur_id = auteur.id
            item_bon_special.bon_id = objet_dao_item_bon_special.bon_id
            item_bon_special.article_id = objet_dao_item_bon_special.article_id
            item_bon_special.quantite_demandee = objet_dao_item_bon_special.quantite_demandee
            item_bon_special.quantite_fournie = objet_dao_item_bon_special.quantite_fournie
            item_bon_special.prix_lot = objet_dao_item_bon_special.prix_lot
            item_bon_special.prix_unitaire = objet_dao_item_bon_special.prix_unitaire
            item_bon_special.type = objet_dao_item_bon_special.type
            item_bon_special.unite = objet_dao_item_bon_special.unite
            item_bon_special.creation_date = timezone.now()
            item_bon_special.save()
            return item_bon_special
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toUpdateItemBonSpecial(id, objet_dao_item_bon_special):
        try:
            item_bon_special = Model_ItemBon.objects.get(pk = id)
            item_bon_special.auteur_id = auteur.id
            item_bon_special.bon_id = objet_dao_item_bon_special.bon_id
            item_bon_special.article_id = objet_dao_item_bon_special.article_id
            item_bon_special.quantite_demandee = objet_dao_item_bon_special.quantite_demandee
            item_bon_special.quantite_fournie = objet_dao_item_bon_special.quantite_fournie
            item_bon_special.prix_lot = objet_dao_item_bon_special.prix_lot
            item_bon_special.prix_unitaire = objet_dao_item_bon_special.prix_unitaire
            item_bon_special.type = objet_dao_item_bon_special.type
            item_bon_special.unite = objet_dao_item_bon_special.unite
            item_bon_special.creation_date = timezone.now()
            item_bon_special.save()
            return item_bon_special
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toGetItemBonSpecial(id):
        try:
            return Model_ItemBon.objects.get(pk = id)
        except Exception as e:
            return None

    @staticmethod
    def toDeleteItemBonSpecial(id):
        try:
            item_bon_special = Model_ItemBon.objects.get(pk = id)
            item_bon_special.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListItemBons(bon_id):
        return Model_ItemBon.objects.filter(bon_id = bon_id)