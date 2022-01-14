from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi, AzuriranjeCena


class ListaPonudaStanaSerializer(serializers.ModelSerializer):
    """
    Listing 'Ponuda' for every 'Stan'
    """
    detalji_kupca_url = serializers.SerializerMethodField()
    detalji_ponude_url = serializers.SerializerMethodField()

    datum_ugovora = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])
    adresa_stana = serializers.ReadOnlyField()  # Get field 'Adresa Stana' from 'Ponuda' model
    cena_stana = serializers.ReadOnlyField()  # Get field 'Cena Stana' from 'Ponuda' model

    class Meta:
        model = Ponude
        fields = (
            "id_ponude",
            "stan_id",
            "kupac",
            "ime_kupca",
            'adresa_stana',
            'cena_stana',
            "cena_stana_za_kupca",
            "napomena",
            "broj_ugovora",
            "datum_ugovora",
            "status_ponude",
            "nacin_placanja",
            'odobrenje',
            "detalji_kupca_url",
            "detalji_ponude_url",
        )

    def get_detalji_kupca_url(self, obj):
        """Prosledi u API putanju do detalja kupca stana"""
        return reverse("kupci:detalji_kupca", args=[obj.kupac.id_kupca])

    def get_detalji_ponude_url(self, obj):
        """Prosledi u API putanju do detalja ponude"""
        return reverse("ponude:detalji_ponude", args=[obj.id_ponude])


class StanoviSerializer(serializers.ModelSerializer):
    """
    Detalji STANA sa redukovanim poljima koje poseduje za prikaz u tabeli
    i u slucaju responiva u frontendu.
    Ukljucene API putanje (API URLs) su:
    ------------------------------------
    * detalji stana
    * uredjivanje stana
    * brisanje stana
    """

    detalji_stana_url = serializers.SerializerMethodField()
    izmeni_stan_url = serializers.SerializerMethodField()
    obrisi_stan_url = serializers.SerializerMethodField()
    kreiraj_stan_url = serializers.SerializerMethodField()

    # Inline lista ponuda stana
    lista_ponuda_stana = ListaPonudaStanaSerializer(many=True, read_only=True)
    # Ukupan broj Ponuda za jedan Stan
    broj_ponuda_za_stan = serializers.SerializerMethodField()

    class Meta:
        model = Stanovi
        fields = (
            "id_stana",
            "lamela",
            "adresa_stana",
            "kvadratura",
            "kvadratura_korekcija",
            "iznos_za_korekciju_kvadrature",
            "sprat",
            "broj_soba",
            "orijentisanost",
            "broj_terasa",
            "cena_stana",
            "cena_kvadrata",
            "napomena",
            "status_prodaje",
            "broj_ponuda_za_stan",
            'lista_ponuda_stana',
            'detalji_stana_url',
            'izmeni_stan_url',
            'obrisi_stan_url',
            'kreiraj_stan_url',
        )

    @staticmethod
    def get_broj_ponuda_za_stan(obj):
        """
        Ukupan broj ponuda za svaki stan. Suma ponuda jednog stana.
        :param obj: ForeignKey in Stanovi ka Ponudi
        :return: ukupan broj Ponuda za jedan Stan
        """
        broj_ponuda_stanovi = Ponude.objects.select_related('stan').filter(stan_id=obj.id_stana).count()
        return broj_ponuda_stanovi

    def get_detalji_stana_url(self, obj):
        """Prosledi u API putanju do detalji stana"""
        return reverse("stanovi:detalji_stana", args=[obj.pk])

    def get_izmeni_stan_url(self, obj):
        """Prosledi u API putanju do uredi stan"""
        return reverse("stanovi:izmeni_stan", args=[obj.pk])

    def get_obrisi_stan_url(self, obj):
        """Prosledi u API putanju do obrisi stan"""
        return reverse("stanovi:obrisi_stan", args=[obj.pk])

    def get_kreiraj_stan_url(self, obj):
        return reverse("stanovi:kreiraj_stan")


class BrojPonudaStanaPoMesecimaSerializer(serializers.ModelSerializer):
    """
    Ukupan broj Ponuda za svaki stan po MESECIMA.
    """

    class Meta:
        model = Ponude
        fields = (
            "id_ponude",
        )


class AzuriranjeCenaSerializer(serializers.ModelSerializer):
    """ Automatska kalkulacija cene Stanova serializers """

    class Meta:
        model = AzuriranjeCena
        fields = (
            "id_azur_cene",
            "sprat",
            "broj_soba",
            "orijentisanost",
            "cena_kvadrata",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Pored Tokena Vrati i podatke o Korisniku"""

    def validate(self, attrs):
        """
        Kada se generise Token, potrebno je i vratiti neke podatke o Korisniku.
        Ovo je potrebno da bi se u Frontu odredio kakav ce meni biti, tj.
        odredjivanje privilegija korisnika sistema na osnovu polja 'ROLE'.
        Ako je npr. Role: Administrator, on sve vidi u CRM sistemu.
        Ako je Role: Prodavac, ovaj tip ne sme da vidi neke stvari u Frontu.
        ---
        @param attrs: Atributi Korisnika JWT.
        @return: data_korisnika_sa_tokenom: Korisnik podaci sa Tokenom.
        """
        # The default result (access/refresh tokens)
        data_korisnika_sa_tokenom = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        # Custom data for Korisnika
        data_korisnika_sa_tokenom.update({'id': self.user.id})
        data_korisnika_sa_tokenom.update({'username': self.user.username})
        data_korisnika_sa_tokenom.update({'role': self.user.role})
        data_korisnika_sa_tokenom.update({'email': self.user.email})
        data_korisnika_sa_tokenom.update({'ime': self.user.ime})
        data_korisnika_sa_tokenom.update({'prezime': self.user.prezime})
        data_korisnika_sa_tokenom.update({'about': self.user.about})
        data_korisnika_sa_tokenom.update({'is_superuser': self.user.is_superuser})
        data_korisnika_sa_tokenom.update({'is_staff': self.user.is_staff})
        data_korisnika_sa_tokenom.update({'is_active': self.user.is_active})

        return data_korisnika_sa_tokenom
