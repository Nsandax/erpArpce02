# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_facture_fournisseur import dao_facture_fournisseur
from ErpBackOffice.models import Model_Facture_fournisseur
from ErpBackOffice.models import Model_Personne

class Test_DaoFactureFournisseur (TestCase):


    @classmethod
    def setUpTestData(cls):
        #Creation d'un Auteur
        Model_Personne.objects.create(nom_complet = "Liliane")
        #Creation d'un objet Transaction Fournisseur
        Model_Facture_fournisseur.objects.create(numero_facture="FAC003-2015",montant=13500)
        Model_Facture_fournisseur.objects.create(numero_facture="FAC004-2015",montant=12500)
        
    def setUp(self):
        #Affectation de l'auteur dans une variable
        self.auteur = Model_Personne.objects.get(pk=1)


    def test_CreateSaveFactureFournisseur(self):
        pprint ('test_CreateSaveFactureFournisseur')
        objet = dao_facture_fournisseur.toCreateFactureFournisseur("FAC005-2015",200.0,False,"2019-01-20",0,0)
        self.assertIsInstance(dao_facture_fournisseur.toSaveFactureFournisseur(self.auteur,objet),Model_Facture_fournisseur)
        pprint('SUCCES')

    def test_UpdateFactureFournisseur(self):
        pprint ('test_UpdateFactureFournisseur')
        objet = dao_facture_fournisseur.toCreateFactureFournisseur("FAC010-2015",200.0,False,"2019-01-20",0,0)
        self.assertIsInstance(dao_facture_fournisseur.toUpdateFactureFournisseur(1,objet),Model_Facture_fournisseur)
        pprint(Model_Facture_fournisseur.objects.get(pk=1))
        pprint('SUCCES')


    def test_toGetFactureFournisseur(self):
        pprint ('test_toGetFactureFournisseur')
        self.assertIsInstance(dao_facture_fournisseur.toGetFactureFournisseur(1),Model_Facture_fournisseur)
        pprint('SUCCES')

    def test_toGetListFactureFournisseur(self):
        pprint ('test_toGetListFactureFournisseur')
        self.assertIn(dao_facture_fournisseur.toGetFactureFournisseur(1),dao_facture_fournisseur.toListFactureFournisseur())
        pprint('SUCCES')

    def test_toDeleteFactureFournisseur(self):
        pprint ('test_toDeleteFactureFournisseur')
        self.assertTrue(dao_facture_fournisseur.toDeleteFactureFournisseur(1))
        pprint('SUCCES')




    