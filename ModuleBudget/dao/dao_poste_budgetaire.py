from __future__ import unicode_literals
from ErpBackOffice.models import Model_Poste_budgetaire
from django.utils import timezone

class dao_poste_budgetaire(object):
	id = 0
	code = ''
	designation = ''

	@staticmethod
	def toListPoste_budgetaire():
		return Model_Poste_budgetaire.objects.all().order_by('-id')



	@staticmethod
	def toCreatePoste_budgetaire(code,designation):
		try:
			poste_budgetaire = dao_poste_budgetaire()
			poste_budgetaire.code = code
			poste_budgetaire.designation = designation
			return poste_budgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA POSTE_BUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toSavePoste_budgetaire(auteur, objet_dao_Poste_budgetaire):
		try:
			poste_budgetaire  = Model_Poste_budgetaire()
			poste_budgetaire.code = objet_dao_Poste_budgetaire.code
			poste_budgetaire.designation = objet_dao_Poste_budgetaire.designation
			poste_budgetaire.created_at = timezone.now()
			poste_budgetaire.updated_at = timezone.now()
			poste_budgetaire.auteur_id = auteur.id

			poste_budgetaire.save()
			return poste_budgetaire
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA POSTE_BUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toUpdatePoste_budgetaire(id, objet_dao_Poste_budgetaire):
		try:
			poste_budgetaire = Model_Poste_budgetaire.objects.get(pk = id)
			poste_budgetaire.code =objet_dao_Poste_budgetaire.code
			poste_budgetaire.designation =objet_dao_Poste_budgetaire.designation
			poste_budgetaire.updated_at = timezone.now()
			poste_budgetaire.save()
			return poste_budgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA POSTE_BUDGETAIRE')
			#print(e)
			return None
	@staticmethod
	def toGetPoste_budgetaire(id):
		try:
			return Model_Poste_budgetaire.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeletePoste_budgetaire(id):
		try:
			poste_budgetaire = Model_Poste_budgetaire.objects.get(pk = id)
			poste_budgetaire.delete()
			return True
		except Exception as e:
			return False