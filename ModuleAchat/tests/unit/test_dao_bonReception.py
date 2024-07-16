# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_bon_reception import dao_bon_reception
from ErpBackOffice.models import Model_Bon_reception
from ErpBackOffice.models import Model_Personne

class Test_DaoBonReception (TestCase):


    @classmethod
    def setUpTestData(cls):
        #Creation d'un Auteur
        Model_Personne.objects.create(nom_complet = "Liliane")
        #Creation d'un objet Transaction Fournisseur
        Model_Bon_reception.objects.create(numero_reception="003-58DR",montant_global=13500,quantite=13)
        Model_Bon_reception.objects.create(numero_reception="004-58DR",montant_global=12500,quantite=2)
        
    def setUp(self):
        #Affectation de l'auteur dans une variable
        self.auteur = Model_Personne.objects.get(pk=1)


    def test_CreateSaveBonReception(self):
        pprint ('test_CreateSaveBonReception')
        objet = dao_bon_reception.toCreateBonReception("005-58DR",200.0,"2019-01-20",False,3,"","endup",0,0,0)
        self.assertIsInstance(dao_bon_reception.toSaveBonReception(self.auteur,objet),Model_Bon_reception)
        pprint('SUCCES')

    def test_UpdateBonReception(self):
        pprint ('test_UpdateBonReception')
        objet = dao_bon_reception.toCreateBonReception("009-58DR",200.0,"2019-01-20",False,3,"","endup",0,0,0)
        self.assertIsInstance(dao_bon_reception.toUpdateBonReception(1,objet),Model_Bon_reception)
        pprint(Model_Bon_reception.objects.get(pk=1))
        pprint('SUCCES')

    def test_toGetBonReception(self):
        pprint ('test_toGetBonReception')
        self.assertIsInstance(dao_bon_reception.toGetBonReception(1),Model_Bon_reception)
        pprint('SUCCES')

    def test_toGetListBonReception(self):
        pprint ('test_toGetListBonReception')
        self.assertIn(dao_bon_reception.toGetBonReception(1),dao_bon_reception.toListBonReception())
        pprint('SUCCES')

    def test_toDeleteBonReception(self):
        pprint ('test_toDeleteBonReception')
        self.assertTrue(dao_bon_reception.toDeleteBonReception(1))
        pprint('SUCCES')




    