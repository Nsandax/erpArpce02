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
from ErpBackOffice.dao.dao_categorie_article import dao_ligne_reception

class Model_Ligne_reception (TestCase):

	def __init__(self, navigator):
		#la liste des ligne_reception
		navigator.find_element_by_id('link_list_model_ligne_reception').click()
		#test de cr�ation d une ligne_reception
		bon_reception_id = one example
		ligne_reception = self.creation(navigator, bon_reception_id)

		#retour � la liste des ligne_reception
		navigator.find_element_by_id('link_list_model_ligne_reception').click()

		#test de modification d'un ligne_reception
		bon_reception_id = another example
		self.modification(navigator, bon_reception_id, ligne_reception)


	def creation(self, navigator, bon_reception_id):
		#print('test concernant la "Cr�ation ligne_reception"')
		navigator.find_element_by_id('btn_creer').click()

		#input_bon_reception_id
		input_bon_reception_id = navigator.find_element_by_name('bon_reception_id')
		input_bon_reception_id.clear()
		input_bon_reception_id.send_keys(bon_reception_id)

		reponse = self.verification(bon_reception_id)
		if reponse != None:
			#print('Test de cr�ation d une ligne_reception est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(bon_reception_id)
			if reponse != None:
				#print('Test de cr�ation d une ligne_reception est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une ligne_reception est un �chec')
				exit()

	def verification(self, bon_reception_id):
		#print('verification de l enregistrement')
		return dao_ligne_reception.toGetLigneReceptionByBon_reception_id(bon_reception_id)

	def modification(self, navigator, bon_reception_id, ligne_reception):
		#print('test concernant la "Modification ligne_reception"')

		item_id = 'link_item_' + str(ligne_reception.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_bon_reception_id
		input_bon_reception_id = navigator.find_element_by_name('bon_reception_id')
		input_bon_reception_id.clear()
		input_bon_reception_id.send_keys(bon_reception_id)
		reponse = self.verification(bon_reception_id)
		if reponse != None:
			#print('Test de modification d une ligne_reception est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(bon_reception_id)
			if reponse != None:
				#print('Test de modification d une ligne_reception est une r�ussite')
			else:
				#print('Test de modification d une ligne_reception est un �chec')
				exit()