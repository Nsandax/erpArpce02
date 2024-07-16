# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_transaction_fournisseur import dao_transaction_fournisseur
from ErpBackOffice.models import Model_Transaction_fournisseur
from ErpBackOffice.models import Model_Personne

class Test_DaoTransactionFournisseur (TestCase):


    @classmethod
    def setUpTestData(cls):
    	#Creation d'un Auteur
        Model_Personne.objects.create(nom_complet = "Liliane")
        #Creation d'un objet Transaction Fournisseur
        Model_Transaction_fournisseur.objects.create(status="en cours", sequence=1)
        Model_Transaction_fournisseur.objects.create(status ="endUp", sequence=4)
        
    def setUp(self):
    	#Affectation de l'auteur dans une variable
    	self.auteur = Model_Personne.objects.get(pk=1)


    def test_CreateSaveTransactionFournisseur(self):
        pprint ('test_CreateSaveTransactionFournisseur')
        objet = dao_transaction_fournisseur.toCreateTransactionFournisseur("en cours","banque",True,2,0)
        self.assertIsInstance(dao_transaction_fournisseur.toSaveTransactionFournisseur(self.auteur,objet),Model_Transaction_fournisseur)
        pprint('SUCCES')

    def test_UpdateTransactionFournisseur(self):
        pprint ('test_UpdateTransactionFournisseur')
        objet = dao_transaction_fournisseur.toCreateTransactionFournisseur("fini","banque",False,2,0)
        self.assertIsInstance(dao_transaction_fournisseur.toUpdateTransactionFournisseur(1,objet),Model_Transaction_fournisseur)
        pprint(Model_Transaction_fournisseur.objects.get(pk=1))
        pprint('SUCCES')

    def test_toGetTransactionFournisseur(self):
    	pprint ('test_toGetTransactionFournisseur')
    	self.assertIsInstance(dao_transaction_fournisseur.toGetTransactionFournisseur(1),Model_Transaction_fournisseur)
    	pprint('SUCCES')

    def test_toGetListTransactionFournisseur(self):
    	pprint ('test_toGetListTransactionFournisseur')
    	self.assertIn(dao_transaction_fournisseur.toGetTransactionFournisseur(1),dao_transaction_fournisseur.toListTransactionFournisseur())
    	pprint('SUCCES')

    def test_toDeleteTransactionFournisseur(self):
    	pprint ('test_toDeleteTransactionFournisseur')
    	self.assertTrue(dao_transaction_fournisseur.toDeleteTransactionFournisseur(1))
    	pprint('SUCCES')




    