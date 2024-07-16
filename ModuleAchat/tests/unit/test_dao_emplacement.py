# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_emplacement import dao_emplacement
from ErpBackOffice.models import Model_Emplacement
from ErpBackOffice.models import Model_Personne

class Test_DaoEmplacement (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_Emplacement pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Emplacement.objects.create(designation="Entrepot")
		Model_Emplacement.objects.create(designation="Magasin")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveEmplacement(self):
		pprint ('test_CreateEmplacement')
		#A Configurer
		objet = dao_Emplacement.toCreateEmplacement()
		self.assertIsInstance(dao_Emplacement.toSaveEmplacement(self.auteur,objet),Model_Emplacement)
		pprint('SUCCES')

	def test_UpdateEmplacement(self):
		pprint ('test_UpdateEmplacement')
		objet = dao_Emplacement.toCreateEmplacement()
		self.assertIsInstance(dao_Emplacement.toUpdateEmplacement(1,objet),Model_Emplacement)
		pprint(Model_Emplacement.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetEmplacement(self):
		pprint ('test_toGetEmplacement')
		self.assertIsInstance(dao_Emplacement.toGetEmplacement(1),Model_Emplacement)
		pprint('SUCCES')

	def test_toGetListEmplacement(self):
		pprint ('test_toGetListEmplacement')
		self.assertIn(dao_Emplacement.toGetEmplacement(1),dao_Emplacement.toListEmplacement())
		pprint('SUCCES')
	def test_toDeleteEmplacement(self):
		pprint ('test_toDeleteEmplacement')
		self.assertTrue(dao_Emplacement.toDeleteEmplacement(1))
		pprint('SUCCES')
