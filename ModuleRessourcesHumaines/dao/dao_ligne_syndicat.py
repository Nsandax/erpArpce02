from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_Syndicat
from django.utils import timezone

class dao_ligne_syndicat(object):
	id = 0
	syndicat_id = 0
	employe_id = 0
	description = ''

	@staticmethod
	def toListLigneSyndicat():
		return Model_Ligne_Syndicat.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigneSyndicat(syndicat_id,employe_id,description):
		try:
			ligne_syndicat = dao_ligne_syndicat()
			ligne_syndicat.syndicat_id = syndicat_id
			ligne_syndicat.employe_id = employe_id
			ligne_syndicat.description = description
			return ligne_syndicat
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneSyndicat(auteur, objet_dao_ligne_syndicat):
		try:
			ligne_syndicat  = Model_Ligne_Syndicat()
			ligne_syndicat.syndicat_id = objet_dao_ligne_syndicat.syndicat_id
			ligne_syndicat.employe_id = objet_dao_ligne_syndicat.employe_id
			ligne_syndicat.description = objet_dao_ligne_syndicat.description
			ligne_syndicat.created_at = timezone.now()
			ligne_syndicat.auteur_id = auteur.id

			ligne_syndicat.save()
			return ligne_syndicat
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneSyndicat(id, objet_dao_ligne_syndicat):
		try:
			ligne_syndicat = Model_Ligne_Syndicat.objects.get(pk = id)
			ligne_syndicat.syndicat_id = objet_dao_ligne_syndicat.syndicat_id
			ligne_syndicat.employe_id = objet_dao_ligne_syndicat.employe_id
			ligne_syndicat.description = objet_dao_ligne_syndicat.description
			ligne_syndicat.updated_at = timezone.now()
			ligne_syndicat.save()
			return ligne_syndicat
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SYNDICAT')
			#print(e)
			return None
	@staticmethod
	def toGetLigneSyndicat(id):
		try:
			return Model_Ligne_Syndicat.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toListLigneSyndicatBySyndicat(syndicat_id):
		try:
			return Model_Ligne_Syndicat.objects.filter(syndicat_id = syndicat_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLigneSyndicat(id):
		try:
			ligne_syndicat = Model_Ligne_Syndicat.objects.get(pk = id)
			ligne_syndicat.delete()
			return True
		except Exception as e:
			return False



	@staticmethod
	def toDeleteLigneSyndicatOfSyndicat(syndicat_id):
		try:
			return Model_Ligne_Syndicat.objects.filter(syndicat_id = syndicat_id).delete()
		except Exception as e:
			return False