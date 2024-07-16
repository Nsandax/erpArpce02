from __future__ import unicode_literals
from ErpBackOffice.models import Model_Expression
from django.db.models import Max
from django.utils import timezone
from django.db.models import Q
from ModuleRessourcesHumaines.dao.dao_unite_fonctionnelle import dao_unite_fonctionnelle
from django.db.models.functions import TruncMonth
from django.db.models import Count


class dao_expression_besoin(object):
    id = 0
    numero_expression = ""
    date_expression = ""
    justification = ""
    demandeur_id = None
    #requete_id = None
    ligne_budgetaire_id = None
    services_ref_id = None
    statut_id = None
    auteur_id = None
    document = ""
    etat = ""
    centre_cout_id = None

    @staticmethod
    def toCreateExpression(numero_expression, date_expression, justification, statut_id, demandeur_id, document, etat,  ligne_budgetaire_id = None, services_ref_id = None,centre_cout_id = None):
        try:
            expression = dao_expression_besoin()
            expression.numero_expression = numero_expression
            expression.date_expression = date_expression
            expression.justification = justification
            expression.statut_id = statut_id
            expression.demandeur_id = demandeur_id
            if ligne_budgetaire_id == '':
                expression.ligne_budgetaire_id = None
            expression.ligne_budgetaire_id = ligne_budgetaire_id
            expression.services_ref_id = services_ref_id
            expression.document = document
            expression.etat = etat
            expression.centre_cout_id = centre_cout_id
            return expression
        except Exception as e:
            #print("ERREUR LORS DE LA CREATION DE ORDRE")
            #print(e)
            return None

    @staticmethod
    def toSaveExpression(auteur, objet_dao_expression_besoin):
        try :
            expression = Model_Expression()
            expression.numero_expression = objet_dao_expression_besoin.numero_expression
            expression.date_expression = objet_dao_expression_besoin.date_expression
            expression.justification = objet_dao_expression_besoin.justification
            expression.statut_id = objet_dao_expression_besoin.statut_id
            expression.demandeur_id = objet_dao_expression_besoin.demandeur_id
            expression.services_ref_id = objet_dao_expression_besoin.services_ref_id
            expression.ligne_budgetaire_id = objet_dao_expression_besoin.ligne_budgetaire_id
            expression.etat = objet_dao_expression_besoin.etat
            expression.centre_cout = objet_dao_expression_besoin.centre_cout_id
            expression.auteur_id = auteur.id
            expression.save()

            return expression
        except Exception as e:
            #print("ERREUR SAVE ORDER")
            #print(e)
            return None

    @staticmethod
    def toUpdateExpression(id, objet_dao_expression_besoin):
        try:
            expression = Model_Expression.objects.get(pk = id)
            expression.date_expression = objet_dao_expression_besoin.date_expression
            expression.justification = objet_dao_expression_besoin.justification
            expression.statut_id = objet_dao_expression_besoin.statut_id
            expression.demandeur_id = objet_dao_expression_besoin.demandeur_id
            expression.ligne_budgetaire_id = objet_dao_expression_besoin.ligne_budgetaire_id
            expression.services_ref_id = objet_dao_expression_besoin.services_ref_id
            expression.centre_cout = objet_dao_expression_besoin.centre_cout_id
            expression.save()
            return True
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return False

    @staticmethod
    def toChangeStatusExpression(id, status):
        try:
            expression = Model_Expression.objects.get(pk = id)
            expression.status = status
            expression.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toGetExpression(id):
        try:
            return Model_Expression.objects.get(pk = id)
        except Exception as e:
            return None


    @staticmethod
    def toGetExpressionMax():
        try:
            #return Model_Expression.objects.all().aggregate(Max('rating'))
            max = Model_Expression.objects.all().count()
            max = max + 1
            return max
        except Exception as e:
            #print("ERREUR")
            #print(e)
            return None


    @staticmethod
    def toDeleteExpression(id):
        try:
            expression = Model_Expression.objects.get(pk = id)
            expression.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def toListExpressions(filtre = None, auteur = None):
        try:
            if not filtre:
                return Model_Expression.objects.all().order_by('-numero_expression')
            else:
                return  eval("Model_Expression.objects." + filtre + ".order_by('-numero_expression')")
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsByAuteur(user_id):
        try:
            demandes = Model_Expression.objects.filter(auteur_id=user_id).order_by('-numero_expression')
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsByServiceRef(services_ref_id):
        try:
            demandes = Model_Expression.objects.filter(services_ref_id = services_ref_id)
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsByServiceRefByAuteur(services_ref_id, user_id):
        try:
            demandes = Model_Expression.objects.filter(services_ref_id = services_ref_id).filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsServiceReferent():
        try:
            demandes = Model_Expression.objects.filter(etat = 'Envoyé au service référent')
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsServiceReferentByAuteur(user_id):
        try:
            demandes = Model_Expression.objects.filter(etat = 'Envoyé au service référent').filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsNonTraites():
        try:
            demandes = Model_Expression.objects.filter(Q(etat = 'Envoyé au service référent')|Q(etat = 'Livré partiellement')|Q(etat="Demande d'achat généré"))
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsNonTraitesByAuteur(user_id):
        try:
            #demandes = Model_Expression.objects.filter(Q(etat = 'Envoyé au service référent')|Q(etat = 'Livré partiellement')|Q(etat="Demande d'achat généré")).filter(auteur_id=user_id)
            demandes = Model_Expression.objects.filter(~Q(etat = 'Créé')&~Q(etat = 'Articles livrés'))
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsNonTraitesByServiceRef(services_ref_id):
        try:
            demandes = Model_Expression.objects.filter(services_ref_id = services_ref_id).filter(~Q(etat = 'Créé')&~Q(etat = 'Articles livrés'))
            return demandes
        except Exception as e:
            return None


    @staticmethod
    def toListExpressionsNonTraitesByServiceRefByAuteur(services_ref_id, user_id):
        try:
            demandes = Model_Expression.objects.filter(services_ref_id = services_ref_id).filter(~Q(etat = 'Créé')&~Q(etat = 'Articles livrés')).filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None


    @staticmethod
    def toListExpressionsNeedDemandeAchat(services_ref_id):
        try:
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(services_ref_id)
            demandes = Model_Expression.objects.filter(services_ref_id = services_ref_id).filter(~Q(etat = 'Créé')&~Q(etat = 'Articles livrés')&~Q(etat = 'Demande d\'achat généré'))
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsNeedDemandeAchatByAuteur(services_ref_id, user_id):
        try:
            service_referent = dao_unite_fonctionnelle.toGetUniteFonctionnelle(services_ref_id)
            demandes = Model_Expression.objects.filter(services_ref_id = services_ref_id).filter(~Q(etat = 'Créé')&~Q(etat = 'Articles livrés')&~Q(etat = 'Demande d\'achat généré')).filter(auteur_id=user_id)
            return demandes
        except Exception as e:
            return None

    @staticmethod
    def toListExpressionsRecentes():
        try:
            demandes = Model_Expression.objects.all().order_by('-id')[:5]
            return demandes
        except Exception as e:
            return None


    @staticmethod
    def toListExpressionsRecentesByAuteur(user_id):
        try:
            demandes = Model_Expression.objects.filter(auteur_id=user_id).order_by('-id')[:5]
            return demandes
        except Exception as e:
            return None


    @staticmethod
    def toGenerateNumeroExpression():
        total_damandes = dao_expression_besoin.toListExpressions().count()
        total_damandes = total_damandes + 1
        temp_numero = str(total_damandes)

        for i in range(len(str(total_damandes)), 4):
            temp_numero = "0" + temp_numero

        mois = timezone.now().month
        if mois < 10: mois = "0%s" % mois

        temp_numero = "EXP%s%s%s" % (timezone.now().year, mois, temp_numero)
        return temp_numero


    @staticmethod
    def toCountExpression_Spec():
        try:
            article_livre = Model_Expression.objects.filter(etat="Articles livrés").count()
            demande_Achat_genere = Model_Expression.objects.filter(etat="Demande d'achat généré").count()
            livre_partiellement = Model_Expression.objects.filter(etat="Livré partiellement").count()
            envoye_au_DAFC = Model_Expression.objects.filter(etat="Envoyé au DAFC").count()
            approuve = Model_Expression.objects.filter(etat="Approuvé").count()
            cree = Model_Expression.objects.filter(etat="Créé")
            Lesarticleslivre = Model_Expression.objects.filter(etat="Articles livrés")
            #print(Lesarticleslivre)
            LesArticleApproue = Model_Expression.objects.filter(etat="Approuvé")
            #print(LesArticleApproue)
            lesExpressiondebesion = Model_Expression.objects.exclude(etat="Approuvé")
            #print(LesArticleApproue)

            return lesExpressiondebesion,Lesarticleslivre,LesArticleApproue,article_livre,demande_Achat_genere,livre_partiellement, envoye_au_DAFC,approuve,cree
        except Exception as e:
            #print("ERREUR ETAT EXPRESSION")
            return None

    @staticmethod
    def toListExpBesoinApprouve(user_id):
        try:
            Expbesions = Model_Expression.objects.exclude(etat="Approuvé").filter(~Q(etat = 'Créé')).filter(auteur_id=user_id)
            return Expbesions
        except Exception as e:
            return None

    @staticmethod
    def toListExpBesoinEnCours(user_id):
        try:
            excludes = ['Créé', 'Articles livrés']
            Expbesions = Model_Expression.objects.exclude(etat__in=excludes).filter(auteur_id=user_id)
            return Expbesions
        except Exception as e:
            return None

    @staticmethod
    def toCountExpression_SpecByAuteur(user_id):
        try:
            article_livre = Model_Expression.objects.filter(etat="Articles livrés").filter(auteur_id=user_id).count()
            demande_Achat_genere = Model_Expression.objects.filter(etat="Demande d'achat généré").filter(auteur_id=user_id).count()
            livre_partiellement = Model_Expression.objects.filter(etat="Livré partiellement").filter(auteur_id=user_id).count()
            envoye_au_DAFC = Model_Expression.objects.filter(etat="Envoyé au DAFC").filter(auteur_id=user_id).count()
            approuve = Model_Expression.objects.filter(etat="Approuvé").filter(auteur_id=user_id).count()

            cree = Model_Expression.objects.filter(etat="Créé").filter(auteur_id=user_id)

            Lesarticleslivre = Model_Expression.objects.filter(etat="Articles livrés").filter(auteur_id=user_id)
            #print(Lesarticleslivre)
            LesArticleApproue = Model_Expression.objects.filter(etat="Approuvé").filter(auteur_id=user_id)
            #print(LesArticleApproue)
            lesExpressiondebesion = Model_Expression.objects.exclude(etat="Envoyé au service référent").filter(auteur_id=user_id)
            #print(LesArticleApproue)

            return lesExpressiondebesion,Lesarticleslivre,LesArticleApproue,article_livre,demande_Achat_genere,livre_partiellement, envoye_au_DAFC,approuve,cree
        except Exception as e:
            #print("ERREUR ETAT EXPRESSION")
            return None

    @staticmethod
    def toListNumberExpressionbyMonth(today=timezone.now().year):
        try:
            ListSol = [0,0,0,0,0,0,0,0,0,0,0,0]
            ListeQuery =Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur')).filter(date_expression__year = today)
            for item in ListeQuery:

                if item["month"].month==1:

                    #ListSol.remove()
                    if item["total"] == 0:
                        ListSol[0] = 0
                    else:
                        ListSol[0] = item["total"]
                    continue
                elif item["month"].month==2:
                    if item["total"] == 0:
                        ListSol[1] = 0
                    else:
                        ListSol[1] = item["total"]
                    continue
                elif item["month"].month==3:
                    if item["total"] == 0:
                        ListSol[2] = 0
                    else:
                        ListSol[2] = item["total"]
                    continue
                elif item["month"].month==4:
                    if item["total"] == 0:
                        ListSol[3] = 0
                    else:
                        ListSol[3] = item["total"]
                    continue
                elif item["month"].month==5:
                    if item["total"] == 0:
                        ListSol[4] = 0
                    else:
                        ListSol[4] = item["total"]
                    continue
                elif item["month"].month==6:
                    if item["total"] == 0:
                        ListSol[5] = 0
                    else:
                        ListSol[5] = item["total"]
                    continue
                elif item["month"].month==7:
                    if item["total"] == 0:
                        ListSol[6] = 0
                    else:
                        ListSol[6] = item["total"]
                    continue
                elif item["month"].month==8:
                    if item["total"] == 0:
                        ListSol[7] = 0
                    else:
                        ListSol[7] = item["total"]
                    continue
                elif item["month"].month==9:
                    if item["total"] == 0:
                        ListSol[8] = 0
                    else:
                        ListSol[8] = item["total"]
                    continue
                elif item["month"].month==10:
                    if item["total"] == 0:
                        ListSol[9] = 0
                    else:
                        ListSol[9] = item["total"]
                    continue
                elif item["month"].month==11:
                    if item["total"] == 0:
                        ListSol[10] = 0
                    else:
                        ListSol[10] = item["total"]
                    continue
                elif item["month"].month==12:
                    if item["total"] == 0:
                        ListSol[11] = 0
                    else:
                        ListSol[11] = item["total"]
                    continue
                else:
                    pass
            return ListSol
        except Exception as e:
            #print("ERRER LISTEEXPRESSION BY MONTH WITHOUT USER ID")
            #print(e)
            pass


    @staticmethod
    def toListNumberExpressionbyMonthByAuteur(user_id, today=timezone.now().year):
        try:

            # ListeExpression = Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur'))
            ListSol = [0,0,0,0,0,0,0,0,0,0,0,0]
            ListeQuery =Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur')).filter(date_expression__year = today).filter(auteur_id=user_id)
            #print("Pour 2020 : {}".format(Model_Expression.objects.annotate(month=TruncMonth('date_expression')).values('month').annotate(total=Count('demandeur')).filter(date_expression__year = 2019)))
            for item in ListeQuery:
                if item["month"].month==1:
                    ListSol.remove()
                    if item["total"] == 0:
                        ListSol[0] = 0
                    else:
                        ListSol[0] = item["total"]
                    continue
                elif item["month"].month==2:
                    if item["total"] == 0:
                        ListSol[1] = 0
                    else:
                        ListSol[1] = item["total"]
                    continue
                elif item["month"].month==3:
                    if item["total"] == 0:
                        ListSol[2] = 0
                    else:
                        ListSol[2] = item["total"]
                    continue
                elif item["month"].month==4:
                    if item["total"] == 0:
                        ListSol[3] = 0
                    else:
                        ListSol[3] = item["total"]
                    continue
                elif item["month"].month==5:
                    if item["total"] == 0:
                        ListSol[4] = 0
                    else:
                        ListSol[4] = item["total"]
                    continue
                elif item["month"].month==6:
                    if item["total"] == 0:
                        ListSol[5] = 0
                    else:
                        ListSol[5] = item["total"]
                    continue
                elif item["month"].month==7:
                    if item["total"] == 0:
                        ListSol[6] = 0
                    else:
                        ListSol[6] = item["total"]
                    continue
                elif item["month"].month==8:
                    if item["total"] == 0:
                        ListSol[7] = 0
                    else:
                        ListSol[7] = item["total"]
                    continue
                elif item["month"].month==9:
                    if item["total"] == 0:
                        ListSol[8] = 0
                    else:
                        ListSol[8] = item["total"]
                    continue
                elif item["month"].month==10:
                    if item["total"] == 0:
                        ListSol[9] = 0
                    else:
                        ListSol[9] = item["total"]
                    continue
                elif item["month"].month==11:
                    if item["total"] == 0:
                        ListSol[10] = 0
                    else:
                        ListSol[10] = item["total"]
                    continue
                elif item["month"].month==12:
                    if item["total"] == 0:
                        ListSol[11] = 0
                    else:
                        ListSol[11] = item["total"]
                    continue
                else:
                    pass

            #print('Liste des expression %s' %ListSol)
            return ListSol
        except Exception as e:
            #print("ERRER LISTEEXPRESSION BY MONTH WITH USER ID")
            #print(e)
            pass
