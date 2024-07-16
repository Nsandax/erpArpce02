# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_type_article import dao_type_article
from ErpBackOffice.models import Model_TypeArticle
from ErpBackOffice.models import Model_Personne

class Test_DaoTypeArticle (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_TypeArticle pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_TypeArticle.objects.create(nature="Cool")
		Model_TypeArticle.objects.create(nature="Pas cool")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveTypeArticle(self):
		pprint ('test_CreateTypeArticle')
		#A Configurer
		objet = dao_Type_article.toCreateTypeArticle()
		self.assertIsInstance(dao_Type_article.toSaveTypeArticle(self.auteur,objet),Model_TypeArticle)
		pprint('SUCCES')

	def test_UpdateTypeArticle(self):
		pprint ('test_UpdateTypeArticle')
		objet = dao_Type_article.toCreateTypeArticle()
		self.assertIsInstance(dao_Type_article.toUpdateTypeArticle(1,objet),Model_TypeArticle)
		pprint(Model_TypeArticle.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetTypeArticle(self):
		pprint ('test_toGetTypeArticle')
		self.assertIsInstance(dao_Type_article.toGetTypeArticle(1),Model_TypeArticle)
		pprint('SUCCES')

	def test_toGetListTypeArticle(self):
		pprint ('test_toGetListTypeArticle')
		self.assertIn(dao_Type_article.toGetTypeArticle(1),dao_Type_article.toListTypeArticle())
		pprint('SUCCES')
	def test_toDeleteTypeArticle(self):
		pprint ('test_toDeleteTypeArticle')
		self.assertTrue(dao_Type_article.toDeleteTypeArticle(1))
		pprint('SUCCES')
