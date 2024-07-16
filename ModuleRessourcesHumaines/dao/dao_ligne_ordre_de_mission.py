from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_ordre_de_mission
from django.utils import timezone

class dao_ligne_ordre_de_mission(object):
	id = 0
	ordre_mission_id = None
	employe_id = None
	frais_de_mission = 0
	frais_hebergement = 0.0
	status = ''
	auteur_id = None

	@staticmethod
	def toListLigne_ordre_de_mission():
		return Model_Ligne_ordre_de_mission.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigne_ordre_de_mission(ordre_mission_id,employe_id,frais_de_mission,frais_hebergement,status):
		try:
			ligne_ordre_de_mission = dao_ligne_ordre_de_mission()
			ligne_ordre_de_mission.ordre_mission_id = ordre_mission_id
			ligne_ordre_de_mission.employe_id = employe_id
			ligne_ordre_de_mission.frais_de_mission = frais_de_mission
			ligne_ordre_de_mission.frais_hebergement = frais_hebergement
			ligne_ordre_de_mission.status = status
			return ligne_ordre_de_mission
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_ORDRE_DE_MISSION')
			#print(e)
			return None

	@staticmethod
	def toSaveLigne_ordre_de_mission(auteur, objet_dao_Ligne_ordre_de_mission):
		try:
			ligne_ordre_de_mission  = Model_Ligne_ordre_de_mission()
			ligne_ordre_de_mission.ordre_mission_id = objet_dao_Ligne_ordre_de_mission.ordre_mission_id
			ligne_ordre_de_mission.employe_id = objet_dao_Ligne_ordre_de_mission.employe_id
			ligne_ordre_de_mission.frais_de_mission = objet_dao_Ligne_ordre_de_mission.frais_de_mission
			ligne_ordre_de_mission.frais_hebergement = objet_dao_Ligne_ordre_de_mission.frais_hebergement
			ligne_ordre_de_mission.status = objet_dao_Ligne_ordre_de_mission.status
			ligne_ordre_de_mission.created_at = timezone.now()
			ligne_ordre_de_mission.updated_at = timezone.now()
			ligne_ordre_de_mission.auteur_id = auteur.id

			ligne_ordre_de_mission.save()
			return ligne_ordre_de_mission
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_ORDRE_DE_MISSION')
			#print(e)
			return None


	@staticmethod
	def toGetLigneRequeteOfOrdreMission(ordre_mission_id):
		return Model_Ligne_ordre_de_mission.objects.filter(ordre_mission_id=ordre_mission_id)

	@staticmethod
	def toUpdateLigne_ordre_de_mission(id, objet_dao_Ligne_ordre_de_mission):
		try:
			ligne_ordre_de_mission = Model_Ligne_ordre_de_mission.objects.get(pk = id)
			ligne_ordre_de_mission.ordre_mission_id =objet_dao_Ligne_ordre_de_mission.ordre_mission_id
			ligne_ordre_de_mission.employe_id =objet_dao_Ligne_ordre_de_mission.employe_id
			ligne_ordre_de_mission.frais_de_mission =objet_dao_Ligne_ordre_de_mission.frais_de_mission
			ligne_ordre_de_mission.frais_hebergement =objet_dao_Ligne_ordre_de_mission.frais_hebergement
			ligne_ordre_de_mission.status =objet_dao_Ligne_ordre_de_mission.status
			ligne_ordre_de_mission.updated_at = timezone.now()
			ligne_ordre_de_mission.save()
			return ligne_ordre_de_mission
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_ORDRE_DE_MISSION')
			#print(e)
			return None
	@staticmethod
	def toGetLigne_ordre_de_mission(id):
		try:
			return Model_Ligne_ordre_de_mission.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigne_ordre_de_mission(id):
		try:
			ligne_ordre_de_mission = Model_Ligne_ordre_de_mission.objects.get(pk = id)
			ligne_ordre_de_mission.delete()
			return True
		except Exception as e:
			return False