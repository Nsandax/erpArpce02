from __future__ import unicode_literals
from ErpBackOffice.models import Model_Projet
from django.utils import timezone

class dao_projet(object):
	id = 0
	codeprojet = ''
	designation = ''
	description = ''
	montant = 0
	date_debut = '2010-01-01'
	date_fin = '2010-01-01'
	devise_id = 0
	categoriebudget_id = 0
	pourcentage_alert = 0.0
	message_alert = ""


	@staticmethod
	def toListProjet():
		return Model_Projet.objects.all().order_by('-id')

	@staticmethod
	def toCreateProjet(codeprojet,designation,description,montant,devise_id, date_debut,date_fin,categoriebudget_id = 0,pourcentage_alert = 0.0, message_alert = ""):
		try:
			projet = dao_projet()
			projet.codeprojet = codeprojet
			projet.designation = designation
			projet.description = description
			projet.montant = montant
			projet.devise_id = devise_id
			projet.pourcentage_alert = pourcentage_alert
			projet.message_alert = message_alert
			projet.date_debut = date_debut
			projet.date_fin = date_fin
			projet.categoriebudget_id = categoriebudget_id
			return projet
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PROJET')
			#print(e)
			return None

	@staticmethod
	def toSaveProjet(auteur, objet_dao_Projet):
		try:
			projet  = Model_Projet()
			projet.codeprojet = objet_dao_Projet.codeprojet
			projet.designation = objet_dao_Projet.designation
			projet.description = objet_dao_Projet.description
			projet.montant = objet_dao_Projet.montant
			projet.devise_id = objet_dao_Projet.devise_id
			projet.message_alert = objet_dao_Projet.message_alert
			projet.pourcentage_alert = objet_dao_Projet.pourcentage_alert
			projet.date_debut = objet_dao_Projet.date_debut
			projet.date_fin = objet_dao_Projet.date_fin
			projet.categoriebudget_id = objet_dao_Projet.categoriebudget_id
			projet.created_at = timezone.now()
			projet.updated_at = timezone.now()
			projet.auteur_id = auteur.id

			projet.save()
			return projet
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PROJET')
			#print(e)
			return None

	@staticmethod
	def toUpdateProjet(id, objet_dao_Projet):
		try:
			projet = Model_Projet.objects.get(pk = id)
			projet.codeprojet =objet_dao_Projet.codeprojet
			projet.designation =objet_dao_Projet.designation
			projet.description =objet_dao_Projet.description
			projet.montant = objet_dao_Projet.montant
			projet.devise_id = objet_dao_Projet.devise_id
			projet.date_debut =objet_dao_Projet.date_debut
			projet.date_fin =objet_dao_Projet.date_fin
			projet.categoriebudget_id = objet_dao_Projet.categoriebudget_id
			projet.updated_at = timezone.now()
			projet.save()
			return projet
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PROJET')
			#print(e)
			return None
	@staticmethod
	def toGetProjet(id):
		try:
			return Model_Projet.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteProjet(id):
		try:
			projet = Model_Projet.objects.get(pk = id)
			projet.delete()
			return True
		except Exception as e:
			return False