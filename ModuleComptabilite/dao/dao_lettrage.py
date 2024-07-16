from __future__ import unicode_literals
from ErpBackOffice.models import Model_Lettrage
from django.utils import timezone
import random
import string

class dao_lettrage(object):
	id = 0
	designation = ''
	description = ''

	@staticmethod
	def toListLettrage():
		return Model_Lettrage.objects.all().order_by('-id')

	@staticmethod
	def toCreateLettrage(designation,description):
		try:
			lettrage = dao_lettrage()
			lettrage.designation = designation
			lettrage.description = description
			return lettrage
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LETTRAGE')
			#print(e)
			return None

	@staticmethod
	def toSaveLettrage(auteur, objet_dao_Lettrage):
		try:
			lettrage  = Model_Lettrage()
			lettrage.designation = objet_dao_Lettrage.designation
			lettrage.description = objet_dao_Lettrage.description
			lettrage.created_at = timezone.now()
			lettrage.updated_at = timezone.now()
			lettrage.auteur_id = auteur.id

			lettrage.save()
			return lettrage
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LETTRAGE')
			#print(e)
			return None

	@staticmethod
	def toUpdateLettrage(id, objet_dao_Lettrage):
		try:
			lettrage = Model_Lettrage.objects.get(pk = id)
			lettrage.designation =objet_dao_Lettrage.designation
			lettrage.description =objet_dao_Lettrage.description
			lettrage.updated_at = timezone.now()
			lettrage.save()
			return lettrage
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LETTRAGE')
			#print(e)
			return None
	@staticmethod
	def toGetLettrage(id):
		try:
			return Model_Lettrage.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLettrage(id):
		try:
			lettrage = Model_Lettrage.objects.get(pk = id)
			lettrage.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateDesignationLettrage():
		uid = ''.join(random.choices(string.digits, k=5))
		return uid