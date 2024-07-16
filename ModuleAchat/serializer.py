from rest_framework import serializers
from ErpBackOffice import models
from ErpProject import settings

class CategorieArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Categorie
        fields = (
            '__all__'
        )

class UniteSerializer(serializers.ModelSerializer):
    categorie_unite = CategorieArticleSerializer()
    categorie = serializers.ReadOnlyField(source = 'categorie_unite.url')
    class Meta:
        model = models.Model_Unite
        fields = (
            '__all__'
        )

class ConditionReglementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_ConditionReglement
        fields = (
            '__all__'
        )

class WkfEtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Wkf_Etape
        fields = (
            '__all__'
        )

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Fournisseur
        fields = (
            '__all__'
        )

class DemandeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Employe
        fields = (
            '__all__'
        )

class BonReceptionSerializer(serializers.ModelSerializer):
    fournisseur = FournisseurSerializer()
    statut = WkfEtapeSerializer()
    four = serializers.ReadOnlyField(source = 'fournisseur.url')
    stat = serializers.ReadOnlyField(source = 'statut.label')
    date_reception = serializers.DateTimeField(format= settings.DATE_FORMAT, required = False)
    date_prevue = serializers.DateTimeField(format= settings.DATE_FORMAT, required = False)
    prix_total = serializers.ReadOnlyField()
    statut_achat = serializers.ReadOnlyField()
    status_paiement = serializers.ReadOnlyField()
    class Meta:
        model = models.Model_Bon_reception
        fields = (
            '__all__'
        )

class DemandeDAchatSerializer(serializers.ModelSerializer):
    demandeur = DemandeurSerializer()
    demandeur = serializers.ReadOnlyField(source = 'demandeur.url')
    class Meta:
        model = models.Model_Demande_achat
        fields = (
            '__all__'
        )