import pytest
from faker import Faker

from real_estate_api.kupci.models import Kupci

fake = Faker()


class TestEntitetaKupci:

    @pytest.mark.django_db(transaction=True)
    def test_create_novi_kupac(self, novi_kupac_fixture):
        kupac_from_db = Kupci.objects.all()
        lice = kupac_from_db[0].lice
        ime_prezime = kupac_from_db[0].ime_prezime
        email = kupac_from_db[0].email
        broj_telefona = kupac_from_db[0].broj_telefona
        Jmbg_Pib = kupac_from_db[0].Jmbg_Pib
        adresa = kupac_from_db[0].adresa

        assert novi_kupac_fixture.lice == lice
        assert novi_kupac_fixture.ime_prezime == ime_prezime
        assert novi_kupac_fixture.email == email
        assert novi_kupac_fixture.broj_telefona == broj_telefona
        assert novi_kupac_fixture.Jmbg_Pib == int(Jmbg_Pib)
        assert novi_kupac_fixture.adresa == adresa

    @pytest.mark.django_db(transaction=True)
    def test_kreiranje_novog_kupca(self, novi_kupac_fixture):
        assert Kupci.objects.all().count() == 1

    @pytest.mark.django_db(transaction=True)
    def test_filter_ime_prezime(self, novi_kupac_fixture):
        assert Kupci.objects.filter(ime_prezime=novi_kupac_fixture.ime_prezime).exists()

    @pytest.mark.django_db(transaction=True)
    def test_promeni_ime_prezime(self, novi_kupac_fixture):
        # Proveri prvo da li je ime_prezime iz fixtura 'ime_prezime'
        assert novi_kupac_fixture.ime_prezime == novi_kupac_fixture.ime_prezime

        novi_kupac_fixture.ime_prezime = 'Slobodan Tomic'
        novi_kupac_fixture.save()
        movo_ime_kupca = Kupci.objects.get(ime_prezime="Slobodan Tomic")

        assert movo_ime_kupca.ime_prezime == "Slobodan Tomic"

    @pytest.mark.django_db(transaction=True)
    def test_filter_lice(self, novi_kupac_fixture):
        assert Kupci.objects.filter(lice=novi_kupac_fixture.lice).exists()

    @pytest.mark.django_db(transaction=True)
    def test_promeni_lice(self, novi_kupac_fixture):
        # Proveri prvo da li je lice iz fixtura 'FIZICKO'
        assert novi_kupac_fixture.lice == "Fizicko"

        novi_kupac_fixture.lice = 'Pravno'
        novi_kupac_fixture.save()
        movo_lice_kupca = Kupci.objects.get(lice="Pravno")
        assert movo_lice_kupca.lice == "Pravno"

    @pytest.mark.django_db(transaction=True)
    def test_filter_email(self, novi_kupac_fixture):
        assert Kupci.objects.filter(email=novi_kupac_fixture.email).exists()

    @pytest.mark.django_db(transaction=True)
    def test_promeni_email(self, novi_kupac_fixture):
        # Proveri prvo da li je iz fixtura 'email'
        assert novi_kupac_fixture.email == novi_kupac_fixture.email

        novi_kupac_fixture.email = 'slobodan.tomic@factoryww.com'
        novi_kupac_fixture.save()
        movi_email_kupca = Kupci.objects.get(email="slobodan.tomic@factoryww.com")

        assert movi_email_kupca.email == "slobodan.tomic@factoryww.com"

    @pytest.mark.django_db(transaction=True)
    def test_filter_broj_telefona(self, novi_kupac_fixture):
        assert Kupci.objects.filter(broj_telefona=novi_kupac_fixture.broj_telefona).exists()

    @pytest.mark.django_db(transaction=True)
    def test_promeni_broj_telefona(self, novi_kupac_fixture):
        # Proveri prvo da li je iz fixtura 'broj_telefona'
        assert novi_kupac_fixture.broj_telefona == novi_kupac_fixture.broj_telefona

        novi_kupac_fixture.broj_telefona = '+381 66 9878 99 88'
        novi_kupac_fixture.save()
        movi_broj_telefona_kupca = Kupci.objects.get(broj_telefona='+381 66 9878 99 88')

        assert movi_broj_telefona_kupca.broj_telefona == '+381 66 9878 99 88'

    @pytest.mark.django_db(transaction=True)
    def test_filter_Jmbg_Pib(self, novi_kupac_fixture):
        assert Kupci.objects.filter(Jmbg_Pib=novi_kupac_fixture.Jmbg_Pib).exists()

    @pytest.mark.django_db(transaction=True)
    def test_promeni_Jmbg_Pib(self, novi_kupac_fixture):
        # Proveri prvo da li je iz fixtura 'Jmbg_Pib'
        assert novi_kupac_fixture.Jmbg_Pib == novi_kupac_fixture.Jmbg_Pib

        novi_kupac_fixture.Jmbg_Pib = '1110975800093'
        novi_kupac_fixture.save()
        movi_Jmbg_Pib_kupca = Kupci.objects.get(Jmbg_Pib='1110975800093')

        assert movi_Jmbg_Pib_kupca.Jmbg_Pib == '1110975800093'

    @pytest.mark.django_db(transaction=True)
    def test_filter_adresa(self, novi_kupac_fixture):
        assert Kupci.objects.filter(adresa=novi_kupac_fixture.adresa).exists()

    @pytest.mark.django_db(transaction=True)
    def test_promeni_adresa(self, novi_kupac_fixture):
        # Proveri prvo da li je iz fixtura 'Jmbg_Pib'
        assert novi_kupac_fixture.adresa == novi_kupac_fixture.adresa

        novi_kupac_fixture.adresa = 'Preradovićeva 23'
        novi_kupac_fixture.save()
        movi_adresa_kupca = Kupci.objects.get(adresa='Preradovićeva 23')

        assert movi_adresa_kupca.adresa == 'Preradovićeva 23'
