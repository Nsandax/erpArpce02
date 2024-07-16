from __future__ import unicode_literals
from ErpBackOffice.models import Model_Emploi
from django.utils import timezone

class dao_emploi(object):
	id = 0
	etablissement = ''
	lieu = ''
	fonctions = ''
	categorie_socio_professionnelle = ''
	date_entree = '2010-01-01'
	date_sortie = '2010-01-01'
	employe_id = None

	@staticmethod
	def toListEmploi():
		return Model_Emploi.objects.all().order_by('-id')

	@staticmethod
	def toListEmploiOfEmploye(employe_id):
		return Model_Emploi.objects.filter(employe_id = employe_id)

	@staticmethod
	def toCreateEmploi(etablissement,lieu,fonctions,categorie_socio_professionnelle,date_entree,date_sortie,employe_id):
		try:
			emploi = dao_emploi()
			emploi.etablissement = etablissement
			emploi.lieu = lieu
			emploi.fonctions = fonctions
			emploi.categorie_socio_professionnelle = categorie_socio_professionnelle
			emploi.date_entree = date_entree
			emploi.date_sortie = date_sortie
			emploi.employe_id = employe_id
			return emploi
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA EMPLOI')
			#print(e)
			return None

	@staticmethod
	def toSaveEmploi(auteur, objet_dao_Emploi):
		try:
			emploi  = Model_Emploi()
			emploi.etablissement = objet_dao_Emploi.etablissement
			emploi.lieu = objet_dao_Emploi.lieu
			emploi.fonctions = objet_dao_Emploi.fonctions
			emploi.categorie_socio_professionnelle = objet_dao_Emploi.categorie_socio_professionnelle
			emploi.date_entree = objet_dao_Emploi.date_entree
			emploi.date_sortie = objet_dao_Emploi.date_sortie
			emploi.employe_id = objet_dao_Emploi.employe_id
			emploi.created_at = timezone.now()
			emploi.updated_at = timezone.now()
			emploi.auteur_id = auteur.id

			emploi.save()
			return emploi
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA EMPLOI')
			#print(e)
			return None

	@staticmethod
	def toUpdateEmploi(id, objet_dao_Emploi):
		try:
			emploi = Model_Emploi.objects.get(pk = id)
			emploi.etablissement =objet_dao_Emploi.etablissement
			emploi.lieu =objet_dao_Emploi.lieu
			emploi.fonctions =objet_dao_Emploi.fonctions
			emploi.categorie_socio_professionnelle =objet_dao_Emploi.categorie_socio_professionnelle
			emploi.date_entree =objet_dao_Emploi.date_entree
			emploi.date_sortie =objet_dao_Emploi.date_sortie
			emploi.employe_id =objet_dao_Emploi.employe_id
			emploi.updated_at = timezone.now()
			emploi.save()
			return emploi
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA EMPLOI')
			#print(e)
			return None
	@staticmethod
	def toGetEmploi(id):
		try:
			return Model_Emploi.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteEmploi(id):
		try:
			emploi = Model_Emploi.objects.get(pk = id)
			emploi.delete()
			return True
		except Exception as e:
			return False