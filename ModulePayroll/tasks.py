import random
from celery import shared_task
from ModulePayroll.dao.dao_dossier_paie import dao_dossier_paie
from . import views
#from ModulePayroll.views import calcul_paie

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y

@shared_task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@shared_task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)


@shared_task
def do_work(auteur_id, lot_bulletin_id, employes, dossier_paie_id):
    #print("******************************************************")
    total_work_to_do = len(employes) #len(list_of_work)
    i = 0

    for employe in employes:
        views.calcul_paie(employe['employe_id'], lot_bulletin_id, auteur_id)
        #dao_dossier_paie.toProceedCalculPaie(employe['employe_id'], lot_bulletin_id, auteur_id)
        do_work.update_state(
            state="EN COURS",
            meta={
                'current': i,
                'total': total_work_to_do,
            }
        )
        i += 1
        #print("i",i)
    dao_dossier_paie.toSetCalculateDossierPaie(dossier_paie_id)

    return "Effectué avec succès"


def toCalculPaiewithoutRedis(auteur_id, lot_bulletin_id, employes, dossier_paie_id):
    try:
        print("******************************************************")
        total_work_to_do = len(employes)
        print(f"total Employe{total_work_to_do}")
        # i = 0
        #Calcul de bulletin one by one
        for employe in employes:
            print('employe:', employe)
            views.calcul_paie(employe['employe_id'], lot_bulletin_id, auteur_id)
            print(f'***Task calcul Bulletin Yes***')

        dao_dossier_paie.toSetCalculateDossierPaie(dossier_paie_id)
        return "Effectué avec succès"
    except Exception as e:
        print('ERREUR toCalculPaiewithoutRedis')
        print(e)
        return None
