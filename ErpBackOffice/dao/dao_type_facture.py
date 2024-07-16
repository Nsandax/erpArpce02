from __future__ import unicode_literals
from ErpBackOffice.models import Model_Typefacture
from django.utils import timezone

class dao_type_facture(object):
	id = 0
	designation = ''
	observation = ''
	type = 2

	@staticmethod
	def toListTypefacture():
		return Model_Typefacture.objects.all()
    
	@staticmethod
	def toListTypefactureClient():
		return Model_Typefacture.objects.filter(type = 2) 

	@staticmethod
	def toCreateTypefacture(designation,observation, type = 2):
		try:
			type_facture = dao_type_facture()
			type_facture.designation = designation
			type_facture.observation = observation
			type_facture.type = 2
			return type_facture
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPEFACTURECLIENT')
			#print(e)
			return None

	@staticmethod
	def toSaveTypefacture(auteur, objet_dao_Typefacture):
		try:
			type_facture  = Model_Typefacture()
			type_facture.designation = objet_dao_Typefacture.designation
			type_facture.observation = objet_dao_Typefacture.observation
			type_facture.type = objet_dao_Typefacture.type
			type_facture.created_at = timezone.now()
			type_facture.updated_at = timezone.now()
			type_facture.auteur_id = auteur.id

			type_facture.save()
			return type_facture
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPEFACTURECLIENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateTypefacture(id, objet_dao_Typefacture):
		try:
			type_facture = Model_Typefacture.objects.get(pk = id)
			type_facture.designation =objet_dao_Typefacture.designation
			type_facture.observation =objet_dao_Typefacture.observation
			type_facture.type = objet_dao_Typefacture.type
			type_facture.updated_at = timezone.now()
			type_facture.save()
			return type_facture
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPEFACTURECLIENT')
			#print(e)
			return None
	@staticmethod
	def toGetTypefacture(id):
		try:
			return Model_Typefacture.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTypefacture(id):
		try:
			type_facture = Model_Typefacture.objects.get(pk = id)
			type_facture.delete()
			return True
		except Exception as e:
			return False