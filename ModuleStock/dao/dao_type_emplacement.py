from __future__ import unicode_literals
from ModuleStock.models import *
from django.utils import timezone

class dao_type_emplacement(object):
	id = 0
	designation = ''

	@staticmethod
	def toList():
		try:
			Type = Model_Type_Emplacement.objects.all()
			# print('Type EMPL', Type)
			return Type
		except Exception as e:
			return []

	@staticmethod
	def toCreate(designation):
		try:
			type_emplacement = dao_type_emplacement()
			type_emplacement.designation = designation
			return type_emplacement
		except Exception as e:
			# print('ERREUR LORS DE LA CREATION DE LA TYPE_EMPLACEMENT')
			# print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_Type_emplacement):
		try:
			type_emplacement  = Model_Type_Emplacement()
			type_emplacement.designation = objet_dao_Type_emplacement.designation
			type_emplacement.auteur_id = auteur.id
			type_emplacement.save()
			return type_emplacement
		except Exception as e:
			# print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPE_EMPLACEMENT')
			# print(e)
			return None

	@staticmethod
	def toUpdate(id, objet_dao_Type_emplacement):
		try:
			type_emplacement = Model_Type_Emplacement.objects.get(pk = id)
			type_emplacement.designation =objet_dao_Type_emplacement.designation
			type_emplacement.save()
			return type_emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPE_EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toGet(id):
		try:
			return Model_Type_Emplacement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDelete(id):
		try:
			type_emplacement = Model_Type_Emplacement.objects.get(pk = id)
			type_emplacement.delete()
			return True
		except Exception as e:
			return False