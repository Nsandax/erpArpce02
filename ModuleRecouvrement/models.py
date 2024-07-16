# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ErpBackOffice.models import Model_Personne

# Create your models here.
ChoixNbJours  =  ((-7, '-7 jours'),(-6, '-6 jours'),(-5, '-5 jours'),(-4, '-4 jours'),(-3, '-3 jours'),(-2, '-2 jours'),(-1, '-1 jour'),(0, '+0 jour'),(1, '+1 jours'),(2, '+2 jours'),(3, '+3 jours'),(4, '+4 jours'),(5, '+5 jours'),(6, '+6 jours'),(7, '+7 jours'))
ChoixTypeAction  =  (('contentieux', 'Contentieux'),('courrier1', 'Courrier (Lettre Simple)'),('courrier2', 'Courrier LRAR (Lettre Récommandée avec Accusé de Réception'),('courrier3', 'Courrier RE (Courrier Récommandé Electronique'),('email', 'Email'),('fax', 'Fax'),('sms', 'SMS'),('telephone', 'Téléphone'))
StatutAction  =  ((1, 'En cours'),(2, 'fermé'))


class Model_Scenario_relance(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_scenario_relance_bye', null = True, blank = True)

	def __str__(self):
		return self.designation


	class Meta:
		verbose_name = 'Scénario de relance'
		verbose_name_plural = 'Scénarios de relance'
		db_table = 'scenario_relance'


class Model_Action_scenario(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	nb_jours    =    models.IntegerField(choices = ChoixNbJours, verbose_name = "Nombre de jours" )
	type_action    =    models.CharField(choices = ChoixTypeAction, max_length = 250, verbose_name = "Type action" )
	scenario    =    models.ForeignKey("Model_Scenario_relance", null = True, blank = True, related_name = "action_scenarios_scenario", on_delete=models.CASCADE, verbose_name = "Scénarios de relance" )
	est_automatique    =    models.BooleanField(default = False, null = True, blank = True, verbose_name = "Relance automatique" )
	description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description" )
	sujet    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Sujet" )
	message    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Message" )
	langue    =    models.CharField(max_length = 250, null = True, blank = True, verbose_name = "Langue" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_action_scenario_smi', null = True, blank = True)

	def __str__(self):
		return self.designation


	class Meta:
		verbose_name = 'Action du scénario de relance'
		verbose_name_plural = 'Actions du scénario de relance'
		db_table = 'action_scenario'


	@property
	def value_nb_jours(self):
		if self.nb_jours: return dict(ChoixNbJours)[int(self.nb_jours)]

	@property
	def list_nb_jours(self):
		list = []
		for key, value in ChoixNbJours:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list

	@property
	def value_type_action(self):
		if self.type_action: return dict(ChoixTypeAction)[str(self.type_action)]

	@property
	def list_type_action(self):
		list = []
		for key, value in ChoixTypeAction:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list

class Model_Dossier_recouvrement(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	client    =    models.ForeignKey("ErpBackOffice.Model_Client", related_name = "dossier_recouvrements_client", on_delete=models.CASCADE, verbose_name = "Client" )
	description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_dossier_recouvrement_aiy', null = True, blank = True)

	def __str__(self):
		return self.designation


	class Meta:
		verbose_name = 'Dossier de recouvrement'
		verbose_name_plural = 'Dossiers de recouvrement'
		db_table = 'dossier_recouvrement'

class Model_Action_relance(models.Model):
	designation    =    models.CharField(max_length = 100, verbose_name = "Désignation" )
	date_action    =    models.DateField(verbose_name = "Date de l'action" )
	montant_action    =    models.FloatField(null = True, blank = True, verbose_name = "Montant de l'action" )
	type_action    =    models.CharField(choices = ChoixTypeAction, max_length = 250, default="email", verbose_name = "Type action" )
	observation    =    models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Observation" )
	statut_action    =    models.IntegerField(choices = StatutAction, verbose_name = "Statut de l'action" )
	dossier_recouvrement    =    models.ForeignKey("Model_Dossier_recouvrement", related_name = "action_relances_dossier_recouvrement", on_delete=models.CASCADE, verbose_name = "Dossier recouvremnet" )
	facture    =    models.ForeignKey("ErpBackOffice.Model_Facture", related_name = "action_relances_facture", on_delete=models.CASCADE, verbose_name = "Facture" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_action_relance_jwv', null = True, blank = True)

	def __str__(self):
		return self.designation


	class Meta:
		verbose_name = 'Relance'
		verbose_name_plural = 'Relances'
		db_table = 'action_relance'


	@property
	def value_statut_action(self):
		if self.statut_action: return dict(StatutAction)[int(self.statut_action)]

	@property
	def list_statut_action(self):
		list = []
		for key, value in StatutAction:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list

	@property
	def value_type_action(self):
		if self.type_action: return dict(ChoixTypeAction)[str(self.type_action)]

	@property
	def list_type_action(self):
		list = []
		for key, value in ChoixTypeAction:
			item = {'id' : key,'designation' : value}
			list.append(item)
		return list

class Model_Secteur_activite(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_secteur_activite_aiy', null = True, blank = True)

	def __str__(self):
		return self.designation


	class Meta:
		verbose_name = 'Secteur Activité'
		verbose_name_plural = 'Secteurs Activité'
		db_table = 'secteur_activite'
  
class Model_Profil_recouvrement(models.Model):
	designation    =    models.CharField(max_length = 250, verbose_name = "Désignation" )
	description    =    models.CharField(max_length = 510, null = True, blank = True, verbose_name = "Description" )
	statut    =    models.ForeignKey('ErpBackOffice.Model_Wkf_Etape', on_delete=models.SET_NULL, blank=True, null=True)
	etat    =    models.CharField(max_length=50, blank=True, null=True)
	creation_date    =    models.DateTimeField(auto_now_add = True)
	update_date    =    models.DateTimeField(auto_now = True)
	auteur    =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name = 'auteur_de_model_profil_recouvrement_aiy', null = True, blank = True)

	def __str__(self):
		return self.designation

	class Meta:
		verbose_name = 'Profil recouvrement'
		verbose_name_plural = 'Profils recouvrement'
		db_table = 'profil_recouvrement'
