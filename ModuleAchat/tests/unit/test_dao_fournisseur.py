# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pprint import pprint
from ModuleAchat.dao.dao_fournisseur import dao_fournisseur
from ErpBackOffice.models import Model_Fournisseur
from ErpBackOffice.models import Model_Personne

class Test_DaoFournisseur (TestCase):


    @classmethod
    def setUpTestData(cls):
        #Creation d'un Auteur
        Model_Personne.objects.create(nom_complet = "Liliane")
        #Creation d'un objet Transaction Fournisseur
        Model_Fournisseur.objects.create(nom_complet="Yoann gourcuff")
        Model_Fournisseur.objects.create(nom_complet="Roman Pavlyuchenko")
        
    def setUp(self):
        #Affectation de l'auteur dans une variable
        self.auteur = Model_Personne.objects.get(pk=1)


    def test_CreateSaveFournisseur(self):
        pprint ('test_CreateSaveFournisseur')
        objet = dao_fournisseur.toCreateFournisseur("Layvin","Kurzawa","Manochi","Layvin Kurzawa","","","","","lingala","kinshasa","2019-01-12","Aceka","agriculture","lifetime","2019-01-20",0,0)
        self.assertIsInstance(dao_fournisseur.toSaveFournisseur(self.auteur,objet),Model_Fournisseur)
        pprint('SUCCES')

    def test_UpdateFournisseur(self):
        pprint ('test_UpdateFournisseur')
        objet = dao_fournisseur.toCreateFournisseur("Thomas","Meunier","Manochi","Layvin Kurzawa","","","","","lingala","kinshasa","2019-01-12","Aceka","agriculture","lifetime","2019-01-20",0,0)
        self.assertIsInstance(dao_fournisseur.toUpdateFournisseur(2,objet),Model_Fournisseur)
        pprint(Model_Fournisseur.objects.get(pk=2))
        pprint('SUCCES')

    def test_toGetFournisseur(self):
        pprint ('test_toGetFournisseur')
        self.assertIsInstance(dao_fournisseur.toGetFournisseur(2),Model_Fournisseur)
        pprint('SUCCES')

    def test_toGetListFournisseur(self):
        pprint ('test_toGetListFournisseur')
        self.assertIn(dao_fournisseur.toGetFournisseur(2),dao_fournisseur.toListFournisseur())
        pprint('SUCCES')

    def test_toDeleteFournisseur(self):
        pprint ('test_toDeleteFournisseur')
        self.assertTrue(dao_fournisseur.toDeleteFournisseur(2))
        pprint('SUCCES')




    