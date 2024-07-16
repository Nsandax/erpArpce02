from __future__ import unicode_literals
from ErpBackOffice.models import Model_Billeterie, Model_LigneBilleterie
from django.utils import timezone

class dao_billeterie(object):
	id = 0
	reference = ''
	total = 0

	
	@staticmethod
	def toCreateBilleterie(reference, total):
		try:
			billeterie = dao_billeterie()
			billeterie.reference = reference
			billeterie.total = total
			return billeterie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA billeterie')
			#print(e)
			return None

	@staticmethod
	def toSaveBilleterie(auteur, objet_dao_billeterie):
		try:
			billeterie  = Model_Billeterie()
			billeterie.reference = objet_dao_billeterie.reference
			billeterie.total = objet_dao_billeterie.total
			billeterie.created_at = timezone.now()
			billeterie.updated_at = timezone.now()
			billeterie.auteur_id = auteur.id

			billeterie.save()
			return billeterie
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA billeterie')
			#print(e)
			return None

	@staticmethod
	def toUpdateBilleterie(id, objet_dao_billeterie):
		try:
			billeterie = Model_Billeterie.objects.get(pk = id)
			billeterie.reference = objet_dao_billeterie.reference
			billeterie.total = objet_dao_billeterie.total
			billeterie.updated_at = timezone.now()
			billeterie.save()
			return billeterie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA billeterie')
			#print(e)
			return None
	@staticmethod
	def toGetBilleterie(id):
		try:
			return Model_Billeterie.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteBilleterie(id):
		try:
			billeterie = Model_Billeterie.objects.get(pk = id)
			billeterie.delete()
			return True
		except Exception as e:
			return False
