from __future__ import unicode_literals
from ErpBackOffice.models import Model_Unite_fonctionnelle
from django.utils import timezone


class dao_unite_fonctionnelle(object):
	id = 0
	libelle=''
	description=''
	niveau=0
	creation_date = None
	type=''
	est_racine = False
	unite_fonctionnelle_id = None
	type_unite_fonctionnelle_id = None
	responsable_id = None
	auteur_id = 0

	@staticmethod
	def toListUniteFonctionnelle():
		return Model_Unite_fonctionnelle.objects.all().order_by('niveau')#.order_by('-id')

	@staticmethod
	def toListUniteFonctionnelleType(type_id):
		return Model_Unite_fonctionnelle.objects.filter(type_unite_fonctionnelle_id = type_id).order_by('-id')

	@staticmethod
	def togetNombreUniteFonctionnelle():
		return Model_Unite_fonctionnelle.objects.all().count()

	@staticmethod
	def toListUniteFonctionnelleWH():
		return Model_Unite_fonctionnelle.objects.exclude(emplacement = None).exclude(emplacement__type_emplacement__designation="INTERNAL").exclude(emplacement__type_emplacement__designation="ENTREPOT")

	@staticmethod
	def toListUniteFonctionnelleWHNoneService():
		return Model_Unite_fonctionnelle.objects.exclude(emplacement = None).exclude(emplacement__type_emplacement__designation="INTERNAL").exclude(emplacement__type_emplacement__designation="ENTREPOT").exclude(libelle= "Ressources Humaines")


	@staticmethod
	def toListServiceHavingWareHouses():
		return Model_Unite_fonctionnelle.objects.exclude(emplacement = None)

	@staticmethod
	def toCreateUniteFonctionnelle(libelle,est_racine,description,niveau,type,unite_fonctionnelle_id=None,responsable_id=None, type_unite_fonctionnelle_id = None, code = None):
		try:
			unite_fonctionnelle = dao_unite_fonctionnelle()
			unite_fonctionnelle.libelle = libelle
			unite_fonctionnelle.est_racine = est_racine
			unite_fonctionnelle.description = description
			unite_fonctionnelle.niveau = niveau
			unite_fonctionnelle.type = type
			unite_fonctionnelle.unite_fonctionnelle_id = unite_fonctionnelle_id
			unite_fonctionnelle.type_unite_fonctionnelle_id = type_unite_fonctionnelle_id
			unite_fonctionnelle.responsable_id = responsable_id
			unite_fonctionnelle.code = code
			return unite_fonctionnelle
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA UNITE_FONCTIONNELLE')
			#print(e)
			return None

	@staticmethod
	def toSaveUniteFonctionnelle(auteur,objet_dao_Unite_fonctionnelle):
		try:
			unite_fonctionnelle  = Model_Unite_fonctionnelle()
			unite_fonctionnelle.libelle =objet_dao_Unite_fonctionnelle.libelle
			unite_fonctionnelle.est_racine =objet_dao_Unite_fonctionnelle.est_racine
			unite_fonctionnelle.description =objet_dao_Unite_fonctionnelle.description
			unite_fonctionnelle.niveau =objet_dao_Unite_fonctionnelle.niveau
			unite_fonctionnelle.type =objet_dao_Unite_fonctionnelle.type
			unite_fonctionnelle.unite_fonctionnelle_id = objet_dao_Unite_fonctionnelle.unite_fonctionnelle_id
			unite_fonctionnelle.type_unite_fonctionnelle_id = objet_dao_Unite_fonctionnelle.type_unite_fonctionnelle_id
			unite_fonctionnelle.responsable_id = objet_dao_Unite_fonctionnelle.responsable_id
			unite_fonctionnelle.code = objet_dao_Unite_fonctionnelle.code
			unite_fonctionnelle.auteur_id=auteur.id
			unite_fonctionnelle.creation_date = timezone.now()
			unite_fonctionnelle.save()
			return unite_fonctionnelle
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA UNITE_FONCTIONNELLE')
			#print(e)
			return None

	@staticmethod
	def toUpdateUniteFonctionnelle(id, objet_dao_Unite_fonctionnelle):
		try:
			unite_fonctionnelle = Model_Unite_fonctionnelle.objects.get(pk = id)
			unite_fonctionnelle.libelle =objet_dao_Unite_fonctionnelle.libelle
			unite_fonctionnelle.est_racine =objet_dao_Unite_fonctionnelle.est_racine
			unite_fonctionnelle.description =objet_dao_Unite_fonctionnelle.description
			unite_fonctionnelle.niveau =objet_dao_Unite_fonctionnelle.niveau
			unite_fonctionnelle.type =objet_dao_Unite_fonctionnelle.type
			unite_fonctionnelle.type_unite_fonctionnelle_id = objet_dao_Unite_fonctionnelle.type_unite_fonctionnelle_id
			unite_fonctionnelle.unite_fonctionnelle_id = objet_dao_Unite_fonctionnelle.unite_fonctionnelle_id
			unite_fonctionnelle.responsable_id = objet_dao_Unite_fonctionnelle.responsable_id
			unite_fonctionnelle.code = objet_dao_Unite_fonctionnelle.code
			unite_fonctionnelle.save()
			return True
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA UNITE_FONCTIONNELLE')
			#print(e)
			return False
	@staticmethod
	def toGetUniteFonctionnelle(id):
		try:
			return Model_Unite_fonctionnelle.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toListOfOneUniteFonctionnelle(id):
		try:
			return Model_Unite_fonctionnelle.objects.filter(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetUniteFonctionnelleOfEmplacement(id):
		try:
			return Model_Unite_fonctionnelle.objects.filter(emplacement = id).first()
		except Exception as e:
			return None


	@staticmethod
	def toDeleteUniteFonctionnelle(id):
		try:
			unite_fonctionnelle = Model_Unite_fonctionnelle.objects.get(pk = id)
			unite_fonctionnelle.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toGetOrCreateUniteFonctionnelle(auteur, code):
		try:
			unite_fonctionnelle = Model_Unite_fonctionnelle.objects.filter(code = code).first()
			if not unite_fonctionnelle:
				unite = dao_unite_fonctionnelle()
				unite_fonctionnelle = unite.toCreateUniteFonctionnelle("",False,"",1,"",None, None, None, code)
				unite_fonctionnelle = unite.toSaveUniteFonctionnelle(auteur, unite_fonctionnelle)
			return unite_fonctionnelle
		except Exception as e:
			#print("Error toGetOrCreateUniteFonctionnelle", e)
			return None