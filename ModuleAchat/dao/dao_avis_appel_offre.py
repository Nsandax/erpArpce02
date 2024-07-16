from __future__ import unicode_literals
from ErpBackOffice.models import Model_Avis_appel_offre
from django.utils import timezone

class dao_avis_appel_offre(object):
	id = 0
	numero_reference = ''
	numero_dossier = ''
	designation_commission = ''
	nombre_lots = 0
	intitule = ''
	financement = ''
	type_appel_offre = ''
	lieu_consultation = ''
	qualification = ''
	type_marche_id = None
	conditions = ''
	date_signature = '2010-01-01'
	lieu_depot = ''
	date_depot = '2010-01-01'
	delai_engagement = ''
	montant_commission = ''
	desc = ''
	demande_achat_id = None

	@staticmethod
	def toListAvis_appel_offre():
		return Model_Avis_appel_offre.objects.all().order_by('-id')

	@staticmethod
	def toListAvis_appel_offreByAuteur(user_id):
		return Model_Avis_appel_offre.objects.filter(auteur_id=user_id)

	@staticmethod
	def toCreateAvis_appel_offre(numero_reference,numero_dossier,designation_commission,intitule,financement,type_appel_offre,lieu_consultation,qualification,conditions,date_signature,lieu_depot,date_depot,delai_engagement,montant_commission,desc, demande_achat_id = None, type_marche_id = None, nombre_lots = 0):
		try:
			avis_appel_offre = dao_avis_appel_offre()
			avis_appel_offre.numero_reference = numero_reference
			avis_appel_offre.numero_dossier = numero_dossier
			avis_appel_offre.designation_commission = designation_commission
			avis_appel_offre.intitule = intitule
			avis_appel_offre.financement = financement
			avis_appel_offre.type_appel_offre = type_appel_offre
			avis_appel_offre.lieu_consultation = lieu_consultation
			avis_appel_offre.qualification = qualification
			avis_appel_offre.conditions = conditions
			avis_appel_offre.date_signature = date_signature
			avis_appel_offre.lieu_depot = lieu_depot
			avis_appel_offre.date_depot = date_depot
			avis_appel_offre.delai_engagement = delai_engagement
			avis_appel_offre.type_marche_id = type_marche_id
			avis_appel_offre.montant_commission = montant_commission
			avis_appel_offre.desc = desc
			avis_appel_offre.demande_achat_id = demande_achat_id
			avis_appel_offre.nombre_lots = nombre_lots
			return avis_appel_offre
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA AVIS_APPEL_OFFRE')
			#print(e)
			return None

	@staticmethod
	def toSaveAvis_appel_offre(auteur, objet_dao_Avis_appel_offre):
		try:
			avis_appel_offre  = Model_Avis_appel_offre()
			avis_appel_offre.numero_reference = objet_dao_Avis_appel_offre.numero_reference
			avis_appel_offre.numero_dossier = objet_dao_Avis_appel_offre.numero_dossier
			avis_appel_offre.designation_commission = objet_dao_Avis_appel_offre.designation_commission
			avis_appel_offre.intitule = objet_dao_Avis_appel_offre.intitule
			avis_appel_offre.financement = objet_dao_Avis_appel_offre.financement
			avis_appel_offre.type_appel_offre = objet_dao_Avis_appel_offre.type_appel_offre
			avis_appel_offre.lieu_consultation = objet_dao_Avis_appel_offre.lieu_consultation
			avis_appel_offre.qualification = objet_dao_Avis_appel_offre.qualification
			avis_appel_offre.conditions = objet_dao_Avis_appel_offre.conditions
			avis_appel_offre.date_signature = objet_dao_Avis_appel_offre.date_signature
			avis_appel_offre.lieu_depot = objet_dao_Avis_appel_offre.lieu_depot
			avis_appel_offre.date_depot = objet_dao_Avis_appel_offre.date_depot
			avis_appel_offre.delai_engagement = objet_dao_Avis_appel_offre.delai_engagement
			avis_appel_offre.montant_commission = objet_dao_Avis_appel_offre.montant_commission
			avis_appel_offre.desc = objet_dao_Avis_appel_offre.desc
			avis_appel_offre.type_marche_id = objet_dao_Avis_appel_offre.type_marche_id
			avis_appel_offre.demande_achat_id = objet_dao_Avis_appel_offre.demande_achat_id
			avis_appel_offre.nombre_lots = objet_dao_Avis_appel_offre.nombre_lots
			avis_appel_offre.created_at = timezone.now()
			avis_appel_offre.updated_at = timezone.now()
			avis_appel_offre.auteur_id = auteur.id

			avis_appel_offre.save()
			return avis_appel_offre
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA AVIS_APPEL_OFFRE')
			#print(e)
			return None

	@staticmethod
	def toUpdateAvis_appel_offre(id, objet_dao_Avis_appel_offre):
		try:
			avis_appel_offre = Model_Avis_appel_offre.objects.get(pk = id)
			avis_appel_offre.numero_reference =objet_dao_Avis_appel_offre.numero_reference
			avis_appel_offre.numero_dossier =objet_dao_Avis_appel_offre.numero_dossier
			avis_appel_offre.designation_commission =objet_dao_Avis_appel_offre.designation_commission
			avis_appel_offre.intitule =objet_dao_Avis_appel_offre.intitule
			avis_appel_offre.financement =objet_dao_Avis_appel_offre.financement
			avis_appel_offre.type_appel_offre =objet_dao_Avis_appel_offre.type_appel_offre
			avis_appel_offre.lieu_consultation =objet_dao_Avis_appel_offre.lieu_consultation
			avis_appel_offre.qualification =objet_dao_Avis_appel_offre.qualification
			avis_appel_offre.conditions =objet_dao_Avis_appel_offre.conditions
			avis_appel_offre.date_signature =objet_dao_Avis_appel_offre.date_signature
			avis_appel_offre.lieu_depot =objet_dao_Avis_appel_offre.lieu_depot
			avis_appel_offre.date_depot =objet_dao_Avis_appel_offre.date_depot
			avis_appel_offre.delai_engagement =objet_dao_Avis_appel_offre.delai_engagement
			avis_appel_offre.montant_commission =objet_dao_Avis_appel_offre.montant_commission
			avis_appel_offre.desc =objet_dao_Avis_appel_offre.desc
			avis_appel_offre.demande_achat_id = objet_dao_Avis_appel_offre.demande_achat_id
			avis_appel_offre.nombre_lots = objet_dao_Avis_appel_offre.nombre_lots
			avis_appel_offre.updated_at = timezone.now()
			avis_appel_offre.save()
			return avis_appel_offre
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA AVIS_APPEL_OFFRE')
			#print(e)
			return None
	@staticmethod
	def toGetAvis_appel_offre(id):
		try:
			return Model_Avis_appel_offre.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteAvis_appel_offre(id):
		try:
			avis_appel_offre = Model_Avis_appel_offre.objects.get(pk = id)
			avis_appel_offre.delete()
			return True
		except Exception as e:
			return False