from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_Competence
from django.utils import timezone

class dao_ligne_competence(object):
	id = 0
	employe_id = 0
	competence = ''
	observation = ''

	@staticmethod
	def toListLigneCompetence():
		return Model_Ligne_Competence.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigneCompetence(competence,observation,employe_id):
		try:
			ligne_competence = dao_ligne_competence()
			ligne_competence.competence = competence
			ligne_competence.employe_id = employe_id
			ligne_competence.observation = observation
			return ligne_competence
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE COMPETENCE')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneCompetence(auteur, objet_dao_ligne_competence):
		try:
			ligne_competence  = Model_Ligne_Competence()
			ligne_competence.competence = objet_dao_ligne_competence.competence
			ligne_competence.employe_id = objet_dao_ligne_competence.employe_id
			ligne_competence.observation = objet_dao_ligne_competence.observation
			ligne_competence.created_at = timezone.now()
			ligne_competence.auteur_id = auteur.id

			ligne_competence.save()
			return ligne_competence
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneCompetence(id, objet_dao_ligne_competence):
		try:
			ligne_competence = Model_Ligne_Competence.objects.get(pk = id)
			ligne_competence.competence = objet_dao_ligne_competence.competence
			ligne_competence.employe_id = objet_dao_ligne_competence.employe_id
			ligne_competence.observation = objet_dao_ligne_competence.observation
			ligne_competence.updated_at = timezone.now()
			ligne_competence.save()
			return ligne_competence
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SYNDICAT')
			#print(e)
			return None
	@staticmethod
	def toGetLigneCompetence(id):
		try:
			return Model_Ligne_Competence.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toListLigneCompetenceByEmploye(employe_id):
		try:
			return Model_Ligne_Competence.objects.filter(employe_id = employe_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLigneCompetence(id):
		try:
			ligne_competence = Model_Ligne_Competence.objects.get(pk = id)
			ligne_competence.delete()
			return True
		except Exception as e:
			return False



	@staticmethod
	def toDeleteLigneCompetenceOfEmploye(employe_id):
		try:
			return Model_Ligne_Competence.objects.filter(employe_id = employe_id).delete()
		except Exception as e:
			return False