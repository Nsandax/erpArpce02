# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_unite_achat_article import dao_unite_achat_article
from ErpBackOffice.models import Model_UniteAchatArticle
from ErpBackOffice.models import Model_Article
from ErpBackOffice.models import Model_Unite
from ErpBackOffice.models import Model_Personne

class Test_DaoUniteAchatArticle (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_UniteAchatArticle pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Unite.objects.create(designation="DOLL")
		Model_Article.objects.create(designation="Stylo")
		Model_Article.objects.create(designation="Crayon")
		Model_UniteAchatArticle.objects.create(article_id=1,unite_id=1)
		Model_UniteAchatArticle.objects.create(article_id=2,unite_id=1)

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveUniteAchatArticle(self):
		pprint ('test_CreateUniteAchatArticle')
		#A Configurer
		objet = dao_Unite_achat_article.toCreateUniteAchatArticle()
		self.assertIsInstance(dao_Unite_achat_article.toSaveUniteAchatArticle(self.auteur,objet),Model_UniteAchatArticle)
		pprint('SUCCES')

	def test_UpdateUniteAchatArticle(self):
		pprint ('test_UpdateUniteAchatArticle')
		objet = dao_Unite_achat_article.toCreateUniteAchatArticle()
		self.assertIsInstance(dao_Unite_achat_article.toUpdateUniteAchatArticle(1,objet),Model_UniteAchatArticle)
		pprint(Model_UniteAchatArticle.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetUniteAchatArticle(self):
		pprint ('test_toGetUniteAchatArticle')
		self.assertIsInstance(dao_Unite_achat_article.toGetUniteAchatArticle(1),Model_UniteAchatArticle)
		pprint('SUCCES')

	def test_toGetListUniteAchatArticle(self):
		pprint ('test_toGetListUniteAchatArticle')
		self.assertIn(dao_Unite_achat_article.toGetUniteAchatArticle(1),dao_Unite_achat_article.toListUniteAchatArticle())
		pprint('SUCCES')
	def test_toDeleteUniteAchatArticle(self):
		pprint ('test_toDeleteUniteAchatArticle')
		self.assertTrue(dao_Unite_achat_article.toDeleteUniteAchatArticle(1))
		pprint('SUCCES')
