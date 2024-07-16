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
from ErpBackOffice.dao.dao_categorie_article import dao_categorie

class Model_Categorie (TestCase):

	def __init__(self, navigator):
		#la liste des categorie
		navigator.find_element_by_id('link_list_model_categorie').click()
		#test de cr�ation d une categorie
		designation = one example
		categorie = self.creation(navigator, designation)

		#retour � la liste des categorie
		navigator.find_element_by_id('link_list_model_categorie').click()

		#test de modification d'un categorie
		designation = another example
		self.modification(navigator, designation, categorie)


	def creation(self, navigator, designation):
		#print('test concernant la "Cr�ation categorie"')
		navigator.find_element_by_id('btn_creer').click()

		#input_designation
		input_designation = navigator.find_element_by_name('designation')
		input_designation.clear()
		input_designation.send_keys(designation)

		reponse = self.verification(designation)
		if reponse != None:
			#print('Test de cr�ation d une categorie est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(designation)
			if reponse != None:
				#print('Test de cr�ation d une categorie est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une categorie est un �chec')
				exit()

	def verification(self, designation):
		#print('verification de l enregistrement')
		return dao_categorie.toGetCategorieByDesignation(designation)

	def modification(self, navigator, designation, categorie):
		#print('test concernant la "Modification categorie"')

		item_id = 'link_item_' + str(categorie.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_designation
		input_designation = navigator.find_element_by_name('designation')
		input_designation.clear()
		input_designation.send_keys(designation)
		reponse = self.verification(designation)
		if reponse != None:
			#print('Test de modification d une categorie est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(designation)
			if reponse != None:
				#print('Test de modification d une categorie est une r�ussite')
			else:
				#print('Test de modification d une categorie est un �chec')
				exit()