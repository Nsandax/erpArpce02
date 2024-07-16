
from __future__ import unicode_literals
from ErpBackOffice.models import Model_DossierPaie
from django.utils import timezone
from ModulePayroll.dao.dao_bulletin_modele import dao_bulletin_modele
from ModulePayroll.dao.dao_constante import dao_constante
from ModulePayroll.dao.dao_item_bulletin import dao_item_bulletin
from ModulePayroll.dao.dao_bulletin import dao_bulletin
from ModuleRessourcesHumaines.dao.dao_employe import dao_employe
from ErpBackOffice.utils.separateur import makeFloat, makeStringFromFloatExcel, makeInt, makeIntId
from ErpBackOffice.utils.function_constante import function_constante

class dao_dossier_paie(object):
	id = 0
	mois = 0
	annee = ''
	est_actif = False
	est_cloture = False

	@staticmethod
	def toListDossierPaie():
		return Model_DossierPaie.objects.all().order_by("-created_at")

	@staticmethod
	def toCreateDossierPaie(mois,annee,est_actif,est_cloture):
		try:
			dossier_paie = dao_dossier_paie()
			dossier_paie.mois = mois
			dossier_paie.annee = annee
			dossier_paie.est_actif = est_actif
			dossier_paie.est_cloture = est_cloture
			return dossier_paie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PERIODEPAIE')
			#print(e)
			return None

	@staticmethod
	def toSaveDossierPaie(auteur, objet_dao_dossierpaie):
		try:
			dossier_paie  = Model_DossierPaie()
			dossier_paie.mois = objet_dao_dossierpaie.mois
			dossier_paie.annee = objet_dao_dossierpaie.annee
			dossier_paie.est_actif = objet_dao_dossierpaie.est_actif
			dossier_paie.est_cloture = objet_dao_dossierpaie.est_cloture
			dossier_paie.created_at = timezone.now()
			dossier_paie.updated_at = timezone.now()
			dossier_paie.auteur_id = auteur.id

			dossier_paie.save()
			return dossier_paie
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PERIODEPAIE')
			#print(e)
			return None

	@staticmethod
	def toUpdateDossierPaie(id, objet_dao_dossierpaie):
		try:
			dossier_paie = Model_DossierPaie.objects.get(pk = id)
			dossier_paie.mois =objet_dao_dossierpaie.mois
			dossier_paie.annee =objet_dao_dossierpaie.annee
			dossier_paie.est_actif =objet_dao_dossierpaie.est_actif
			dossier_paie.est_cloture = objet_dao_dossierpaie.est_cloture
			dossier_paie.updated_at = timezone.now()
			dossier_paie.save()
			return dossier_paie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PERIODEPAIE')
			#print(e)
			return None
	@staticmethod
	def toGetDossierPaie(id):
		try:
			return Model_DossierPaie.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toGetDossierPaieByDesignation(mois, annee):
		try:
			return Model_DossierPaie.objects.filter(mois = mois, annee = annee)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteDossierPaie(id):
		try:
			dossier_paie = Model_DossierPaie.objects.get(pk = id)
			dossier_paie.delete()
			return True
		except Exception as e:
			return False
	
	@staticmethod
	def toGetActiveDossierPaie():
		try:
			return Model_DossierPaie.objects.filter(est_actif = True).first()
		except Exception as e:
			#print(e)
			return None
			

	@staticmethod
	def toSetActiveDossierPaie(id):
		try:
			Model_DossierPaie.objects.all().update(est_actif = False)

			dossier_paie = dao_dossier_paie.toGetDossierPaie(id)
			dossier_paie.est_actif = True
			dossier_paie.save()
			return True
		except Exception as e:
			#print("ERREUR DU UPDATE")
			#print(e)
			return False

	@staticmethod
	def toClotureDossierPaie(id):
		try:
			dossier_paie = Model_DossierPaie.objects.get(pk = id)
			dossier_paie.est_actif = False
			dossier_paie.est_cloture = True
			dossier_paie.save()
			return True
		except Exception as e:
			#print("ERREUR DU UPDATE")
			#print(e)
			return False
	
	@staticmethod
	def toSetCalculateDossierPaie(id):
		try:
			dossier_paie = Model_DossierPaie.objects.get(pk = id)
			dossier_paie.est_calcul = True
			dossier_paie.save()
			return True
		except Exception as e:
			#print("ERREUR DU UPDATE")
			#print(e)
			return False
	