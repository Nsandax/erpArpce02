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
from ErpBackOffice.dao.dao_categorie_article import dao_fournisseur

class Model_Fournisseur (TestCase):

	def __init__(self, navigator):
		#la liste des fournisseur
		navigator.find_element_by_id('link_list_model_fournisseur').click()
		#test de cr�ation d une fournisseur
		nom_complet = one example
		fournisseur = self.creation(navigator, nom_complet)

		#retour � la liste des fournisseur
		navigator.find_element_by_id('link_list_model_fournisseur').click()

		#test de modification d'un fournisseur
		nom_complet = another example
		self.modification(navigator, nom_complet, fournisseur)


	def creation(self, navigator, nom_complet):
		#print('test concernant la "Cr�ation fournisseur"')
		navigator.find_element_by_id('btn_creer').click()

		#input_nom_complet
		input_nom_complet = navigator.find_element_by_name('nom_complet')
		input_nom_complet.clear()
		input_nom_complet.send_keys(nom_complet)

		reponse = self.verification(nom_complet)
		if reponse != None:
			#print('Test de cr�ation d une fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(nom_complet)
			if reponse != None:
				#print('Test de cr�ation d une fournisseur est une r�ussite')
				return reponse
			else:
				#print('Test de cr�ation d une fournisseur est un �chec')
				exit()

	def verification(self, nom_complet):
		#print('verification de l enregistrement')
		return dao_fournisseur.toGetFournisseurByNom_complet(nom_complet)

	def modification(self, navigator, nom_complet, fournisseur):
		#print('test concernant la "Modification fournisseur"')

		item_id = 'link_item_' + str(fournisseur.id)
		navigator.find_element_by_id(item_id).click()
		navigator.find_element_by_id('btn_modifier').click()

		#input_nom_complet
		input_nom_complet = navigator.find_element_by_name('nom_complet')
		input_nom_complet.clear()
		input_nom_complet.send_keys(nom_complet)
		reponse = self.verification(nom_complet)
		if reponse != None:
			#print('Test de modification d une fournisseur est un �chec car existe d�j�')
			return reponse
		else:
			navigator.find_element_by_id('btn_valider').click()
			reponse = self.verification(nom_complet)
			if reponse != None:
				#print('Test de modification d une fournisseur est une r�ussite')
			else:
				#print('Test de modification d une fournisseur est un �chec')
				exit()