from __future__ import unicode_literals
from ErpBackOffice.models import Model_Typetransactionbudgetaire
from django.utils import timezone

class dao_typetransactionbudgetaire(object):
	id = 0
	designation = ''

	@staticmethod
	def toListTypetransactionbudgetaire():
		return Model_Typetransactionbudgetaire.objects.all().order_by('-id')

	@staticmethod
	def toCreateTypetransactionbudgetaire(designation):
		try:
			typetransactionbudgetaire = dao_typetransactionbudgetaire()
			typetransactionbudgetaire.designation = designation
			return typetransactionbudgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPETRANSACTIONBUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toSaveTypetransactionbudgetaire(auteur, objet_dao_Typetransactionbudgetaire):
		try:
			typetransactionbudgetaire  = Model_Typetransactionbudgetaire()
			typetransactionbudgetaire.designation = objet_dao_Typetransactionbudgetaire.designation
			typetransactionbudgetaire.created_at = timezone.now()
			typetransactionbudgetaire.updated_at = timezone.now()
			typetransactionbudgetaire.auteur_id = auteur.id

			typetransactionbudgetaire.save()
			return typetransactionbudgetaire
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPETRANSACTIONBUDGETAIRE')
			#print(e)
			return None

	@staticmethod
	def toUpdateTypetransactionbudgetaire(id, objet_dao_Typetransactionbudgetaire):
		try:
			typetransactionbudgetaire = Model_Typetransactionbudgetaire.objects.get(pk = id)
			typetransactionbudgetaire.designation =objet_dao_Typetransactionbudgetaire.designation
			typetransactionbudgetaire.updated_at = timezone.now()
			typetransactionbudgetaire.save()
			return typetransactionbudgetaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPETRANSACTIONBUDGETAIRE')
			#print(e)
			return None
	@staticmethod
	def toGetTypetransactionbudgetaire(id):
		try:
			return Model_Typetransactionbudgetaire.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetTypeRetrait():
		try:
			return Model_Typetransactionbudgetaire.objects.get(designation = "Retrait")
		except Exception as e:
			return None

	@staticmethod
	def toGetTypeNormal():
		try:
			return Model_Typetransactionbudgetaire.objects.get(designation = "Normal")
		except Exception as e:
			return None

	@staticmethod
	def toGetTypeRallonge():
		try:
			return Model_Typetransactionbudgetaire.objects.get(designation = "Rallonge")
		except Exception as e:
			return None

	@staticmethod
	def toDeleteTypetransactionbudgetaire(id):
		try:
			typetransactionbudgetaire = Model_Typetransactionbudgetaire.objects.get(pk = id)
			typetransactionbudgetaire.delete()
			return True
		except Exception as e:
			return False