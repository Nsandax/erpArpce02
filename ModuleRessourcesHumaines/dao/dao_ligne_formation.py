from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ligne_Formation
from django.utils import timezone
from ErpBackOffice.models import Model_Categorie_employe
from ErpBackOffice.models import Model_Employe
from ErpBackOffice.models import Model_Formation
from django.db.models import Count

class dao_ligne_formation(object):
	id = 0
	formation_id = 0
	employe_id = 0
	competence = ''
	description = ''

	@staticmethod
	def toListLigneFormation():
		return Model_Ligne_Formation.objects.all().order_by('-id')

	@staticmethod
	def toCreateLigneFormation(formation_id,employe_id,competence,description):
		try:
			ligne_formation = dao_ligne_formation()
			ligne_formation.formation_id = formation_id
			ligne_formation.employe_id = employe_id
			ligne_formation.competence = competence
			ligne_formation.description = description
			return ligne_formation
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA LIGNE SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toSaveLigneFormation(auteur, objet_dao_ligne_formation):
		try:
			ligne_formation  = Model_Ligne_Formation()
			ligne_formation.formation_id = objet_dao_ligne_formation.formation_id
			ligne_formation.employe_id = objet_dao_ligne_formation.employe_id
			ligne_formation.competence = objet_dao_ligne_formation.competence
			ligne_formation.description = objet_dao_ligne_formation.description
			ligne_formation.created_at = timezone.now()
			ligne_formation.auteur_id = auteur.id

			ligne_formation.save()
			return ligne_formation
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA SYNDICAT')
			#print(e)
			return None

	@staticmethod
	def toUpdateLigneFormation(id, objet_dao_ligne_formation):
		try:
			ligne_formation = Model_Ligne_Formation.objects.get(pk = id)
			ligne_formation.formation_id = objet_dao_ligne_formation.formation_id
			ligne_formation.employe_id = objet_dao_ligne_formation.employe_id
			ligne_formation.competence = objet_dao_ligne_formation.competence
			ligne_formation.description = objet_dao_ligne_formation.description
			ligne_formation.updated_at = timezone.now()
			ligne_formation.save()
			return ligne_formation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA SYNDICAT')
			#print(e)
			return None
	@staticmethod
	def toGetLigneFormation(id):
		try:
			return Model_Ligne_Formation.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toList_employer_by_formation(id):
		try:
			return Model_Ligne_Formation.objects.filter(formation__pk= id)
		except Exception as e:
			#print(e)
			pass

	@staticmethod
	def toListLigneFormationByFormation(formation_id):
		try:
			return Model_Ligne_Formation.objects.filter(formation_id = formation_id)
		except Exception as e:
			return None

	@staticmethod
	def toDeleteLigneFormation(id):
		try:
			ligne_formation = Model_Ligne_Formation.objects.get(pk = id)
			ligne_formation.delete()
			return True
		except Exception as e:
			return False



	@staticmethod
	def toDeleteLigneFormationOfFormation(formation_id):
		try:
			return Model_Ligne_Formation.objects.filter(formation_id = formation_id).delete()
		except Exception as e:
			return False

	@staticmethod
	def toGetLigneFormationOfEmploye(employe_id):
		try:
			return Model.Ligne_Formation.objects.filter(employe_id = employe_id)
		except:
			return None


	@staticmethod
	def toGet_taux_depart_formation_by_categorie():
		somme = 0
		Year = timezone.now().year
		Total_formation = 0
		Taux_Formation = {}
		Agent_Formation = {}
		try:
			Liste_cat = Model_Categorie_employe.objects.all()
			Liste_employe = Model_Employe.objects.all()
			i = 2010
			while i <= Year:
				for item in Liste_employe:
					for cat in Liste_cat:
						somme += Model_Ligne_Formation.objects.filter(employe_id = item.id, employe__categorie_employe__categorie = cat.categorie, formation__annee = i).count()
				Total_formation += Model_Formation.objects.filter(annee = i).count()
				if somme != 0:
					Taux_Formation[i] = (100 * somme) / Total_formation
				else:
					Taux_Formation[i] = 0
				somme = 0
				Total_formation = 0
				i = i + 1
			# #print('**Dao_Ligne_Formation -- Taux de Formation par Categorie --: %s' %Taux_Formation)
			return Taux_Formation
		except Exception as e:
			#print(e)
			return Taux_Formation


	@staticmethod
	def toGet_taux_depart_formation_by_Direction():
		somme = 0
		Year = timezone.now().year
		Total_formation_Direct = 0
		Taux_Formation_Direct = {}
		List_Direction = ['DG', 'DAFC', 'DRSCE', 'DEM', 'DAJ', 'DMTHT']
		try:
			i = 2010 #
			while i <= Year:
				for item in List_Direction:
					somme += Model_Ligne_Formation.objects.filter(formation__annee = i, formation__departement = item).count()

				Total_formation_Direct = Model_Formation.objects.filter(annee = i).count()

				if somme != 0:
					Taux_Formation_Direct[i] = (100 * somme) / Total_formation_Direct
				else:
					Taux_Formation_Direct[i] = 0

				somme = 0
				Total_formation_Direct = 0
				i = i + 1

			# #print('**Dao_Ligne_Formation** Taux de formation par Direction: %s' %Taux_Formation_Direct)
			return Taux_Formation_Direct
		except Exception as e:
			#print(e)
			return Taux_Formation_Direct

	@staticmethod
	def toGet_Agent_Categorie_Formation():
		somme = 0
		Year = timezone.now().year
		List_personne = []
		Agent_Formation = {}
		try:
			Liste_cat = Model_Categorie_employe.objects.all()
			# employe__categorie_employe__categorie = cat.categorie,  for cat in Liste_cat:
			i = 2010
			while i <= Year:
				# for cat in Liste_cat:
				Ligne_Formation = Model_Ligne_Formation.objects.filter(created_at__year = i)
				for item in Ligne_Formation:
					List_personne.append(item.employe)

				somme = len(List_personne)
				Agent_Formation[i] = somme

				somme = 0
				i = i + 1

			# #print('--Dao_Ligne_Formation -- Nombre Agent parti en formation --: %s' %Agent_Formation)
			return Agent_Formation
		except Exception as e:
			#print(e)
			return Agent_Formation
