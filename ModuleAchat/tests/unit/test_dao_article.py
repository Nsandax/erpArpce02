# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_article import dao_article
from ErpBackOffice.models import Model_Article
from ErpBackOffice.models import Model_Personne

class Test_DaoArticle (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_Article pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Article.objects.create(designation="Stylo")
		Model_Article.objects.create(designation="Crayon")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveArticle(self):
		pprint ('test_CreateArticle')
		#A Configurer
		objet = dao_Article.toCreateArticle()
		self.assertIsInstance(dao_Article.toSaveArticle(self.auteur,objet),Model_Article)
		pprint('SUCCES')

	def test_UpdateArticle(self):
		pprint ('test_UpdateArticle')
		objet = dao_Article.toCreateArticle()
		self.assertIsInstance(dao_Article.toUpdateArticle(1,objet),Model_Article)
		pprint(Model_Article.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetArticle(self):
		pprint ('test_toGetArticle')
		self.assertIsInstance(dao_Article.toGetArticle(1),Model_Article)
		pprint('SUCCES')

	def test_toGetListArticle(self):
		pprint ('test_toGetListArticle')
		self.assertIn(dao_Article.toGetArticle(1),dao_Article.toListArticle())
		pprint('SUCCES')
	def test_toDeleteArticle(self):
		pprint ('test_toDeleteArticle')
		self.assertTrue(dao_Article.toDeleteArticle(1))
		pprint('SUCCES')
