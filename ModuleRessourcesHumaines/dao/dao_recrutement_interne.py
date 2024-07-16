from __future__ import unicode_literals
from ErpBackOffice.models import Model_Recrutement_interne
from django.utils import timezone

class dao_recrutement_interne(object):
	id = 0
	designation = ''
	description = ''
	date_debut = '2010-01-01'
	date_fin = '2010-01-01'
	est_fini = False
	service_id = None

	@staticmethod
	def toListRecrutement_interne():
		return Model_Recrutement_interne.objects.all().order_by('-id')

	@staticmethod
	def toListRecrutement_interneByAuteur():
		return Model_Recrutement_interne.objects.filter(auteur_id=user_id)

	@staticmethod
	def toCreateRecrutement_interne(designation,description,date_debut,date_fin,est_fini,service_id):
		try:
			recrutement_interne = dao_recrutement_interne()
			recrutement_interne.designation = designation
			recrutement_interne.description = description
			recrutement_interne.date_debut = date_debut
			recrutement_interne.date_fin = date_fin
			recrutement_interne.est_fini = est_fini
			recrutement_interne.service_id = service_id
			return recrutement_interne
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA RECRUTEMENT_INTERNE')
			#print(e)
			return None

	@staticmethod
	def toSaveRecrutement_interne(auteur, objet_dao_Recrutement_interne):
		try:
			recrutement_interne  = Model_Recrutement_interne()
			recrutement_interne.designation = objet_dao_Recrutement_interne.designation
			recrutement_interne.description = objet_dao_Recrutement_interne.description
			recrutement_interne.date_debut = objet_dao_Recrutement_interne.date_debut
			recrutement_interne.date_fin = objet_dao_Recrutement_interne.date_fin
			recrutement_interne.est_fini = objet_dao_Recrutement_interne.est_fini
			recrutement_interne.service_id = objet_dao_Recrutement_interne.service_id
			recrutement_interne.created_at = timezone.now()
			recrutement_interne.updated_at = timezone.now()
			recrutement_interne.auteur_id = auteur.id

			recrutement_interne.save()
			return recrutement_interne
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA RECRUTEMENT_INTERNE')
			#print(e)
			return None

	@staticmethod
	def toUpdateRecrutement_interne(id, objet_dao_Recrutement_interne):
		try:
			recrutement_interne = Model_Recrutement_interne.objects.get(pk = id)
			recrutement_interne.designation =objet_dao_Recrutement_interne.designation
			recrutement_interne.description =objet_dao_Recrutement_interne.description
			recrutement_interne.date_debut =objet_dao_Recrutement_interne.date_debut
			recrutement_interne.date_fin =objet_dao_Recrutement_interne.date_fin
			recrutement_interne.est_fini =objet_dao_Recrutement_interne.est_fini
			recrutement_interne.service_id =objet_dao_Recrutement_interne.service_id
			recrutement_interne.updated_at = timezone.now()
			recrutement_interne.save()
			return recrutement_interne
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA RECRUTEMENT_INTERNE')
			#print(e)
			return None
	@staticmethod
	def toGetRecrutement_interne(id):
		try:
			return Model_Recrutement_interne.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteRecrutement_interne(id):
		try:
			recrutement_interne = Model_Recrutement_interne.objects.get(pk = id)
			recrutement_interne.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGet_Recru_by_year():
		List_Recru_Tot={}
		try:
			Year = timezone.now().year
			somme_year =0
			i = 2010
			while i <= Year:
				somme_year += Model_Recrutement_interne.objects.filter(date_debut__year = i).count()
				List_Recru_Tot[i] = somme_year
				somme_year = 0
				i = i + 1

			#print('** Liste Recru**%s' %List_Recru_Tot)
			return List_Recru_Tot
		except Exception as e:
			#print('**Erreur Part de Recru Mobilite par year** %s' %List_Recru_Tot)
			#print(e)
			return List_Recru_Tot