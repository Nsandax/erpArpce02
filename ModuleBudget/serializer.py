from rest_framework import serializers
from ModuleAchat import serializer as seri
from ModuleRessourcesHumaines import serializer as seria
from ErpBackOffice import models
from ErpProject import settings


class BudgetSerializer(serializers.ModelSerializer):
    unite_fonctionnelle = seria.UniteFonctionnelleSerializer()
    departement = serializers.ReadOnlyField(source = 'unite_fonctionnelle.url')
    #date_debut = serializers.DateTimeField()
    class Meta:
        model = models.Model_Budget
        fields = (
            '__all__'
        )

class LigneBudgetaireSerializer(serializers.ModelSerializer):
    budget = BudgetSerializer()
    bud = serializers.ReadOnlyField(source = 'budget.url')
    responsable = seria.EmployeSerializer()
    resp = serializers.ReadOnlyField(source = 'responsable.url')
    class Meta:
        model = models.Model_LigneBudgetaire
        fields = (
            '__all__'
        )



