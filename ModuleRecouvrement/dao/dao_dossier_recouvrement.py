from __future__ import unicode_literals
from ModuleRecouvrement.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_dossier_recouvrement(object):
	designation = ''
	client_id = None
	description = ''

	@staticmethod
	def toList(query=None):
		try:
			if query == None:
				return Model_Dossier_recouvrement.objects.all().order_by('creation_date')

			return Model_Dossier_recouvrement.objects.filter(Q(designation__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE DOSSIER_RECOUVREMENT')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', client_id = None, description = ''):
		try:
			dossier_recouvrement = dao_dossier_recouvrement()
			dossier_recouvrement.designation = designation
			dossier_recouvrement.client_id = client_id
			dossier_recouvrement.description = description
			return dossier_recouvrement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA DOSSIER_RECOUVREMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_dossier_recouvrement):
		try:
			dossier_recouvrement  = Model_Dossier_recouvrement()
			dossier_recouvrement.designation = objet_dao_dossier_recouvrement.designation
			dossier_recouvrement.client_id = objet_dao_dossier_recouvrement.client_id
			if objet_dao_dossier_recouvrement.description != None : dossier_recouvrement.description = objet_dao_dossier_recouvrement.description
			if auteur != None : dossier_recouvrement.auteur_id = auteur.id

			dossier_recouvrement.save()

			return True, dossier_recouvrement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA DOSSIER_RECOUVREMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_dossier_recouvrement):
		try:
			dossier_recouvrement = Model_Dossier_recouvrement.objects.get(pk = id)
			dossier_recouvrement.designation = objet_dao_dossier_recouvrement.designation
			dossier_recouvrement.client_id = objet_dao_dossier_recouvrement.client_id
			dossier_recouvrement.description = objet_dao_dossier_recouvrement.description
			dossier_recouvrement.save()

			return True, dossier_recouvrement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DOSSIER_RECOUVREMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Dossier_recouvrement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Dossier_recouvrement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			dossier_recouvrement = Model_Dossier_recouvrement.objects.get(pk = id)
			dossier_recouvrement.delete()
			return True
		except Exception as e:
			return False