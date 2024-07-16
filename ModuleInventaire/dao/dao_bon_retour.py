from __future__ import unicode_literals
from ErpBackOffice.models import Model_Bon_transfert
from ErpBackOffice.models import Model_Bon_retour, Model_Emplacement, Model_TypeEmplacement
from django.utils import timezone

class dao_bon_retour(object):
	id = 0
	numero_bon_retour=''
	montant_global=0.0
	date_retour='2010-01-01'
	quantite=0
	description=''
	employe_id = None
	responsable_id = None
	auteur_id = None
	operation_stock_id = None
	emplacement_destination_id = None
	emplacement_origine_id = None
	est_realisee = False
	date_realisation = None
	reference_document = ""
	type=""
	agent_id = 0

	@staticmethod
	def toListBonRetour():
		return Model_Bon_retour.objects.all().order_by('-id')

	@staticmethod
	def toListBonOfTypeBonTransmission():
		return Model_Bon_retour.objects.filter(type__contains = "BON TRANSMISSION")

	@staticmethod
	def toListBonOfTypeBonTransmissionByAuteur(user_id):
		return Model_Bon_retour.objects.filter(type__contains = "BON TRANSMISSION").filter(auteur_id=user_id)

	@staticmethod
	def toListBonOfTypeSortieMaterielle():
		return Model_Bon_retour.objects.filter(type__contains = "SORTIE MATERIEL")

	@staticmethod
	def toListBonOfTypeRetourStock():
		return Model_Bon_retour.objects.filter(type__contains = "RETOUR STOCK")

	@staticmethod
	def toListBonOfTypeRetourStockByAuteur(user_id):
		return Model_Bon_retour.objects.filter(type__contains = "RETOUR STOCK").filter(auteur_id=user_id)

	@staticmethod
	def toListBonOfTypeSortieMaterielleByAuteur(user_id):
		return Model_Bon_retour.objects.filter(type__contains = "RETOUR MATERIEL").filter(auteur_id=user_id)

	@staticmethod
	def toListBonRetourByAuteur(user_id):
		return Model_Bon_retour.objects.filter(auteur_id=user_id)

	@staticmethod
	def toListRetourDuType(operation_stock_id):
		return Model_Bon_retour.objects.filter(operation_stock_id = operation_stock_id).order_by("-creation_date")

	@staticmethod
	def toListRetourDuTypeByAuteur(operation_stock_id, user_id):
		return Model_Bon_retour.objects.filter(operation_stock_id = operation_stock_id).filter(auteur_id=user_id).order_by("-creation_date")

	@staticmethod
	def toListTransfertsDeReferenceByAuteur(reference, user_id):
		transferts = []
		try:
			type_emplacement = Model_TypeEmplacement.objects.get(designation = reference)
			emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
			for emplacement in emplacements:
				trans = Model_Bon_retour.objects.filter(est_realisee = False).filter(auteur_id=user_id).filter(emplacement_id = emplacement.id).order_by("-creation_date")
				for item in trans :
					transferts.append(item)
			return transferts
		except Exception as e:
			##print("ERREUR LIST TRANSFERT")
			##print(e)
			return transferts

	@staticmethod
	def toListRetourStockDeReference(reference):
		transferts = []
		try:
			type_emplacement = Model_TypeEmplacement.objects.get(designation = reference)
			emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
			for emplacement in emplacements:
				trans = Model_Bon_retour.objects.filter(est_realisee = False).filter(emplacement_id = emplacement.id).order_by("-creation_date")
				for item in trans :
					transferts.append(item)
			return transferts
		except Exception as e:
			##print("ERREUR LIST TRANSFERT")
			##print(e)
			return transferts

	@staticmethod
	def toCreateBonTransfert(numero_bon_retour, est_realisee, date_retour, type, operation_stock_id = None,emplacement_origine_id=None, emplacement_destination_id = None, employe_id = None, reference_document = "", description = "", montant_global = 0.0, quantite = 0,status = "", date_realisation = None, responsable_id = None, agent_id = None):
		try:
			bon_retour = dao_bon_retour()
			if numero_bon_retour == None or numero_bon_retour == "":
				numero_bon_retour = dao_bon_retour.toGenerateNumeroBonRetour()
			bon_retour.numero_bon_retour = numero_bon_retour
			bon_retour.operation_stock_id = operation_stock_id
			bon_retour.emplacement_destination_id = emplacement_destination_id
			bon_retour.emplacement_origine_id = emplacement_origine_id
			bon_retour.employe_id = employe_id
			bon_retour.agent_id = agent_id
			bon_retour.reference_document = reference_document
			bon_retour.description = description
			bon_retour.montant_global = montant_global
			bon_retour.date_retour = date_retour
			bon_retour.est_realisee = est_realisee
			bon_retour.quantite = quantite
			bon_retour.status = status
			bon_retour.type = type
			bon_retour.responsable_id = responsable_id
			#print('**DEMANDEUR:', bon_retour.agent_id)
			return bon_retour
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DU BON RETOUR')
			#print(e)
			return None

	@staticmethod
	def toSaveBonTransfert(auteur,objet_dao_Bon_retour):
		try:
			##print("inside")
			bon_retour  = Model_Bon_retour()
			bon_retour.numero_bon_retour =objet_dao_Bon_retour.numero_bon_retour
			bon_retour.montant_global =objet_dao_Bon_retour.montant_global
			bon_retour.date_retour =objet_dao_Bon_retour.date_retour
			bon_retour.est_realisee =objet_dao_Bon_retour.est_realisee
			bon_retour.emplacement_origine_id = objet_dao_Bon_retour.emplacement_origine_id
			bon_retour.operation_stock_id = objet_dao_Bon_retour.operation_stock_id
			bon_retour.emplacement_destination_id = objet_dao_Bon_retour.emplacement_destination_id
			bon_retour.reference_document = objet_dao_Bon_retour.reference_document
			bon_retour.quantite = objet_dao_Bon_retour.quantite
			bon_retour.creaton_date = timezone.now()
			bon_retour.description =objet_dao_Bon_retour.description
			bon_retour.status =objet_dao_Bon_retour.status
			bon_retour.type = objet_dao_Bon_retour.type
			bon_retour.employe_id = objet_dao_Bon_retour.employe_id
			bon_retour.agent_id = objet_dao_Bon_retour.agent_id
			bon_retour.responsable_id = objet_dao_Bon_retour.responsable_id
			bon_retour.auteur_id = auteur.id
			bon_retour.save()
			return bon_retour
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DU BON RETOUR')
			#print(e)
			return None

	@staticmethod
	def toUpdateBonTransfert(id, objet_dao_Bon_transfert):
		try:
			bon_transfert = Model_Bon_retour.objects.get(pk = id)
			bon_transfert.numero_bon_retour =objet_dao_Bon_transfert.numero_bon_retour
			bon_transfert.montant_global =objet_dao_Bon_transfert.montant_global
			bon_transfert.date_retour =objet_dao_Bon_transfert.date_retour
			bon_transfert.est_realisee =objet_dao_Bon_transfert.est_realisee
			bon_transfert.operation_stock_id = objet_dao_Bon_transfert.operation_stock_id
			bon_transfert.emplacement_destination_id = objet_dao_Bon_transfert.emplacement_destination_id
			bon_transfert.emplacement_origine_id = objet_dao_Bon_transfert.emplacement_origine_id
			bon_transfert.reference_document = objet_dao_Bon_transfert.reference_document
			bon_transfert.quantite =objet_dao_Bon_transfert.quantite
			bon_transfert.description =objet_dao_Bon_transfert.description
			bon_transfert.date_realisation = objet_dao_Bon_transfert.date_realisation
			bon_transfert.status =objet_dao_Bon_transfert.status
			bon_transfert.type = objet_dao_Bon_transfert.type
			bon_transfert.employe_id = objet_dao_Bon_transfert.employe_id
			##print("dao")
			##print(objet_dao_Bon_transfert.agent_id)
			bon_transfert.agent_id = objet_dao_Bon_transfert.agent_id
			bon_transfert.responsable_id = objet_dao_Bon_transfert.responsable_id
			bon_transfert.save()
			##print("Bon transfert {0} modifie ".format(bon_transfert.id))
			return True
		except Exception as e:
			#print("Erreur Bon transfert {0} non modifie ".format(id))
			#print(e)
			return False

	@staticmethod
	def toGetBonRetour(id):
		try:
			return Model_Bon_retour.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteBonRetour(id):
		try:
			bon_retour = Model_Bon_retour.objects.get(pk = id)
			bon_retour.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroBonRetour():
		total_transferts = Model_Bon_retour.objects.all().count()
		total_transferts = total_transferts + 1
		temp_numero = str(total_transferts)

		for i in range(len(str(total_transferts)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "RET-%s%s%s" % (timezone.now().year, mois, temp_numero)
		#print('****NUMERO RETOUR***', temp_numero)
		return temp_numero