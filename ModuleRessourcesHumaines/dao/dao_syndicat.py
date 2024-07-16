from __future__ import unicode_literals
from ErpBackOffice.models import Model_Syndicat
from django.utils import timezone

class dao_syndicat(object):
	id = 0
	designation = ''
	role = ''
	objectifs = ''
	delegue_principal_id = None
	delegue_secondaire_id = None
	description = ''

	@staticmethod
	def toListSyndicat():
		return Model_Syndicat.objects.all().order_by('-id')

	@staticmethod
	def toCreateSyndicat(designation,role,objectifs,delegue_principal_id,delegue_secondaire_id,description):
		try:
			syndicat = dao_syndicat()
			syndicat.designation = designation
			syndicat.role = role
			syndicat.objectifs = objectifs
			syndicat.delegue_principal_id = delegue_principal_id
			syndicat.delegue_secondaire_id = delegue_secondaire_id
			syndicat.description = description
			return syndicat
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toSaveSyndicat(auteur, objet_dao_Syndicat):
		try:
			syndicat  = Model_Syndicat()
			syndicat.designation = objet_dao_Syndicat.designation
			syndicat.role = objet_dao_Syndicat.role
			syndicat.objectifs = objet_dao_Syndicat.objectifs
			syndicat.delegue_principal_id = objet_dao_Syndicat.delegue_principal_id
			syndicat.delegue_secondaire_id = objet_dao_Syndicat.delegue_secondaire_id
			syndicat.description = objet_dao_Syndicat.description
			syndicat.created_at = timezone.now()
			syndicat.updated_at = timezone.now()
			syndicat.auteur_id = auteur.id

			syndicat.save()
			return syndicat
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateSyndicat(id, objet_dao_Syndicat):
		try:
			syndicat = Model_Syndicat.objects.get(pk = id)
			syndicat.designation =objet_dao_Syndicat.designation
			syndicat.role =objet_dao_Syndicat.role
			syndicat.objectifs =objet_dao_Syndicat.objectifs
			syndicat.delegue_principal_id =objet_dao_Syndicat.delegue_principal_id
			syndicat.delegue_secondaire_id =objet_dao_Syndicat.delegue_secondaire_id
			syndicat.description =objet_dao_Syndicat.description
			syndicat.updated_at = timezone.now()
			syndicat.save()
			return syndicat
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SYNDICAT')
			#print(e)
			return None
	@staticmethod
	def toGetSyndicat(id):
		try:
			return Model_Syndicat.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteSyndicat(id):
		try:
			syndicat = Model_Syndicat.objects.get(pk = id)
			syndicat.delete()
			return True
		except Exception as e:
			return False