from __future__ import unicode_literals
from ErpBackOffice.models import Model_Pret, Model_PaiementInterne
from django.utils import timezone


class dao_pret(object):
	id = 0
	montant=0.0
	devise_id=None
	periodicite=4
	date_pret=None
	delai='2010-01-01'
	tranche_mensuelle=0.0
	creation_date = None
	employe_id = 0
	auteur_id = 0

	@staticmethod
	def toListPret():
		return Model_Pret.objects.all().order_by('-id')

	@staticmethod
	def toCreatePret(montant, devise_id, tranche_mensuelle, employe_id = None, delai = None, date_pret = None, auteur_id = None, periodicite = 4):
		try:
			pret = dao_pret()
			pret.montant = montant
			pret.devise_id = devise_id
			pret.date_pret = date_pret
			pret.delai = delai
			pret.tranche_mensuelle = tranche_mensuelle
			pret.employe_id = employe_id
			pret.periodicite = periodicite
			return pret
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PRET')
			#print(e)
			return None

	@staticmethod
	def toSavePret(auteur,objet_dao_Pret):
		try:
			pret  					= Model_Pret()
			pret.reference          = dao_pret.toGenerateNumero()
			pret.montant 			= objet_dao_Pret.montant
			pret.devise_id			= objet_dao_Pret.devise_id
			pret.periodicite 		= objet_dao_Pret.periodicite
			pret.date_pret 			= objet_dao_Pret.date_pret
			pret.delai 				= objet_dao_Pret.delai
			pret.tranche_mensuelle 	= objet_dao_Pret.tranche_mensuelle
			pret.employe_id 		= objet_dao_Pret.employe_id
			pret.auteur_id 			= auteur.id
			pret.save()
			return pret
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PRET')
			#print(e)
			return None

	@staticmethod
	def toUpdatePret(id, objet_dao_Pret):
		try:
			pret 					= Model_Pret.objects.get(pk = id)
			pret.montant 			= objet_dao_Pret.montant
			pret.devise_id			= objet_dao_Pret.devise_id
			pret.periodicite 		= objet_dao_Pret.periodicite
			pret.date_pret 			= objet_dao_Pret.date_pret
			pret.delai 				= objet_dao_Pret.delai
			pret.tranche_mensuelle 	= objet_dao_Pret.tranche_mensuelle
			pret.employe_id 		= objet_dao_Pret.employe_id
			pret.save()
			return pret
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PRET')
			#print(e)
			return None
	@staticmethod
	def toGetPret(id):
		try:
			return Model_Pret.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListPretActif():
		return Model_Pret.objects.filter(est_actif = True)

	@staticmethod
	def toDeletePret(id):
		try:
			pret = Model_Pret.objects.get(pk = id)
			pret.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toListPretNoPaidOfDossier(dossier_id):
		pretsList = []
		try:
			prets = Model_Pret.objects.filter(est_actif = True)
			for pret in prets:
				paiements = Model_PaiementInterne.objects.filter(pret_id = pret.id, dossier_paie_id = dossier_id).count()
				#print("Nbre paiement: {}".format(paiements))
				if(paiements == 0): pretsList.append(pret)
			return pretsList
		except Exception as e:
			#print("ERREUR FONCTION (toListPretNoPaidOfDossier)")
			#print(e)
			return pretsList

	@staticmethod
	def toGetResttoPayToDate(pret_id):
		montant = 0
		try:
			pret = Model_Pret.objects.get(pk = pret_id)
			paiements = Model_PaiementInterne.objects.filter(pret_id = pret.id, creation_date__year = '2019', creation_date__month = '07')
			for paiement in paiements:
				if(paiement.devise == pret.devise): montant = montant + paiement.montant
				else:
					taux = Model_Taux.objects.get(pk = paiement.taux_id)
					montant = montant + (paiement.montant / taux.montant)
			return montant
		except Exception as e:
			#print("ERREUR FONCTION (toGetResttoPayToDate)")
			#print(e)
			return montant

	@staticmethod
	def toGenerateNumero():
		total = dao_pret.toListPret().count()
		total = total + 1
		temp_numero = str(total)

		for i in range(len(str(total)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "PRET-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero

	@staticmethod
	def toGetOrderMax():
		try:
			max = Model_Pret.objects.all().count()
			max = max + 1
			return max
		except Exception as e:
			#print("ERREUR")
			#print(e)
			return None