from __future__ import unicode_literals
from ModuleStock.models import Model_Operation_Stock
from django.utils import timezone

class dao_operation_stock(object):
	id = 0
	numero = ''
	type = None
	emplacement = None
	emplacement_destination = None
	document = ''
	statut = None
	operation_parent = None

	@staticmethod
	def toList():
		return Model_Operation_Stock.objects.all()

	@staticmethod
	def toCreate(numero,type_id,emplacement_id,emplacement_destination_id,document,statut_id,operation_parent_id):
		try:
			operation_stock = dao_operation_stock()
			operation_stock.numero = numero
			operation_stock.type_id = type_id
			operation_stock.emplacement_id = emplacement_id
			operation_stock.emplacement_destination_id = emplacement_destination_id
			operation_stock.document = document
			operation_stock.statut_id = statut_id
			operation_stock.operation_parent_id = operation_parent_id
			return operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Operation_stock):
		try:
			operation_stock  = Model_Operation_Stock()
			operation_stock.numero = objet_dao_Operation_stock.numero
			operation_stock.type_id = objet_dao_Operation_stock.type_id
			operation_stock.emplacement_id = objet_dao_Operation_stock.emplacement_id
			operation_stock.emplacement_destination_id = objet_dao_Operation_stock.emplacement_destination_id
			operation_stock.document = objet_dao_Operation_stock.document
			operation_stock.statut_id = objet_dao_Operation_stock.statut_id
			operation_stock.operation_parent_id = objet_dao_Operation_stock.operation_parent_id
			operation_stock.auteur_id = auteur.id
			operation_stock.save()
			return operation_stock
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Operation_stock):
		try:
			operation_stock = Model_Operation_Stock.objects.get(pk = id)
			operation_stock.numero =objet_dao_Operation_stock.numero
			operation_stock.type_id =objet_dao_Operation_stock.type_id
			operation_stock.emplacement_id =objet_dao_Operation_stock.emplacement_id
			operation_stock.emplacement_destination_id =objet_dao_Operation_stock.emplacement_destination_id
			operation_stock.document =objet_dao_Operation_stock.document
			operation_stock.statut_id =objet_dao_Operation_stock.statut_id
			operation_stock.operation_parent_id =objet_dao_Operation_stock.operation_parent_id
			operation_stock.save()
			return operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Operation_Stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			operation_stock = Model_Operation_Stock.objects.get(pk = id)
			operation_stock.delete()
			return True
		except Exception as e:
			return False