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
from ErpBackOffice.dao.dao_categorie_article import dao_bon_reception

class Model_Bon_reception (TestCase):

	def __init__(self, navigator):
		#la liste des bon_reception
		navigator.find_element_by_id('link_list_model_bon_reception').click()
		#test de cr�ation d une bon_reception
		numero_reception = one example
		bon_reception = self.creation(navigator, numero_reception)

		#retour � la liste des bon_reception
		navigator.find_element_by_id('link_list_model_bon_reception').click()

		#test de modification d'un bon_reception
		numero_reception = another example
		self.modification(navigator, numero_reception, bon_reception)


	def creation(self, navigator, numero_reception):
		#print('test concernant la "Cr�ation bon_reception"')
		navigator.find_element_by_id('btn_creer').click()

		#input_numero_reception
		input_numero_reception = navigator.find_element_by_name('numero_reception')
		input_numero_reception.clear()
		input_numero_reception.send_keys(numero_reception)

		reponse = self.verification(numero_reception)
		if reponse != None:
			#print('Test de cr�ation d une bon_reception est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(numero_reception)
			if reponse != None:
				#print('Test de cr�ation d une bon_reception est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une bon_reception est un �chec')
				exit()

	def verification(self, numero_reception):
		#print('verification de l enregistrement')
		return dao_bon_reception.toGetBonReceptionByNumero_reception(numero_reception)

	def modification(self, navigator, numero_reception, bon_reception):
		#print('test concernant la "Modification bon_reception"')

		item_id = 'link_item_' + str(bon_reception.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_numero_reception
		input_numero_reception = navigator.find_element_by_name('numero_reception')
		input_numero_reception.clear()
		input_numero_reception.send_keys(numero_reception)
		reponse = self.verification(numero_reception)
		if reponse != None:
			#print('Test de modification d une bon_reception est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(numero_reception)
			if reponse != None:
				#print('Test de modification d une bon_reception est une r�ussite')
			else:
				#print('Test de modification d une bon_reception est un �chec')
				exit()