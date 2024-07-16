from __future__ import unicode_literals
from ErpBackOffice.models import Model_Grade
from django.utils import timezone


class dao_grade(object):
	id = 0
	denomination=''
	salaire=0.0
	unite_fonctionnelle_id = 0
	creation_date = None
	auteur_id = 0

	@staticmethod
	def toListGrade():
		return Model_Grade.objects.all().order_by('-id')

	@staticmethod
	def toCreateGrade(denomination,salaire, unite_fonctionnelle_id):
		try:
			grade = dao_grade()
			grade.denomination = denomination
			grade.salaire = salaire
			if unite_fonctionnelle_id != 0:
				grade.unite_fonctionnelle_id = unite_fonctionnelle_id
			return grade
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA GRADE')
			#print(e)
			return None

	@staticmethod
	def toSaveGrade(auteur,objet_dao_Grade):
		try:
			grade  = Model_Grade()
			grade.denomination =objet_dao_Grade.denomination
			grade.salaire =objet_dao_Grade.salaire
			grade.unite_fonctionnelle_id = objet_dao_Grade.unite_fonctionnelle_id
			grade.auteur_id = auteur.id
			grade.creation_date = timezone.now()
			grade.save()
			return grade
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA GRADE')
			#print(e)
			return None

	@staticmethod
	def toUpdateGrade(id, objet_dao_Grade):
		try:
			grade = Model_Grade.objects.get(pk = id)
			grade.denomination =objet_dao_Grade.denomination
			grade.salaire =objet_dao_Grade.salaire
			grade.unite_fonctionnelle_id = objet_dao_Grade.unite_fonctionnelle_id
			grade.save()
			return grade
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA GRADE')
			#print(e)
			return None
	@staticmethod
	def toGetGrade(id):
		try:
			return Model_Grade.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteGrade(id):
		try:
			grade = Model_Grade.objects.get(pk = id)
			grade.delete()
			return True
		except Exception as e:
			return False