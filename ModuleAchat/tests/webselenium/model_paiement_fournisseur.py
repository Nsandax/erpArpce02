# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import time
from django.core.urlresolvers import reverse
from django.test import Client
from pprint import pprint

#import dao relatif au model
from ErpBackOffice.dao.dao_categorie_article import dao_paiement_fournisseur

class Model_Paiement_fournisseur (TestCase):

	def __init__(self, navigator):
		#la liste des paiement_fournisseur
		navigator.find_element_by_id('link_list_model_paiement_fournisseur').click()
		#test de cr�ation d une paiement_fournisseur
		facture_fournisseur_id = one example
		paiement_fournisseur = self.creation(navigator, facture_fournisseur_id)

		#retour � la liste des paiement_fournisseur
		navigator.find_element_by_id('link_list_model_paiement_fournisseur').click()

		#test de modification d'un paiement_fournisseur
		facture_fournisseur_id = another example
		self.modification(navigator, facture_fournisseur_id, paiement_fournisseur)


	def creation(self, navigator, facture_fournisseur_id):
		#print('test concernant la "Cr�ation paiement_fournisseur"')
		navigator.find_element_by_id('btn_creer').click()

		#input_facture_fournisseur_id
		input_facture_fournisseur_id = navigator.find_element_by_name('facture_fournisseur_id')
		input_facture_fournisseur_id.clear()
		input_facture_fournisseur_id.send_keys(facture_fournisseur_id)

		reponse = self.verification(facture_fournisseur_id)
		if reponse != None:
			#print('Test de cr�ation d une paiement_fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(facture_fournisseur_id)
			if reponse != None:
				#print('Test de cr�ation d une paiement_fournisseur est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une paiement_fournisseur est un �chec')
				exit()

	def verification(self, facture_fournisseur_id):
		#print('verification de l enregistrement')
		return dao_paiement_fournisseur.toGetPaiementFournisseurByFacture_fournisseur_id(facture_fournisseur_id)

	def modification(self, navigator, facture_fournisseur_id, paiement_fournisseur):
		#print('test concernant la "Modification paiement_fournisseur"')

		item_id = 'link_item_' + str(paiement_fournisseur.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_facture_fournisseur_id
		input_facture_fournisseur_id = navigator.find_element_by_name('facture_fournisseur_id')
		input_facture_fournisseur_id.clear()
		input_facture_fournisseur_id.send_keys(facture_fournisseur_id)
		reponse = self.verification(facture_fournisseur_id)
		if reponse != None:
			#print('Test de modification d une paiement_fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(facture_fournisseur_id)
			if reponse != None:
				#print('Test de modification d une paiement_fournisseur est une r�ussite')
			else:
				#print('Test de modification d une paiement_fournisseur est un �chec')
				exit()