from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class TestModelaEntitetaPonude:
    """Testitanje entiteta modela Ponude"""

    def test_da_li_je_jedna_ponuda_kreirana(self, nova_jedna_ponuda):
        """
        Test da li je samo jedana Ponuda kreirana u bazi. Trenutno je samo jedna
        Ponuda kreirana.

            * @see /test_ponude/conftest.py : nova_jedna_ponuda
        ---
        @param nova_jedna_ponuda: Ponude
        """

        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 1

    def test_provera_polja_novo_kreirane_ponude(self, nova_jedna_ponuda):
        """
        Testiranje kreiranja nove jedne Ponude i provera podataka nakon kreiranja.

            * @see /test_ponude/conftest.py : nova_jedna_ponuda
        ---
        @param nova_jedna_ponuda: Ponude
        """

        ponuda_from_db = Ponude.objects.all()

        id_ponude = ponuda_from_db[0].id_ponude
        kupac = ponuda_from_db[0].kupac
        stan = ponuda_from_db[0].stan
        klijent_prodaje = ponuda_from_db[0].klijent_prodaje
        cena_stana_za_kupca = ponuda_from_db[0].cena_stana_za_kupca
        napomena = ponuda_from_db[0].napomena
        broj_ugovora = ponuda_from_db[0].broj_ugovora
        datum_ugovora = ponuda_from_db[0].datum_ugovora
        status_ponude = ponuda_from_db[0].status_ponude
        nacin_placanja = ponuda_from_db[0].nacin_placanja
        odobrenje = ponuda_from_db[0].odobrenje

        assert nova_jedna_ponuda.id_ponude == id_ponude
        assert nova_jedna_ponuda.kupac == kupac
        assert nova_jedna_ponuda.stan == stan
        assert nova_jedna_ponuda.klijent_prodaje == klijent_prodaje
        assert nova_jedna_ponuda.cena_stana_za_kupca == cena_stana_za_kupca
        assert nova_jedna_ponuda.napomena == napomena
        assert nova_jedna_ponuda.broj_ugovora == broj_ugovora
        assert nova_jedna_ponuda.datum_ugovora == datum_ugovora
        assert nova_jedna_ponuda.status_ponude == status_ponude
        assert nova_jedna_ponuda.nacin_placanja == nacin_placanja
        assert nova_jedna_ponuda.odobrenje == odobrenje

    def test_ime_kupca_from_propery_model_ponude(self, nova_jedna_ponuda):
        """
        Testiranje property polja 'ime_kupca' iz modela Ponude i uporedjivanje sa
        poljem iz fixtura 'nova_jedna_ponuda'.

            * @see /test_ponude/conftest.py : nova_jedna_ponuda
        ---
        @param nova_jedna_ponuda: Ponude
        """

        # Uzmi ime_prezime Kupca iz table Kupci.
        ime_prezime_kupca_from_db = Kupci.objects.all().first().ime_prezime

        # Uzmi ime_prezime Kupca iz poperty polja modela Ponude.
        ime_prezime_kupca_iz_modela_ponude = nova_jedna_ponuda.ime_kupca

        assert ime_prezime_kupca_from_db == ime_prezime_kupca_iz_modela_ponude

    def test_adresa_stana_from_propery_model_ponude(self, nova_jedna_ponuda):
        """
        Testiranje property polja 'adresa_stana' iz modela Ponude i uporedjivanje sa
        poljem iz fixtura 'nova_jedna_ponuda'.

            * @see /test_ponude/conftest.py : nova_jedna_ponuda
        ---
        @param nova_jedna_ponuda: Ponude
        """

        # Uzmi ime_prezime Kupca iz table Kupci.
        adresa_stana_from_db = Stanovi.objects.all().first().adresa_stana

        # Uzmi 'ime_prezime' Kupca iz poperty polja modela Ponude.
        adresa_stana_iz_modela_ponude = nova_jedna_ponuda.adresa_stana

        assert adresa_stana_from_db == adresa_stana_iz_modela_ponude

    def test_cena_stana_from_propery_model_ponude(self, nova_jedna_ponuda):
        """
        Testiranje property polja 'cena_stana' iz modela Ponude i uporedjivanje sa
        poljem iz fixtura 'nova_jedna_ponuda'.

            * @see /test_ponude/conftest.py : nova_jedna_ponuda
        ---
        @param nova_jedna_ponuda: Ponude
        """

        # Uzmi cenu stana iz table Stanovi.
        cena_stana_from_db = Stanovi.objects.all().first().cena_stana

        # Uzmi 'cena_stana' iz poperty polja modela Ponude.
        cena_stana_iz_modela_ponude = nova_jedna_ponuda.cena_stana

        assert cena_stana_from_db == cena_stana_iz_modela_ponude

    def test_lamela_stana_from_propery_model_ponude(self, nova_jedna_ponuda):
        """
        Testiranje property polja 'lamela_stana' iz modela Ponude i uporedjivanje sa
        poljem iz fixtura 'nova_jedna_ponuda'.

            * @see /test_ponude/conftest.py : nova_jedna_ponuda
        ---
        @param nova_jedna_ponuda: Ponude
        """

        # Uzmi 'lamela' vrednost iz table Stanovi.
        lamela_stana_from_db = Stanovi.objects.all().first().lamela

        # Uzmi 'lamela_stana' iz poperty polja modela Ponude.
        lamela_stana_iz_modela_ponude = nova_jedna_ponuda.lamela_stana

        assert lamela_stana_from_db == lamela_stana_iz_modela_ponude
