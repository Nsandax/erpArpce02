from __future__ import unicode_literals
from ErpBackOffice.models import Model_Lettre_commande
from django.utils import timezone

class dao_lettre_commande(object):
	id = 0
	numero_reference = ''
	intitule = ""
	financement = ""
	nombre_lots = 0
	demande_achat_id = None
	montant = 0.0
	devise_id = None
	type_marche_id = None
	description = ''

	@staticmethod
	def toListLettre_commande():
		return Model_Lettre_commande.objects.all()
	
	@staticmethod
	def toListLettreCommandeByTypeMarche(type_marche_id):
		return Model_Lettre_commande.objects.filter(type_marche_id = type_marche_id).order_by('-id')

	@staticmethod
	def toCreateLettre_commande(numero_reference,demande_achat_id,montant,devise_id,type_marche_id,description, intitule="", financement="", nombre_lots = 0):
		try:
			lettre_commande = dao_lettre_commande()
			lettre_commande.numero_reference = numero_reference
			lettre_commande.intitule = intitule
			lettre_commande.financement = financement
			lettre_commande.nombre_lots = nombre_lots
			lettre_commande.demande_achat_id = demande_achat_id
			lettre_commande.montant = montant
			lettre_commande.devise_id = devise_id
			lettre_commande.type_marche_id = type_marche_id
			lettre_commande.description = description
			return lettre_commande
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LETTRE_COMMANDE')
			#print(e)
			return None

	@staticmethod
	def toSaveLettre_commande(auteur, objet_dao_Lettre_commande):
		try:
			lettre_commande  = Model_Lettre_commande()
			lettre_commande.numero_reference = objet_dao_Lettre_commande.numero_reference
			lettre_commande.intitule = objet_dao_Lettre_commande.intitule
			lettre_commande.financement = objet_dao_Lettre_commande.financement
			lettre_commande.nombre_lots = objet_dao_Lettre_commande.nombre_lots
			lettre_commande.demande_achat_id = objet_dao_Lettre_commande.demande_achat_id
			lettre_commande.montant = objet_dao_Lettre_commande.montant
			lettre_commande.devise_id = objet_dao_Lettre_commande.devise_id
			lettre_commande.type_marche_id = objet_dao_Lettre_commande.type_marche_id
			lettre_commande.description = objet_dao_Lettre_commande.description
			lettre_commande.created_at = timezone.now()
			lettre_commande.updated_at = timezone.now()
			lettre_commande.auteur_id = auteur.id

			lettre_commande.save()
			return lettre_commande
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA LETTRE_COMMANDE')
			#print(e)
			return None

	@staticmethod
	def toUpdateLettre_commande(id, objet_dao_Lettre_commande):
		try:
			lettre_commande = Model_Lettre_commande.objects.get(pk = id)
			lettre_commande.numero_reference =objet_dao_Lettre_commande.numero_reference
			lettre_commande.intitule = objet_dao_Lettre_commande.intitule
			lettre_commande.financement = objet_dao_Lettre_commande.financement
			lettre_commande.nombre_lots = objet_dao_Lettre_commande.nombre_lots
			lettre_commande.demande_achat_id =objet_dao_Lettre_commande.demande_achat_id
			lettre_commande.montant =objet_dao_Lettre_commande.montant
			lettre_commande.devise_id =objet_dao_Lettre_commande.devise_id
			lettre_commande.type_marche_id =objet_dao_Lettre_commande.type_marche_id
			lettre_commande.description =objet_dao_Lettre_commande.description
			lettre_commande.updated_at = timezone.now()
			lettre_commande.save()
			return lettre_commande
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA LETTRE_COMMANDE')
			#print(e)
			return None
	@staticmethod
	def toGetLettre_commande(id):
		try:
			return Model_Lettre_commande.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteLettre_commande(id):
		try:
			lettre_commande = Model_Lettre_commande.objects.get(pk = id)
			lettre_commande.delete()
			return True
		except Exception as e:
			return False