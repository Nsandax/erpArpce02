import sched
import time as time_module
from ErpBackOffice.models import Model_Bon_reception, Model_Notification, Model_Temp_Notification
import datetime
from time import gmtime, strftime
import threading
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone

# scheduler = sched.scheduler(time_module.time, time_module.sleep)
# t = time_module.strptime('2020-01-11 13:36:00', '%Y-%m-%d %H:%M:%S')
# t = time_module.mktime(t)
# scheduler_e = scheduler.enterabs(t, 1, traitement_duree_vie_bc, ())
# scheduler.run()
def action_duree_vie_bc():
    # print('*****DUREE BON DE COMMNADE****')
    return None

def traitement_duree_vie_bc():
	Bons = Model_Bon_reception.objects.filter(is_actif=True)
	scheduler = sched.scheduler(time_module.time, time_module.sleep)
	t = time_module.strptime('2022-03-07 11:18:00', '%Y-%m-%d %H:%M:%S')
	t = time_module.mktime(t)
	while strftime("%Y-%m-%d %H:%M:%S", gmtime()) < str(t):t.sleep(10)
	scheduler_e = scheduler.enterabs(t, 1, action_duree_vie_bc, ())
	scheduler.run()
	# return Bons

# class ThreadingExample(object):
#     """ Threading example class
#     The run() method will be started and it will run in the background
#     until the application exits.
#     """

#     def __init__(self, interval=86400): #86400 Interaval d'un Jour
#         """ Constructor
#         :type interval: int
#         :param interval: Check interval, in seconds
#         """
#         self.interval = interval

#         thread = threading.Thread(target=self.run, args=())
#         thread.daemon = True                            # Daemonize thread
#         thread.start()                                  # Start the execution

#     def run(self):
#         """ Method that runs forever """
#         while True:
#             # Do something
#             # print('Doing something imporant in the background', self.interval)
#             lien_action = 'module_achat_detail_bon_reception'
#             time_add = 0
#             formatcurrencedate = datetime.now()
#             currentdate = formatcurrencedate.strftime('%Y-%m-%d')
#             lesbons = Model_Bon_reception.objects.filter(is_actif=True)
#             for a in lesbons:
#                 # print('num_bon:',a.numero_reception,'user_id:')
#                 texte = "Le bon de commande N° {0} vous est envoyé pour traitement (duree de vie)".format(a.numero_reception)
#                 duree = a.duree
#                 if duree == 1:
#                     time_add = 6
#                 else: time_add = 12
#                 datecreation = a.creation_date
#                 # datecreation = a.date_prevue
#                 # dateAdds = datecreation + timedelta(minutes=int(time_add))
#                 dateAdds = datecreation + relativedelta(months=time_add)
#                 dateAdds = dateAdds.strftime('%Y-%m-%d')
#                 # print('**DANS LE CALCUL D DUREE AJOUTE', dateAdds)
#                 # print("***Currence Date", currentdate)

#                 if dateAdds <= currentdate:
#                     #création de la notification
#                     # print('Dans la creation de notif')
#                     notif = Model_Notification.objects.create(module_source = "MODULE_ACHAT",text=texte,created_at = timezone.now())
#                     #On cree la notification
#                     Model_Temp_Notification.objects.create(user_id=a.auteur_id, type_action = 'Link', lien_action = lien_action, source_identifiant=a.id, notification_id = notif.id, est_lu = False, created_at = timezone.now())
#                     # print('**Notification Créée')
#             time.sleep(self.interval)

# example = ThreadingExample()