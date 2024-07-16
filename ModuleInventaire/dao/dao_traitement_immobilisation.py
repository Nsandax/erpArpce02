from __future__ import unicode_literals
from ErpBackOffice.models import Model_TraitementImmobilisation
from django.utils import timezone

class dao_traitement_immobilisation(object):
	id = 0
	numero_traitement = ''
	rapport_inventaire_id = None
	description = ''
	typeTraitement = 1

	@staticmethod
	def toListTraitement_immobilisation():
		return Model_TraitementImmobilisation.objects.all().order_by('-id')

	@staticmethod
	def toCreateTraitement_immobilisation(numero_traitement,description, typeTraitement, rapport_inventaire_id = None):
		try:
			traitement_immobilisation = dao_traitement_immobilisation()
			traitement_immobilisation.numero_traitement = numero_traitement
			traitement_immobilisation.rapport_inventaire_id = rapport_inventaire_id
			traitement_immobilisation.description = description
			traitement_immobilisation.typeTraitement = typeTraitement
			return traitement_immobilisation
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA TRAITEMENT_IMMOBILISATION')
			#print(e)
			return None

	@staticmethod
	def toSaveTraitement_immobilisation(auteur, objet_dao_Traitement_immobilisation):
		try:
			traitement_immobilisation  = Model_TraitementImmobilisation()
			traitement_immobilisation.numero_traitement = objet_dao_Traitement_immobilisation.numero_traitement
			traitement_immobilisation.rapport_inventaire_id = objet_dao_Traitement_immobilisation.rapport_inventaire_id
			traitement_immobilisation.description = objet_dao_Traitement_immobilisation.description
			traitement_immobilisation.created_at = timezone.now()
			traitement_immobilisation.updated_at = timezone.now()
			traitement_immobilisation.auteur_id = auteur.id
			traitement_immobilisation.type_traitement = objet_dao_Traitement_immobilisation.typeTraitement

			traitement_immobilisation.save()
			return traitement_immobilisation
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA TRAITEMENT_IMMOBILISATION')
			#print(e)
			return None

	@staticmethod
	def toUpdateTraitement_immobilisation(id, objet_dao_Traitement_immobilisation):
		try:
			traitement_immobilisation = Model_TraitementImmobilisation.objects.get(pk = id)
			traitement_immobilisation.numero_traitement =objet_dao_Traitement_immobilisation.numero_traitement
			traitement_immobilisation.rapport_inventaire_id =objet_dao_Traitement_immobilisation.rapport_inventaire_id
			traitement_immobilisation.description =objet_dao_Traitement_immobilisation.description
			traitement_immobilisation.type_traitement = objet_dao_Traitement_immobilisation.typeTraitement
			traitement_immobilisation.updated_at = timezone.now()
			traitement_immobilisation.save()
			return traitement_immobilisation
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA TRAITEMENT_IMMOBILISATION')
			#print(e)
			return None
	@staticmethod
	def toGetTraitement_immobilisation(id):
		try:
			return Model_TraitementImmobilisation.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTraitement_immobilisation(id):
		try:
			traitement_immobilisation = Model_TraitementImmobilisation.objects.get(pk = id)
			traitement_immobilisation.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGenerateNumeroTraitement_immo():
		total_traitement_immo = dao_traitement_immobilisation.toListTraitement_immobilisation().count()
		total_traitement_immo = total_traitement_immo + 1
		temp_numero = str(total_traitement_immo)

		for i in range(len(str(total_traitement_immo)), 4):
			temp_numero = "0" + temp_numero

		mois = timezone.now().month
		if mois < 10: mois = "0%s" % mois

		temp_numero = "TRAIT-IMMO%s%s%s" % (timezone.now().year, mois, temp_numero)
		return temp_numero