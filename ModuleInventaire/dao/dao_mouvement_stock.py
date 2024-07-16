from __future__ import unicode_literals
from ErpBackOffice.models import Model_Mouvement_stock
from django.utils import timezone

class dao_mouvement_stock(object):
	id = 0
	quantite_mouvement=0
	details=''
	type=''
	stock_article_entrant_id = 0
	stock_article_sortant_id = 0
	bon_commande_id = 0
	bon_reception_id = 0
	bon_inventaire_id = 0
	bon_transfert_id = 0
	auteur_id = 0

	@staticmethod
	def toListMouvementStock():
		return Model_Mouvement_stock.objects.all().order_by('-id')


	@staticmethod
	def toListMouvementStockByAuteur(user_id):
		return Model_Mouvement_stock.objects.filter(auteur_id = user_id)

	@staticmethod
	def toCreateMouvementStock(quantite_mouvement,details,type,stock_article_entrant_id=None,stock_article_sortant_id=None,bon_commande_id=None,bon_reception_id=None,bon_inventaire_id=None,bon_transfert_id=None):
		try:
			mouvement_stock = dao_mouvement_stock()
			mouvement_stock.quantite_mouvement = quantite_mouvement
			mouvement_stock.details = details
			mouvement_stock.type = type
			mouvement_stock.stock_article_entrant_id = stock_article_entrant_id
			mouvement_stock.stock_article_sortant_id = stock_article_sortant_id
			mouvement_stock.bon_commande_id = bon_commande_id
			mouvement_stock.bon_reception_id = bon_reception_id
			mouvement_stock.bon_inventaire_id = bon_inventaire_id
			mouvement_stock.bon_transfert_id = bon_transfert_id
			return mouvement_stock
		except Exception as e:
			# print('ERREUR LORS DE LA CREATION DE LA MOUVEMENT_STOCK')
			# print(e)
			return None

	@staticmethod
	def toSaveMouvementStock(auteur,objet_dao_Mouvement_stock):
		try:
			mouvement_stock  = Model_Mouvement_stock()
			mouvement_stock.reference = dao_mouvement_stock.toGenerateNumeroMouvement()
			mouvement_stock.quantite_mouvement =objet_dao_Mouvement_stock.quantite_mouvement
			mouvement_stock.details =objet_dao_Mouvement_stock.details
			mouvement_stock.type =objet_dao_Mouvement_stock.type
			mouvement_stock.creation_date = timezone.now()
			mouvement_stock.stock_article_entrant_id = objet_dao_Mouvement_stock.stock_article_entrant_id
			mouvement_stock.stock_article_sortant_id = objet_dao_Mouvement_stock.stock_article_sortant_id
			mouvement_stock.bon_reception_id = objet_dao_Mouvement_stock.bon_reception_id
			mouvement_stock.bon_commande_id = objet_dao_Mouvement_stock.bon_commande_id
			mouvement_stock.bon_transfert_id = objet_dao_Mouvement_stock.bon_transfert_id
			mouvement_stock.bon_inventaire_id = objet_dao_Mouvement_stock.bon_inventaire_id
			mouvement_stock.auteur_id = auteur.id
			mouvement_stock.save()
			return mouvement_stock
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA MOUVEMENT_STOCK')
			print(e)
			return None

	@staticmethod
	def toUpdateMouvementStock(id, objet_dao_Mouvement_stock):
		try:
			mouvement_stock = Model_Mouvement_stock.objects.get(pk = id)
			mouvement_stock.quantite_mouvement =objet_dao_Mouvement_stock.quantite_mouvement
			mouvement_stock.details =objet_dao_Mouvement_stock.details
			mouvement_stock.type =objet_dao_Mouvement_stock.type
			mouvement_stock.stock_article_entrant_id = objet_dao_Mouvement_stock.stock_article_entrant_id
			mouvement_stock.stock_article_sortant_id = objet_dao_Mouvement_stock.stock_article_sortant_id
			mouvement_stock.bon_reception_id = objet_dao_Mouvement_stock.bon_reception_id
			mouvement_stock.bon_commande_id = objet_dao_Mouvement_stock.bon_commande_id
			mouvement_stock.bon_transfert_id = objet_dao_Mouvement_stock.bon_transfert_id
			mouvement_stock.bon_inventaire_id = objet_dao_Mouvement_stock.bon_inventaire_id
			mouvement_stock.save()
			return mouvement_stock
		except Exception as e:
			##print('ERREUR LORS DE LA MODIFICATION DE LA MOUVEMENT_STOCK')
			##print(e)
			return None
	@staticmethod
	def toGetMouvementStock(id):
		try:
			return Model_Mouvement_stock.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteMouvementStock(id):
		try:
			mouvement_stock = Model_Mouvement_stock.objects.get(pk = id)
			mouvement_stock.delete()
			return True
		except Exception as e:
			##print("ERREUR LORS DU SELECT")
			##print(e)
			return False

	@staticmethod
	def toListMouvementStockOfIventaire(bon_inventaire_id):
		try:
			return Model_Mouvement_stock.objects.filter(bon_inventaire_id = bon_inventaire_id)
		except Exception as e:
			##print("ERREUR LORS DU SELECT")
			##print(e)
			return []

	@staticmethod
	def toGenerateNumeroMouvement():
		total_mouvements = dao_mouvement_stock.toListMouvementStock().count()
		total_mouvements = total_mouvements + 1
		temp_numero = str(total_mouvements)

		for i in range(len(str(total_mouvements)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "MV-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero