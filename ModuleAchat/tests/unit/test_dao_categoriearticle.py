# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_categorie_article import dao_categorie_article
from ErpBackOffice.models import Model_Categorie
from ErpBackOffice.models import Model_Personne

class Test_DaoCategorieArticle (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_Categorie pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Categorie.objects.create(designation="Achetable")
		Model_Categorie.objects.create(designation="Stockable")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveCategorieArticle(self):
		pprint ('test_CreateCategorieArticle')
		#A Configurer
		objet = dao_Categorie_article.toCreateCategorieArticle()
		self.assertIsInstance(dao_Categorie_article.toSaveCategorieArticle(self.auteur,objet),Model_Categorie)
		pprint('SUCCES')

	def test_UpdateCategorieArticle(self):
		pprint ('test_UpdateCategorieArticle')
		objet = dao_Categorie_article.toCreateCategorieArticle()
		self.assertIsInstance(dao_Categorie_article.toUpdateCategorieArticle(1,objet),Model_Categorie)
		pprint(Model_Categorie.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetCategorieArticle(self):
		pprint ('test_toGetCategorieArticle')
		self.assertIsInstance(dao_Categorie_article.toGetCategorieArticle(1),Model_Categorie)
		pprint('SUCCES')

	def test_toGetListCategorieArticle(self):
		pprint ('test_toGetListCategorieArticle')
		self.assertIn(dao_Categorie_article.toGetCategorieArticle(1),dao_Categorie_article.toListCategorieArticle())
		pprint('SUCCES')
	def test_toDeleteCategorieArticle(self):
		pprint ('test_toDeleteCategorieArticle')
		self.assertTrue(dao_Categorie_article.toDeleteCategorieArticle(1))
		pprint('SUCCES')
