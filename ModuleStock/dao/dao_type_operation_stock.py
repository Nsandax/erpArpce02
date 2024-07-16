from __future__ import unicode_literals
from ModuleStock.models import Model_Type_Operation_Stock
from django.utils import timezone

class dao_type_operation_stock(object):
	id = 0
	designation = ''

	@staticmethod
	def toList():
		return Model_Type_Operation_Stock.objects.all()

	@staticmethod
	def toCreate(designation):
		try:
			type_operation_stock = dao_type_operation_stock()
			type_operation_stock.designation = designation
			return type_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPE_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Type_operation_stock):
		try:
			type_operation_stock  = Model_Type_Operation_Stock()
			type_operation_stock.designation = objet_dao_Type_operation_stock.designation
			type_operation_stock.auteur_id = auteur.id
			type_operation_stock.save()
			return type_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Type_operation_stock):
		try:
			type_operation_stock = Model_Type_Operation_Stock.objects.get(pk = id)
			type_operation_stock.designation =objet_dao_Type_operation_stock.designation
			type_operation_stock.save()
			return type_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Type_Operation_Stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			type_operation_stock = Model_Type_Operation_Stock.objects.get(pk = id)
			type_operation_stock.delete()
			return True
		except Exception as e:
			return False