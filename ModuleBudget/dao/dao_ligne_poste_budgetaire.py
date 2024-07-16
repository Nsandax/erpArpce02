from __future__ import unicode_literals
from ErpBackOffice.models import Model_LignePosteBudgetaire
from django.utils import timezone

class dao_ligne_poste_budgetaire(object):
	id = 0
	compte_id = None
	poste_budgetaire_id = None

	@staticmethod
	def toListLignePoste_budgetaire():
		return Model_LignePosteBudgetaire.objects.all().order_by('-id')

	@staticmethod
	def toListLigneOfPosteBudgetaire(poste_budgetaire_id):
		return Model_LignePosteBudgetaire.objects.filter(poste_budgetaire_id = poste_budgetaire_id)

	@staticmethod
	def toCreateLignePoste_budgetaire(compte_id, poste_budgetaire_id):
		try:
			ligne_poste_budgetaire = dao_ligne_poste_budgetaire()
			ligne_poste_budgetaire.compte_id = compte_id
			ligne_poste_budgetaire.poste_budgetaire_id = poste_budgetaire_id
			return ligne_poste_budgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA POSTE_BUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toSaveLignePoste_budgetaire(objet_dao_ligne_poste_budgetaire):
		try:
			ligne_poste_budgetaire  = Model_LignePosteBudgetaire()
			ligne_poste_budgetaire.compte_id = objet_dao_ligne_poste_budgetaire.compte_id
			ligne_poste_budgetaire.poste_budgetaire_id = objet_dao_ligne_poste_budgetaire.poste_budgetaire_id

			ligne_poste_budgetaire.save()
			return ligne_poste_budgetaire
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA POSTE_BUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toUpdateLignePoste_budgetaire(id, objet_dao_ligne_poste_budgetaire):
		try:
			ligne_poste_budgetaire = Model_LignePosteBudgetaire.objects.get(pk = id)
			ligne_poste_budgetaire.compte_id =objet_dao_ligne_poste_budgetaire.compte_id
			ligne_poste_budgetaire.poste_budgetaire_id = objet_dao_ligne_poste_budgetaire.poste_budgetaire_id

			return ligne_poste_budgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA POSTE_BUDGETAIRE')
			#print(e)
			return None
	@staticmethod
	def toGetLignePoste_budgetaire(id):
		try:
			return Model_LignePosteBudgetaire.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLignePoste_budgetaire(id):
		try:
			ligne_poste_budgetaire = Model_LignePosteBudgetaire.objects.get(pk = id)
			ligne_poste_budgetaire.delete()
			return True
		except Exception as e:
			return False