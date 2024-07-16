from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_requete
from django.utils import timezone

class dao_ligne_requete(object):
	id = 0
	requete_id = None
	employe_id = None
	frais_de_mission = 0
	frais_hebergement = 0.0
	description = ''
	url = ''
	status = 0

	@staticmethod
	def toListLigne_requete():
		return Model_Ligne_requete.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigne_requete(requete_id,employe_id,frais_de_mission,frais_hebergement,description,status):
		try:
			ligne_requete = dao_ligne_requete()
			ligne_requete.requete_id = requete_id
			ligne_requete.employe_id = employe_id
			ligne_requete.frais_de_mission = frais_de_mission
			ligne_requete.frais_hebergement = frais_hebergement
			ligne_requete.description = description
			ligne_requete.status = status
			return ligne_requete
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE_REQUETE')
			#print(e)
			return None

	@staticmethod
	def toSaveLigne_requete(auteur, objet_dao_Ligne_requete):
		try:
			ligne_requete  = Model_Ligne_requete()
			ligne_requete.requete_id = objet_dao_Ligne_requete.requete_id
			ligne_requete.employe_id = objet_dao_Ligne_requete.employe_id
			ligne_requete.frais_de_mission = objet_dao_Ligne_requete.frais_de_mission
			ligne_requete.frais_hebergement = objet_dao_Ligne_requete.frais_hebergement
			ligne_requete.description = objet_dao_Ligne_requete.description
			ligne_requete.created_at = timezone.now()
			ligne_requete.updated_at = timezone.now()
			ligne_requete.status = objet_dao_Ligne_requete.status
			ligne_requete.auteur_id = auteur.id

			ligne_requete.save()
			return ligne_requete
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LIGNE_REQUETE')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigne_requete(id, objet_dao_Ligne_requete):
		try:
			ligne_requete = Model_Ligne_requete.objects.get(pk = id)
			ligne_requete.requete_id =objet_dao_Ligne_requete.requete_id
			ligne_requete.employe_id =objet_dao_Ligne_requete.employe_id
			ligne_requete.frais_de_mission =objet_dao_Ligne_requete.frais_de_mission
			ligne_requete.frais_hebergement =objet_dao_Ligne_requete.frais_hebergement
			ligne_requete.description =objet_dao_Ligne_requete.description
			ligne_requete.status = objet_dao_Ligne_requete.status
			ligne_requete.updated_at = timezone.now()
			ligne_requete.save()
			return ligne_requete
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LIGNE_REQUETE')
			#print(e)
			return None

	@staticmethod
	def toGetLigneRequeteOfRequete(requete_id):
		return Model_Ligne_requete.objects.filter(requete_id=requete_id)

	@staticmethod
	def toGetLigne_requete(id):
		try:
			return Model_Ligne_requete.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLigne_requete(id):
		try:
			ligne_requete = Model_Ligne_requete.objects.get(pk = id)
			ligne_requete.delete()
			return True
		except Exception as e:
			return False