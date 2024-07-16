from __future__ import unicode_literals
from ErpBackOffice.models import Model_Ordre_paie
from django.utils import timezone


class dao_ordre_paie(object):
	id = 0
	numero_ordre_paie=''
	date_paie='2010-01-01'
	montant_global=0.0
	preuve=''
	creation_date=None
	is_accepted =False
	is_validate=False
	compte_id=0
	auteur_id=0

	@staticmethod
	def toListOrdrePaie():
		return Model_Ordre_paie.objects.all().order_by('-id')

	@staticmethod
	def toCreateOrdrePaie(numero_ordre_paie,date_paie,is_validate,is_accepted,montant_global,preuve,compte_id=0):
		try:
			ordre_paie = dao_ordre_paie()
			ordre_paie.numero_ordre_paie = numero_ordre_paie
			ordre_paie.date_paie = date_paie
			ordre_paie.is_validate = is_validate
			ordre_paie.is_accepted = is_accepted
			ordre_paie.montant_global = montant_global
			ordre_paie.preuve = preuve
			if compte_id != 0:
				ordre_paie.compte_id = compte_id
			return ordre_paie
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA ORDRE_PAIE')
			#print(e)
			return None

	@staticmethod
	def toSaveOrdrePaie(auteur,objet_dao_Ordre_paie):
		try:
			ordre_paie  = Model_Ordre_paie()
			ordre_paie.numero_ordre_paie =objet_dao_Ordre_paie.numero_ordre_paie
			ordre_paie.date_paie =objet_dao_Ordre_paie.date_paie
			ordre_paie.is_validate =objet_dao_Ordre_paie.is_validate
			ordre_paie.is_accepted =objet_dao_Ordre_paie.is_accepted
			ordre_paie.montant_global =objet_dao_Ordre_paie.montant_global
			ordre_paie.preuve =objet_dao_Ordre_paie.preuve
			ordre_paie.compte_id = objet_dao_Ordre_paie.compte_id
			ordre_paie.creation_date = timezone.now()
			ordre_paie.auteur_id = auteur.id
			ordre_paie.save()
			return ordre_paie
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA ORDRE_PAIE')
			#print(e)
			return None

	@staticmethod
	def toUpdateOrdrePaie(id, objet_dao_Ordre_paie):
		try:
			ordre_paie = Model_Ordre_paie.objects.get(pk = id)
			ordre_paie.numero_ordre_paie =objet_dao_Ordre_paie.numero_ordre_paie
			ordre_paie.date_paie =objet_dao_Ordre_paie.date_paie
			ordre_paie.is_validate =objet_dao_Ordre_paie.is_validate
			ordre_paie.is_accepted =objet_dao_Ordre_paie.is_accepted
			ordre_paie.montant_global =objet_dao_Ordre_paie.montant_global
			ordre_paie.compte_id = objet_dao_Ordre_paie.compte_id
			ordre_paie.preuve =objet_dao_Ordre_paie.preuve
			ordre_paie.save()
			return ordre_paie
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA ORDRE_PAIE')
			#print(e)
			return None
	@staticmethod
	def toGetOrdrePaie(id):
		try:
			return Model_Ordre_paie.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteOrdrePaie(id):
		try:
			ordre_paie = Model_Ordre_paie.objects.get(pk = id)
			ordre_paie.delete()
			return True
		except Exception as e:
			return False