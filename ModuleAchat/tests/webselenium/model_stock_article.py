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
from ErpBackOffice.dao.dao_categorie_article import dao_stock_article

class Model_Stock_article (TestCase):

	def __init__(self, navigator):
		#la liste des stock_article
		navigator.find_element_by_id('link_list_model_stock_article').click()
		#test de cr�ation d une stock_article
		article_id = one example
		stock_article = self.creation(navigator, article_id)

		#retour � la liste des stock_article
		navigator.find_element_by_id('link_list_model_stock_article').click()

		#test de modification d'un stock_article
		article_id = another example
		self.modification(navigator, article_id, stock_article)


	def creation(self, navigator, article_id):
		#print('test concernant la "Cr�ation stock_article"')
		navigator.find_element_by_id('btn_creer').click()

		#input_article_id
		input_article_id = navigator.find_element_by_name('article_id')
		input_article_id.clear()
		input_article_id.send_keys(article_id)

		reponse = self.verification(article_id)
		if reponse != None:
			#print('Test de cr�ation d une stock_article est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(article_id)
			if reponse != None:
				#print('Test de cr�ation d une stock_article est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une stock_article est un �chec')
				exit()

	def verification(self, article_id):
		#print('verification de l enregistrement')
		return dao_stock_article.toGetStockArticleByArticle_id(article_id)

	def modification(self, navigator, article_id, stock_article):
		#print('test concernant la "Modification stock_article"')

		item_id = 'link_item_' + str(stock_article.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_article_id
		input_article_id = navigator.find_element_by_name('article_id')
		input_article_id.clear()
		input_article_id.send_keys(article_id)
		reponse = self.verification(article_id)
		if reponse != None:
			#print('Test de modification d une stock_article est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(article_id)
			if reponse != None:
				#print('Test de modification d une stock_article est une r�ussite')
			else:
				#print('Test de modification d une stock_article est un �chec')
				exit()