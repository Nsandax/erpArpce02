from __future__ import unicode_literals
from ErpBackOffice.models import Model_Config_Comptabilite
from django.utils import timezone

class dao_config_comptabilite(object):
	annee_fiscale_id    =    None
	societe_configure   =    False
	tresorerie_configure=    False
	periode_configure   =    False
	compte_configure   =    False
	est_active          =    False
	est_ajour           =    False
	digit_compte        =    6
	auteur_id           =    None

	@staticmethod
	def toListConfigComptabilite():
		return Model_Config_Comptabilite.objects.all().order_by('-id')

	@staticmethod
	def toCreateConfigComptabilite(annee_fiscale_id = None, societe_configure = False, tresorerie_configure = False, periode_configure = False, compte_configure = True, est_active = True, est_ajour = False, digit_compte = 6):
		try:
			config_comptabilite = dao_config_comptabilite()
			config_comptabilite.annee_fiscale_id = annee_fiscale_id
			config_comptabilite.societe_configure = societe_configure
			config_comptabilite.tresorerie_configure = tresorerie_configure
			config_comptabilite.periode_configure = periode_configure
			config_comptabilite.compte_configure = compte_configure
			config_comptabilite.est_active = est_active
			config_comptabilite.est_ajour = est_ajour
			return config_comptabilite
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA CONFIGURATION')
			#print(e)
			return None

	@staticmethod
	def toSaveConfigComptabilite(auteur, objet_dao_config_comptabilite):
		try:
			config_comptabilite  = Model_Config_Comptabilite()
			config_comptabilite.annee_fiscale_id = objet_dao_config_comptabilite.annee_fiscale_id
			config_comptabilite.societe_configure = objet_dao_config_comptabilite.societe_configure
			config_comptabilite.tresorerie_configure = objet_dao_config_comptabilite.tresorerie_configure
			config_comptabilite.periode_configure = objet_dao_config_comptabilite.periode_configure
			config_comptabilite.compte_configure = objet_dao_config_comptabilite.compte_configure
			config_comptabilite.est_active = objet_dao_config_comptabilite.est_active
			config_comptabilite.est_ajour = objet_dao_config_comptabilite.est_ajour
			config_comptabilite.auteur_id = auteur.id

			config_comptabilite.save()
			return config_comptabilite
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA Config Comptabilite')
			#print(e)
			return None

	@staticmethod
	def toUpdateConfigComptabilite(id, objet_dao_config_comptabilite):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk = id)
			config_comptabilite.annee_fiscale_id = objet_dao_config_comptabilite.annee_fiscale_id
			config_comptabilite.societe_configure = objet_dao_config_comptabilite.societe_configure
			config_comptabilite.tresorerie_configure = objet_dao_config_comptabilite.tresorerie_configure
			config_comptabilite.periode_configure = objet_dao_config_comptabilite.periode_configure
			config_comptabilite.compte_configure = objet_dao_config_comptabilite.compte_configure
			config_comptabilite.est_active = objet_dao_config_comptabilite.est_active
			config_comptabilite.est_ajour = objet_dao_config_comptabilite.est_ajour
			config_comptabilite.save()
			return config_comptabilite
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA Config Comptabilite')
			#print(e)
			return None
	@staticmethod
	def toGetConfigComptabilite(id):
		try:
			return Model_Config_Comptabilite.objects.get(pk = id)
		except Exception as e:
			return None

	@staticmethod
	def toGetConfigComptabiliteActive():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			return config
		except Exception as e:
			return None

	@staticmethod
	def toGetDigitCompte():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			digit = config.digit_compte
			return digit
		except Exception as e:
			return 6

	@staticmethod
	def estAjour():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			#print("config existe {}".format(config.id))
			return config.est_ajour
		except Exception as e:
			return False

	@staticmethod
	def societeEstAjour():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			#print("config existe {}".format(config.id))
			return config.societe_configure
		except Exception as e:
			return False

	@staticmethod
	def tresorerieEstAjour():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			#print("config existe {}".format(config.id))
			return config.tresorerie_configure
		except Exception as e:
			return False

	@staticmethod
	def periodeEstAjour():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			#print("config existe {}".format(config.id))
			return config.periode_configure
		except Exception as e:
			return False

	@staticmethod
	def compteEstAjour():
		try:
			config = Model_Config_Comptabilite.objects.filter(est_active = True).last()
			#print("config existe {}".format(config.id))
			return config.compte_configure
		except Exception as e:
			return False

	@staticmethod
	def toSetConfigComptabiliteActive(id):
		try:
			Model_Config_Comptabilite.objects.all().update(est_active = False)
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk=id)
			config_comptabilite.est_active = True
			config_comptabilite.save()
		except Exception as e:
			return None

	@staticmethod
	def toSetConfigComptabiliteAjour(id):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk=id)
			config_comptabilite.est_ajour = True
			config_comptabilite.save()
		except Exception as e:
			return None

	@staticmethod
	def toSetConfigSocieteConfigure(id):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk=id)
			config_comptabilite.societe_configure = True
			config_comptabilite.save()
		except Exception as e:
			return None

	@staticmethod
	def toSetConfigTresorerieConfigure(id):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk=id)
			config_comptabilite.tresorerie_configure = True
			config_comptabilite.save()
		except Exception as e:
			return None

	@staticmethod
	def toSetConfigPeriodeConfigure(id):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk=id)
			config_comptabilite.periode_configure = True
			config_comptabilite.save()
		except Exception as e:
			return None

	@staticmethod
	def toSetConfigCompteConfigure(id):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk=id)
			config_comptabilite.compte_configure = True
			config_comptabilite.save()
		except Exception as e:
			return None

	@staticmethod
	def toDeleteConfigComptabilite(id):
		try:
			config_comptabilite = Model_Config_Comptabilite.objects.get(pk = id)
			config_comptabilite.delete()
			return True
		except Exception as e:
			return False