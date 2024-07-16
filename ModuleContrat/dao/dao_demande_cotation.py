from __future__ import unicode_literals
from ErpBackOffice.models import Model_Demande_cotation
from django.utils import timezone

class dao_demande_cotation(object):
	id = 0
	numero_reference = ''
	intitule = ""
	financement = ""
	nombre_lots = 0
	demande_achat_id = None
	montant = 0.0
	devise_id = None
	fournisseur_id = None
	type_marche_id = None
	description = ''

	@staticmethod
	def toListDemande_cotation():
		return Model_Demande_cotation.objects.all().order_by('-id')
	
	@staticmethod
	def toListDemandeCotationByTypeMarche(type_marche_id):
		return Model_Demande_cotation.objects.filter(type_marche_id = type_marche_id).order_by('-id')

	@staticmethod
	def toCreateDemande_cotation(numero_reference,demande_achat_id,montant,devise_id,fournisseur_id,type_marche_id,description, intitule="", financement="", nombre_lots = 0):
		try:
			demande_cotation = dao_demande_cotation()
			demande_cotation.numero_reference = numero_reference
			demande_cotation.intitule = intitule
			demande_cotation.financement = financement
			demande_cotation.nombre_lots = nombre_lots
			demande_cotation.demande_achat_id = demande_achat_id
			demande_cotation.montant = montant
			demande_cotation.devise_id = devise_id
			demande_cotation.fournisseur_id = fournisseur_id
			demande_cotation.type_marche_id = type_marche_id
			demande_cotation.description = description
			return demande_cotation
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA DEMANDE_COTATION')
			print(e)
			return None

	@staticmethod
	def toSaveDemande_cotation(auteur, objet_dao_Demande_cotation):
		try:
			demande_cotation  = Model_Demande_cotation()
			demande_cotation.numero_reference = objet_dao_Demande_cotation.numero_reference
			demande_cotation.demande_achat_id = objet_dao_Demande_cotation.demande_achat_id
			demande_cotation.intitule = objet_dao_Demande_cotation.intitule
			demande_cotation.financement = objet_dao_Demande_cotation.financement
			demande_cotation.nombre_lots = objet_dao_Demande_cotation.nombre_lots
			demande_cotation.montant = objet_dao_Demande_cotation.montant
			demande_cotation.devise_id = objet_dao_Demande_cotation.devise_id
			demande_cotation.fournisseur_id = objet_dao_Demande_cotation.fournisseur_id
			demande_cotation.type_marche_id = objet_dao_Demande_cotation.type_marche_id
			demande_cotation.description = objet_dao_Demande_cotation.description
			demande_cotation.created_at = timezone.now()
			demande_cotation.updated_at = timezone.now()
			demande_cotation.auteur_id = auteur.id

			demande_cotation.save()
			return demande_cotation
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA DEMANDE_COTATION')
			print(e)
			return None

	@staticmethod
	def toUpdateDemande_cotation(id, objet_dao_Demande_cotation):
		try:
			demande_cotation = Model_Demande_cotation.objects.get(pk = id)
			demande_cotation.numero_reference =objet_dao_Demande_cotation.numero_reference
			demande_cotation.intitule = objet_dao_Demande_cotation.intitule
			demande_cotation.financement = objet_dao_Demande_cotation.financement
			demande_cotation.nombre_lots = objet_dao_Demande_cotation.nombre_lots
			demande_cotation.demande_achat_id =objet_dao_Demande_cotation.demande_achat_id
			demande_cotation.montant =objet_dao_Demande_cotation.montant
			demande_cotation.devise_id =objet_dao_Demande_cotation.devise_id
			demande_cotation.fournisseur_id =objet_dao_Demande_cotation.fournisseur_id
			demande_cotation.type_marche_id =objet_dao_Demande_cotation.type_marche_id
			demande_cotation.description =objet_dao_Demande_cotation.description
			demande_cotation.updated_at = timezone.now()
			demande_cotation.save()
			return demande_cotation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA DEMANDE_COTATION')
			#print(e)
			return None
	@staticmethod
	def toGetDemande_cotation(id):
		try:
			return Model_Demande_cotation.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteDemande_cotation(id):
		try:
			demande_cotation = Model_Demande_cotation.objects.get(pk = id)
			demande_cotation.delete()
			return True
		except Exception as e:
			return False