from __future__ import unicode_literals
from ErpBackOffice.models import Model_Contrat
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class dao_contrat(object):
	id = 0
	numero_reference = ""
	objet = ''
	montant = 0.0
	devise_id = None
	type_marche_id = ''
	modalite = ""
	date_debut = None
	demande_cotation_id = 0
	appel_offre_id = None
	fournisseur_id = None
	date_fin = None


	@staticmethod
	def toListContrats():
		return Model_Contrat.objects.all().order_by('-id')

	@staticmethod
	def toListContrats_Garantie():
		return Model_Contrat.objects.filter(etat = "Garantie de bonne exécution").order_by('-id')
		# return Model_Contrat.objects.all()

	@staticmethod
	def toListContrats_receptio_pro():
		return Model_Contrat.objects.filter(etat = "Réception provisoire").order_by('-id')

	@staticmethod
	def toListContrats_reception_def():
		return Model_Contrat.objects.filter(etat = "Réception définitive").order_by('-id')

	@staticmethod
	def toListByTypeMarche(type_marche_id):
		return Model_Contrat.objects.filter(type_marche_id = type_marche_id).order_by('-id')

	@staticmethod
	def toCreateContrat(numero_reference, objet, montant, devise_id, type_marche_id, date_debut, fournisseur_id = None,  date_fin = None,demande_cotation_id = None, appel_offre_id = None, modalite = ""):
		try:
			contrat = dao_contrat()
			contrat.numero_reference = numero_reference
			contrat.objet = objet
			contrat.montant = montant
			contrat.devise_id = devise_id
			contrat.type_marche_id = type_marche_id
			contrat.date_debut = date_debut
			contrat.appel_offre_id = appel_offre_id
			contrat.demande_cotation_id = demande_cotation_id
			contrat.fournisseur_id = fournisseur_id
			contrat.date_fin = date_fin
			contrat.modalite = modalite

			return contrat
		except Exception as e:
			print('ERREUR LORS DE LA CREATION DE LA CONTRAT')
			print(e)
			return None

	@staticmethod
	def toSaveContrat(auteur, objet_dao_Contrat):
		try:
			contrat  = Model_Contrat()
			contrat.numero_reference = objet_dao_Contrat.numero_reference
			contrat.objet = objet_dao_Contrat.objet
			contrat.montant = objet_dao_Contrat.montant
			contrat.devise_id = objet_dao_Contrat.devise_id
			contrat.type_marche_id = objet_dao_Contrat.type_marche_id
			contrat.date_debut = objet_dao_Contrat.date_debut
			contrat.appel_offre_id = objet_dao_Contrat.appel_offre_id
			contrat.demande_cotation_id = objet_dao_Contrat.demande_cotation_id
			contrat.fournisseur_id = objet_dao_Contrat.fournisseur_id
			contrat.modalite = objet_dao_Contrat.modalite
			contrat.date_fin = objet_dao_Contrat.date_fin
			contrat.created_at = timezone.now()
			contrat.updated_at = timezone.now()
			contrat.auteur_id = auteur.id

			contrat.save()
			return contrat
		except Exception as e:
			print('ERREUR LORS DE L ENREGISTREMENT DE LA CONTRAT')
			print(e)
			return None

	@staticmethod
	def toUpdateContrat(id, objet_dao_Contrat):
		try:
			contrat = Model_Contrat.objects.get(pk = id)
			contrat.numero_reference = objet_dao_Contrat.numero_reference
			contrat.objet =objet_dao_Contrat.objet
			contrat.montant =objet_dao_Contrat.montant
			contrat.devise_id =objet_dao_Contrat.devise_id
			contrat.type_marche_id =objet_dao_Contrat.type_marche_id
			contrat.date_debut =objet_dao_Contrat.date_debut
			contrat.demande_cotation_id =objet_dao_Contrat.demande_cotation_id
			contrat.fournisseur_id = objet_dao_Contrat.fournisseur_id
			contrat.modalite = objet_dao_Contrat.modalite
			contrat.date_fin = objet_dao_Contrat.date_fin
			contrat.updated_at = timezone.now()
			contrat.save()
			return contrat
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CONTRAT')
			#print(e)
			return None
	@staticmethod
	def toGetContrat(id):
		try:
			return Model_Contrat.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteContrat(id):
		try:
			contrat = Model_Contrat.objects.get(pk = id)
			contrat.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroContrat():
		total_contrat = dao_contrat.toListContrats().count()
		total_contrat = total_contrat + 1
		temp_numero = str(total_contrat)

		for i in range(len(str(total_contrat)), 4):
			temp_numero = "0" + temp_numero

		# mois = timezone.now().month
		# if mois < 10: mois = "0%s" % mois

		# temp_numero = "CT-%s%s%s"%(timezone.now().year, temp_numero)
		_numero = "CT-{0}-ARPCE-DG-CGMP-{1}".format(temp_numero, timezone.now().year)
		return _numero