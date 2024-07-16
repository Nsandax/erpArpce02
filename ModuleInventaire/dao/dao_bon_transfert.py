from __future__ import unicode_literals
from ErpBackOffice.models import Model_Bon_transfert
from django.utils import timezone

class dao_bon_transfert(object):
	id = 0
	numero_transfert=''
	montant_global=0.0
	date_transfert='2010-01-01'
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
	def toListBonTransfert():
		return Model_Bon_transfert.objects.all().order_by('-id')

	@staticmethod
	def toListBonOfTypeBonTransmission():
		return Model_Bon_transfert.objects.filter(type__contains = "BON TRANSMISSION")

	@staticmethod
	def toListBonOfTypeBonTransmissionByAuteur(user_id):
		return Model_Bon_transfert.objects.filter(type__contains = "BON TRANSMISSION").filter(auteur_id=user_id)

	@staticmethod
	def toListBonOfTypeSortieMaterielle():
		return Model_Bon_transfert.objects.filter(type__contains = "SORTIE MATERIEL")

	@staticmethod
	def toListBonOfTypeSortieMaterielleByAuteur(user_id):
		return Model_Bon_transfert.objects.filter(type__contains = "SORTIE MATERIEL").filter(auteur_id=user_id)

	@staticmethod
	def toListBonTransfertByAuteur(user_id):
		return Model_Bon_transfert.objects.filter(auteur_id=user_id)

	@staticmethod
	def toListTransfertsDuType(operation_stock_id):
		return Model_Bon_transfert.objects.filter(operation_stock_id = operation_stock_id).order_by("-creation_date")

	@staticmethod
	def toListTransfertsDuTypeByAuteur(operation_stock_id, user_id):
		return Model_Bon_transfert.objects.filter(operation_stock_id = operation_stock_id).filter(auteur_id=user_id).order_by("-creation_date")

	@staticmethod
	def toListTransfertsDeReferenceByAuteur(reference, user_id):
		transferts = []
		try:
			type_emplacement = Model_TypeEmplacement.objects.get(designation = reference)
			emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
			for emplacement in emplacements:
				trans = Model_Bon_transfert.objects.filter(est_realisee = False).filter(auteur_id=user_id).filter(emplacement_id = emplacement.id).order_by("-creation_date")
				for item in trans :
					transferts.append(item)
			return transferts
		except Exception as e:
			#print("ERREUR LIST TRANSFERT")
			#print(e)
			return transferts

	@staticmethod
	def toListTransfertsDeReference(reference):
		transferts = []
		try:
			type_emplacement = Model_TypeEmplacement.objects.get(designation = reference)
			emplacements = Model_Emplacement.objects.filter(type_emplacement_id = type_emplacement.id)
			for emplacement in emplacements:
				trans = Model_Bon_transfert.objects.filter(est_realisee = False).filter(emplacement_id = emplacement.id).order_by("-creation_date")
				for item in trans :
					transferts.append(item)
			return transferts
		except Exception as e:
			#print("ERREUR LIST TRANSFERT")
			#print(e)
			return transferts

	@staticmethod
	def toCreateBonTransfert(numero_transfert, est_realisee, date_transfert, type, operation_stock_id = None,emplacement_origine_id=None, emplacement_destination_id = None, employe_id = None, reference_document = "", description = "", montant_global = 0.0, quantite = 0,status = "", date_realisation = None, responsable_id = None, agent_id = None):
		try:
			bon_transfert = dao_bon_transfert()
			if numero_transfert == None or numero_transfert == "":
				numero_transfert = dao_bon_transfert.toGenerateNumeroTransfert()
			bon_transfert.numero_transfert = numero_transfert
			bon_transfert.operation_stock_id = operation_stock_id
			bon_transfert.emplacement_destination_id = emplacement_destination_id
			bon_transfert.emplacement_origine_id = emplacement_origine_id
			bon_transfert.employe_id = employe_id
			bon_transfert.agent_id = agent_id
			bon_transfert.reference_document = reference_document
			bon_transfert.description = description
			bon_transfert.montant_global = montant_global
			bon_transfert.date_transfert = date_transfert
			bon_transfert.est_realisee = est_realisee
			bon_transfert.quantite = quantite
			bon_transfert.status = status
			bon_transfert.type = type
			bon_transfert.responsable_id = responsable_id
			return bon_transfert
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DU Bon de transfert')
			#print(e)
			return None

	@staticmethod
	def toSaveBonTransfert(auteur,objet_dao_Bon_transfert):
		try:
			#print("inside")
			bon_transfert  = Model_Bon_transfert()
			bon_transfert.numero_transfert =objet_dao_Bon_transfert.numero_transfert
			bon_transfert.montant_global =objet_dao_Bon_transfert.montant_global
			bon_transfert.date_transfert =objet_dao_Bon_transfert.date_transfert
			bon_transfert.est_realisee =objet_dao_Bon_transfert.est_realisee
			bon_transfert.emplacement_origine_id = objet_dao_Bon_transfert.emplacement_origine_id
			bon_transfert.operation_stock_id = objet_dao_Bon_transfert.operation_stock_id
			bon_transfert.emplacement_destination_id = objet_dao_Bon_transfert.emplacement_destination_id
			bon_transfert.reference_document = objet_dao_Bon_transfert.reference_document
			bon_transfert.quantite = objet_dao_Bon_transfert.quantite
			bon_transfert.creaton_date = timezone.now()
			bon_transfert.description =objet_dao_Bon_transfert.description
			bon_transfert.status =objet_dao_Bon_transfert.status
			bon_transfert.type = objet_dao_Bon_transfert.type
			bon_transfert.employe_id = objet_dao_Bon_transfert.employe_id
			bon_transfert.agent_id = objet_dao_Bon_transfert.agent_id
			bon_transfert.responsable_id = objet_dao_Bon_transfert.responsable_id
			bon_transfert.auteur_id = auteur.id
			bon_transfert.save()
			return bon_transfert
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DU Bon de transfert')
			print(e)
			return None

	@staticmethod
	def toUpdateBonTransfert(id, objet_dao_Bon_transfert):
		try:
			bon_transfert = Model_Bon_transfert.objects.get(pk = id)
			bon_transfert.numero_transfert =objet_dao_Bon_transfert.numero_transfert
			bon_transfert.montant_global =objet_dao_Bon_transfert.montant_global
			bon_transfert.date_transfert =objet_dao_Bon_transfert.date_transfert
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
			#print("dao")
			#print(objet_dao_Bon_transfert.agent_id)
			bon_transfert.agent_id = objet_dao_Bon_transfert.agent_id
			bon_transfert.responsable_id = objet_dao_Bon_transfert.responsable_id
			bon_transfert.save()
			#print("Bon transfert {0} modifie ".format(bon_transfert.id))
			return True
		except Exception as e:
			#print("Erreur Bon transfert {0} non modifie ".format(id))
			#print(e)
			return False

	@staticmethod
	def toGetBonTransfert(id):
		try:
			return Model_Bon_transfert.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteBonTransfert(id):
		try:
			bon_transfert = Model_Bon_transfert.objects.get(pk = id)
			bon_transfert.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroTransfert():
		total_transferts = dao_bon_transfert.toListBonTransfert().count()
		total_transferts = total_transferts + 1
		temp_numero = str(total_transferts)

		for i in range(len(str(total_transferts)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "TRA%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero


	@staticmethod
	def toGenerateNumeroBonSortie():
		total_transferts = dao_bon_transfert.toListBonTransfert().count()
		total_transferts = total_transferts + 1
		temp_numero = str(total_transferts)

		for i in range(len(str(total_transferts)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "BON-SORTIE-MAT-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero