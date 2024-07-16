from __future__ import unicode_literals
from ModuleRecouvrement.models import *
from ErpBackOffice.models import *
from django.utils import timezone

class dao_profil_recouvrement(object):
	designation = ''
	description = ''

	@staticmethod
	def toList(query=None):
		try:
			if query == None:
				return Model_Profil_recouvrement.objects.all().order_by('creation_date')

			return Model_Profil_recouvrement.objects.filter(Q(designation__icontains = query) | Q(description__icontains = query)).order_by('creation_date').distinct()
		except Exception as e:
			#print('ERREUR LORS DE LA SELECTION DE LA LISTE PROFIL_RECOUVREMENT')
			#print(e)
			return []

	@staticmethod
	def toCreate(designation = '', description = ''):
		try:
			profil_recouvrement = dao_profil_recouvrement()
			profil_recouvrement.designation = designation
			profil_recouvrement.description = description
			return profil_recouvrement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PROFIL_RECOUVREMENT')
			#print(e)
			return None

	@staticmethod
	def toSave(auteur, objet_dao_profil_recouvrement):
		try:
			profil_recouvrement  = Model_Profil_recouvrement()
			profil_recouvrement.designation = objet_dao_profil_recouvrement.designation
			if objet_dao_profil_recouvrement.description != None : profil_recouvrement.description = objet_dao_profil_recouvrement.description
			if auteur != None : profil_recouvrement.auteur_id = auteur.id

			profil_recouvrement.save()

			return True, profil_recouvrement, ''
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PROFIL_RECOUVREMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toUpdate(id, objet_dao_profil_recouvrement):
		try:
			profil_recouvrement = Model_Profil_recouvrement.objects.get(pk = id)
			profil_recouvrement.designation = objet_dao_profil_recouvrement.designation
			profil_recouvrement.description = objet_dao_profil_recouvrement.description
			profil_recouvrement.save()

			return True, profil_recouvrement, ''
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PROFIL_RECOUVREMENT')
			#print(e)
			return False, None, e

	@staticmethod
	def toGet(id):
		try:
			return Model_Profil_recouvrement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListById(id):
		try:
			return Model_Profil_recouvrement.objects.filter(pk = id)
		except Exception as e:
			return []

	@staticmethod
	def toDelete(id):
		try:
			profil_recouvrement = Model_Profil_recouvrement.objects.get(pk = id)
			profil_recouvrement.delete()
			return True
		except Exception as e:
			return False