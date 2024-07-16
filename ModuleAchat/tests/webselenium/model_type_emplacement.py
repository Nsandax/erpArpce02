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
from ErpBackOffice.dao.dao_categorie_article import dao_type_emplacement

class Model_Type_emplacement (TestCase):

	def __init__(self, navigator):
		#la liste des type_emplacement
		navigator.find_element_by_id('link_list_model_type_emplacement').click()
		#test de cr�ation d une type_emplacement
		designation = one example
		type_emplacement = self.creation(navigator, designation)

		#retour � la liste des type_emplacement
		navigator.find_element_by_id('link_list_model_type_emplacement').click()

		#test de modification d'un type_emplacement
		designation = another example
		self.modification(navigator, designation, type_emplacement)


	def creation(self, navigator, designation):
		#print('test concernant la "Cr�ation type_emplacement"')
		navigator.find_element_by_id('btn_creer').click()

		#input_designation
		input_designation = navigator.find_element_by_name('designation')
		input_designation.clear()
		input_designation.send_keys(designation)

		reponse = self.verification(designation)
		if reponse != None:
			#print('Test de cr�ation d une type_emplacement est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(designation)
			if reponse != None:
				#print('Test de cr�ation d une type_emplacement est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une type_emplacement est un �chec')
				exit()

	def verification(self, designation):
		#print('verification de l enregistrement')
		return dao_type_emplacement.toGetTypeEmplacementByDesignation(designation)

	def modification(self, navigator, designation, type_emplacement):
		#print('test concernant la "Modification type_emplacement"')

		item_id = 'link_item_' + str(type_emplacement.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_designation
		input_designation = navigator.find_element_by_name('designation')
		input_designation.clear()
		input_designation.send_keys(designation)
		reponse = self.verification(designation)
		if reponse != None:
			#print('Test de modification d une type_emplacement est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(designation)
			if reponse != None:
				#print('Test de modification d une type_emplacement est une r�ussite')
			else:
				#print('Test de modification d une type_emplacement est un �chec')
				exit()