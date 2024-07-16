# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_categorie_unite import dao_categorie_unite
from ErpBackOffice.models import Model_Categorie
from ErpBackOffice.models import Model_Personne

class Test_DaoCategorieUnite (TestCase):

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

	def test_CreateSaveCategorieUnite(self):
		pprint ('test_CreateCategorieUnite')
		#A Configurer
		objet = dao_Categorie_unite.toCreateCategorieUnite()
		self.assertIsInstance(dao_Categorie_unite.toSaveCategorieUnite(self.auteur,objet),Model_Categorie)
		pprint('SUCCES')

	def test_UpdateCategorieUnite(self):
		pprint ('test_UpdateCategorieUnite')
		objet = dao_Categorie_unite.toCreateCategorieUnite()
		self.assertIsInstance(dao_Categorie_unite.toUpdateCategorieUnite(1,objet),Model_Categorie)
		pprint(Model_Categorie.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetCategorieUnite(self):
		pprint ('test_toGetCategorieUnite')
		self.assertIsInstance(dao_Categorie_unite.toGetCategorieUnite(1),Model_Categorie)
		pprint('SUCCES')

	def test_toGetListCategorieUnite(self):
		pprint ('test_toGetListCategorieUnite')
		self.assertIn(dao_Categorie_unite.toGetCategorieUnite(1),dao_Categorie_unite.toListCategorieUnite())
		pprint('SUCCES')
	def test_toDeleteCategorieUnite(self):
		pprint ('test_toDeleteCategorieUnite')
		self.assertTrue(dao_Categorie_unite.toDeleteCategorieUnite(1))
		pprint('SUCCES')
