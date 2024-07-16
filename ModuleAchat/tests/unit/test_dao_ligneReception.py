# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_ligne_reception import dao_ligne_reception
from ErpBackOffice.models import Model_Ligne_reception
from ErpBackOffice.models import Model_Personne

class Test_DaoLigneReception (TestCase):


    @classmethod
    def setUpTestData(cls):
        #Creation d'un Auteur
        Model_Personne.objects.create(nom_complet = "Liliane")
        #Creation d'un objet Transaction Fournisseur
        Model_Ligne_reception.objects.create(quantite_demandee=18,quantite_fournie=14, prix_unitaire=5000.0, prix_lot=150000.0)
        Model_Ligne_reception.objects.create(quantite_demandee=6,quantite_fournie=5, prix_unitaire=4000.0, prix_lot=160000.0)
        
    def setUp(self):
        #Affectation de l'auteur dans une variable
        self.auteur = Model_Personne.objects.get(pk=1)


    def test_CreateSaveLigneReception(self):
        pprint ('test_CreateSaveLigneReception')
        objet = dao_ligne_reception.toCreateLigneReception(15,13,500,1500,'lubicz',0,0)
        self.assertIsInstance(dao_ligne_reception.toSaveLigneReception(self.auteur,objet),Model_Ligne_reception)
        pprint('SUCCES')

    def test_UpdateLigneReception(self):
        pprint ('test_UpdateLigneReception')
        objet = dao_ligne_reception.toCreateLigneReception(18,14,504,1600,'yourg',0,0)
        self.assertIsInstance(dao_ligne_reception.toUpdateLigneReception(1,objet),Model_Ligne_reception)
        pprint(Model_Ligne_reception.objects.get(pk=1))
        pprint('SUCCES')

    def test_toGetLigneReception(self):
        pprint ('test_toGetLigneReception')
        self.assertIsInstance(dao_ligne_reception.toGetLigneReception(1),Model_Ligne_reception)
        pprint('SUCCES')

    def test_toGetListLigneReception(self):
        pprint ('test_toGetListLigneReception')
        self.assertIn(dao_ligne_reception.toGetLigneReception(1),dao_ligne_reception.toListLigneReception())
        pprint('SUCCES')

    def test_toDeleteLigneReception(self):
        pprint ('test_toDeleteLigneReception')
        self.assertTrue(dao_ligne_reception.toDeleteLigneReception(1))
        pprint('SUCCES')




    