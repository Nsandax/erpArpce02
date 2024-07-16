from __future__ import unicode_literals
from ErpBackOffice.models import Model_Emplacement, Model_TypeEmplacement
from django.utils import timezone

class dao_emplacement(object):
	id = 0
	designation=''
	couloir=0
	rayon=0
	creation_date='2010-01-01'
	is_racine = False
	emplacement_id = 0
	type_emplacement_id = 0
	auteur_id = 0
	est_systeme = False

	@staticmethod
	def toListEmplacement():
		return Model_Emplacement.objects.all().order_by('-id')


	@staticmethod
	def toListEntrepot():
		type_emplacement = Model_TypeEmplacement.objects.filter(designation = "ENTREPOT")
		for type_empl in type_emplacement:
			emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_empl.id)
		return emplacements

	@staticmethod
	def toCreateEmplacement(designation,couloir,rayon,is_racine, est_systeme, type_emplacement_id=None,emplacement_id=None):
		try:
			emplacement = dao_emplacement()
			emplacement.designation = designation
			emplacement.couloir = couloir
			emplacement.rayon = rayon
			emplacement.is_racine = is_racine
			emplacement.est_systeme = est_systeme
			emplacement.emplacement_id = emplacement_id
			emplacement.auteur_id = type_emplacement_id
			return emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE L\'EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toSaveEmplacement(auteur,objet_dao_Emplacement):
		try:
			emplacement  = Model_Emplacement()
			emplacement.designation =objet_dao_Emplacement.designation
			emplacement.couloir =objet_dao_Emplacement.couloir
			emplacement.rayon =objet_dao_Emplacement.rayon
			emplacement.creation_date =timezone.now()
			emplacement.is_racine =objet_dao_Emplacement.is_racine
			emplacement.est_systeme = objet_dao_Emplacement.est_systeme
			emplacement.type_emplacement_id = objet_dao_Emplacement.type_emplacement_id
			emplacement.emplacement_id = objet_dao_Emplacement.emplacement_id
			emplacement.auteur_id = auteur.id
			emplacement.save()
			return emplacement
		except Exception as e:
			#print('ERREUR LORS DE L\'ENREGISTREMENT DE L\'EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toUpdateEmplacement(id, objet_dao_Emplacement):
		try:
			emplacement = Model_Emplacement.objects.get(pk = id)
			emplacement.designation =objet_dao_Emplacement.designation
			emplacement.couloir =objet_dao_Emplacement.couloir
			emplacement.rayon =objet_dao_Emplacement.rayon
			emplacement.is_racine =objet_dao_Emplacement.is_racine
			emplacement.est_systeme = objet_dao_Emplacement.est_systeme
			emplacement.type_emplacement_id = objet_dao_Emplacement.type_emplacement_id
			emplacement.emplacement_id = objet_dao_Emplacement.emplacement_id
			emplacement.save()
			return emplacement
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE L\'EMPLACEMENT')
			#print(e)
			return None

	@staticmethod
	def toGetEmplacement(id):
		try:
			return Model_Emplacement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListEmplacementOfId(id):
		try:
			return Model_Emplacement.objects.filter(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListEmplacementsInEntrepot(entrepot_id):
		try:
			return Model_Emplacement.objects.filter(parent_id = entrepot_id).order_by("designation")
		except Exception as e:
			#print("ERREUR")
			#print(e)
			return []

	@staticmethod
	def toListEmplacementsOfType(type_emplacement_id):
		return Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement_id).order_by("designation")


	@staticmethod
	def toDeleteEmplacement(id):
		try:
			emplacement = Model_Emplacement.objects.get(pk = id)
			emplacement.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetEmplacement(id):
		try:
			return Model_Emplacement.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementEntree(type_emplacement_entree):
		try:
			return Model_Emplacement.objects.filter(est_systeme = True).get(type_emplacement_id = type_emplacement_entree.id)
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementStock(type_emplacement_stock):
		try:
			return Model_Emplacement.objects.filter(est_systeme = True).filter(type_emplacement_id = type_emplacement_stock.id)
		except Exception as e:
			return []

	@staticmethod
	def toGetEmplacementReserve(type_emplacement_reserve):
		try:
			return Model_Emplacement.objects.filter(est_systeme = True).get(type_emplacement_id = type_emplacement_reserve.id)
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementStockageSBA():
		try:
			return Model_Emplacement.objects.filter(designation = "Stockage SBA").first()
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementEntrepot(type_emplacement_id):
		try:
			return Model_Emplacement.objects.filter(est_systeme = True).filter(type_emplacement_id = type_emplacement_id).first()
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementInternalBusiness():
		try:
			return Model_Emplacement.objects.filter(designation = 'internal_busness_good').first()
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementMoyensGeneraux():
		try:
			return Model_Emplacement.objects.filter(designation = 'Stockage Moyens généraux').first()
		except Exception as e:
			return None

	@staticmethod
	def toGetEmplacementBySBA():
		try:
			return Model_Emplacement.objects.filter(designation = 'Stockage SBA').first()
		except Exception as e:
			return None


	@staticmethod
	def toListAllEmplacementNotRebut():
		try:
			return Model_Emplacement.objects.exclude(designation='REBUT')
		except Exception as e:
			return None


	@staticmethod
	def toGetEmplacementByREBUT():
		try:
			return Model_Emplacement.objects.filter(designation='REBUT').first()
		except Exception as e:
			return None