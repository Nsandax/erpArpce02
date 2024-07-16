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
from ErpBackOffice.models import Model_Personne
from pprint import pprint
from ErpBackOffice import views

#login
# TEST DE CONNEXION
# A CONFIGURER EN FONCTION DU CHEMIN DE VOTRE NAVIGATEUR
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
caps = DesiredCapabilities.FIREFOX.copy()
caps['marionette'] = True
navigator = webdriver.Firefox(firefox_binary=binary,capabilities=caps, executable_path='C:\laragon\www\DjangoApps\ErpProject\selenium_driver\geckodriver')
navigator.get('http://127.0.0.1:8000/utilisateur/connexion/')
navigator.maximize_window()
# LOGIN
loginBox = navigator.find_element_by_name('email')
loginBox.clear()
loginBox.send_keys('admin')
passwordBox = navigator.find_element_by_name('password')
passwordBox.clear()
passwordBox.send_keys('Password01')
time.sleep(1)
navigator.find_element_by_id('btn_connecter').click()
navigator.find_element_by_id('navbar_link_module_achat').click()
#print('\nDEBUT TEST DU ModuleAchat \n')

#_1 Appel du sc�nario pour le model article
from ModuleAchat.tests.webselenium.model_article import Model_Article
Model_Article(navigator)
#print('\n')

#_2 Appel du sc�nario pour le model bon_reception
from ModuleAchat.tests.webselenium.model_bon_reception import Model_Bon_reception
Model_Bon_reception(navigator)
#print('\n')

#_3 Appel du sc�nario pour le model categorie
from ModuleAchat.tests.webselenium.model_categorie import Model_Categorie
Model_Categorie(navigator)
#print('\n')

#_4 Appel du sc�nario pour le model condition_reglement
from ModuleAchat.tests.webselenium.model_condition_reglement import Model_Condition_reglement
Model_Condition_reglement(navigator)
#print('\n')

#_5 Appel du sc�nario pour le model emplacement
from ModuleAchat.tests.webselenium.model_emplacement import Model_Emplacement
Model_Emplacement(navigator)
#print('\n')
#print('\nFIN TEST DU MODULEACHAT \n')# -*- coding: utf-8 -*-
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
from ErpBackOffice.models import Model_Personne
from pprint import pprint
from ErpBackOffice import views

#login
# TEST DE CONNEXION
# A CONFIGURER EN FONCTION DU CHEMIN DE VOTRE NAVIGATEUR
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
caps = DesiredCapabilities.FIREFOX.copy()
caps['marionette'] = True
navigator = webdriver.Firefox(firefox_binary=binary,capabilities=caps, executable_path='C:\laragon\www\DjangoApps\ErpProject\selenium_driver\geckodriver')
navigator.get('http://127.0.0.1:8000/utilisateur/connexion/')
navigator.maximize_window()
# LOGIN
loginBox = navigator.find_element_by_name('email')
loginBox.clear()
loginBox.send_keys('admin')
passwordBox = navigator.find_element_by_name('password')
passwordBox.clear()
passwordBox.send_keys('Password01')
time.sleep(1)
navigator.find_element_by_id('btn_connecter').click()
navigator.find_element_by_id('navbar_link_module_achat').click()
#print('\nDEBUT TEST DU ModuleAchat \n')

#_1 Appel du sc�nario pour le model facture_fournisseur
from ModuleAchat.tests.webselenium.model_facture_fournisseur import Model_Facture_fournisseur
Model_Facture_fournisseur(navigator)
#print('\n')

#_2 Appel du sc�nario pour le model fournisseur
from ModuleAchat.tests.webselenium.model_fournisseur import Model_Fournisseur
Model_Fournisseur(navigator)
#print('\n')

#_3 Appel du sc�nario pour le model fournisseur_article
from ModuleAchat.tests.webselenium.model_fournisseur_article import Model_Fournisseur_article
Model_Fournisseur_article(navigator)
#print('\n')

#_4 Appel du sc�nario pour le model ligne_reception
from ModuleAchat.tests.webselenium.model_ligne_reception import Model_Ligne_reception
Model_Ligne_reception(navigator)
#print('\n')

#_5 Appel du sc�nario pour le model paiement_fournisseur
from ModuleAchat.tests.webselenium.model_paiement_fournisseur import Model_Paiement_fournisseur
Model_Paiement_fournisseur(navigator)
#print('\n')

#_6 Appel du sc�nario pour le model stock_article
from ModuleAchat.tests.webselenium.model_stock_article import Model_Stock_article
Model_Stock_article(navigator)
#print('\n')

#_7 Appel du sc�nario pour le model transaction_fournisseur
from ModuleAchat.tests.webselenium.model_transaction_fournisseur import Model_Transaction_fournisseur
Model_Transaction_fournisseur(navigator)
#print('\n')

#_8 Appel du sc�nario pour le model type_article
from ModuleAchat.tests.webselenium.model_type_article import Model_Type_article
Model_Type_article(navigator)
#print('\n')

#_9 Appel du sc�nario pour le model type_emplacement
from ModuleAchat.tests.webselenium.model_type_emplacement import Model_Type_emplacement
Model_Type_emplacement(navigator)
#print('\n')

#_10 Appel du sc�nario pour le model unite
from ModuleAchat.tests.webselenium.model_unite import Model_Unite
Model_Unite(navigator)
#print('\n')

#_11 Appel du sc�nario pour le model unite_achat_article
from ModuleAchat.tests.webselenium.model_unite_achat_article import Model_Unite_achat_article
Model_Unite_achat_article(navigator)
#print('\n')
#print('\nFIN TEST DU MODULEACHAT \n')
