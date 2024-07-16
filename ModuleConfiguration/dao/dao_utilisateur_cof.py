from __future__ import unicode_literals
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session



class dao_utilisateur_cof(object):

    @staticmethod
    def toGetNombre():
            try:
                #print(' toGetNombre')

                Nombre = User.objects.all().order_by('-id')

                return Nombre
            except Exception as e:
                #print("ERRER LISTECONGE BY toGetNombre Dao")
                #print(e)
                pass

    # recuperer les utilisateur connectés
    @staticmethod
    def get_current_users():
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
        return User.objects.filter(id__in=user_id_list)
