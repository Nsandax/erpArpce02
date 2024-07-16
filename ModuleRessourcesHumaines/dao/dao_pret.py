from __future__ import unicode_literals
from ErpBackOffice.models import Model_Pret, Model_PaiementInterne
from ModulePayroll.dao.dao_ligne_paiement_pret import dao_ligne_paiement_pret
from django.utils import timezone


class dao_pret(object):
	id = 0
	reference = None
	montant=0.0
	devise_id=None
	nbre_mensualite=4
	date_premiere_echeance = None
	taux_interet = 0
	description=None
	employe_id = None
	auteur_id = None
	rubrique_id = None

	@staticmethod
	def toListPret():
		return Model_Pret.objects.all().order_by('-id')
	
	@staticmethod
	def toListPretOfEmploye(employe_id):
		return Model_Pret.objects.filter(employe_id = employe_id).order_by('-id')

	@staticmethod
	def toCreatePret(reference, montant, devise_id, nbre_mensualite, employe_id, description, date_premiere_echeance, taux_interet = 0, rubrique_id = None):
		try:
			pret = dao_pret()
			pret.reference = reference
			pret.montant = montant
			pret.devise_id = devise_id
			pret.description = description
			pret.date_premiere_echeance = date_premiere_echeance
			pret.taux_interet = taux_interet
			pret.employe_id = employe_id
			pret.nbre_mensualite = nbre_mensualite
			pret.rubrique_id = rubrique_id
			return pret
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DU PRET')
			#print(e)
			return None

	@staticmethod
	def toSavePret(auteur,objet_dao_Pret):
		try:
			pret = Model_Pret()
			#print("objet_dao_Pret.employe_id", objet_dao_Pret.employe_id)
			#print("objet_dao_Pret.devise_id", objet_dao_Pret.devise_id)
			#print("objet_dao_Pret.rubrique_id", objet_dao_Pret.rubrique_id)
			pret.reference = objet_dao_Pret.reference
			pret.montant = objet_dao_Pret.montant
			pret.devise_id = objet_dao_Pret.devise_id
			pret.nbre_mensualite = objet_dao_Pret.nbre_mensualite
			pret.description = objet_dao_Pret.description
			pret.date_premiere_echeance = objet_dao_Pret.date_premiere_echeance
			pret.taux_interet = objet_dao_Pret.taux_interet
			pret.rubrique_id = objet_dao_Pret.rubrique_id
			pret.employe_id = objet_dao_Pret.employe_id
			pret.auteur_id = auteur.id
			pret.save()
			return pret
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT Du PRET')
			#print(e)
			return None

	@staticmethod
	def toUpdatePret(id, objet_dao_Pret):
		try:
			pret = Model_Pret.objects.get(pk = id)
			pret.montant = objet_dao_Pret.montant
			pret.devise_id = objet_dao_Pret.devise_id
			pret.nbre_mensualite = objet_dao_Pret.nbre_mensualite
			pret.description = objet_dao_Pret.description
			pret.date_premiere_echeance = objet_dao_Pret.date_premiere_echeance
			pret.taux_interet = objet_dao_Pret.taux_interet
			pret.rubrique_id = objet_dao_Pret.rubrique_id
			pret.employe_id = objet_dao_Pret.employe_id
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
	
	@staticmethod
	def toComputeMontantARembourser(employe_id):
		try:
			valeur = 0
			prets = dao_pret.toListPretOfEmploye(employe_id)
			for pret in prets:
				montant = pret.amount_to_pay if pret.is_running else 0
				valeur += montant

			if valeur > 0:
				ligne_paiement_pret = dao_ligne_paiement_pret.toCreateLignePaiementPret("Paiement pret {}".format(pret.reference), valeur, pret.devise_id, pret.id, True, "Paiement pret")
				ligne_paiement_pret = dao_ligne_paiement_pret.toSaveLignePaiementPret(None, ligne_paiement_pret)

			return valeur
		except Exception as e:
			#print("ERREUR montantARembourser")
			#print(e)
			return 0