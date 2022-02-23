from real_estate_api.kupci.models import Kupci
from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class TestModelaEntitetaPonudeLokala:
    """Testitanje entiteta modela Ponude Lokala"""

    def test_da_li_je_jedna_ponuda_lokala_kreirana(self, nova_ponuda_lokala_fixture):
        """
        Test da li je jedna Ponuda Lokala kreirana u bazi. Treba da bude samo jedna.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
        ---
        @param nova_jedna_ponuda_lokala_fixture: Ponude Lokala
        """
        broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_from_db == 1

    def test_da_li_je_jedna_ponuda_lokala_kreirana_bez_ugovora(self, nova_jedna_ponuda_lokala_bez_ugovora_fixture):
        """
        Broj Ugovora se dodeljuje tek nakon sto Notar overi Ugovor, pa je
        inicijalno br. Ugovora 'null'.
        Test da li je jedna Ponuda Lokala kreirana u bazi bez broja ugovora.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_bez_ugovora_fixture
        ---
        @param nova_jedna_ponuda_lokala_bez_ugovora_fixture: Ponude Lokala
        """
        broj_ponuda_lokala_bez_ugovora_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_bez_ugovora_from_db == 1

    def test_provera_svih_polja_kreirane_ponude_lokala(self, nova_ponuda_lokala_fixture):
        """
        Testiranje kreiranja nove Ponude Lokala i provera podataka nakon kreiranja.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
        ---
        @param nova_jedna_ponuda_lokala_fixture: Ponude Lokala
        """
        ponuda_lokala_from_db = PonudeLokala.objects.all()

        id_ponude_lokala = ponuda_lokala_from_db[0].id_ponude_lokala
        kupac_lokala = ponuda_lokala_from_db[0].kupac_lokala
        lokali = ponuda_lokala_from_db[0].lokali
        cena_lokala_za_kupca = ponuda_lokala_from_db[0].cena_lokala_za_kupca
        napomena_ponude_lokala = ponuda_lokala_from_db[0].napomena_ponude_lokala
        broj_ugovora_lokala = ponuda_lokala_from_db[0].broj_ugovora_lokala
        datum_ugovora_lokala = ponuda_lokala_from_db[0].datum_ugovora_lokala
        status_ponude_lokala = ponuda_lokala_from_db[0].status_ponude_lokala
        nacin_placanja_lokala = ponuda_lokala_from_db[0].nacin_placanja_lokala
        odobrenje_kupovine_lokala = ponuda_lokala_from_db[0].odobrenje_kupovine_lokala
        klijent_prodaje_lokala = ponuda_lokala_from_db[0].klijent_prodaje_lokala

        assert nova_ponuda_lokala_fixture.id_ponude_lokala == id_ponude_lokala
        assert nova_ponuda_lokala_fixture.kupac_lokala == kupac_lokala
        assert nova_ponuda_lokala_fixture.lokali == lokali
        assert nova_ponuda_lokala_fixture.cena_lokala_za_kupca == cena_lokala_za_kupca
        assert nova_ponuda_lokala_fixture.napomena_ponude_lokala == napomena_ponude_lokala
        assert nova_ponuda_lokala_fixture.broj_ugovora_lokala == broj_ugovora_lokala
        assert nova_ponuda_lokala_fixture.datum_ugovora_lokala == datum_ugovora_lokala
        assert nova_ponuda_lokala_fixture.status_ponude_lokala == status_ponude_lokala
        assert nova_ponuda_lokala_fixture.nacin_placanja_lokala == nacin_placanja_lokala
        assert nova_ponuda_lokala_fixture.odobrenje_kupovine_lokala == odobrenje_kupovine_lokala
        assert nova_ponuda_lokala_fixture.klijent_prodaje_lokala == klijent_prodaje_lokala

    def test_ime_kupca_lokala_from_property_model_ponude_lokala(self, nova_ponuda_lokala_fixture):
        """
        Testiranje property polja 'ime_kupca_lokala' iz modela Ponude Lokala i uporedjivanje sa
        poljem iz fixture 'nova_jedna_ponuda_lokala_fixture'.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
        ---
        @param nova_jedna_ponuda_lokala_fixture: Ponude Lokala
        """
        # Uzmi ime_prezime Kupca iz table Kupci.
        ime_prezime_kupca_from_db = Kupci.objects.all().first().ime_prezime

        # Uzmi ime_prezime Kupca iz poperty polja modela Ponude Lokala.
        ime_prezime_kupca_iz_modela_ponude_lokala = nova_ponuda_lokala_fixture.ime_kupca_lokala

        assert ime_prezime_kupca_from_db == ime_prezime_kupca_iz_modela_ponude_lokala

    def test_adresa_lokala_from_property_model_ponude_lokala(self, nova_ponuda_lokala_fixture):
        """
        Testiranje property polja 'adresa_lokala' iz modela Ponude Lokala i uporedjivanje sa
        poljem iz fixture 'nova_jedna_ponuda_lokala_fixture'.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
        ---
        @param nova_jedna_ponuda_lokala_fixture: Ponude Lokala
        """
        # Uzmi 'adresa_lokala' iz table Lokali.
        adresa_lokala_from_db = Lokali.objects.all().first().adresa_lokala

        # Uzmi 'adresa_lokala' iz poperty polja modela Ponude Lokala.
        adresa_lokala_iz_modela_ponude_lokala = nova_ponuda_lokala_fixture.adresa_lokala

        assert adresa_lokala_from_db == adresa_lokala_iz_modela_ponude_lokala

    def test_lamela_lokala_from_property_model_ponude_lokala(self, nova_ponuda_lokala_fixture):
        """
        Testiranje property polja 'lamela_lokala' iz modela Ponude Lokala i uporedjivanje sa
        poljem iz fixture 'nova_jedna_ponuda_lokala_fixture'.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
        ---
        @param nova_jedna_ponuda_lokala_fixture: Ponude Lokala
        """
        # Uzmi 'lamela_lokala' vrednost iz tabele Lokali.
        lamela_lokala_from_db = Lokali.objects.all().first().lamela_lokala

        # Uzmi 'lamela_lokala' iz poperty polja modela Ponude Lokala.
        lamela_lokala_iz_modela_ponude_lokala = nova_ponuda_lokala_fixture.lamela_lokala

        assert lamela_lokala_from_db == lamela_lokala_iz_modela_ponude_lokala

    def test_cena_lokala_from_property_model_ponude_lokala(self, nova_ponuda_lokala_fixture):
        """
        Testiranje property polja 'cena_lokala' iz modela Ponude Lokala i uporedjivanje sa
        poljem iz fixture 'nova_jedna_ponuda_lokala_fixture'.

            * @see /test_ponude_lokala/conftest.py : nova_jedna_ponuda_lokala_fixture
        ---
        @param nova_jedna_ponuda_lokala_fixture: Ponude Lokala
        """
        # Uzmi 'cena_lokala' iz tabele Lokali.
        cena_lokala_from_db = Lokali.objects.all().first().cena_lokala

        # Uzmi 'cena_lokala' iz poperty polja modela Ponude Lokala.
        cena_lokala_iz_modela_ponude_lokala = nova_ponuda_lokala_fixture.cena_lokala

        assert cena_lokala_from_db == cena_lokala_iz_modela_ponude_lokala
