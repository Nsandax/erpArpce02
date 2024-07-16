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
from ErpBackOffice.dao.dao_categorie_article import dao_transaction_fournisseur

class Model_Transaction_fournisseur (TestCase):

	def __init__(self, navigator):
		#la liste des transaction_fournisseur
		navigator.find_element_by_id('link_list_model_transaction_fournisseur').click()
		#test de cr�ation d une transaction_fournisseur
		status = one example
		transaction_fournisseur = self.creation(navigator, status)

		#retour � la liste des transaction_fournisseur
		navigator.find_element_by_id('link_list_model_transaction_fournisseur').click()

		#test de modification d'un transaction_fournisseur
		status = another example
		self.modification(navigator, status, transaction_fournisseur)


	def creation(self, navigator, status):
		#print('test concernant la "Cr�ation transaction_fournisseur"')
		navigator.find_element_by_id('btn_creer').click()

		#input_status
		input_status = navigator.find_element_by_name('status')
		input_status.clear()
		input_status.send_keys(status)

		reponse = self.verification(status)
		if reponse != None:
			#print('Test de cr�ation d une transaction_fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(status)
			if reponse != None:
				#print('Test de cr�ation d une transaction_fournisseur est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une transaction_fournisseur est un �chec')
				exit()

	def verification(self, status):
		#print('verification de l enregistrement')
		return dao_transaction_fournisseur.toGetTransactionFournisseurByStatus(status)

	def modification(self, navigator, status, transaction_fournisseur):
		#print('test concernant la "Modification transaction_fournisseur"')

		item_id = 'link_item_' + str(transaction_fournisseur.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_status
		input_status = navigator.find_element_by_name('status')
		input_status.clear()
		input_status.send_keys(status)
		reponse = self.verification(status)
		if reponse != None:
			#print('Test de modification d une transaction_fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(status)
			if reponse != None:
				#print('Test de modification d une transaction_fournisseur est une r�ussite')
			else:
				#print('Test de modification d une transaction_fournisseur est un �chec')
				exit()