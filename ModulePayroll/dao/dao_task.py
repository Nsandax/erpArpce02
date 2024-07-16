from __future__ import unicode_literals

from django.utils import timezone
from ModulePayroll.tasks import add, do_work, mul, toCalculPaiewithoutRedis
from ModulePayroll.dao.dao_lot_bulletin import dao_lot_bulletin
# from ModulePayroll.views import *
from ModulePayroll.dao.dao_dossier_paie import dao_dossier_paie
# from ./ import views


class dao_task(object):

	@staticmethod
	def toProcessCalculPaie(auteur_id, lot_bulletin_id, employes,dossier_paie_id):
		try:
			#return mul(5,6)
			return do_work.delay(auteur_id, lot_bulletin_id, employes, dossier_paie_id)
			#return toCalculPaiewithoutRedis(auteur_id, lot_bulletin_id, employes, dossier_paie_id)
		except Exception as e:
			print("ERREUR DU toProcessCalculPaie")
			print(e)
			return None