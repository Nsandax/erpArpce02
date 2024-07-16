from __future__ import unicode_literals
from django.utils import timezone
from ErpBackOffice.models import Model_Bon_reception
from django.db.models import Q


class dao_bon_reception(object):
	id = 0
	numero_reception = ''
	date_prevue = None
	fournisseur_id = None
	ligne_budgetaire_id = None
	document_id = None
	condition_reglement_id = None
	demande_achat_id = None
	montant_total = 0.0
	est_realisee = False
	statut_id = None
	etat = ''
	auteur_id = None
	description = ""
	devise_id = None


	@staticmethod
	def toCreateBonReception(numero_reception,date_prevue,montant_total, etat, fournisseur_id = None,document_id = None, condition_reglement_id = None,demande_achat_id = None,ligne_budgetaire_id = None, est_realisee = False, description="", devise_id=None):
		try:
			bon_reception = dao_bon_reception()
			bon_reception.numero_reception = numero_reception
			bon_reception.date_prevue = date_prevue
			bon_reception.montant_total = montant_total
			bon_reception.etat = etat
			bon_reception.fournisseur_id = fournisseur_id
			bon_reception.document_id = document_id
			bon_reception.condition_reglement_id = condition_reglement_id
			bon_reception.demande_achat_id = demande_achat_id
			bon_reception.est_realisee = est_realisee
			bon_reception.ligne_budgetaire_id = ligne_budgetaire_id
			bon_reception.description = description
			bon_reception.devise_id = devise_id
			return bon_reception
		except Exception as e:
			# print('ERREUR LORS DE LA CREATION DE LA BON_reception')
			# print(e)
			return None

	@staticmethod
	def toSaveBonReception(auteur,objet_dao_Bon_reception):
		try:
			bon_reception  = Model_Bon_reception()
			bon_reception.numero_reception = objet_dao_Bon_reception.numero_reception
			bon_reception.date_prevue = objet_dao_Bon_reception.date_prevue
			bon_reception.montant_total = objet_dao_Bon_reception.montant_total
			bon_reception.etat = objet_dao_Bon_reception.etat
			bon_reception.fournisseur_id = objet_dao_Bon_reception.fournisseur_id
			bon_reception.ligne_budgetaire_id = objet_dao_Bon_reception.ligne_budgetaire_id
			bon_reception.document_id = objet_dao_Bon_reception.document_id
			bon_reception.condition_reglement_id = objet_dao_Bon_reception.condition_reglement_id
			bon_reception.demande_achat_id = objet_dao_Bon_reception.demande_achat_id
			bon_reception.est_realisee = objet_dao_Bon_reception.est_realisee
			bon_reception.description = objet_dao_Bon_reception.description
			bon_reception.auteur_id = auteur.id
			bon_reception.devise_id = objet_dao_Bon_reception.devise_id
			bon_reception.save()
			return bon_reception
		except Exception as e:
			# print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_reception')
			# print(e)
			return None

	@staticmethod
	def toListBonReception():
		return Model_Bon_reception.objects.filter(is_actif=True).order_by("-creation_date")

	@staticmethod
	def toListBonReceptionByAuteur(user_id):
		return Model_Bon_reception.objects.filter(auteur_id=user_id,is_actif=True).order_by("-creation_date")

	@staticmethod
	def toListBonReceptionRecentes():
		try:
			bons = Model_Bon_reception.objects.filter(is_actif=True).order_by('-id')[:5]
			return bons
		except Exception as e:
			return None

	@staticmethod
	def toListBonReceptionRecentesByAuteur(user_id):
		try:
			bons = Model_Bon_reception.objects.filter(auteur_id=user_id,is_actif=True).order_by('-id')[:5]
			return bons
		except Exception as e:
			return None

	@staticmethod
	def toListBCencours():
		try:
			bons = Model_Bon_reception.objects.filter(Q(etat__gt='Créé') | Q(etat = 'Approuvé')|Q(is_actif=True))
			return bons
		except Exception as e:
			return None

	@staticmethod
	def toListBonsReceptionDuStatus(etat):
		return Model_Bon_reception.objects.filter(date_reception__isnull = False,is_actif=True).filter(etat = etat).order_by("-creation_date")

	@staticmethod
	def toListBonsReceptionDuStatusByAuteur(etat, user_id):
		return Model_Bon_reception.objects.filter(date_reception__isnull = False,is_actif=True).filter(etat = etat).filter(auteur_id=user_id).order_by("-creation_date")

	@staticmethod
	def toListBonsReceptionEnAttente():
		return Model_Bon_reception.objects.filter(est_realisee = False,is_actif=True).filter(etat = "Accusé de reception téléchargé").order_by("-creation_date")

	@staticmethod
	def toListBonsReceptionEnAttenteByAuteur(user_id):
		return Model_Bon_reception.objects.filter(est_realisee = False,is_actif=True).filter(etat = "Accusé de reception téléchargé").filter(auteur_id=user_id).order_by("-creation_date")

	@staticmethod
	def toListBonsReceptionFournisseur(bon_reception_id):
		return Model_Bon_reception.objects.filter(bon_reception_id = bon_reception_id).order_by("-creation_date")

	@staticmethod
	def toListBonsReceptionFournisseurByAuteur(bon_reception_id, user_id):
		return Model_Bon_reception.objects.filter(bon_reception_id = bon_reception_id).filter(auteur_id=user_id, is_actif=True).order_by("-creation_date")

	@staticmethod
	def toListFournitures():
		return Model_Bon_reception.objects.filter(est_realisee = True).order_by("-creation_date")

	@staticmethod
	def toListFournituresByAuteur(user_id):
		return Model_Bon_reception.objects.filter(auteur_id=user_id).filter(est_realisee = True).order_by("-creation_date")

	@staticmethod
	def toListFournituresFacturables():
		list = []
		for fourniture in dao_bon_reception.toListFournitures() :
			if fourniture.est_facturable == True : list.append(fourniture)
		return list

	@staticmethod
	def toListFournituresFacturablesByWorkflow():
		list = []
		for fourniture in dao_bon_reception.toListFournitures() :
			if fourniture.etat == "Articles récus" : list.append(fourniture)
		return list

	@staticmethod
	def toListFournituresFacturablesByAuteur(user_id):
		list = []
		for fourniture in dao_bon_reception.toListFournituresByAuteur(user_id) :
			if fourniture.est_facturable == True : list.append(fourniture)
		return list

	@staticmethod
	def toListFournituresDuFournisseur(fournisseur_id):
		return Model_Bon_reception.objects.filter(est_realisee = True,is_actif=True).filter(fournisseur_id = fournisseur_id).order_by("-creation_date")

	@staticmethod
	def toListFournituresDuFournisseurByAuteur(fournisseur_id, user_id):
		return Model_Bon_reception.objects.filter(est_realisee = True, is_actif=True).filter(fournisseur_id = fournisseur_id).filter(auteur_id=user_id).order_by("-creation_date")

	@staticmethod
	def toListFournituresFacturablesDuFournisseur(fournisseur_id):
		list = []
		for fourniture in dao_bon_reception.toListFournituresDuFournisseur(fournisseur_id) :
			if fourniture.est_facturable == True : list.append(fourniture)
		return list

	@staticmethod
	def toListFournituresFacturablesDuFournisseurByAuteur(fournisseur_id, user_id):
		list = []
		for fourniture in dao_bon_reception.toListFournituresDuFournisseurByAuteur(fournisseur_id, user_id) :
			if fourniture.est_facturable == True : list.append(fourniture)
		return list

	@staticmethod
	def toUpdateBonReception(id, objet_dao_Bon_reception):
		try:
			bon_reception = Model_Bon_reception.objects.get(pk = id)
			bon_reception.numero_reception = objet_dao_Bon_reception.numero_reception
			#bon_reception.date_reception = objet_dao_Bon_reception.date_reception
			bon_reception.montant_total = objet_dao_Bon_reception.montant_total
			bon_reception.etat = objet_dao_Bon_reception.etat
			bon_reception.fournisseur_id = objet_dao_Bon_reception.fournisseur_id
			bon_reception.document_id = objet_dao_Bon_reception.document_id
			bon_reception.ligne_budgetaire_id = objet_dao_Bon_reception.ligne_budgetaire_id
			bon_reception.condition_reglement_id = objet_dao_Bon_reception.condition_reglement_id
			bon_reception.demande_achat_id = objet_dao_Bon_reception.demande_achat_id
			bon_reception.est_realisee = objet_dao_Bon_reception.est_realisee
			bon_reception.description = objet_dao_Bon_reception.description
			bon_reception.save()
			return bon_reception

		except Exception as e:
			# print('ERREUR LORS DE LA MODIFICATION DE LA BON_reception')
			# print(e)
			return None

	@staticmethod
	def toGetBonReception(id):
		try:
			return Model_Bon_reception.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetBonReceptionCount():
		try:
			temps= timezone.now().month
			return Model_Bon_reception.objects.filter(creation_date__month=temps).count()
		except Exception as e:
			return None

	@staticmethod
	def toDeleteBonReception(id):
		try:
			bon_reception = Model_Bon_reception.objects.get(pk = id)
			bon_reception.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroReception():
		total_receptions = dao_bon_reception.toListBonReception().count()
		total_receptions = total_receptions + 1
		temp_numero = str(total_receptions)

		for i in range(len(str(total_receptions)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "BC-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero

	@staticmethod
	def toGetOrderMax():
		try:
			#return Model_Order.objects.all().aggregate(Max('rating'))
			max = Model_Bon_reception.objects.all().count()
			max = max + 1
			return max
		except Exception as e:
			#print("ERREUR")
			#print(e)
			return None

	@staticmethod
	def toGetOrderMaxByAuteur(user_id):
		try:
			#return Model_Order.objects.all().aggregate(Max('rating'))
			max = Model_Bon_reception.objects.filter(auteur_id=user_id).count()
			max = max + 1
			return max
		except Exception as e:
			#print("ERREUR")
			#print(e)
			return None
