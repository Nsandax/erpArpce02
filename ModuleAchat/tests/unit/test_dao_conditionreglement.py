# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_condition_reglement import dao_condition_reglement
from ErpBackOffice.models import Model_ConditionReglement
from ErpBackOffice.models import Model_Personne

class Test_DaoConditionReglement (TestCase):

	@classmethod
	def setUpTestData(cls):
		#Creation d'un Auteur
		Model_Personne.objects.create(nom_complet = 'Serena')
		#Enregistrement dans la BD Test de deux objets Model_ConditionReglement pour besoin de test
		#A CONFIGURER LES PARAMETRES ENTRE PARENTHESE SELON L'EXEMPLE  !!!!!!
		Model_ConditionReglement.objects.create(designation="Pay Cash")
		Model_ConditionReglement.objects.create(designation="Tranche")

	def setUp(self):
		#Affectation de l'auteur dans une variable
		self.auteur = Model_Personne.objects.get(pk=1)

	def test_CreateSaveConditionReglement(self):
		pprint ('test_CreateConditionReglement')
		#A Configurer
		objet = dao_Condition_reglement.toCreateConditionReglement()
		self.assertIsInstance(dao_Condition_reglement.toSaveConditionReglement(self.auteur,objet),Model_ConditionReglement)
		pprint('SUCCES')

	def test_UpdateConditionReglement(self):
		pprint ('test_UpdateConditionReglement')
		objet = dao_Condition_reglement.toCreateConditionReglement()
		self.assertIsInstance(dao_Condition_reglement.toUpdateConditionReglement(1,objet),Model_ConditionReglement)
		pprint(Model_ConditionReglement.objects.get(pk=1))
		pprint('SUCCES')

	def test_toGetConditionReglement(self):
		pprint ('test_toGetConditionReglement')
		self.assertIsInstance(dao_Condition_reglement.toGetConditionReglement(1),Model_ConditionReglement)
		pprint('SUCCES')

	def test_toGetListConditionReglement(self):
		pprint ('test_toGetListConditionReglement')
		self.assertIn(dao_Condition_reglement.toGetConditionReglement(1),dao_Condition_reglement.toListConditionReglement())
		pprint('SUCCES')
	def test_toDeleteConditionReglement(self):
		pprint ('test_toDeleteConditionReglement')
		self.assertTrue(dao_Condition_reglement.toDeleteConditionReglement(1))
		pprint('SUCCES')
