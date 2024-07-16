from __future__ import unicode_literals
from ErpBackOffice.models import Model_MobiliteEmploye
from django.utils import timezone
from ErpBackOffice.models import Model_Employe
from django.template.defaulttags import register
from django import template

register = template.Library()

class dao_mobilite_employe(object):
	id = 0
	reference = ''
	employe_id = None
	type_mobilite = ''
	date_mobilite = ''
	poste_id = None
	categorie_id = None
	classification_pro_id = None
	observation = ''
	
	@staticmethod
	def toListMobiliteEmploye():
		return Model_MobiliteEmploye.objects.all().order_by('-id')

	@staticmethod
	def toCreateMobiliteEmploye(reference,employe_id,type_mobilite,date_mobilite, poste_id,categorie_id,classification_pro_id,observation=""):
		try:
			mobilite = dao_mobilite_employe()
			mobilite.reference = reference
			mobilite.employe_id = employe_id
			mobilite.type_mobilite = type_mobilite
			mobilite.date_mobilite = date_mobilite
			mobilite.poste_id = poste_id
			mobilite.categorie_id = categorie_id
			mobilite.classification_pro_id = classification_pro_id
			mobilite.observation = observation
			return mobilite
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA MOBILITE IN DAO MOBILITE TO CREATEMOB ')
			#print(e)
			return None

	@staticmethod
	def toSaveMobiliteEmploye(auteur, objet_dao_mobilite_employe):
		try:
			mobilite  = Model_MobiliteEmploye()
			mobilite.reference = objet_dao_mobilite_employe.reference
			mobilite.employe_id = objet_dao_mobilite_employe.employe_id
			mobilite.type_mobilite = objet_dao_mobilite_employe.type_mobilite
			mobilite.date_mobilite = objet_dao_mobilite_employe.date_mobilite
			mobilite.categorie_id = objet_dao_mobilite_employe.categorie_id
			mobilite.classification_pro_id = objet_dao_mobilite_employe.classification_pro_id
			mobilite.observation = objet_dao_mobilite_employe.observation
			mobilite.poste_id = objet_dao_mobilite_employe.poste_id
			mobilite.created_at = timezone.now()
			mobilite.updated_at = timezone.now()
			mobilite.auteur_id = auteur.id

			mobilite.save()
			return mobilite
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA MOBILITE IN DAO MOBILTE TO SAVE')
			#print(e)
			return None

	@staticmethod
	def toUpdateMobiliteEmploye(id, objet_dao_mobilite_employe):
		try:
			mobilite = Model_MobiliteEmploye.objects.get(pk = id)
			mobilite.reference =objet_dao_mobilite_employe.reference
			mobilite.employe_id =objet_dao_mobilite_employe.employe_id
			mobilite.type_mobilite=objet_dao_mobilite_employe.type_mobilite
			mobilite.date_mobilite =objet_dao_mobilite_employe.date_mobilite
			mobilite.categorie_id = objet_dao_mobilite_employe.categorie_id
			mobilite.classification_pro_id = objet_dao_mobilite_employe.classification_pro_id
			mobilite.observation =objet_dao_mobilite_employe.observation
			mobilite.poste_id = objet_dao_mobilite_employe.poste_id
			mobilite.updated_at = timezone.now()
			mobilite.save()
			return mobilite
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA MOBILITE')
			#print(e)
			return None
	@staticmethod
	def toGetMobiliteEmploye(id):
		try:
			return Model_MobiliteEmploye.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetMobiliteByEmploye(employe_id):
		try:
			return Model_MobiliteEmploye.objects.filter(employe_id = employe_id)
		except Exception as e:
			return []

	@staticmethod
	def toDeleteMobilite(id):
		try:
			mobilite = Model_MobiliteEmploye.objects.get(pk = id)
			mobilite.delete()
			return True
		except Exception as e:
			return False








