# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_stock_article import dao_stock_article
from ErpBackOffice.models import Model_StockArticle
from ErpBackOffice.models import Model_Article
from ErpBackOffice.models import Model_Personne

class Test_DaoStockArticle (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_StockArticle pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Article.objects.create(designation="Stylo")
		Model_StockArticle.objects.create(article_id=1,quantite_disponible=10)
		Model_StockArticle.objects.create(article_id=1,quantite_disponible=30)

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveStockArticle(self):
		pprint ('test_CreateStockArticle')
		#A Configurer
		objet = dao_Stock_article.toCreateStockArticle()
		self.assertIsInstance(dao_Stock_article.toSaveStockArticle(self.auteur,objet),Model_StockArticle)
		pprint('SUCCES')

	def test_UpdateStockArticle(self):
		pprint ('test_UpdateStockArticle')
		objet = dao_Stock_article.toCreateStockArticle()
		self.assertIsInstance(dao_Stock_article.toUpdateStockArticle(1,objet),Model_StockArticle)
		pprint(Model_StockArticle.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetStockArticle(self):
		pprint ('test_toGetStockArticle')
		self.assertIsInstance(dao_Stock_article.toGetStockArticle(1),Model_StockArticle)
		pprint('SUCCES')

	def test_toGetListStockArticle(self):
		pprint ('test_toGetListStockArticle')
		self.assertIn(dao_Stock_article.toGetStockArticle(1),dao_Stock_article.toListStockArticle())
		pprint('SUCCES')
	def test_toDeleteStockArticle(self):
		pprint ('test_toDeleteStockArticle')
		self.assertTrue(dao_Stock_article.toDeleteStockArticle(1))
		pprint('SUCCES')
