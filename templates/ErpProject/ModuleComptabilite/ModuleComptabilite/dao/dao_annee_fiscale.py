from __future__ import unicode_literals
from ErpBackOffice.models import Model_Annee_fiscale
from django.utils import timezone

class dao_annee_fiscale(object):
	id = 0
	designation = ''
	observation = ''
	date_debut = '2010-01-01'
	date_fin = '2010-01-01'
	est_active = False

	@staticmethod
	def toListAnnee_fiscale():
		return Model_Annee_fiscale.objects.all().order_by('-id')

	@staticmethod
	def toCreateAnnee_fiscale(designation,observation,date_debut,date_fin,est_active):
		try:
			annee_fiscale = dao_annee_fiscale()
			annee_fiscale.designation = designation
			annee_fiscale.observation = observation
			annee_fiscale.date_debut = date_debut
			annee_fiscale.date_fin = date_fin
			annee_fiscale.est_active = est_active
			return annee_fiscale
		except Exception as e:
			# print('ERREUR LORS DE LA CREATION DE LA ANNEE_FISCALE')
			# print(e)
			return None

	@staticmethod
	def toSaveAnnee_fiscale(auteur, objet_dao_Annee_fiscale):
		try:
			annee_fiscale  = Model_Annee_fiscale()
			annee_fiscale.designation = objet_dao_Annee_fiscale.designation
			annee_fiscale.observation = objet_dao_Annee_fiscale.observation
			annee_fiscale.date_debut = objet_dao_Annee_fiscale.date_debut
			annee_fiscale.date_fin = objet_dao_Annee_fiscale.date_fin
			annee_fiscale.est_active = objet_dao_Annee_fiscale.est_active
			annee_fiscale.created_at = timezone.now()
			annee_fiscale.updated_at = timezone.now()
			annee_fiscale.auteur_id = auteur.id

			annee_fiscale.save()
			return annee_fiscale
		except Exception as e:
			# print('ERREUR LORS DE L ENREGISTREMENT DE LA ANNEE_FISCALE')
			# print(e)
			return None

	@staticmethod
	def toUpdateAnnee_fiscale(id, objet_dao_Annee_fiscale):
		try:
			annee_fiscale = Model_Annee_fiscale.objects.get(pk = id)
			annee_fiscale.designation =objet_dao_Annee_fiscale.designation
			annee_fiscale.observation =objet_dao_Annee_fiscale.observation
			annee_fiscale.date_debut =objet_dao_Annee_fiscale.date_debut
			annee_fiscale.date_fin =objet_dao_Annee_fiscale.date_fin
			annee_fiscale.est_active =objet_dao_Annee_fiscale.est_active
			annee_fiscale.updated_at = timezone.now()
			annee_fiscale.save()
			return annee_fiscale
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ANNEE_FISCALE')
			#print(e)
			return None
	@staticmethod
	def toGetAnnee_fiscale(id):
		try:
			return Model_Annee_fiscale.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetAnneeFiscaleActive():
		try:
			return Model_Annee_fiscale.objects.filter(est_active = True).first()
		except Exception as e:
			return None




	@staticmethod
	def toSetAnneeFiscaleActive(id):
		try:
			Model_Annee_fiscale.objects.all().update(est_active = False)
			annee_fiscale = Model_Annee_fiscale.objects.get(pk=id)
			annee_fiscale.est_active = True
			annee_fiscale.save()
		except Exception as e:
			return None

	@staticmethod
	def toDeleteAnnee_fiscale(id):
		try:
			annee_fiscale = Model_Annee_fiscale.objects.get(pk = id)
			annee_fiscale.delete()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toGetSeuilImmobilisationOfAnneeFiscaleActive():
		try:
			seuil_immobilisation = 0
			annee = Model_Annee_fiscale.objects.filter(est_active = True).first()
			if annee:
				seuil_immobilisation = annee.seuil_immobilisation

			return seuil_immobilisation
		except Exception as e:
			#print(e)
			return 0

	@staticmethod
	def toUpdateSeuilImmobilisationOfAnneeFiscaleActive(seuil_immobilisation):
		try:
			annee_fiscale = Model_Annee_fiscale.objects.filter(est_active = True).first()
			annee_fiscale.seuil_immobilisation = seuil_immobilisation
			annee_fiscale.save()

			return annee_fiscale
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ANNEE_FISCALE')
			#print(e)
			return None