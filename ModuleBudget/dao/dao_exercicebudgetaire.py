from __future__ import unicode_literals
from ErpBackOffice.models import Model_Exercicebudgetaire
from ErpBackOffice.dao.dao_devise import dao_devise
from django.utils import timezone

class dao_exercicebudgetaire(object):
	id = 0
	designation = ''
	montant = 0.0
	annee = 0
	date_debut = None
	date_fin = None

	@staticmethod
	def toListExercicebudgetaire():
		return Model_Exercicebudgetaire.objects.all().order_by('-id')

	@staticmethod
	def toCreateExercicebudgetaire(designation,montant,annee, date_debut, date_fin):
		try:
			exercicebudgetaire = dao_exercicebudgetaire()
			exercicebudgetaire.designation = designation
			exercicebudgetaire.montant = montant
			exercicebudgetaire.annee = annee
			exercicebudgetaire.date_debut = date_debut
			exercicebudgetaire.date_fin = date_fin
			return exercicebudgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA EXERCICEBUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toSaveExercicebudgetaire(auteur, objet_dao_Exercicebudgetaire):
		try:
			exercicebudgetaire  = Model_Exercicebudgetaire()
			exercicebudgetaire.designation = objet_dao_Exercicebudgetaire.designation
			exercicebudgetaire.montant = objet_dao_Exercicebudgetaire.montant
			exercicebudgetaire.annee = objet_dao_Exercicebudgetaire.annee
			exercicebudgetaire.devise = dao_devise.toGetDeviseReference()
			exercicebudgetaire.date_debut = objet_dao_Exercicebudgetaire.date_debut
			exercicebudgetaire.date_fin = objet_dao_Exercicebudgetaire.date_fin
			exercicebudgetaire.created_at = timezone.now()
			exercicebudgetaire.updated_at = timezone.now()
			exercicebudgetaire.auteur_id = auteur.id

			exercicebudgetaire.save()
			return exercicebudgetaire
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA EXERCICEBUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toUpdateExercicebudgetaire(id, objet_dao_Exercicebudgetaire):
		try:
			exercicebudgetaire = Model_Exercicebudgetaire.objects.get(pk = id)
			exercicebudgetaire.designation =objet_dao_Exercicebudgetaire.designation
			exercicebudgetaire.montant =objet_dao_Exercicebudgetaire.montant
			exercicebudgetaire.annee =objet_dao_Exercicebudgetaire.annee
			exercicebudgetaire.date_debut = objet_dao_Exercicebudgetaire.date_debut
			exercicebudgetaire.date_fin = objet_dao_Exercicebudgetaire.date_fin
			exercicebudgetaire.updated_at = timezone.now()
			exercicebudgetaire.save()
			return exercicebudgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA EXERCICEBUDGETAIRE')
			#print(e)
			return None
	@staticmethod
	def toGetExercicebudgetaire(id):
		try:
			return Model_Exercicebudgetaire.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteExercicebudgetaire(id):
		try:
			exercicebudgetaire = Model_Exercicebudgetaire.objects.get(pk = id)
			exercicebudgetaire.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetActiveExercicebudgetaire():
		try:
			'''year = timezone.now().year
			exercicebudgetaire = Model_Exercicebudgetaire.objects.filter(annee = int(year)).first()
			#print("hhghg",exercicebudgetaire)

			return exercicebudgetaire'''
			return Model_Exercicebudgetaire.objects.filter(is_active = True).first()
		except Exception as e:
			#print(e)
			return None

	@staticmethod
	def toSetActiveExerciceBudgetaire(id):
		try:
			Model_Exercicebudgetaire.objects.all().update(is_active = False)

			exercicebudgetaire = dao_exercicebudgetaire.toGetExercicebudgetaire(id)
			exercicebudgetaire.is_active = True
			exercicebudgetaire.save()
			return True
		except Exception as e:
			#print("ERREUR DU UPDATE")
			#print(e)
			return False

	@staticmethod
	def toClotureExerciceBudgetaire(id):
		try:
			exercicebudgetaire = Model_Exercicebudgetaire.objects.get(pk = id)
			exercicebudgetaire.is_active = False
			exercicebudgetaire.is_cloture = True
			exercicebudgetaire.save()
			return True
		except Exception as e:
			#print("ERREUR DU UPDATE")
			#print(e)
			return False


