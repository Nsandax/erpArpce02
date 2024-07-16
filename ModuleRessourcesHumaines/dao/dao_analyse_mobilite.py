from __future__ import unicode_literals
from ErpBackOffice.models import Model_Mobilite
from django.utils import timezone
from ErpBackOffice.models import Model_Employe
from django.db.models import Count
import numpy as np
from django.template.defaulttags import register
from django import template

register = template.Library()


class dao_analyse_mobilite(object):

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


	@staticmethod
	def toGet_Nombre_recrutement_mobilite():
		Year = timezone.now().year
		somme = 0
		Total_recru_monilite = {}
		try:
			i = 2010
			while i <= Year:
				somme += Model_Mobilite.objects.filter(employe__date_entree__year = i, type_mobilite ='Recrutement Interne').count()

				Total_recru_monilite[i] = somme

				somme = 0
				i = i + 1
			# #print('**DAO MOBILITE Recrutement par Mobilite ** %s' %Total_recru_monilite)
			return Total_recru_monilite
		except Exception as e:
			#print('**ERREUR DAO MOBILITE Recrutement par Mobilite** %s' %Total_recru_monilite)
			#print(e)
			return Total_recru_monilite


	@staticmethod
	def toGet_Nombre_recrutement_Total():
		Year = timezone.now().year
		somme = 0
		Total_Number = {}
		try:
			i = 2010
			while i <= Year:
				somme += Model_Employe.objects.filter(profilrh__date_engagement__year = i).count()

				Total_Number[i] = somme

				somme = 0
				i = i + 1
			# #print('**DAO MOBILITE Recrutement Total ** %s' %Total_Number)
			return Total_Number
		except Exception as e:
			#print('**ERREUR DAO MOBILITE Recrutement Total** %s' %Total_Number)
			#print(e)
			return Total_Number,






