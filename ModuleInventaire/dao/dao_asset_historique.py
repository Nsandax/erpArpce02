from __future__ import unicode_literals
from ErpBackOffice.models import Model_AssetHistorique
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class dao_asset_historique(object):
	id = 0
	reference = ""
	document = ""
	est_initial = False
	asset_id = None
	employe_id = None
	content_type_id = None
	bon_id = None




	@staticmethod
	def toListAssetHistorique():
		return Model_AssetHistorique.objects.all().order_by('-id')

	@staticmethod
	def toListHistorique(asset_id):
		return Model_AssetHistorique.objects.filter(asset_id = asset_id)

	@staticmethod
	def toCreateAssetHistorique(reference,document,asset_id,objet_bon,employe_id=None,est_initial=False):
		try:
			content_type = ContentType.objects.get_for_model(objet_bon)
			asset_historique = dao_asset_historique()
			asset_historique.reference = reference
			asset_historique.document = document
			asset_historique.asset_id = asset_id
			asset_historique.employe_id = employe_id
			asset_historique.content_type_id = content_type.id
			asset_historique.est_initial = est_initial
			return asset_historique
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE HISTORIQUE ASSET')
			#print(e)
			return None

	@staticmethod
	def toSaveAssetHistorique(auteur, objet_dao_asset_historique):
		try:
			asset_historique  = Model_AssetHistorique()
			asset_historique.reference = objet_dao_asset_historique.reference
			asset_historique.document = objet_dao_asset_historique.document
			asset_historique.asset_id = objet_dao_asset_historique.asset_id
			asset_historique.employe_id = objet_dao_asset_historique.employe_id
			asset_historique.content_type_id = objet_dao_asset_historique.content_type_id
			asset_historique.est_initial = objet_dao_asset_historique.est_initial
			asset_historique.created_at = timezone.now()
			asset_historique.updated_at = timezone.now()
			asset_historique.auteur_id = auteur.id

			asset_historique.save()
			return asset_historique
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA HISTORIQUE ASSET')
			#print(e)
			return None

	@staticmethod
	def toUpdateAssetHistorique(id, objet_dao_asset_historique):
		try:
			asset_historique = Model_AssetHistorique.objects.get(pk = id)
			asset_historique.reference = objet_dao_asset_historique.reference
			asset_historique.document = objet_dao_asset_historique.document
			asset_historique.asset_id = objet_dao_asset_historique.asset_id
			asset_historique.employe_id = objet_dao_asset_historique.employe_id
			asset_historique.content_type_id = objet_dao_asset_historique.content_type_id
			asset_historique.est_initial = objet_dao_asset_historique.est_initial
			asset_historique.updated_at = timezone.now()

			asset_historique.save()
			return asset_historique
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA HISTORIQUE ASSET')
			#print(e)
			return None



	@staticmethod
	def toDeleteAssetHistorique(id):
		try:
			asset_historique = Model_AssetHistorique.objects.get(pk = id)
			asset_historique.delete()
			return True
		except Exception as e:
			return False