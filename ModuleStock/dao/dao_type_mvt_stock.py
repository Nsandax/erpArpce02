from __future__ import unicode_literals
from ModuleStock.models import Model_Type_Mvt_Stock
from django.utils import timezone

class dao_type_mvt_stock(object):
	id = 0
	designation = ''

	@staticmethod
	def toList():
		return Model_Type_Mvt_Stock.objects.all()

	@staticmethod
	def toCreate(designation):
		try:
			type_mvt_stock = dao_type_mvt_stock()
			type_mvt_stock.designation = designation
			return type_mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Type_mvt_stock):
		try:
			type_mvt_stock  = Model_Type_Mvt_Stock()
			type_mvt_stock.designation = objet_dao_Type_mvt_stock.designation
			type_mvt_stock.auteur_id = auteur.id
			type_mvt_stock.save()
			return type_mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Type_mvt_stock):
		try:
			type_mvt_stock = Model_Type_Mvt_Stock.objects.get(pk = id)
			type_mvt_stock.designation =objet_dao_Type_mvt_stock.designation
			type_mvt_stock.save()
			return type_mvt_stock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_MVT_STOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Type_Mvt_Stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			type_mvt_stock = Model_Type_Mvt_Stock.objects.get(pk = id)
			type_mvt_stock.delete()
			return True
		except Exception as e:
			return False