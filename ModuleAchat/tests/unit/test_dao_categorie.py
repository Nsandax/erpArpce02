# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_categorie import dao_categorie
from ErpBackOffice.models import Model_Categorie
from ErpBackOffice.models import Model_Personne

class Test_DaoCategorie (TestCase):

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

	def test_CreateSaveCategorie(self):
		pprint ('test_CreateCategorie')
		#A Configurer
		objet = dao_Categorie.toCreateCategorie()
		self.assertIsInstance(dao_Categorie.toSaveCategorie(self.auteur,objet),Model_Categorie)
		pprint('SUCCES')

	def test_UpdateCategorie(self):
		pprint ('test_UpdateCategorie')
		objet = dao_Categorie.toCreateCategorie()
		self.assertIsInstance(dao_Categorie.toUpdateCategorie(1,objet),Model_Categorie)
		pprint(Model_Categorie.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetCategorie(self):
		pprint ('test_toGetCategorie')
		self.assertIsInstance(dao_Categorie.toGetCategorie(1),Model_Categorie)
		pprint('SUCCES')

	def test_toGetListCategorie(self):
		pprint ('test_toGetListCategorie')
		self.assertIn(dao_Categorie.toGetCategorie(1),dao_Categorie.toListCategorie())
		pprint('SUCCES')
	def test_toDeleteCategorie(self):
		pprint ('test_toDeleteCategorie')
		self.assertTrue(dao_Categorie.toDeleteCategorie(1))
		pprint('SUCCES')
