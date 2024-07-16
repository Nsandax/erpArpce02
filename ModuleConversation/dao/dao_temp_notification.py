from __future__ import unicode_literals
from ErpBackOffice.models import Model_Temp_Notification
from django.utils import timezone

class dao_temp_notification(object):
	id = 0
	user_id = None
	notification_id = None
	est_lu = False

	@staticmethod
	def toListTempNotification():
		return Model_Temp_Notification.objects.all().order_by('-id')


	@staticmethod
	def toGetTempNotification(id):
		try:
			return Model_Temp_Notification.objects.get(pk = id)
		except Exception as e:
			return None
	@staticmethod
	def toDeleteTempNotification(id):
		try:
			notification = Model_Temp_Notification.objects.get(pk = id)
			notification.delete()
			return True
		except Exception as e:
			return False
	#NOTIF FROM MESSAGES
	@staticmethod
	def toCountTempNotificationUnread(user_id,):
		try:
			notif = Model_Temp_Notification.objects.filter(user_id = user_id).filter(est_lu = False)
			return notif.count()
		except Exception as e:
			return None
	@staticmethod
	def toGetListTempNotificationUnread(user_id, module_name):
		try:
			LesNotifs = Model_Temp_Notification.objects.filter(user_id = user_id).filter(notification__module_source = module_name).filter(est_lu = False).order_by('-created_at')
			# print("**Les Notif**", LesNotifs)
			return LesNotifs
		except Exception as e:
			return None

	@staticmethod
	def toUpdateTempNotificationRead(id):
		try:
			temp_notification = Model_Temp_Notification.objects.get(pk = id)
			temp_notification.est_lu = True
			temp_notification.save()
			return temp_notification
		except Exception as e:
			#print('ERREUR LORS DE LA MODIFICATION DE LA NOTIFICATION')
			#print(e)
			return None