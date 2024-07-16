# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_fournisseur_article import dao_fournisseur_article
from ErpBackOffice.models import Model_FournisseurArticle
from ErpBackOffice.models import Model_Article
from ErpBackOffice.models import Model_Fournisseur
from ErpBackOffice.models import Model_Personne

class Test_DaoFournisseurArticle (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_FournisseurArticle pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Article.objects.create(designation="Stylo")
		Model_Fournisseur.objects.create(nom_complet="Yoann gourcuff")
		Model_FournisseurArticle.objects.create(article_id=1,fournisseur_id=2,quantite_minimale=10)
		Model_FournisseurArticle.objects.create(article_id=1,fournisseur_id=2,quantite_minimale=20)

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveFournisseurArticle(self):
		pprint ('test_CreateFournisseurArticle')
		#A Configurer
		objet = dao_Fournisseur_article.toCreateFournisseurArticle()
		self.assertIsInstance(dao_Fournisseur_article.toSaveFournisseurArticle(self.auteur,objet),Model_FournisseurArticle)
		pprint('SUCCES')

	def test_UpdateFournisseurArticle(self):
		pprint ('test_UpdateFournisseurArticle')
		objet = dao_Fournisseur_article.toCreateFournisseurArticle()
		self.assertIsInstance(dao_Fournisseur_article.toUpdateFournisseurArticle(1,objet),Model_FournisseurArticle)
		pprint(Model_FournisseurArticle.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetFournisseurArticle(self):
		pprint ('test_toGetFournisseurArticle')
		self.assertIsInstance(dao_Fournisseur_article.toGetFournisseurArticle(1),Model_FournisseurArticle)
		pprint('SUCCES')

	def test_toGetListFournisseurArticle(self):
		pprint ('test_toGetListFournisseurArticle')
		self.assertIn(dao_Fournisseur_article.toGetFournisseurArticle(1),dao_Fournisseur_article.toListFournisseurArticle())
		pprint('SUCCES')
	def test_toDeleteFournisseurArticle(self):
		pprint ('test_toDeleteFournisseurArticle')
		self.assertTrue(dao_Fournisseur_article.toDeleteFournisseurArticle(1))
		pprint('SUCCES')
