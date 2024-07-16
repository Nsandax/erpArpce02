from rest_framework import serializers
from ErpBackOffice import models
from ErpProject import settings


class PersonneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Personne
        fields = (
            '__all__'
        )

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Place
        fields = (
            '__all__'
        )

class TypeOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_TypeOrganisation
        fields = (
            '__all__'
        )

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Organisation
        fields = (
            '__all__'
        )

class UniteFonctionnelleSerializer(serializers.ModelSerializer):
    unite_fonctionnelle = "UniteFonctionnelleSerializer()"
    class Meta:
        model = models.Model_Unite_fonctionnelle
        fields = (
            '__all__'
        )

class ProfilRHSerializer(serializers.ModelSerializer):
    agent = PersonneSerializer()
    class Meta:
        model = models.Model_ProfilRH
        fields = (
            '__all__'
        )

class PosteSerializer(serializers.ModelSerializer):
    departement = UniteFonctionnelleSerializer()
    depart = serializers.ReadOnlyField(source = 'departement.url')
    class Meta:
        model = models.Model_Poste
        fields = (
            '__all__'
        )

class EmployeSerializer(serializers.ModelSerializer):
    unite_fonctionnelle  = UniteFonctionnelleSerializer()
    unite = serializers.ReadOnlyField(source = 'unite_fonctionnelle.designation')
    profilrh = ProfilRHSerializer()
    poste_str = serializers.ReadOnlyField()
    class Meta:
        model = models.Model_Employe
        fields = (
            '__all__'
        )

class DependantSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()
    class Meta:
        model = models.Model_Dependant
        fields = (
            '__all__'
        )

class PretSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()
    class Meta:
        model = models.Model_Pret
        fields = (
            '__all__'
        )

class PresenceSerializer(serializers.ModelSerializer):
    hisemploye = serializers.ReadOnlyField()
    hisunitefonctionnelle = serializers.ReadOnlyField()
    date = serializers.DateField(format = settings.DATE, required = False)
    arrive = serializers.TimeField(format= settings.HEURE, required = False)
    depart = serializers.TimeField(format= settings.HEURE, required = False)
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = models.Model_Presence
        fields = (
            '__all__'
        )

class TypeCongeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_active_str = serializers.ReadOnlyField()
    double_validation_str = serializers.ReadOnlyField()
    class Meta:
        model = models.Model_Type_conge
        fields = (
            '__all__'
        )

class CongeSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()
    empl = serializers.ReadOnlyField(source = 'employe.url')
    id = serializers.ReadOnlyField()
    hisemploye = serializers.ReadOnlyField()
    histypeconge = serializers.ReadOnlyField()
    date_from = serializers.DateTimeField(format = settings.DATE, required = False)
    date_to = serializers.DateTimeField(format = settings.DATE, required = False)
    class Meta:
        model = models.Model_Conge
        fields = (
            '__all__'
        )


class ModelVehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Vehicule_model
        fields = (
            '__all__'
        )

class VehiculeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    hisemploye = serializers.ReadOnlyField()
    hisvehiculemodel = serializers.ReadOnlyField()
    employe = EmployeSerializer()
    date_acquisition = serializers.DateTimeField(format=settings.DATE_FORMAT, required = False)
    class Meta:
        model = models.Model_Vehicule
        fields = (
            '__all__'
        )

class LotBulletinSerializer(serializers.ModelSerializer):
    departement = UniteFonctionnelleSerializer()

    class Meta:
        model = models.Model_LotBulletins
        fields =(
            '__all__'
        )

class BulletinSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()
    employe = serializers.ReadOnlyField(source = 'employe.url')
    lot = LotBulletinSerializer()
    lot = serializers.ReadOnlyField(source = 'lot.url')

    class Meta:
        model = models.Model_Bulletin
        fields = (
            '__all__'
        )

class TypeElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeElementBulletin
        fields = (
            '__all__'
        )

class CategorieElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategorieElementBulletin
        fields = (
            '__all__'
        )

class ElementBulletinSerializer(serializers.ModelSerializer):
    nom_categorie_element = serializers.ReadOnlyField()
    nom_type_element = serializers.ReadOnlyField()
    class Meta:
        model = models.Model_ElementBulletin
        fields = (
            '__all__'
        )

class ItemBulletinSerializer(serializers.ModelSerializer):
    element = ElementBulletinSerializer()
    bulletin = BulletinSerializer()
    class Meta:
        model = models.Model_ItemBulletin
        fields = (
            '__all__'
        )

class DeviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Devise
        fields = (
            '__all__'
        )

class BaremeSerializer(serializers.ModelSerializer):
    devise = DeviseSerializer()
    dev = serializers.ReadOnlyField(source = 'devise.url')
    auteur = PersonneSerializer()
    aut = serializers.ReadOnlyField(source = 'auteur.nom_complet')
    class Meta:
        model = models.Model_Bareme
        fields = (
            '__all__'
        )

class TrancheBareme(serializers.ModelSerializer):
    bareme = BaremeSerializer()
    devise = DeviseSerializer()

    class Meta:
        model = models.Model_TrancheBareme
        fields = (
            '__all__'
        )

class ProfilPayeSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()
    empl = serializers.ReadOnlyField(source = 'employe.url')
    poste = PosteSerializer()
    post = serializers.ReadOnlyField(source = 'poste.url')
    date_profil = serializers.DateTimeField(format=settings.DATE_FORMAT, required = False)

    class Meta:
        model = models.Model_ProfilPaye
        fields = (
            '__all__'
        )

class ItemProfilPaieSerializer(serializers.ModelSerializer):
    element = ElementBulletinSerializer()
    profil_paie = ProfilPayeSerializer()

    class Meta:
        model = models.Model_ItemProfilPaye
        fields = (
            '__all__'
        )

class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model_Compte
        fields = (
            '__all__'
        )

class OrdreSerializer(serializers.ModelSerializer):
    compte  = CompteSerializer()
    class Meta:
        fields = (
            '__all__'
        )