from __future__ import unicode_literals
from ModuleStock.models import Model_Statut_Operation_stock
from django.utils import timezone

class dao_statut_operation_stock(object):
	id = 0
	designation = ''

	@staticmethod
	def toList():
		return Model_Statut_Operation_stock.objects.all()

	@staticmethod
	def toCreate(designation):
		try:
			statut_operation_stock = dao_statut_operation_stock()
			statut_operation_stock.designation = designation
			return statut_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA STATUT_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Statut_operation_stock):
		try:
			statut_operation_stock  = Model_Statut_Operation_stock()
			statut_operation_stock.designation = objet_dao_Statut_operation_stock.designation
			statut_operation_stock.auteur_id = auteur.id
			statut_operation_stock.save()
			return statut_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA STATUT_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Statut_operation_stock):
		try:
			statut_operation_stock = Model_Statut_Operation_stock.objects.get(pk = id)
			statut_operation_stock.designation =objet_dao_Statut_operation_stock.designation
			statut_operation_stock.save()
			return statut_operation_stock
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA STATUT_OPERATION_STOCK')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Statut_Operation_stock.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			statut_operation_stock = Model_Statut_Operation_stock.objects.get(pk = id)
			statut_operation_stock.delete()
			return True
		except Exception as e:
			return False