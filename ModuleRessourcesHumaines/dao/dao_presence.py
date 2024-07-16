from __future__ import unicode_literals
from ErpBackOffice.models import Model_Presence
from django.utils import timezone

class dao_presence(object):
	id = 0
	employe_id = None
	unite_fonctionelle_id = None
	arrive = '2010-01-01'
	depart = '2010-01-01'

	@staticmethod
	def toListPresence():
		return Model_Presence.objects.all().order_by('-id')

	@staticmethod
	def toCreatePresence(employe_id,unite_fonctionelle_id,date,arrive,depart):
		try:
			presence = dao_presence()
			presence.employe_id = employe_id
			presence.unite_fonctionelle_id = unite_fonctionelle_id
			presence.date  = date
			presence.arrive = arrive
			presence.depart = depart
			return presence
		except Exception as e:
			#print('ERREUR LORS DE LA CREATION DE LA PRESENCE')
			#print(e)
			return None

	@staticmethod
	def toSavePresence(auteur, objet_dao_Presence):
		try:
			presence  = Model_Presence()
			presence.employe_id = objet_dao_Presence.employe_id
			presence.unite_fonctionelle_id = objet_dao_Presence.unite_fonctionelle_id
			presence.date = objet_dao_Presence.date
			presence.arrive = objet_dao_Presence.arrive
			presence.depart = objet_dao_Presence.depart
			presence.created_at = timezone.now()
			presence.updated_at = timezone.now()
			presence.auteur_id = auteur.id

			presence.save()
			return presence
		except Exception as e:
			#print('ERREUR LORS DE L ENREGISTREMENT DE LA PRESENCE')
			#print(e)
			return None

	@staticmethod
	def toUpdatePresence(id, objet_dao_Presence):
		try:
			presence = Model_Presence.objects.get(pk = id)
			presence.employe_id =objet_dao_Presence.employe_id
			presence.unite_fonctionelle_id =objet_dao_Presence.unite_fonctionelle_id
			presence.date = objet_dao_Presence.date
			presence.arrive =objet_dao_Presence.arrive
			presence.depart =objet_dao_Presence.depart
			presence.updated_at = timezone.now()
			presence.save()
			return presence
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA PRESENCE')
			#print(e)
			return None
	@staticmethod
	def toGetPresence(id):
		try:
			return Model_Presence.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toGetPresenceOfEmploye(id):
		try:
			return Model_Presence.objects.filter(employe_id = id).order_by('-created_at')
		except Exception as e:
			return None
	@staticmethod
	def toDeletePresence(id):
		try:
			presence = Model_Presence.objects.get(pk = id)
			presence.delete()
			return True
		except Exception as e:
			return False