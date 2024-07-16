from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_postulation
from django.utils import timezone

class dao_ligne_postulation(object):
	id = 0
	employe_id = 0
	date_postulation = None
	recrutement_id = 0
	auteur_id = 0

	@staticmethod
	def toListLignePostulation():
		return Model_Ligne_postulation.objects.all().order_by('-id')

	@staticmethod
	def toCreateLignePostulation(recrutement_id,employe_id, date_postulation):
		try:
			ligne_postulation = dao_ligne_postulation()
			ligne_postulation.recrutement_id = recrutement_id
			ligne_postulation.employe_id = employe_id
			ligne_postulation.date_postulation = date_postulation
			return ligne_postulation
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE postulation')
			#print(e)
			return None

	@staticmethod
	def toSaveLignePostulation(auteur, objet_dao_ligne_postulation):
		try:
			ligne_postulation  = Model_Ligne_postulation()
			ligne_postulation.recrutement = objet_dao_ligne_postulation.recrutement_id
			ligne_postulation.employe_id = objet_dao_ligne_postulation.employe_id
			ligne_postulation.date_postulation = objet_dao_ligne_postulation.date_postulation
			ligne_postulation.auteur_id = auteur.id

			ligne_postulation.save()
			return ligne_postulation
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLignePostulation(id, objet_dao_ligne_postulation):
		try:
			ligne_postulation = Model_Ligne_postulation.objects.get(pk = id)
			ligne_postulation.recrutement = objet_dao_ligne_postulation.recrutement_id
			ligne_postulation.employe_id = objet_dao_ligne_postulation.employe_id
			ligne_postulation.date_postulation = objet_dao_ligne_postulation.date_postulation
			ligne_postulation.save()
			return ligne_postulation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SYNDICAT')
			#print(e)
			return None
	@staticmethod
	def toGetLignePostulation(id):
		try:
			return Model_Ligne_postulation.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toListLignePostulationByEmploye(date_postulation):
		try:
			return Model_Ligne_postulation.objects.filter(date_postulation = date_postulation)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLignePostulation(id):
		try:
			ligne_postulation = Model_Ligne_postulation.objects.get(pk = id)
			ligne_postulation.delete()
			return True
		except Exception as e:
			return False



	@staticmethod
	def toDeleteLignePostulationOfEmploye(employe_id):
		try:
			return Model_Ligne_postulation.objects.filter(employe_id = employe_id).delete()
		except Exception as e:
			return False