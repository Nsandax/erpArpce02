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
from ErpBackOffice.dao.dao_categorie_article import dao_facture_fournisseur

class Model_Facture_fournisseur (TestCase):

	def __init__(self, navigator):
		#la liste des facture_fournisseur
		navigator.find_element_by_id('link_list_model_facture_fournisseur').click()
		#test de cr�ation d une facture_fournisseur
		numero_facture = one example
		facture_fournisseur = self.creation(navigator, numero_facture)

		#retour � la liste des facture_fournisseur
		navigator.find_element_by_id('link_list_model_facture_fournisseur').click()

		#test de modification d'un facture_fournisseur
		numero_facture = another example
		self.modification(navigator, numero_facture, facture_fournisseur)


	def creation(self, navigator, numero_facture):
		#print('test concernant la "Cr�ation facture_fournisseur"')
		navigator.find_element_by_id('btn_creer').click()

		#input_numero_facture
		input_numero_facture = navigator.find_element_by_name('numero_facture')
		input_numero_facture.clear()
		input_numero_facture.send_keys(numero_facture)

		reponse = self.verification(numero_facture)
		if reponse != None:
			#print('Test de cr�ation d une facture_fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(numero_facture)
			if reponse != None:
				#print('Test de cr�ation d une facture_fournisseur est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une facture_fournisseur est un �chec')
				exit()

	def verification(self, numero_facture):
		#print('verification de l enregistrement')
		return dao_facture_fournisseur.toGetFactureFournisseurByNumero_facture(numero_facture)

	def modification(self, navigator, numero_facture, facture_fournisseur):
		#print('test concernant la "Modification facture_fournisseur"')

		item_id = 'link_item_' + str(facture_fournisseur.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_numero_facture
		input_numero_facture = navigator.find_element_by_name('numero_facture')
		input_numero_facture.clear()
		input_numero_facture.send_keys(numero_facture)
		reponse = self.verification(numero_facture)
		if reponse != None:
			#print('Test de modification d une facture_fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(numero_facture)
			if reponse != None:
				#print('Test de modification d une facture_fournisseur est une r�ussite')
			else:
				#print('Test de modification d une facture_fournisseur est un �chec')
				exit()