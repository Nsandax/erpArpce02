from __future__ import unicode_literals
from ErpBackOffice.models import Model_StockArticle
from django.utils import timezone

class dao_stock_article(object):
	id = 0
	quantite_disponible=0
	emplacement_id = 0
	article_id = 0
	auteur_id = 0


	@staticmethod
	def toListStockArticle():
		return Model_StockArticle.objects.all().order_by('-id')

	@staticmethod
	def toCreateStockArticle(quantite_disponible, emplacement_id=None, article_id=None):
		try:
			stock_article = dao_stock_article()
			stock_article.quantite_disponible = quantite_disponible
			stock_article.emplacement_id = emplacement_id
			stock_article.article_id = article_id
			return stock_article
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA STOCK_ARTICLE')
			#print(e)
			return None

	@staticmethod
	def toSaveStockArticle(auteur,objet_dao_Stock_article):
		try:
			stock_article  = Model_StockArticle()
			stock_article.quantite_disponible =objet_dao_Stock_article.quantite_disponible
			stock_article.emplacement_id = objet_dao_Stock_article.emplacement_id
			stock_article.article_id = objet_dao_Stock_article.article_id
			stock_article.creation_date = timezone.now()
			stock_article.auteur_id = auteur.id
			stock_article.save()
			return stock_article
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA STOCK_ARTICLE')
			#print(e)
			return None

	@staticmethod
	def toUpdateStockArticle(id, objet_dao_Stock_article):
		try:
			stock_article = Model_StockArticle.objects.get(pk = id)
			stock_article.quantite_disponible =objet_dao_Stock_article.quantite_disponible
			stock_article.emplacement_id = objet_dao_Stock_article.emplacement_id
			stock_article.article_id = objet_dao_Stock_article.article_id
			stock_article.save()
			return stock_article
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA STOCK_ARTICLE')
			#print(e)
			return None
	@staticmethod
	def toGetStockArticle(id):
		try:
			return Model_StockArticle.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteStockArticle(id):
		try:
			stock_article = Model_StockArticle.objects.get(pk = id)
			stock_article.delete()
			return True
		except Exception as e:
			return False

	@staticmethod
	def toListStocksInEmplacement(emplacement_id):
		try:
			return Model_StockArticle.objects.filter(emplacement_id = emplacement_id)
		except Exception as e:
		    return None


	@staticmethod
	def toListStocksOfArticleInEmplacement(article_id, emplacement_id):
	    try:
	        return Model_StockArticle.objects.filter(article_id = article_id).filter(emplacement_id = emplacement_id)
	    except Exception as e:
	        return None

	@staticmethod
	def toGetQuantiteStockOfEmplacement(article, id_emplacement):
		try:
			#print("ARRIVED ICI")
			if article.est_service: return "INFINIE"
			#print("Article Id", article.id)
			quantite_stock = 0
			#print(id_emplacement)
			if id_emplacement != 0:
				#print("2")
				stocks = Model_StockArticle.objects.filter(article_id = article.id).filter(emplacement_id = id_emplacement)
				#print("Stock", stocks)
				for stock in stocks :
					#print("4")
					quantite_stock = quantite_stock + stock.quantite_disponible
			return quantite_stock
		except Exception as e:
			return None

