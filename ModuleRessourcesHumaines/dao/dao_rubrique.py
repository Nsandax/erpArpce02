from __future__ import unicode_literals
from ErpBackOffice.models import Model_Rubrique
from django.utils import timezone

class dao_rubrique(object):
	

	@staticmethod
	def toListRubriques():
		return Model_Rubrique.objects.all().order_by('-id')

	@staticmethod
	def toGetRubrique(id):
		try:
			return Model_Rubrique.objects.get(pk = id)
		except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_regle_salariale)")
            #print(e)
			return None
	

	@staticmethod
	def toGetRubriqueRemboursementPret():
		try:
			return Model_Rubrique.objects.filter(code = "620").first()
		except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE (dao_regle_salariale)")
            #print(e)
			return None
	
	