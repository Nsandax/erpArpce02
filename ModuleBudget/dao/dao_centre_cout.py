from __future__ import unicode_literals
from ErpBackOffice.models import Model_Centre_cout, Model_LigneBudgetaire, Model_GroupeAnalytique, Model_Ecriture_analytique
from django.utils import timezone

class dao_centre_cout(object):
	id = 0
	designation = ''
	code = ''
	centre_cout_id = None
	typeCentre = 2
	abbreviation = ""
	groupe_analytique_id = None


	@staticmethod
	def toListCentre_cout():
		return Model_Centre_cout.objects.all().order_by('-id')

	@staticmethod
	def toListCentreCoutOfTypeView():
		return Model_Centre_cout.objects.filter(typeCentre=1)

	@staticmethod
	def toListCentreCoutOfTypeAccount():
		return Model_Centre_cout.objects.filter(typeCentre=2)

	@staticmethod
	def toListCentreCoutOfProjet():
		list_centre = []
		groupes = Model_GroupeAnalytique.objects.filter(designation__icontains="projet")
		for groupe in groupes:
			centres = Model_Centre_cout.objects.filter(groupe_analytique_id = groupe.id)
			if centres:
				list_centre.extend(centres)

		return list_centre

	@staticmethod
	def toCreateCentre_cout(designation,code,typeCentre, abbreviation,centre_cout_id, groupe_analytique_id = None):
		try:
			centre_cout = dao_centre_cout()
			centre_cout.designation = designation
			centre_cout.code = code
			centre_cout.abbreviation = abbreviation
			centre_cout.typeCentre = typeCentre
			centre_cout.centre_cout_id = centre_cout_id
			centre_cout.groupe_analytique_id = groupe_analytique_id
			return centre_cout
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CENTRE_COUT')
			#print(e)
			return None

	@staticmethod
	def toSaveCentre_cout(auteur, objet_dao_Centre_cout):
		try:
			centre_cout  = Model_Centre_cout()
			centre_cout.designation = objet_dao_Centre_cout.designation
			centre_cout.code = objet_dao_Centre_cout.code
			centre_cout.centre_cout_id = objet_dao_Centre_cout.centre_cout_id
			centre_cout.abbreviation = objet_dao_Centre_cout.abbreviation
			centre_cout.typeCentre = objet_dao_Centre_cout.typeCentre
			centre_cout.groupe_analytique_id = objet_dao_Centre_cout.groupe_analytique_id
			centre_cout.created_at = timezone.now()
			centre_cout.updated_at = timezone.now()
			centre_cout.auteur_id = auteur.id

			centre_cout.save()
			return centre_cout
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA CENTRE_COUT')
			#print(e)
			return None

	@staticmethod
	def toUpdateCentre_cout(id, objet_dao_Centre_cout):
		try:
			centre_cout = Model_Centre_cout.objects.get(pk = id)
			centre_cout.designation =objet_dao_Centre_cout.designation
			centre_cout.code =objet_dao_Centre_cout.code
			centre_cout.abbreviation = objet_dao_Centre_cout.abbreviation
			centre_cout.typeCentre = objet_dao_Centre_cout.typeCentre
			centre_cout.centre_cout_id =objet_dao_Centre_cout.centre_cout_id
			centre_cout.groupe_analytique_id = objet_dao_Centre_cout.groupe_analytique_id
			centre_cout.updated_at = timezone.now()
			centre_cout.save()
			return centre_cout
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA CENTRE_COUT')
			#print(e)
			return None
	@staticmethod
	def toGetCentre_cout(id):
		try:
			return Model_Centre_cout.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteCentre_cout(id):
		try:
			centre_cout = Model_Centre_cout.objects.get(pk = id)
			centre_cout.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toListLigneOfCentreTypeAccount(centre_cout_id):
		try:
			lignes = Model_LigneBudgetaire.objects.filter(centre_cout_id = centre_cout_id).order_by('-id')
			return lignes
		except Exception as e:
			return None

	@staticmethod
	def toRetrieveSousCentreofCentreCout(centre_cout_id):
		liste_centre = []
		centres = Model_Centre_cout.objects.filter(centre_cout_id = centre_cout_id)
		#print("centres before retrieve", centres)
		for centre in centres:
			if centre.typeCentre == 2:
				#print("centre 2",centre)
				liste_centre.append(centre)
			elif centre.typeCentre == 1:
				#print("centre 1",centre)
				liste_centre.extend(dao_centre_cout.toRetrieveSousCentreofCentreCout(centre.id))

		return liste_centre


	@staticmethod
	def toListLigneOfCentreTypeView(centre_cout_id):
		try:
			lignes_list = []
			centres = dao_centre_cout.toRetrieveSousCentreofCentreCout(centre_cout_id)
			#print("enjoyment",centres)
			for centre in centres:
				lignes = Model_LigneBudgetaire.objects.filter(centre_cout_id = centre.id).order_by('-id')
				if lignes:
					lignes_list.extend(lignes)
			return lignes_list
		except Exception as e:
			return None
	
	
	@staticmethod
	def toListEcritureAnalytiqueOfCentreTypeView(centre_cout_id, date_debut, date_fin):
		try:
			ecritures_list = []
			centres = dao_centre_cout.toRetrieveSousCentreofCentreCout(centre_cout_id)
			#print("enjoyment",centres)
			for centre in centres:
				ecritures = Model_Ecriture_analytique.objects.filter(centre_cout_id = centre.id).filter(created_at__lte = date_debut, created_at__gte = date_fin).order_by('-id')
				if ecritures:
					ecritures_list.extend(ecritures)
			return ecritures_list
		except Exception as e:
			return None

	@staticmethod
	def toComputeProjet():
		resultat = {
                'prevision':0,
                'realisation':0,
                'ecart':0
                }
		try:

			prevision = 0
			realisation = 0
			lignes = Model_LigneBudgetaire.objects.filter(centre_cout__groupe_analytique__est_projet = True)
			#print("lignes", lignes)
			for ligne in lignes:
				prevision += ligne.montant_alloue
				realisation += float(ligne.valeur_total_consommee)

			resultat['prevision'] = prevision
			resultat['realisation'] = realisation
			resultat['ecart'] = prevision - realisation

			return resultat
		except Exception as e:
			#print(e)
			return resultat