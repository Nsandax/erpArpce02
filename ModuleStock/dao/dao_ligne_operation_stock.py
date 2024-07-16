from __future__ import unicode_literals
from ModuleStock.models import Model_Ligne_Operation_Stock
from django.utils import timezone

class dao_ligne_operation_stock(object):
	id = 0
	operation = None
	article = None
	series = None
	quantite_demandee = 0.0
	quantite_fait = 0.0
	prix_unitaire = 0.0
	unite = None
	devise = None
	description = ''
	fait = False

	@staticmethod
	def toList():
		return Model_Ligne_Operation_Stock.objects.all()

	@staticmethod
	def toCreate(operation_id,article_id,series_id,quantite_demandee,quantite_fait,prix_unitaire,unite_id,devise_id,description,fait):
		try:
			ligne_operation_stock = dao_ligne_operation_stock()
			ligne_operation_stock.operation_id = operation_id
			ligne_operation_stock.article_id = article_id
			ligne_operation_stock.series_id = series_id
			ligne_operation_stock.quantite_demandee = quantite_demandee
			ligne_operation_stock.quantite_fait = quantite_fait
			ligne_operation_stock.prix_unitaire = prix_unitaire
			ligne_operation_stock.unite_id = unite_id
			ligne_operation_stock.devise_id = devise_id
			ligne_operation_stock.description = description
			ligne_operation_stock.fait = fait
			return ligne_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Ligne_operation_stock):
		try:
			ligne_operation_stock  = Model_Ligne_Operation_Stock()
			ligne_operation_stock.operation_id = objet_dao_Ligne_operation_stock.operation_id
			ligne_operation_stock.article_id = objet_dao_Ligne_operation_stock.article_id
			ligne_operation_stock.series_id = objet_dao_Ligne_operation_stock.series_id
			ligne_operation_stock.quantite_demandee = objet_dao_Ligne_operation_stock.quantite_demandee
			ligne_operation_stock.quantite_fait = objet_dao_Ligne_operation_stock.quantite_fait
			ligne_operation_stock.prix_unitaire = objet_dao_Ligne_operation_stock.prix_unitaire
			ligne_operation_stock.unite_id = objet_dao_Ligne_operation_stock.unite_id
			ligne_operation_stock.devise_id = objet_dao_Ligne_operation_stock.devise_id
			ligne_operation_stock.description = objet_dao_Ligne_operation_stock.description
			ligne_operation_stock.fait = objet_dao_Ligne_operation_stock.fait
			ligne_operation_stock.auteur_id = auteur.id
			ligne_operation_stock.save()
			return ligne_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Ligne_operation_stock):
		try:
			ligne_operation_stock = Model_Ligne_Operation_Stock.objects.get(pk = id)
			ligne_operation_stock.operation_id =objet_dao_Ligne_operation_stock.operation_id
			ligne_operation_stock.article_id =objet_dao_Ligne_operation_stock.article_id
			ligne_operation_stock.series_id =objet_dao_Ligne_operation_stock.series_id
			ligne_operation_stock.quantite_demandee =objet_dao_Ligne_operation_stock.quantite_demandee
			ligne_operation_stock.quantite_fait =objet_dao_Ligne_operation_stock.quantite_fait
			ligne_operation_stock.prix_unitaire =objet_dao_Ligne_operation_stock.prix_unitaire
			ligne_operation_stock.unite_id =objet_dao_Ligne_operation_stock.unite_id
			ligne_operation_stock.devise_id =objet_dao_Ligne_operation_stock.devise_id
			ligne_operation_stock.description =objet_dao_Ligne_operation_stock.description
			ligne_operation_stock.fait =objet_dao_Ligne_operation_stock.fait
			ligne_operation_stock.save()
			return ligne_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Ligne_Operation_Stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			ligne_operation_stock = Model_Ligne_Operation_Stock.objects.get(pk = id)
			ligne_operation_stock.delete()
			return True
		except Exception as e:
			return False