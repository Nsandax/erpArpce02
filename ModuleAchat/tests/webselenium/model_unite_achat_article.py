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
from ErpBackOffice.dao.dao_categorie_article import dao_unite_achat_article

class Model_Unite_achat_article (TestCase):

	def __init__(self, navigator):
		#la liste des unite_achat_article
		navigator.find_element_by_id('link_list_model_unite_achat_article').click()
		#test de cr�ation d une unite_achat_article
		article_id = one example
		unite_achat_article = self.creation(navigator, article_id)

		#retour � la liste des unite_achat_article
		navigator.find_element_by_id('link_list_model_unite_achat_article').click()

		#test de modification d'un unite_achat_article
		article_id = another example
		self.modification(navigator, article_id, unite_achat_article)


	def creation(self, navigator, article_id):
		#print('test concernant la "Cr�ation unite_achat_article"')
		navigator.find_element_by_id('btn_creer').click()

		#input_article_id
		input_article_id = navigator.find_element_by_name('article_id')
		input_article_id.clear()
		input_article_id.send_keys(article_id)

		reponse = self.verification(article_id)
		if reponse != None:
			#print('Test de cr�ation d une unite_achat_article est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(article_id)
			if reponse != None:
				#print('Test de cr�ation d une unite_achat_article est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une unite_achat_article est un �chec')
				exit()

	def verification(self, article_id):
		#print('verification de l enregistrement')
		return dao_unite_achat_article.toGetUniteAchatArticleByArticle_id(article_id)

	def modification(self, navigator, article_id, unite_achat_article):
		#print('test concernant la "Modification unite_achat_article"')

		item_id = 'link_item_' + str(unite_achat_article.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_article_id
		input_article_id = navigator.find_element_by_name('article_id')
		input_article_id.clear()
		input_article_id.send_keys(article_id)
		reponse = self.verification(article_id)
		if reponse != None:
			#print('Test de modification d une unite_achat_article est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(article_id)
			if reponse != None:
				#print('Test de modification d une unite_achat_article est une r�ussite')
			else:
				#print('Test de modification d une unite_achat_article est un �chec')
				exit()