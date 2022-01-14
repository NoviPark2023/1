from rest_framework import serializers
from rest_framework.reverse import reverse

from real_estate_api.korisnici.views import Korisnici

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class KorisniciSerializers(serializers.ModelSerializer):
    """
    Detalji KORISNIKA sa redukovanim poljima koje poseduje za
    prikaz u tabeli i u slucaju responiva u frontendu.
        * Ukljucene API putanje (API URLs) su:
        ------------------------------------
        - detalji korisnika
        - uredjivanje korisnika
        - brisanje korisnika
        - lista_korisnika
        - kreiraj_korisnika
      """
    detalji_korisnika_url = serializers.SerializerMethodField()
    izmeni_korisnika_url = serializers.SerializerMethodField()
    obrisi_korisnika_url = serializers.SerializerMethodField()
    lista_korisnika_url = serializers.SerializerMethodField()
    kreiraj_korisnika_url = serializers.SerializerMethodField()

    class Meta:
        """
        Opisni model entiteta Korisnici sa ukljucenim poljim a ka opeacijama sa istim.
        * Ukljucena dodatna polja modela entiteta *(Lakse u Frontendu):
        -----------------------------------------
        - detalji_korisnika_url
        - izmeni_korisnika_url
        - obrisi_korisnika_url
        - lista_korisnika_url
        - kreiraj_korisnika_url
        """
        model = Korisnici
        fields = (
            "id",
            "ime",
            "prezime",
            "email",
            "username",
            "password",
            "role",
            # "last_login",
            "is_superuser",
            "is_staff",
            # "start_date",
            "about",
            "detalji_korisnika_url",
            "izmeni_korisnika_url",
            "obrisi_korisnika_url",
            "lista_korisnika_url",
            "kreiraj_korisnika_url"
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Prilikom kreiranja novok Korisnika mora da se lozinka hesuje, jer je potrebno za prijavu.

        :param validated_data:
        :return: Meta.model(**validated_data)
        """
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    @staticmethod
    def get_detalji_korisnika_url(obj):
        """Prosledi u API putanju do detalji kupca"""
        return reverse("korisnici:detalji_korisnika", args=[obj.pk])

    @staticmethod
    def get_izmeni_korisnika_url(obj):
        """Prosledi u API putanju do uredi kupca"""
        return reverse("korisnici:izmeni_korisnika", args=[obj.pk])

    def get_lista_korisnika_url(self, obj):
        return reverse("korisnici:lista_korisnika")

    def get_obrisi_korisnika_url(self, obj):
        """Prosledi u API putanju do obrisi kupca"""
        return reverse("korisnici:obrisi_korisnika", args=[obj.pk])

    def get_kreiraj_korisnika_url(self, obj):
        return reverse("korisnici:kreiraj_korisnika")


class DetaljiKorisnikaSerializers(serializers.ModelSerializer):
    """
    Detalji KORISNIKA sa redukovanim poljima koje poseduje za
    prikaz u tabeli i u slucaju responiva u frontendu.
        * Ukljucene API putanje (API URLs) su:
        ------------------------------------
        - detalji korisnika
        - uredjivanje korisnika
        - brisanje korisnika
        - lista_korisnika
        - kreiraj_korisnika
      """

    # Putanja do detalja Korisnika
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Korisnici
        fields = (
            "id",
            "password",
            "last_login",
            "username",
            "ime",
            "prezime",
            "email",
            "role",
            "date_joined",
            "absolute_url"
        )

    def get_absolute_url(self, obj):
        return reverse("korisnici:detalji_korisnika")


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
