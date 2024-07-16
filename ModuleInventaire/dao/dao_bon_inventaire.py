from __future__ import unicode_literals
from ErpBackOffice.models import Model_Bon_inventaire
from django.utils import timezone

class dao_bon_inventaire(object):
	id = 0
	numero_inventaire=''
	montant_global=0.0
	date_inventaire='2010-01-01'
	quantite=0
	description=''
	employe_id = 0
	emplacement_id = 0
	auteur_id = 0
	est_realisee = False


	@staticmethod
	def toListBonInventaire():
		return Model_Bon_inventaire.objects.all().order_by('-id')

	@staticmethod
	def toListBonInventaireByAuteur(user_id):
		return Model_Bon_inventaire.objects.filter(auteur_id = user_id)

	@staticmethod
	def toCreateBonInventaire(numero_inventaire, date_inventaire,employe_id=None,emplacement_id=None, status = "", description = "", montant_global = 0, est_realisee = True, quantite =0):
		try:
			bon_inventaire = dao_bon_inventaire()
			bon_inventaire.numero_inventaire = numero_inventaire
			bon_inventaire.montant_global = montant_global
			bon_inventaire.date_inventaire = date_inventaire
			bon_inventaire.est_realisee = est_realisee
			bon_inventaire.quantite = quantite
			bon_inventaire.description = description
			bon_inventaire.status = status
			if employe_id != 0:
				bon_inventaire.employe_id = employe_id
			if emplacement_id != 0:
				bon_inventaire.emplacement_id = emplacement_id
			return bon_inventaire
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BON_inventaire')
			#print(e)
			return None

	@staticmethod
	def toSaveBonInventaire(auteur, objet_dao_Bon_inventaire):
		try:
			bon_inventaire  = Model_Bon_inventaire()
			bon_inventaire.numero_inventaire =objet_dao_Bon_inventaire.numero_inventaire
			bon_inventaire.montant_global =objet_dao_Bon_inventaire.montant_global
			bon_inventaire.date_inventaire =objet_dao_Bon_inventaire.date_inventaire
			bon_inventaire.est_realisee =objet_dao_Bon_inventaire.est_realisee
			bon_inventaire.quantite =objet_dao_Bon_inventaire.quantite
			bon_inventaire.description =objet_dao_Bon_inventaire.description
			bon_inventaire.status =objet_dao_Bon_inventaire.status
			bon_inventaire.creation_date = timezone.now()
			bon_inventaire.employe_id = objet_dao_Bon_inventaire.employe_id
			bon_inventaire.emplacement_id = objet_dao_Bon_inventaire.emplacement_id
			bon_inventaire.auteur_id = auteur.id
			bon_inventaire.save()
			return bon_inventaire
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_inventaire')
			#print(e)
			return None

	@staticmethod
	def toUpdateBonInventaire(id, objet_dao_Bon_inventaire):
		try:
			bon_inventaire = Model_Bon_inventaire.objects.get(pk = id)
			bon_inventaire.numero_inventaire =objet_dao_Bon_inventaire.numero_inventaire
			bon_inventaire.montant_global =objet_dao_Bon_inventaire.montant_global
			bon_inventaire.date_inventaire =objet_dao_Bon_inventaire.date_inventaire
			bon_inventaire.est_realisee =objet_dao_Bon_inventaire.est_realisee
			bon_inventaire.quantite =objet_dao_Bon_inventaire.quantite
			bon_inventaire.description =objet_dao_Bon_inventaire.description
			bon_inventaire.status =objet_dao_Bon_inventaire.status
			bon_inventaire.employe_id = objet_dao_Bon_inventaire.employe_id
			bon_inventaire.emplacement_id = objet_dao_Bon_inventaire.emplacement_id
			bon_inventaire.save()
			return bon_inventaire
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BON_inventaire')
			#print(e)
			return None
	@staticmethod
	def toGetBonInventaire(id):
		try:
			return Model_Bon_inventaire.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteBonInventaire(id):
		try:
			bon_inventaire = Model_Bon_inventaire.objects.get(pk = id)
			bon_inventaire.delete()
			return True
		except Exception as e:
			return False