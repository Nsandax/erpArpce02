from __future__ import unicode_literals
from ErpBackOffice.models import Model_Projet_professionnel
from django.utils import timezone

class dao_projet_professionnel(object):
	id = 0
	projet = ''
	employe_id = None
	numero_projet = ''

	@staticmethod
	def toListProjet_professionnel():
		return Model_Projet_professionnel.objects.all().order_by('-id')

	@staticmethod
	def toListProjet_professionnelByAuteur(user_id):
		return Model_Projet_professionnel.objects.filter(auteur_id=user_id)

	@staticmethod
	def toListProjet_professionnelByEmploye(employe_id):
		return Model_Projet_professionnel.objects.filter(employe_id=employe_id)

	@staticmethod
	def toCreateProjet_professionnel(projet,employe_id,numero_projet):
		try:
			projet_professionnel = dao_projet_professionnel()
			projet_professionnel.projet = projet
			projet_professionnel.employe_id = employe_id
			projet_professionnel.numero_projet = numero_projet
			return projet_professionnel
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PROJET_PROFESSIONNEL')
			#print(e)
			return None

	@staticmethod
	def toSaveProjet_professionnel(auteur, objet_dao_Projet_professionnel):
		try:
			projet_professionnel  = Model_Projet_professionnel()
			projet_professionnel.projet = objet_dao_Projet_professionnel.projet
			projet_professionnel.employe = objet_dao_Projet_professionnel.employe_id
			projet_professionnel.numero_projet = objet_dao_Projet_professionnel.numero_projet
			projet_professionnel.created_at = timezone.now()
			projet_professionnel.updated_at = timezone.now()
			projet_professionnel.auteur_id = auteur.id

			projet_professionnel.save()
			return projet_professionnel
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PROJET_PROFESSIONNEL')
			#print(e)
			return None

	@staticmethod
	def toUpdateProjet_professionnel(id, objet_dao_Projet_professionnel):
		try:
			projet_professionnel = Model_Projet_professionnel.objects.get(pk = id)
			projet_professionnel.projet =objet_dao_Projet_professionnel.projet
			projet_professionnel.employe =objet_dao_Projet_professionnel.employe_id
			projet_professionnel.numero_projet =objet_dao_Projet_professionnel.numero_projet
			projet_professionnel.updated_at = timezone.now()
			projet_professionnel.save()
			return projet_professionnel
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PROJET_PROFESSIONNEL')
			#print(e)
			return None
	@staticmethod
	def toGetProjet_professionnel(id):
		try:
			return Model_Projet_professionnel.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteProjet_professionnel(id):
		try:
			projet_professionnel = Model_Projet_professionnel.objects.get(pk = id)
			projet_professionnel.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateProjetProfessionel():
		total_receptions = dao_projet_professionnel.toListProjet_professionnel().count()
		total_receptions = total_receptions + 1
		temp_numero = str(total_receptions)

		for i in range(len(str(total_receptions)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "PROJ-%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero