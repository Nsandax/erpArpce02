# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_unite import dao_unite
from ErpBackOffice.models import Model_Unite
from ErpBackOffice.models import Model_Personne

class Test_DaoUnite (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_Unite pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_Unite.objects.create(designation="DOLL")
		Model_Unite.objects.create(designation="UNI")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveUnite(self):
		pprint ('test_CreateUnite')
		#A Configurer
		objet = dao_Unite.toCreateUnite()
		self.assertIsInstance(dao_Unite.toSaveUnite(self.auteur,objet),Model_Unite)
		pprint('SUCCES')

	def test_UpdateUnite(self):
		pprint ('test_UpdateUnite')
		objet = dao_Unite.toCreateUnite()
		self.assertIsInstance(dao_Unite.toUpdateUnite(1,objet),Model_Unite)
		pprint(Model_Unite.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetUnite(self):
		pprint ('test_toGetUnite')
		self.assertIsInstance(dao_Unite.toGetUnite(1),Model_Unite)
		pprint('SUCCES')

	def test_toGetListUnite(self):
		pprint ('test_toGetListUnite')
		self.assertIn(dao_Unite.toGetUnite(1),dao_Unite.toListUnite())
		pprint('SUCCES')
	def test_toDeleteUnite(self):
		pprint ('test_toDeleteUnite')
		self.assertTrue(dao_Unite.toDeleteUnite(1))
		pprint('SUCCES')
