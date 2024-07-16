# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_paiement_fournisseur import dao_paiement_fournisseur
from ErpBackOffice.models import Model_Paiement_fournisseur
from ErpBackOffice.models import Model_Personne

class Test_DaoPaiementFournisseur (TestCase):


    @classmethod
    def setUpTestData(cls):
        #Creation d'un Auteur
        Model_Personne.objects.create(nom_complet = "Liliane")
        #Creation d'un objet Transaction Fournisseur
        Model_Paiement_fournisseur.objects.create(montant=13500)
        Model_Paiement_fournisseur.objects.create(montant=12500)
        
    def setUp(self):
        #Affectation de l'auteur dans une variable
        self.auteur = Model_Personne.objects.get(pk=1)


    def test_CreateSavePaiementFournisseur(self):
        pprint ('test_CreateSavePaiementFournisseur')
        objet = dao_paiement_fournisseur.toCreatePaiementFournisseur(12500,'2019-01-20',False)
        self.assertIsInstance(dao_paiement_fournisseur.toSavePaiementFournisseur(self.auteur,objet),Model_Paiement_fournisseur)
        pprint('SUCCES')

    def test_UpdatePaiementFournisseur(self):
        pprint ('test_UpdatePaiementFournisseur')
        objet = dao_paiement_fournisseur.toCreatePaiementFournisseur(17500,'2019-01-22',False)
        self.assertIsInstance(dao_paiement_fournisseur.toUpdatePaiementFournisseur(1,objet),Model_Paiement_fournisseur)
        pprint(Model_Paiement_fournisseur.objects.get(pk=1))
        pprint('SUCCES')

    def test_toGetPaiementFournisseur(self):
        pprint ('test_toGetPaiementFournisseur')
        self.assertIsInstance(dao_paiement_fournisseur.toGetPaiementFournisseur(1),Model_Paiement_fournisseur)
        pprint('SUCCES')

    def test_toGetListPaiementFournisseur(self):
        pprint ('test_toGetListPaiementFournisseur')
        self.assertIn(dao_paiement_fournisseur.toGetPaiementFournisseur(1),dao_paiement_fournisseur.toListPaiementFournisseur())
        pprint('SUCCES')

    def test_toDeletePaiementFournisseur(self):
        pprint ('test_toDeletePaiementFournisseur')
        self.assertTrue(dao_paiement_fournisseur.toDeletePaiementFournisseur(1))
        pprint('SUCCES')




    