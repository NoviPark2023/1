from faker import Faker

from real_estate_api.kupci.models import Kupci

fake = Faker()


class TestEntitetaKupci:
    """Testitanje entiteta Kupci"""

    def test_create_novi_kupac(self, novi_kupac_fixture):
        """
        Testiranje kreiranja novog Kupca i provera podataka nakon kreiranja.
            * @see conftest.py

        @param novi_kupac_fixture: entitet Kupci
        """
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

    def test_kreiranje_novog_kupca(self, novi_kupac_fixture):
        """
        Test da li je samo jedan Kupac kreiran u bazi.

        @param novi_kupac_fixture: Kupci
        """

        assert Kupci.objects.all().count() == 1

    def test_filter_ime_prezime(self, novi_kupac_fixture):
        """
        Testiranje Filtera po 'ime_prezime' polju.

        @param novi_kupac_fixture: Kupci
        """
        assert Kupci.objects.filter(ime_prezime=novi_kupac_fixture.ime_prezime).exists()

    def test_promeni_ime_prezime(self, novi_kupac_fixture):
        """
        Test Promena Imena i Prezimena, ali provo provera da li je u fixture ta vrednost.

        @param novi_kupac_fixture: Kupci
        """
        # Proveri prvo da li je ime_prezime iz fixtura 'ime_prezime'
        assert novi_kupac_fixture.ime_prezime == novi_kupac_fixture.ime_prezime

        novi_kupac_fixture.ime_prezime = 'Slobodan Tomic'
        novi_kupac_fixture.save()
        movo_ime_kupca = Kupci.objects.get(ime_prezime="Slobodan Tomic")

        assert movo_ime_kupca.ime_prezime == "Slobodan Tomic"

    def test_filter_lice(self, novi_kupac_fixture):
        """
        Testiranje Filtera po 'lice' polju.

        @param novi_kupac_fixture: Kupci
        """
        assert Kupci.objects.filter(lice=novi_kupac_fixture.lice).exists()

    def test_promeni_lice(self, novi_kupac_fixture):
        """
        Test Promena polja 'lice', ali provo provera da li je u fixture ta vrednost.

        @param novi_kupac_fixture: Kupci
        """

        # Proveri prvo da li je lice iz fixtura 'FIZICKO'
        assert novi_kupac_fixture.lice == "Fizicko"

        novi_kupac_fixture.lice = 'Pravno'
        novi_kupac_fixture.save()
        movo_lice_kupca = Kupci.objects.get(lice="Pravno")
        assert movo_lice_kupca.lice == "Pravno"

    def test_filter_email(self, novi_kupac_fixture):
        """
        Testiranje Filtera po 'email' polju.

        @param novi_kupac_fixture: Kupci
        """

        assert Kupci.objects.filter(email=novi_kupac_fixture.email).exists()

    def test_promeni_email(self, novi_kupac_fixture):
        """
        Test Promena polja 'email', ali provo provera da li je u fixture ta vrednost.

        @param novi_kupac_fixture: Kupci
        """

        # Proveri prvo da li je iz fixtura 'email'
        assert novi_kupac_fixture.email == novi_kupac_fixture.email

        novi_kupac_fixture.email = 'slobodan.tomic@factoryww.com'
        novi_kupac_fixture.save()
        movi_email_kupca = Kupci.objects.get(email="slobodan.tomic@factoryww.com")

        assert movi_email_kupca.email == "slobodan.tomic@factoryww.com"

    def test_filter_broj_telefona(self, novi_kupac_fixture):
        """
        Testiranje Filtera po 'broj_telefona' polju.

        @param novi_kupac_fixture: Kupci
        """

        assert Kupci.objects.filter(broj_telefona=novi_kupac_fixture.broj_telefona).exists()

    def test_promeni_broj_telefona(self, novi_kupac_fixture):
        """
        Test Promena polja 'broj_telefona', ali provo provera da li je u fixture ta vrednost.

        @param novi_kupac_fixture: Kupci
        """

        # Proveri prvo da li je iz fixtura 'broj_telefona'
        assert novi_kupac_fixture.broj_telefona == novi_kupac_fixture.broj_telefona

        novi_kupac_fixture.broj_telefona = '+381 66 9878 99 88'
        novi_kupac_fixture.save()
        movi_broj_telefona_kupca = Kupci.objects.get(broj_telefona='+381 66 9878 99 88')

        assert movi_broj_telefona_kupca.broj_telefona == '+381 66 9878 99 88'

    def test_filter_Jmbg_Pib(self, novi_kupac_fixture):
        """
        Testiranje Filtera po 'Jmbg_Pib' polju.

        @param novi_kupac_fixture: Kupci
        """

        assert Kupci.objects.filter(Jmbg_Pib=novi_kupac_fixture.Jmbg_Pib).exists()

    def test_promeni_Jmbg_Pib(self, novi_kupac_fixture):
        """
        Test Promena polja 'Jmbg_Pib', ali provo provera da li je u fixture ta vrednost.

        @param novi_kupac_fixture: Kupci
        """

        # Proveri prvo da li je iz fixtura 'Jmbg_Pib'
        assert novi_kupac_fixture.Jmbg_Pib == novi_kupac_fixture.Jmbg_Pib

        novi_kupac_fixture.Jmbg_Pib = '1110975800093'
        novi_kupac_fixture.save()
        movi_Jmbg_Pib_kupca = Kupci.objects.get(Jmbg_Pib='1110975800093')

        assert movi_Jmbg_Pib_kupca.Jmbg_Pib == '1110975800093'

    def test_filter_adresa(self, novi_kupac_fixture):
        """
        Testiranje Filtera po 'adresa' polju.

        @param novi_kupac_fixture: Kupci
        """

        assert Kupci.objects.filter(adresa=novi_kupac_fixture.adresa).exists()

    def test_promeni_adresa(self, novi_kupac_fixture):
        """
        Test Promena polja 'adresa', ali provo provera da li je u fixture ta vrednost.

        @param novi_kupac_fixture: Kupci
        """

        # Proveri prvo da li je iz fixtura 'Jmbg_Pib'
        assert novi_kupac_fixture.adresa == novi_kupac_fixture.adresa

        novi_kupac_fixture.adresa = 'Preradovićeva 23'
        novi_kupac_fixture.save()
        movi_adresa_kupca = Kupci.objects.get(adresa='Preradovićeva 23')

        assert movi_adresa_kupca.adresa == 'Preradovićeva 23'

    def test_delete_kupca_iz_bazepodataka(self, novi_kupac_fixture):
        """
        Test brisanja Kupca iz baze podataka.

        @param novi_kupac_fixture: Kupci
        """

        # Proveri prvo da li postoji kreiran Kupac u bazi.
        assert Kupci.objects.all().count() == 1

        Kupci.objects.get(id_kupca=novi_kupac_fixture.id_kupca).delete()

        assert Kupci.objects.all().count() == 0
