# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_type_emplacement import dao_type_emplacement
from ErpBackOffice.models import Model_TypeEmplacement
from ErpBackOffice.models import Model_Personne

class Test_DaoTypeEmplacement (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_TypeEmplacement pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_TypeEmplacement.objects.create(designation="Rangée")
		Model_TypeEmplacement.objects.create(designation="Ligné")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveTypeEmplacement(self):
		pprint ('test_CreateTypeEmplacement')
		#A Configurer
		objet = dao_Type_emplacement.toCreateTypeEmplacement()
		self.assertIsInstance(dao_Type_emplacement.toSaveTypeEmplacement(self.auteur,objet),Model_TypeEmplacement)
		pprint('SUCCES')

	def test_UpdateTypeEmplacement(self):
		pprint ('test_UpdateTypeEmplacement')
		objet = dao_Type_emplacement.toCreateTypeEmplacement()
		self.assertIsInstance(dao_Type_emplacement.toUpdateTypeEmplacement(1,objet),Model_TypeEmplacement)
		pprint(Model_TypeEmplacement.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetTypeEmplacement(self):
		pprint ('test_toGetTypeEmplacement')
		self.assertIsInstance(dao_Type_emplacement.toGetTypeEmplacement(1),Model_TypeEmplacement)
		pprint('SUCCES')

	def test_toGetListTypeEmplacement(self):
		pprint ('test_toGetListTypeEmplacement')
		self.assertIn(dao_Type_emplacement.toGetTypeEmplacement(1),dao_Type_emplacement.toListTypeEmplacement())
		pprint('SUCCES')
	def test_toDeleteTypeEmplacement(self):
		pprint ('test_toDeleteTypeEmplacement')
		self.assertTrue(dao_Type_emplacement.toDeleteTypeEmplacement(1))
		pprint('SUCCES')
