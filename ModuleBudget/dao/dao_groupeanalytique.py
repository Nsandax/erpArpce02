from __future__ import unicode_literals
from ErpBackOffice.models import Model_GroupeAnalytique
from django.utils import timezone

class dao_groupeanalytique(object):
	id = 0
	designation = ''
	description = ''
	est_projet = False
	groupe_analytique_id = None

	@staticmethod
	def toListGroupeanalytique():
		return Model_GroupeAnalytique.objects.all().order_by('-id')

	@staticmethod
	def toCreateGroupeanalytique(designation,description,groupe_analytique_id, est_projet = False):
		try:
			groupeanalytique = dao_groupeanalytique()
			groupeanalytique.designation = designation
			groupeanalytique.description = description
			groupeanalytique.groupe_analytique_id = groupe_analytique_id
			groupeanalytique.est_projet = est_projet
			return groupeanalytique
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA GROUPEANALYTIQUE')
			#print(e)
			return None

	@staticmethod
	def toSaveGroupeanalytique(auteur, objet_dao_Groupeanalytique):
		try:
			groupeanalytique  = Model_GroupeAnalytique()
			groupeanalytique.designation = objet_dao_Groupeanalytique.designation
			groupeanalytique.description = objet_dao_Groupeanalytique.description
			groupeanalytique.groupe_analytique_id = objet_dao_Groupeanalytique.groupe_analytique_id
			groupeanalytique.est_projet = objet_dao_Groupeanalytique.est_projet
			groupeanalytique.created_at = timezone.now()
			groupeanalytique.updated_at = timezone.now()
			groupeanalytique.auteur_id = auteur.id

			groupeanalytique.save()
			return groupeanalytique
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA GROUPEANALYTIQUE')
			#print(e)
			return None

	@staticmethod
	def toUpdateGroupeanalytique(id, objet_dao_Groupeanalytique):
		try:
			groupeanalytique = Model_GroupeAnalytique.objects.get(pk = id)
			groupeanalytique.designation =objet_dao_Groupeanalytique.designation
			groupeanalytique.description =objet_dao_Groupeanalytique.description
			groupeanalytique.est_projet = objet_dao_Groupeanalytique.est_projet
			groupeanalytique.groupe_analytique_id =objet_dao_Groupeanalytique.groupe_analytique_id
			groupeanalytique.updated_at = timezone.now()
			groupeanalytique.save()
			return groupeanalytique
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA GROUPEANALYTIQUE')
			#print(e)
			return None
	@staticmethod
	def toGetGroupeanalytique(id):
		try:
			return Model_GroupeAnalytique.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteGroupeanalytique(id):
		try:
			groupeanalytique = Model_GroupeAnalytique.objects.get(pk = id)
			groupeanalytique.delete()
			return True
		except Exception as e:
			return False