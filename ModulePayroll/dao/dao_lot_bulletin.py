# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ErpBackOffice.models import Model_LotBulletins
from django.utils import timezone
from datetime import datetime
from ModulePayroll.dao.dao_dossier_paie import dao_dossier_paie
from ErpBackOffice.models import Model_DossierPaie

class dao_lot_bulletin(object):
    id = 0
    designation = ""
    reference = ""
    type = ""
    auteur_id = 0
    departement_id = 0
    date_dossier = None
    dossier_paie_id = None


    @staticmethod
    def toList():
        return Model_LotBulletins.objects.all().order_by("-dossier_paie")

    @staticmethod
    def toListSoumis():
        return Model_LotBulletins.objects.filter(est_soumis = True).order_by("designation")

    @staticmethod
    def toListValide():
        return Model_LotBulletins.objects.filter(est_valide = True).order_by("designation")

    @staticmethod
    def toCreate(auteur_id, designation, departement_id, type = "", reference = "", date_dossier = None, date_debut = None, date_fin = None, dossier_paie_id = None, est_regulier = False):
        try:
            lot_bulletin = dao_lot_bulletin()
            lot_bulletin.auteur_id = auteur_id
            lot_bulletin.designation = designation
            if reference == None or reference == "": reference = dao_lot_bulletin.toGenerateNumero()
            lot_bulletin.reference = reference
            lot_bulletin.type = type
            lot_bulletin.departement_id = departement_id
            lot_bulletin.date_dossier = date_dossier
            lot_bulletin.date_debut = date_debut
            lot_bulletin.date_fin = date_fin
            lot_bulletin.dossier_paie_id = dossier_paie_id
            lot_bulletin.est_regulier = est_regulier
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION")
            #print(e)
            return None

    @staticmethod
    def toSave(dao_lot_bulletin_object):
        try:
            lot_bulletin = Model_LotBulletins()
            lot_bulletin.designation = dao_lot_bulletin_object.designation
            lot_bulletin.auteur_id = dao_lot_bulletin_object.auteur_id
            lot_bulletin.reference = dao_lot_bulletin_object.reference
            lot_bulletin.type = dao_lot_bulletin_object.type
            lot_bulletin.departement_id = dao_lot_bulletin_object.departement_id
            lot_bulletin.creation_date = timezone.now()
            lot_bulletin.date_dossier = dao_lot_bulletin_object.date_dossier
            lot_bulletin.dossier_paie_id = dao_lot_bulletin_object.dossier_paie_id
            lot_bulletin.est_regulier = dao_lot_bulletin_object.est_regulier
            lot_bulletin.save()
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None


    @staticmethod
    def toUpdate(id, dao_lot_bulletin_object):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            lot_bulletin.designation = dao_lot_bulletin_object.designation
            lot_bulletin.reference = dao_lot_bulletin_object.reference
            lot_bulletin.type = dao_lot_bulletin_object.type
            lot_bulletin.departement_id = dao_lot_bulletin_object.departement_id
            lot_bulletin.date_dossier = dao_lot_bulletin_object.date_dossier
            lot_bulletin.dossier_paie_id = dao_lot_bulletin_object.dossier_paie_id
            lot_bulletin.est_regulier = dao_lot_bulletin_object.est_regulier
            lot_bulletin.save()
            return True, lot_bulletin
        except Exception as e:
            print("ERREUR LORS DE MISE A JOUR")
            print(e)
            return False, None


    @staticmethod
    def toDelete(dao_lot_bulletin_object):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = dao_lot_bulletin_object.id)
            lot_bulletin.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DE LA SUPPRESSION")
            #print(e)
            return False


    @staticmethod
    def toGet(id):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None
    @staticmethod
    def toListLotBulletinFromDossierPaie(dossier_paie_id):
        try:
            lot_bulletin = Model_LotBulletins.objects.filter(dossier_paie_id = dossier_paie_id)
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toSetLotBulletinActifOfDossierPaie(lot_bulletin_id):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = lot_bulletin_id)
            #Initialize the status of all other lot bulletin
            Model_LotBulletins.objects.filter(dossier_paie_id = lot_bulletin.dossier_paie_id).update(est_soumis = True, est_valide = True)
            lot_bulletin.est_soumis = True
            lot_bulletin.est_valide = True
            return lot_bulletin
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetLotBulletinSoumisFromDossierPaie(dossier_paie_id):
        try:
            return Model_LotBulletins.objects.filter(dossier_paie_id = dossier_paie_id, est_soumis = True, est_valide = True).first()
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetLotRegulierFromDossierPaie(dossier_paie_id):
        try:
            return Model_LotBulletins.objects.filter(dossier_paie_id = dossier_paie_id, est_regulier = True).first()
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toGetMois(id):
        try:
            mois = ""
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            date_du_mois = lot_bulletin.creation_date
            if lot_bulletin.date_dossier != None : date_du_mois = lot_bulletin.date_dossier
            mois = lot_bulletin.date_dossier.strftime("%B")
            return mois
        except Exception as e:
            #print("ERREUR LORS DU L'AFFICHAGE")
            #print(e)
            return None

    @staticmethod
    def toSoumetre(id):
        try:
            lot_bulletin = Model_LotBulletins.objects.get(pk = id)
            lot_bulletin.est_soumis = True
            lot_bulletin.save()
            return lot_bulletin
        except Exception as e:
            #print("ERREUR toSoumetre(id)")
            #print(e)
            return None

    @staticmethod
    def toGenerateNumero():
        total = dao_lot_bulletin.toList().count()
        total = total + 1
        temp_numero = str(total)

        for i in range(len(str(total)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois

        temp_numero = "DOS-PAY-%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero

    @staticmethod
    def toGetOrderMax():
        try:
            max = dao_lot_bulletin.toList().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None

    @staticmethod
    def toGetOrCreatelotbyperiode(auteur,date_doc, est_regulier = True):
        try:
            date_dossier = date_doc
            # chaine = date_doc
            # date_ ='{0}'.format(date_dossier)
            # print('DATE RECUPERER', date_dossier)
            # date_fin = datetime.strptime(date_, '%Y-%m-%d %H:%M:%S')
            date_debut = date_dossier.replace(day=1)
            date_fin = date_dossier

            # print("Date Debut {} ::: Date Fin {}".format(date_debut, date_fin))

            mois = date_fin.month
            annee = date_fin.year
            lot = Model_LotBulletins.objects.filter(date_fin__month=mois,date_fin__year=annee,est_regulier=est_regulier).first()
            # print(lot)
            if lot == None:
                lotbulletin = dao_lot_bulletin()
                if est_regulier == True: designation = 'Bulletins de paie {0} {1}'.format(mois, annee)
                else: designation = 'Bulletins 13e mois {0} {1}'.format(mois, annee)
                reference = dao_lot_bulletin.toGenerateNumero()
                type = "TOUS"
                typeModele = 1
                periode = 0

                # ~Creation du periode de paie
                # print('Creation du periode de paie')
                month = int(mois)
                year = str(annee)
                # print('month {} :: Year {}'.format(month, year))
                dossierpaie = Model_DossierPaie.objects.filter(mois = month, annee=year).first()
                if dossierpaie:
                    periode = dossierpaie.id
                    # print('periode {} ::'.format(periode))
                else:
                    dossier_paie  = Model_DossierPaie()
                    dossier_paie.mois   =  month
                    dossier_paie.annee  =  year
                    dossier_paie.est_cloture   =  True
                    dossier_paie.est_calcul  =  True
                    dossier_paie.save()

                    periode = dossier_paie.id
                    # print("Periode Paie cree ID {} {}".format(dossier_paie.mois, dossier_paie.annee))



                # Enregistrement de Lot de Bulletin
                lot = lotbulletin.toCreate(auteur,designation,None,type,reference,date_dossier,periode,False)
                lot = lotbulletin.toSave(lot)
                lot.date_debut = date_debut
                lot.date_fin = date_fin
                lot.est_regulier = est_regulier
                lot.est_soumis = True
                lot.est_valide = True
                lot.dossier_paie_id = periode
                lot.save()
                # print("Lot Bulletin cree ID {}".format(lot.id))
            return lot
        except Exception as e:
            print("Error toGetOrCreateLotBulletin", e)
            return None