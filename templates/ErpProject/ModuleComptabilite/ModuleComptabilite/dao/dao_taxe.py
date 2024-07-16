from __future__ import unicode_literals
from ErpBackOffice.models import Model_Taxe
from django.utils import timezone
from ModuleComptabilite.dao.dao_compte import dao_compte
from django.db.models import Q


class dao_taxe(object):
	id = 0
	designation = ''
	categorie_taxe = ''
	portee_taxe = 0
	type_montant_taxe = ''
	montant = 0.0
	compte_taxe_id = None
	est_active = False
	description = ''
	devise_id = None

	@staticmethod
	def toListTaxe():
		return Model_Taxe.objects.all().order_by('-id')

	@staticmethod
	def toListTaxeOfTypeAchat():
		return Model_Taxe.objects.exclude(portee_taxe = 1)

	@staticmethod
	def toListTaxeOfTypeVente():
		return Model_Taxe.objects.exclude(portee_taxe = 2)

	@staticmethod
	def toCreateTaxe(designation,categorie_taxe,portee_taxe,type_montant_taxe,montant,compte_taxe_id,est_active,description, devise_id=None):
		try:
			taxe = dao_taxe()
			taxe.designation = designation
			taxe.categorie_taxe = categorie_taxe
			taxe.portee_taxe = portee_taxe
			taxe.type_montant_taxe = type_montant_taxe
			taxe.montant = montant
			taxe.compte_taxe_id = compte_taxe_id
			taxe.est_active = est_active
			taxe.description = description
			taxe.devise_id = devise_id
			return taxe
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TAXE')
			#print(e)
			return None

	@staticmethod
	def toSaveTaxe(auteur, objet_dao_Taxe):
		try:
			taxe  = Model_Taxe()
			taxe.designation = objet_dao_Taxe.designation
			taxe.categorie_taxe = objet_dao_Taxe.categorie_taxe
			taxe.portee_taxe = objet_dao_Taxe.portee_taxe
			taxe.type_montant_taxe = objet_dao_Taxe.type_montant_taxe
			taxe.montant = objet_dao_Taxe.montant
			taxe.compte_taxe_id = objet_dao_Taxe.compte_taxe_id
			taxe.est_active = objet_dao_Taxe.est_active
			taxe.description = objet_dao_Taxe.description
			taxe.devise_id = objet_dao_Taxe.devise_id
			taxe.created_at = timezone.now()
			taxe.updated_at = timezone.now()
			taxe.auteur_id = auteur.id

			taxe.save()
			return taxe
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TAXE')
			#print(e)
			return None

	@staticmethod
	def toUpdateTaxe(id, objet_dao_Taxe):
		try:
			taxe = Model_Taxe.objects.get(pk = id)
			taxe.designation =objet_dao_Taxe.designation
			taxe.categorie_taxe =objet_dao_Taxe.categorie_taxe
			taxe.portee_taxe =objet_dao_Taxe.portee_taxe
			taxe.type_montant_taxe =objet_dao_Taxe.type_montant_taxe
			taxe.montant =objet_dao_Taxe.montant
			taxe.compte_taxe_id =objet_dao_Taxe.compte_taxe_id
			taxe.est_active =objet_dao_Taxe.est_active
			taxe.description =objet_dao_Taxe.description
			taxe.devise_id = objet_dao_Taxe.devise_id
			taxe.updated_at = timezone.now()
			taxe.save()
			return taxe
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TAXE')
			#print(e)
			return None
	@staticmethod
	def toGetTaxe(id):
		try:
			return Model_Taxe.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTaxe(id):
		try:
			taxe = Model_Taxe.objects.get(pk = id)
			taxe.delete()
			return True
		except Exception as e:
			return False


	@staticmethod
	def toComputeMontantAndEcritureTaxe(list_taxe_id, montant_total,ecritures_taxes, centre_cout_id = None):
		try:
			montant_taxe = 0
			montant_ttc = 0
			#print("we are here")
			for taxe_id in list_taxe_id:
				montant_ecriture = 0
				taxe = dao_taxe.toGetTaxe(taxe_id)
				if taxe.type_montant_taxe == 1:
					montant_taxe += taxe.montant
					montant_ecriture = taxe.montant
					#ecriture comptable
					if taxe.compte_taxe_id != None:
						ecriture = {
						"id" : taxe.compte_taxe_id,
						"libelle" : taxe.designation,
						"compte" : "%s %s" % (taxe.compte_taxe.numero, taxe.compte_taxe.designation),
						"montant" : montant_ecriture,
						"centre_cout_id":centre_cout_id
						}
						ecritures_taxes.append(ecriture)
					else:
						if taxe.montant != 0:
							compte_taxe = dao_compte.toGetCompteTaxe()
							ecriture = {
							"id" : compte_taxe.id,
							"libelle" : taxe.designation,
							"compte" : "%s %s" % (compte_taxe.numero, compte_taxe.designation),
							"montant" : montant_ecriture,
							"centre_cout_id":centre_cout_id
							}
							ecritures_taxes.append(ecriture)

				elif taxe.type_montant_taxe == 2:
					montant_taxe += montant_total * (taxe.montant/100)
					montant_ecriture = montant_total * (taxe.montant/100)
					#ecriture comptable
					if taxe.compte_taxe_id != None:
						ecriture = {
						"id" : taxe.compte_taxe_id,
						"libelle" : taxe.designation,
						"compte" : "%s %s" % (taxe.compte_taxe.numero, taxe.compte_taxe.designation),
						"montant" : montant_ecriture,
						"centre_cout_id":centre_cout_id
						}
						ecritures_taxes.append(ecriture)
					else:
						if taxe.montant != 0:
							compte_taxe = dao_compte.toGetCompteTaxe()
							ecriture = {
							"id" : compte_taxe.id,
							"libelle" : taxe.designation,
							"compte" : "%s %s" % (compte_taxe.numero, compte_taxe.designation),
							"montant" : montant_ecriture,
							"centre_cout_id":centre_cout_id
							}
							ecritures_taxes.append(ecriture)





			for taxe_id in list_taxe_id:
				taxe = dao_taxe.toGetTaxe(taxe_id)
				if taxe.type_montant_taxe == 3:
					montant_ttc = montant_total + montant_taxe
					montant_taxe = montant_ttc * (taxe.montant/100)
					montant_ecriture = montant_ttc * (taxe.montant/100)
					#ecriture comptable
					if taxe.compte_taxe_id != None:
						ecriture = {
						"id" : taxe.compte_taxe_id,
						"libelle" : taxe.designation,
						"compte" : "%s %s" % (taxe.compte_taxe.numero, taxe.compte_taxe.designation),
						"montant" : montant_ecriture
						}
						ecritures_taxes.append(ecriture)
					else:
						if taxe.montant != 0:
							compte_taxe = dao_compte.toGetCompteTaxe()
							ecriture = {
							"id" : compte_taxe.id,
							"libelle" : taxe.designation,
							"compte" : "%s %s" % (compte_taxe.numero, compte_taxe.designation),
							"montant" : montant_ecriture
							}
							ecritures_taxes.append(ecriture)

			#print("quit out",ecritures_taxes)
			return montant_taxe, ecritures_taxes
		except Exception as e:
			return 0, []


	@staticmethod
	def toDesignListTaxe(list_taxe_id, list_counter_select):
		try:
			list_taxe_final = []
			list_inside = []
			compteur = 0
			taille = 0

			for elt in list_counter_select:
				taille = compteur + int(elt)
				for i in range(compteur,taille):
					list_inside.append(list_taxe_id[i])
				list_taxe_final.append(list_inside)
				list_inside = []
				compteur = taille

			return list_taxe_final
		except Exception as e:
			return []




