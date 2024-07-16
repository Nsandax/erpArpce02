from __future__ import unicode_literals
from ErpBackOffice.models import Model_Bon_commande
from django.utils import timezone

class dao_bon_commande(object):
	id = 0
	numero_commande=''
	date_commande= None
	montant_total = 0
	devise_id = None
	est_realisee = False
	reference_document = ""
	document_id = None
	client_id = None
	condition_reglement_id = None
	etat = ""
	statut_id = None
	auteur_id = None

	@staticmethod
	def toListBonCommande():
		return Model_Bon_commande.objects.all().order_by('-id')

	@staticmethod
	def toCreateBonCommande(numero_commande,date_commande,reference_document,etat,montant_total,devise_id=None,est_realisee=False,document_id=None,client_id=None,condition_reglement_id=None, statut_id=None):
		try:
			bon_commande = dao_bon_commande()
			bon_commande.numero_commande = numero_commande
			bon_commande.date_commande = date_commande
			bon_commande.reference_document = reference_document
			bon_commande.etat = etat
			bon_commande.montant_total = montant_total
			bon_commande.devise_id = devise_id
			bon_commande.est_realisee = est_realisee
			bon_commande.document_id = document_id
			bon_commande.client_id = client_id
			bon_commande.condition_reglement_id = condition_reglement_id
			bon_commande.statut_id = statut_id


			return bon_commande
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA BON_COMMANDE')
			#print(e)
			return None



	@staticmethod
	def toSaveBonCommande(auteur,objet_dao_Bon_commande):
		try:
			bon_commande  = Model_Bon_commande()
			bon_commande.numero_commande = objet_dao_Bon_commande.numero_commande
			bon_commande.date_commande = objet_dao_Bon_commande.date_commande
			bon_commande.reference_document = objet_dao_Bon_commande.reference_document
			bon_commande.etat = objet_dao_Bon_commande.etat
			bon_commande.montant_total = objet_dao_Bon_commande.montant_total
			bon_commande.devise_id = objet_dao_Bon_commande.devise_id
			bon_commande.est_realisee = objet_dao_Bon_commande.est_realisee
			bon_commande.document_id = objet_dao_Bon_commande.document_id
			bon_commande.client_id = objet_dao_Bon_commande.client_id
			bon_commande.condition_reglement_id = objet_dao_Bon_commande.condition_reglement_id
			bon_commande.statut_id = objet_dao_Bon_commande.statut_id
			bon_commande.auteur_id = auteur.id
			bon_commande.save()
			return bon_commande
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA BON_COMMANDE')
			#print(e)
			return None

	@staticmethod
	def toUpdateBonCommande(id, objet_dao_Bon_commande):
		try:
			bon_commande = Model_Bon_commande.objects.get(pk = id)
			bon_commande.numero_commande = objet_dao_Bon_commande.numero_commande
			bon_commande.date_commande = objet_dao_Bon_commande.date_commande
			bon_commande.reference_document = objet_dao_Bon_commande.reference_document
			bon_commande.etat = objet_dao_Bon_commande.etat
			bon_commande.montant_total = objet_dao_Bon_commande.montant_total
			bon_commande.devise_id = objet_dao_Bon_commande.devise_id
			bon_commande.est_realisee = objet_dao_Bon_commande.est_realisee
			bon_commande.document_id = objet_dao_Bon_commande.document_id
			bon_commande.client_id = objet_dao_Bon_commande.client_id
			bon_commande.condition_reglement_id = objet_dao_Bon_commande.condition_reglement_id
			bon_commande.statut_id = objet_dao_Bon_commande.statut_id
			bon_commande.save()
			return bon_commande
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA BON_COMMANDE')
			#print(e)
			return None

	@staticmethod
	def toGetBonCommande(id):
		try:
			return Model_Bon_commande.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toListCommandes():
		try:
			return Model_Bon_commande.objects.all()
		except Exception as e:
			return None

	@staticmethod
	def toDeleteBonCommande(id):
		try:
			bon_commande = Model_Bon_commande.objects.get(pk = id)
			bon_commande.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroCommande():
		total_commandes = dao_bon_commande.toListBonCommande().count()
		total_commandes = total_commandes + 1
		temp_numero = str(total_commandes)

		for i in range(len(str(total_commandes)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "BC-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero

	@staticmethod
	def toGetOrderMax():
		try:
			#return Model_Order.objects.all().aggregate(Max('rating'))
			max = Model_Bon_commande.objects.all().count()
			max = max + 1
			return max
		except Exception as e:
			#print("ERREUR")
			#print(e)
			return None
