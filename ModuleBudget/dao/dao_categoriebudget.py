from __future__ import unicode_literals
from ErpBackOffice.models import Model_Categoriebudget, Model_LigneBudgetaire
from django.utils import timezone

class dao_categoriebudget(object):
	id = 0
	designation = ''
	description = ''
	type = None

	@staticmethod
	def toListCategoriebudget():
		return Model_Categoriebudget.objects.all().order_by('-id')

	@staticmethod
	def toListCategoriebudgetOfType(type):
		try:
			categories = Model_Categoriebudget.objects.filter(type = type)
			return categories
		except Exception as e:
			return None


	@staticmethod
	def toCreateCategoriebudget(designation,description,type = 2):
		try:
			categoriebudget = dao_categoriebudget()
			categoriebudget.designation = designation
			categoriebudget.description = description
			categoriebudget.type = type
			return categoriebudget
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CATEGORIEBUDGET')
			#print(e)
			return None

	@staticmethod
	def toSaveCategoriebudget(auteur, objet_dao_Categoriebudget):
		try:
			categoriebudget  = Model_Categoriebudget()
			categoriebudget.designation = objet_dao_Categoriebudget.designation
			categoriebudget.description = objet_dao_Categoriebudget.description
			categoriebudget.type = objet_dao_Categoriebudget.type
			categoriebudget.created_at = timezone.now()
			categoriebudget.updated_at = timezone.now()
			categoriebudget.auteur_id = auteur.id

			categoriebudget.save()
			return categoriebudget
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CATEGORIEBUDGET')
			#print(e)
			return None

	@staticmethod
	def toUpdateCategoriebudget(id, objet_dao_Categoriebudget):
		try:
			categoriebudget = Model_Categoriebudget.objects.get(pk = id)
			categoriebudget.designation =objet_dao_Categoriebudget.designation
			categoriebudget.description =objet_dao_Categoriebudget.description
			categoriebudget.type =objet_dao_Categoriebudget.type
			categoriebudget.updated_at = timezone.now()
			categoriebudget.save()
			return categoriebudget
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CATEGORIEBUDGET')
			#print(e)
			return None
	@staticmethod
	def toGetCategoriebudget(id):
		try:
			return Model_Categoriebudget.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteCategoriebudget(id):
		try:
			categoriebudget = Model_Categoriebudget.objects.get(pk = id)
			categoriebudget.delete()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toComputeBudgetByCategorie():
		list_categorie = []
		try:

			categoriebudgets = Model_Categoriebudget.objects.all()
			#print("categorie", categoriebudgets)
			for categorie in categoriebudgets:
				categorie_budget = {
				'categorie_budget':'',
				'dotation':0,
				'engagements':0,
				'reels':0,
				'ecart':0,
			}
				#print("une categorie", categorie)
				categorie_budget['categorie_budget'] = categorie.designation
				lignes = Model_LigneBudgetaire.objects.filter(budget__categoriebudget = categorie)
				for ligne in lignes:
					#print('inside')
					categorie_budget['dotation'] += ligne.montant_alloue
					categorie_budget['engagements'] += float(ligne.valeur_engagement)
					categorie_budget['reels'] += float(ligne.valeur_reel)
					categorie_budget['ecart'] += ligne.montant_alloue - float(ligne.valeur_engagement) - float(ligne.valeur_reel)
				list_categorie.append(categorie_budget)
			return list_categorie
		except Exception as e:
			#print(e)
			return list_categorie

	@staticmethod
	def toGetTypecategorieBudgetbyid(id):
		try:
			categorie = Model_Categoriebudget.objects.get(pk = id)
			return categorie.type
		except Exception as e:
			print(e)
			return None


