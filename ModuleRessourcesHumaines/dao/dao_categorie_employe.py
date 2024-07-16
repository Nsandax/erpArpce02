from __future__ import unicode_literals
from ErpBackOffice.models import Model_Categorie_employe
from django.utils import timezone

class dao_categorie_employe(object):
	id = 0
	categorie_id = None
	echelon_id = None
	salaire_base = 0.0
	devise_id = None
	description = ''

	@staticmethod
	def toListCategorie_employe():
		return Model_Categorie_employe.objects.all().order_by('-id')

	@staticmethod
	def toCreateCategorie_employe(categorie,echelon,salaire_base,devise_id,description):
		try:
			categorie_employe = dao_categorie_employe()
			categorie_employe.categorie_id = categorie
			categorie_employe.echelon_id = echelon
			categorie_employe.salaire_base = salaire_base
			categorie_employe.devise_id = devise_id
			categorie_employe.description = description
			return categorie_employe
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA CATEGORIE_EMPLOYE')
			print(e)
			return None

	@staticmethod
	def toSaveCategorie_employe(auteur, objet_dao_Categorie_employe):
		try:
			categorie_employe  = Model_Categorie_employe()
			categorie_employe.categorie_id = objet_dao_Categorie_employe.categorie_id
			categorie_employe.echelon_id = objet_dao_Categorie_employe.echelon_id
			categorie_employe.salaire_base = objet_dao_Categorie_employe.salaire_base
			categorie_employe.devise_id = objet_dao_Categorie_employe.devise_id
			categorie_employe.description = objet_dao_Categorie_employe.description
			categorie_employe.created_at = timezone.now()
			categorie_employe.updated_at = timezone.now()
			categorie_employe.auteur_id = auteur.id

			categorie_employe.save()
			return categorie_employe
		except Exception as e:
			# print('ERREUR LORS DE L ENREGISTREMENT DE LA CATEGORIE_EMPLOYE')
			# print(e)
			return None

	@staticmethod
	def toUpdateCategorie_employe(id, objet_dao_Categorie_employe):
		try:
			categorie_employe = Model_Categorie_employe.objects.get(pk = id)
			categorie_employe.categorie_id =objet_dao_Categorie_employe.categorie_id
			categorie_employe.echelon_id = objet_dao_Categorie_employe.echelon_id
			categorie_employe.salaire_base =objet_dao_Categorie_employe.salaire_base
			categorie_employe.devise_id =objet_dao_Categorie_employe.devise_id
			categorie_employe.description =objet_dao_Categorie_employe.description
			categorie_employe.updated_at = timezone.now()
			categorie_employe.save()
			return categorie_employe
		except Exception as e:
			print('ERREUR LORS DE LA MODIFICATION DE LA CATEGORIE_EMPLOYE')
			print(e)
			return None
	@staticmethod
	def toGetCategorie_employe(id):
		try:
			return Model_Categorie_employe.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetCategorieByLabel(label):
		try:
			label = label.strip().rstrip()
			categories = Model_Categorie_employe.objects.all()
			for categorie in categories:
				if categorie.label == label:
					return categorie
			return None
		except Exception as e:
			# print("Error toGetCategorieByLabel", e)
			return None

	@staticmethod
	def toDeleteCategorie_employe(id):
		try:
			categorie_employe = Model_Categorie_employe.objects.get(pk = id)
			categorie_employe.delete()
			return True
		except Exception as e:
			return False