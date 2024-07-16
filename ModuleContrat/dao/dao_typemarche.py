from __future__ import unicode_literals
from ErpBackOffice.dao.dao_devise import dao_devise
from ErpBackOffice.models import Model_TypeMarche
from ErpBackOffice.models import Model_Demande_cotation
from ErpBackOffice.models import Model_Lettre_commande
from ErpBackOffice.models import Model_Avis_appel_offre
from ModuleAchat.dao.dao_demande_achat import dao_demande_achat
from ModuleContrat.dao.dao_contrat import dao_contrat
from ModuleContrat.dao.dao_demande_cotation import dao_demande_cotation
from ModuleContrat.dao.dao_lettre_commande import dao_lettre_commande
from ModuleContrat.dao.dao_avis_appel_offre import dao_avis_appel_offre

from django.utils import timezone

class dao_typemarche(object):
	id = 0
	designation = ''
	code = ''
	description = ''

	@staticmethod
	def toListTypemarche():
		return Model_TypeMarche.objects.all()

	@staticmethod
	def toCreateTypemarche(designation,code,description):
		try:
			typemarche = dao_typemarche()
			typemarche.designation = designation
			typemarche.code = code
			typemarche.description = description
			return typemarche
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TYPEMARCHE')
			#print(e)
			return None

	@staticmethod
	def toSaveTypemarche(auteur, objet_dao_Typemarche):
		try:
			typemarche  = Model_TypeMarche()
			typemarche.designation = objet_dao_Typemarche.designation
			typemarche.code = objet_dao_Typemarche.code
			typemarche.description = objet_dao_Typemarche.description
			typemarche.created_at = timezone.now()
			typemarche.updated_at = timezone.now()
			typemarche.auteur_id = auteur.id

			typemarche.save()
			return typemarche
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TYPEMARCHE')
			#print(e)
			return None

	@staticmethod
	def toUpdateTypemarche(id, objet_dao_Typemarche):
		try:
			typemarche = Model_TypeMarche.objects.get(pk = id)
			typemarche.designation =objet_dao_Typemarche.designation
			typemarche.code =objet_dao_Typemarche.code
			typemarche.description =objet_dao_Typemarche.description
			typemarche.updated_at = timezone.now()
			typemarche.save()
			return typemarche
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TYPEMARCHE')
			#print(e)
			return None
	@staticmethod
	def toGetTypemarche(id):
		try:
			return Model_TypeMarche.objects.get(pk = id)
		except Exception as e:
			print("toGetTypemarche", e)
			return None
	@staticmethod
	def toDeleteTypemarche(id):
		try:
			typemarche = Model_TypeMarche.objects.get(pk = id)
			typemarche.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def torefallitems(id):
		try:
			type = dao_typemarche.toGetTypemarche(id)
			list_cotation = Model_Demande_cotation.objects.filter(type_marche_id = type.id)
			list_commande = Model_Lettre_commande.objects.filter(type_marche_id = type.id)
			print('Cotation',list_cotation)
			print('commande',list_commande)
			return list_cotation, list_commande
		except Exception as e:
			return None, None