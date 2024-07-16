from __future__ import unicode_literals
from ErpBackOffice.models import Model_Mobilite
from django.utils import timezone
from ErpBackOffice.models import Model_Employe
from django.template.defaulttags import register
from django import template

register = template.Library()

class dao_mobilite(object):
	id = 0
	direction = ''
	service = ""
	type_mobilite = ''
	fonctions_occupees = ''
	ponderation = 0
	categorie_socio_professionnelle = ''
	categorie_socia_pro_precedent = ''
	modalites = ''
	date_entree = '01/01/2010'
	date_sortie =  '01/01/2010'
	employe_id = None

	@staticmethod
	def toListMobilite():
		return Model_Mobilite.objects.all().order_by('-id')

	@staticmethod
	def toCreateMobilite(direction,service,type_mobilite,fonctions_occupees, ponderation,categorie_socio_professionnelle,modalites,date_entree,date_sortie,employe_id,categorie_socia_pro_precedent=""):
		try:
			mobilite = dao_mobilite()
			mobilite.direction = direction
			mobilite.service = service
			mobilite.type_mobilite = type_mobilite
			mobilite.fonctions_occupees = fonctions_occupees
			mobilite.ponderation = ponderation
			mobilite.categorie_socio_professionnelle = categorie_socio_professionnelle
			mobilite.categorie_socia_pro_precedent = categorie_socia_pro_precedent
			mobilite.modalites = modalites
			mobilite.date_entree = date_entree
			mobilite.date_sortie = date_sortie
			mobilite.employe_id = employe_id
			return mobilite
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA MOBILITE IN DAO MOBILITE TO CREATEMOB ')
			#print(e)
			return None

	@staticmethod
	def toSaveMobilite(auteur, objet_dao_Mobilite):
		try:
			mobilite  = Model_Mobilite()
			mobilite.direction = objet_dao_Mobilite.direction
			mobilite.service = objet_dao_Mobilite.service
			mobilite.type_mobilite = objet_dao_Mobilite.type_mobilite
			mobilite.fonctions_occupees = objet_dao_Mobilite.fonctions_occupees
			mobilite.categorie_socio_professionnelle = objet_dao_Mobilite.categorie_socio_professionnelle
			mobilite.categorie_socia_pro_precedent = objet_dao_Mobilite.categorie_socia_pro_precedent
			mobilite.modalites = objet_dao_Mobilite.modalites
			mobilite.ponderation = objet_dao_Mobilite.ponderation
			mobilite.date_entree = objet_dao_Mobilite.date_entree
			mobilite.date_sortie = objet_dao_Mobilite.date_sortie
			mobilite.employe_id = objet_dao_Mobilite.employe_id
			mobilite.created_at = timezone.now()
			mobilite.updated_at = timezone.now()
			mobilite.auteur_id = auteur.id

			mobilite.save()
			return mobilite
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA MOBILITE IN DAO MOBILTE TO SAVE')
			#print(e)
			return None

	@staticmethod
	def toUpdateMobilite(id, objet_dao_Mobilite):
		try:
			mobilite = Model_Mobilite.objects.get(pk = id)
			mobilite.direction =objet_dao_Mobilite.direction
			mobilite.service =objet_dao_Mobilite.service
			mobilite.type_mobilite=objet_dao_Mobilite.type_mobilite
			mobilite.fonctions_occupees =objet_dao_Mobilite.fonctions_occupees
			mobilite.categorie_socio_professionnelle = objet_dao_Mobilite.categorie_socio_professionnelle
			mobilite.categorie_socia_pro_precedent = objet_dao_Mobilite.categorie_socia_pro_precedent
			mobilite.modalites =objet_dao_Mobilite.modalites
			mobilite.ponderation = objet_dao_Mobilite.ponderation
			mobilite.date_entree =objet_dao_Mobilite.date_entree
			mobilite.date_sortie =objet_dao_Mobilite.date_sortie
			mobilite.employe_id =objet_dao_Mobilite.employe_id
			mobilite.updated_at = timezone.now()
			mobilite.save()
			return mobilite
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA MOBILITE')
			#print(e)
			return None
	@staticmethod
	def toGetMobilite(id):
		try:
			return Model_Mobilite.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetMobiliteByEmploye(employe_id):
		try:
			return Model_Mobilite.objects.filter(employe_id = employe_id)
		except Exception as e:
			return []

	@staticmethod
	def toDeleteMobilite(id):
		try:
			mobilite = Model_Mobilite.objects.get(pk = id)
			mobilite.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toCountMobiliteByCategorie():
		ListeMobilite = {"A": 0, "B_devenu_A": 0, "B_devenu_A": 0, "C_devenu_B": 0, "D_devenu_C": 0, "E_devenu_D": 0, "F_devenu_E": 0, "F_devenu_E": 0, "E": 0}
		NbrA = 0
		NbrBA = 0
		NbrCB = 0
		NbrDC = 0
		NbrED = 0
		NbrFE = 0
		NbrE = 0
		try:
			Liste_Employe = Model_Employe.objects.all()
			#print('**Listes employe ** %s' %Liste_Employe)
			for item in Liste_Employe:
				NbrA += Model_Mobilite.objects.filter(categorie_socia_pro_precedent__isnull =True, categorie_socio_professionnelle = 'A', employe_id =item.id).count()
				if NbrA != 0 :
					ListeMobilite["A"] = NbrA
				else:
					pass
				NbrBA += Model_Mobilite.objects.filter(categorie_socia_pro_precedent = 'B', categorie_socio_professionnelle = 'A', employe_id =item.id).count()
				if NbrBA != 0 :
					ListeMobilite["B_devenu_A"] = NbrBA
				else:
					pass

				NbrCB += Model_Mobilite.objects.filter(categorie_socia_pro_precedent = 'C', categorie_socio_professionnelle = 'B', employe_id =item.id).count()
				if NbrCB != 0 :
					ListeMobilite["C_devenu_B"] = NbrCB
				else:
					pass

				NbrDC += Model_Mobilite.objects.filter(categorie_socia_pro_precedent = 'D', categorie_socio_professionnelle = 'C', employe_id =item.id).count()
				if NbrDC != 0 :
					ListeMobilite["D_devenu_C"] = NbrDC
				else:
					pass

				NbrED += Model_Mobilite.objects.filter(categorie_socia_pro_precedent = 'E', categorie_socio_professionnelle = 'D', employe_id =item.id).count()
				if NbrED != 0 :
					ListeMobilite["E_devenu_D"] = NbrED
				else:
					pass

				NbrFE += Model_Mobilite.objects.filter(categorie_socia_pro_precedent = 'F', categorie_socio_professionnelle = 'E', employe_id =item.id).count()
				if NbrFE != 0 :
					ListeMobilite["F_devenu_E"] = NbrFE
				else:
					pass

				NbrE += Model_Mobilite.objects.filter(categorie_socia_pro_precedent__isnull =True, categorie_socio_professionnelle = 'E', employe_id =item.id).count()
				if NbrE != 0 :
					ListeMobilite["E"] = NbrE
				else:
					pass

			# #print('**La liste de Mobilite par categorie** %s' %ListeMobilite)
			return ListeMobilite
		except Exception as e:
			#print(e)
			return ListeMobilite


	@staticmethod
	def toCount_Agent_by_Mobilite_year():
		Year = timezone.now().year
		Liste_Employe = Model_Employe.objects.all()
		somme_year = 0
		List_year = {}
		try:
			i = 2010
			while i <= Year:
				for item in Liste_Employe:
					somme_year += Model_Mobilite.objects.filter(categorie_socia_pro_precedent__isnull = False, date_entree__year = i, employe_id =item.id).count()
				List_year[i] = 	somme_year
				somme_year = 0
				i = i + 1

			# #print('**La liste de Mobilite par year** %s' %List_year)
			return List_year
		except Exception as e:
			#print('**Erreur Count Liste Mobilite par year** %s' %List_year)
			#print(e)
			return List_year

	@staticmethod
	def toGet_Part_Recru_by_Mobilite():
		Year = timezone.now().year
		Liste_Employe = Model_Employe.objects.all()
		Total_Mobilite = 0
		somme_year = 0
		List_Part = {}
		Nombre_Part = []
		List_Mobilite_Tot={}
		try:
			i = 2010
			while i <= Year:
				for item in Liste_Employe:
					somme_year += Model_Mobilite.objects.filter(categorie_socia_pro_precedent__isnull = False, date_entree__year = i, employe_id =item.id).count()
					Total_Mobilite += Model_Mobilite.objects.filter(date_entree__year = i, employe_id =item.id).count()
				List_Mobilite_Tot[i] =  Total_Mobilite
				if somme_year != 0:
					List_Part[i] = 	(100 * somme_year) / Total_Mobilite
				else:
					List_Part[i] = 0
				Nombre_Part.append(somme_year)
				somme_year = 0
				i = i + 1

			# #print('**Part de Recru Mobilite par year** %s' %List_Part)
			# #print('**Total Mobilite par year** %s' %List_Mobilite_Tot)
			# #print('**Nombre de recrutement via Mobilité interne %s' %Nombre_Part)
			return List_Part, Nombre_Part
		except Exception as e:
			#print('**Erreur Part de Recru Mobilite par year** %s' %List_Part)
			#print(e)
			return List_Part, Nombre_Part

	@staticmethod
	def toMouvement_Personnel():
		Year = timezone.now().year
		Liste_Employe = Model_Employe.objects.all()
		Total_Mouvement = 0
		somme_year = 0
		Mouvement_Perso = {}
		try:
			i = 2010
			while i <= Year:
				for item in Liste_Employe:
					somme_year += Model_Mobilite.objects.filter(categorie_socia_pro_precedent__isnull = True, date_entree__year = i, employe_id =item.id).count()
					Total_Mouvement += Model_Mobilite.objects.filter(date_entree__year = i, employe_id =item.id).count()
				if somme_year != 0:
					Mouvement_Perso[i] = 	(100 * somme_year) / Total_Mouvement
				else:
					Mouvement_Perso[i] = 0
				somme_year = 0
				i = i + 1

			# #print('**Mouvement Personnel par year** %s' %Mouvement_Perso)
			return Mouvement_Perso
		except Exception as e:
			#print('**Erreur Mouvement Personnel par year** %s' %Mouvement_Perso)
			#print(e)
			return Mouvement_Perso


	@staticmethod
	def taux_Mobilite_interne():
		Year = timezone.now().year
		somme_year = 0
		Taux_Mobilite = {}
		count_recru = 0
		Nombre_Recru = []
		try:
			i = 2010
			while i <= Year:
				somme_year += Model_Mobilite.objects.filter(date_entree__year = i).count()
				count_recru += Model_Mobilite.objects.filter(date_entree__year = i,categorie_socia_pro_precedent__isnull = True).count()

				Nombre_Recru.append(count_recru)
				Taux_Mobilite[i] = somme_year

				somme_year = 0
				count_recru = 0
				i = i + 1

			# #print('**Taux de Mobilite par year** %s' %Taux_Mobilite)
			# #print('**Nombre de recrutement** %s' %Nombre_Recru)
			return Taux_Mobilite, Nombre_Recru
		except Exception as e:
			#print('**Erreur Taux de Mobilite par year** %s' %Taux_Mobilite)
			#print(e)
			return Taux_Mobilite, Nombre_Recru









