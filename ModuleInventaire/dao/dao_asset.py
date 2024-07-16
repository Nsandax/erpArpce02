from __future__ import unicode_literals
from ErpBackOffice.models import Model_Asset
from django.utils import timezone
from ModuleComptabilite.dao.dao_annee_fiscale import dao_annee_fiscale

class dao_asset(object):
	id = 0
	numero_identification = ''
	type=''
	article_id = None
	employe_id = None
	emplacement_id = None
	bon_transfert = None
	description = ""

	@staticmethod
	def toListAsset():
		return Model_Asset.objects.all().order_by('-created_at')

	@staticmethod
	def toListAssetNonImmobilise():
		annee = dao_annee_fiscale.toGetAnneeFiscaleActive()
		#print("annee sksdjs", annee.seuil_immobilisation)
		return Model_Asset.objects.filter(est_immobilise = False).filter(article__est_amortissable = True).filter(article__prix_unitaire__gte = annee.seuil_immobilisation)



	@staticmethod
	def toCreateAsset(numero_identification,type,article_id,employe_id,emplacement_id, description):
		try:
			asset = dao_asset()
			asset.numero_identification = numero_identification
			asset.type = type
			asset.article_id = article_id
			asset.employe_id = employe_id
			asset.emplacement_id = emplacement_id
			asset.description = description
			return asset
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA IMMOBILIER')
			#print(e)
			return None

	@staticmethod
	def toSaveAsset(auteur, objet_dao_asset):
		try:
			asset  = Model_Asset()
			asset.numero_identification = objet_dao_asset.numero_identification
			asset.type = objet_dao_asset.type
			asset.article_id = objet_dao_asset.article_id
			asset.employe_id = objet_dao_asset.employe_id
			asset.emplacement_id = objet_dao_asset.emplacement_id
			asset.description = objet_dao_asset.description
			asset.created_at = timezone.now()
			asset.updated_at = timezone.now()
			asset.auteur_id = auteur.id

			asset.save()
			return asset
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA IMMOBILIER')
			#print(e)
			return None

	@staticmethod
	def toUpdateAsset(id, objet_dao_asset):
		try:
			asset = Model_Asset.objects.get(pk = id)
			asset.numero_identification =objet_dao_asset.numero_identification
			asset.type = objet_dao_asset.type
			asset.article_id =objet_dao_asset.article_id
			asset.employe_id =objet_dao_asset.employe_id
			asset.description = objet_dao_asset.description
			asset.emplacement_id =objet_dao_asset.emplacement_id
			asset.bon_transfert_id = objet_dao_asset.bon_transfert_id
			asset.updated_at = timezone.now()
			asset.save()
			return asset
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA IMMOBILIER')
			#print(e)
			return None

	@staticmethod
	def toUpdateAssetAffectation(id, employe_id, emplacement_id = None):
		try:
			asset = Model_Asset.objects.get(pk = id)
			asset.employe_id =employe_id
			asset.emplacement_id = emplacement_id
			asset.updated_at = timezone.now()
			asset.save()
			return asset
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA IMMOBILIER')
			#print(e)
			return None
	@staticmethod
	def toGetAsset(id):
		try:
			return Model_Asset.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetAssetByEmplacement(id):
		try:
			return Model_Asset.objects.filter(emplacement_id = id).order_by('-created_at')
		except Exception as e:
			return None


	@staticmethod
	def toGetAssetByArticle(id):
		try:
			return Model_Asset.objects.filter(article_id = id).filter(employe_id = None)
		except Exception as e:
			return None

	@staticmethod
	def toGetAssetByArticleOfEmplacement(id, emplacement_id):
		try:
			return Model_Asset.objects.filter(article_id = id).filter(employe_id = None).filter(emplacement_id =emplacement_id).filter(est_immobilise = False)
		except Exception as e:
			return None


	@staticmethod
	def toDeleteAsset(id):
		try:
			asset = Model_Asset.objects.get(pk = id)
			asset.delete()
			return True
		except Exception as e:
			return False