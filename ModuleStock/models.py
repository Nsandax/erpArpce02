# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ErpBackOffice.models import *

# Create your models here.

class Model_Entrepot(models.Model):
    designation              =   models.CharField(max_length = 255)
    designation_court        =   models.CharField(max_length = 255)
    est_principal            =   models.BooleanField(default=False)
    services_ref             =    models.ForeignKey("ErpBackOffice.Model_Unite_fonctionnelle", blank=True, null=True, on_delete = models.SET_NULL, default=None, related_name="services_referent_of_bt_Entrepot")
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_Entrpot_emplacement", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_Type_Emplacement(models.Model):
    designation              =   models.CharField(max_length = 255)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_Type_emplacement", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_EmplacementStock(models.Model):
    designation              =   models.CharField(max_length = 255)
    type                     =   models.ForeignKey(Model_Type_Emplacement, on_delete=models.CASCADE,related_name='type_emplacement')
    entrepot                 =   models.ForeignKey(Model_Entrepot, on_delete=models.CASCADE, blank=True, null=True, related_name='empl_entrepot')
    defaut                   =   models.BooleanField(default=False)
    visible                  =   models.BooleanField(default=True)
    couloir                  =   models.IntegerField(default=0)
    rayon                    =   models.IntegerField(default=0)
    hauteur                  =   models.IntegerField(default=0)
    is_racine                =   models.BooleanField(default = False)
    est_systeme              =   models.BooleanField(default = False)
    # parent                   =   models.ForeignKey("Model_EmplacementStock", on_delete = models.SET_NULL, related_name="emplacement_parent_ES", null = True, blank = True)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_emplacement_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.reference

    @property
    def reference(self):
        empl = self.designation

        try:
            ent = self.entrepot.designation_court
            empl = ent + '/' + empl
        except Exception as e:
            pass

        return empl


class Model_Stockage(models.Model):
    emplacement              =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, related_name="emplacement_stock_stockage")
    article                  =   models.ForeignKey(Model_Article,on_delete=models.CASCADE, related_name="article_stock_stockage")
    quantite                 =   models.FloatField(default=0.0)
    unite                    =   models.ForeignKey(Model_Unite,on_delete=models.SET_NULL, blank=True, null=True, related_name="unite_stock_stockage")
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_stockage_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.emplacement.designation + " / "+ self.article.designation


class Model_Type_Operation_Stock(models.Model):
    designation              =   models.CharField(max_length = 50)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_type_op_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_Statut_Operation_stock(models.Model):
    designation              =   models.CharField(max_length = 50)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_statut_operation_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.designation


class Model_Operation_Stock(models.Model):
    numero                   =   models.CharField(max_length = 100)
    date                     =   models.DateTimeField(auto_now_add=True)
    type                     =   models.ForeignKey(Model_Type_Operation_Stock, on_delete=models.CASCADE, related_name="type_op_stock")
    emplacement              =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, related_name="op_stock_empl_source")
    emplacement_destination  =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, blank=True, null=True, related_name="op_stock_empl_dest")
    document                 =   models.CharField(max_length = 25, blank=True, null=True)
    statut                   =   models.ForeignKey("Model_Statut_Operation_stock", on_delete=models.SET_NULL, blank=True, null=True, related_name="statut_op_stock_op")
    # bon_achat                       =   models.ForeignKey('App_Achat.Model_Demande', on_delete = models.SET_NULL, related_name="bon_achat_op_stock", null = True, blank = True)
    # bon_vente                       =   models.ForeignKey('App_Vente.Model_Devis', on_delete = models.SET_NULL, related_name="bon_vente_op_stock", null = True, blank = True)
    operation_parent         =   models.ForeignKey("Model_Operation_Stock", on_delete=models.SET_NULL, blank=True, null=True, related_name="operation_stock_parent")
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_op_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)


    def __str__(self):
        return self.numero



class Model_Ligne_Operation_Stock(models.Model):
    operation                =   models.ForeignKey(Model_Operation_Stock, on_delete=models.CASCADE, related_name="ligne_op_stock")
    article                  =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="ligne_op_stock_article")
    series                   =   models.ManyToManyField(Model_Asset)
    quantite_demandee        =   models.FloatField()
    quantite_fait            =   models.FloatField(blank=True, null=True, default=0)
    prix_unitaire            =   models.FloatField(blank=True, null=True, default=0)
    unite                    =   models.ForeignKey(Model_Unite, on_delete=models.SET_NULL,blank=True, null=True, related_name="unite_op_stock")
    devise                   =   models.ForeignKey(Model_Devise, on_delete=models.SET_NULL, blank=True, null=True, related_name="devise_op_stock")
    description              =   models.CharField(max_length = 255, blank=True, null=True)
    fait                     =   models.BooleanField(default=False)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ligne_operation_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.operation.numero + " / " + self.article.designation

    @property
    def total(self):
        return self.prix_unitaire * self.quantite

    @property
    def quantite_restante(self):
        return self.quantite_demandee - self.quantite_fait

class Model_Type_Mvt_Stock(models.Model):
    designation             =   models.CharField(max_length = 20)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_type_mvt_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation

class Model_Mvt_Stock(models.Model):
    date                     =   models.DateTimeField(auto_now_add=True)
    type                     =   models.ForeignKey(Model_Type_Mvt_Stock, on_delete=models.CASCADE, related_name='type_mvt_stock')
    article                  =   models.ForeignKey(Model_Article,on_delete=models.CASCADE, related_name="mvt_article_stock")
    series                   =   models.ManyToManyField(Model_Asset)
    emplacement              =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, related_name="mvt_stock")
    operation                =   models.ForeignKey(Model_Operation_Stock, on_delete=models.CASCADE, blank=True, null=True, related_name="operation_mvt_stock")
    ajustement               =   models.ForeignKey("Model_Ajustement", on_delete=models.CASCADE, blank=True, null=True, related_name="ajustement_mvt_stock")
    rebut                    =   models.ForeignKey("Model_Rebut", on_delete=models.CASCADE, blank=True, null=True, related_name="rebut_mvt_stock")
    document                 =   models.CharField(max_length =255, blank=True, null=True)
    quantite_initiale        =   models.FloatField()
    unite_initiale           =   models.ForeignKey(Model_Unite, on_delete=models.SET_NULL,blank=True, null=True, related_name="mvt_unte_initiale_stock")
    quantite                 =   models.FloatField()
    unite                    =   models.ForeignKey(Model_Unite, on_delete=models.SET_NULL,blank=True, null=True, related_name="mvt_unte_stock")
    est_fabrication          =   models.BooleanField(default=False)
    est_destruction          =   models.BooleanField(default=False)
    est_ajustement           =   models.BooleanField(default=False)
    est_rebut                =   models.BooleanField(default=False)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_mtv_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.article.designation + ' / ' + str(self.quantite)


class Model_Rebut(models.Model):
    numero                   =   models.CharField(max_length=25)
    date                     =   models.DateTimeField(auto_now_add=True)
    article                  =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, related_name="rebut_article")
    serie_article            =   models.ForeignKey(Model_Asset, on_delete=models.SET_NULL, blank=True, null=True, related_name="serie_rebut")
    quantite                 =   models.FloatField()
    unite                    =   models.ForeignKey(Model_Unite, on_delete=models.SET_NULL, blank=True, null=True, related_name="unite_rebut")
    emplacement              =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, related_name="emplacement_rebut")
    emplacement_rebut        =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, related_name="emplacement_rebut_destination")
    document                 =   models.CharField(max_length=25, blank=True, null=True)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_rebut_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.numero


class Model_Statut_Ajustement(models.Model):
    designation             =   models.CharField(max_length = 100)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_statut_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.designation


class Model_Ajustement(models.Model):
    reference                =   models.CharField(max_length = 100)
    date                     =   models.DateTimeField(auto_now_add=True)
    emplacement              =   models.ForeignKey(Model_EmplacementStock, on_delete=models.CASCADE, related_name="emplacement_ajustement")
    statut                   =   models.ForeignKey(Model_Statut_Ajustement, on_delete=models.CASCADE, related_name="statut_ajustement")
    inventaire_de            =   models.IntegerField(blank=True, null=True)
    document                 =   models.CharField(max_length = 100, blank=True, null=True)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ajustement_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.reference

    def numero(self):
        return "INV-%05d" % (self.pk,)


class Model_Ligne_Ajustement(models.Model):
    ajustement               =   models.ForeignKey(Model_Ajustement, on_delete=models.CASCADE, related_name="ligne_ajustement")
    article                  =   models.ForeignKey(Model_Article, on_delete=models.CASCADE, blank=True, null=True, related_name="ligne_ajustement_article")
    series                   =   models.ManyToManyField(Model_Asset)
    quantite_theorique       =   models.FloatField()
    quantite_reelle          =   models.FloatField(blank=True, null=True, default=0)
    unite                    =   models.ForeignKey(Model_Unite, on_delete=models.SET_NULL,blank=True, null=True, related_name="ligne_ajustement_unite")
    fait                     =   models.BooleanField(default=False)
    statut                   =    models.ForeignKey("ErpBackOffice.Model_Wkf_Etape", on_delete=models.SET_NULL, blank=True, null=True)
    etat                     =    models.CharField(max_length=50, blank=True, null=True)
    creation_date            =    models.DateTimeField(auto_now = True)
    update_date              =    models.DateTimeField(auto_now=True)
    auteur                   =    models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_ligne_ajustement_stock", null = True, blank = True)
    url                      =    models.CharField(max_length = 250, blank=True, null=True)

    def __str__(self):
        return self.ajustement.reference
