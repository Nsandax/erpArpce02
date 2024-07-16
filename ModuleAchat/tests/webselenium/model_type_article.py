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
from ErpBackOffice.dao.dao_categorie_article import dao_type_article

class Model_Type_article (TestCase):

	def __init__(self, navigator):
		#la liste des type_article
		navigator.find_element_by_id('link_list_model_type_article').click()
		#test de cr�ation d une type_article
		nature = one example
		type_article = self.creation(navigator, nature)

		#retour � la liste des type_article
		navigator.find_element_by_id('link_list_model_type_article').click()

		#test de modification d'un type_article
		nature = another example
		self.modification(navigator, nature, type_article)


	def creation(self, navigator, nature):
		#print('test concernant la "Cr�ation type_article"')
		navigator.find_element_by_id('btn_creer').click()

		#input_nature
		input_nature = navigator.find_element_by_name('nature')
		input_nature.clear()
		input_nature.send_keys(nature)

		reponse = self.verification(nature)
		if reponse != None:
			#print('Test de cr�ation d une type_article est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(nature)
			if reponse != None:
				#print('Test de cr�ation d une type_article est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une type_article est un �chec')
				exit()

	def verification(self, nature):
		#print('verification de l enregistrement')
		return dao_type_article.toGetTypeArticleByNature(nature)

	def modification(self, navigator, nature, type_article):
		#print('test concernant la "Modification type_article"')

		item_id = 'link_item_' + str(type_article.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_nature
		input_nature = navigator.find_element_by_name('nature')
		input_nature.clear()
		input_nature.send_keys(nature)
		reponse = self.verification(nature)
		if reponse != None:
			#print('Test de modification d une type_article est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(nature)
			if reponse != None:
				#print('Test de modification d une type_article est une r�ussite')
			else:
				#print('Test de modification d une type_article est un �chec')
				exit()