from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_releve
from django.utils import timezone

class dao_ligne_releve(object):
	id = 0
	employe_id = 0
	superieur_id = 0
	degre = ''
	created_at = None
	update_at = None
	auteur_id = 0

	@staticmethod
	def toListLigneReleve():
		return Model_Ligne_releve.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigneReleve(degre,employe_id, superieur_id):
		try:
			ligne_releve = dao_ligne_releve()
			ligne_releve.degre = degre
			ligne_releve.employe_id = employe_id
			ligne_releve.superieur_id = superieur_id
			return ligne_releve
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE releve')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneReleve(auteur, objet_dao_ligne_releve):
		try:
			ligne_releve  = Model_Ligne_releve()
			ligne_releve.degre = objet_dao_ligne_releve.degre
			ligne_releve.employe_id = objet_dao_ligne_releve.employe_id
			ligne_releve.superieur_id = objet_dao_ligne_releve.superieur_id
			ligne_releve.created_at = timezone.now()
			ligne_releve.auteur_id = auteur.id

			ligne_releve.save()
			return ligne_releve
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneReleve(id, objet_dao_ligne_releve):
		try:
			ligne_releve = Model_Ligne_releve.objects.get(pk = id)
			ligne_releve.degre = objet_dao_ligne_releve.degre
			ligne_releve.employe_id = objet_dao_ligne_releve.employe_id
			ligne_releve.superieur_id = objet_dao_ligne_releve.superieur_id
			ligne_releve.updated_at = timezone.now()
			ligne_releve.save()
			return ligne_releve
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SYNDICAT')
			#print(e)
			return None
	@staticmethod
	def toGetLigneReleve(id):
		try:
			return Model_Ligne_releve.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toListLigneReleveByEmploye(superieur_id):
		try:
			return Model_Ligne_releve.objects.filter(superieur_id = superieur_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLignereleve(id):
		try:
			ligne_releve = Model_Ligne_releve.objects.get(pk = id)
			ligne_releve.delete()
			return True
		except Exception as e:
			return False



	@staticmethod
	def toDeleteLigneReleveOfEmploye(employe_id):
		try:
			return Model_Ligne_releve.objects.filter(employe_id = employe_id).delete()
		except Exception as e:
			return False