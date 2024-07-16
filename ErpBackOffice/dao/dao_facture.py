from __future__ import unicode_literals
from ErpBackOffice.models import Model_Facture, Model_ConditionReglement, Model_Paiement, Model_Transaction
from django.utils import timezone
import json
from datetime import time, timedelta, datetime
from django.db.models import Q


class dao_facture(object):
	id = 0
	numero_facture = ""
	montant = 0
	est_soldee = False
	bon_commande_id = 0
	bon_reception_id = 0
	fournisseur_id = None
	client_id = None
	periode = ""
	date_facturation = ""
	document = ""
	journal_comptable_id  = 0
	type = ""
	auteur_id = 0
	facture_mere_id = None
	lettrage_id  = None
	condition_reglement_id = None
	montant_en_lettre = ""
	etat_facturation_id = None
	type_facture_client = None

	@staticmethod
	def toUpdateFacture(id, objet_dao_facture):
		try:
			facture = Model_Facture.objects.get(pk = id)
			facture.facture_mere_id = objet_dao_facture.facture_mere_id
			facture.numero_facture = objet_dao_facture.numero_facture
			facture.fournisseur_id = objet_dao_facture.fournisseur_id
			facture.client_id = objet_dao_facture.client_id
			facture.montant =	objet_dao_facture.montant
			facture.date_facturation = objet_dao_facture.date_facturation
			facture.est_soldee = objet_dao_facture.est_soldee
			facture.bon_commande_id	= objet_dao_facture.bon_commande_id
			facture.journal_comptable_id = objet_dao_facture.journal_comptable_id
			facture.periode = objet_dao_facture.periode
			facture.save()
			return facture
		except Exception as e:
			#print("ERREUR UPDATE DAO FACTURE")
			#print(e)
			return None

	@staticmethod
	def toCreateFacture(date_facturation, numero_facture, montant, bon_commande_id = None, bon_reception_id = None, journal_comptable_id = None, periode = "", document = "", fournisseur_id = None, client_id = None, facture_mere_id = None, lettrage_id = None, condition_reglement_id = None, montant_en_lettre = "",etat_facturation_id = None, type_facture_client = None):
		try:
			#print(bon_commande_id)
			#print(bon_reception_id)
			facture = dao_facture()
			if numero_facture == None or numero_facture == "":
				numero_facture = dao_facture.toGenerateNumeroFacture()
			facture.numero_facture = numero_facture
			facture.facture_mere_id = facture_mere_id
			facture.montant = montant
			facture.date_facturation = date_facturation
			facture.est_soldee = False
			facture.bon_commande_id = bon_commande_id
			facture.bon_reception_id = bon_reception_id
			if periode == None or periode == "":
				periode = dao_facture.toMakePeriodeFacture(date_facturation)
			facture.periode = periode
			facture.fournisseur_id = fournisseur_id
			facture.client_id = client_id
			facture.journal_comptable_id = journal_comptable_id
			facture.document = document
			facture.lettrage_id = lettrage_id
			facture.condition_reglement_id = condition_reglement_id
			facture.montant_en_lettre = montant_en_lettre
			facture.etat_facturation_id = etat_facturation_id
			facture.type_facture_client = type_facture_client
			return facture
		except Exception as e:
			#print("ERREUR LORS DE LA CREATION DE LA FACTURE")
			#print(e)
			return None


	@staticmethod
	def toSaveFacture(auteur, objet_dao_facture):
		try :
			#print("sdud")
			facture = Model_Facture()
			facture.numero_facture = objet_dao_facture.numero_facture
			facture.facture_mere_id = objet_dao_facture.facture_mere_id
			facture.fournisseur_id = objet_dao_facture.fournisseur_id
			facture.client_id = objet_dao_facture.client_id
			facture.montant = objet_dao_facture.montant
			facture.est_soldee = objet_dao_facture.est_soldee
			if objet_dao_facture.date_facturation == None:
				facture.date_facturation = timezone.now()
			else : facture.date_facturation = objet_dao_facture.date_facturation
			#print("jskjskj")
			facture.bon_commande_id = objet_dao_facture.bon_commande_id
			facture.bon_reception_id = objet_dao_facture.bon_reception_id
			facture.periode = objet_dao_facture.periode
			facture.type = objet_dao_facture.type
			#print("ksoklsk")
			facture.journal_comptable_id = objet_dao_facture.journal_comptable_id
			facture.auteur_id = auteur.id
			facture.creation_date = timezone.now()
			facture.document = objet_dao_facture.document
			facture.lettrage_id = objet_dao_facture.lettrage_id
			facture.montant_en_lettre = objet_dao_facture.montant_en_lettre
			facture.etat_facturation_id = objet_dao_facture.etat_facturation_id
			facture.condition_reglement_id = objet_dao_facture.condition_reglement_id
			#print("condition de reglement")
			if objet_dao_facture.condition_reglement_id != None and objet_dao_facture.condition_reglement_id != 0:
				condition_reglement = Model_ConditionReglement.objects.get(pk = objet_dao_facture.condition_reglement_id)
				date_echeance = facture.date_facturation.date() + timedelta(days = condition_reglement.nombre_jours)
				facture.date_echeance = date_echeance
			facture.type_facture_client = objet_dao_facture.type_facture_client
			facture.save()
			return facture
		except Exception as e:
			#print("ERREUR")
			#print(e)
			return None

	@staticmethod
	def toGetFacture(id):
		try:
			return Model_Facture.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListFactures():
		try:
			return Model_Facture.objects.all()
		except Exception as e:
			return None

	@staticmethod
	def toListFacturesNonSoldees():
		try:
			return Model_Facture.objects.filter(est_soldee = False).filter(Q(etat = "Facture approuvée") | Q(etat = "Accusé de reception téléchargée"))
		except Exception as e:
			return None

	@staticmethod
	def toDeleteFacture(id):
		try:
			facture = Model_Facture.objects.get(pk = id)
			facture.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toMakePeriodeFacture(date_facturation):
		periode = "Janvier"
		if date_facturation.month == 2: periode = "Fevrier"
		elif date_facturation.month == 3: periode = "Mars"
		elif date_facturation.month == 4: periode = "Avril"
		elif date_facturation.month == 5: periode = "Mai"
		elif date_facturation.month == 6: periode = "Juin"
		elif date_facturation.month == 7: periode = "Juillet"
		elif date_facturation.month == 8: periode = "Aout"
		elif date_facturation.month == 9: periode = "Septembre"
		elif date_facturation.month == 10: periode = "Octobre"
		elif date_facturation.month == 11: periode = "Novembre"
		elif date_facturation.month == 12: periode = "Decembre"

		return "%s %s" % (periode, date_facturation.year)

	@staticmethod
	def toGenerateNumeroFacture():
		total_factures = Model_Facture.objects.count()
		total_factures = total_factures + 1
		temp_numero = str(total_factures)

		for i in range(len(str(total_factures)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "FA%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero


	@staticmethod
	def toListFacturesFilles(facture_mere_id):
		try:
			return Model_Facture.objects.filter(facture_mere = facture_mere_id)
		except Exception as e:
			print(e)
			return None

	@staticmethod
	def toCheckIfHasGotFactureAvoir(id):
		try:
			factures_filles = Model_Facture.objects.filter(facture_mere = id)
			has_got_facture_avoir = False
			for facture in factures_filles:
				if facture.est_facture_avoir:
					has_got_facture_avoir = True
			return has_got_facture_avoir
		except Exception as e:
			return False



	@staticmethod
	def toGetMontantRestantOfPaymentFacture(facture_id):
		try:
			montant = 0
			paiements = Model_Paiement.objects.filter(facture_id = facture_id, est_valide = True)

			if paiements.count() != 0 :
				for paiement in paiements:
					if int(paiement.transaction.moyen_paiement) == 1:
						montant = montant + paiement.montant
					elif int(paiement.transaction.moyen_paiement) == 2 :
						transaction = Model_Transaction.objects.get(paiement_id = paiement.id)
						payloads = json.loads(transaction.payloads.replace("'",'"'))

						pay_montant = float(payloads["montant"])
						pay_currency = int(payloads["devise"])
						montant = montant + pay_montant
			return montant
		except Exception as e:
			return 0


	@staticmethod
	def toListTypeFactClientNotCreated(etat_facturation_id):
		try:
			data = []
			factures = Model_Facture.objects.filter(etat_facturation = etat_facturation_id)
			if not factures :
				#print("Aucun")
				data.append("Agence")
				data.append("Trésor publique")
			else:
				if not Model_Facture.objects.filter(etat_facturation = etat_facturation_id, type_facture_client = "Agence"):
					#print("Agence pas trouvé")
					data.append("Agence")
				if not Model_Facture.objects.filter(etat_facturation = etat_facturation_id, type_facture_client = "Trésor publique"):
					#print("Trésor pas trouvé")
					data.append("Trésor publique")

			return data
		except Exception as e:
			#print("Erreur Get Type Facture")
			#print(e)
			pass
