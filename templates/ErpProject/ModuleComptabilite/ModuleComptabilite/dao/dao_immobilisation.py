from __future__ import unicode_literals
from django.utils import timezone
from ErpBackOffice.models import Model_Immobilisation, Model_Ligne_Immobilisation
from ModuleComptabilite.dao.dao_piece_comptable import dao_piece_comptable
from ModuleComptabilite.dao.dao_ecriture_comptable import dao_ecriture_comptable
from datetime import datetime
from dateutil import relativedelta



class dao_immobilisation:
    id = 0
    code = ""
    immobilier_id = None
    taux_amortissement = 1
    valeur_immobilier = 0
    date_acquisition = None
    auteur_id = None
    compte_dotation_id = None
    compte_depreciation_id = None
    compte_immobilier_id = None
    coefficient = 0
    type_amortissement = 1
    duree_amortissement = 0
    local_id = None

    @staticmethod
    def toCreate(code, immobilier_id, date_acquisition, taux_amortissement, valeur_immobilier, duree_amortissement, coefficient = 0 , type_amortissement = 1,compte_dotation_id = None, compte_depreciation_id = None, compte_immobilier_id = None, local_id = None):
        try:
            immobilisation = dao_immobilisation()
            immobilisation.code = code
            immobilisation.immobilier_id = immobilier_id
            immobilisation.taux_amortissement = taux_amortissement
            immobilisation.valeur_immobilier = valeur_immobilier
            immobilisation.date_acquisition = date_acquisition
            immobilisation.duree_amortissement = duree_amortissement
            immobilisation.type_amortissement = type_amortissement
            immobilisation.coefficient = coefficient
            immobilisation.compte_dotation_id = compte_dotation_id
            immobilisation.compte_depreciation_id  = compte_depreciation_id
            immobilisation.compte_immobilier_id = compte_immobilier_id
            immobilisation.local_id = local_id
            return immobilisation
        except Exception as e:
            #print("ERREUR LORS DU CREATE")
            #print(e)
            return None

    @staticmethod
    def toSave(auteur, objet_dao):
        try:
            immobilisation = Model_Immobilisation()
            immobilisation.code = objet_dao.code
            #print("SAVE IMMO 0", objet_dao.code)
            immobilisation.immobilier_id = objet_dao.immobilier_id
            #print("SAVE IMMO 1", objet_dao.immobilier_id)
            immobilisation.taux_amortissement = objet_dao.taux_amortissement
            immobilisation.valeur_immobilier = objet_dao.valeur_immobilier
            immobilisation.date_acquisition = objet_dao.date_acquisition
            immobilisation.coefficient = objet_dao.coefficient
            #print("SAVE IMMO 2", objet_dao.coefficient, objet_dao.valeur_immobilier)
            immobilisation.duree_amortissement = objet_dao.duree_amortissement
            immobilisation.type_amortissement = objet_dao.type_amortissement
            immobilisation.compte_depreciation_id = objet_dao.compte_depreciation_id
            immobilisation.compte_dotation_id  =objet_dao.compte_dotation_id
            #print("SAVE IMMO 3", objet_dao.compte_dotation_id)
            immobilisation.compte_immobilier_id = objet_dao.compte_immobilier_id
            immobilisation.local_id = objet_dao.local_id
            immobilisation.date_creation = timezone.now()
            #print("SAVE IMMO 4", objet_dao.local_id)
            Auteur = auteur.id
            if Auteur:
                immobilisation.auteur_id = auteur.id
            else: immobilisation.auteur_id = None
            #print("SAVE IMMO 5", auteur.id)
            immobilisation.save()
            return immobilisation
        except Exception as e:
            #print("ERREUR LORS DU SAVE")
            #print(e)
            return None

    @staticmethod
    def toUpdate(id, objet_dao):
        try:
            immobilisation = Model_Immobilisation.objects.get(pk=id)
            immobilisation.code = objet_dao.code
            immobilisation.taux_amortissement = objet_dao.taux_amortissement
            immobilisation.valeur_immobilier = objet_dao.valeur_immobilier
            immobilisation.local_id = objet_dao.local_id
            immobilisation.save()
            return True
        except Exception as e:
            #print("ERREUR LORS DU UPDATE")
            #print(e)
            return False

    @staticmethod
    def toDelete(id):
        try:
            immobilisation = Model_Immobilisation.objects.get(pk=id)
            immobilisation.delete()
            return True
        except Exception as e:
            #print("ERREUR LORS DU DELETE")
            #print(e)
            return False

    @staticmethod
    def toListImmobilisationAvailableAndComptabilise():
        try:
            return Model_Immobilisation.objects.filter(is_available = True).filter(est_comptabilise = True).order_by("date_acquisition")
        except Exception as e:
            ##print("ERREUR LORS DU SELECT")
            ##print(e)
            return []

    @staticmethod
    def toList():
        try:
            return Model_Immobilisation.objects.all().order_by("date_acquisition")
        except Exception as e:
            ##print("ERREUR LORS DU SELECT")
            ##print(e)
            return []

    @staticmethod
    def toListLigneAmortissement(immobilisation_id):
        try:
            return Model_Ligne_Immobilisation.objects.filter(immobilisation_id = immobilisation_id)
        except Exception as e:
            ##print("ERREUR LORS DU SELECT")
            ##print(e)
            return []

    @staticmethod
    def toGet(id):
        try:
            return Model_Immobilisation.objects.get(pk=id)
        except Exception as e:
            ##print("ERREUR LORS DU GET")
            ##print(e)
            return None

    @staticmethod
    def toSetImmobilisationNonAvailable(id):
        try:
            immobilisation = Model_Immobilisation.objects.get(pk=id)
            immobilisation.is_available = False
            immobilisation.save()
            return True
        except Exception as e:
            return False
    @staticmethod
    def toSetImmobilisationComptabilise(id):
        try:
            immobilisation = Model_Immobilisation.objects.get(pk=id)
            immobilisation.est_comptabilise = True
            immobilisation.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toWriteDotationAmortissement(auteur):
        #Fonction permettant de passer les écritures de dotations à la fin de l'année

        #recuperation des immobilisations n'ayant pas encore été cedé ou mis au rebut
        immobilisations = Model_Immobilisation.objects.filter(is_available = True)

        #Debut de traitement sur chaque Immo
        for immobilisation in immobilisations:

            annee_courante = timezone.now().year
            annee_acquisition = immobilisation.date_acquisition.year


            #recuperation de la dernière ligne d'amortissement
            ligne = Model_Ligne_Immobilisation.objects.filter(immobilisation = immobilisation).order_by("-date_amortissement").first()

            #Si une ligne d'amortissement précedente existe
            if ligne :
                #Amortissement précédent existe so!
                #Si type amortissement est linéaire
                if immobilisation.type_amortissement == 1:
                    delta = timezone.now() - ligne.date_amortissement
                    if delta.days >= 360:
                        valeur_dotation = immobilisation.valeur_immobilier * immobilisation.taux_amortissement
                    else:
                        valeur_dotation = immobilisation.valeur_immobilier * immobilisation.taux_amortissement * delta.days / 36000


                    cumulation = ligne.cumul + valeur_dotation
                    valeur_residuelle = immobilisation.valeur_immobilier - cumulation



                    Model_Ligne_Immobilisation.objects.create(
                        annee = annee_courante,
                        base_amortissement = immobilisation.valeur_immobilier,
                        dotation = valeur_dotation,
                        cumul = cumulation,
                        valeur_residuelle = valeur_residuelle,
                        immobilisation = immobilisation,
                        date_amortissement = timezone.now()
                        )
                elif immobilisation.type_amortissement == 2 :
                    delta = timezone.now() - ligne.date_amortissement
                    rdelta = relativedelta.relativedelta(timezone.now(), immobilisation.date_acquisition)
                    nombre_mois = rdelta.months
                    if rdelta.days > 0 : nombre_mois += 1

                    #comparaison native entre taux lineaire et taux degressif afin de trouver le taux à appliquer
                    gap_year = int(annee_courante) - int(annee_acquisition)
                    if gap_year == 0:
                        gap_year = immobilisation.duree_amortissement
                    else:
                        gap_year = immobilisation.duree_amortissement - gap_year

                    taux_lineaire = 100 / gap_year #Le taux linéaire est fonction de la duree d'amortissement en fonction des années restantes!
                    taux_degressif = immobilisation.taux_amortissement
                    taux_applique = taux_degressif if taux_degressif >= taux_lineaire else taux_lineaire

                    if delta.days >= 360:
                        valeur_dotation = ligne.base_amortissement * taux_applique
                    else:
                        valeur_dotation = ligne.base_amortissement * taux_applique * nombre_mois / 12


                    cumulation = ligne.cumul + valeur_dotation
                    valeur_residuelle = immobilisation.valeur_immobilier - cumulation
                    valeur_base_amortissement = ligne.base_amortissement - valeur_dotation

                    Model_Ligne_Immobilisation.objects.create(
                        annee = annee_courante,
                        base_amortissement = valeur_base_amortissement,
                        dotation = valeur_dotation,
                        cumul = cumulation,
                        valeur_residuelle = valeur_residuelle,
                        immobilisation = immobilisation,
                        date_amortissement = timezone.now()
                        )
            #Si aucune ligne n'existe, il s'agit de la première écriture d'amortissement
            else:
                #1ère écriture de Dotation so
                #Si type_amortissement est linéaire, le calcul de l'immobilisation se fait sur base du
                #de la date d'acquisition. Il faudrait donc calculer le nombre de jour entre la date d'acquisition et le jour du passage des ecritures
                if immobilisation.type_amortissement == 1:
                    delta = timezone.now() - immobilisation.date_acquisition
                    valeur_dotation = immobilisation.valeur_immobilier * immobilisation.taux_amortissement * delta.days / 36000
                    cumulation = valeur_dotation
                    valeur_residuelle = immobilisation.valeur_immobilier - cumulation
                    Model_Ligne_Immobilisation.objects.create(
                        annee = annee_courante,
                        base_amortissement = immobilisation.valeur_immobilier,
                        dotation = valeur_dotation,
                        cumul = cumulation,
                        valeur_residuelle = valeur_residuelle,
                        immobilisation = immobilisation,
                        date_amortissement = timezone.now()
                        )


                #Si type amortissement est degressif, l'amortissement est en MOIS entier et le point de depart est le 1er jour du mois d'achat
                elif immobilisation.type_amortissement == 2:
                    #calcul du nombre de mois entre les deux dates
                    rdelta = relativedelta.relativedelta(timezone.now(), immobilisation.date_acquisition)
                    nombre_mois = rdelta.months
                    if rdelta.days > 0 : nombre_mois += 1

                    #comparaison native entre taux lineaire et taux degressif afin de trouver le taux à appliquer
                    taux_lineaire = 100 / immobilisation.duree_amortissement
                    taux_degressif = immobilisation.taux_amortissement
                    taux_applique = taux_degressif if taux_degressif >= taux_lineaire else taux_lineaire

                    valeur_dotation = immobilisation.valeur_immobilier * taux_applique * nombre_mois / 12
                    cumulation = valeur_dotation
                    valeur_residuelle = immobilisation.valeur_immobilier - cumulation

                    Model_Ligne_Immobilisation.objects.create(
                        annee = annee_courante,
                        base_amortissement = immobilisation.valeur_immobilier,
                        dotation = valeur_dotation,
                        cumul = cumulation,
                        valeur_residuelle = valeur_residuelle,
                        immobilisation = immobilisation,
                        date_amortissement = timezone.now()
                        )


            ####################Ecritures Comptables###################
            texte = "Amortissement Année " + str(annee_courante) + " - " + str(immobilisation.immobilier.numero_identification) + " / " + immobilisation.immobilier.article.designation
            ref = "AMO" + str(annee_courante) + "" + str(immobilisation.immobilier.numero_identification)
            piece = dao_piece_comptable.toCreatePieceComptable(texte,ref,valeur_dotation,immobilisation.journal_id,timezone.now(),immobilisation.immobilier.bon_reception.fournisseur_id,None,immobilisation.immobilier.bon_reception_id,None,"",immobilisation.journal.devise_id, None)
            piece = dao_piece_comptable.toSavePieceComptable(auteur.id,piece)

            #Dotation
            ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(immobilisation.compte_dotation.designation,valeur_dotation,0,immobilisation.compte_dotation_id,piece.id)
            ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)

            #Depreciation
            ecriture_comptable = dao_ecriture_comptable.toCreateEcritureComptable(immobilisation.compte_depreciation.designation, 0, valeur_dotation, immobilisation.compte_depreciation_id,piece.id)
            ecriture_comptable = dao_ecriture_comptable.toSaveEcritureComptable(ecriture_comptable)


    @staticmethod
    def toGenerateNumeroImmo():
        total_immo = Model_Immobilisation.objects.all().count()
        total_immo = total_immo + 1
        temp_numero = str(total_immo)

        for i in range(len(str(total_immo)), 4):temp_numero = "0" + temp_numero

        sampleDate = datetime.now()
        dateFormatted = sampleDate.strftime("%y")

        temp_numero = "IMMO-%s-%s" % (temp_numero, dateFormatted)
        return temp_numero




